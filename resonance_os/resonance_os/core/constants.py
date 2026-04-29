"""
Core constants for ResonanceOS
"""

from typing import List, Dict, Any
import numpy as np

# Resonance Tone Factor Dimensions
RESONANCE_DIMENSIONS: List[str] = [
    "lexical_density",
    "emotional_valence", 
    "cadence_variability",
    "sentence_entropy",
    "metaphor_frequency",
    "abstraction_level",
    "assertiveness_score",
    "rhythm_signature",
    "narrative_intensity_curve",
    "cognitive_load_index"
]

# Default resonance thresholds
DEFAULT_RESONANCE_THRESHOLD: float = 0.92
DEFAULT_DRIFT_THRESHOLD: float = 0.05
MAX_CORRECTION_ATTEMPTS: int = 3

# Generation parameters
DEFAULT_TEMPERATURE: float = 0.7
DEFAULT_TOP_P: float = 0.9
DEFAULT_MAX_TOKENS: int = 2048
DEFAULT_BATCH_SIZE: int = 32

# Model configurations
DEFAULT_OPENAI_MODEL: str = "gpt-3.5-turbo"
DEFAULT_EMBEDDING_MODEL: str = "text-embedding-ada-002"
DEFAULT_SPACY_MODEL: str = "en_core_web_lg"

# File paths and directories
DEFAULT_DATA_DIR: str = "data"
DEFAULT_PROFILES_DIR: str = "profiles"
DEFAULT_CACHE_DIR: str = ".cache"
DEFAULT_LOG_DIR: str = "logs"

# API configuration
DEFAULT_API_HOST: str = "0.0.0.0"
DEFAULT_API_PORT: int = 8000
DEFAULT_API_WORKERS: int = 4

# Logging
DEFAULT_LOG_LEVEL: str = "INFO"

# Feature extraction weights
FEATURE_WEIGHTS: Dict[str, float] = {
    "lexical_density": 0.1,
    "emotional_valence": 0.15,
    "cadence_variability": 0.1,
    "sentence_entropy": 0.1,
    "metaphor_frequency": 0.08,
    "abstraction_level": 0.12,
    "assertiveness_score": 0.1,
    "rhythm_signature": 0.1,
    "narrative_intensity_curve": 0.08,
    "cognitive_load_index": 0.07
}

# Similarity methods
SIMILARITY_METHODS: List[str] = [
    "cosine",
    "euclidean", 
    "manhattan",
    "pearson",
    "spearman"
]

# Reinforcement learning parameters
DEFAULT_REWARD_SCALE: float = 1.0
DEFAULT_PENALTY_SCALE: float = 0.5
DEFAULT_DISCOUNT_RATE: float = 0.95
DEFAULT_LEARNING_RATE: float = 0.001

# Evolution parameters
EVOLUTION_GENERATIONS: int = 100
EVOLUTION_POPULATION_SIZE: int = 50
EVOLUTION_MUTATION_RATE: float = 0.1
EVOLUTION_CROSSOVER_RATE: float = 0.8

# Text processing
MIN_SENTENCE_LENGTH: int = 5
MAX_SENTENCE_LENGTH: int = 100
MIN_PARAGRAPH_LENGTH: int = 20
MAX_PARAGRAPH_LENGTH: int = 500

# Emotional valence ranges
EMOTIONAL_RANGES: Dict[str, tuple] = {
    "very_negative": (-1.0, -0.6),
    "negative": (-0.6, -0.2),
    "neutral": (-0.2, 0.2),
    "positive": (0.2, 0.6),
    "very_positive": (0.6, 1.0)
}

# Abstraction levels
ABSTRACTION_LEVELS: Dict[str, float] = {
    "very_concrete": 0.0,
    "concrete": 0.25,
    "moderate": 0.5,
    "abstract": 0.75,
    "very_abstract": 1.0
}

# Cadence patterns
CADENCE_PATTERNS: Dict[str, List[float]] = {
    "steady": [0.5, 0.5, 0.5, 0.5],
    "building": [0.3, 0.4, 0.6, 0.8],
    "declining": [0.8, 0.6, 0.4, 0.3],
    "wave": [0.3, 0.7, 0.4, 0.8],
    "explosive": [0.2, 0.3, 0.9, 0.6]
}

# Default brand identity template
DEFAULT_BRAND_PROFILE: Dict[str, Any] = {
    "name": "Default Brand",
    "version": "1.0",
    "resonance_vector": np.zeros(len(RESONANCE_DIMENSIONS)).tolist(),
    "emotional_curve": [0.5, 0.6, 0.7, 0.6, 0.5],
    "cadence_pattern": CADENCE_PATTERNS["steady"],
    "abstraction_preference": ABSTRACTION_LEVELS["moderate"],
    "created_at": None,
    "updated_at": None,
    "metadata": {
        "description": "Default brand identity profile",
        "industry": "general",
        "target_audience": "general",
        "tone_guidelines": []
    }
}
