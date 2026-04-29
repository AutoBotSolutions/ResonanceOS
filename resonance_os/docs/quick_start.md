# ResonanceOS Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/trenaman/resonance-os.git
cd resonance-os

# Install dependencies
pip install -e .

# Setup environment
cp .env.example .env
# Edit .env with your API keys
```

## Quick Start

### 1. Create a Style Profile

```bash
# From text corpus
resonance-os profile --name "my_style" --corpus ./my_writings/ --description "My personal writing style"

# From direct text input
resonance-os profile --name "quick_style" --corpus ./sample.txt --tier 2
```

### 2. Generate Content

```bash
# Basic generation
resonance-os generate --topic "AI architecture" --profile "my_style"

# Advanced generation with parameters
resonance-os generate \
  --topic "Future of machine learning" \
  --profile "my_style" \
  --tokens 1500 \
  --similarity 0.95 \
  --corrections 5 \
  --output generated_text.txt
```

### 3. Compare Profiles

```bash
# Compare multiple profiles
resonance-os compare --profiles "my_style" "professional" --method cosine

# List all profiles
resonance-os list --format table
```

### 4. Start API Server

```bash
# Development server
resonance-os serve --host 0.0.0.0 --port 8000 --reload

# Production server
resonance-os serve --host 0.0.0.0 --port 8000 --workers 4
```

## API Usage

### Create Profile from Text

```python
import requests

# Create profile from text
response = requests.post("http://localhost:8000/profiles", json={
    "name": "sample_profile",
    "corpus_path": "./sample.txt",
    "description": "Sample writing style",
    "tier": 1
})

profile_data = response.json()
print(f"Profile created: {profile_data['data']['profile_name']}")
```

### Generate Text

```python
# Generate text with style alignment
response = requests.post("http://localhost:8000/generate", json={
    "topic": "Artificial intelligence in healthcare",
    "profile_name": "sample_profile",
    "max_tokens": 1000,
    "similarity_threshold": 0.92
})

result = response.json()
print(f"Generated text similarity: {result['data']['similarity_score']:.3f}")
print(f"Content: {result['data']['content'][:200]}...")
```

### Calculate Similarity

```python
# Compare two profiles
response = requests.post("http://localhost:8000/similarity", json={
    "profile1_name": "sample_profile",
    "profile2_name": "professional",
    "method": "cosine"
})

similarity_data = response.json()
print(f"Similarity: {similarity_data['data']['similarity_score']:.3f}")
```

## Python API Usage

### Basic Usage

```python
from resonance_os import ResonanceOS, StyleProfile, GenerationConfig

# Initialize ResonanceOS
ros = ResonanceOS()

# Create profile from text
profile = ros.create_profile_from_text(
    name="my_style",
    text_content="Your sample text here...",
    description="My writing style"
)

# Generate content
config = GenerationConfig(
    topic="The future of AI",
    target_profile=profile,
    max_tokens=500,
    similarity_threshold=0.92
)

result = ros.generate_article(config)
print(f"Generated: {result.content}")
print(f"Similarity: {result.metrics.similarity_score:.3f}")
```

### Advanced Usage

```python
from resonance_os.profiling import CorpusLoader, StyleVectorBuilder
from resonance_os.generation import AdaptiveWriter
from resonance_os.similarity import SimilarityCalculator

# Load and analyze corpus
loader = CorpusLoader()
documents = loader.load_corpus("./my_corpus/")

vector_builder = StyleVectorBuilder(tier=2)
resonance_vector = vector_builder.build_vector(documents)

# Create profile
profile = StyleProfile(
    name="advanced_style",
    resonance_vector=resonance_vector,
    emotional_curve=[0.5, 0.6, 0.7, 0.6, 0.5],
    cadence_pattern=[0.4, 0.6, 0.8, 0.7],
    abstraction_preference=0.7
)

# Generate with adaptive writer
writer = AdaptiveWriter(tier=2)
config = GenerationConfig(
    topic="Machine learning trends",
    target_profile=profile,
    enable_feedback=True,
    enable_drift_detection=True
)

result = await writer.generate_article(config)
```

## Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key

# Optional
DEFAULT_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002
RESONANCE_THRESHOLD=0.92
DRIFT_THRESHOLD=0.05
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### Custom Configuration

```python
from resonance_os.core.config import Settings, get_config

# Get current config
config = get_config()

# Update settings
config.models.openai_api_key = "your_key"
config.resonance.threshold = 0.95
config.api.port = 8080
```

## Examples

### Content Marketing

```bash
# Create marketing style profile
resonance-os profile \
  --name "marketing" \
  --corpus ./marketing_content/ \
  --description "Engaging marketing copy" \
  --tier 2

# Generate marketing content
resonance-os generate \
  --topic "Benefits of our new product" \
  --profile "marketing" \
  --tokens 800 \
  --output marketing_copy.txt
```

### Technical Documentation

```bash
# Create technical writer profile
resonance-os profile \
  --name "technical_writer" \
  --corpus ./docs/ \
  --description "Clear technical documentation" \
  --tier 3

# Generate documentation
resonance-os generate \
  --topic "API reference guide" \
  --profile "technical_writer" \
  --tokens 2000 \
  --similarity 0.95
```

### Brand Voice Consistency

```bash
# Compare brand voice with target style
resonance-os compare \
  --profiles "brand_voice" "target_style" \
  --method cosine

# Evolve brand voice to match target
resonance-os evolve \
  --profile "brand_voice" \
  --topics "product_launch" "customer_success" \
  --generations 50 \
  --population 30
```

## Troubleshooting

### Common Issues

1. **Profile creation fails**
   - Check corpus path exists
   - Ensure text files are readable
   - Verify sufficient text content

2. **Low similarity scores**
   - Increase similarity threshold gradually
   - Check profile quality
   - Verify topic relevance

3. **API connection issues**
   - Check API keys in .env
   - Verify network connectivity
   - Check API rate limits

### Debug Mode

```bash
# Enable verbose logging
resonance-os --verbose generate --topic "test" --profile "my_profile"

# Check system statistics
resonance-os stats
```

## Next Steps

- Explore the [API documentation](http://localhost:8000/docs)
- Try the [Jupyter notebook examples](./notebooks/)
- Read the [architecture guide](./docs/architecture.md)
- Join our [community discussions](https://github.com/trenaman/resonance-os/discussions)
