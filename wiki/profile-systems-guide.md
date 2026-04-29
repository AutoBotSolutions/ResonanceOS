# Profile Systems Guide - ResonanceOS v6

## Overview

The Profile Systems module provides multi-tenant profile management and HRV extraction capabilities for ResonanceOS v6. This module enables the creation, storage, and retrieval of HRV profiles that define brand voice and writing styles, as well as the extraction of HRV vectors from existing text content.

## System Architecture

```
Profile Systems
├── hrv_extractor.py (HRV Extraction)
├── multi_tenant_hr_profiles.py (Profile Management)
└── hr_profiles/ (Profile Storage)
```

## System Components

### 1. HRV Extractor (`hrv_extractor.py`)

Extracts 8-dimensional HRV vectors from text content through linguistic analysis.

#### Architecture

```python
class HRVExtractor:
    def extract(self, text: str) -> List[float]:
        # Extract HRV dimensions from text
        return [
            variance / 10.0,           # sentence_variance
            max(-1.0, min(1.0, sentiment * 10)),  # emotional_valence
            abs(sentiment * 10),       # emotional_intensity
            0.5,                       # assertiveness_index (placeholder)
            0.5,                       # curiosity_index (placeholder)
            0.1,                       # metaphor_density (placeholder)
            0.2,                       # storytelling_index (placeholder)
            0.7                        # active_voice_ratio (placeholder)
        ]
```

#### Extraction Methodology

The extractor analyzes text to compute:

1. **Sentence Variance**: Variance in sentence lengths
   - Calculated from sentence length statistics
   - Normalized to [0.0, 1.0] range
   - Higher values indicate more varied sentence structures

2. **Emotional Valence**: Sentiment analysis
   - Based on positive/negative word lists
   - Range: [-1.0, 1.0] normalized to [0.0, 1.0]
   - 0.5 = neutral, <0.5 = negative, >0.5 = positive

3. **Emotional Intensity**: Strength of emotion
   - Derived from absolute sentiment value
   - Range: [0.0, 1.0]
   - Higher values indicate more intense language

4-8. **Placeholder Dimensions**: Currently use fixed values
   - Assertiveness Index: 0.5 (moderate)
   - Curiosity Index: 0.5 (moderate)
   - Metaphor Density: 0.1 (low)
   - Storytelling Index: 0.2 (low)
   - Active Voice Ratio: 0.7 (mostly active)

#### Usage Example

```python
from resonance_os.profiles.hrv_extractor import HRVExtractor

extractor = HRVExtractor()
text = "The innovative technology transforms how we approach sustainable energy solutions."
hrv = extractor.extract(text)
print(f"HRV Vector: {hrv}")
```

#### Limitations

- **Simple sentiment**: Basic word-list approach, not ML-based
- **Placeholder dimensions**: Several dimensions use fixed values
- **No external dependencies**: Uses only standard library
- **Limited accuracy**: Suitable for basic use, not production

### 2. Multi-Tenant HR Profiles (`multi_tenant_hr_profiles.py`)

Manages HRV profiles with multi-tenant support for enterprise deployments.

#### Architecture

```python
class HRVProfileManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_profile(self, tenant: str, profile_name: str, hrv_vector: List[float]):
        # Save profile to tenant-specific directory

    def load_profile(self, tenant: str, profile_name: str) -> List[float]:
        # Load profile from tenant-specific directory

    def list_profiles(self, tenant: str) -> List[str]:
        # List all profiles for a tenant
```

#### Directory Structure

```
base_dir/
├── tenant_1/
│   ├── profile_a.json
│   ├── profile_b.json
│   └── ...
├── tenant_2/
│   ├── corporate_tone.json
│   ├── marketing_voice.json
│   └── ...
└── ...
```

#### Usage Examples

**Initialize Manager**

```python
from pathlib import Path
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager

manager = HRVProfileManager(Path("./profiles/hr_profiles"))
```

**Save Profile**

```python
hrv_vector = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
manager.save_profile("default", "professional", hrv_vector)
```

**Load Profile**

```python
profile = manager.load_profile("default", "professional")
print(f"Loaded profile: {profile}")
```

**List Profiles**

```python
profiles = manager.list_profiles("default")
print(f"Available profiles: {profiles}")
```

#### Profile Format

Profiles are stored as JSON files containing the 8-dimensional HRV vector:

```json
[0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
```

#### Multi-Tenant Support

The profile manager supports multiple tenants for enterprise deployments:

- **Tenant Isolation**: Each tenant has its own directory
- **Scalability**: Unlimited tenants supported
- **Security**: Tenant-specific profile access
- **Flexibility**: Different profiles per tenant

## Integration Points

The Profile Systems module integrates with:

- **Generation Systems**: Uses profiles for target HRV specification
- **API Systems**: Provides profile loading for API requests
- **CLI Systems**: Enables profile-based CLI generation
- **Core Systems**: Uses HRV types and constants

## Usage Patterns

### Creating Profiles from Existing Content

```python
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager

# Extract HRV from sample content
extractor = HRVExtractor()
sample_text = """
The company has developed an innovative approach to sustainable technology.
Our solutions transform how businesses approach environmental challenges.
We believe in creating lasting impact through practical implementation.
"""

hrv = extractor.extract(sample_text)

# Save as profile
manager = HRVProfileManager(Path("./profiles/hr_profiles"))
manager.save_profile("company_a", "brand_voice", hrv)
```

### Profile-Based Generation

```python
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.generation.human_resonant_writer import HumanResonantWriter

manager = HRVProfileManager(Path("./profiles/hr_profiles"))
profile = manager.load_profile("default", "professional")

writer = HumanResonantWriter()
# Use profile HRV for generation
# (Implementation depends on generation pipeline integration)
```

### Tenant-Specific Operations

```python
manager = HRVProfileManager(Path("./profiles/hr_profiles"))

# Company A profiles
manager.save_profile("company_a", "corporate", [0.5, 0.6, 0.7, 0.8, 0.4, 0.3, 0.5, 0.7])
manager.save_profile("company_a", "marketing", [0.7, 0.8, 0.6, 0.5, 0.6, 0.4, 0.7, 0.6])

# Company B profiles
manager.save_profile("company_b", "technical", [0.4, 0.5, 0.6, 0.7, 0.5, 0.2, 0.4, 0.8])
manager.save_profile("company_b", "casual", [0.8, 0.7, 0.6, 0.4, 0.7, 0.5, 0.8, 0.5])
```

## Profile Templates

### Professional Profile

```python
professional_hrv = [0.4, 0.6, 0.5, 0.7, 0.5, 0.3, 0.6, 0.8]
# Moderate variance, positive, moderate intensity, confident, balanced curiosity, 
# low metaphor, good storytelling, mostly active voice
```

### Creative Profile

```python
creative_hrv = [0.8, 0.7, 0.8, 0.4, 0.8, 0.7, 0.8, 0.6]
# High variance, positive, intense, less assertive, very curious, 
# high metaphor, excellent storytelling, moderate active voice
```

### Technical Profile

```python
technical_hrv = [0.3, 0.5, 0.4, 0.6, 0.5, 0.2, 0.3, 0.9]
# Low variance, neutral, low intensity, moderately assertive, balanced curiosity, 
# very low metaphor, low storytelling, mostly active voice
```

## Performance Considerations

- **HRV Extraction**: Fast, no external dependencies
- **Profile Loading**: Minimal overhead, JSON parsing
- **Profile Saving**: Fast, simple file I/O
- **Scalability**: File-based system, suitable for moderate use

## Best Practices

1. **Profile naming**: Use descriptive, consistent names
2. **Tenant organization**: Use meaningful tenant identifiers
3. **Profile validation**: Validate HRV vectors before saving
4. **Backup profiles**: Regular backups of profile directories
5. **Version control**: Track profile changes in version control

## Common Issues

**Issue**: Profile not found
**Solution**: Verify tenant and profile name are correct

**Issue**: Permission denied
**Solution**: Check file permissions on profile directory

**Issue**: Invalid HRV vector
**Solution**: Ensure vector has exactly 8 values in [0.0, 1.0]

**Issue**: Poor extraction quality
**Solution**: Use longer, more representative text samples

## Future Enhancements

- **ML-based extraction**: Replace word-list sentiment with ML model
- **Profile metadata**: Add description, tags, and creation timestamps
- **Profile versioning**: Support for profile versioning
- **Profile blending**: Blend multiple profiles for hybrid styles
- **Profile validation**: Comprehensive validation and error checking
- **Profile templates**: Pre-built profile templates for common styles
- **Profile search**: Search profiles by characteristics

## Troubleshooting

**Issue**: Empty HRV vector
**Solution**: Ensure input text is not empty or whitespace only

**Issue**: Out-of-range HRV values
**Solution**: Validate normalization in extraction logic

**Issue**: Directory creation errors
**Solution**: Check write permissions on base directory

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Generation Systems Guide](./generation-systems-guide.md)
- [API Systems Guide](./api-systems-guide.md)
