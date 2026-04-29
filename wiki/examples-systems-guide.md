# Examples Systems Guide - ResonanceOS v6

## Overview

The Examples Systems module provides comprehensive examples and tutorials demonstrating how to use ResonanceOS v6 for various use cases. This module includes basic usage examples, advanced usage patterns, business scenarios, creative applications, data science examples, integration examples, and testing examples.

## System Architecture

```
Examples Systems
├── basic_usage/ (Basic Usage Examples)
├── advanced_usage/ (Advanced Usage Examples)
├── business_scenarios/ (Business Use Cases)
├── creative_applications/ (Creative Writing Examples)
├── data_science_examples/ (Data Science Applications)
├── integration_examples/ (Integration Patterns)
├── testing_examples/ (Testing Examples)
└── tutorials/ (Step-by-Step Tutorials)
```

## System Components

### 1. Basic Usage Examples (`basic_usage/`)

Provides fundamental examples for getting started with ResonanceOS v6.

#### Files

- `hrv_extraction.py` - Demonstrates HRV extraction from text
- `profile_creation.py` - Shows how to create style profiles
- `simple_generation.py` - Basic content generation example

#### HRV Extraction Example

```python
from resonance_os.profiles.hrv_extractor import HRVExtractor

extractor = HRVExtractor()

# Extract HRV from sample text
text = "The innovative technology transforms how we approach sustainable energy solutions."
hrv_vector = extractor.extract(text)

print(f"HRV Vector: {hrv_vector}")
print(f"Dimensions: {len(hrv_vector)}")
```

**Output:**
- 8-dimensional HRV vector
- Values for each resonance dimension
- Ready for profile creation or comparison

#### Profile Creation Example

```python
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from pathlib import Path

manager = HRVProfileManager(Path("./profiles"))

# Create and save profile
profile_hrv = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
manager.save_profile("default", "professional", profile_hrv)

# Load and verify
loaded_profile = manager.load_profile("default", "professional")
print(f"Loaded profile: {loaded_profile}")
```

**Output:**
- Profile saved to JSON file
- Multi-tenant support
- Profile listing capability

#### Simple Generation Example

```python
from resonance_os.generation.human_resonant_writer import HumanResonantWriter

writer = HumanResonantWriter()

# Generate content from prompt
prompt = "The future of artificial intelligence in business"
content = writer.generate(prompt)

print(f"Generated content:\n{content}")
```

**Output:**
- Multi-paragraph generated content
- HRV-constrained generation
- Real-time feedback integration

### 2. Advanced Usage Examples (`advanced_usage/`)

Provides advanced usage patterns and techniques for power users.

#### Files

- `batch_processing.py` - Batch content generation and processing

#### Batch Processing Example

```python
from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor

writer = HumanResonantWriter()
extractor = HRVExtractor()

# Process multiple prompts
prompts = [
    "AI in healthcare",
    "Machine learning applications",
    "Ethical considerations in AI"
]

results = []
for prompt in prompts:
    content = writer.generate(prompt)
    hrv = extractor.extract(content)
    results.append({
        "prompt": prompt,
        "content": content,
        "hrv": hrv
    })

# Save results
import json
with open("batch_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

**Features:**
- Parallel processing support
- Result aggregation
- HRV analysis for each generation

### 3. Business Scenarios (`business_scenarios/`)

Provides examples tailored for business use cases.

#### Common Business Use Cases

- **Marketing Content Generation**: Generate marketing copy with brand voice
- **Customer Support Responses**: Create consistent support responses
- **Internal Communications**: Standardize internal messaging
- **Product Descriptions**: Generate product descriptions with consistent tone
- **Email Templates**: Create email templates with brand alignment

#### Example Pattern

```python
# Brand-aligned content generation
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.generation.human_resonant_writer import HumanResonantWriter

manager = HRVProfileManager(Path("./profiles"))
writer = HumanResonantWriter()

# Load brand profile
brand_profile = manager.load_profile("company_a", "brand_voice")

# Generate brand-aligned content
prompt = "New product launch announcement"
content = writer.generate(prompt)

# Verify brand alignment
from resonance_os.profiles.hrv_extractor import HRVExtractor
extractor = HRVExtractor()
generated_hrv = extractor.extract(content)

# Compare with brand profile
# (Similarity calculation logic)
```

### 4. Creative Applications (`creative_applications/`)

Provides examples for creative writing and artistic applications.

#### Creative Use Cases

- **Story Generation**: Generate stories with specific narrative styles
- **Character Voice**: Create consistent character dialogue
- **Genre Writing**: Write in specific genre styles
- **Poetry Generation**: Generate poetry with specific emotional tones
- **Screenplay Writing**: Create screenplay dialogue with character voices

#### Example Pattern

```python
# Creative writing with style profiles
from resonance_os.generation.human_resonant_writer import HumanResonantWriter

writer = HumanResonantWriter()

# Load creative profile
creative_profile = manager.load_profile("default", "storyteller")

# Generate creative content
prompt = "A mysterious discovery in an ancient library"
story = writer.generate(prompt)

print(story)
```

### 5. Data Science Examples (`data_science_examples/`)

Provides examples for data science and analytical applications.

#### Data Science Use Cases

- **Corpus Analysis**: Analyze large text corpora
- **Style Clustering**: Cluster documents by style
- **Trend Analysis**: Track style trends over time
- **A/B Testing**: Compare different writing styles
- **Quality Metrics**: Measure content quality metrics

#### Example Pattern

```python
# Corpus analysis and profiling
from resonance_os.resonance_os.profiling.corpus_loader import CorpusLoader
from resonance_os.resonance_os.profiling.style_vector_builder import StyleVectorBuilder

loader = CorpusLoader()
builder = StyleVectorBuilder(tier=2)

# Load corpus
documents = loader.load_corpus("corpora/business_reports")

# Build style profile
vector = builder.build_vector(documents)

print(f"Style vector: {vector.values}")
print(f"Confidence: {vector.confidence}")
```

### 6. Integration Examples (`integration_examples/`)

Provides examples for integrating ResonanceOS with other systems.

#### Integration Patterns

- **API Integration**: REST API integration examples
- **Database Integration**: Store and retrieve profiles from databases
- **Web Framework Integration**: Integration with Flask, Django, FastAPI
- **Queue Integration**: Integration with task queues (Celery, RQ)
- **Monitoring Integration**: Integration with monitoring systems

#### Example Pattern

```python
# API integration example
import requests

# Call ResonanceOS API
response = requests.post(
    "http://localhost:8000/generate",
    json={
        "prompt": "Product description for new service",
        "profile_name": "brand_voice",
        "max_tokens": 500
    }
)

result = response.json()
print(f"Generated: {result['article']}")
print(f"HRV: {result['hrv_feedback']}")
```

### 7. Testing Examples (`testing_examples/`)

Provides examples for testing ResonanceOS components.

#### Testing Patterns

- **Unit Tests**: Test individual components
- **Integration Tests**: Test component integration
- **Performance Tests**: Test performance characteristics
- **Load Tests**: Test under high load
- **End-to-End Tests**: Test complete workflows

#### Example Pattern

```python
import unittest
from resonance_os.profiles.hrv_extractor import HRVExtractor

class TestHRVExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = HRVExtractor()
    
    def test_extract_basic(self):
        text = "Test sentence."
        hrv = self.extractor.extract(text)
        self.assertEqual(len(hrv), 8)
        self.assertTrue(all(isinstance(x, (int, float)) for x in hrv))
    
    def test_extract_empty(self):
        hrv = self.extractor.extract("")
        self.assertEqual(len(hrv), 8)

if __name__ == "__main__":
    unittest.main()
```

### 8. Tutorials (`tutorials/`)

Provides step-by-step tutorials for learning ResonanceOS.

#### Tutorial Topics

- **Getting Started**: First steps with ResonanceOS
- **Profile Creation**: Creating custom style profiles
- **Content Generation**: Generating content with profiles
- **API Usage**: Using the ResonanceOS API
- **Advanced Features**: Using advanced features

#### Tutorial Structure

Each tutorial includes:
- Prerequisites
- Step-by-step instructions
- Code examples
- Expected output
- Common issues and solutions

## Usage Patterns

### Quick Start

```bash
# Run basic examples
cd examples/basic_usage
python hrv_extraction.py
python profile_creation.py
python simple_generation.py

# Run advanced examples
cd ../advanced_usage
python batch_processing.py
```

### Custom Examples

```python
# Create your own example
from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor

writer = HumanResonantWriter()
extractor = HRVExtractor()

# Your custom workflow
prompt = "Your custom prompt"
content = writer.generate(prompt)
hrv = extractor.extract(content)

print(f"Content: {content}")
print(f"HRV: {hrv}")
```

## Best Practices

1. **Start with basic examples**: Begin with basic_usage examples
2. **Understand HRV vectors**: Learn how HRV vectors work
3. **Create custom profiles**: Build profiles for your use case
4. **Test thoroughly**: Test with your specific data
5. **Iterate**: Refine profiles based on results

## Common Issues

**Issue**: Import errors when running examples
**Solution**: Ensure resonance_os is in Python path

**Issue**: Profile not found
**Solution**: Verify profile exists in correct directory

**Issue**: Generation quality poor
**Solution**: Adjust profile or use different model

**Issue**: Slow generation
**Solution**: Reduce max_tokens or use batch processing

## Integration Points

The Examples Systems module integrates with:

- **All Systems**: Demonstrates usage of all system components
- **Core Systems**: Shows HRV extraction and profile creation
- **Generation Systems**: Demonstrates content generation
- **API Systems**: Shows API integration patterns
- **Profile Systems**: Demonstrates profile management

## Future Enhancements

- **More examples**: Additional use case examples
- **Interactive tutorials**: Interactive Jupyter notebooks
- **Video tutorials**: Video walkthrough examples
- **Community examples**: Community-contributed examples
- **Example templates**: Template examples for customization

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Generation Systems Guide](./generation-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [API Systems Guide](./api-systems-guide.md)
