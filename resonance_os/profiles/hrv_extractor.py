import math
from typing import List

class HRVExtractor:
    def extract(self, text: str) -> List[float]:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        words = text.split()
        
        # Basic metrics without external dependencies
        if not sentences:
            sentences = [text]
        
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_len = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        # Calculate variance
        if len(sentence_lengths) > 1:
            mean = avg_len
            variance = sum((x - mean) ** 2 for x in sentence_lengths) / len(sentence_lengths)
        else:
            variance = 0
        
        # Lexical diversity
        lexical_diversity = len(set(words)) / max(len(words), 1)
        
        # Simple sentiment approximation (based on positive/negative words)
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'best', 'awesome'}
        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'worst', 'disgusting', 'poor', 'fail'}
        
        pos_count = sum(1 for word in words if word.lower() in positive_words)
        neg_count = sum(1 for word in words if word.lower() in negative_words)
        sentiment = (pos_count - neg_count) / max(len(words), 1)
        
        # HRV vector construction
        return [
            variance / 10.0,           # sentence_variance (normalized)
            max(-1.0, min(1.0, sentiment * 10)),  # emotional_valence
            abs(sentiment * 10),       # emotional_intensity
            0.5,                       # assertiveness_index (placeholder)
            0.5,                       # curiosity_index (placeholder)
            0.1,                       # metaphor_density (placeholder)
            0.2,                       # storytelling_index (placeholder)
            0.7                        # active_voice_ratio (placeholder)
        ]
