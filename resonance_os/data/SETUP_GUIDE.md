# ResonanceOS v6 Data Directory Setup Guide

This guide provides comprehensive instructions for setting up and configuring the data directory for ResonanceOS v6.

## 🚀 Quick Start

### 1. Directory Structure Creation
The data directory structure is automatically created when you first run ResonanceOS. However, you can create it manually:

```bash
mkdir -p /home/giganutt/artificial_intelligence/mimic/resonance_os/data/{config,samples,corpora,models,profiles,scripts,logs,exports}
```

### 2. Basic Configuration
Copy the sample configuration files:

```bash
cp config/default_profiles.json config/your_profiles.json
cp config/system_config.json config/your_system_config.json
```

### 3. Initialize Profiles
Create your first HRV profile:

```bash
python data/scripts/profile_generator.py create \
  --tenant your_organization \
  --name default_profile \
  --description "Default profile for general use" \
  --vector "0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5"
```

## 📁 Detailed Setup Instructions

### Configuration Files

#### System Configuration
Edit `config/system_config.json` to match your environment:

```json
{
  "system": {
    "name": "ResonanceOS v6",
    "debug": false,
    "log_level": "INFO"
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8000
  },
  "profiles": {
    "default_directory": "./data/profiles/hr_profiles"
  }
}
```

#### Default Profiles
Customize `config/default_profiles.json` for your specific use cases:

```json
{
  "profiles": {
    "your_custom_profile": {
      "name": "Your Custom Profile",
      "description": "Profile tailored to your needs",
      "hrv_vector": [0.6, 0.4, 0.7, 0.8, 0.5, 0.3, 0.4, 0.7]
    }
  }
}
```

### Sample Data Setup

#### Adding Sample Texts
Place your sample texts in `samples/sample_texts/`:

```bash
# Add business documents
cp your_business_report.txt samples/sample_texts/

# Add creative content
cp your_story.txt samples/sample_texts/
```

#### Creating Sample Profiles
Create profiles from your sample texts:

```bash
python data/scripts/data_processing.py profile \
  --input samples/sample_texts/ \
  --output samples/sample_profiles/your_profile.json \
  --profile-name "Your Generated Profile"
```

### Training Corpora Setup

#### Adding Training Data
Organize your training data in `corpora/`:

```bash
mkdir -p corpora/training corpora/validation corpora/test

# Add training documents
cp your_training_data/* corpora/training/

# Add validation documents
cp your_validation_data/* corpora/validation/
```

#### Corpus Format
Ensure your corpus files follow the JSON format:

```json
{
  "name": "Your Corpus",
  "documents": [
    {
      "id": "doc_001",
      "title": "Document Title",
      "content": "Document content...",
      "metadata": {
        "author": "Author Name",
        "date": "2026-03-09"
      }
    }
  ]
}
```

### Model Files Setup

#### HRF Model Configuration
Configure your HRF model in `models/hrf_models/`:

```bash
# Update model metadata
cp models/hrf_models/model_metadata.json models/hrf_models/your_model_metadata.json
```

#### Model Training
Train custom models using the provided scripts:

```bash
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output models/analysis_results.json
```

### Profile Management

#### Creating Custom Profiles
Use the profile generator to create custom profiles:

```bash
# Create profile from scratch
python data/scripts/profile_generator.py random \
  --tenant your_org \
  --name creative_profile \
  --description "Creative writing profile"

# Blend existing profiles
python data/scripts/profile_generator.py blend \
  --tenant your_org \
  --profile1 professional_business \
  --profile2 creative_storytelling \
  --weight1 0.6 \
  --weight2 0.4
```

#### Profile Templates
Use templates in `profiles/templates/`:

```bash
cp profiles/templates/blank_profile.json profiles/your_custom_profile.json
# Edit the file to customize your profile
```

### Script Usage

#### Data Processing
Process text files and extract HRV features:

```bash
python data/scripts/data_processing.py process \
  --input your_text_files/ \
  --output processed_results.json \
  --format json
```

#### Corpus Analysis
Analyze your text corpora:

```bash
python data/scripts/corpus_analyzer.py analyze \
  --input your_corpus/ \
  --output corpus_analysis.json
```

#### Batch Processing
Process multiple requests efficiently:

```bash
python data/scripts/batch_processor.py generate \
  --input batch_requests.json \
  --output batch_results.json \
  --workers 4
```

### Logging Setup

#### Configure Logging
Set up logging directories:

```bash
mkdir -p logs/{generation,api,performance,errors}
```

#### Log Rotation
Configure log rotation in `config/system_config.json`:

```json
{
  "logging": {
    "log_rotation": true,
    "max_log_size": "100MB",
    "max_log_files": 10
  }
}
```

### Analytics and Monitoring

#### Enable Analytics
Configure analytics collection:

```json
{
  "monitoring": {
    "metrics_enabled": true,
    "performance_metrics": true,
    "usage_analytics": true
  }
}
```

#### Dashboard Access
View the HRV dashboard:

```bash
# Open in browser
open data/exports/visualizations/hrv_dashboard.html
```

### Backup and Recovery

#### Automated Backups
Set up automated backups:

```bash
# Create backup script
echo "python data/scripts/backup_data.py" > backup_script.sh
chmod +x backup_script.sh

# Add to cron job for daily backups
crontab -e
# Add: 0 2 * * * /path/to/backup_script.sh
```

#### Manual Backup
Create manual backup:

```bash
python data/scripts/backup_data.py \
  --output backups/manual_backup_$(date +%Y%m%d).tar.gz
```

## 🔧 Advanced Configuration

### Performance Tuning

#### Batch Processing Optimization
Configure batch processing settings:

```json
{
  "performance": {
    "batch_processing": true,
    "batch_size": 32,
    "parallel_processing": true,
    "max_workers": 4
  }
}
```

#### Memory Management
Configure memory limits:

```json
{
  "performance": {
    "memory_limit": "4GB",
    "cache_size": "1GB"
  }
}
```

### Security Configuration

#### Enable Encryption
Configure data encryption:

```json
{
  "security": {
    "encryption_enabled": true,
    "api_key_required": true,
    "tenant_isolation": true
  }
}
```

#### Access Control
Set up access controls:

```json
{
  "security": {
    "rate_limiting": true,
    "max_requests_per_minute": 100
  }
}
```

## 🧪 Testing Your Setup

### Verify Installation
Test your setup with the provided scripts:

```bash
# Test data processing
python data/scripts/data_processing.py single \
  --input samples/sample_texts/business_report.txt

# Test profile generation
python data/scripts/profile_generator.py list \
  --tenant your_organization

# Test batch processing
echo '{"prompts": ["Test prompt 1", "Test prompt 2"]}' > test_batch.json
python data/scripts/batch_processor.py generate \
  --input test_batch.json \
  --output test_results.json
```

### Run System Tests
Execute the comprehensive test suite:

```bash
cd /home/giganutt/artificial_intelligence/mimic
python -m resonance_os.tests.run_all_tests
```

## 📊 Monitoring and Maintenance

### Daily Tasks
- Check system logs for errors
- Monitor performance metrics
- Verify backup completion
- Review analytics reports

### Weekly Tasks
- Update training corpora
- Optimize profile performance
- Clean up old log files
- Review usage statistics

### Monthly Tasks
- Update system configuration
- Re-train models if needed
- Archive old data
- Performance optimization

## 🆘 Troubleshooting

### Common Issues

#### Profile Not Found
```bash
# Check profile directory
ls -la data/profiles/hr_profiles/

# Recreate profile
python data/scripts/profile_generator.py create \
  --tenant your_tenant \
  --name missing_profile \
  --vector "0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5"
```

#### Generation Errors
```bash
# Check logs
tail -f logs/generation/generation_$(date +%Y_%m_%d).log

# Verify configuration
python -c "import json; print(json.load(open('data/config/system_config.json')))"
```

#### Performance Issues
```bash
# Check system resources
python data/scripts/batch_processor.py metrics

# Optimize configuration
# Reduce max_workers or batch_size in config
```

### Getting Help

#### Check Documentation
- Main README: `data/README.md`
- Schema definitions: `data/profiles/schemas/`
- Script help: `python data/scripts/script_name.py --help`

#### Contact Support
- Technical support: support@resonanceos.ai
- Documentation: docs@resonanceos.ai
- Community: community.resonanceos.ai

## 📚 Additional Resources

### Documentation
- [API Documentation](../api/docs/)
- [CLI Guide](../cli/README.md)
- [Test Suite](../tests/README.md)

### Examples
- [Sample Profiles](samples/sample_profiles/)
- [Example Corpora](corpora/training/)
- [Analytics Reports](exports/analytics/)

### Tools
- [Data Processing Scripts](scripts/)
- [Profile Generator](scripts/profile_generator.py)
- [Batch Processor](scripts/batch_processor.py)

This setup guide should help you get your ResonanceOS v6 data directory properly configured and ready for production use.
