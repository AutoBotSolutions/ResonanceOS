# Scripts Directory

This directory contains utility scripts for data processing, profile management, corpus analysis, and batch operations in ResonanceOS v6.

## 📁 Directory Structure

```
scripts/
├── README.md                    # This file
├── data_processing.py          # Data processing and HRV extraction utilities
├── profile_generator.py        # Profile creation and management tools
├── corpus_analyzer.py          # Comprehensive corpus analysis tools
├── batch_processor.py          # High-performance batch operations
├── backup_data.py              # Data backup and recovery utilities
├── validate_system.py          # System validation and health checks
└── performance_monitor.py       # Performance monitoring and reporting
```

## 🛠️ Script Overview

### Data Processing (`data_processing.py`)
Comprehensive data processing utilities for ResonanceOS v6.

**Key Features:**
- HRV vector extraction from text
- Corpus processing and analysis
- Profile creation from content
- Data export in multiple formats
- Quality assessment and metrics

**Usage Examples:**
```bash
# Process single text file
python data/scripts/data_processing.py single \
  --input samples/sample_texts/business_report.txt

# Process entire directory
python data/scripts/data_processing.py process \
  --input samples/sample_texts/ \
  --output processed_results.json

# Create profile from corpus
python data/scripts/data_processing.py profile \
  --input corpora/training/sample_business_corpus.json \
  --output business_profile.json

# Analyze corpus quality
python data/scripts/data_processing.py analyze \
  --input corpora/training/ \
  --output corpus_analysis.json
```

### Profile Generator (`profile_generator.py`)
Advanced profile management and generation tools.

**Key Features:**
- Create profiles from HRV vectors
- Generate random profiles with constraints
- Blend multiple profiles
- Adapt existing profiles
- Profile comparison and analysis
- Batch profile operations

**Usage Examples:**
```bash
# Create profile from vector
python data/scripts/profile_generator.py create \
  --tenant your_org \
  --name my_profile \
  --vector "0.6,0.4,0.7,0.8,0.5,0.3,0.4,0.7"

# Generate random profile
python data/scripts/profile_generator.py random \
  --tenant your_org \
  --name random_profile \
  --constraints "emotional_valence:0.5:1.0"

# Blend two profiles
python data/scripts/profile_generator.py blend \
  --tenant your_org \
  --profile1 profile1 \
  --profile2 profile2 \
  --weight1 0.6 \
  --weight2 0.4

# Adapt existing profile
python data/scripts/profile_generator.py adapt \
  --tenant your_org \
  --profile1 base_profile \
  --name adapted_profile \
  --adjustments "emotional_valence:0.2,assertiveness_index:0.1"

# List all profiles
python data/scripts/profile_generator.py list \
  --tenant your_org

# Analyze profile differences
python data/scripts/profile_generator.py analyze \
  --tenant your_org \
  --profile1 profile1 \
  --profile2 profile2
```

### Corpus Analyzer (`corpus_analyzer.py`)
Advanced text corpus analysis and insights generation.

**Key Features:**
- Comprehensive linguistic analysis
- HRV pattern identification
- Content classification
- Readability assessment
- Quality metrics calculation
- Trend analysis and recommendations

**Usage Examples:**
```bash
# Analyze single text
python data/scripts/corpus_analyzer.py single \
  --input samples/sample_texts/business_report.txt

# Analyze entire corpus
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output corpus_analysis.json

# Generate recommendations
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output recommendations.json
```

### Batch Processor (`batch_processor.py`)
High-performance batch processing for large-scale operations.

**Key Features:**
- Parallel content generation
- Batch HRV extraction
- Multi-tenant profile operations
- Performance optimization
- Resource management
- Progress monitoring

**Usage Examples:**
```bash
# Batch content generation
python data/scripts/batch_processor.py generate \
  --input batch_requests.json \
  --output batch_results.json \
  --workers 4

# Batch HRV extraction
python data/scripts/batch_processor.py extract_hrv \
  --input batch_texts.json \
  --output hrv_results.json

# Batch profile creation
python data/scripts/batch_processor.py create_profiles \
  --input profile_data.json \
  --tenant your_org

# System metrics
python data/scripts/batch_processor.py metrics
```

## 🚀 Quick Start Guide

### Environment Setup
```bash
# Ensure Python path includes project root
export PYTHONPATH="/home/giganutt/artificial_intelligence/mimic:$PYTHONPATH"

# Verify script installation
python data/scripts/data_processing.py --help
```

### Basic Workflow
```bash
# 1. Process sample data
python data/scripts/data_processing.py process \
  --input samples/sample_texts/ \
  --output sample_analysis.json

# 2. Create custom profile
python data/scripts/profile_generator.py create \
  --tenant demo_org \
  --name demo_profile \
  --vector "0.6,0.4,0.7,0.8,0.5,0.3,0.4,0.7"

# 3. Analyze corpus
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output corpus_insights.json

# 4. Batch processing
echo '{"prompts": ["Test prompt 1", "Test prompt 2"]}' > batch_input.json
python data/scripts/batch_processor.py generate \
  --input batch_input.json \
  --output batch_output.json
```

## 📊 Script Capabilities

### Data Processing Capabilities

#### Text Analysis
- **HRV Extraction**: 8-dimensional vector extraction
- **Linguistic Features**: Sentiment, readability, complexity
- **Content Classification**: Automatic category detection
- **Quality Assessment**: Overall content quality scoring

#### Data Export Formats
- **JSON**: Structured data with full metadata
- **CSV**: Tabular format for spreadsheet analysis
- **Custom**: Configurable output formats

#### Quality Metrics
- **HRV Alignment**: How well content matches target HRV
- **Readability**: Flesch-Kincaid and other readability scores
- **Coherence**: Logical flow and structure assessment
- **Engagement**: Predicted audience engagement

### Profile Management Capabilities

#### Profile Creation
- **From Vectors**: Direct HRV vector input
- **From Content**: Automatic profile generation from text
- **Random Generation**: Constrained random profile creation
- **Template Based**: Profile creation from templates

#### Profile Operations
- **Blending**: Combine multiple profiles with weights
- **Adaptation**: Modify existing profiles with adjustments
- **Analysis**: Compare and analyze profile differences
- **Validation**: Ensure profile quality and compliance

#### Profile Analytics
- **Usage Statistics**: Track profile usage patterns
- **Performance Metrics**: Measure profile effectiveness
- **Similarity Analysis**: Find similar profiles
- **Optimization Suggestions**: Improvement recommendations

### Corpus Analysis Capabilities

#### Linguistic Analysis
- **Sentiment Analysis**: Positive/negative/neutral classification
- **Readability Scoring**: Multiple readability metrics
- **Complexity Assessment**: Text complexity measurement
- **Style Classification**: Automatic style detection

#### HRV Analysis
- **Dimension Statistics**: Per-dimension analysis
- **Pattern Recognition**: Identify HRV patterns
- **Outlier Detection**: Find unusual HRV vectors
- **Diversity Metrics**: Measure HRV variety

#### Content Insights
- **Quality Assessment**: Overall content quality
- **Improvement Suggestions**: Specific recommendations
- **Trend Analysis**: Identify patterns and trends
- **Classification**: Automatic content categorization

### Batch Processing Capabilities

#### Performance Optimization
- **Parallel Processing**: Multi-threaded/multi-process execution
- **Resource Management**: Memory and CPU optimization
- **Load Balancing**: Distribute workload efficiently
- **Progress Monitoring**: Real-time progress tracking

#### Scalability Features
- **Large Dataset Handling**: Process thousands of documents
- **Memory Efficiency**: Optimized memory usage
- **Error Handling**: Robust error recovery
- **Retry Logic**: Automatic retry for failed operations

## 🔧 Advanced Usage

### Custom Processing Pipelines
```bash
# Create custom pipeline
python data/scripts/data_processing.py process \
  --input raw_data/ \
  --output processed_data/ \
  --format json \
  --quality-filter 0.7

# Chain multiple operations
python data/scripts/data_processing.py process \
  --input raw_data/ \
  --temp intermediate.json

python data/scripts/profile_generator.py create \
  --tenant pipeline_org \
  --name pipeline_profile \
  --input intermediate.json

python data/scripts/corpus_analyzer.py analyze \
  --input intermediate.json \
  --output final_analysis.json
```

### Performance Tuning
```bash
# Optimize for speed
python data/scripts/batch_processor.py generate \
  --input large_batch.json \
  --output results.json \
  --workers 8 \
  --batch-size 64 \
  --use-threads

# Optimize for memory
python data/scripts/batch_processor.py generate \
  --input large_batch.json \
  --output results.json \
  --workers 2 \
  --batch-size 16
```

### Custom Configuration
```bash
# Use custom configuration
python data/scripts/data_processing.py process \
  --input data/ \
  --config custom_config.json \
  --output results.json

# Create custom config
echo '{
  "performance": {
    "max_workers": 6,
    "batch_size": 48
  },
  "quality": {
    "min_score": 0.75
  }
}' > custom_config.json
```

## 📋 Script Reference

### Data Processing Commands

| Command | Description | Example |
|---------|-------------|---------|
| `single` | Process single text file | `--input file.txt` |
| `process` | Process directory of files | `--input dir/ --output results.json` |
| `profile` | Create profile from content | `--input corpus.json --profile-name name` |
| `analyze` | Analyze corpus quality | `--input corpus/ --output analysis.json` |

### Profile Generator Commands

| Command | Description | Example |
|---------|-------------|---------|
| `create` | Create profile from vector | `--tenant org --name profile --vector "0.5,0.5..."` |
| `random` | Generate random profile | `--tenant org --name profile --constraints "dim:min:max"` |
| `blend` | Blend two profiles | `--profile1 p1 --profile2 p2 --weight1 0.6` |
| `adapt` | Adapt existing profile | `--profile1 base --name adapted --adjustments "dim:val"` |
| `list` | List all profiles | `--tenant org` |
| `analyze` | Compare profiles | `--profile1 p1 --profile2 p2` |
| `export` | Export profiles | `--tenant org --output export.json` |
| `import` | Import profiles | `--tenant org --input import.json` |

### Corpus Analyzer Commands

| Command | Description | Example |
|---------|-------------|---------|
| `analyze` | Analyze corpus | `--input corpus/ --output analysis.json` |
| `single` | Analyze single text | `--input file.txt --output analysis.json` |

### Batch Processor Commands

| Command | Description | Example |
|---------|-------------|---------|
| `generate` | Batch content generation | `--input requests.json --output results.json` |
| `extract_hrv` | Batch HRV extraction | `--input texts.json --output hrv.json` |
| `create_profiles` | Batch profile creation | `--input profiles.json --tenant org` |
| `analyze` | Batch content analysis | `--input contents.json --output analysis.json` |
| `metrics` | System performance metrics | (no additional args) |

## 🔍 Script Monitoring

### Performance Monitoring
```bash
# Monitor script performance
python data/scripts/performance_monitor.py \
  --script data_processing.py \
  --duration 3600

# View performance logs
tail -f logs/performance/script_performance.log
```

### Error Tracking
```bash
# Check error logs
tail -f logs/errors/script_errors.log

# Generate error report
python data/scripts/error_report.py \
  --start-date 2026-03-01 \
  --end-date 2026-03-09
```

### Resource Usage
```bash
# Monitor resource usage
python data/scripts/resource_monitor.py \
  --interval 60 \
  --duration 3600
```

## 🛡️ Security Considerations

### Input Validation
All scripts include input validation:
- File path validation
- JSON format validation
- HRV vector validation
- Parameter range checking

### Access Control
- Tenant isolation for multi-tenant operations
- Profile access permissions
- File system access restrictions

### Data Privacy
- No sensitive data logging
- Secure temporary file handling
- Input sanitization

## 🔧 Script Maintenance

### Regular Updates
- Update script dependencies
- Add new features based on user feedback
- Optimize performance
- Fix reported issues

### Testing
- Unit tests for all major functions
- Integration tests for workflows
- Performance regression tests
- Error handling validation

### Documentation
- Update help documentation
- Add usage examples
- Maintain change logs
- Update README files

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**
```bash
# Check Python path
echo $PYTHONPATH

# Set correct path
export PYTHONPATH="/home/giganutt/artificial_intelligence/mimic:$PYTHONPATH"
```

2. **Permission Errors**
```bash
# Check file permissions
ls -la data/scripts/

# Fix permissions
chmod +x data/scripts/*.py
```

3. **Memory Issues**
```bash
# Monitor memory usage
python data/scripts/memory_monitor.py

# Reduce batch size
python data/scripts/batch_processor.py generate \
  --input large_batch.json \
  --batch-size 16
```

4. **Performance Issues**
```bash
# Check system resources
python data/scripts/system_check.py

# Optimize configuration
python data/scripts/batch_processor.py metrics
```

### Getting Help

#### Script Help
```bash
# Get help for any script
python data/scripts/script_name.py --help

# Get detailed help
python data/scripts/script_name.py --help --verbose
```

#### Debug Mode
```bash
# Enable debug logging
export DEBUG=1
python data/scripts/script_name.py --input file.txt

# Verbose output
python data/scripts/script_name.py --input file.txt --verbose
```

#### Contact Support
- Review script documentation
- Check system logs
- Validate input formats
- Contact support: support@resonanceos.ai

## 📚 Script Development

### Adding New Scripts
1. Follow existing naming conventions
2. Include comprehensive help documentation
3. Add input validation
4. Implement error handling
5. Include unit tests
6. Update this README

### Contributing Guidelines
- Follow PEP 8 style guidelines
- Include type hints
- Add docstrings
- Test thoroughly
- Document changes

### Code Quality
- Use meaningful variable names
- Add comments for complex logic
- Handle edge cases
- Provide meaningful error messages
- Log important operations

This scripts directory provides a comprehensive toolkit for managing ResonanceOS v6 data, profiles, and operations, enabling efficient automation and analysis at scale.
