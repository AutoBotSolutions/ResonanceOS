# Core Systems Guide - ResonanceOS v6

## Overview

The Core Systems module provides the fundamental building blocks for the Human-Resonant Value (HRV) framework that powers ResonanceOS v6. This module defines the 8-dimensional HRV vector space, type definitions, and core data structures used throughout the system.

## System Components

### 1. HRV Constants (`hrv_constants.py`)

The HRV constants define the 8-dimensional vector space used to quantify human resonance in text content.

#### HRV Dimensions

The 8 HRV dimensions capture different aspects of human communication:

1. **Sentence Variance** (`sentence_variance`)
   - Description: Cadence and rhythm variation in sentence structure
   - Range: 0.0 - 1.0
   - Higher values indicate more varied sentence structures and rhythms
   - Impact: Creates more dynamic, engaging content flow

2. **Emotional Valence** (`emotional_valence`)
   - Description: Positive/negative sentiment balance
   - Range: 0.0 - 1.0
   - 0.0 = negative sentiment, 1.0 = positive sentiment
   - 0.5 = neutral sentiment
   - Impact: Controls emotional tone of generated content

3. **Emotional Intensity** (`emotional_intensity`)
   - Description: Strength of emotion expressed
   - Range: 0.0 - 1.0
   - Higher values indicate more passionate, intense language
   - Impact: Affects emotional engagement level

4. **Assertiveness Index** (`assertiveness_index`)
   - Description: Authoritative tone level
   - Range: 0.0 - 1.0
   - Higher values indicate more confident, authoritative language
   - Impact: Influences perceived expertise and confidence

5. **Curiosity Index** (`curiosity_index`)
   - Description: Curiosity and intrigue level
   - Range: 0.0 - 1.0
   - Higher values indicate more inquisitive, exploratory language
   - Impact: Creates engaging, thought-provoking content

6. **Metaphor Density** (`metaphor_density`)
   - Description: Metaphoric richness in language
   - Range: 0.0 - 1.0
   - Higher values indicate more figurative language use
   - Impact: Enhances creativity and vivid imagery

7. **Storytelling Index** (`storytelling_index`)
   - Description: Narrative engagement quality
   - Range: 0.0 - 1.0
   - Higher values indicate more compelling storytelling elements
   - Impact: Improves narrative flow and reader engagement

8. **Active Voice Ratio** (`active_voice_ratio`)
   - Description: Ratio of active vs passive sentence construction
   - Range: 0.0 - 1.0
   - 1.0 = all active voice, 0.0 = all passive voice
   - Impact: Affects readability and directness

#### Usage Example

```python
from resonance_os.core.hrv_constants import HRV_DIMENSIONS

# Access all dimensions
print(HRV_DIMENSIONS)
# ['sentence_variance', 'emotional_valence', 'emotional_intensity', 
#  'assertiveness_index', 'curiosity_index', 'metaphor_density', 
#  'storytelling_index', 'active_voice_ratio']

# Create a target HRV vector
target_hrv = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
# High variance, positive, intense, moderate assertiveness, 
# moderate curiosity, low metaphor, good storytelling, active voice
```

### 2. HRV Types (`hrv_types.py`)

Type definitions for HRV-related data structures to ensure type safety and compatibility across the system.

#### Type Aliases

- **HRVVector**: `List[float]`
  - Represents an 8-dimensional HRV vector
  - Example: `[0.5, 0.6, 0.7, 0.4, 0.5, 0.6, 0.7, 0.5]`
  - Always contains exactly 8 float values between 0.0 and 1.0

- **HRVProfile**: `Dict[str, Union[float, List[float], str]]`
  - Represents a complete HRV profile configuration
  - Contains profile metadata and HRV vectors
  - Example structure:
    ```python
    {
        "name": "professional_modern",
        "target_hrv": [0.5, 0.6, 0.7, 0.4, 0.5, 0.6, 0.7, 0.5],
        "description": "Modern professional tone",
        "created_at": "2026-03-09"
    }
    ```

#### Usage Example

```python
from resonance_os.core.hrv_types import HRVVector, HRVProfile

# Create an HRV vector
my_vector: HRVVector = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]

# Create an HRV profile
my_profile: HRVProfile = {
    "name": "creative_storyteller",
    "target_hrv": my_vector,
    "description": "Engaging narrative style",
    "category": "creative"
}
```

## System Architecture

```
Core Systems
├── hrv_constants.py (HRV dimension definitions)
└── hrv_types.py (Type definitions)
```

## Integration Points

The Core Systems module is used by:

- **Generation Systems**: For target HRV specification
- **Profile Systems**: For profile structure definitions
- **Similarity Systems**: For vector comparison operations
- **Profiling Systems**: For HRV extraction and analysis
- **API Systems**: For request/response type definitions

## Best Practices

1. **Always use type aliases** (`HRVVector`, `HRVProfile`) for type safety
2. **Validate HRV vectors** to ensure they contain exactly 8 values in [0.0, 1.0]
3. **Document HRV profiles** with clear descriptions of intended use cases
4. **Use dimension names** from `HRV_DIMENSIONS` for consistency
5. **Maintain backward compatibility** when modifying type definitions

## Common Operations

### Creating a Target HRV Vector

```python
from resonance_os.core.hrv_constants import HRV_DIMENSIONS
from resonance_os.core.hrv_types import HRVVector

# Define target for professional tone
professional_hrv: HRVVector = [
    0.4,  # sentence_variance (moderate)
    0.6,  # emotional_valence (slightly positive)
    0.5,  # emotional_intensity (moderate)
    0.7,  # assertiveness_index (confident)
    0.5,  # curiosity_index (balanced)
    0.3,  # metaphor_density (low)
    0.6,  # storytelling_index (good)
    0.8   # active_voice_ratio (mostly active)
]
```

### Validating an HRV Vector

```python
def validate_hrv_vector(vector: HRVVector) -> bool:
    """Validate that an HRV vector is properly formatted."""
    if len(vector) != 8:
        return False
    if not all(0.0 <= v <= 1.0 for v in vector):
        return False
    return True
```

## Performance Considerations

- HRV vectors are lightweight (8 floats per vector)
- Type checking adds minimal overhead
- No external dependencies required
- Suitable for real-time operations

## Future Enhancements

- Add validation functions for HRV vectors
- Include default profile templates
- Add dimension-specific constraint ranges
- Support for custom dimension definitions

## Troubleshooting

**Issue**: Type errors when passing HRV vectors
**Solution**: Ensure you're using the `HRVVector` type alias and passing a list of exactly 8 floats

**Issue**: Dimension mismatch errors
**Solution**: Verify your HRV vectors match the order in `HRV_DIMENSIONS`

**Issue**: Out-of-range HRV values
**Solution**: Validate that all values are between 0.0 and 1.0 before use

## References

- [Generation Systems Guide](./generation-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [Similarity Systems Guide](./similarity-systems-guide.md)
