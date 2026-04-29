# ResonanceOS v6 - Human-Resonant AI Writing Engine

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/docs-github--pages-blue.svg)](https://roberttrenaman.github.io/mimic/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

## 🎯 Overview

ResonanceOS v6 is a revolutionary AI system that generates content with quantifiable human resonance metrics. Unlike traditional AI writers that focus solely on semantic coherence, ResonanceOS leverages Human-Resonant Value (HRV) vectors to ensure content aligns with human engagement patterns.

## 🚀 Key Features

- **🧠 Human-Resonant Value (HRV) System**: 8-dimensional vectors measuring textual resonance
- **👥 Multi-Tenant Profile Management**: Support for multiple clients/brands with distinct HRV profiles
- **⚡ Real-Time Feedback Loop**: Paragraph-level resonance optimization during generation
- **🔧 Modular Architecture**: Clean separation between planning, generation, and refinement layers
- **📊 Zero Dependencies**: Core functionality uses only Python standard library
- **🌐 REST API**: Complete API for integration with external systems
- **💻 CLI Interface**: Command-line tools for content generation and management
- **📈 Analytics Dashboard**: Real-time performance and quality monitoring

## Architecture

```
resonance_os/
├── core/                    # Core constants and types
│   ├── hrv_constants.py     # HRV dimension definitions
│   └── hrv_types.py         # Type definitions
├── generation/              # Content generation pipeline
│   ├── human_resonant_writer.py  # Main generation engine
│   ├── planner_layer.py     # Strategic content planning
│   ├── sentence_layer.py    # Sentence-level generation
│   ├── refiner_layer.py     # Content refinement
│   └── hrf_model.py         # Human resonance feedback model
├── profiles/                # Profile management
│   ├── hrv_extractor.py     # HRV vector extraction
│   └── multi_tenant_hr_profiles.py  # Profile storage
├── api/                     # REST API
│   └── hr_server.py         # FastAPI server
└── cli/                     # Command line interface
    └── hr_main.py          # CLI entry point
```

## HRV Dimensions

The Human-Resonant Value (HRV) system measures 8 key dimensions:

1. **Sentence Variance**: Cadence and rhythm variation
2. **Emotional Valence**: Positive/negative sentiment
3. **Emotional Intensity**: Strength of emotion
4. **Assertiveness Index**: Authoritative tone
5. **Curiosity Index**: Intrigue and engagement potential
6. **Metaphor Density**: Metaphoric richness
7. **Storytelling Index**: Narrative engagement
8. **Active Voice Ratio**: Active vs. passive sentence ratio

## 🚀 Quick Start

### 📦 Installation & Setup

```bash
# Clone or download the project
cd resonance_os

# Run complete setup (recommended)
python setup.py

# Or check existing installation
python setup.py --check-only
```

### 🧪 System Verification

```bash
# Run comprehensive system check
python system_runner.py --all

# Run tests
python test_runner.py

# Start API server
python system_runner.py --serve
```

### 💻 CLI Usage

```bash
# Generate content with default settings
python resonance_os/cli/hr_main --prompt "The future of renewable energy"

# With specific tenant and profile
python resonance_os/cli/hr_main --prompt "AI in healthcare" --tenant "healthcare" --profile "medical"

# Batch generation
python resonance_os/cli/hr_main --batch --input prompts.txt --output results.json
```

### 🌐 API Usage

```python
from resonance_os.api.hr_server import SimpleRequest, hr_generate

# Create generation request
request = SimpleRequest(prompt="Benefits of machine learning")
response = hr_generate(request)

print(response.article)        # Generated content
print(response.hrv_feedback)   # HRV resonance scores
```

### 🔧 Programmatic Usage

```python
from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor

# Generate content
writer = HumanResonantWriter()
article = writer.generate("The impact of climate change")

# Extract HRV vectors
extractor = HRVExtractor()
hrv_vector = extractor.extract(article)
```

### 📚 Examples & Tutorials

```bash
# Getting started tutorial
python examples/tutorials/getting_started.py

# Profile mastery
python examples/tutorials/profile_mastery.py

# Business scenarios
python examples/business_scenarios/content_marketing.py

# Creative writing
python examples/creative_applications/story_generation.py
```

## 📋 System Requirements

- **Python 3.8+** (recommended 3.10+)
- **Standard library modules only** (for core functionality)
- **Optional**: FastAPI, uvicorn for API deployment
- **Memory**: 512MB minimum, 2GB recommended
- **Storage**: 100MB minimum for full installation

## 🧪 Testing & Quality Assurance

```bash
# Run all tests
python test_runner.py

# Run specific test categories
python test_runner.py --basic
python test_runner.py --integration
python test_runner.py --performance
python test_runner.py --unit

# Run with verbose output
python test_runner.py --verbose
```

## 📊 System Management

```bash
# System diagnostics
python system_runner.py --diagnostics

# Performance benchmarks
python system_runner.py --benchmark

# Generate system report
python system_runner.py --report

# Complete system check
python system_runner.py --all
```

## 📁 Project Structure

```
resonance_os/
├── 📁 data/                   # Data directory
│   ├── config/               # System configurations
│   ├── profiles/             # HRV profiles
│   ├── corpora/              # Training data
│   ├── models/               # ML models
│   ├── scripts/              # Utility scripts
│   ├── logs/                 # System logs
│   └── exports/              # Analytics & reports
├── 📁 examples/              # Usage examples
│   ├── basic_usage/          # Getting started
│   ├── advanced_usage/       # Advanced features
│   ├── business_scenarios/   # Real-world applications
│   ├── creative_applications/ # Creative writing
│   └── tutorials/            # Learning guides
├── 📁 tests/                 # Test suite
├── 📄 setup.py              # System setup script
├── 📄 system_runner.py      # System management
├── 📄 test_runner.py        # Test runner
└── 📄 README.md             # This file
```

## Configuration

Environment variables:

- `API_HOST`: API server host (default: 0.0.0.0)
- `API_PORT`: API server port (default: 8000)
- `HRV_TENANT_DIR`: Directory for HRV profiles (default: ./profiles/hr_profiles)

## Project Status

✅ **Core Functionality**: All modules operational  
✅ **CLI Interface**: Fully functional  
✅ **API Layer**: Basic implementation ready  
✅ **Profile Management**: Multi-tenant support  
✅ **Testing**: Comprehensive test coverage  

## Next Steps

- Enhanced ML models for HRF prediction
- Transformer-based text generation
- Advanced resonance optimization algorithms
- Web dashboard for resonance analytics
- Integration with external content management systems

## License

This project represents cutting-edge research in human-AI content resonance. See LICENSE file for details.
