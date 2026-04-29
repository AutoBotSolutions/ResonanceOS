# Profiling Systems Guide - ResonanceOS v6

## Overview

The Profiling Systems module provides comprehensive corpus loading, profile persistence, and style vector building capabilities for ResonanceOS v6. This module enables the analysis of text corpora to extract HRV profiles, persistent storage of style profiles, and advanced linguistic feature extraction.

## System Architecture

```
Profiling Systems
├── corpus_loader.py (Corpus Loading and Preprocessing)
├── profile_persistence.py (Profile Storage and Management)
└── style_vector_builder.py (Style Vector Extraction)
```

## System Components

### 1. Corpus Loader (`corpus_loader.py`)

Loads and processes text corpora for style analysis with support for multiple file formats and intelligent preprocessing.

#### Architecture

```python
@dataclass
class TextDocument:
    """Single text document"""
    content: str
    source: str
    file_path: Optional[Path] = None
    metadata: Optional[Dict] = None

class CorpusLoader:
    """Loads and processes text corpora for style analysis"""
    
    def __init__(self):
        self.config = get_config()
        self.supported_extensions = {'.txt', '.md', '.rtf', '.html', '.htm'}
```

#### Supported File Formats

- `.txt` - Plain text files
- `.md` - Markdown files
- `.rtf` - Rich text format
- `.html` / `.htm` - HTML files
- Future: `.pdf`, `.docx` (with additional dependencies)

#### Usage Example

```python
from resonance_os.resonance_os.profiling.corpus_loader import CorpusLoader

loader = CorpusLoader()

# Load from directory
documents = loader.load_corpus("/path/to/corpus", recursive=True)
print(f"Loaded {len(documents)} documents")

# Load single file
documents = loader.load_corpus("/path/to/document.txt")

# Analyze corpus
corpus_info = loader.analyze_corpus(documents)
print(f"Total words: {corpus_info.total_words}")
print(f"Total sentences: {corpus_info.total_sentences}")
print(f"Language: {corpus_info.language}")
```

#### Document Iterator

For large corpora, use the iterator to avoid memory issues:

```python
from resonance_os.resonance_os.profiling.corpus_loader import DocumentIterator

iterator = DocumentIterator(Path("/path/to/large/corpus"), batch_size=100)

for batch in iterator:
    # Process batch of documents
    for doc in batch:
        print(f"Processing: {doc.source}")
```

#### Preprocessing Features

- **Encoding detection**: Automatic encoding detection using chardet
- **HTML tag removal**: Strips HTML tags from content
- **Whitespace normalization**: Removes excessive whitespace
- **Quote normalization**: Normalizes different quote characters
- **Punctuation normalization**: Fixes excessive punctuation
- **Content splitting**: Splits long documents into manageable chunks

#### Corpus Analysis

```python
# Analyze corpus statistics
corpus_info = loader.analyze_corpus(documents)

# Save analysis
loader.save_corpus_info(corpus_info, Path("corpus_analysis.json"))

# Load analysis
loaded_info = loader.load_corpus_info(Path("corpus_analysis.json"))
```

### 2. Profile Persistence (`profile_persistence.py`)

Handles saving and loading of style profiles with support for multiple formats and version management.

#### Architecture

```python
class ProfilePersistence:
    """Handles saving and loading of style profiles"""
    
    def __init__(self, profiles_dir: Optional[Path] = None):
        self.config = get_config()
        self.profiles_dir = profiles_dir or self.config.paths.profiles_dir
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
```

#### Supported Formats

- **JSON**: Human-readable, portable format (default)
- **Pickle**: Binary format for Python objects

#### Usage Example

```python
from resonance_os.resonance_os.profiling.profile_persistence import ProfilePersistence
from resonance_os.resonance_os.core.types import StyleProfile, ResonanceVector

persistence = ProfilePersistence(Path("/path/to/profiles"))

# Create profile
profile = StyleProfile(
    name="professional_tone",
    description="Professional business writing style",
    resonance_vector=ResonanceVector(
        values=[0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7],
        dimensions=RESONANCE_DIMENSIONS,
        confidence=0.95
    )
)

# Save profile
profile_path = persistence.save_profile(profile, format="json")

# Load profile
loaded_profile = persistence.load_profile(profile_path)

# List all profiles
profiles = persistence.list_profiles()
for profile_info in profiles:
    print(f"Name: {profile_info['name']}")
    print(f"Confidence: {profile_info['confidence']:.2f}")
```

#### Profile Management

**Load by Name**

```python
# Load most recent version by name
profile = persistence.load_profile_by_name("professional_tone")
```

**Delete Profile**

```python
# Delete all versions of a profile
deleted = persistence.delete_profile("professional_tone")
```

**Export/Import**

```python
# Export specific profiles
persistence.export_profiles(
    Path("exports/selected_profiles.json"),
    profile_names=["professional_tone", "creative_style"]
)

# Import profiles
count = persistence.import_profiles(Path("exports/selected_profiles.json"))
```

**Backup/Restore**

```python
# Create backup
backup_path = persistence.create_profile_backup()

# Restore from backup
restored_count = persistence.restore_profile_backup(backup_path)
```

#### Profile Validation

```python
# Validate profile structure
errors = persistence.validate_profile(profile)
if errors:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Profile is valid")
```

#### Profile Statistics

```python
# Get statistics about stored profiles
stats = persistence.get_profile_statistics()
print(f"Total profiles: {stats['total_profiles']}")
print(f"Average confidence: {stats['average_confidence']:.2f}")
print(f"Formats: {stats['formats']}")
```

### 3. Style Vector Builder (`style_vector_builder.py`)

Builds resonance vectors from text documents using multi-tier linguistic analysis.

#### Architecture

```python
class StyleVectorBuilder:
    """Builds resonance vectors from text documents"""
    
    def __init__(self, tier: int = 1):
        self.tier = tier
        self.config = get_config()
        self._load_models()
```

#### Analysis Tiers

**Tier 1: Basic Statistical Features**
- Lexical density
- Emotional valence (TextBlob)
- Cadence variability
- Sentence entropy
- Metaphor frequency (pattern-based)
- Abstraction level
- Assertiveness score
- Rhythm signature
- Narrative intensity curve
- Cognitive load index

**Tier 2: Advanced Linguistic Features**
- Enhanced lexical density (POS tagging)
- Enhanced emotional analysis (spaCy)
- Enhanced cadence analysis (spaCy)
- Enhanced abstraction analysis (spaCy)

**Tier 3: Transformer-Based Features**
- Transformer-based feature extraction (placeholder for future implementation)

#### Usage Example

```python
from resonance_os.resonance_os.profiling.style_vector_builder import StyleVectorBuilder
from resonance_os.resonance_os.profiling.corpus_loader import CorpusLoader

# Load corpus
loader = CorpusLoader()
documents = loader.load_corpus("/path/to/corpus")

# Build vector (Tier 1)
builder = StyleVectorBuilder(tier=1)
vector = builder.build_vector(documents)

print(f"Resonance Vector: {vector.values}")
print(f"Confidence: {vector.confidence:.2f}")
print(f"Dimensions: {vector.dimensions}")
```

#### Feature Extraction

**Basic Features**

```python
# Extract basic features
features = builder._extract_basic_features(documents)

for feature_name, value in features.items():
    print(f"{feature_name}: {value:.3f}")
```

**Linguistic Features**

```python
# Use Tier 2 for advanced features
builder = StyleVectorBuilder(tier=2)
vector = builder.build_vector(documents)
```

#### Feature Analysis

**Sentiment Analysis**

```python
# Analyze sentiment
text = "The innovative technology transforms how we approach sustainable energy solutions."
sentiment = builder._analyze_sentiment(text)
print(f"Sentiment: {sentiment:.3f}")  # Range: [-1, 1]
```

**Metaphor Detection**

```python
# Detect metaphors
metaphor_frequency = builder._detect_metaphors(text)
print(f"Metaphor frequency: {metaphor_frequency:.3f}")
```

**Abstraction Analysis**

```python
# Analyze abstraction level
abstraction = builder._analyze_abstraction(text)
print(f"Abstraction level: {abstraction:.3f}")  # 0 = concrete, 1 = abstract
```

**Cognitive Load**

```python
# Analyze cognitive load
cognitive_load = builder._analyze_cognitive_load(text)
print(f"Cognitive load: {cognitive_load:.3f}")
```

#### Tier Management

```python
# Change analysis tier
builder.set_tier(2)  # Upgrade to Tier 2
builder.set_tier(1)  # Downgrade to Tier 1
```

## Integration Points

The Profiling Systems module integrates with:

- **Core Systems**: Uses types, constants, and logging
- **Profile Systems**: Provides profile data for profile manager
- **Similarity Systems**: Uses similarity metrics for comparison
- **Generation Systems**: Provides target HRV vectors for generation

## Usage Patterns

### Complete Profile Creation Workflow

```python
from resonance_os.resonance_os.profiling.corpus_loader import CorpusLoader
from resonance_os.resonance_os.profiling.style_vector_builder import StyleVectorBuilder
from resonance_os.resonance_os.profiling.profile_persistence import ProfilePersistence
from resonance_os.resonance_os.core.types import StyleProfile

# 1. Load corpus
loader = CorpusLoader()
documents = loader.load_corpus("/path/to/sample_writings", recursive=True)

# 2. Build resonance vector
builder = StyleVectorBuilder(tier=2)
vector = builder.build_vector(documents)

# 3. Create profile
profile = StyleProfile(
    name="brand_voice_v1",
    description="Brand voice extracted from sample writings",
    resonance_vector=vector,
    metadata={
        "source_documents": len(documents),
        "created_by": "system",
        "tier": 2
    }
)

# 4. Save profile
persistence = ProfilePersistence()
profile_path = persistence.save_profile(profile, format="json")

print(f"Profile saved to: {profile_path}")
```

### Batch Profile Creation

```python
# Create profiles for multiple authors
authors = ["author_a", "author_b", "author_c"]

for author in authors:
    corpus_path = f"/path/to/corpora/{author}"
    documents = loader.load_corpus(corpus_path)
    
    if documents:
        vector = builder.build_vector(documents)
        profile = StyleProfile(
            name=f"{author}_style",
            description=f"Writing style of {author}",
            resonance_vector=vector
        )
        persistence.save_profile(profile)
```

### Profile Comparison

```python
from resonance_os.resonance_os.similarity.metrics import SimilarityCalculator

# Load two profiles
profile_a = persistence.load_profile_by_name("author_a_style")
profile_b = persistence.load_profile_by_name("author_b_style")

# Compare vectors
calculator = SimilarityCalculator()
similarity = calculator.calculate_similarity(
    profile_a.resonance_vector.values,
    profile_b.resonance_vector.values
)

print(f"Similarity: {similarity:.3f}")
```

## Performance Considerations

- **CorpusLoader**: Fast for small corpora, use iterator for large corpora
- **ProfilePersistence**: Fast JSON/pickle operations
- **StyleVectorBuilder**: 
  - Tier 1: Fast, no external dependencies
  - Tier 2: Moderate, requires spaCy
  - Tier 3: Slow, requires transformer models

## Best Practices

1. **Use iterators**: For large corpora to avoid memory issues
2. **Validate profiles**: Always validate before using profiles
3. **Backup regularly**: Create profile backups before major changes
4. **Choose appropriate tier**: Use Tier 1 for speed, Tier 2 for accuracy
5. **Monitor confidence**: Check confidence scores for profile reliability

## Common Issues

**Issue**: Encoding errors loading files
**Solution**: Ensure chardet is installed, or specify encoding manually

**Issue**: spaCy model not found
**Solution**: Install spaCy model: `python -m spacy download en_core_web_sm`

**Issue**: Low confidence scores
**Solution**: Increase document count or use higher analysis tier

**Issue**: Memory errors with large corpora
**Solution**: Use DocumentIterator instead of loading all documents

## Dependencies

```bash
# Basic dependencies
pip install chardet

# Tier 2 dependencies
pip install spacy textblob nltk
python -m spacy download en_core_web_sm
python -m textblob.download_corpora
python -m nltk.downloader punkt vader_lexicon

# Tier 3 dependencies (future)
# pip install transformers torch
```

## Future Enhancements

- **Additional file formats**: PDF, DOCX support
- **Incremental updates**: Update profiles with new documents
- **Profile versioning**: Automatic version management
- **Profile clustering**: Group similar profiles automatically
- **Transformer tier**: Full transformer-based analysis
- **Distributed processing**: Parallel corpus processing
- **Web interface**: UI for profile management

## Troubleshooting

**Issue**: Import errors for chardet
**Solution**: Install with `pip install chardet`

**Issue**: NLTK data not found
**Solution**: Run `python -m nltk.downloader punkt vader_lexicon`

**Issue**: spaCy import errors
**Solution**: Install spaCy: `pip install spacy` and download model

**Issue**: Profile validation errors
**Solution**: Check resonance vector values are in [0.0, 1.0] range

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [Similarity Systems Guide](./similarity-systems-guide.md)
