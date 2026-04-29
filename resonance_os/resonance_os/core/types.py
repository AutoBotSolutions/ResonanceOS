"""
Type definitions for ResonanceOS
"""

from typing import List, Dict, Optional, Union, Any, Tuple
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
import numpy as np


class SimilarityMethod(str, Enum):
    """Methods for calculating resonance similarity"""
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    MANHATTAN = "manhattan"
    PEARSON = "pearson"
    SPEARMAN = "spearman"


class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class GenerationStatus(str, Enum):
    """Status of text generation"""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    CORRECTING = "correcting"


class ResonanceVector(BaseModel):
    """Multi-dimensional resonance vector"""
    values: List[float] = Field(description="Vector values for each resonance dimension")
    dimensions: List[str] = Field(description="Names of resonance dimensions")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array"""
        return np.array(self.values)
    
    @classmethod
    def from_numpy(cls, values: np.ndarray, dimensions: List[str], confidence: float = 1.0):
        """Create from numpy array"""
        return cls(
            values=values.tolist(),
            dimensions=dimensions,
            confidence=confidence
        )


class StyleProfile(BaseModel):
    """Writer style profile with resonance vector"""
    name: str = Field(description="Profile name")
    description: Optional[str] = Field(default=None, description="Profile description")
    resonance_vector: ResonanceVector = Field(description="Resonance vector")
    emotional_curve: List[float] = Field(description="Emotional intensity curve across paragraphs")
    cadence_pattern: List[float] = Field(description="Cadence rhythm pattern")
    abstraction_preference: float = Field(ge=0.0, le=1.0, description="Preferred abstraction level")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class GenerationConfig(BaseModel):
    """Configuration for text generation"""
    topic: str = Field(description="Topic or prompt for generation")
    target_profile: StyleProfile = Field(description="Target style profile")
    max_tokens: int = Field(default=2048, ge=100, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    stop_sequences: Optional[List[str]] = Field(default=None)
    similarity_threshold: float = Field(default=0.92, ge=0.0, le=1.0)
    max_corrections: int = Field(default=3, ge=0, le=10)
    enable_feedback: bool = Field(default=True)
    enable_drift_detection: bool = Field(default=True)


class FeedbackMetrics(BaseModel):
    """Metrics from resonance feedback analysis"""
    similarity_score: float = Field(ge=0.0, le=1.0, description="Current similarity score")
    target_similarity: float = Field(ge=0.0, le=1.0, description="Target similarity threshold")
    drift_rate: float = Field(description="Rate of style drift")
    deviation_vector: List[float] = Field(description="Vector of deviations per dimension")
    correction_needed: bool = Field(description="Whether correction is needed")
    correction_strength: float = Field(default=0.0, ge=0.0, le=1.0, description="Strength of correction needed")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class GenerationResult(BaseModel):
    """Result from text generation"""
    content: str = Field(description="Generated text content")
    profile_used: StyleProfile = Field(description="Profile used for generation")
    config: GenerationConfig = Field(description="Generation configuration")
    metrics: FeedbackMetrics = Field(description="Final resonance metrics")
    status: GenerationStatus = Field(description="Generation status")
    tokens_generated: int = Field(description="Number of tokens generated")
    corrections_made: int = Field(default=0, description="Number of corrections applied")
    generation_time: float = Field(description="Time taken for generation in seconds")
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CorpusInfo(BaseModel):
    """Information about a text corpus"""
    name: str = Field(description="Corpus name")
    source: str = Field(description="Source of corpus")
    file_count: int = Field(description="Number of files in corpus")
    total_characters: int = Field(description="Total character count")
    total_words: int = Field(description="Total word count")
    total_sentences: int = Field(description="Total sentence count")
    avg_sentence_length: float = Field(description="Average sentence length")
    language: str = Field(default="en", description="Language code")
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TrainingProgress(BaseModel):
    """Progress tracking for model training"""
    epoch: int = Field(description="Current epoch")
    total_epochs: int = Field(description="Total epochs")
    loss: float = Field(description="Current loss")
    accuracy: float = Field(description="Current accuracy")
    similarity_score: float = Field(description="Current resonance similarity")
    learning_rate: float = Field(description="Current learning rate")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class APIResponse(BaseModel):
    """Standard API response format"""
    success: bool = Field(description="Whether request was successful")
    message: str = Field(description="Response message")
    data: Optional[Any] = Field(default=None, description="Response data")
    errors: Optional[List[str]] = Field(default=None, description="Error messages")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ProfileRequest(BaseModel):
    """Request for profile creation/analysis"""
    name: str = Field(description="Profile name")
    corpus_path: str = Field(description="Path to corpus files")
    description: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GenerationRequest(BaseModel):
    """Request for text generation"""
    topic: str = Field(description="Topic or prompt")
    profile_name: str = Field(description="Name of profile to use")
    max_tokens: int = Field(default=2048, ge=100, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    similarity_threshold: float = Field(default=0.92, ge=0.0, le=1.0)


class CorrectionAction(BaseModel):
    """Action to take for resonance correction"""
    parameter: str = Field(description="Parameter to adjust")
    current_value: float = Field(description="Current parameter value")
    adjustment: float = Field(description="Adjustment amount")
    new_value: float = Field(description="New parameter value")
    reason: str = Field(description="Reason for adjustment")


class DriftAnalysis(BaseModel):
    """Analysis of style drift"""
    current_similarity: float = Field(description="Current similarity score")
    baseline_similarity: float = Field(description="Baseline similarity score")
    drift_rate: float = Field(description="Rate of drift")
    drift_direction: str = Field(description="Direction of drift (increasing/decreasing/stable)")
    affected_dimensions: List[str] = Field(description="Most affected dimensions")
    severity: str = Field(description="Severity level (low/medium/high)")
    recommendation: str = Field(description="Recommended action")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Type aliases for better readability
Vector = Union[List[float], np.ndarray]
ProfileDict = Dict[str, Any]
MetricsDict = Dict[str, Union[float, List[float], bool, datetime]]
