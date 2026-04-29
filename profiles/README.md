# ResonanceOS v6 Profiles Directory

This directory contains Human-Resonant Value (HRV) profiles and profile management utilities for ResonanceOS v6.

## Directory Structure

```
profiles/
├── README.md                      # This file
├── hr_profiles/                    # Main profiles directory
│   ├── README.md                  # Profiles documentation
│   ├── config.json               # Profile system configuration
│   ├── profile_generator.py      # Profile generation utilities
│   ├── profile_validator.py      # Profile validation utilities
│   └── default/                  # Default tenant profiles
│       ├── neutral_professional.json
│       ├── creative_storytelling.json
│       ├── marketing_enthusiastic.json
│       ├── tech_startup.json
│       └── persuasive_sales.json
└── [tenant_name]/                 # Additional tenant directories
    └── [profile_name].json
```

## HRV Profiles Overview

HRV profiles define the target characteristics for content generation using the 8-dimensional Human-Resonant Value system:

### HRV Dimensions

1. **Sentence Variance** (0.0-1.0) - Variety in sentence lengths and structures
2. **Emotional Valence** (-1.0 to 1.0) - Positive/negative sentiment balance  
3. **Emotional Intensity** (0.0-1.0) - Strength of emotional content
4. **Assertiveness Index** (0.0-1.0) - Confidence and directness
5. **Curiosity Index** (0.0-1.0) - Question and curiosity elements
6. **Metaphor Density** (0.0-1.0) - Metaphorical language usage
7. **Storytelling Index** (0.0-1.0) - Narrative and storytelling elements
8. **Active Voice Ratio** (0.0-1.0) - Active vs passive voice

## Available Profiles

### Default Profiles

| Profile | Description | Use Case | HRV Score |
|---------|-------------|----------|-----------|
| `neutral_professional` | Balanced professional tone | Business documents, reports | 0.54 |
| `creative_storytelling` | Creative and narrative focus | Stories, articles, blogs | 0.66 |
| `marketing_enthusiastic` | High-energy marketing | Campaigns, promotions | 0.66 |
| `tech_startup` | Technology and innovation | Tech docs, startups | 0.55 |
| `persuasive_sales` | Sales and conversion focus | Sales pages, proposals | 0.68 |

## Profile Management

### Using the Profile Manager

```python
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager

# Initialize profile manager
manager = HRVProfileManager("./profiles/hr_profiles")

# Load a profile
profile = manager.load_profile("default", "neutral_professional")

# Save a new profile
manager.save_profile("default", "my_profile", profile_data)

# List available profiles
profiles = manager.list_profiles("default")
```

### Profile Generation

Create new profiles from sample text:

```bash
python profile_generator.py --action create --text "Your sample text here" --output my_profile
```

Or from a file:

```bash
python profile_generator.py --action create --sample sample.txt --output my_profile
```

### Profile Validation

Validate profile structure and performance:

```bash
python profile_validator.py --action validate --profile neutral_professional
```

Analyze profile performance with test generation:

```bash
python profile_validator.py --action analyze --profile neutral_professional --samples 10
```

Compare two profiles:

```bash
python profile_validator.py --action compare --profile1 neutral_professional --profile2 creative_storytelling
```

### Profile Optimization

Optimize existing profiles based on goals:

```python
from profile_generator import HRVProfileGenerator

generator = HRVProfileGenerator()

# Load existing profile
profile = generator.load_profile("default", "neutral_professional")

# Optimize for higher engagement
optimization_goals = {
    "curiosity_index": 0.8,
    "storytelling_index": 0.7
}

optimized_profile = generator.optimize_profile(profile, optimization_goals)
generator.save_profile(optimized_profile, "default")
```

### Profile Blending

Create hybrid profiles by blending existing ones:

```bash
python profile_generator.py --action blend --profile1 neutral_professional --profile2 creative_storytelling --weight 0.7 --output blended_profile
```

## Multi-Tenant Support

ResonanceOS v6 supports multiple tenants with isolated profile sets:

```
hr_profiles/
├── default/           # Default tenant
├── tenant_a/          # Customer A's profiles
├── tenant_b/          # Customer B's profiles
└── tenant_c/          # Customer C's profiles
```

Each tenant can have:
- Up to 100 custom profiles
- Profile versioning
- Independent profile management
- Tenant-specific configurations

## Profile Configuration

The `config.json` file contains system-wide settings:

- HRV dimension definitions
- Validation rules
- Performance settings
- API configuration
- Default profile mappings

## Best Practices

### Profile Creation

1. **Start with Samples**: Use representative sample text for profile generation
2. **Test Thoroughly**: Validate profiles with multiple content types
3. **Iterate Gradually**: Make small adjustments and test results
4. **Document Purpose**: Include clear descriptions and use cases
5. **Version Control**: Use semantic versioning for updates

### Profile Management

1. **Regular Validation**: Periodically validate profile performance
2. **Backup Important Profiles**: Maintain backups of critical profiles
3. **Monitor Performance**: Track HRV achievement rates in production
4. **Update Based on Feedback**: Refine profiles based on user feedback
5. **Clean Up Regularly**: Remove unused or outdated profiles

### Multi-Tenant Usage

1. **Isolate Tenant Data**: Keep tenant profiles in separate directories
2. **Customize per Tenant**: Tailor profiles to specific tenant needs
3. **Monitor Usage**: Track profile usage patterns per tenant
4. **Provide Templates**: Offer starting templates for new tenants
5. **Maintain Standards**: Ensure consistency across tenant profiles

## Troubleshooting

### Common Issues

**Profile Validation Fails**
- Check JSON syntax and structure
- Verify HRV vector has 8 dimensions
- Ensure values are within valid ranges
- Validate required metadata fields

**Poor Performance Results**
- Check if HRV values are too extreme
- Verify profile matches intended use case
- Test with different content types
- Consider profile optimization

**Multi-Tenant Issues**
- Verify directory permissions
- Check tenant name formatting
- Validate profile file naming
- Ensure proper isolation

### Debug Tools

Use the validator utilities for debugging:

```bash
# Validate all profiles in a directory
python profile_validator.py --action batch_validate --directory ./hr_profiles/default

# Detailed performance analysis
python profile_validator.py --action analyze --profile my_profile --samples 20

# Compare with similar profiles
python profile_validator.py --action compare --profile1 my_profile --profile2 similar_profile
```

## API Integration

Profiles can be managed via the ResonanceOS API:

```python
import requests

# List profiles
response = requests.get("http://localhost:8000/profiles?tenant=default")
profiles = response.json()

# Load profile
response = requests.get("http://localhost:8000/profiles/default/neutral_professional")
profile = response.json()

# Create profile
profile_data = {...}
response = requests.post("http://localhost:8000/profiles", json=profile_data)
```

## Performance Monitoring

Monitor profile performance with built-in metrics:

- **HRV Achievement Rate**: How closely generated content matches target HRV
- **Success Rate**: Percentage of successful content generation
- **User Engagement**: Content performance metrics
- **Error Rates**: Generation failures and issues

Use the performance analysis tools to track these metrics over time.

## Security Considerations

- **Profile Isolation**: Ensure tenant profiles are properly isolated
- **Access Control**: Implement proper authentication for profile management
- **Validation**: Validate all profile data before storage
- **Audit Logging**: Track profile changes and access
- **Backup Security**: Secure backup of profile configurations

## Future Enhancements

Planned improvements to the profile system:

- **AI-Assisted Optimization**: Machine learning-based profile tuning
- **Dynamic Profiles**: Self-adjusting profiles based on performance
- **Profile Templates**: Pre-built templates for common use cases
- **Advanced Analytics**: Enhanced performance analytics and insights
- **Integration Tools**: Better integration with external systems

## Support

For profile-related issues:

1. Check the documentation in `hr_profiles/README.md`
2. Use the validation tools to diagnose problems
3. Review the configuration in `config.json`
4. Test with sample generation to verify performance
5. Contact support with detailed error information and profile data

## Version History

- **v1.0** - Initial profile system with 8-dimensional HRV
- **v1.1** - Added multi-tenant support and validation tools
- **v1.2** - Enhanced profile generation and optimization features
- **v1.3** - Added performance analysis and batch operations
