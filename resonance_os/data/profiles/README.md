# Profiles Directory

This directory contains HRV (Human-Resonant Value) profiles, templates, schemas, and management tools for ResonanceOS v6. Profiles define the tonal and stylistic characteristics for content generation.

## 📁 Directory Structure

```
profiles/
├── README.md                    # This file
├── hr_profiles/                 # Active HRV profiles (auto-created)
│   ├── tenant1/                  # Tenant-specific profiles
│   │   ├── profile1.json        # HRV vector data
│   │   ├── profile2.json        # HRV vector data
│   │   └── metadata/             # Profile metadata
│   │       ├── profile1.json    # Full profile with metadata
│   │       └── profile2.json    # Full profile with metadata
│   └── tenant2/
├── schemas/                     # Profile validation schemas
│   └── profile_schema.json      # JSON schema for profile validation
├── templates/                   # Profile templates
│   ├── blank_profile.json       # Empty profile template
│   ├── business_template.json   # Business profile template
│   ├── creative_template.json   # Creative profile template
│   └── technical_template.json  # Technical profile template
└── examples/                    # Example profiles
    ├── tech_startup.json        # Technology startup example
    ├── lifestyle_blog.json      # Lifestyle blog example
    ├── academic_research.json   # Academic research example
    └── marketing_agency.json    # Marketing agency example
```

## 🎯 Profile Overview

### What is an HRV Profile?
An HRV profile defines the 8-dimensional vector that guides content generation:
- **Sentence Variance**: Variety in sentence lengths (0.0-1.0)
- **Emotional Valence**: Positive/negative sentiment balance (-1.0-1.0)
- **Emotional Intensity**: Strength of emotion (0.0-1.0)
- **Assertiveness Index**: Confidence and directness (0.0-1.0)
- **Curiosity Index**: Question and curiosity elements (0.0-1.0)
- **Metaphor Density**: Metaphorical language usage (0.0-1.0)
- **Storytelling Index**: Narrative elements (0.0-1.0)
- **Active Voice Ratio**: Active vs passive voice usage (0.0-1.0)

### Profile Structure
```json
{
  "name": "Profile Name",
  "description": "Detailed description of profile purpose",
  "hrv_vector": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
  "metadata": {
    "created_at": "2026-03-09T00:00:00Z",
    "updated_at": "2026-03-09T00:00:00Z",
    "version": "1.0",
    "category": "business|creative|academic|marketing",
    "formality": "formal|business|casual",
    "use_cases": ["specific_use_cases"],
    "target_audience": ["target_audience_types"],
    "brand_personality": ["personality_traits"],
    "tone_guidelines": {
      "vocabulary": ["preferred_words"],
      "sentence_style": "style_description",
      "emotional_tone": "tone_description",
      "persuasion_level": "low|moderate|high"
    }
  }
}
```

## 📋 Profile Categories

### Business Profiles
- **Professional Business**: Formal, balanced business communications
- **Tech Startup**: Innovative, confident technology content
- **Corporate Communications**: Official corporate messaging
- **Financial Reports**: Data-driven, analytical content

### Creative Profiles
- **Creative Storytelling**: Engaging narrative content
- **Marketing Content**: Persuasive, promotional writing
- **Lifestyle Blog**: Friendly, relatable content
- **Social Media**: Casual, engaging social content

### Academic Profiles
- **Academic Research**: Formal, scholarly writing
- **Technical Documentation**: Precise, technical content
- **Educational Content**: Clear, instructional writing
- **Research Papers**: Rigorous, academic content

### Specialized Profiles
- **Customer Support**: Empathetic, helpful content
- **News Journalism**: Objective, informative writing
- **Legal Content**: Precise, formal legal writing
- **Medical Content**: Professional, accurate medical writing

## 🔧 Profile Management

### Creating Profiles

#### Using Profile Generator Script
```bash
# Create profile from scratch
python data/scripts/profile_generator.py create \
  --tenant your_organization \
  --name your_profile \
  --description "Your profile description" \
  --vector "0.6,0.4,0.7,0.8,0.5,0.3,0.4,0.7"

# Create random profile
python data/scripts/profile_generator.py random \
  --tenant your_organization \
  --name random_profile \
  --description "Randomly generated profile"
```

#### Using Templates
```bash
# Copy template
cp profiles/templates/business_template.json profiles/your_custom_profile.json

# Edit template
nano profiles/your_custom_profile.json

# Load profile
python -c "
import json
profile = json.load(open('profiles/your_custom_profile.json'))
print(f'Profile created: {profile[\"name\"]}')
"
```

#### From Existing Content
```bash
# Create profile from text
python data/scripts/data_processing.py profile \
  --input your_content.txt \
  --output profiles/generated_profile.json \
  --profile-name "Generated Profile"
```

### Managing Profiles

#### Listing Profiles
```bash
# List all profiles for tenant
python data/scripts/profile_generator.py list \
  --tenant your_organization

# List with details
python -c "
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
manager = HRVProfileManager('./profiles/hr_profiles')
profiles = manager.list_profiles('your_organization')
for profile in profiles:
    print(f'Profile: {profile}')
"
```

#### Updating Profiles
```bash
# Adapt existing profile
python data/scripts/profile_generator.py adapt \
  --tenant your_organization \
  --profile1 existing_profile \
  --name adapted_profile \
  --adjustments "emotional_valence:0.2,assertiveness_index:0.1"

# Blend profiles
python data/scripts/profile_generator.py blend \
  --tenant your_organization \
  --profile1 profile1 \
  --profile2 profile2 \
  --weight1 0.6 \
  --weight2 0.4
```

#### Deleting Profiles
```bash
# Delete profile (manual)
rm -f profiles/hr_profiles/your_organization/profile_name.json
rm -f profiles/hr_profiles/your_organization/metadata/profile_name.json
```

### Profile Analysis

#### Comparing Profiles
```bash
# Analyze profile differences
python data/scripts/profile_generator.py analyze \
  --tenant your_organization \
  --profile1 profile1 \
  --profile2 profile2
```

#### Profile Performance
```bash
# Test profile with generation
python -c "
from resonance_os.api.hr_server import hr_generate, SimpleRequest
request = SimpleRequest(
    prompt='Test prompt',
    profile_name='your_profile'
)
response = hr_generate(request)
print(f'Generated content length: {len(response.article)}')
print(f'HRV Feedback: {response.hrv_feedback}')
"
```

## 📊 Profile Templates

### Blank Template (`templates/blank_profile.json`)
Basic template for creating custom profiles:
- Neutral HRV vector `[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]`
- Complete metadata structure
- Customizable guidelines and constraints

### Business Template (`templates/business_template.json`)
Professional business profile template:
- Formal tone with moderate assertiveness
- Balanced emotional content
- Professional vocabulary guidelines
- Business-specific use cases

### Creative Template (`templates/creative_template.json`)
Creative writing profile template:
- High storytelling and metaphor density
- Emotional and engaging content
- Creative vocabulary suggestions
- Artistic use cases

### Technical Template (`templates/technical_template.json`)
Technical documentation template:
- Formal, precise tone
- High active voice ratio
- Technical vocabulary
- Documentation use cases

## 🔍 Profile Validation

### Schema Validation
```bash
# Validate profile against schema
python -c "
import json
from jsonschema import validate, ValidationError

schema = json.load(open('profiles/schemas/profile_schema.json'))
profile = json.load(open('profiles/examples/tech_startup.json'))

try:
    validate(instance=profile, schema=schema)
    print('Profile validation: PASSED')
except ValidationError as e:
    print(f'Profile validation: FAILED - {e.message}')
"
```

### HRV Vector Validation
```bash
# Validate HRV vector format
python -c "
import json

def validate_hrv_vector(vector):
    if not isinstance(vector, list):
        return False, 'Vector must be a list'
    if len(vector) != 8:
        return False, 'Vector must have 8 dimensions'
    for i, value in enumerate(vector):
        if not isinstance(value, (int, float)):
            return False, f'Dimension {i} must be numeric'
        if not -1.0 <= value <= 1.0:
            return False, f'Dimension {i} must be between -1.0 and 1.0'
    return True, 'Vector is valid'

profile = json.load(open('profiles/examples/tech_startup.json'))
valid, message = validate_hrv_vector(profile['hrv_vector'])
print(f'HRV validation: {message}')
"
```

### Metadata Validation
```bash
# Validate profile metadata
python -c "
import json

def validate_metadata(metadata):
    required_fields = ['created_at', 'updated_at', 'version']
    for field in required_fields:
        if field not in metadata:
            return False, f'Missing required field: {field}'
    return True, 'Metadata is valid'

profile = json.load(open('profiles/examples/tech_startup.json'))
valid, message = validate_metadata(profile['metadata'])
print(f'Metadata validation: {message}')
"
```

## 🎨 Profile Customization

### Adjusting HRV Dimensions
```bash
# Fine-tune specific dimensions
python data/scripts/profile_generator.py adapt \
  --tenant your_organization \
  --profile1 base_profile \
  --name tuned_profile \
  --adjustments "emotional_valence:0.3,storytelling_index:0.2"
```

### Custom Tone Guidelines
```json
{
  "tone_guidelines": {
    "vocabulary": ["innovative", "disrupt", "scale", "optimize"],
    "sentence_style": "clear and direct with occasional complexity",
    "emotional_tone": "optimistic and confident",
    "persuasion_level": "moderate to high"
  }
}
```

### Constraints and Rules
```json
{
  "constraints": {
    "avoid": ["corporate jargon", "overly technical explanations"],
    "prefer": ["action-oriented language", "metrics and data"],
    "readability_level": "college-educated professional",
    "average_sentence_length": "15-20 words"
  }
}
```

### Adaptation Rules
```json
{
  "adaptation_rules": {
    "formal_contexts": {
      "adjustments": {
        "assertiveness_index": "+0.2",
        "emotional_valence": "-0.1"
      }
    },
    "casual_contexts": {
      "adjustments": {
        "curiosity_index": "+0.3",
        "storytelling_index": "+0.2"
      }
    }
  }
}
```

## 📈 Profile Analytics

### Usage Statistics
```bash
# Track profile usage
python -c "
import json
import os
from collections import Counter

# Analyze profile usage (placeholder for actual implementation)
usage_stats = {
    'tech_startup': 145,
    'professional_business': 234,
    'creative_storytelling': 89
}

print('Profile Usage Statistics:')
for profile, count in sorted(usage_stats.items(), key=lambda x: x[1], reverse=True):
    print(f'{profile}: {count} uses')
"
```

### Performance Metrics
```bash
# Analyze profile performance
python data/scripts/corpus_analyzer.py analyze \
  --input profiles/examples/ \
  --output profile_performance.json

# View performance results
python -c "
import json
performance = json.load(open('profile_performance.json'))
print('Profile Performance Metrics:')
for profile, metrics in performance.items():
    print(f'{profile}: {metrics[\"quality_score\"]:.3f}')
"
```

### A/B Testing
```bash
# Compare profile effectiveness
python data/scripts/profile_generator.py analyze \
  --tenant your_organization \
  --profile1 profile_a \
  --profile2 profile_b
```

## 🔧 Profile Maintenance

### Regular Updates
- Review profile effectiveness quarterly
- Update HRV vectors based on performance data
- Refresh metadata and guidelines
- Archive unused profiles

### Quality Assurance
- Validate all profiles against schema
- Test profiles with sample content
- Monitor HRV score distributions
- Check for profile drift

### Backup and Recovery
```bash
# Backup profiles
tar -czf profiles_backup_$(date +%Y%m%d).tar.gz profiles/hr_profiles/

# Restore profiles
tar -xzf profiles_backup_20260309.tar.gz
```

### Version Control
```bash
# Track profile changes
git add profiles/
git commit -m "Profile updates: new profiles and optimizations"

# Tag profile versions
git tag -a profiles_v1.1 -m "Profile collection version 1.1"
```

## 📋 Profile Development Guidelines

### Quality Standards
- **HRV Validation**: All dimensions within valid ranges
- **Metadata Completeness**: All required fields populated
- **Schema Compliance**: Valid against profile schema
- **Performance Testing**: Tested with sample content

### Naming Conventions
- Use lowercase with underscores: `tech_startup`
- Be descriptive and concise
- Include category prefix if needed: `business_professional`
- Avoid special characters and spaces

### Documentation Requirements
- Clear description of profile purpose
- Specific use case examples
- Tone and style guidelines
- Target audience specification

## 🆘 Troubleshooting

### Common Issues

1. **Profile Not Loading**
```bash
# Check profile existence
ls -la profiles/hr_profiles/your_organization/

# Validate profile format
python -c "
import json
try:
    profile = json.load(open('profiles/hr_profiles/your_organization/profile_name.json'))
    print('Profile format: VALID')
except Exception as e:
    print(f'Profile format error: {e}')
"
```

2. **Invalid HRV Vector**
```bash
# Check HRV vector
python -c "
import json
profile = json.load(open('profiles/examples/tech_startup.json'))
vector = profile['hrv_vector']
print(f'HRV Vector: {vector}')
print(f'Length: {len(vector)}')
print(f'Range: {min(vector):.3f} to {max(vector):.3f}')
"
```

3. **Generation Issues**
```bash
# Test profile with generation
python -c "
from resonance_os.api.hr_server import hr_generate, SimpleRequest
try:
    request = SimpleRequest(prompt='Test', profile_name='your_profile')
    response = hr_generate(request)
    print('Profile generation: SUCCESS')
except Exception as e:
    print(f'Profile generation error: {e}')
"
```

### Getting Help
- Review profile documentation
- Check profile schemas and templates
- Validate profile format
- Contact support: support@resonanceos.ai

## 📚 Profile Resources

### Documentation
- [Profile Schema](schemas/profile_schema.json) - Complete validation schema
- [Profile Templates](templates/) - Ready-to-use profile templates
- [Example Profiles](examples/) - Real-world profile examples

### Tools
- [Profile Generator](../scripts/profile_generator.py) - Profile management CLI
- [Data Processing](../scripts/data_processing.py) - Profile creation from content
- [Corpus Analyzer](../scripts/corpus_analyzer.py) - Profile analysis tools

### Best Practices
- Start with templates when creating new profiles
- Test profiles with sample content before deployment
- Monitor profile performance and usage
- Keep profile documentation up to date

This profiles directory provides comprehensive tools and resources for managing HRV profiles, enabling precise control over content generation style and tone in ResonanceOS v6.
