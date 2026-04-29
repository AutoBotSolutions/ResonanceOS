# Samples Directory

This directory contains sample data, examples, and templates to help you understand and use ResonanceOS v6 effectively.

## 📁 Directory Structure

```
samples/
├── README.md                    # This file
├── sample_texts/               # Example text files
│   ├── business_report.txt      # Business communication example
│   ├── creative_story.txt       # Creative writing example
│   └── technical_article.txt    # Technical writing example
├── sample_profiles/            # Example HRV profiles
│   ├── tech_startup.json        # Technology startup profile
│   └── lifestyle_blog.json      # Lifestyle blog profile
└── example_outputs/            # Generated content examples
    └── generated_business_report.txt
```

## 📝 Sample Texts

### Business Report (`sample_texts/business_report.txt`)
- **Purpose**: Demonstrates professional business communication
- **Style**: Formal, data-driven, analytical
- **Length**: ~500 words
- **Use Case**: Financial reports, strategic planning, business analysis

**Key Features:**
- Executive summary format
- Data-driven insights
- Professional terminology
- Structured recommendations

### Creative Story (`sample_texts/creative_story.txt`)
- **Purpose**: Shows creative storytelling capabilities
- **Style**: Narrative, descriptive, engaging
- **Length**: ~800 words
- **Use Case**: Blog posts, creative content, storytelling

**Key Features:**
- Narrative structure
- Descriptive language
- Emotional engagement
- Character development

### Technical Article (`sample_texts/technical_article.txt`)
- **Purpose**: Technical and academic writing example
- **Style**: Formal, precise, educational
- **Length**: ~1000 words
- **Use Case**: Documentation, research papers, technical articles

**Key Features:**
- Technical terminology
- Structured arguments
- Citations and references
- Methodical presentation

## 👥 Sample Profiles

### Tech Startup Profile (`sample_profiles/tech_startup.json`)
- **Target Audience**: Investors, employees, customers
- **Tone**: Innovative, confident, forward-thinking
- **Use Cases**: Pitch decks, investor updates, product announcements

**HRV Vector**: `[0.6, 0.4, 0.7, 0.7, 0.8, 0.3, 0.4, 0.8]`

**Key Characteristics:**
- High assertiveness (0.7)
- Strong curiosity (0.8)
- Professional tone (0.8 active voice)
- Moderate emotional intensity (0.7)

### Lifestyle Blog Profile (`sample_profiles/lifestyle_blog.json`)
- **Target Audience**: General consumers, wellness enthusiasts
- **Tone**: Friendly, inspiring, relatable
- **Use Cases**: Blog posts, social media, newsletters

**HRV Vector**: `[0.7, 0.6, 0.8, 0.3, 0.7, 0.6, 0.8, 0.6]`

**Key Characteristics:**
- High storytelling (0.8)
- Strong emotional content (0.6, 0.8)
- Engaging curiosity (0.7)
- Conversational style (0.6 active voice)

## 🎯 Example Outputs

### Generated Business Report (`example_outputs/generated_business_report.txt`)
Demonstrates the complete generation pipeline:
- **Input**: "Q4 2024 Strategic Planning and Market Analysis"
- **Process**: Planning → Generation → Refinement → HRF Feedback
- **Output**: Professional business content with HRV feedback integration

**Key Features:**
- Paragraph-level HRF feedback scores
- HRV vector analysis
- Performance metrics
- Quality assessment

## 🚀 Usage Examples

### Analyzing Sample Texts

```bash
# Analyze business report
python data/scripts/data_processing.py single \
  --input samples/sample_texts/business_report.txt

# Analyze all sample texts
python data/scripts/data_processing.py process \
  --input samples/sample_texts/ \
  --output sample_analysis.json
```

### Using Sample Profiles

```bash
# Generate content with tech startup profile
python -c "
from resonance_os.api.hr_server import hr_generate, SimpleRequest
request = SimpleRequest(
    prompt='Our latest product launch',
    profile_name='tech_startup'
)
response = hr_generate(request)
print(response.article)
"
```

### Creating Profiles from Samples

```bash
# Create profile from business report
python data/scripts/data_processing.py profile \
  --input samples/sample_texts/business_report.txt \
  --output profiles/business_profile.json \
  --profile-name "Business Communication"
```

## 📊 Sample Analysis Results

### HRV Vector Analysis

| Text Type | Sentence Variance | Emotional Valence | Emotional Intensity | Assertiveness |
|-----------|------------------|-------------------|--------------------|---------------|
| Business Report | 0.45 | -0.08 | 0.24 | 0.78 |
| Creative Story | 0.82 | 0.67 | 0.91 | 0.34 |
| Technical Article | 0.32 | -0.12 | 0.18 | 0.81 |

### Performance Metrics

| Metric | Business Report | Creative Story | Technical Article |
|--------|-----------------|----------------|------------------|
| Word Count | 456 | 782 | 1,024 |
| Sentences | 18 | 34 | 42 |
| Avg. Sentence Length | 25.3 | 23.0 | 24.4 |
| Readability Score | 45.2 | 68.7 | 38.9 |

## 🎨 Customization Examples

### Modifying Sample Profiles

```bash
# Create more aggressive tech profile
python data/scripts/profile_generator.py adapt \
  --tenant samples \
  --profile1 tech_startup \
  --name aggressive_tech \
  --adjustments "assertiveness_index:0.2,emotional_valence:0.1"
```

### Blending Sample Profiles

```bash
# Blend tech and creative profiles
python data/scripts/profile_generator.py blend \
  --tenant samples \
  --profile1 tech_startup \
  --profile2 lifestyle_blog \
  --weight1 0.6 \
  --weight2 0.4
```

### Creating Custom Samples

```bash
# Add your own sample text
echo "Your custom content here" > samples/sample_texts/your_sample.txt

# Analyze your sample
python data/scripts/corpus_analyzer.py single \
  --input samples/sample_texts/your_sample.txt
```

## 📋 Sample Categories

### Content Types
- **Business**: Reports, proposals, communications
- **Creative**: Stories, blogs, marketing content
- **Technical**: Documentation, articles, research
- **Academic**: Papers, thesis, educational content

### Profile Categories
- **Professional**: Business, academic, formal
- **Creative**: Storytelling, marketing, engaging
- **Technical**: Documentation, precise, informative
- **Casual**: Blogs, social media, conversational

## 🔍 Quality Assessment

### Sample Quality Metrics

All samples meet these quality standards:
- **HRV Alignment**: > 0.70 average score
- **Readability**: Appropriate for target audience
- **Coherence**: Logical flow and structure
- **Engagement**: Suitable for intended use case

### Evaluation Criteria

| Criterion | Excellent | Good | Acceptable |
|-----------|------------|------|------------|
| HRV Score | > 0.85 | 0.70-0.85 | 0.55-0.70 |
| Readability | 60-80 | 40-60 | 30-40 |
| Coherence | > 0.90 | 0.80-0.90 | 0.70-0.80 |
| Engagement | > 0.85 | 0.70-0.85 | 0.55-0.70 |

## 🛠️ Sample Development

### Creating New Samples

1. **Write Sample Content**
```bash
# Create new sample
nano samples/sample_texts/your_new_sample.txt
```

2. **Analyze HRV Features**
```bash
python data/scripts/corpus_analyzer.py single \
  --input samples/sample_texts/your_new_sample.txt
```

3. **Create Matching Profile**
```bash
python data/scripts/data_processing.py profile \
  --input samples/sample_texts/your_new_sample.txt \
  --output samples/sample_profiles/your_new_profile.json \
  --profile-name "Your New Profile"
```

4. **Test Generation**
```bash
python -c "
from resonance_os.api.hr_server import hr_generate, SimpleRequest
request = SimpleRequest(
    prompt='Test prompt',
    profile_name='your_new_profile'
)
response = hr_generate(request)
print(response.article)
"
```

### Sample Validation

```bash
# Validate all samples
python data/scripts/corpus_analyzer.py analyze \
  --input samples/sample_texts/ \
  --output samples_validation.json

# Check sample quality
python -c "
import json
results = json.load(open('samples_validation.json'))
print('Sample Quality Report:')
print(f'Total Samples: {results[\"valid_files\"]}')
print(f'Average HRV Score: {results[\"hrv_analysis\"][\"overall_score\"]:.2f}')
"
```

## 📚 Learning Resources

### Understanding HR Vectors
- Study the 8-dimensional HRV system
- Compare vectors across different content types
- Analyze how dimensions affect content style

### Profile Creation
- Use sample profiles as templates
- Understand HRV vector tuning
- Practice profile adaptation and blending

### Content Generation
- Study sample outputs for structure
- Analyze HRF feedback integration
- Learn quality assessment techniques

## 🔧 Sample Maintenance

### Regular Updates
- Add new sample texts periodically
- Update profiles based on usage patterns
- Refresh example outputs with latest models

### Quality Assurance
- Validate sample HRV scores
- Check content quality metrics
- Ensure appropriate use case alignment

### Community Contributions
- Share custom samples with community
- Contribute new profile templates
- Provide feedback on sample effectiveness

## 🆘 Troubleshooting

### Common Issues

1. **Sample Not Loading**
```bash
# Check file paths
ls -la samples/sample_texts/
python -c "import os; print(os.path.exists('samples/sample_texts/business_report.txt'))"
```

2. **Profile Not Working**
```bash
# Validate profile format
python -c "import json; json.load(open('samples/sample_profiles/tech_startup.json'))"
```

3. **Generation Quality Poor**
```bash
# Check HRV alignment
python data/scripts/data_processing.py single \
  --input samples/sample_texts/business_report.txt
```

### Getting Help

- Review sample documentation
- Check configuration settings
- Validate file formats
- Contact support: support@resonanceos.ai

This samples directory provides comprehensive examples to help you master ResonanceOS v6 capabilities and create effective content for any use case.
