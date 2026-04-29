# Data Systems Guide - ResonanceOS v6

## Overview

The Data Systems module provides comprehensive data management infrastructure for ResonanceOS v6, including configuration management, corpus storage, model persistence, profile storage, sample data management, and utility scripts. This module ensures organized, scalable data handling across the entire system.

## System Architecture

```
Data Systems
├── config/ (Configuration Files)
├── corpora/ (Text Corpora Storage)
├── exports/ (Exported Data)
├── logs/ (System Logs)
├── models/ (Model Storage)
├── profiles/ (Profile Storage)
├── samples/ (Sample Data)
└── scripts/ (Utility Scripts)
```

## System Components

### 1. Configuration (`config/`)

Stores system configuration files for various components.

#### Directory Structure

```
config/
├── default_config.yaml
├── model_config.yaml
└── api_config.yaml
```

#### Configuration Files

**default_config.yaml**
- System-wide settings
- Path configurations
- Default parameters
- Feature flags

**model_config.yaml**
- Model hyperparameters
- Training configurations
- Model paths
- Performance settings

**api_config.yaml**
- API endpoint configurations
- Rate limiting settings
- Authentication settings
- CORS configuration

#### Usage

Configuration files are loaded using the configuration management system:

```python
from resonance_os.core.config import get_config

config = get_config()
print(f"Profiles directory: {config.paths.profiles_dir}")
print(f"Model path: {config.models.model_path}")
```

### 2. Corpora (`corpora/`)

Stores text corpora for profile creation and analysis.

#### Directory Structure

```
corpora/
├── README.md
├── training/
│   ├── academic/
│   ├── business/
│   └── creative/
└── reference/
    ├── style_samples/
    └── domain_specific/
```

#### Corpus Organization

**Training Corpora**
- Domain-specific text samples
- Author-specific collections
- Genre-based groupings

**Reference Corpora**
- Style reference materials
- Benchmark texts
- Quality standards

#### Usage Example

```python
from resonance_os.resonance_os.profiling.corpus_loader import CorpusLoader

loader = CorpusLoader()
documents = loader.load_corpus("resonance_os/data/corpora/training/business")
```

### 3. Exports (`exports/`)

Stores exported data including profile exports, analysis results, and generated content.

#### Directory Structure

```
exports/
├── profiles/
│   ├── profile_exports.json
│   └── batch_exports/
├── analyses/
│   ├── corpus_analysis.json
│   └── drift_reports/
└── content/
    ├── generated_articles/
    └── batch_outputs/
```

#### Export Types

**Profile Exports**
- Individual profile exports
- Batch profile exports
- Backup exports

**Analysis Exports**
- Corpus analysis results
- Drift detection reports
- Statistical summaries

**Content Exports**
- Generated articles
- Batch processing outputs
- Quality assessment reports

#### Usage Example

```python
from resonance_os.resonance_os.profiling.profile_persistence import ProfilePersistence

persistence = ProfilePersistence()
persistence.export_profiles(
    Path("resonance_os/data/exports/profiles/profile_exports.json"),
    profile_names=["professional", "creative"]
)
```

### 4. Logs (`logs/`)

Stores system logs for debugging, monitoring, and auditing.

#### Directory Structure

```
logs/
├── application.log
├── generation.log
├── api.log
└── error.log
```

#### Log Files

**application.log**
- General application events
- System startup/shutdown
- Configuration changes

**generation.log**
- Content generation events
- HRV feedback data
- Performance metrics

**api.log**
- API request/response logs
- Authentication events
- Rate limiting events

**error.log**
- Error messages and stack traces
- Exception details
- Failure analysis

#### Usage Example

```python
from resonance_os.core.logging import get_logger

logger = get_logger(__name__)
logger.info("System initialized")
logger.error("Generation failed", exc_info=True)
```

### 5. Models (`models/`)

Stores trained models and model checkpoints.

#### Directory Structure

```
models/
├── README.md
├── hrf_models/
│   ├── hrf_model_v1.pkl
│   └── hrf_model_v2.pkl
├── rl_models/
│   ├── ppo_model_v1.pt
│   └── ppo_model_v2.pt
└── embeddings/
    ├── word_embeddings.npy
    └── sentence_embeddings.npy
```

#### Model Types

**HRF Models**
- Human-Resonance Feedback models
- Sentiment analysis models
- Engagement prediction models

**RL Models**
- PPO (Proximal Policy Optimization) models
- Reward models
- Policy checkpoints

**Embeddings**
- Word embeddings
- Sentence embeddings
- Contextual embeddings

#### Usage Example

```python
import pickle

# Load model
with open("resonance_os/data/models/hrf_models/hrf_model_v1.pkl", "rb") as f:
    model = pickle.load(f)

# Use model
prediction = model.predict(text)
```

### 6. Profiles (`profiles/`)

Stores HRV profiles for different writing styles and brand voices.

#### Directory Structure

```
profiles/
├── README.md
├── default/
│   ├── professional.json
│   ├── creative.json
│   └── technical.json
├── tenant_1/
│   ├── brand_voice.json
│   └── marketing_style.json
└── tenant_2/
    ├── corporate_tone.json
    └── academic_style.json
```

#### Profile Organization

**Default Profiles**
- System-provided profiles
- Common writing styles
- Benchmark profiles

**Tenant Profiles**
- Multi-tenant isolation
- Custom brand voices
- Organization-specific styles

#### Usage Example

```python
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager

manager = HRVProfileManager(Path("resonance_os/data/profiles"))
profile = manager.load_profile("default", "professional")
```

### 7. Samples (`samples/`)

Stores sample data for testing, demonstrations, and tutorials.

#### Directory Structure

```
samples/
├── README.md
├── text_samples/
│   ├── academic/
│   ├── business/
│   └── creative/
├── prompt_samples/
│   ├── generation_prompts.txt
│   └── analysis_prompts.txt
└── output_samples/
    ├── generated_content/
    └── analysis_results/
```

#### Sample Types

**Text Samples**
- Domain-specific examples
- Style reference texts
- Quality benchmarks

**Prompt Samples**
- Generation prompts
- Analysis prompts
- Tutorial examples

**Output Samples**
- Example generated content
- Analysis result examples
- Expected output formats

#### Usage Example

```python
from resonance_os.resonance_os.profiling.corpus_loader import CorpusLoader

loader = CorpusLoader()
samples = loader.load_corpus("resonance_os/data/samples/text_samples/business")
```

### 8. Scripts (`scripts/`)

Contains utility scripts for data management and system maintenance.

#### Directory Structure

```
scripts/
├── README.md
├── setup_data.py
├── backup_profiles.py
├── clean_logs.py
├── validate_profiles.py
└── export_reports.py
```

#### Script Descriptions

**setup_data.py**
- Initialize data directories
- Create default profiles
- Set up configuration files

**backup_profiles.py**
- Create profile backups
- Schedule regular backups
- Restore from backups

**clean_logs.py**
- Rotate log files
- Archive old logs
- Clean up temporary logs

**validate_profiles.py**
- Validate profile structure
- Check data integrity
- Report validation errors

**export_reports.py**
- Generate analysis reports
- Export statistics
- Create summaries

#### Usage Example

```bash
# Run setup script
python resonance_os/data/scripts/setup_data.py

# Create backup
python resonance_os/data/scripts/backup_profiles.py

# Validate profiles
python resonance_os/data/scripts/validate_profiles.py
```

## Integration Points

The Data Systems module integrates with:

- **Core Systems**: Provides configuration and logging
- **Profile Systems**: Uses profile storage directory
- **Profiling Systems**: Uses corpora for analysis
- **Generation Systems**: Stores models and generated content
- **API Systems**: Stores API logs and exports

## Usage Patterns

### Initial Setup

```python
from resonance_os.data.scripts.setup_data import setup_directories

# Initialize all data directories
setup_directories(base_path=Path("resonance_os/data"))
```

### Profile Management

```python
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.resonance_os.profiling.profile_persistence import ProfilePersistence

# Use profile storage
manager = HRVProfileManager(Path("resonance_os/data/profiles"))
persistence = ProfilePersistence(Path("resonance_os/data/profiles"))
```

### Corpus Analysis

```python
from resonance_os.resonance_os.profiling.corpus_loader import CorpusLoader

# Load and analyze corpus
loader = CorpusLoader()
documents = loader.load_corpus("resonance_os/data/corpora/training")
corpus_info = loader.analyze_corpus(documents)
```

### Model Management

```python
import pickle
from pathlib import Path

# Save model
with open("resonance_os/data/models/hrf_models/new_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Load model
with open("resonance_os/data/models/hrf_models/model.pkl", "rb") as f:
    model = pickle.load(f)
```

## Best Practices

1. **Organize by tenant**: Use tenant-specific directories for profiles
2. **Version models**: Include version numbers in model filenames
3. **Rotate logs**: Implement log rotation to prevent disk overflow
4. **Backup regularly**: Schedule regular profile and data backups
5. **Validate data**: Validate data integrity before use
6. **Document structure**: Keep README files updated with directory descriptions

## Common Issues

**Issue**: Permission denied accessing data directories
**Solution**: Check file permissions and ensure proper ownership

**Issue**: Out of disk space
**Solution**: Implement log rotation and clean old exports

**Issue**: Corrupted profile files
**Solution**: Use backup/restore functionality to recover

**Issue**: Missing model files
**Solution**: Ensure models are properly saved and paths are correct

## Performance Considerations

- **Profile storage**: Fast JSON/pickle operations
- **Corpus loading**: Use iterators for large corpora
- **Model loading**: Can be slow for large models
- **Log writing**: Asynchronous logging recommended

## Security Considerations

- **Access control**: Implement proper file permissions
- **Sensitive data**: Encrypt sensitive profile data
- **Backup security**: Secure backup storage
- **Log sanitization**: Remove sensitive information from logs

## Future Enhancements

- **Database integration**: Replace file-based storage with database
- **Cloud storage**: Support for cloud storage backends
- **Data versioning**: Git-like versioning for data
- **Automated cleanup**: Automatic old data cleanup
- **Data validation**: Comprehensive data validation framework
- **Monitoring**: Data usage monitoring and alerting

## Troubleshooting

**Issue**: Missing directories
**Solution**: Run setup script to create directories

**Issue**: Corrupted configuration files
**Solution**: Restore from backup or regenerate defaults

**Issue**: Model loading errors
**Solution**: Verify model format and dependencies

**Issue**: Profile not found
**Solution**: Check profile path and tenant directory

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [Profiling Systems Guide](./profiling-systems-guide.md)
