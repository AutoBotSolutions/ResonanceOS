# Utility Systems Guide - ResonanceOS v6

## Overview

The Utility Systems module provides helper functions and tools for HRV computation and text emotion analysis. These utilities support the core functionality of ResonanceOS v6 by providing essential calculations and text processing capabilities.

## System Architecture

```
Utility Systems
├── hrv_utils.py (HRV Computation Utilities)
└── text_emotion_tools.py (Text Emotion Analysis)
```

## System Components

### 1. HRV Utils (`hrv_utils.py`)

Provides HRV vector similarity computation using cosine similarity.

#### Architecture

```python
import numpy as np

def compute_hrv_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute cosine similarity between two HRV vectors"""
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
```

#### Cosine Similarity

Cosine similarity measures the cosine of the angle between two vectors:

- **Range**: [-1.0, 1.0]
- **1.0**: Identical direction (perfect similarity)
- **0.0**: Orthogonal (no similarity)
- **-1.0**: Opposite direction (inverse similarity)

For HRV vectors (all values in [0.0, 1.0]), similarity typically ranges [0.0, 1.0].

#### Usage Example

```python
import numpy as np
from resonance_os.utils.hrv_utils import compute_hrv_similarity

vec1 = np.array([0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7])
vec2 = np.array([0.6, 0.7, 0.7, 0.5, 0.5, 0.4, 0.5, 0.8])

similarity = compute_hrv_similarity(vec1, vec2)
print(f"Similarity: {similarity:.3f}")
```

#### Applications

- **Profile Matching**: Find profiles similar to target HRV
- **Quality Assessment**: Compare generated HRV to target HRV
- **Clustering**: Group similar HRV vectors
- **Recommendation**: Suggest similar profiles

#### Performance Considerations

- **Fast**: O(n) computation where n is vector dimension
- **Memory**: Minimal memory footprint
- **Dependencies**: Requires numpy for vector operations

### 2. Text Emotion Tools (`text_emotion_tools.py`)

Provides sentiment analysis and emotion intensity computation using TextBlob.

#### Architecture

```python
from textblob import TextBlob

def sentiment_score(text: str) -> float:
    """Compute sentiment polarity score for text"""
    return TextBlob(text).sentiment.polarity

def emotion_intensity(text: str) -> float:
    """Compute emotion intensity from sentiment polarity"""
    return abs(TextBlob(text).sentiment.polarity)
```

#### Sentiment Score

**Range**: [-1.0, 1.0]
- **-1.0**: Very negative sentiment
- **0.0**: Neutral sentiment
- **1.0**: Very positive sentiment

#### Emotion Intensity

**Range**: [0.0, 1.0]
- **0.0**: No emotional content
- **1.0**: Maximum emotional intensity

#### Usage Example

```python
from resonance_os.utils.text_emotion_tools import sentiment_score, emotion_intensity

text = "The innovative technology transforms how we approach sustainable energy solutions."

sentiment = sentiment_score(text)
intensity = emotion_intensity(text)

print(f"Sentiment: {sentiment:.3f}")
print(f"Intensity: {intensity:.3f}")
```

#### Applications

- **HRV Extraction**: Compute emotional valence and intensity dimensions
- **Content Analysis**: Analyze emotional tone of text
- **Quality Control**: Verify emotional alignment with targets
- **A/B Testing**: Compare emotional content across variants

#### Dependencies

- **TextBlob**: Natural language processing library
- **NLTK**: Underlying NLP library (TextBlob dependency)

#### Installation

```bash
pip install textblob
python -m textblob.download_corpora
```

## Integration Points

The Utility Systems module integrates with:

- **Profile Systems**: Used for HRV similarity computation
- **Generation Systems**: Used for quality assessment
- **Similarity Systems**: Provides core similarity metrics
- **Profiling Systems**: Used in HRV extraction pipeline

## Usage Patterns

### Profile Similarity Search

```python
import numpy as np
from resonance_os.utils.hrv_utils import compute_hrv_similarity

target_hrv = np.array([0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7])
profiles = {
    "professional": np.array([0.5, 0.6, 0.7, 0.8, 0.4, 0.3, 0.5, 0.7]),
    "creative": np.array([0.8, 0.7, 0.6, 0.4, 0.8, 0.7, 0.8, 0.6]),
    "technical": np.array([0.4, 0.5, 0.6, 0.7, 0.5, 0.2, 0.4, 0.8])
}

similarities = {
    name: compute_hrv_similarity(target_hrv, profile)
    for name, profile in profiles.items()
}

best_match = max(similarities, key=similarities.get)
print(f"Best match: {best_match} (similarity: {similarities[best_match]:.3f})")
```

### Batch Similarity Computation

```python
import numpy as np
from resonance_os.utils.hrv_utils import compute_hrv_similarity

def batch_similarity(target: np.ndarray, candidates: list) -> list:
    """Compute similarity for multiple candidates"""
    return [compute_hrv_similarity(target, c) for c in candidates]

candidates = [np.random.rand(8) for _ in range(100)]
target = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])

similarities = batch_similarity(target, candidates)
```

### Text Emotion Analysis

```python
from resonance_os.utils.text_emotion_tools import sentiment_score, emotion_intensity

texts = [
    "I love this amazing product!",
    "This is terrible and awful.",
    "The product works as expected."
]

for text in texts:
    sentiment = sentiment_score(text)
    intensity = emotion_intensity(text)
    print(f"Text: {text}")
    print(f"Sentiment: {sentiment:.3f}, Intensity: {intensity:.3f}")
    print()
```

## Performance Considerations

- **HRV Utils**: Fast, numpy-optimized operations
- **Text Emotion Tools**: Moderate speed, depends on text length
- **Memory**: Minimal memory footprint
- **Scalability**: Suitable for batch processing

## Best Practices

1. **Validate inputs**: Ensure vectors are numpy arrays with correct dimensions
2. **Handle edge cases**: Check for zero-length vectors
3. **Batch operations**: Use vectorized operations for efficiency
4. **Error handling**: Wrap TextBlob calls in try-except blocks
5. **Cache results**: Cache sentiment analysis for repeated texts

## Common Issues

**Issue**: Zero division error in similarity computation
**Solution**: Add check for zero-norm vectors

**Issue**: TextBlob import error
**Solution**: Install TextBlob and download corpora

**Issue**: Slow sentiment analysis on long texts
**Solution**: Process in chunks or use sampling

**Issue**: Inconsistent sentiment results
**Solution**: Ensure TextBlob corpora are properly downloaded

## Future Enhancements

- **Alternative similarity metrics**: Euclidean, Manhattan, etc.
- **Advanced emotion models**: VADER, transformer-based models
- **Batch processing**: Optimized batch operations
- **Caching**: Built-in result caching
- **GPU acceleration**: CUDA support for large-scale operations

## Troubleshooting

**Issue**: Import errors for numpy
**Solution**: Install with `pip install numpy`

**Issue**: TextBlob corpora not found
**Solution**: Run `python -m textblob.download_corpora`

**Issue**: Unexpected similarity values
**Solution**: Verify input vectors are normalized to [0.0, 1.0]

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [Similarity Systems Guide](./similarity-systems-guide.md)
