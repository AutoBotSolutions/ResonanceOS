"""
FastAPI server for ResonanceOS
"""

import asyncio
from typing import List, Optional, Dict, Any
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..core.types import (
    StyleProfile, GenerationConfig, GenerationResult, APIResponse,
    ProfileRequest, GenerationRequest, SimilarityMethod
)
from ..core.config import get_config
from ..core.logging import get_logger, log_api_request
from ..profiling.corpus_loader import CorpusLoader
from ..profiling.style_vector_builder import StyleVectorBuilder
from ..profiling.profile_persistence import ProfilePersistence
from ..generation.adaptive_writer import AdaptiveWriter
from ..evolution.tone_evolver import ToneEvolver

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ResonanceOS API",
    description="Adaptive Stylistic Alignment Engine",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
config = get_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components
corpus_loader = CorpusLoader()
vector_builder = StyleVectorBuilder()
profile_persistence = ProfilePersistence()
adaptive_writer = AdaptiveWriter()
tone_evolver = ToneEvolver()


# Pydantic models for API
class ProfileCreateRequest(BaseModel):
    name: str = Field(..., description="Profile name")
    corpus_path: str = Field(..., description="Path to corpus files")
    description: Optional[str] = Field(None, description="Profile description")
    tier: int = Field(default=1, ge=1, le=3, description="Analysis tier")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProfileResponse(BaseModel):
    name: str
    description: Optional[str]
    resonance_vector: List[float]
    confidence: float
    created_at: str
    updated_at: str


class GenerationResponse(BaseModel):
    content: str
    similarity_score: float
    corrections_made: int
    generation_time: float
    tokens_generated: int
    status: str


class SimilarityRequest(BaseModel):
    profile1_name: str = Field(..., description="First profile name")
    profile2_name: str = Field(..., description="Second profile name")
    method: SimilarityMethod = Field(default=SimilarityMethod.COSINE)


class SimilarityResponse(BaseModel):
    similarity_score: float
    method: str
    profile1_name: str
    profile2_name: str


class EvolutionRequest(BaseModel):
    profile_name: str = Field(..., description="Profile to evolve")
    target_topics: List[str] = Field(..., description="Target topics for optimization")
    generations: int = Field(default=100, ge=10, le=1000)
    population_size: int = Field(default=50, ge=10, le=200)


class EvolutionResponse(BaseModel):
    evolved_profile_name: str
    generations_completed: int
    final_fitness: float
    fitness_improvement: float


# Dependency functions
async def get_profile_by_name(profile_name: str) -> StyleProfile:
    """Get profile by name or raise HTTPException"""
    profile = profile_persistence.load_profile_by_name(profile_name)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile '{profile_name}' not found")
    return profile


# Health check endpoint
@app.get("/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint"""
    return APIResponse(
        success=True,
        message="ResonanceOS API is healthy",
        data={"status": "healthy", "version": "0.1.0"}
    )


# Profile management endpoints
@app.post("/profiles", response_model=APIResponse)
async def create_profile(request: ProfileCreateRequest):
    """Create a new style profile from corpus"""
    
    try:
        # Load corpus
        documents = corpus_loader.load_corpus(request.corpus_path)
        
        if not documents:
            raise HTTPException(status_code=400, detail="No documents found in corpus")
        
        # Build resonance vector
        vector_builder.set_tier(request.tier)
        resonance_vector = vector_builder.build_vector(documents)
        
        # Create profile
        profile = StyleProfile(
            name=request.name,
            description=request.description,
            resonance_vector=resonance_vector,
            emotional_curve=[0.5] * 5,  # Default emotional curve
            cadence_pattern=[0.5] * 4,  # Default cadence pattern
            abstraction_preference=0.5,  # Neutral abstraction
            metadata=request.metadata
        )
        
        # Save profile
        profile_persistence.save_profile(profile)
        
        return APIResponse(
            success=True,
            message=f"Profile '{request.name}' created successfully",
            data={
                "profile_name": profile.name,
                "confidence": resonance_vector.confidence,
                "documents_analyzed": len(documents),
                "tier": request.tier
            }
        )
        
    except Exception as e:
        logger.error(f"Profile creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profiles", response_model=APIResponse)
async def list_profiles():
    """List all available profiles"""
    
    try:
        profiles = profile_persistence.list_profiles()
        
        profile_list = []
        for profile_info in profiles:
            profile_list.append({
                "name": profile_info["name"],
                "description": profile_info.get("description"),
                "confidence": profile_info.get("confidence", 0.0),
                "created_at": profile_info.get("created_at"),
                "format": profile_info.get("format", "json")
            })
        
        return APIResponse(
            success=True,
            message=f"Found {len(profile_list)} profiles",
            data={"profiles": profile_list}
        )
        
    except Exception as e:
        logger.error(f"Profile listing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profiles/{profile_name}", response_model=APIResponse)
async def get_profile(profile_name: str):
    """Get profile details"""
    
    try:
        profile = await get_profile_by_name(profile_name)
        
        return APIResponse(
            success=True,
            message=f"Profile '{profile_name}' retrieved",
            data={
                "name": profile.name,
                "description": profile.description,
                "resonance_vector": profile.resonance_vector.values,
                "dimensions": profile.resonance_vector.dimensions,
                "confidence": profile.resonance_vector.confidence,
                "emotional_curve": profile.emotional_curve,
                "cadence_pattern": profile.cadence_pattern,
                "abstraction_preference": profile.abstraction_preference,
                "created_at": profile.created_at.isoformat(),
                "updated_at": profile.updated_at.isoformat(),
                "metadata": profile.metadata
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/profiles/{profile_name}", response_model=APIResponse)
async def delete_profile(profile_name: str):
    """Delete a profile"""
    
    try:
        success = profile_persistence.delete_profile(profile_name)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Profile '{profile_name}' not found")
        
        return APIResponse(
            success=True,
            message=f"Profile '{profile_name}' deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile deletion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Generation endpoints
@app.post("/generate", response_model=APIResponse)
async def generate_text(request: GenerationRequest):
    """Generate text with style alignment"""
    
    try:
        # Get profile
        profile = await get_profile_by_name(request.profile_name)
        
        # Create generation config
        generation_config = GenerationConfig(
            topic=request.topic,
            target_profile=profile,
            max_tokens=request.max_tokens,
            similarity_threshold=request.similarity_threshold,
            temperature=0.7,  # Default temperature
            enable_feedback=True,
            enable_drift_detection=True
        )
        
        # Generate text
        result = await adaptive_writer.generate_article(generation_config)
        
        return APIResponse(
            success=True,
            message="Text generated successfully",
            data={
                "content": result.content,
                "similarity_score": result.metrics.similarity_score,
                "target_similarity": result.metrics.target_similarity,
                "corrections_made": result.corrections_made,
                "generation_time": result.generation_time,
                "tokens_generated": result.tokens_generated,
                "status": result.status.value,
                "drift_rate": result.metrics.drift_rate,
                "profile_used": result.profile_used.name
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/batch", response_model=APIResponse)
async def generate_batch(requests: List[GenerationRequest]):
    """Generate multiple texts in batch"""
    
    try:
        from ..generation.adaptive_writer import BatchGenerator
        
        # Create generation configs
        configs = []
        for req in requests:
            profile = await get_profile_by_name(req.profile_name)
            config = GenerationConfig(
                topic=req.topic,
                target_profile=profile,
                max_tokens=req.max_tokens,
                similarity_threshold=req.similarity_threshold,
                enable_feedback=True,
                enable_drift_detection=True
            )
            configs.append(config)
        
        # Generate batch
        batch_generator = BatchGenerator(adaptive_writer)
        results = await batch_generator.generate_batch(configs)
        
        # Format results
        batch_results = []
        for result in results:
            batch_results.append({
                "content": result.content,
                "similarity_score": result.metrics.similarity_score,
                "corrections_made": result.corrections_made,
                "generation_time": result.generation_time,
                "tokens_generated": result.tokens_generated,
                "status": result.status.value,
                "profile_used": result.profile_used.name
            })
        
        return APIResponse(
            success=True,
            message=f"Generated {len(batch_results)} texts",
            data={
                "results": batch_results,
                "statistics": batch_generator.get_batch_statistics()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Similarity endpoints
@app.post("/similarity", response_model=APIResponse)
async def calculate_similarity(request: SimilarityRequest):
    """Calculate similarity between two profiles"""
    
    try:
        # Get profiles
        profile1 = await get_profile_by_name(request.profile1_name)
        profile2 = await get_profile_by_name(request.profile2_name)
        
        # Calculate similarity
        from ..similarity.metrics import SimilarityCalculator
        calculator = SimilarityCalculator(request.method)
        similarity = calculator.calculate_similarity(
            profile1.resonance_vector, 
            profile2.resonance_vector
        )
        
        return APIResponse(
            success=True,
            message="Similarity calculated",
            data={
                "similarity_score": similarity,
                "method": request.method.value,
                "profile1_name": request.profile1_name,
                "profile2_name": request.profile2_name
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Similarity calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Evolution endpoints
@app.post("/evolution", response_model=APIResponse)
async def evolve_profile(request: EvolutionRequest):
    """Evolve a profile to improve performance"""
    
    try:
        # Get profile
        profile = await get_profile_by_name(request.profile_name)
        
        # Configure evolver
        from ..evolution.tone_evolver import EvolutionConfig
        evolution_config = EvolutionConfig(
            generations=request.generations,
            population_size=request.population_size
        )
        
        # Set up fitness evaluator
        def fitness_evaluator(resonance_vector, target_topics):
            # Simple fitness based on topic relevance and balance
            # In a real implementation, this would use actual generation testing
            values = resonance_vector.values
            balance_score = 1.0 - (max(values) - min(values))  # Reward balance
            topic_score = 0.8  # Placeholder for topic relevance
            return (balance_score + topic_score) / 2
        
        tone_evolver.set_fitness_evaluator(fitness_evaluator)
        
        # Evolve profile
        evolved_profile = tone_evolver.evolve_profile(profile, request.target_topics)
        
        # Save evolved profile
        profile_persistence.save_profile(evolved_profile)
        
        # Get statistics
        stats = tone_evolver.get_evolution_statistics()
        
        return APIResponse(
            success=True,
            message="Profile evolution completed",
            data={
                "evolved_profile_name": evolved_profile.name,
                "generations_completed": stats["total_generations"],
                "final_fitness": stats["best_fitness"],
                "fitness_improvement": stats.get("fitness_improvement", 0.0),
                "convergence_generation": stats.get("convergence_generation")
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile evolution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Statistics and monitoring endpoints
@app.get("/statistics", response_model=APIResponse)
async def get_statistics():
    """Get system statistics"""
    
    try:
        # Profile statistics
        profile_stats = profile_persistence.get_profile_statistics()
        
        # Generation statistics
        gen_stats = adaptive_writer.get_generation_statistics()
        
        # Drift statistics
        drift_stats = adaptive_writer.drift_detector.get_drift_statistics()
        
        # Parameter statistics
        param_stats = adaptive_writer.parameter_controller.get_parameter_statistics()
        
        return APIResponse(
            success=True,
            message="Statistics retrieved",
            data={
                "profiles": profile_stats,
                "generation": gen_stats,
                "drift": drift_stats,
                "parameters": param_stats
            }
        )
        
    except Exception as e:
        logger.error(f"Statistics retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/export", response_model=APIResponse)
async def export_data():
    """Export system data"""
    
    try:
        # Export all data
        export_data = {
            "profiles": profile_persistence.list_profiles(),
            "generation_data": adaptive_writer.export_generation_data(),
            "parameter_config": adaptive_writer.parameter_controller.export_configuration(),
            "drift_data": adaptive_writer.drift_detector.export_drift_data()
        }
        
        return APIResponse(
            success=True,
            message="Data exported successfully",
            data=export_data
        )
        
    except Exception as e:
        logger.error(f"Data export failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Background task endpoints
@app.post("/backup", response_model=APIResponse)
async def create_backup(background_tasks: BackgroundTasks):
    """Create system backup"""
    
    try:
        # Create backup in background
        def perform_backup():
            try:
                backup_path = profile_persistence.create_profile_backup()
                logger.info(f"Backup created: {backup_path}")
            except Exception as e:
                logger.error(f"Backup failed: {str(e)}")
        
        background_tasks.add_task(perform_backup)
        
        return APIResponse(
            success=True,
            message="Backup task started"
        )
        
    except Exception as e:
        logger.error(f"Backup initiation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Middleware for request logging
@app.middleware("http")
async def log_requests(request, call_next):
    """Log API requests"""
    import time
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    log_api_request(request.method, str(request.url), response.status_code, process_time)
    
    return response


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content=APIResponse(
            success=False,
            message="Resource not found",
            errors=["The requested resource was not found"]
        ).dict()
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            message="Internal server error",
            errors=["An unexpected error occurred"]
        ).dict()
    )


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("ResonanceOS API starting up")
    
    # Ensure directories exist
    config.paths.profiles_dir.mkdir(parents=True, exist_ok=True)
    config.paths.data_dir.mkdir(parents=True, exist_ok=True)
    config.paths.cache_dir.mkdir(parents=True, exist_ok=True)
    config.paths.log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("ResonanceOS API startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("ResonanceOS API shutting down")
    
    # Save any pending data
    try:
        # Create final backup
        profile_persistence.create_profile_backup()
    except Exception as e:
        logger.error(f"Final backup failed: {str(e)}")
    
    logger.info("ResonanceOS API shutdown complete")


# Main function for running the server
def run_server(
    host: str = None,
    port: int = None,
    workers: int = None,
    reload: bool = False
):
    """Run the FastAPI server"""
    
    host = host or config.api.host
    port = port or config.api.port
    workers = workers or config.api.workers
    
    logger.info(f"Starting ResonanceOS API server on {host}:{port}")
    
    uvicorn.run(
        "resonance_os.api.fastapi_server:app",
        host=host,
        port=port,
        workers=workers,
        reload=reload,
        log_level=config.logging.level.lower()
    )


if __name__ == "__main__":
    run_server(reload=True)
