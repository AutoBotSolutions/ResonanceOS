"""
Adaptive writer for ResonanceOS
"""

import asyncio
import time
from typing import Dict, List, Optional, Union, Callable
from datetime import datetime
import numpy as np

from ..core.types import (
    StyleProfile, GenerationConfig, GenerationResult, FeedbackMetrics,
    ResonanceVector, GenerationStatus, TextDocument
)
from ..core.constants import DEFAULT_RESONANCE_THRESHOLD, MAX_CORRECTION_ATTEMPTS
from ..core.logging import get_logger, log_performance, log_generation_metrics
from ..core.config import get_config
from ..profiling.style_vector_builder import StyleVectorBuilder
from ..similarity.metrics import SimilarityCalculator
from ..similarity.drift import DriftDetector
from .parameter_controller import ParameterController

logger = get_logger(__name__)


class AdaptiveWriter:
    """Adaptive writing engine with real-time resonance feedback"""
    
    def __init__(self, tier: int = 1):
        self.config = get_config()
        self.tier = tier
        
        # Initialize components
        self.vector_builder = StyleVectorBuilder(tier)
        self.similarity_calculator = SimilarityCalculator()
        self.drift_detector = DriftDetector()
        self.parameter_controller = ParameterController()
        
        # Generation state
        self.current_profile: Optional[StyleProfile] = None
        self.generation_history: List[GenerationResult] = []
        self.correction_count = 0
        
        # Callbacks for external LLM integration
        self.llm_generator: Optional[Callable] = None
        self.embedding_generator: Optional[Callable] = None
    
    def set_llm_generator(self, generator_func: Callable):
        """Set external LLM generator function"""
        self.llm_generator = generator_func
        logger.info("Set external LLM generator")
    
    def set_embedding_generator(self, embedding_func: Callable):
        """Set external embedding generator function"""
        self.embedding_generator = embedding_func
        logger.info("Set external embedding generator")
    
    @log_performance
    async def generate_article(
        self,
        config: GenerationConfig,
        progress_callback: Optional[Callable] = None
    ) -> GenerationResult:
        """Generate article with adaptive resonance control"""
        
        start_time = time.time()
        
        try:
            # Set current profile
            self.current_profile = config.target_profile
            
            # Initialize generation state
            self.correction_count = 0
            current_content = ""
            paragraph_count = 0
            
            # Generate content paragraph by paragraph with feedback
            while paragraph_count < 10:  # Max 10 paragraphs
                # Generate next paragraph
                paragraph = await self._generate_paragraph(
                    config, current_content, paragraph_count
                )
                
                if not paragraph:
                    break
                
                # Add to content
                if current_content:
                    current_content += "\n\n" + paragraph
                else:
                    current_content = paragraph
                
                paragraph_count += 1
                
                # Analyze resonance of current content
                if config.enable_feedback:
                    feedback = await self._analyze_resonance(current_content, config)
                    
                    # Check if correction is needed
                    if feedback.correction_needed and self.correction_count < config.max_corrections:
                        await self._apply_corrections(feedback, config)
                        self.correction_count += 1
                        
                        # Optionally regenerate last paragraph with corrections
                        if feedback.correction_strength > 0.5:
                            current_content = current_content[:-(len(paragraph) + 2)]
                            paragraph = await self._generate_paragraph(
                                config, current_content, paragraph_count - 1
                            )
                            if current_content:
                                current_content += "\n\n" + paragraph
                            else:
                                current_content = paragraph
                
                # Progress callback
                if progress_callback:
                    progress_callback({
                        'paragraph': paragraph_count,
                        'content_length': len(current_content),
                        'corrections': self.correction_count
                    })
                
                # Check if we have enough content
                if len(current_content) >= config.max_tokens * 3:  # Rough token estimate
                    break
            
            # Final analysis
            final_feedback = await self._analyze_resonance(current_content, config)
            
            # Create result
            generation_time = time.time() - start_time
            
            result = GenerationResult(
                content=current_content,
                profile_used=config.target_profile,
                config=config,
                metrics=final_feedback,
                status=GenerationStatus.COMPLETED,
                tokens_generated=len(current_content.split()),
                corrections_made=self.correction_count,
                generation_time=generation_time,
                created_at=datetime.now()
            )
            
            # Store in history
            self.generation_history.append(result)
            
            # Log metrics
            log_generation_metrics({
                'similarity_score': final_feedback.similarity_score,
                'drift_rate': final_feedback.drift_rate,
                'corrections_made': self.correction_count,
                'tokens_generated': result.tokens_generated
            })
            
            logger.info(f"Generated article: {result.tokens_generated} tokens, {self.correction_count} corrections")
            
            return result
            
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            
            # Return failed result
            return GenerationResult(
                content="",
                profile_used=config.target_profile,
                config=config,
                metrics=FeedbackMetrics(
                    similarity_score=0.0,
                    target_similarity=config.similarity_threshold,
                    drift_rate=1.0,
                    deviation_vector=[],
                    correction_needed=True,
                    correction_strength=1.0,
                    timestamp=datetime.now()
                ),
                status=GenerationStatus.FAILED,
                tokens_generated=0,
                corrections_made=self.correction_count,
                generation_time=time.time() - start_time,
                created_at=datetime.now()
            )
    
    async def _generate_paragraph(
        self,
        config: GenerationConfig,
        previous_content: str,
        paragraph_index: int
    ) -> str:
        """Generate a single paragraph"""
        
        # Build prompt
        prompt = self._build_prompt(config, previous_content, paragraph_index)
        
        # Get current parameters
        parameters = self.parameter_controller.get_current_parameters()
        
        # Generate using external LLM or fallback
        if self.llm_generator:
            try:
                paragraph = await self._call_external_llm(prompt, parameters)
            except Exception as e:
                logger.error(f"External LLM failed: {str(e)}")
                paragraph = self._fallback_generation(prompt, paragraph_index)
        else:
            paragraph = self._fallback_generation(prompt, paragraph_index)
        
        return paragraph.strip()
    
    def _build_prompt(
        self,
        config: GenerationConfig,
        previous_content: str,
        paragraph_index: int
    ) -> str:
        """Build generation prompt"""
        
        # Base prompt
        prompt = f"Write about: {config.topic}\n\n"
        
        # Style guidance
        if self.current_profile:
            prompt += f"Style: {self.current_profile.description or 'Professional and engaging'}\n"
            prompt += f"Tone: Match the target style with {config.similarity_threshold:.0%} similarity\n"
        
        # Context from previous content
        if previous_content:
            prompt += f"\nPrevious content:\n{previous_content[-500:]}\n\n"
            prompt += f"Continue writing paragraph {paragraph_index + 1} that flows naturally:\n\n"
        else:
            prompt += f"\nWrite the first paragraph:\n\n"
        
        # Length guidance
        prompt += f"Write 3-5 sentences (approximately 50-100 words).\n"
        
        # Quality requirements
        prompt += "Ensure the writing is original, coherent, and maintains consistency.\n\n"
        
        return prompt
    
    async def _call_external_llm(self, prompt: str, parameters: Dict[str, float]) -> str:
        """Call external LLM API"""
        
        if not self.llm_generator:
            raise ValueError("No LLM generator configured")
        
        # Prepare parameters for external API
        api_params = {
            'prompt': prompt,
            'max_tokens': parameters.get('max_tokens', 150),
            'temperature': parameters.get('temperature', 0.7),
            'top_p': parameters.get('top_p', 0.9),
            'presence_penalty': parameters.get('presence_penalty', 0.0),
            'frequency_penalty': parameters.get('frequency_penalty', 0.0),
            'stop': None
        }
        
        # Call external generator
        result = await self.llm_generator(api_params)
        
        # Extract text from result
        if isinstance(result, str):
            return result
        elif isinstance(result, dict) and 'text' in result:
            return result['text']
        else:
            raise ValueError(f"Unexpected result format: {type(result)}")
    
    def _fallback_generation(self, prompt: str, paragraph_index: int) -> str:
        """Fallback generation when external LLM is not available"""
        
        # Simple template-based fallback
        templates = [
            f"This aspect of {prompt.split('Write about:')[1].split('\n')[0].strip()} deserves careful consideration.",
            f"Building on this foundation, we can see several key emerging patterns.",
            f"The implications of this development are both significant and far-reaching.",
            f"From this perspective, the underlying mechanisms become clearer.",
            f"This analysis reveals important insights that warrant further exploration."
        ]
        
        template = templates[paragraph_index % len(templates)]
        
        # Add some topic-specific content
        topic_words = prompt.split('Write about:')[1].split('\n')[0].strip().split()[:3]
        topic_context = " ".join(topic_words)
        
        return f"{template} When examining {topic_context}, we find compelling evidence that supports this view. This understanding helps frame our approach to the broader challenges ahead."
    
    async def _analyze_resonance(
        self,
        content: str,
        config: GenerationConfig
    ) -> FeedbackMetrics:
        """Analyze resonance of generated content"""
        
        # Create document from content
        document = TextDocument(
            content=content,
            source="generation",
            metadata={'config': config.dict()}
        )
        
        # Build resonance vector
        current_vector = self.vector_builder.build_vector([document])
        
        # Calculate similarity
        similarity = self.similarity_calculator.calculate_similarity(
            current_vector, config.target_profile.resonance_vector
        )
        
        # Calculate deviation vector
        target_values = np.array(config.target_profile.resonance_vector.values)
        current_values = np.array(current_vector.values)
        deviation_vector = (current_values - target_values).tolist()
        
        # Check if correction is needed
        correction_needed = similarity < config.similarity_threshold
        
        # Calculate correction strength
        correction_strength = max(0.0, (config.similarity_threshold - similarity) / config.similarity_threshold)
        
        # Update drift detector
        drift_analysis = self.drift_detector.add_measurement(
            current_vector, config.target_profile.resonance_vector
        )
        
        return FeedbackMetrics(
            similarity_score=similarity,
            target_similarity=config.similarity_threshold,
            drift_rate=drift_analysis.drift_rate,
            deviation_vector=deviation_vector,
            correction_needed=correction_needed,
            correction_strength=correction_strength,
            timestamp=datetime.now()
        )
    
    async def _apply_corrections(self, feedback: FeedbackMetrics, config: GenerationConfig):
        """Apply parameter corrections based on feedback"""
        
        # Calculate corrections
        corrections = self.parameter_controller.calculate_corrections(
            feedback, config.similarity_threshold
        )
        
        logger.info(f"Applied {len(corrections)} corrections: similarity={feedback.similarity_score:.3f}")
        
        # Update drift detector with correction information
        self.drift_detector.reset_baseline()
    
    def get_generation_statistics(self) -> Dict[str, Union[int, float, str]]:
        """Get statistics about generation performance"""
        
        if not self.generation_history:
            return {
                'total_generations': 0,
                'average_similarity': 0.0,
                'average_corrections': 0.0,
                'average_generation_time': 0.0,
                'success_rate': 0.0
            }
        
        successful_generations = [
            gen for gen in self.generation_history 
            if gen.status == GenerationStatus.COMPLETED
        ]
        
        similarities = [gen.metrics.similarity_score for gen in successful_generations]
        corrections = [gen.corrections_made for gen in successful_generations]
        generation_times = [gen.generation_time for gen in successful_generations]
        
        return {
            'total_generations': len(self.generation_history),
            'successful_generations': len(successful_generations),
            'average_similarity': np.mean(similarities) if similarities else 0.0,
            'average_corrections': np.mean(corrections) if corrections else 0.0,
            'average_generation_time': np.mean(generation_times) if generation_times else 0.0,
            'success_rate': len(successful_generations) / len(self.generation_history),
            'current_profile': self.current_profile.name if self.current_profile else None
        }
    
    def reset_state(self):
        """Reset generation state"""
        
        self.current_profile = None
        self.correction_count = 0
        self.drift_detector = DriftDetector()
        self.parameter_controller.reset_parameters()
        
        logger.info("Reset adaptive writer state")
    
    def export_generation_data(self) -> Dict[str, Union[List, Dict]]:
        """Export generation data for analysis"""
        
        return {
            'generation_history': [
                {
                    'content': gen.content[:500] + "..." if len(gen.content) > 500 else gen.content,
                    'similarity_score': gen.metrics.similarity_score,
                    'corrections_made': gen.corrections_made,
                    'generation_time': gen.generation_time,
                    'status': gen.status.value,
                    'created_at': gen.created_at.isoformat()
                }
                for gen in self.generation_history[-10:]  # Last 10 generations
            ],
            'statistics': self.get_generation_statistics(),
            'parameter_controller': self.parameter_controller.export_configuration(),
            'drift_detector': self.drift_detector.export_drift_data()
        }


class BatchGenerator:
    """Batch generation for multiple articles"""
    
    def __init__(self, adaptive_writer: AdaptiveWriter):
        self.writer = adaptive_writer
        self.batch_results: List[GenerationResult] = []
    
    async def generate_batch(
        self,
        configs: List[GenerationConfig],
        max_concurrent: int = 3,
        progress_callback: Optional[Callable] = None
    ) -> List[GenerationResult]:
        """Generate multiple articles concurrently"""
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def generate_single(config: GenerationConfig, index: int) -> GenerationResult:
            async with semaphore:
                result = await self.writer.generate_article(
                    config,
                    progress_callback=lambda p: progress_callback(index, p) if progress_callback else None
                )
                return result
        
        # Run all generations concurrently
        tasks = [generate_single(config, i) for i, config in enumerate(configs)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log them
        successful_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Generation {i} failed: {str(result)}")
            else:
                successful_results.append(result)
        
        self.batch_results = successful_results
        
        logger.info(f"Batch generation completed: {len(successful_results)}/{len(configs)} successful")
        
        return successful_results
    
    def get_batch_statistics(self) -> Dict[str, Union[int, float, List]]:
        """Get statistics for batch generation"""
        
        if not self.batch_results:
            return {
                'total_articles': 0,
                'successful_articles': 0,
                'average_similarity': 0.0,
                'average_corrections': 0.0,
                'total_time': 0.0,
                'similarity_distribution': []
            }
        
        similarities = [gen.metrics.similarity_score for gen in self.batch_results]
        corrections = [gen.corrections_made for gen in self.batch_results]
        times = [gen.generation_time for gen in self.batch_results]
        
        return {
            'total_articles': len(self.batch_results),
            'successful_articles': len(self.batch_results),
            'average_similarity': np.mean(similarities),
            'average_corrections': np.mean(corrections),
            'total_time': sum(times),
            'similarity_distribution': similarities,
            'correction_distribution': corrections
        }
