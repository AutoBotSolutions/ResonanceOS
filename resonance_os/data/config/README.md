# Configuration Directory

This directory contains all configuration files for ResonanceOS v6, including system settings, default profiles, and model parameters.

## 📁 Files Overview

### `default_profiles.json`
Contains 8 pre-configured HRV profiles for different use cases:

- **neutral_professional**: Balanced business communications
- **creative_storytelling**: Engaging narrative content
- **technical_academic**: Formal academic and technical writing
- **marketing_enthusiastic**: High-energy promotional content
- **empathetic_support**: Customer service and support content
- **news_journalistic**: Objective news and journalism
- **educational_tutorial**: Clear instructional content
- **persuasive_sales**: Conversion-focused sales content

### `system_config.json`
Complete system configuration including:
- System settings and debugging options
- HRV dimension definitions and thresholds
- API server configuration
- Profile management settings
- Logging and monitoring configuration
- Performance and security settings
- Feature flags and experimental options

### `model_settings.json`
Detailed model configuration:
- HRF model parameters and training settings
- Planner layer configuration
- Sentence generation parameters
- Refinement layer settings
- HRV extraction feature definitions
- Optimization and evaluation metrics

## 🔧 Configuration Guide

### Modifying System Settings

1. **API Configuration**
```json
{
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "timeout": 30
  }
}
```

2. **Performance Tuning**
```json
{
  "performance": {
    "cache_enabled": true,
    "cache_size": "1GB",
    "batch_processing": true,
    "max_workers": 4
  }
}
```

3. **Security Settings**
```json
{
  "security": {
    "encryption_enabled": false,
    "tenant_isolation": true,
    "audit_logging": true
  }
}
```

### Creating Custom Profiles

1. **Copy Default Template**
```bash
cp config/default_profiles.json config/custom_profiles.json
```

2. **Add Your Profile**
```json
{
  "profiles": {
    "your_profile": {
      "name": "Your Profile Name",
      "description": "Profile description",
      "hrv_vector": [0.6, 0.4, 0.7, 0.8, 0.5, 0.3, 0.4, 0.7],
      "metadata": {
        "category": "your_category",
        "formality": "professional",
        "use_cases": ["your_use_cases"]
      }
    }
  }
}
```

3. **Load Custom Profiles**
```bash
# Use custom profiles in API calls
curl -X POST "http://localhost:8000/hr_generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your prompt", "profile_name": "your_profile"}'
```

## 📊 HRV Vector Reference

Each HRV vector contains 8 dimensions:

| Index | Dimension | Range | Description |
|-------|-----------|-------|-------------|
| 0 | sentence_variance | 0.0-1.0 | Variety in sentence lengths |
| 1 | emotional_valence | -1.0-1.0 | Positive/negative sentiment |
| 2 | emotional_intensity | 0.0-1.0 | Strength of emotion |
| 3 | assertiveness_index | 0.0-1.0 | Confidence and directness |
| 4 | curiosity_index | 0.0-1.0 | Question and curiosity elements |
| 5 | metaphor_density | 0.0-1.0 | Metaphorical language usage |
| 6 | storytelling_index | 0.0-1.0 | Narrative elements |
| 7 | active_voice_ratio | 0.0-1.0 | Active vs passive voice |

## 🚀 Quick Start

### 1. Review Default Configuration
```bash
cat config/system_config.json
```

### 2. Customize for Your Environment
```bash
# Edit system configuration
nano config/system_config.json

# Edit model settings
nano config/model_settings.json
```

### 3. Test Configuration
```bash
# Test with default profile
python -c "
import json
from resonance_os.api.hr_server import hr_generate, SimpleRequest
request = SimpleRequest(prompt='Test prompt')
response = hr_generate(request)
print('Configuration working!')
"
```

### 4. Monitor Performance
```bash
# Check logs for configuration issues
tail -f logs/generation/generation_$(date +%Y_%m_%d).log
```

## 🔍 Configuration Validation

### Validate JSON Files
```bash
# Validate system configuration
python -c "import json; json.load(open('config/system_config.json'))"

# Validate profiles
python -c "import json; json.load(open('config/default_profiles.json'))"

# Validate model settings
python -c "import json; json.load(open('config/model_settings.json'))"
```

### Check Profile Schema
```bash
# Validate against schema
python -c "
import json
schema = json.load(open('data/profiles/schemas/profile_schema.json'))
profiles = json.load(open('config/default_profiles.json'))
# Validation logic here
"
```

## 🛠️ Advanced Configuration

### Environment-Specific Settings

Create environment-specific configurations:

```bash
# Development
cp config/system_config.json config/system_config_dev.json

# Production
cp config/system_config.json config/system_config_prod.json

# Testing
cp config/system_config.json config/system_config_test.json
```

### Feature Flags

Enable/disable experimental features:

```json
{
  "experimental": {
    "reinforcement_learning": false,
    "transformer_models": false,
    "multilingual_support": false
  }
}
```

### Performance Optimization

Fine-tune performance parameters:

```json
{
  "performance": {
    "cache_enabled": true,
    "cache_size": "2GB",
    "batch_processing": true,
    "batch_size": 64,
    "parallel_processing": true,
    "max_workers": 8
  }
}
```

## 📋 Configuration Checklist

- [ ] Review and customize `system_config.json`
- [ ] Verify HRV dimensions and thresholds
- [ ] Configure API settings for your environment
- [ ] Set up logging and monitoring
- [ ] Configure security and access controls
- [ ] Customize default profiles or create new ones
- [ ] Validate all JSON files
- [ ] Test configuration with sample requests
- [ ] Monitor system performance
- [ ] Set up backup and recovery procedures

## 🆘 Troubleshooting

### Common Issues

1. **Invalid JSON Format**
```bash
# Check JSON syntax
python -m json.tool config/system_config.json
```

2. **Missing HRV Dimensions**
```bash
# Verify vector length
python -c "
import json
profiles = json.load(open('config/default_profiles.json'))
for name, profile in profiles['profiles'].items():
    if len(profile['hrv_vector']) != 8:
        print(f'Invalid vector length in {name}')
"
```

3. **Configuration Not Loading**
```bash
# Check file permissions
ls -la config/

# Verify file paths
python -c "
import os
print('Current directory:', os.getcwd())
print('Config files:', os.listdir('config/'))
"
```

### Getting Help

- Check system logs: `logs/generation/`
- Validate configuration files
- Review documentation: `../README.md`
- Contact support: support@resonanceos.ai

## 🔧 Maintenance

### Regular Tasks
- Review and update configuration files
- Monitor performance metrics
- Validate profile effectiveness
- Update feature flags as needed

### Backup Configuration
```bash
# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz config/
```

### Version Control
```bash
# Track configuration changes
git add config/
git commit -m "Configuration updates"
```

This configuration directory provides complete control over ResonanceOS v6 behavior and performance.
