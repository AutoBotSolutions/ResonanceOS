# Corpora Directory

This directory contains training, validation, and test corpora for ResonanceOS v6. Corpora are essential for training HRV extraction models, validating system performance, and testing content generation capabilities.

## 📁 Directory Structure

```
corpora/
├── README.md                    # This file
├── training/                    # Training datasets
│   ├── sample_business_corpus.json
│   ├── technical_documents.json
│   ├── creative_content.json
│   └── academic_papers.json
├── validation/                  # Validation datasets
│   ├── business_validation.json
│   ├── creative_validation.json
│   └── technical_validation.json
├── test/                        # Test datasets
│   ├── unit_test_corpus.json
│   ├── integration_test.json
│   └── performance_test.json
└── metadata/                    # Corpus metadata and schemas
    ├── corpus_schema.json
    └── corpus_statistics.json
```

## 📊 Corpus Format

All corpus files follow this standardized JSON format:

```json
{
  "name": "Corpus Name",
  "description": "Detailed description of corpus content",
  "source": "Source information",
  "language": "en",
  "category": "business|creative|technical|academic",
  "created_at": "2026-03-09T00:00:00Z",
  "version": "1.0",
  "documents": [
    {
      "id": "unique_document_id",
      "title": "Document Title",
      "content": "Document content...",
      "metadata": {
        "author": "Author Name",
        "date": "2026-03-09",
        "word_count": 1500,
        "document_type": "report|article|story|paper",
        "formality": "formal|business|casual",
        "target_audience": ["executives", "developers", "general"],
        "tags": ["tag1", "tag2", "tag3"]
      }
    }
  ],
  "statistics": {
    "total_documents": 100,
    "total_words": 50000,
    "avg_words_per_document": 500,
    "document_types": ["report", "article", "story"],
    "authors": ["Author1", "Author2"],
    "date_range": ["2026-01-01", "2026-03-09"]
  }
}
```

## 🎯 Training Corpora

### Sample Business Corpus (`training/sample_business_corpus.json`)
- **Purpose**: Train HRV extraction for business content
- **Documents**: 5 business documents
- **Total Words**: 920
- **Categories**: Reports, proposals, roadmaps, analysis, strategy

**Key Features:**
- Financial reports and analysis
- Strategic planning documents
- Business proposals and communications
- Performance metrics and KPIs

### Technical Documents Corpus (`training/technical_documents.json`)
- **Purpose**: Train HRV extraction for technical content
- **Documents**: Technical documentation and articles
- **Focus Areas**: Software development, engineering, research

### Creative Content Corpus (`training/creative_content.json`)
- **Purpose**: Train HRV extraction for creative writing
- **Documents**: Stories, blogs, marketing content
- **Styles**: Narrative, descriptive, persuasive

### Academic Papers Corpus (`training/academic_papers.json`)
- **Purpose**: Train HRV extraction for academic content
- **Documents**: Research papers, theses, educational content
- **Fields**: Computer science, linguistics, psychology

## ✅ Validation Corpora

### Business Validation (`validation/business_validation.json`)
- **Purpose**: Validate business content HRV extraction
- **Size**: 20 documents
- **Use Case**: Model validation and performance testing

### Creative Validation (`validation/creative_validation.json`)
- **Purpose**: Validate creative content analysis
- **Size**: 15 documents
- **Use Case**: Creative writing model validation

### Technical Validation (`validation/technical_validation.json`)
- **Purpose**: Validate technical content processing
- **Size**: 25 documents
- **Use Case**: Technical documentation validation

## 🧪 Test Corpora

### Unit Test Corpus (`test/unit_test_corpus.json`)
- **Purpose**: Unit testing of individual components
- **Size**: 10 diverse documents
- **Use Case**: Component-level testing

### Integration Test Corpus (`test/integration_test.json`)
- **Purpose**: End-to-end system testing
- **Size**: 15 documents
- **Use Case**: Full pipeline testing

### Performance Test Corpus (`test/performance_test.json`)
- **Purpose**: Performance benchmarking
- **Size**: 100 documents
- **Use Case**: Load and stress testing

## 📈 Corpus Statistics

### Size Metrics
- **Training**: ~50,000 words across 200 documents
- **Validation**: ~15,000 words across 60 documents
- **Test**: ~25,000 words across 125 documents

### Distribution
- **Business**: 40% of total corpus
- **Technical**: 30% of total corpus
- **Creative**: 20% of total corpus
- **Academic**: 10% of total corpus

### Quality Metrics
- **Average HRV Score**: 0.76
- **Readability Range**: 30-80 (Flesch score)
- **Content Quality**: 85% rated as good or excellent

## 🚀 Usage Examples

### Loading and Analyzing Corpus

```bash
# Analyze business corpus
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/sample_business_corpus.json \
  --output business_corpus_analysis.json

# Analyze all training corpora
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output all_training_analysis.json
```

### Training HRV Models

```bash
# Train on business corpus
python data/scripts/data_processing.py process \
  --input corpora/training/sample_business_corpus.json \
  --output training_data.json \
  --format json

# Use training data for model training
python -c "
import json
from resonance_os.profiles.hrv_extractor import HRVExtractor

extractor = HRVExtractor()
training_data = json.load(open('training_data.json'))

# Process each document for training
for result in training_data:
    if 'hrv_vector' in result:
        print(f'Training on: {result[\"file_path\"]}')
        print(f'HRV: {result[\"hrv_vector\"]}')
"
```

### Validating Model Performance

```bash
# Validate on business validation corpus
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/validation/business_validation.json \
  --output validation_results.json

# Check validation metrics
python -c "
import json
results = json.load(open('validation_results.json'))
print(f'Validation HRV Score: {results[\"hrv_analysis\"][\"overall_score\"]:.2f}')
print(f'Quality Score: {results[\"quality_metrics\"][\"overall_quality\"]:.2f}')
"
```

### Running Performance Tests

```bash
# Performance test with performance corpus
python data/scripts/batch_processor.py generate \
  --input corpora/test/performance_test.json \
  --output performance_results.json \
  --workers 4

# Analyze performance
python -c "
import json
results = json.load(open('performance_results.json'))
total_time = sum(r['generation_time'] for r in results if 'generation_time' in r)
avg_time = total_time / len(results)
print(f'Average Generation Time: {avg_time:.3f}s')
print(f'Total Documents: {len(results)}')
"
```

## 📊 Corpus Analysis

### HRV Distribution Analysis

```bash
# Analyze HRV distribution across corpora
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output hrv_distribution.json

# View distribution
python -c "
import json
analysis = json.load(open('hrv_distribution.json'))
print('HRV Dimension Statistics:')
for dim, stats in analysis['hrv_analysis']['dimension_statistics'].items():
    print(f'{dim}: mean={stats[\"mean\"]:.3f}, std={stats[\"std\"]:.3f}')
"
```

### Content Type Analysis

```bash
# Analyze content type distribution
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output content_analysis.json

# View content distribution
python -c "
import json
analysis = json.load(open('content_analysis.json'))
print('Content Distribution:')
for content_type, count in analysis['content_distribution']['content_types'].items():
    print(f'{content_type}: {count} documents')
"
```

### Quality Assessment

```bash
# Assess corpus quality
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output quality_assessment.json

# View quality metrics
python -c "
import json
assessment = json.load(open('quality_assessment.json'))
print(f'Overall Quality Score: {assessment[\"quality_metrics\"][\"overall_score\"]:.2f}')
print(f'Readability Score: {assessment[\"quality_metrics\"][\"readability_score\"]:.2f}')
print(f'HRV Balance Score: {assessment[\"quality_metrics\"][\"hrv_balance\"]:.2f}')
"
```

## 🛠️ Corpus Management

### Adding New Corpora

1. **Create Corpus File**
```bash
# Create new corpus file
nano corpora/training/your_new_corpus.json
```

2. **Follow Format Schema**
```json
{
  "name": "Your New Corpus",
  "description": "Description of your corpus",
  "language": "en",
  "category": "your_category",
  "documents": [
    {
      "id": "doc_001",
      "title": "Document Title",
      "content": "Document content...",
      "metadata": {
        "author": "Author",
        "date": "2026-03-09",
        "word_count": 1000
      }
    }
  ]
}
```

3. **Validate Corpus**
```bash
# Validate corpus format
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/your_new_corpus.json \
  --output validation.json

# Check validation results
python -c "
import json
results = json.load(open('validation.json'))
if 'error' in results:
    print(f'Validation Error: {results[\"error\"]}')
else:
    print(f'Corpus Valid: {results[\"valid_files\"]} documents')
"
```

4. **Update Statistics**
```bash
# Update corpus statistics
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output updated_statistics.json
```

### Corpus Preprocessing

```bash
# Preprocess raw text files
python data/scripts/data_processing.py process \
  --input raw_text_files/ \
  --output corpora/training/processed_corpus.json \
  --format json

# Clean and normalize text
python -c "
import json
import re

def clean_text(text):
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Fix common punctuation issues
    text = re.sub(r' +', ' ', text)
    return text.strip()

corpus = json.load(open('corpora/training/processed_corpus.json'))
for doc in corpus['documents']:
    doc['content'] = clean_text(doc['content'])

with open('corpora/training/cleaned_corpus.json', 'w') as f:
    json.dump(corpus, f, indent=2)
"
```

### Corpus Quality Enhancement

```bash
# Enhance corpus quality
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output quality_report.json

# Filter low-quality documents
python -c "
import json

report = json.load(open('quality_report.json'))
high_quality_docs = []

for doc in report['file_analyses']:
    if 'quality_score' in doc and doc['quality_score'] > 0.7:
        high_quality_docs.append(doc)

print(f'High-quality documents: {len(high_quality_docs)}/{len(report[\"file_analyses\"])}')
"
```

## 📋 Corpus Development Guidelines

### Quality Standards
- **Minimum Word Count**: 100 words per document
- **Maximum Word Count**: 5,000 words per document
- **HRV Score**: > 0.60 average
- **Readability**: 30-80 Flesch score
- **Content Quality**: No plagiarism, original content

### Diversity Requirements
- **Author Diversity**: Minimum 5 different authors per corpus
- **Topic Variety**: Multiple sub-topics within category
- **Style Variation**: Different writing styles and tones
- **Length Distribution**: Mix of short, medium, and long documents

### Metadata Requirements
- **Required Fields**: id, title, content, author, date
- **Recommended Fields**: word_count, document_type, formality, target_audience
- **Optional Fields**: tags, source, language, category

## 🔧 Corpus Maintenance

### Regular Updates
- Add new documents monthly
- Remove outdated content quarterly
- Refresh validation datasets bi-annually
- Update test corpora annually

### Quality Assurance
- Validate corpus formats weekly
- Check HRV score distributions monthly
- Review content quality quarterly
- Update metadata as needed

### Version Control
```bash
# Track corpus changes
git add corpora/
git commit -m "Corpus updates: new documents and quality improvements"

# Tag corpus versions
git tag -a corpus_v1.1 -m "Corpus version 1.1 with quality improvements"
```

## 🆘 Troubleshooting

### Common Issues

1. **Corpus Format Errors**
```bash
# Validate JSON format
python -m json.tool corpora/training/sample_business_corpus.json

# Check against schema
python -c "
import json
schema = json.load(open('data/profiles/schemas/profile_schema.json'))
# Validate corpus against schema
"
```

2. **Low HRV Scores**
```bash
# Analyze HRV distribution
python data/scripts/corpus_analyzer.py analyze \
  --input corpora/training/ \
  --output hrv_analysis.json

# Identify low-scoring documents
python -c "
import json
analysis = json.load(open('hrv_analysis.json'))
outliers = analysis['hrv_analysis']['outliers']
print(f'Low HRV documents: {len(outliers)}')
"
```

3. **Performance Issues**
```bash
# Check corpus size
du -sh corpora/training/

# Optimize corpus loading
python data/scripts/batch_processor.py metrics
```

### Getting Help

- Review corpus documentation
- Check format schemas
- Validate file integrity
- Contact support: support@resonanceos.ai

## 📚 Corpus Resources

### External Corpora
- **Common Crawl**: Web-scale text corpus
- **Wikipedia Dump**: Encyclopedic content
- **arXiv**: Academic papers
- **Project Gutenberg**: Literary works

### Processing Tools
- **NLTK**: Natural language processing
- **spaCy**: Advanced NLP library
- **TextBlob**: Simple text processing
- **BeautifulSoup**: Web scraping

### Quality Assessment
- **Grammarly**: Writing quality checker
- **Hemingway Editor**: Readability analyzer
- **Copyscape**: Plagiarism detection
- **Readable**: Readability scoring

This corpora directory provides comprehensive training, validation, and test datasets to ensure ResonanceOS v6 delivers high-quality, human-resonant content across all use cases.
