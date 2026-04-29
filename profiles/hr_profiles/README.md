# HRV Profiles Directory

This directory contains Human-Resonant Value (HRV) profiles for ResonanceOS v6.

## Profile Structure

Each profile is stored as a JSON file with the following structure:

```json
{
  "name": "profile_name",
  "version": "1.0",
  "description": "Profile description",
  "target_hrv": [0.5, 0.3, 0.6, 0.7, 0.4, 0.5, 0.6, 0.8],
  "metadata": {
    "created_at": "2026-03-09T12:16:00Z",
    "created_by": "system",
    "tags": ["professional", "business", "formal"],
    "use_case": "Business documentation and reports"
  }
}
```

## HRV Dimensions

The 8-dimensional HRV vector represents:

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
- `neutral_professional.json` - Balanced professional tone
- `creative_storytelling.json` - Creative and narrative focus
- `marketing_enthusiastic.json` - High-energy marketing content
- `tech_startup.json` - Technology and innovation focus
- `persuasive_sales.json` - Sales and conversion focused

### Tenant-Specific Profiles
Each tenant can have their own subdirectory containing custom profiles:
```
hr_profiles/
├── default/
│   ├── neutral_professional.json
│   └── creative_storytelling.json
├── tenant_a/
│   ├── brand_voice.json
│   └── marketing_content.json
└── tenant_b/
    └── technical_docs.json
```

## Profile Management

Use the `HRVProfileManager` class to manage profiles:

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

## Profile Creation Guidelines

1. **Define Clear Use Cases** - Each profile should have a specific purpose
2. **Test HRV Values** - Validate profiles with sample content generation
3. **Document Metadata** - Include clear descriptions and tags
4. **Version Control** - Use version numbers for profile updates
5. **Tenant Isolation** - Keep tenant-specific profiles separate

## Best Practices

- Start with default profiles and modify values incrementally
- Test profiles with various content types before deployment
- Monitor HRV achievement rates in production
- Update profiles based on performance metrics
- Maintain backup copies of critical profiles

## Profile Validation

Profiles are automatically validated for:
- Correct JSON structure
- Valid HRV vector format (8 dimensions)
- Proper value ranges for each dimension
- Required metadata fields

Invalid profiles will be rejected with detailed error messages.
