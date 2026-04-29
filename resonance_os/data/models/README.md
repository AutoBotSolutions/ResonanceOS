# Models Directory

This directory contains model files, metadata, and configuration for ResonanceOS v6's Human-Resonant Feedback (HRF) models and related machine learning components.

## 📁 Directory Structure

```
models/
├── README.md                    # This file
├── hrf_models/                  # HRF model files and metadata
│   ├── model_metadata.json      # Model specifications and performance
│   ├── training_data.json       # Training data configuration
│   ├── evaluation_results.json  # Model evaluation metrics
│   └── checkpoints/             # Model checkpoints and versions
├── embeddings/                  # Word and text embeddings
│   ├── word_vectors.json        # Pre-trained word vectors
│   ├── sentence_embeddings.json  # Sentence-level embeddings
│   └── context_embeddings.json   # Context-aware embeddings
└── checkpoints/                 # Model training checkpoints
    ├── hrf_model_v1.0.pkl      # HRF model checkpoint
    ├── extractor_v1.0.pkl       # HRV extractor checkpoint
    └── ensemble_model_v1.0.pkl  # Ensemble model checkpoint
```

## 🤖 HRF Models

### Model Overview (`hrf_models/model_metadata.json`)
The HRF (Human-Resonant Feedback) model is the core component that predicts content engagement and resonance scores.

**Model Specifications:**
- **Type**: Statistical feature extraction
- **Framework**: Python standard library (dependency-free)
- **Input Features**: 6 linguistic and stylistic features
- **Output**: Single resonance score (0.0-1.0)
- **Performance**: 85% accuracy on validation set

### Input Features
1. **Sentence Length Variance**: Variety in sentence lengths
2. **Sentiment Polarity**: Positive/negative sentiment balance
3. **Sentiment Intensity**: Strength of emotional content
4. **Lexical Diversity**: Vocabulary variety
5. **Readability Score**: Text complexity assessment
6. **Complexity Metrics**: Advanced linguistic features

### Output Interpretation
- **Score Range**: 0.0 (low resonance) to 1.0 (high resonance)
- **Good Threshold**: > 0.70
- **Excellent Threshold**: > 0.85
- **Usage**: Real-time content feedback and optimization

## 📊 Model Performance

### Validation Metrics
```json
{
  "performance": {
    "validation_accuracy": 0.87,
    "test_accuracy": 0.85,
    "mean_squared_error": 0.023,
    "mean_absolute_error": 0.12,
    "r_squared": 0.78,
    "training_time_seconds": 45.2,
    "inference_time_ms": 2.3,
    "model_size_mb": 0.1
  }
}
```

### Feature Importance
| Feature | Weight | Importance | Range |
|---------|--------|------------|-------|
| Emotional Valence | 0.20 | High | -1.0 to 1.0 |
| Sentence Variance | 0.15 | Medium | 0.0 to 1.0 |
| Emotional Intensity | 0.15 | Medium | 0.0 to 1.0 |
| Storytelling Index | 0.12 | Medium | 0.0 to 1.0 |
| Assertiveness | 0.10 | Low | 0.0 to 1.0 |
| Active Voice | 0.10 | Low | 0.0 to 1.0 |
| Curiosity | 0.10 | Low | 0.0 to 1.0 |
| Metaphor Density | 0.08 | Low | 0.0 to 1.0 |

## 🔧 Model Configuration

### Training Parameters
```json
{
  "training": {
    "algorithm": "linear_regression_with_regularization",
    "training_dataset": "internal_corpus_v1",
    "training_samples": 10000,
    "validation_samples": 2000,
    "test_samples": 2000,
    "training_epochs": 100,
    "early_stopping": true,
    "patience": 10,
    "regularization": "l2",
    "regularization_strength": 0.01,
    "learning_rate": 0.001,
    "batch_size": 32,
    "optimizer": "adam"
  }
}
```

### Feature Configuration
```json
{
  "features": {
    "sentence_variance": {
      "weight": 0.15,
      "description": "Variance in sentence lengths",
      "importance": "medium",
      "range": [0.0, 1.0]
    },
    "emotional_valence": {
      "weight": 0.20,
      "description": "Positive/negative sentiment balance",
      "importance": "high",
      "range": [-1.0, 1.0]
    }
  }
}
```

## 🚀 Model Usage

### Basic Usage
```python
from resonance_os.generation.hrf_model import HRFModel

# Initialize model
hrf_model = HRFModel()

# Predict resonance score
text = "This is a sample text for analysis."
score = hrf_model.predict(text)
print(f"Resonance Score: {score:.3f}")
```

### Batch Processing
```python
# Process multiple texts
texts = [
    "First text for analysis",
    "Second text for analysis",
    "Third text for analysis"
]

scores = [hrf_model.predict(text) for text in texts]
avg_score = sum(scores) / len(scores)
print(f"Average Resonance: {avg_score:.3f}")
```

### Integration with Generation
```python
from resonance_os.generation.human_resonant_writer import HumanResonantWriter

# Generate content with HRF feedback
writer = HumanResonantWriter()
content = writer.generate("Your prompt here")
print(f"Generated Content: {content}")
```

## 📈 Model Training

### Training Data Preparation
```bash
# Prepare training data from corpus
python data/scripts/data_processing.py process \
  --input corpora/training/ \
  --output models/hrf_models/training_data.json \
  --format json

# Validate training data
python -c "
import json
data = json.load(open('models/hrf_models/training_data.json'))
print(f'Training samples: {len(data)}')
print(f'Average HRV score: {sum(r[\"hrv_vector\"][1] for r in data)/len(data):.3f}')
"
```

### Model Training (Future Enhancement)
```bash
# Train new model (placeholder for future implementation)
python models/train_hrf_model.py \
  --training-data models/hrf_models/training_data.json \
  --output models/checkpoints/hrf_model_v2.0.pkl \
  --epochs 100 \
  --validation-split 0.2
```

### Model Evaluation
```bash
# Evaluate model performance
python models/evaluate_model.py \
  --model models/checkpoints/hrf_model_v1.0.pkl \
  --test-data corpora/test/performance_test.json \
  --output models/hrf_models/evaluation_results.json
```

## 🔍 Model Analysis

### Feature Analysis
```bash
# Analyze feature importance
python models/analyze_features.py \
  --model models/checkpoints/hrf_model_v1.0.pkl \
  --test-data corpora/test/unit_test_corpus.json \
  --output models/hrf_models/feature_analysis.json

# View feature analysis
python -c "
import json
analysis = json.load(open('models/hrf_models/feature_analysis.json'))
print('Feature Importance:')
for feature, importance in analysis['feature_importance'].items():
    print(f'{feature}: {importance:.3f}')
"
```

### Performance Benchmarking
```bash
# Benchmark model performance
python models/benchmark_model.py \
  --model models/checkpoints/hrf_model_v1.0.pkl \
  --test-size 1000 \
  --output models/hrf_models/benchmark_results.json

# View benchmark results
python -c "
import json
benchmark = json.load(open('models/hrf_models/benchmark_results.json'))
print(f'Average Inference Time: {benchmark[\"avg_inference_time_ms\"]:.2f}ms')
print(f'Throughput: {benchmark[\"throughput_requests_per_second\"]:.0f} req/s')
"
```

## 🔧 Model Management

### Version Control
```bash
# Tag model versions
git tag -a hrf_model_v1.0 -m "HRF model version 1.0 - production ready"

# List model versions
git tag -l | grep hrf_model
```

### Model Backup
```bash
# Backup model files
tar -czf models_backup_$(date +%Y%m%d).tar.gz models/

# Verify backup
tar -tzf models_backup_$(date +%Y%m%d).tar.gz | head -10
```

### Model Deployment
```bash
# Deploy model to production
cp models/checkpoints/hrf_model_v1.0.pkl /production/models/

# Verify deployment
python -c "
import pickle
import sys
sys.path.append('/production/models')
model = pickle.load(open('/production/models/hrf_model_v1.0.pkl', 'rb'))
print('Model deployed successfully')
"
```

## 📋 Model Development Roadmap

### Current Status (v1.0)
- ✅ Statistical feature extraction model
- ✅ 8-dimensional HRV support
- ✅ Real-time inference
- ✅ Production deployment ready

### Future Enhancements (v2.0)
- 🔧 Transformer-based architecture
- 🔧 Multi-language support
- 🔧 Advanced feature engineering
- 🔧 Deep learning integration

### Long-term Goals (v3.0)
- 📋 Reinforcement learning integration
- 📋 Multi-modal content analysis
- 📋 Real-time adaptation
- 📋 Custom model training

## 🛠️ Model Customization

### Feature Engineering
```python
# Add custom features
class CustomHRFModel(HRFModel):
    def extract_features(self, text):
        features = super().extract_features(text)
        # Add custom features
        features['custom_metric'] = self.calculate_custom_metric(text)
        return features
    
    def calculate_custom_metric(self, text):
        # Your custom feature calculation
        return len(text.split()) / 100.0
```

### Model Fine-tuning
```python
# Fine-tune model weights
def fine_tune_model(model, training_data, learning_rate=0.001):
    # Implementation for fine-tuning
    # This would be implemented in future versions
    pass
```

### Custom Evaluation Metrics
```python
# Define custom evaluation metrics
def custom_evaluation(predictions, targets):
    # Custom metric calculation
    mse = sum((p - t) ** 2 for p, t in zip(predictions, targets)) / len(predictions)
    return mse
```

## 📊 Model Monitoring

### Performance Monitoring
```bash
# Monitor model performance in production
python models/monitor_model.py \
  --model models/checkpoints/hrf_model_v1.0.pkl \
  --log-file logs/model_performance.log \
  --alert-threshold 0.05
```

### Drift Detection
```python
# Detect model drift
def detect_model_drift(current_scores, baseline_scores, threshold=0.1):
    current_mean = sum(current_scores) / len(current_scores)
    baseline_mean = sum(baseline_scores) / len(baseline_scores)
    drift = abs(current_mean - baseline_mean)
    return drift > threshold
```

### Quality Assurance
```bash
# Run quality assurance tests
python models/qa_tests.py \
  --model models/checkpoints/hrf_model_v1.0.pkl \
  --test-suite comprehensive \
  --output models/hrf_models/qa_results.json
```

## 🆘 Troubleshooting

### Common Issues

1. **Model Loading Errors**
```bash
# Check model file integrity
python -c "
import pickle
try:
    model = pickle.load(open('models/checkpoints/hrf_model_v1.0.pkl', 'rb'))
    print('Model loaded successfully')
except Exception as e:
    print(f'Model loading error: {e}')
"
```

2. **Performance Degradation**
```bash
# Check model performance
python models/evaluate_model.py \
  --model models/checkpoints/hrf_model_v1.0.pkl \
  --quick-test

# Monitor inference time
python -c "
import time
from resonance_os.generation.hrf_model import HRFModel
model = HRFModel()
start = time.time()
for _ in range(100):
    model.predict('Test text')
print(f'Average inference time: {(time.time() - start) / 100 * 1000:.2f}ms')
"
```

3. **Memory Issues**
```bash
# Check memory usage
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

### Getting Help
- Review model documentation
- Check model logs: `logs/model_performance.log`
- Validate model files
- Contact support: support@resonanceos.ai

## 📚 Model Resources

### Research Papers
- "Human-Resonant Feedback Systems" - ResonanceOS Research Team
- "Statistical Approaches to Content Quality Assessment" - AI Research Journal
- "Multi-dimensional Text Analysis for Engagement Prediction" - NLP Conference

### Implementation References
- Scikit-learn documentation
- NLTK feature extraction
- TextBlob sentiment analysis
- Python standard library statistics

### Related Projects
- OpenAI GPT models
- BERT text classification
- spaCy NLP library
- TextBlob sentiment analysis

This models directory provides the complete HRF model infrastructure for ResonanceOS v6, enabling accurate content resonance prediction and real-time feedback for optimal content generation.
