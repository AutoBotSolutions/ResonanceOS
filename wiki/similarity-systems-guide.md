# Similarity Systems Guide - ResonanceOS v6

## Overview

The Similarity Systems module provides comprehensive similarity metrics and drift detection capabilities for ResonanceOS v6. This module enables comparison of HRV vectors, detection of style drift over time, and analysis of content similarity using multiple mathematical approaches.

## System Architecture

```
Similarity Systems
├── metrics.py (Similarity Metrics)
└── drift.py (Drift Detection)
```

## System Components

### 1. Similarity Metrics (`metrics.py`)

Provides multiple similarity calculation methods for HRV vector comparison.

#### Architecture

```python
class SimilarityCalculator:
    """Calculates similarity between resonance vectors"""
    
    def __init__(self, default_method: SimilarityMethod = SimilarityMethod.COSINE):
        self.default_method = default_method
    
    def calculate_similarity(self, vector1, vector2, method=None, weights=None):
        """Calculate similarity between two resonance vectors"""
```

#### Similarity Methods

**COSINE** (default)
- Range: [0.0, 1.0]
- Measures cosine of angle between vectors
- 1.0 = identical direction, 0.0 = orthogonal
- Best for: General similarity assessment

**EUCLIDEAN**
- Range: [0.0, 1.0]
- Based on Euclidean distance
- 1.0 = identical, 0.0 = maximum distance
- Best for: Magnitude-sensitive comparison

**MANHATTAN**
- Range: [0.0, 1.0]
- Based on Manhattan distance
- 1.0 = identical, 0.0 = maximum distance
- Best for: Robust to outliers

**PEARSON**
- Range: [0.0, 1.0]
- Based on Pearson correlation
- 1.0 = perfect correlation, 0.0 = no correlation
- Best for: Pattern similarity

**SPEARMAN**
- Range: [0.0, 1.0]
- Based on Spearman rank correlation
- 1.0 = perfect rank correlation, 0.0 = no correlation
- Best for: Non-linear relationships

#### Usage Example

```python
from resonance_os.resonance_os.similarity.metrics import SimilarityCalculator, SimilarityMethod

calculator = SimilarityCalculator(SimilarityMethod.COSINE)

vec1 = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
vec2 = [0.6, 0.7, 0.7, 0.5, 0.5, 0.4, 0.5, 0.8]

similarity = calculator.calculate_similarity(vec1, vec2)
print(f"Cosine similarity: {similarity:.3f}")

# Try different method
euclidean_sim = calculator.calculate_similarity(vec1, vec2, SimilarityMethod.EUCLIDEAN)
print(f"Euclidean similarity: {euclidean_sim:.3f}")
```

#### Batch Operations

```python
# Calculate similarity for multiple candidates
target = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
candidates = [[0.4, 0.6, 0.7, 0.5, 0.4, 0.3, 0.6, 0.7] for _ in range(10)]

similarities = calculator.calculate_batch_similarity(target, candidates)

# Find most similar
most_similar = calculator.find_most_similar(target, candidates, top_k=3)
for idx, sim in most_similar:
    print(f"Candidate {idx}: similarity = {sim:.3f}")
```

#### Weighted Similarity

```python
# Weight dimensions differently
weights = {
    'sentence_variance': 0.2,
    'emotional_valence': 0.3,
    'emotional_intensity': 0.2,
    'assertiveness_index': 0.1,
    'curiosity_index': 0.1,
    'metaphor_density': 0.05,
    'storytelling_index': 0.05,
    'active_voice_ratio': 0.0
}

weighted_sim = calculator.calculate_similarity(vec1, vec2, weights=weights)
```

#### Dimension Contributions

```python
# Analyze which dimensions contribute most to similarity
contributions = calculator.calculate_dimension_contributions(vec1, vec2)
for dim, contribution in contributions.items():
    print(f"{dim}: {contribution:.3f}")
```

### 2. Multi-Method Similarity

Combines multiple similarity methods for robust comparison.

#### Architecture

```python
class MultiMethodSimilarity:
    """Calculates similarity using multiple methods and combines results"""
    
    def __init__(self, methods: List[SimilarityMethod], weights: Optional[List[float]] = None):
        self.methods = methods
        self.weights = weights or [1.0 / len(methods)] * len(methods)
```

#### Usage Example

```python
from resonance_os.resonance_os.similarity.metrics import MultiMethodSimilarity, SimilarityMethod

methods = [SimilarityMethod.COSINE, SimilarityMethod.EUCLIDEAN, SimilarityMethod.PEARSON]
weights = [0.4, 0.3, 0.3]

multi_sim = MultiMethodSimilarity(methods, weights)
results = multi_sim.calculate_combined_similarity(vec1, vec2)

print(f"Individual: {results['individual']}")
print(f"Combined: {results['combined']:.3f}")
print(f"Weights: {results['weights']}")

# Check consensus
consensus = multi_sim.get_method_consensus(vec1, vec2, threshold=0.92)
print(f"Consensus: {consensus['consensus_ratio']:.2f}")
print(f"Meets threshold: {consensus['meets_threshold']}")
```

### 3. Drift Detection (`drift.py`)

Detects and analyzes style drift in real-time using similarity measurements.

#### Architecture

```python
class DriftDetector:
    """Detects and analyzes style drift in real-time"""
    
    def __init__(
        self,
        window_size: int = 10,
        drift_threshold: float = 0.1,
        similarity_method: SimilarityMethod = SimilarityMethod.COSINE
    ):
        self.window_size = window_size
        self.drift_threshold = drift_threshold
        self.similarity_method = similarity_method
```

#### Key Features

- **Real-time monitoring**: Tracks similarity over time
- **Trend analysis**: Identifies improving/declining patterns
- **Severity assessment**: Categorizes drift severity
- **Predictive capability**: Predicts future drift
- **Adaptive thresholds**: Adjusts based on performance feedback

#### Usage Example

```python
from resonance_os.resonance_os.similarity.drift import DriftDetector

detector = DriftDetector(window_size=10, drift_threshold=0.1)

# Add measurements over time
target_vector = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]

for i in range(20):
    # Simulate gradual drift
    current_vector = [v + (i * 0.01) for v in target_vector]
    current_vector = [min(1.0, v) for v in current_vector]
    
    analysis = detector.add_measurement(current_vector, target_vector)
    print(f"Step {i}: similarity={analysis.current_similarity:.3f}, "
          f"drift_rate={analysis.drift_rate:.3f}, severity={analysis.severity}")
```

#### Drift Analysis Output

```python
DriftAnalysis(
    current_similarity=0.85,
    baseline_similarity=0.95,
    drift_rate=0.05,
    drift_direction="declining",
    affected_dimensions=["emotional_valence", "sentence_variance"],
    severity="medium",
    recommendation="monitor_and_adjust",
    timestamp=datetime.now()
)
```

#### Trend Analysis

```python
# Get drift trend over time
trend = detector.get_drift_trend(lookback=5)
print(f"Trend: {trend['trend']}")
print(f"Average similarity: {trend['average']:.3f}")
print(f"Variance: {trend['variance']:.3f}")
```

#### Drift Prediction

```python
# Predict future drift
prediction = detector.predict_drift(steps_ahead=5)
print(f"Prediction: {prediction['prediction']}")
print(f"Predicted similarities: {prediction['predicted_similarities']}")
print(f"Confidence: {prediction['confidence']:.3f}")
```

#### Statistics

```python
# Get comprehensive statistics
stats = detector.get_drift_statistics()
print(f"Total measurements: {stats['total_measurements']}")
print(f"Average drift rate: {stats['average_drift_rate']:.3f}")
print(f"Drift episodes: {stats['drift_episodes']}")
print(f"Drift frequency: {stats['drift_frequency']:.3f}")
```

#### Baseline Management

```python
# Reset baseline
detector.reset_baseline(new_baseline=target_vector)

# Export drift data
data = detector.export_drift_data()
```

### 4. Adaptive Drift Detector

Enhanced drift detector with adaptive threshold adjustment.

#### Architecture

```python
class AdaptiveDriftDetector(DriftDetector):
    """Adaptive drift detector that adjusts thresholds based on patterns"""
    
    def update_threshold(self, performance_feedback: Dict[str, Union[bool, float]]):
        """Update adaptive threshold based on performance feedback"""
```

#### Usage Example

```python
from resonance_os.resonance_os.similarity.drift import AdaptiveDriftDetector

adaptive_detector = AdaptiveDriftDetector(window_size=10)

# Provide feedback on detector performance
adaptive_detector.update_threshold({
    'false_positive': False,
    'false_negative': True
})

# Get adaptive statistics
stats = adaptive_detector.get_adaptive_statistics()
print(f"Current threshold: {stats['current_threshold']:.3f}")
print(f"Original threshold: {stats['original_threshold']:.3f}")
print(f"False positives: {stats['false_positives']}")
print(f"False negatives: {stats['false_negatives']}")
```

## Integration Points

The Similarity Systems module integrates with:

- **Core Systems**: Uses HRV types and constants
- **Profile Systems**: Compares profile HRV vectors
- **Generation Systems**: Assesses generation quality
- **Profiling Systems**: Measures drift in extracted HRV

## Usage Patterns

### Profile Matching

```python
from resonance_os.resonance_os.similarity.metrics import SimilarityCalculator

calculator = SimilarityCalculator()
target_hrv = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
profiles = {
    "professional": [0.5, 0.6, 0.7, 0.8, 0.4, 0.3, 0.5, 0.7],
    "creative": [0.8, 0.7, 0.6, 0.4, 0.8, 0.7, 0.8, 0.6],
    "technical": [0.4, 0.5, 0.6, 0.7, 0.5, 0.2, 0.4, 0.8]
}

similarities = {
    name: calculator.calculate_similarity(target_hrv, profile)
    for name, profile in profiles.items()
}

best_match = max(similarities, key=similarities.get)
print(f"Best match: {best_match} (similarity: {similarities[best_match]:.3f})")
```

### Quality Assessment

```python
# Compare generated HRV to target HRV
target_hrv = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
generated_hrv = [0.68, 0.62, 0.75, 0.52, 0.38, 0.32, 0.58, 0.72]

similarity = calculator.calculate_similarity(target_hrv, generated_hrv)
if similarity >= 0.92:
    print("Quality: Excellent")
elif similarity >= 0.85:
    print("Quality: Good")
else:
    print("Quality: Needs improvement")
```

### Drift Monitoring

```python
from resonance_os.resonance_os.similarity.drift import DriftDetector

detector = DriftDetector(window_size=20)

# Monitor generation over time
for generation in generations:
    current_hrv = extract_hrv(generation.content)
    analysis = detector.add_measurement(current_hrv, target_hrv)
    
    if analysis.severity == "high":
        print("WARNING: High drift detected!")
        print(f"Recommendation: {analysis.recommendation}")
        print(f"Affected dimensions: {analysis.affected_dimensions}")
```

## Performance Considerations

- **Similarity Calculator**: Fast, O(n) for n-dimensional vectors
- **Batch Operations**: Linear in number of candidates
- **Drift Detection**: Fast, O(window_size) for each measurement
- **Memory**: Minimal, uses deque for bounded history
- **Dependencies**: numpy, scipy, sklearn

## Best Practices

1. **Choose appropriate method**: Use COSINE for general similarity, EUCLIDEAN for magnitude-sensitive comparison
2. **Set appropriate thresholds**: Use domain knowledge to set drift thresholds
3. **Monitor trends**: Use drift detector for long-term monitoring
4. **Validate results**: Cross-check with human evaluation
5. **Use multi-method**: Combine methods for robust comparison

## Common Issues

**Issue**: NaN in Pearson correlation
**Solution**: Handle edge cases with try-except blocks

**Issue**: High false positive rate in drift detection
**Solution**: Use AdaptiveDriftDetector with threshold adjustment

**Issue**: Slow batch similarity calculation
**Solution**: Use vectorized operations or reduce candidate count

**Issue**: Inconsistent similarity across methods
**Solution**: Use MultiMethodSimilarity with consensus voting

## Future Enhancements

- **GPU acceleration**: CUDA support for large-scale operations
- **Advanced metrics**: Jensen-Shannon divergence, KL divergence
- **Temporal drift**: More sophisticated temporal modeling
- **Anomaly detection**: Unsupervised anomaly detection
- **Visualization**: Drift visualization and plotting

## Dependencies

```bash
pip install numpy scipy scikit-learn
```

## Troubleshooting

**Issue**: Import errors for scipy
**Solution**: Install with `pip install scipy`

**Issue**: Sklearn compatibility issues
**Solution**: Ensure compatible sklearn version

**Issue**: Memory errors with large datasets
**Solution**: Process in batches or reduce window size

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [Profiling Systems Guide](./profiling-systems-guide.md)
