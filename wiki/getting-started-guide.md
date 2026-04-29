# Getting Started Guide - ResonanceOS v6

## Overview

ResonanceOS v6 is an Adaptive Stylistic Alignment Engine that enables AI writing with real-time tonal alignment. This guide will help you get started with installation, setup, and basic usage of the system.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Basic Usage](#basic-usage)
5. [Configuration](#configuration)
6. [Next Steps](#next-steps)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before installing ResonanceOS v6, ensure you have the following:

- **Python**: 3.8 or higher
- **pip**: Package manager for Python
- **Virtual Environment**: Recommended for isolation
- **System Requirements**:
  - Minimum: 4GB RAM, 2 CPU cores
  - Recommended: 8GB RAM, 4 CPU cores
  - For advanced features: 16GB RAM, 8 CPU cores

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/resonance-os.git
cd resonance-os
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Using conda (optional)
conda create -n resonance-os python=3.8
conda activate resonance-os
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Or install from setup.py (if available)
pip install -e .
```

### Step 4: Verify Installation

```bash
# Run the test suite
python -m pytest resonance_os/tests/

# Or run the demo
python demo.py
```

## Quick Start

### Option 1: Using the CLI

The easiest way to get started is using the command-line interface.

```bash
# List available commands
resonance --help

# Create a profile from your corpus
resonance profile \
    --name my_style \
    --corpus /path/to/your/writing_samples \
    --description "My personal writing style" \
    --tier 1

# Generate text with your style
resonance generate \
    --topic "Artificial Intelligence in Healthcare" \
    --profile my_style \
    --output generated_text.txt
```

### Option 2: Using Python API

For programmatic access, use the Python API.

```python
from resonance_os.resonance_os.profiling.corpus_loader import CorpusLoader
from resonance_os.resonance_os.profiling.style_vector_builder import StyleVectorBuilder
from resonance_os.resonance_os.profiling.profile_persistence import ProfilePersistence
from resonance_os.resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.resonance_os.core.types import StyleProfile, GenerationConfig

# Load your corpus
loader = CorpusLoader()
documents = loader.load_corpus("/path/to/your/writing_samples")

# Build style profile
vector_builder = StyleVectorBuilder(tier=1)
resonance_vector = vector_builder.build_vector(documents)

# Create profile
profile = StyleProfile(
    name="my_style",
    description="My personal writing style",
    resonance_vector=resonance_vector
)

# Save profile
persistence = ProfilePersistence()
persistence.save_profile(profile)

# Generate text
writer = HumanResonantWriter()
config = GenerationConfig(
    topic="Artificial Intelligence in Healthcare",
    target_profile=profile,
    max_tokens=500
)

result = writer.generate(config)
print(result.content)
```

### Option 3: Using the API Server

Start the API server for HTTP access.

```bash
# Start the server
resonance serve --host 0.0.0.0 --port 8000

# Access the interactive documentation
# Open http://localhost:8000/docs in your browser
```

Then use curl or any HTTP client:

```bash
# Create profile
curl -X POST "http://localhost:8000/profiles" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_style",
    "corpus_path": "/path/to/corpus",
    "description": "My writing style",
    "tier": 1
  }'

# Generate text
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI in Healthcare",
    "profile_name": "my_style",
    "max_tokens": 500
  }'
```

## Basic Usage

### Creating a Style Profile

A style profile captures your unique writing characteristics.

**Step 1: Prepare Your Corpus**

Collect 10-50 writing samples that represent your style:
- Articles, blog posts, essays
- Emails, reports, documentation
- Any text that reflects your writing voice

**Step 2: Create the Profile**

```bash
resonance profile \
    --name professional \
    --corpus ./my_writing_samples \
    --description "Professional business writing style" \
    --tier 2
```

**Step 3: Verify the Profile**

```bash
# List all profiles
resonance list

# Compare with other profiles
resonance compare --profiles professional creative --method cosine
```

### Generating Content

Once you have a profile, generate content in your style.

```bash
resonance generate \
    --topic "The Future of Remote Work" \
    --profile professional \
    --tokens 1024 \
    --similarity 0.92 \
    --output article.txt
```

**Parameters:**
- `--topic`: What to write about
- `--profile`: Which style to use
- `--tokens`: Maximum length (default: 2048)
- `--similarity`: How closely to match style (0.0-1.0)
- `--temperature`: Creativity level (0.0-1.0)
- `--corrections`: Max auto-corrections (default: 3)

### Comparing Styles

Understand how different styles relate to each other.

```bash
# Compare multiple profiles
resonance compare \
    --profiles professional creative technical academic \
    --method cosine

# Available methods: cosine, euclidean, manhattan, pearson, spearman
```

### Evolving Profiles

Optimize your profile for specific topics or use cases.

```bash
resonance evolve \
    --profile professional \
    --topics business finance strategy \
    --generations 50 \
    --population 30
```

## Configuration

### Environment Variables

Set environment variables for system-wide configuration:

```bash
# Set profile directory
export RESONANCE_PROFILES_DIR=/path/to/profiles

# Set log level
export RESONANCE_LOG_LEVEL=DEBUG

# Set API configuration
export RESONANCE_API_HOST=0.0.0.0
export RESONANCE_API_PORT=8000
```

### Configuration File

Create a `config.yaml` file in the project root:

```yaml
database:
  host: localhost
  port: 5432
  name: resonance_os

api:
  host: 0.0.0.0
  port: 8000
  workers: 4

model:
  temperature: 0.7
  max_tokens: 2048

paths:
  data_dir: ./data
  profiles_dir: ./profiles/hr_profiles
  cache_dir: ./cache
  log_dir: ./logs

logging:
  level: INFO
  file: ./logs/resonance_os.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

Load configuration:

```bash
resonance --config config.yaml profile --name my_style --corpus ./corpus
```

## Next Steps

### Explore Examples

Check out the examples directory for more usage patterns:

```bash
cd examples/basic_usage
python hrv_extraction.py
python profile_creation.py
python simple_generation.py
```

### Read System Guides

Detailed guides for each system component:

- [Core Systems Guide](./core-systems-guide.md)
- [Generation Systems Guide](./generation-systems-guide.md)
- [API Systems Guide](./api-systems-guide.md)
- [CLI Systems Guide](./cli-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [Similarity Systems Guide](./similarity-systems-guide.md)

### Advanced Features

Once comfortable with basics, explore:

- **Adaptive Writing**: Real-time resonance feedback
- **Batch Processing**: Process multiple texts efficiently
- **Profile Evolution**: Optimize profiles with genetic algorithms
- **Multi-tenant Profiles**: Manage profiles for multiple users
- **Custom Fitness Evaluators**: Define custom evolution criteria

### Integration

Integrate ResonanceOS into your applications:

```python
# Custom integration example
from resonance_os.resonance_os.generation.adaptive_writer import AdaptiveWriter

writer = AdaptiveWriter(tier=2)

# Set external LLM integration
async def my_llm_generator(params):
    # Call your external LLM API
    return await external_llm_api.generate(params)

writer.set_llm_generator(my_llm_generator)

# Generate with custom LLM
result = await writer.generate_article(config)
```

## Troubleshooting

### Installation Issues

**Issue**: Module not found errors
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: Dependency conflicts
```bash
# Solution: Update pip and try clean install
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
```

### Profile Creation Issues

**Issue**: No documents found in corpus
```bash
# Solution: Check file extensions and paths
# Supported: .txt, .md, .rtf, .html, .htm
ls -la /path/to/corpus
```

**Issue**: Low confidence score
```bash
# Solution: Use more diverse corpus samples
# Increase corpus size to 20+ documents
# Use higher analysis tier (--tier 2)
```

### Generation Issues

**Issue**: Generation too slow
```bash
# Solution: Reduce max_tokens
# Lower similarity threshold
# Use tier 1 profile instead of tier 2
```

**Issue**: Poor style alignment
```bash
# Solution: Improve corpus quality
# Increase similarity threshold
# Use profile evolution for optimization
```

### API Server Issues

**Issue**: Port already in use
```bash
# Solution: Use different port
resonance serve --port 8001
```

**Issue**: Connection refused
```bash
# Solution: Check firewall settings
# Ensure server is running
# Verify host binding (use 0.0.0.0 for external access)
```

### Performance Issues

**Issue**: High memory usage
```bash
# Solution: Reduce batch size
# Limit concurrent operations
# Use lower analysis tier
```

**Issue**: Slow processing
```bash
# Solution: Increase worker count
# Use multiprocessing for batch operations
# Optimize corpus size
```

## Getting Help

- **Documentation**: Check system-specific guides in `/website/pages/`
- **Examples**: Review `/examples/` directory
- **Tests**: Run test suite for verification: `python -m pytest resonance_os/tests/`
- **Issues**: Report bugs on GitHub Issues
- **Community**: Join discussions in GitHub Discussions

## Best Practices

1. **Start Simple**: Begin with tier 1 analysis and basic generation
2. **Quality Corpus**: Use diverse, representative writing samples
3. **Iterate**: Evolve profiles based on generation results
4. **Monitor**: Use statistics command to track system performance
5. **Backup**: Regularly backup profiles with the backup command
6. **Test**: Validate profiles with small generations before large batches
7. **Configure**: Adjust parameters based on your specific use case
8. **Document**: Keep track of profile configurations and results

## Resources

- **Project Repository**: https://github.com/your-org/resonance-os
- **API Documentation**: http://localhost:8000/docs (when server running)
- **System Guides**: All guides available in `/website/pages/`
- **Examples**: `/examples/` directory with usage examples
- **Tests**: `/resonance_os/tests/` for verification

## Summary

You should now have:
- ResonanceOS v6 installed and configured
- At least one style profile created from your corpus
- Generated text in your style
- Understanding of basic CLI, API, and Python usage
- Knowledge of where to find more information

Ready to explore more? Check out the system-specific guides for detailed information on each component.
