# Data Scripts Systems Guide - ResonanceOS v6

## Overview

The Data Scripts Systems module provides utility scripts for batch processing, corpus analysis, data processing, and profile generation. These scripts enable large-scale operations on text corpora, HRV extraction, and profile management for ResonanceOS v6.

## System Architecture

```
Data Scripts Systems
├── batch_processor.py (Batch Processing Utility)
├── corpus_analyzer.py (Corpus Analysis Utility)
├── data_processing.py (Data Processing Utility)
└── profile_generator.py (Profile Generation Utility)
```

## System Components

### 1. Batch Processor (`batch_processor.py`)

High-performance batch processing utility for large-scale content generation, profile management, and data analysis.

#### Architecture

```python
class BatchProcessor:
    """High-performance batch processing utility"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.writer = HumanResonantWriter()
        self.extractor = HRVExtractor()
        self.profile_manager = HRVProfileManager()
        self.max_workers = config.get('max_workers', min(cpu_count(), 8))
        self.batch_size = config.get('batch_size', 32)
        self.use_multiprocessing = config.get('use_multiprocessing', True)
```

#### Key Features

- **Parallel Processing**: Multi-threaded and multi-process execution
- **Batch Operations**: Generate content, extract HRV, create profiles, analyze content
- **Performance Monitoring**: Track generation time, word count, success rates
- **File-based Processing**: Process JSON input files and save results
- **Configurable Workers**: Adjust worker count and batch size for optimal performance

#### Usage Examples

**Batch Content Generation**
```python
from resonance_os.data.scripts.batch_processor import BatchProcessor

# Initialize processor
config = {
    'max_workers': 8,
    'batch_size': 32,
    'use_multiprocessing': True
}
processor = BatchProcessor(config)

# Generate content for multiple prompts
prompts = [
    "AI technology in healthcare",
    "Sustainable energy solutions",
    "Digital transformation in business"
]

results = processor.batch_generate_content(
    prompts=prompts,
    tenant="default",
    profile_name="professional"
)

for result in results:
    if result['success']:
        print(f"Generated: {result['content'][:100]}...")
        print(f"Time: {result['generation_time']:.2f}s")
    else:
        print(f"Error: {result['error']}")
```

**Batch HRV Extraction**
```python
# Extract HRV from multiple texts
texts = [
    "Sample text 1 for HRV extraction...",
    "Sample text 2 for HRV extraction...",
    "Sample text 3 for HRV extraction..."
]

results = processor.batch_extract_hrv(texts)

for result in results:
    if result['success']:
        print(f"HRV: {result['hrv_vector']}")
        print(f"Time: {result['extraction_time']:.2f}s")
```

**Batch Profile Creation**
```python
# Create multiple profiles
profiles_data = [
    {'name': 'professional', 'hrv_vector': [0.7, 0.6, 0.8, ...]},
    {'name': 'creative', 'hrv_vector': [0.5, 0.8, 0.6, ...]},
    {'name': 'technical', 'hrv_vector': [0.8, 0.5, 0.7, ...]}
]

results = processor.batch_create_profiles(profiles_data, tenant="default")

for result in results:
    if result['success']:
        print(f"Created: {result['name']}")
```

**Batch Content Analysis**
```python
# Analyze multiple contents
contents = [
    "Content 1 to analyze...",
    "Content 2 to analyze...",
    "Content 3 to analyze..."
]

results = processor.batch_analyze_content(contents)

for result in results:
    if result['success']:
        print(f"Quality score: {result['quality_score']:.3f}")
        print(f"Word count: {result['word_count']}")
```

**File-based Processing**
```python
# Process from JSON file
success = processor.process_batch_file(
    input_file="input.json",
    output_file="output.json",
    operation="generate",
    tenant="default",
    profile_name="professional"
)

if success:
    print("Batch processing completed")
```

**Performance Metrics**
```python
# Get system performance metrics
metrics = processor.get_performance_metrics()
print(f"Max workers: {metrics['max_workers']}")
print(f"Batch size: {metrics['batch_size']}")
print(f"CPU count: {metrics['cpu_count']}")
```

#### Command-Line Usage

```bash
# Generate content from batch file
python batch_processor.py generate \
    --input prompts.json \
    --output results.json \
    --tenant default \
    --profile professional \
    --workers 8

# Extract HRV from texts
python batch_processor.py extract_hrv \
    --input texts.json \
    --output hrv_results.json \
    --workers 4

# Create profiles from batch
python batch_processor.py create_profiles \
    --input profiles.json \
    --output creation_results.json \
    --tenant default

# Analyze content
python batch_processor.py analyze \
    --input contents.json \
    --output analysis_results.json

# Get performance metrics
python batch_processor.py metrics
```

#### Quality Score Calculation

The batch processor calculates quality scores based on:
- **Length Score**: Ideal 200-500 words
- **Variety Score**: Sentence length variance
- **HRV Balance Score**: Balance around 0.5
- **Readability Score**: 10-20 words per sentence ideal

### 2. Corpus Analyzer (`corpus_analyzer.py`)

Advanced corpus analysis utility for extracting insights, patterns, and recommendations from text corpora.

#### Architecture

```python
class CorpusAnalyzer:
    """Advanced corpus analysis utility"""
    
    def __init__(self):
        self.hrv_extractor = HRVExtractor()
        self.positive_words = {...}
        self.negative_words = {...}
        self.assertive_words = {...}
        self.curiosity_words = {...}
        self.storytelling_words = {...}
        self.metaphor_patterns = [...]
```

#### Key Features

- **Comprehensive Text Analysis**: Basic stats, HRV, linguistic features, readability
- **Content Classification**: Business, technical, creative, academic classification
- **Formality Detection**: Formal, informal, neutral classification
- **HRV Pattern Analysis**: Outlier detection, clustering, diversity scoring
- **Recommendations Generation**: Insights for improving corpus quality

#### Usage Examples

**Single Text Analysis**
```python
from resonance_os.data.scripts.corpus_analyzer import CorpusAnalyzer

analyzer = CorpusAnalyzer()

text = "Your sample text here for analysis..."
result = analyzer.analyze_text(text)

print(f"Word count: {result['basic_stats']['word_count']}")
print(f"HRV vector: {result['hrv_vector']}")
print(f"Reading level: {result['readability']['reading_level']}")
print(f"Content type: {result['content_classification']['primary_type']}")
print(f"Formality: {result['content_classification']['formality']}")
```

**Corpus Directory Analysis**
```python
# Analyze entire corpus directory
result = analyzer.analyze_corpus(directory="/path/to/corpus", pattern="*.txt")

print(f"Total files: {len(result['file_analyses'])}")
print(f"Aggregate statistics: {result['aggregate_statistics']}")
print(f"HRV analysis: {result['hrv_analysis']}")
print(f"Content distribution: {result['content_distribution']}")
print(f"Recommendations: {result['recommendations']}")
```

**Linguistic Features**
```python
# Extract linguistic features
features = analyzer._extract_linguistic_features(text)

print(f"Sentiment ratio: {features['sentiment_ratio']:.3f}")
print(f"Assertiveness ratio: {features['assertiveness_ratio']:.3f}")
print(f"Curiosity ratio: {features['curiosity_ratio']:.3f}")
print(f"Storytelling ratio: {features['storytelling_ratio']:.3f}")
print(f"Metaphor ratio: {features['metaphor_ratio']:.3f}")
print(f"Active voice ratio: {features['active_voice_ratio']:.3f}")
```

**Readability Metrics**
```python
# Calculate readability
readability = analyzer._calculate_readability(text)

print(f"Flesch score: {readability['flesch_score']:.1f}")
print(f"Reading level: {readability['reading_level']}")
print(f"Avg sentence length: {readability['avg_sentence_length']:.1f}")
print(f"Avg word length: {readability['avg_word_length']:.1f}")
```

**Content Classification**
```python
# Classify content type
classification = analyzer._classify_content(text)

print(f"Primary type: {classification['primary_type']}")
print(f"Type scores: {classification['type_scores']}")
print(f"Formality: {classification['formality']}")
```

**HRV Pattern Analysis**
```python
# Analyze HRV patterns across corpus
hrv_analysis = analyzer._analyze_corpus_hrv(analyses)

print(f"Dimension statistics: {hrv_analysis['dimension_statistics']}")
print(f"Outliers: {hrv_analysis['outliers']}")
print(f"Patterns: {hrv_analysis['patterns']}")
print(f"Diversity score: {hrv_analysis['diversity_score']:.3f}")
```

#### Command-Line Usage

```bash
# Analyze single file
python corpus_analyzer.py single \
    --input document.txt \
    --output analysis.json

# Analyze corpus directory
python corpus_analyzer.py analyze \
    --input /path/to/corpus \
    --pattern "*.txt" \
    --output corpus_analysis.json
```

#### Analysis Components

**Basic Statistics**
- Word count, sentence count
- Average sentence length
- Lexical diversity
- Unique words

**Linguistic Features**
- Sentiment analysis (positive/negative)
- Assertiveness indicators
- Curiosity indicators
- Storytelling elements
- Metaphor patterns
- Active voice estimation

**Readability Metrics**
- Flesch Reading Ease score
- Reading level classification
- Average sentence/word length

**Content Classification**
- Business/technical/creative/academic
- Formal/informal/neutral
- Dominant style identification

**HRV Analysis**
- Dimension statistics (mean, min, max, std)
- Outlier detection
- Pattern identification
- Diversity scoring

### 3. Data Processing (`data_processing.py`)

Data processing utilities for text corpora, HRV feature extraction, and profile creation.

#### Architecture

```python
class DataProcessor:
    """Main data processing class for ResonanceOS"""
    
    def __init__(self, config_path: str = None):
        self.hrv_extractor = HRVExtractor()
        self.config = self._load_config(config_path)
```

#### Key Features

- **Text File Processing**: Extract HRV features from individual files
- **Directory Processing**: Batch process entire directories
- **Profile Creation**: Generate HRV profiles from corpus
- **Quality Analysis**: Analyze corpus quality and variety
- **Export Options**: JSON and CSV export formats

#### Usage Examples

**Process Single File**
```python
from resonance_os.data.scripts.data_processing import DataProcessor

processor = DataProcessor()

result = processor.process_text_file("document.txt")

print(f"Word count: {result['word_count']}")
print(f"HRV vector: {result['hrv_vector']}")
print(f"Content preview: {result['content_preview']}")
```

**Process Directory**
```python
# Process all files in directory
results = processor.process_directory(
    directory="/path/to/corpus",
    pattern="*.txt"
)

for result in results:
    if 'error' not in result:
        print(f"Processed: {result['file_path']}")
```

**Create Corpus Profile**
```python
# Create profile from processed results
profile = processor.create_corpus_profile(
    results=results,
    profile_name="my_corpus_profile"
)

print(f"Profile name: {profile['name']}")
print(f"HRV vector: {profile['hrv_vector']}")
print(f"Source documents: {profile['metadata']['source_documents']}")
```

**Export Results**
```python
# Export as JSON
processor.export_results(
    results=results,
    output_path="results.json",
    format="json"
)

# Export as CSV
processor.export_results(
    results=results,
    output_path="results.csv",
    format="csv"
)
```

**Analyze Corpus Quality**
```python
# Analyze corpus quality
analysis = processor.analyze_corpus_quality(results)

print(f"Document count: {analysis['document_count']}")
print(f"Total words: {analysis['total_words']}")
print(f"Quality score: {analysis['quality_score']:.3f}")
print(f"HRV statistics: {analysis['hrv_statistics']}")
```

#### Command-Line Usage

```bash
# Process file or directory
python data_processing.py process \
    --input /path/to/corpus \
    --pattern "*.txt" \
    --output results.json \
    --format json

# Analyze corpus
python data_processing.py analyze \
    --input /path/to/corpus \
    --output analysis.json

# Create profile
python data_processing.py profile \
    --input /path/to/corpus \
    --profile-name my_profile \
    --output profile.json
```

#### Quality Score Calculation

The data processor calculates quality scores based on:
- **Length Score**: Ideal around 500 words per document
- **Sentence Score**: Ideal around 20 sentences per document
- **HRV Variety Score**: Average pairwise HRV distance

### 4. Profile Generator (`profile_generator.py`)

Profile generation and management utility for creating, blending, adapting, and analyzing HRV profiles.

#### Architecture

```python
class ProfileGenerator:
    """Profile generation and management utility"""
    
    def __init__(self, profiles_dir: str = None):
        self.profiles_dir = Path(profiles_dir or "./profiles/hr_profiles")
        self.manager = HRVProfileManager(self.profiles_dir)
        self.dimensions = [
            'sentence_variance',
            'emotional_valence',
            'emotional_intensity',
            'assertiveness_index',
            'curiosity_index',
            'metaphor_density',
            'storytelling_index',
            'active_voice_ratio'
        ]
```

#### Key Features

- **Profile Creation**: Create profiles from HRV vectors
- **Profile Blending**: Blend multiple profiles with weights
- **Profile Adaptation**: Adapt profiles with dimension adjustments
- **Random Generation**: Generate random profiles with constraints
- **Profile Analysis**: Compare and analyze profile differences
- **Batch Operations**: Export/import profiles in bulk

#### Usage Examples

**Create Profile from Vector**
```python
from resonance_os.data.scripts.profile_generator import ProfileGenerator

generator = ProfileGenerator()

# Create profile
profile = generator.create_profile_from_vector(
    name="professional",
    description="Professional business writing style",
    hrv_vector=[0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7],
    metadata={"industry": "business"}
)

# Save profile
generator.save_profile(tenant="default", profile_name="professional", profile=profile)
```

**Blend Profiles**
```python
# Load two profiles
profile1 = generator.load_profile(tenant="default", profile_name="professional")
profile2 = generator.load_profile(tenant="default", profile_name="creative")

# Blend with weights
blended = generator.blend_profiles(
    profile1=profile1,
    profile2=profile2,
    weight1=0.7,
    weight2=0.3
)

generator.save_profile(tenant="default", profile_name=blended['name'], profile=blended)
```

**Adapt Profile**
```python
# Load base profile
base_profile = generator.load_profile(tenant="default", profile_name="professional")

# Apply adjustments
adjustments = {
    'emotional_valence': 0.1,
    'assertiveness_index': 0.15,
    'curiosity_index': 0.05
}

adapted = generator.generate_adaptive_profile(base_profile, adjustments)

generator.save_profile(tenant="default", profile_name="adapted_professional", profile=adapted)
```

**Generate Random Profile**
```python
# Generate random profile
random_profile = generator.generate_random_profile(
    name="random_style",
    description="Randomly generated style",
    constraints={
        'emotional_valence': (0.5, 0.8),
        'assertiveness_index': (0.3, 0.7)
    }
)

generator.save_profile(tenant="default", profile_name="random_style", profile=random_profile)
```

**Analyze Profile Differences**
```python
# Load two profiles
profile1 = generator.load_profile(tenant="default", profile_name="professional")
profile2 = generator.load_profile(tenant="default", profile_name="creative")

# Analyze differences
analysis = generator.analyze_profile_differences(profile1, profile2)

print(f"Total difference: {analysis['total_difference']:.3f}")
print(f"Similarity score: {analysis['similarity_score']:.3f}")
print(f"Dimension differences: {analysis['dimension_differences']}")
```

**List Profiles**
```python
# List all profiles for tenant
profiles = generator.list_profiles(tenant="default")

for profile_name in profiles:
    print(f"- {profile_name}")
```

**Export/Import Profiles**
```python
# Export all profiles
generator.export_profile_batch(
    tenant="default",
    output_file="default_profiles.json"
)

# Import profiles
generator.import_profile_batch(
    tenant="default",
    input_file="default_profiles.json"
)
```

#### Command-Line Usage

```bash
# Create profile
python profile_generator.py create \
    --tenant default \
    --name professional \
    --vector 0.7,0.6,0.8,0.5,0.4,0.3,0.6,0.7 \
    --description "Professional business writing"

# Blend profiles
python profile_generator.py blend \
    --tenant default \
    --profile1 professional \
    --profile2 creative \
    --weight1 0.7 \
    --weight2 0.3

# Adapt profile
python profile_generator.py adapt \
    --tenant default \
    --name adapted_professional \
    --profile1 professional \
    --adjustments "emotional_valence:0.1,assertiveness_index:0.15"

# Generate random profile
python profile_generator.py random \
    --tenant default \
    --name random_style \
    --constraints "emotional_valence:0.5-0.8,assertiveness_index:0.3-0.7"

# List profiles
python profile_generator.py list \
    --tenant default

# Analyze profiles
python profile_generator.py analyze \
    --tenant default \
    --profile1 professional \
    --profile2 creative

# Export profiles
python profile_generator.py export \
    --tenant default \
    --output default_profiles.json

# Import profiles
python profile_generator.py import \
    --tenant default \
    --input default_profiles.json
```

## Integration Points

The Data Scripts Systems module integrates with:

- **Core Systems**: Uses HRV types and constants
- **Profiling Systems**: Uses HRV extractor and profile manager
- **Generation Systems**: Uses HumanResonantWriter for content generation
- **API Systems**: Uses API server for comparison

## Usage Patterns

### Large-Scale Corpus Processing

```python
# Process entire corpus with batch operations
from resonance_os.data.scripts.batch_processor import BatchProcessor
from resonance_os.data.scripts.corpus_analyzer import CorpusAnalyzer

# Analyze corpus
analyzer = CorpusAnalyzer()
corpus_analysis = analyzer.analyze_corpus("/path/to/corpus")

# Batch generate content
processor = BatchProcessor(config={'max_workers': 16})
prompts = [f"Topic {i}" for i in range(100)]
results = processor.batch_generate_content(prompts)
```

### Profile Management Workflow

```python
# Complete profile management workflow
from resonance_os.data.scripts.profile_generator import ProfileGenerator

generator = ProfileGenerator()

# Create base profiles
base_profiles = [...]
for profile_data in base_profiles:
    profile = generator.create_profile_from_vector(**profile_data)
    generator.save_profile(tenant="default", profile_name=profile['name'], profile=profile)

# Blend profiles for new styles
blended = generator.blend_profiles(profile1, profile2, 0.7, 0.3)
generator.save_profile(tenant="default", profile_name=blended['name'], profile=blended)

# Export for backup
generator.export_profile_batch(tenant="default", output_file="backup.json")
```

### Quality Assurance Pipeline

```python
# Quality assurance for generated content
from resonance_os.data.scripts.batch_processor import BatchProcessor

processor = BatchProcessor()

# Generate content
results = processor.batch_generate_content(prompts)

# Analyze quality
analysis_results = processor.batch_analyze_content([r['content'] for r in results if r['success']])

# Filter by quality
high_quality = [r for r, a in zip(results, analysis_results) if a['quality_score'] > 0.8]
```

## Best Practices

1. **Use appropriate worker counts**: Set based on CPU cores and memory
2. **Batch size optimization**: Balance between memory and throughput
3. **Monitor performance**: Track generation times and success rates
4. **Validate profiles**: Check HRV vector dimensions and values
5. **Regular backups**: Export profiles regularly for backup
6. **Quality thresholds**: Set appropriate quality score thresholds
7. **Error handling**: Implement proper error handling for batch operations
8. **Resource management**: Monitor memory usage for large batches

## Common Issues

**Issue**: Batch processing too slow
**Solution**: Increase worker count or use multiprocessing

**Issue**: Memory exhaustion
**Solution**: Reduce batch size or worker count

**Issue**: Profile creation fails
**Solution**: Verify HRV vector has exactly 8 dimensions

**Issue**: Corpus analysis errors
**Solution**: Check file encoding and format

**Issue**: Quality scores inconsistent
**Solution**: Adjust quality score calculation parameters

## Performance Considerations

- **Worker count**: Optimal at CPU count or slightly less
- **Batch size**: 32-64 for most workloads
- **Multiprocessing**: Use for CPU-bound operations
- **Threading**: Use for I/O-bound operations
- **Memory**: Monitor for large batch operations
- **Disk I/O**: SSD recommended for large corpora

## Future Enhancements

- **Distributed processing**: Support for distributed batch processing
- **Progress bars**: Real-time progress visualization
- **Resume capability**: Resume interrupted batch operations
- **Advanced metrics**: More sophisticated quality metrics
- **Template profiles**: Pre-built profile templates
- **Version control**: Profile versioning and history

## Dependencies

```bash
# Core dependencies
pip install numpy
```

## References

- [Data Systems Guide](./data-systems-guide.md)
- [Profiling Systems Guide](./profiling-systems-guide.md)
- [Generation Systems Guide](./generation-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
