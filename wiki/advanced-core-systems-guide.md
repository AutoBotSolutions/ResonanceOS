# Advanced Core Systems Guide - ResonanceOS v6

## Overview

The Advanced Core Systems module provides enhanced configuration management, logging infrastructure, type definitions, and constants for ResonanceOS v6. This module serves as the foundational infrastructure for the entire system, enabling type-safe operations, structured logging, and flexible configuration.

## System Architecture

```
Advanced Core Systems
├── config.py (Configuration Management)
├── logging.py (Logging Infrastructure)
├── types.py (Type Definitions)
└── constants.py (System Constants)
```

## System Components

### 1. Configuration Management (`config.py`)

Provides comprehensive configuration management using Pydantic BaseSettings with environment variable support.

#### Architecture

```python
class Settings(BaseSettings):
    """Main application settings"""
    
    # Sub-settings
    database: DatabaseSettings = DatabaseSettings()
    api: APISettings = APISettings()
    models: ModelSettings = ModelSettings()
    resonance: ResonanceSettings = ResonanceSettings()
    generation: GenerationSettings = GenerationSettings()
    paths: PathSettings = PathSettings()
    logging: LoggingSettings = LoggingSettings()
```

#### Configuration Classes

**DatabaseSettings**
- `url`: Database connection URL (default: sqlite:///./resonance_os.db)
- `echo`: SQL echo for debugging (default: False)

**APISettings**
- `host`: API server host (default: "0.0.0.0")
- `port`: API server port (default: 8000)
- `workers`: Number of worker processes (default: 4)
- `reload`: Auto-reload on code changes (default: False)
- `log_level`: Logging level (default: "info")

**ModelSettings**
- `openai_api_key`: OpenAI API key (required)
- `huggingface_api_key`: HuggingFace API key (optional)
- `default_model`: Default AI model (default: "gpt-3.5-turbo")
- `embedding_model`: Embedding model (default: "text-embedding-ada-002")
- `spacy_model`: spaCy model (default: "en_core_web_lg")

**ResonanceSettings**
- `threshold`: Resonance similarity threshold (default: 0.92)
- `drift_threshold`: Drift detection threshold (default: 0.05)
- `max_correction_attempts`: Maximum correction attempts (default: 3)
- `similarity_method`: Similarity calculation method (default: "cosine")

**GenerationSettings**
- `temperature`: Generation temperature (default: 0.7)
- `top_p`: Top-p sampling parameter (default: 0.9)
- `max_tokens`: Maximum tokens to generate (default: 2048)
- `batch_size`: Batch processing size (default: 32)

**PathSettings**
- `data_dir`: Data directory path (default: Path("data"))
- `profiles_dir`: Profiles directory path (default: Path("profiles"))
- `cache_dir`: Cache directory path (default: Path(".cache"))
- `log_dir`: Log directory path (default: Path("logs"))

**LoggingSettings**
- `level`: Logging level (default: "INFO")
- `file`: Log file path (optional)
- `format`: Log message format
- `date_format`: Date format for logs

#### Usage Example

```python
from resonance_os.core.config import get_config, reload_config, get_env_vars

# Get configuration
config = get_config()
print(f"API Host: {config.api.host}")
print(f"Default Model: {config.models.default_model}")
print(f"Resonance Threshold: {config.resonance.threshold}")

# Reload configuration
config = reload_config()

# Get environment variables
env_vars = get_env_vars()
print(f"Environment: {env_vars['ENVIRONMENT']}")
```

#### Environment Variables

Configuration can be set via environment variables:

```bash
# API Configuration
export API_HOST=0.0.0.0
export API_PORT=8000
export LOG_LEVEL=info

# Model Configuration
export OPENAI_API_KEY=your_api_key
export DEFAULT_MODEL=gpt-4
export EMBEDDING_MODEL=text-embedding-ada-002

# Resonance Configuration
export RESONANCE_THRESHOLD=0.92
export DRIFT_THRESHOLD=0.05
export SIMILARITY_METHOD=cosine

# Generation Configuration
export TEMPERATURE=0.7
export TOP_P=0.9
export MAX_TOKENS=2048

# Path Configuration
export DATA_DIR=/path/to/data
export PROFILES_DIR=/path/to/profiles
```

### 2. Logging Infrastructure (`logging.py`)

Provides structured logging with colored console output, file logging, and performance monitoring decorators.

#### Architecture

```python
class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""

def setup_logging(name, level, log_file, console) -> logging.Logger
def get_logger(name) -> logging.Logger
def log_performance(func)
def log_generation_metrics(metrics)
def log_profile_analysis(profile_name, metrics)
def log_api_request(method, path, status_code, duration)

class StructuredLogger:
    """Structured logger for better parsing and analysis"""
```

#### Color Scheme

- **DEBUG**: Cyan
- **INFO**: Green
- **WARNING**: Yellow
- **ERROR**: Red
- **CRITICAL**: Magenta

#### Usage Examples

**Basic Logging**

```python
from resonance_os.core.logging import get_logger

logger = get_logger(__name__)
logger.info("System initialized")
logger.warning("Performance degradation detected")
logger.error("Generation failed", exc_info=True)
```

**Setup Custom Logging**

```python
from resonance_os.core.logging import setup_logging
from pathlib import Path

logger = setup_logging(
    name="my_module",
    level="DEBUG",
    log_file=Path("logs/my_module.log"),
    console=True
)
```

**Performance Logging**

```python
from resonance_os.core.logging import log_performance

@log_performance
def expensive_operation():
    # This function's execution time will be logged
    time.sleep(1)
    return "result"

result = expensive_operation()
# Output: Function 'expensive_operation' completed in 1.001s
```

**Structured Logging**

```python
from resonance_os.core.logging import StructuredLogger

logger = StructuredLogger("my_module")

# Log events
logger.log_event("generation_started", prompt="AI technology", profile="professional")

# Log metrics
logger.log_metric("similarity_score", 0.95, dimension="emotional_valence")

# Log errors
logger.log_error("generation_failed", error_message="API timeout", retry_count=3)
```

**Specialized Logging Functions**

```python
from resonance_os.core.logging import (
    log_generation_metrics,
    log_profile_analysis,
    log_api_request
)

# Log generation metrics
log_generation_metrics({
    'similarity_score': 0.95,
    'drift_rate': 0.02,
    'corrections_made': 1,
    'tokens_generated': 500
})

# Log profile analysis
log_profile_analysis("professional", {
    'confidence': 0.92,
    'dimensions_analyzed': 10,
    'sample_count': 100
})

# Log API request
log_api_request("POST", "/generate", 200, 1.234)
```

### 3. Type Definitions (`types.py`)

Provides comprehensive type definitions using Pydantic BaseModel for type-safe operations throughout the system.

#### Architecture

```python
class SimilarityMethod(str, Enum)
class LogLevel(str, Enum)
class GenerationStatus(str, Enum)

class ResonanceVector(BaseModel)
class StyleProfile(BaseModel)
class GenerationConfig(BaseModel)
class FeedbackMetrics(BaseModel)
class GenerationResult(BaseModel)
class CorpusInfo(BaseModel)
class TrainingProgress(BaseModel)
class APIResponse(BaseModel)
class ProfileRequest(BaseModel)
class GenerationRequest(BaseModel)
class CorrectionAction(BaseModel)
class DriftAnalysis(BaseModel)
```

#### Key Type Classes

**SimilarityMethod**
- COSINE, EUCLIDEAN, MANHATTAN, PEARSON, SPEARMAN

**GenerationStatus**
- PENDING, GENERATING, COMPLETED, FAILED, CORRECTING

**ResonanceVector**
```python
class ResonanceVector(BaseModel):
    values: List[float]
    dimensions: List[str]
    confidence: float = 1.0
    created_at: datetime
    
    def to_numpy(self) -> np.ndarray
    @classmethod
    def from_numpy(cls, values, dimensions, confidence)
```

**StyleProfile**
```python
class StyleProfile(BaseModel):
    name: str
    description: Optional[str]
    resonance_vector: ResonanceVector
    emotional_curve: List[float]
    cadence_pattern: List[float]
    abstraction_preference: float
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

**GenerationConfig**
```python
class GenerationConfig(BaseModel):
    topic: str
    target_profile: StyleProfile
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    stop_sequences: Optional[List[str]]
    similarity_threshold: float = 0.92
    max_corrections: int = 3
    enable_feedback: bool = True
    enable_drift_detection: bool = True
```

**FeedbackMetrics**
```python
class FeedbackMetrics(BaseModel):
    similarity_score: float
    target_similarity: float
    drift_rate: float
    deviation_vector: List[float]
    correction_needed: bool
    correction_strength: float
    timestamp: datetime
```

**GenerationResult**
```python
class GenerationResult(BaseModel):
    content: str
    profile_used: StyleProfile
    config: GenerationConfig
    metrics: FeedbackMetrics
    status: GenerationStatus
    tokens_generated: int
    corrections_made: int
    generation_time: float
    created_at: datetime
```

#### Usage Examples

**Creating Resonance Vectors**

```python
from resonance_os.core.types import ResonanceVector
import numpy as np

# From list
vector = ResonanceVector(
    values=[0.5, 0.6, 0.7, 0.8, 0.5, 0.4, 0.6, 0.7],
    dimensions=RESONANCE_DIMENSIONS,
    confidence=0.95
)

# From numpy array
np_values = np.array([0.5, 0.6, 0.7, 0.8, 0.5, 0.4, 0.6, 0.7])
vector = ResonanceVector.from_numpy(np_values, RESONANCE_DIMENSIONS, confidence=0.95)

# Convert to numpy
np_array = vector.to_numpy()
```

**Creating Style Profiles**

```python
from resonance_os.core.types import StyleProfile, ResonanceVector

profile = StyleProfile(
    name="professional_tone",
    description="Professional business writing style",
    resonance_vector=vector,
    emotional_curve=[0.5, 0.6, 0.7, 0.6, 0.5],
    cadence_pattern=[0.5, 0.5, 0.5, 0.5],
    abstraction_preference=0.5,
    metadata={"industry": "business", "audience": "professional"}
)
```

**API Request/Response**

```python
from resonance_os.core.types import GenerationRequest, APIResponse

request = GenerationRequest(
    topic="AI technology benefits",
    profile_name="professional",
    max_tokens=2048,
    temperature=0.7,
    similarity_threshold=0.92
)

response = APIResponse(
    success=True,
    message="Generation successful",
    data=generation_result,
    errors=None
)
```

### 4. System Constants (`constants.py`)

Provides system-wide constants for resonance dimensions, thresholds, model configurations, and more.

#### Key Constants

**Resonance Dimensions**
```python
RESONANCE_DIMENSIONS = [
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
```

**Thresholds**
- `DEFAULT_RESONANCE_THRESHOLD`: 0.92
- `DEFAULT_DRIFT_THRESHOLD`: 0.05
- `MAX_CORRECTION_ATTEMPTS`: 3

**Generation Parameters**
- `DEFAULT_TEMPERATURE`: 0.7
- `DEFAULT_TOP_P`: 0.9
- `DEFAULT_MAX_TOKENS`: 2048
- `DEFAULT_BATCH_SIZE`: 32

**Model Configurations**
- `DEFAULT_OPENAI_MODEL`: "gpt-3.5-turbo"
- `DEFAULT_EMBEDDING_MODEL`: "text-embedding-ada-002"
- `DEFAULT_SPACY_MODEL`: "en_core_web_lg"

**Feature Weights**
```python
FEATURE_WEIGHTS = {
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
```

**Emotional Ranges**
```python
EMOTIONAL_RANGES = {
    "very_negative": (-1.0, -0.6),
    "negative": (-0.6, -0.2),
    "neutral": (-0.2, 0.2),
    "positive": (0.2, 0.6),
    "very_positive": (0.6, 1.0)
}
```

**Abstraction Levels**
```python
ABSTRACTION_LEVELS = {
    "very_concrete": 0.0,
    "concrete": 0.25,
    "moderate": 0.5,
    "abstract": 0.75,
    "very_abstract": 1.0
}
```

**Cadence Patterns**
```python
CADENCE_PATTERNS = {
    "steady": [0.5, 0.5, 0.5, 0.5],
    "building": [0.3, 0.4, 0.6, 0.8],
    "declining": [0.8, 0.6, 0.4, 0.3],
    "wave": [0.3, 0.7, 0.4, 0.8],
    "explosive": [0.2, 0.3, 0.9, 0.6]
}
```

#### Usage Examples

```python
from resonance_os.core.constants import (
    RESONANCE_DIMENSIONS,
    DEFAULT_RESONANCE_THRESHOLD,
    FEATURE_WEIGHTS,
    EMOTIONAL_RANGES,
    ABSTRACTION_LEVELS,
    CADENCE_PATTERNS
)

# Use resonance dimensions
for dimension in RESONANCE_DIMENSIONS:
    print(f"Dimension: {dimension}")

# Check emotional range
valence = 0.7
for level, (min_val, max_val) in EMOTIONAL_RANGES.items():
    if min_val <= valence <= max_val:
        print(f"Emotional level: {level}")

# Use cadence pattern
pattern = CADENCE_PATTERNS["building"]
print(f"Building pattern: {pattern}")
```

## Integration Points

The Advanced Core Systems module integrates with:

- **All Systems**: Provides configuration, logging, and types for all modules
- **Generation Systems**: Uses GenerationConfig and GenerationResult types
- **Profile Systems**: Uses StyleProfile and ResonanceVector types
- **API Systems**: Uses APIResponse and request types
- **Similarity Systems**: Uses SimilarityMethod enum and constants

## Usage Patterns

### Custom Configuration

```python
from resonance_os.core.config import get_config

config = get_config()

# Modify configuration at runtime
config.resonance.threshold = 0.95
config.generation.temperature = 0.8

# Access nested configuration
model = config.models.default_model
host = config.api.host
```

### Type-Safe Operations

```python
from resonance_os.core.types import GenerationConfig, StyleProfile, ResonanceVector
from resonance_os.core.constants import RESONANCE_DIMENSIONS

# Create type-safe configuration
config = GenerationConfig(
    topic="AI technology",
    target_profile=profile,
    similarity_threshold=0.92
)

# Validate configuration automatically
try:
    # Pydantic validates automatically
    result = generate(config)
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Structured Logging

```python
from resonance_os.core.logging import StructuredLogger

logger = StructuredLogger("generation")

# Log structured events
logger.log_event("generation_started", 
    prompt="AI technology",
    profile="professional",
    config=config.dict()
)

# Log metrics
logger.log_metric("similarity", 0.95, dimension="emotional_valence")
```

## Best Practices

1. **Use type hints**: Leverage type definitions for better code quality
2. **Environment variables**: Store sensitive data in environment variables
3. **Structured logging**: Use StructuredLogger for better log parsing
4. **Configuration validation**: Let Pydantic validate configuration
5. **Performance monitoring**: Use log_performance decorator for critical functions

## Common Issues

**Issue**: Configuration not loading from environment
**Solution**: Ensure .env file exists and is properly formatted

**Issue**: Log file not created
**Solution**: Check directory permissions and path configuration

**Issue**: Type validation errors
**Solution**: Ensure data types match Pydantic model expectations

**Issue**: Constants not updated
**Solution**: Reload configuration after modifying constants

## Future Enhancements

- **Configuration hot-reloading**: Automatic configuration reload on file changes
- **Distributed logging**: Integration with centralized logging systems
- **Advanced types**: More sophisticated type definitions
- **Configuration validation**: Enhanced validation rules
- **Log aggregation**: Built-in log aggregation and analysis

## Dependencies

```bash
pip install pydantic python-dotenv
```

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Generation Systems Guide](./generation-systems-guide.md)
- [API Systems Guide](./api-systems-guide.md)
