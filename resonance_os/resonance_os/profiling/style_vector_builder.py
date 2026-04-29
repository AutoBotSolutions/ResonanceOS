"""
Style vector builder for ResonanceOS
"""

import numpy as np
import re
import statistics
from typing import List, Dict, Optional, Tuple
from collections import Counter
import nltk
from textblob import TextBlob
import spacy

from ..core.types import ResonanceVector, TextDocument
from ..core.constants import RESONANCE_DIMENSIONS, FEATURE_WEIGHTS
from ..core.logging import get_logger, log_performance
from ..core.config import get_config

logger = get_logger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')


class StyleVectorBuilder:
    """Builds resonance vectors from text documents"""
    
    def __init__(self, tier: int = 1):
        self.tier = tier
        self.config = get_config()
        self._load_models()
    
    def _load_models(self):
        """Load required models based on tier"""
        
        # Tier 1: Basic models
        self.sentiment_analyzer = None
        
        # Tier 2: spaCy
        if self.tier >= 2:
            try:
                self.nlp = spacy.load(self.config.models.spacy_model)
                logger.info(f"Loaded spaCy model: {self.config.models.spacy_model}")
            except OSError:
                logger.warning(f"spaCy model {self.config.models.spacy_model} not found, using tier 1")
                self.tier = 1
                self.nlp = None
        
        # Tier 3: Transformers (would be implemented separately)
        if self.tier >= 3:
            logger.info("Tier 3: Transformer models would be loaded here")
    
    @log_performance
    def build_vector(self, documents: List[TextDocument]) -> ResonanceVector:
        """Build resonance vector from documents"""
        
        if not documents:
            raise ValueError("No documents provided")
        
        # Extract features for each dimension
        features = {}
        
        # Tier 1: Basic statistical features
        features.update(self._extract_basic_features(documents))
        
        # Tier 2: Advanced linguistic features
        if self.tier >= 2 and hasattr(self, 'nlp') and self.nlp:
            features.update(self._extract_linguistic_features(documents))
        
        # Tier 3: Transformer-based features
        if self.tier >= 3:
            features.update(self._extract_transformer_features(documents))
        
        # Ensure all dimensions are present
        vector_values = []
        for dim in RESONANCE_DIMENSIONS:
            value = features.get(dim, 0.0)
            # Normalize to [0, 1] range
            if dim in ['lexical_density', 'emotional_valence', 'abstraction_level', 'assertiveness_score']:
                value = max(0.0, min(1.0, (value + 1) / 2))  # Convert from [-1, 1] to [0, 1]
            else:
                value = max(0.0, min(1.0, value))
            vector_values.append(value)
        
        # Calculate confidence based on document count and feature coverage
        confidence = self._calculate_confidence(features, len(documents))
        
        return ResonanceVector(
            values=vector_values,
            dimensions=RESONANCE_DIMENSIONS,
            confidence=confidence
        )
    
    def _extract_basic_features(self, documents: List[TextDocument]) -> Dict[str, float]:
        """Extract basic statistical features"""
        
        all_text = " ".join(doc.content for doc in documents)
        words = all_text.split()
        sentences = re.split(r'[.!?]+', all_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        features = {}
        
        # Lexical density
        content_words = [w for w in words if len(w) > 3 and w.isalpha()]
        features['lexical_density'] = len(content_words) / max(len(words), 1)
        
        # Emotional valence
        features['emotional_valence'] = self._analyze_sentiment(all_text)
        
        # Cadence variability
        sentence_lengths = [len(s.split()) for s in sentences]
        features['cadence_variability'] = statistics.stdev(sentence_lengths) / max(statistics.mean(sentence_lengths), 1) if len(sentence_lengths) > 1 else 0.0
        
        # Sentence entropy
        length_distribution = Counter(sentence_lengths)
        total_sentences = len(sentences)
        entropy = -sum((count/total_sentences) * np.log2(count/total_sentences) 
                      for count in length_distribution.values())
        features['sentence_entropy'] = entropy / max(np.log2(len(length_distribution)), 1)
        
        # Metaphor frequency (simplified detection)
        features['metaphor_frequency'] = self._detect_metaphors(all_text)
        
        # Abstraction level
        features['abstraction_level'] = self._analyze_abstraction(all_text)
        
        # Assertiveness score
        features['assertiveness_score'] = self._analyze_assertiveness(all_text)
        
        # Rhythm signature
        features['rhythm_signature'] = self._analyze_rhythm(sentences)
        
        # Narrative intensity curve
        features['narrative_intensity_curve'] = self._analyze_narrative_intensity(sentences)
        
        # Cognitive load index
        features['cognitive_load_index'] = self._analyze_cognitive_load(all_text)
        
        return features
    
    def _extract_linguistic_features(self, documents: List[TextDocument]) -> Dict[str, float]:
        """Extract advanced linguistic features using spaCy"""
        
        if not hasattr(self, 'nlp') or not self.nlp:
            return {}
        
        features = {}
        all_docs = []
        
        for doc in documents:
            try:
                spacy_doc = self.nlp(doc.content)
                all_docs.append(spacy_doc)
            except Exception as e:
                logger.warning(f"spaCy processing failed: {str(e)}")
                continue
        
        if not all_docs:
            return {}
        
        # Enhanced lexical density with POS tagging
        content_pos = {'NOUN', 'VERB', 'ADJ', 'ADV'}
        total_tokens = sum(len(doc) for doc in all_docs)
        content_tokens = sum(len([token for token in doc if token.pos_ in content_pos]) for doc in all_docs)
        features['lexical_density'] = content_tokens / max(total_tokens, 1)
        
        # Enhanced emotional analysis
        features['emotional_valence'] = self._analyze_sentiment_spacy(all_docs)
        
        # Enhanced cadence analysis
        features['cadence_variability'] = self._analyze_cadence_spacy(all_docs)
        
        # Enhanced abstraction analysis
        features['abstraction_level'] = self._analyze_abstraction_spacy(all_docs)
        
        return features
    
    def _extract_transformer_features(self, documents: List[TextDocument]) -> Dict[str, float]:
        """Extract features using transformer models (placeholder)"""
        
        # This would implement transformer-based feature extraction
        # For now, return empty dict as placeholder
        logger.info("Transformer feature extraction not yet implemented")
        return {}
    
    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment using TextBlob"""
        
        try:
            blob = TextBlob(text)
            # Polarity ranges from -1 to 1
            return blob.sentiment.polarity
        except Exception:
            return 0.0
    
    def _analyze_sentiment_spacy(self, spacy_docs) -> float:
        """Enhanced sentiment analysis using spaCy"""
        
        # Simple sentiment based on emotional words
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic'}
        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'disappointing'}
        
        positive_count = 0
        negative_count = 0
        total_words = 0
        
        for doc in spacy_docs:
            for token in doc:
                if token.is_alpha and not token.is_stop:
                    total_words += 1
                    word_lower = token.text.lower()
                    if word_lower in positive_words:
                        positive_count += 1
                    elif word_lower in negative_words:
                        negative_count += 1
        
        if total_words == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / total_words
        return max(-1.0, min(1.0, sentiment))
    
    def _detect_metaphors(self, text: str) -> float:
        """Detect metaphor usage (simplified)"""
        
        # Simple metaphor detection based on common patterns
        metaphor_patterns = [
            r'\b(is|are|was|were)\s+(a|the)\s+\w+\s+of\b',
            r'\blike\s+a\s+\w+\b',
            r'\bas\s+\w+\s+as\b',
            r'\b(time|love|life|death)\s+(is|are)\s+\w+\b'
        ]
        
        metaphor_count = 0
        words = text.split()
        
        for pattern in metaphor_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            metaphor_count += len(matches)
        
        return metaphor_count / max(len(words), 1)
    
    def _analyze_abstraction(self, text: str) -> float:
        """Analyze abstraction level"""
        
        # Simple abstraction analysis based on abstract vs concrete words
        abstract_words = {
            'concept', 'idea', 'theory', 'principle', 'philosophy', 'thought',
            'abstract', 'theoretical', 'conceptual', 'metaphysical', 'ideological'
        }
        
        concrete_words = {
            'table', 'chair', 'house', 'car', 'tree', 'water', 'food', 'book',
            'computer', 'phone', 'door', 'window', 'floor', 'wall', 'street'
        }
        
        words = text.lower().split()
        abstract_count = sum(1 for word in words if word in abstract_words)
        concrete_count = sum(1 for word in words if word in concrete_words)
        
        total_relevant = abstract_count + concrete_count
        if total_relevant == 0:
            return 0.5  # Neutral
        
        return abstract_count / total_relevant
    
    def _analyze_abstraction_spacy(self, spacy_docs) -> float:
        """Enhanced abstraction analysis using spaCy"""
        
        abstract_pos = {'NOUN', 'ADJ'}
        concrete_pos = {'PROPN', 'NUM'}
        
        abstract_count = 0
        concrete_count = 0
        
        for doc in spacy_docs:
            for token in doc:
                if token.pos_ in abstract_pos and not token.is_stop:
                    abstract_count += 1
                elif token.pos_ in concrete_pos:
                    concrete_count += 1
        
        total = abstract_count + concrete_count
        if total == 0:
            return 0.5
        
        return abstract_count / total
    
    def _analyze_assertiveness(self, text: str) -> float:
        """Analyze assertiveness level"""
        
        # Assertiveness indicators
        assertive_words = {
            'must', 'should', 'will', 'definitely', 'certainly', 'absolutely',
            'clearly', 'obviously', 'undoubtedly', 'unquestionably'
        }
        
        hesitant_words = {
            'maybe', 'perhaps', 'might', 'could', 'possibly', 'probably',
            'seems', 'appears', 'suggests', 'indicates'
        }
        
        words = text.lower().split()
        assertive_count = sum(1 for word in words if word in assertive_words)
        hesitant_count = sum(1 for word in words if word in hesitant_words)
        
        total_assertive_words = assertive_count + hesitant_count
        if total_assertive_words == 0:
            return 0.5  # Neutral
        
        return assertive_count / total_assertive_words
    
    def _analyze_rhythm(self, sentences: List[str]) -> float:
        """Analyze sentence rhythm patterns"""
        
        if len(sentences) < 2:
            return 0.5
        
        # Calculate rhythm based on sentence length variation
        lengths = [len(s.split()) for s in sentences]
        
        # Rhythm complexity based on variation patterns
        if len(lengths) < 2:
            return 0.5
        
        # Calculate pattern consistency
        patterns = []
        for i in range(len(lengths) - 1):
            if lengths[i] > 0:
                ratio = lengths[i + 1] / lengths[i]
                patterns.append(ratio)
        
        if not patterns:
            return 0.5
        
        # More consistent patterns = lower rhythm score
        pattern_variance = statistics.variance(patterns)
        rhythm_score = 1.0 / (1.0 + pattern_variance)
        
        return max(0.0, min(1.0, rhythm_score))
    
    def _analyze_cadence_spacy(self, spacy_docs) -> float:
        """Enhanced cadence analysis using spaCy"""
        
        sentence_lengths = []
        
        for doc in spacy_docs:
            for sent in doc.sents:
                sentence_lengths.append(len(sent))
        
        if len(sentence_lengths) < 2:
            return 0.5
        
        mean_length = statistics.mean(sentence_lengths)
        if mean_length == 0:
            return 0.5
        
        # Cadence variability based on sentence length variation
        std_dev = statistics.stdev(sentence_lengths)
        variability = std_dev / mean_length
        
        return max(0.0, min(1.0, variability))
    
    def _analyze_narrative_intensity(self, sentences: List[str]) -> float:
        """Analyze narrative intensity curve"""
        
        if len(sentences) < 3:
            return 0.5
        
        # Simple intensity based on sentence length and punctuation
        intensities = []
        
        for sentence in sentences:
            # Base intensity from length
            length_intensity = len(sentence.split()) / 20.0  # Normalize by expected length
            
            # Boost from exclamation marks and question marks
            punctuation_boost = sentence.count('!') * 0.2 + sentence.count('?') * 0.1
            
            # Overall intensity
            intensity = min(1.0, length_intensity + punctuation_boost)
            intensities.append(intensity)
        
        # Calculate curve complexity (variation in intensity)
        if len(intensities) < 2:
            return 0.5
        
        intensity_variance = statistics.variance(intensities)
        curve_complexity = intensity_variance
        
        return max(0.0, min(1.0, curve_complexity))
    
    def _analyze_cognitive_load(self, text: str) -> float:
        """Analyze cognitive load index"""
        
        # Cognitive load indicators
        long_words = len([w for w in text.split() if len(w) > 6])
        complex_punctuation = text.count(';') + text.count(':') + text.count('—')
        subordinate_clauses = len(re.findall(r'\b(although|because|since|while|whereas|if|unless|when)\b', text, re.IGNORECASE))
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.5
        
        # Cognitive load score
        load_score = (long_words + complex_punctuation * 2 + subordinate_clauses * 3) / total_words
        
        return max(0.0, min(1.0, load_score * 10))  # Scale to [0, 1]
    
    def _calculate_confidence(self, features: Dict[str, float], document_count: int) -> float:
        """Calculate confidence score for the vector"""
        
        # Base confidence from document count
        count_confidence = min(1.0, document_count / 10.0)  # 10 docs = full confidence
        
        # Feature coverage confidence
        feature_count = len([v for v in features.values() if v is not None])
        max_features = len(RESONANCE_DIMENSIONS)
        coverage_confidence = feature_count / max_features
        
        # Combined confidence
        overall_confidence = (count_confidence + coverage_confidence) / 2.0
        
        return max(0.1, min(1.0, overall_confidence))
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance weights"""
        return FEATURE_WEIGHTS.copy()
    
    def set_tier(self, tier: int):
        """Change analysis tier"""
        if tier != self.tier:
            self.tier = tier
            self._load_models()
            logger.info(f"Changed to tier {tier} analysis")
