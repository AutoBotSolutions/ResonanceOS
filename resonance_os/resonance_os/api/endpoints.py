"""
API endpoints for ResonanceOS
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from ..core.types import (
    StyleProfile, GenerationConfig, APIResponse, SimilarityMethod,
    ProfileRequest, GenerationRequest
)
from ..core.logging import get_logger
from ..profiling.profile_persistence import ProfilePersistence
from ..generation.adaptive_writer import AdaptiveWriter
from ..similarity.metrics import SimilarityCalculator

logger = get_logger(__name__)

# Create router
router = APIRouter(prefix="/api/v1", tags=["resonance"])

# Dependencies
profile_persistence = ProfilePersistence()
adaptive_writer = AdaptiveWriter()

async def get_profile_by_name(profile_name: str) -> StyleProfile:
    """Get profile by name or raise HTTPException"""
    profile = profile_persistence.load_profile_by_name(profile_name)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile '{profile_name}' not found")
    return profile


# Profile endpoints
@router.post("/profiles/create", response_model=APIResponse)
async def create_profile_from_text(
    name: str,
    text_content: str,
    description: Optional[str] = None,
    tier: int = 1
):
    """Create profile from direct text input"""
    
    try:
        from ..profiling.style_vector_builder import StyleVectorBuilder
        from ..core.types import TextDocument
        
        # Create document
        document = TextDocument(
            content=text_content,
            source="direct_input",
            metadata={"tier": tier}
        )
        
        # Build resonance vector
        vector_builder = StyleVectorBuilder(tier)
        resonance_vector = vector_builder.build_vector([document])
        
        # Create profile
        profile = StyleProfile(
            name=name,
            description=description,
            resonance_vector=resonance_vector,
            emotional_curve=[0.5] * 5,
            cadence_pattern=[0.5] * 4,
            abstraction_preference=0.5,
            metadata={"source": "direct_input", "tier": tier}
        )
        
        # Save profile
        profile_persistence.save_profile(profile)
        
        return APIResponse(
            success=True,
            message=f"Profile '{name}' created from text",
            data={
                "profile_name": name,
                "confidence": resonance_vector.confidence,
                "text_length": len(text_content),
                "tier": tier
            }
        )
        
    except Exception as e:
        logger.error(f"Profile creation from text failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profiles/{profile_name}/analyze", response_model=APIResponse)
async def analyze_profile(profile_name: str):
    """Get detailed analysis of a profile"""
    
    try:
        profile = await get_profile_by_name(profile_name)
        
        # Get dimension analysis
        dimensions = profile.resonance_vector.dimensions
        values = profile.resonance_vector.values
        
        dimension_analysis = []
        for dim, val in zip(dimensions, values):
            level = "high" if val > 0.7 else "medium" if val > 0.3 else "low"
            dimension_analysis.append({
                "dimension": dim,
                "value": val,
                "level": level
            })
        
        return APIResponse(
            success=True,
            message=f"Profile '{profile_name}' analyzed",
            data={
                "profile_name": profile.name,
                "confidence": profile.resonance_vector.confidence,
                "dimension_analysis": dimension_analysis,
                "emotional_curve": profile.emotional_curve,
                "cadence_pattern": profile.cadence_pattern,
                "abstraction_preference": profile.abstraction_preference,
                "created_at": profile.created_at.isoformat(),
                "metadata": profile.metadata
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/profiles/{profile_name}/clone", response_model=APIResponse)
async def clone_profile(
    profile_name: str,
    new_name: str,
    modifications: Optional[Dict[str, float]] = None
):
    """Clone a profile with optional modifications"""
    
    try:
        # Get original profile
        original_profile = await get_profile_by_name(profile_name)
        
        # Create clone
        cloned_vector = original_profile.resonance_vector
        
        # Apply modifications if provided
        if modifications:
            values = cloned_vector.values.copy()
            dimensions = cloned_vector.dimensions.copy()
            
            for dim_name, new_value in modifications.items():
                if dim_name in dimensions:
                    idx = dimensions.index(dim_name)
                    values[idx] = max(0.0, min(1.0, new_value))
            
            cloned_vector.values = values
        
        cloned_profile = StyleProfile(
            name=new_name,
            description=f"Cloned from {profile_name}",
            resonance_vector=cloned_vector,
            emotional_curve=original_profile.emotional_curve.copy(),
            cadence_pattern=original_profile.cadence_pattern.copy(),
            abstraction_preference=original_profile.abstraction_preference,
            metadata={
                **original_profile.metadata,
                "cloned_from": profile_name,
                "modifications": modifications or {}
            }
        )
        
        # Save cloned profile
        profile_persistence.save_profile(cloned_profile)
        
        return APIResponse(
            success=True,
            message=f"Profile '{new_name}' cloned from '{profile_name}'",
            data={
                "original_profile": profile_name,
                "cloned_profile": new_name,
                "modifications": modifications or {}
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile cloning failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Advanced generation endpoints
@router.post("/generate/progressive", response_model=APIResponse)
async def generate_progressive(
    topic: str,
    profile_name: str,
    target_paragraphs: int = 5,
    similarity_threshold: float = 0.92,
    enable_corrections: bool = True
):
    """Generate text with progressive paragraph-by-paragraph feedback"""
    
    try:
        profile = await get_profile_by_name(profile_name)
        
        # Create generation config
        config = GenerationConfig(
            topic=topic,
            target_profile=profile,
            max_tokens=target_paragraphs * 100,  # Rough estimate
            similarity_threshold=similarity_threshold,
            enable_feedback=enable_corrections,
            enable_drift_detection=True,
            max_corrections=10
        )
        
        # Track progress
        progress_data = []
        
        def progress_callback(progress):
            progress_data.append(progress)
        
        # Generate text
        result = await adaptive_writer.generate_article(config, progress_callback)
        
        return APIResponse(
            success=True,
            message="Progressive generation completed",
            data={
                "content": result.content,
                "similarity_score": result.metrics.similarity_score,
                "corrections_made": result.corrections_made,
                "generation_time": result.generation_time,
                "tokens_generated": result.tokens_generated,
                "progress_data": progress_data,
                "final_drift_rate": result.metrics.drift_rate
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Progressive generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/comparison", response_model=APIResponse)
async def generate_comparison(
    topic: str,
    profile_names: List[str],
    similarity_threshold: float = 0.92
):
    """Generate text using multiple profiles for comparison"""
    
    try:
        results = []
        
        for profile_name in profile_names:
            profile = await get_profile_by_name(profile_name)
            
            config = GenerationConfig(
                topic=topic,
                target_profile=profile,
                max_tokens=500,  # Shorter for comparison
                similarity_threshold=similarity_threshold,
                enable_feedback=True,
                enable_drift_detection=True
            )
            
            result = await adaptive_writer.generate_article(config)
            
            results.append({
                "profile_name": profile_name,
                "content": result.content,
                "similarity_score": result.metrics.similarity_score,
                "corrections_made": result.corrections_made,
                "generation_time": result.generation_time
            })
        
        return APIResponse(
            success=True,
            message=f"Generated {len(results)} comparisons",
            data={
                "topic": topic,
                "results": results,
                "summary": {
                    "best_similarity": max(r["similarity_score"] for r in results),
                    "average_similarity": sum(r["similarity_score"] for r in results) / len(results),
                    "total_corrections": sum(r["corrections_made"] for r in results)
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Comparison generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Analysis endpoints
@router.post("/analyze/similarity-matrix", response_model=APIResponse)
async def create_similarity_matrix(
    profile_names: List[str],
    method: SimilarityMethod = SimilarityMethod.COSINE
):
    """Create similarity matrix for multiple profiles"""
    
    try:
        # Load all profiles
        profiles = []
        for name in profile_names:
            profile = await get_profile_by_name(name)
            profiles.append(profile)
        
        # Calculate similarity matrix
        calculator = SimilarityCalculator(method)
        matrix = []
        
        for i, profile1 in enumerate(profiles):
            row = []
            for j, profile2 in enumerate(profiles):
                if i == j:
                    similarity = 1.0
                else:
                    similarity = calculator.calculate_similarity(
                        profile1.resonance_vector, profile2.resonance_vector
                    )
                row.append(similarity)
            matrix.append(row)
        
        return APIResponse(
            success=True,
            message="Similarity matrix created",
            data={
                "profile_names": profile_names,
                "similarity_matrix": matrix,
                "method": method.value,
                "statistics": {
                    "average_similarity": sum(sum(row) for row in matrix) / (len(matrix) * len(matrix)),
                    "most_similar_pair": _find_most_similar_pair(profile_names, matrix),
                    "least_similar_pair": _find_least_similar_pair(profile_names, matrix)
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Similarity matrix creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def _find_most_similar_pair(profile_names: List[str], matrix: List[List[float]]) -> Dict[str, str]:
    """Find most similar pair of profiles"""
    max_similarity = 0.0
    best_pair = {}
    
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            similarity = matrix[i][j]
            if similarity > max_similarity:
                max_similarity = similarity
                best_pair = {
                    "profile1": profile_names[i],
                    "profile2": profile_names[j],
                    "similarity": similarity
                }
    
    return best_pair


def _find_least_similar_pair(profile_names: List[str], matrix: List[List[float]]) -> Dict[str, str]:
    """Find least similar pair of profiles"""
    min_similarity = 1.0
    worst_pair = {}
    
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            similarity = matrix[i][j]
            if similarity < min_similarity:
                min_similarity = similarity
                worst_pair = {
                    "profile1": profile_names[i],
                    "profile2": profile_names[j],
                    "similarity": similarity
                }
    
    return worst_pair


@router.get("/analyze/dimension-importance", response_model=APIResponse)
async def get_dimension_importance():
    """Get importance weights for different resonance dimensions"""
    
    try:
        from ..core.constants import FEATURE_WEIGHTS
        
        return APIResponse(
            success=True,
            message="Dimension importance retrieved",
            data={
                "feature_weights": FEATURE_WEIGHTS,
                "dimensions": list(FEATURE_WEIGHTS.keys()),
                "total_weight": sum(FEATURE_WEIGHTS.values())
            }
        )
        
    except Exception as e:
        logger.error(f"Dimension importance retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# System management endpoints
@router.post("/system/reset", response_model=APIResponse)
async def reset_system(
    component: str = "all",
    background_tasks: BackgroundTasks = None
):
    """Reset system components"""
    
    try:
        reset_tasks = []
        
        if component in ["all", "generation"]:
            def reset_generation():
                adaptive_writer.reset_state()
                logger.info("Generation system reset")
            
            if background_tasks:
                background_tasks.add_task(reset_generation)
            else:
                reset_generation()
            reset_tasks.append("generation")
        
        if component in ["all", "drift"]:
            def reset_drift():
                adaptive_writer.drift_detector = adaptive_writer.drift_detector.__class__()
                logger.info("Drift detector reset")
            
            if background_tasks:
                background_tasks.add_task(reset_drift)
            else:
                reset_drift()
            reset_tasks.append("drift")
        
        if component in ["all", "parameters"]:
            def reset_parameters():
                adaptive_writer.parameter_controller.reset_parameters()
                logger.info("Parameter controller reset")
            
            if background_tasks:
                background_tasks.add_task(reset_parameters)
            else:
                reset_parameters()
            reset_tasks.append("parameters")
        
        return APIResponse(
            success=True,
            message=f"Reset initiated for: {', '.join(reset_tasks)}",
            data={"reset_components": reset_tasks}
        )
        
    except Exception as e:
        logger.error(f"System reset failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/system/health/detailed", response_model=APIResponse)
async def detailed_health_check():
    """Detailed health check with component status"""
    
    try:
        health_status = {
            "api": "healthy",
            "components": {}
        }
        
        # Check profile system
        try:
            profile_count = len(profile_persistence.list_profiles())
            health_status["components"]["profiles"] = {
                "status": "healthy",
                "profile_count": profile_count
            }
        except Exception as e:
            health_status["components"]["profiles"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["api"] = "degraded"
        
        # Check generation system
        try:
            gen_stats = adaptive_writer.get_generation_statistics()
            health_status["components"]["generation"] = {
                "status": "healthy",
                "total_generations": gen_stats["total_generations"],
                "success_rate": gen_stats["success_rate"]
            }
        except Exception as e:
            health_status["components"]["generation"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["api"] = "degraded"
        
        # Check drift detection
        try:
            drift_stats = adaptive_writer.drift_detector.get_drift_statistics()
            health_status["components"]["drift"] = {
                "status": "healthy",
                "total_measurements": drift_stats["total_measurements"]
            }
        except Exception as e:
            health_status["components"]["drift"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["api"] = "degraded"
        
        return APIResponse(
            success=True,
            message="Health check completed",
            data=health_status
        )
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
