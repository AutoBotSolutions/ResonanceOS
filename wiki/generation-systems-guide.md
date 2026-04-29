# Generation Systems Guide - ResonanceOS v6

## Overview

The Generation Systems module is the core content synthesis engine of ResonanceOS v6. It orchestrates a multi-layered generation pipeline that produces human-resonant text through coordinated interaction between planning, sentence generation, refinement, and feedback mechanisms.

## System Architecture

The generation pipeline follows a hierarchical architecture:

```
HumanResonantWriter (Orchestrator)
├── PlannerLayer (Structural Planning)
├── SentenceLayer (Sentence Generation)
├── RefinerLayer (Content Refinement)
└── HRFModel (Human Resonance Feedback)
```

## System Components

### 1. HumanResonantWriter (`human_resonant_writer.py`)

The main orchestrator that coordinates all generation layers into a cohesive pipeline.

#### Architecture

```python
class HumanResonantWriter:
    def __init__(self):
        self.planner = PlannerLayer()          # Structural planning
        self.sentence_layer = SentenceLayer()   # Sentence generation
        self.refiner = RefinerLayer()          # Content refinement
        self.hrf = HRFModel()                   # Feedback prediction
```

#### Generation Pipeline

1. **Input**: Prompt (text description)
2. **Planning**: Generate paragraph outlines and target HRV vectors
3. **Generation**: Create sentences constrained by target HRV
4. **Feedback**: Predict human resonance for each sentence
5. **Refinement**: Adjust sentences based on feedback
6. **Output**: Complete article with HRV optimization

#### Usage Example

```python
from resonance_os.generation.human_resonant_writer import HumanResonantWriter

writer = HumanResonantWriter()
article = writer.generate("The future of artificial intelligence in business")
print(article)
```

#### Key Features

- **Multi-layer generation**: Separate planning, generation, and refinement stages
- **Real-time feedback**: HRF predictions guide content optimization
- **HRV-aware generation**: All stages consider target HRV vectors
- **Modular design**: Each layer can be customized independently

### 2. PlannerLayer (`planner_layer.py`)

Handles high-level structural planning for content generation.

#### Responsibilities

- Generate paragraph-level outlines from prompts
- Assign target HRV vectors to each paragraph
- Determine content structure and flow

#### Method Signature

```python
def plan_paragraphs(self, prompt: str, num_paragraphs=3) -> Tuple[List[str], List[List[float]]]:
    """
    Generate paragraph outlines and target HRV vectors.
    
    Args:
        prompt: Input prompt describing desired content
        num_paragraphs: Number of paragraphs to plan (default: 3)
    
    Returns:
        Tuple of (paragraph_outlines, target_hrv_vectors)
    """
```

#### Output Structure

- **Paragraph Outlines**: List of paragraph descriptions
- **Target HRVs**: List of 8-dimensional HRV vectors, one per paragraph

#### Usage Example

```python
from resonance_os.generation.planner_layer import PlannerLayer

planner = PlannerLayer()
paragraphs, target_hrvs = planner.plan_paragraphs("Climate change solutions", num_paragraphs=5)
print(f"Planned {len(paragraphs)} paragraphs with target HRVs")
```

#### Planning Strategy

- Analyze prompt to extract key themes
- Determine optimal paragraph count based on content complexity
- Assign HRV vectors that create coherent narrative flow
- Balance variation and consistency across paragraphs

### 3. SentenceLayer (`sentence_layer.py`)

Generates individual sentences constrained by target HRV vectors.

#### Responsibilities

- Convert paragraph outlines into sentences
- Enforce HRV constraints during generation
- Maintain linguistic quality and coherence

#### Method Signature

```python
def generate_sentences(self, outline: str, target_hrv: List[float]) -> List[str]:
    """
    Generate sentences constrained by target HRV vector.
    
    Args:
        outline: Paragraph outline to expand
        target_hrv: 8-dimensional target HRV vector
    
    Returns:
        List of generated sentences
    """
```

#### Generation Constraints

- **Emotional valence**: Match target sentiment
- **Sentence variance**: Control rhythm and cadence
- **Metaphor density**: Adjust figurative language usage
- **Active voice ratio**: Control sentence construction

#### Usage Example

```python
from resonance_os.generation.sentence_layer import SentenceLayer

sentence_layer = SentenceLayer()
sentences = sentence_layer.generate_sentences(
    outline="Introduction to renewable energy",
    target_hrv=[0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
)
for sentence in sentences:
    print(sentence)
```

### 4. RefinerLayer (`refiner_layer.py`)

Refines generated sentences based on HRF feedback to improve human resonance.

#### Responsibilities

- Analyze HRF feedback for each sentence
- Adjust sentence structure and vocabulary
- Optimize for better HRV alignment

#### Method Signature

```python
def refine(self, sentence: str, hrv_feedback: float) -> str:
    """
    Adjust sentence to improve HRV resonance.
    
    Args:
        sentence: Original generated sentence
        hrv_feedback: Predicted human resonance score (0.0 - 1.0)
    
    Returns:
        Refined sentence with improved resonance
    """
```

#### Refinement Strategies

- **Low feedback**: Increase emotional intensity, add metaphors
- **High feedback**: Maintain current structure, fine-tune details
- **Specific dimensions**: Adjust based on which HRV dimensions need improvement

#### Usage Example

```python
from resonance_os.generation.refiner_layer import RefinerLayer

refiner = RefinerLayer()
original = "The technology is good."
feedback = 0.6  # Moderate resonance
refined = refiner.refine(original, feedback)
print(f"Original: {original}")
print(f"Refined: {refined}")
```

### 5. HRFModel (`hrf_model.py`)

Human-Resonant Feedback model that predicts engagement and emotional response.

#### Purpose

- Predict human resonance scores for generated text
- Guide refinement decisions
- Provide real-time quality assessment

#### Method Signature

```python
def predict(self, text: str) -> float:
    """
    Predict human resonance score for text.
    
    Args:
        text: Text to evaluate
    
    Returns:
        Resonance score between 0.0 and 1.0
        Higher scores indicate better human resonance
    """
```

#### Prediction Factors

- **Emotional alignment**: Match between content and intended tone
- **Engagement quality**: Interest and attention capture
- **Linguistic quality**: Grammar, vocabulary, coherence
- **HRV consistency**: Alignment with target HRV vector

#### Usage Example

```python
from resonance_os.generation.hrf_model import HRFModel

hrf = HRFModel()
text = "The innovative technology transforms how we approach sustainable energy solutions."
score = hrf.predict(text)
print(f"Resonance score: {score:.2f}")
```

#### Model Architecture

Current implementation uses a placeholder random predictor. Production deployment requires:

- Training on engagement data
- Integration with ML frameworks (TensorFlow/PyTorch)
- Feature extraction from text
- Multi-dimensional output (per-dimension feedback)

## Integration Points

The Generation Systems module integrates with:

- **Profile Systems**: Uses target HRV profiles from profile manager
- **Core Systems**: Uses HRV dimension definitions and types
- **Similarity Systems**: Measures similarity between generated and target HRV
- **API Systems**: Exposed through generation endpoints
- **CLI Systems**: Used by command-line interface

## Usage Patterns

### Basic Generation

```python
from resonance_os.generation.human_resonant_writer import HumanResonantWriter

writer = HumanResonantWriter()
article = writer.generate("Write about machine learning applications")
```

### Profile-Based Generation

```python
from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager

writer = HumanResonantWriter()
profile_manager = HRVProfileManager(path="profiles/hr_profiles")
profile = profile_manager.load_profile("default", "professional")

# Use profile HRV for generation
# (Implementation depends on profile integration)
```

### Custom Pipeline

```python
from resonance_os.generation.planner_layer import PlannerLayer
from resonance_os.generation.sentence_layer import SentenceLayer
from resonance_os.generation.refiner_layer import RefinerLayer
from resonance_os.generation.hrf_model import HRFModel

planner = PlannerLayer()
sentence_layer = SentenceLayer()
refiner = RefinerLayer()
hrf = HRFModel()

paragraphs, target_hrvs = planner.plan_paragraphs("Custom prompt", num_paragraphs=4)
for outline, target_hrv in zip(paragraphs, target_hrvs):
    sentences = sentence_layer.generate_sentences(outline, target_hrv)
    for sentence in sentences:
        feedback = hrf.predict(sentence)
        refined = refiner.refine(sentence, feedback)
        print(refined)
```

## Performance Considerations

- **PlannerLayer**: Fast, minimal computation
- **SentenceLayer**: Moderate, depends on sentence complexity
- **RefinerLayer**: Fast, simple transformations
- **HRFModel**: Current placeholder is fast; ML model will be slower

## Best Practices

1. **Always validate HRV vectors** before passing to generation layers
2. **Use appropriate paragraph counts** for content complexity
3. **Monitor HRF feedback** to identify generation quality issues
4. **Profile generation performance** to identify bottlenecks
5. **Cache HRF predictions** when using same text multiple times

## Common Issues

**Issue**: Generated content doesn't match intended tone
**Solution**: Verify target HRV vectors align with desired characteristics

**Issue**: Slow generation speed
**Solution**: Reduce paragraph count or optimize HRF model

**Issue**: Poor refinement quality
**Solution**: Adjust refinement thresholds or improve HRF model

**Issue**: Inconsistent paragraph flow
**Solution**: Improve planner layer to better maintain narrative coherence

## Future Enhancements

- **Advanced planning**: Incorporate content analysis for better structure
- **Context-aware generation**: Use previous content to maintain coherence
- **Multi-modal generation**: Support for images, diagrams, etc.
- **Real-time adaptation**: Adjust generation based on user feedback
- **Style transfer**: Match specific writing styles automatically

## Troubleshooting

**Issue**: Type errors when using generation layers
**Solution**: Ensure proper type annotations and HRV vector format

**Issue**: Memory errors with long content
**Solution**: Process in chunks or increase memory allocation

**Issue**: Poor quality generated content
**Solution**: Train HRF model on relevant engagement data

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [Similarity Systems Guide](./similarity-systems-guide.md)
- [API Systems Guide](./api-systems-guide.md)
