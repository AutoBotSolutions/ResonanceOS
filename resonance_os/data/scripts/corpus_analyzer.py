#!/usr/bin/env python3
"""
Corpus Analyzer for ResonanceOS v6

This script analyzes text corpora to extract insights, patterns, and
recommendations for HRV profile creation and content generation.
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import argparse
from collections import Counter, defaultdict
import math

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.profiles.hrv_extractor import HRVExtractor


class CorpusAnalyzer:
    """Advanced corpus analysis utility"""
    
    def __init__(self):
        """Initialize the corpus analyzer"""
        self.hrv_extractor = HRVExtractor()
        
        # Sentiment word lists (simplified)
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 
            'love', 'like', 'best', 'awesome', 'brilliant', 'outstanding',
            'superb', 'magnificent', 'marvelous', 'terrific', 'splendid'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 
            'worst', 'disgusting', 'poor', 'fail', 'dreadful', 'appalling',
            'atrocious', 'dismal', 'deplorable', 'lousy', 'abysmal'
        }
        
        # Assertiveness indicators
        self.assertive_words = {
            'must', 'should', 'will', 'definitely', 'certainly', 'absolutely',
            'undoubtedly', 'clearly', 'obviously', 'without', 'doubt'
        }
        
        # Curiosity indicators
        self.curiosity_words = {
            'what', 'how', 'why', 'when', 'where', 'who', 'which',
            'interesting', 'fascinating', 'curious', 'wonder', 'discover',
            'explore', 'investigate', 'question', 'mystery'
        }
        
        # Storytelling indicators
        self.storytelling_words = {
            'once', 'story', 'tale', 'narrative', 'journey', 'adventure',
            'character', 'plot', 'setting', 'scene', 'chapter', 'beginning',
            'ending', 'climax', 'twist', 'surprise'
        }
        
        # Metaphor indicators
        self.metaphor_patterns = [
            'like a', 'as if', 'similar to', 'represents', 'symbolizes',
            'metaphor', 'analogy', 'compared to', 'resembles'
        ]
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Comprehensive analysis of a single text"""
        # Basic statistics
        words = text.split()
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # HRV analysis
        hrv_vector = self.hrv_extractor.extract(text)
        
        # Advanced linguistic analysis
        linguistic_features = self._extract_linguistic_features(text)
        
        # Readability metrics
        readability = self._calculate_readability(text)
        
        # Content classification
        content_type = self._classify_content(text)
        
        return {
            'basic_stats': {
                'word_count': len(words),
                'sentence_count': len(sentences),
                'avg_sentence_length': sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0,
                'unique_words': len(set(words)),
                'lexical_diversity': len(set(words)) / len(words) if words else 0
            },
            'hrv_vector': hrv_vector,
            'linguistic_features': linguistic_features,
            'readability': readability,
            'content_classification': content_type
        }
    
    def _extract_linguistic_features(self, text: str) -> Dict[str, Any]:
        """Extract detailed linguistic features"""
        words = text.lower().split()
        word_count = len(words)
        
        if word_count == 0:
            return {}
        
        # Sentiment analysis
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        sentiment_ratio = (pos_count - neg_count) / word_count
        
        # Assertiveness analysis
        assertive_count = sum(1 for w in words if w in self.assertive_words)
        assertiveness_ratio = assertive_count / word_count
        
        # Curiosity analysis
        curiosity_count = sum(1 for w in words if w in self.curiosity_words)
        curiosity_ratio = curiosity_count / word_count
        
        # Storytelling analysis
        storytelling_count = sum(1 for w in words if w in self.storytelling_words)
        storytelling_ratio = storytelling_count / word_count
        
        # Metaphor analysis
        text_lower = text.lower()
        metaphor_count = sum(1 for pattern in self.metaphor_patterns if pattern in text_lower)
        metaphor_ratio = metaphor_count / word_count
        
        # Active voice estimation (simplified)
        passive_indicators = ['was', 'were', 'been', 'being', 'by']
        passive_count = sum(1 for w in words if w in passive_indicators)
        active_voice_ratio = 1.0 - (passive_count / word_count)
        
        return {
            'sentiment_ratio': sentiment_ratio,
            'assertiveness_ratio': assertiveness_ratio,
            'curiosity_ratio': curiosity_ratio,
            'storytelling_ratio': storytelling_ratio,
            'metaphor_ratio': metaphor_ratio,
            'active_voice_ratio': max(0.0, active_voice_ratio)
        }
    
    def _calculate_readability(self, text: str) -> Dict[str, Any]:
        """Calculate readability metrics"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        words = text.split()
        
        if not sentences or not words:
            return {}
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Average word length
        avg_word_length = sum(len(w) for w in words) / len(words)
        
        # Simplified Flesch Reading Ease
        if avg_sentence_length > 0:
            flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_word_length)
        else:
            flesch_score = 0
        
        # Reading level classification
        if flesch_score >= 90:
            reading_level = "Very Easy"
        elif flesch_score >= 80:
            reading_level = "Easy"
        elif flesch_score >= 70:
            reading_level = "Fairly Easy"
        elif flesch_score >= 60:
            reading_level = "Standard"
        elif flesch_score >= 50:
            reading_level = "Fairly Difficult"
        elif flesch_score >= 30:
            reading_level = "Difficult"
        else:
            reading_level = "Very Difficult"
        
        return {
            'avg_sentence_length': avg_sentence_length,
            'avg_word_length': avg_word_length,
            'flesch_score': max(0, min(100, flesch_score)),
            'reading_level': reading_level
        }
    
    def _classify_content(self, text: str) -> Dict[str, Any]:
        """Classify content type and style"""
        text_lower = text.lower()
        
        # Content type indicators
        business_indicators = ['revenue', 'profit', 'market', 'business', 'financial', 'strategy']
        technical_indicators = ['algorithm', 'system', 'technical', 'data', 'analysis', 'method']
        creative_indicators = ['story', 'imagine', 'creative', 'art', 'beautiful', 'inspire']
        academic_indicators = ['research', 'study', 'analysis', 'methodology', 'theory', 'hypothesis']
        
        scores = {}
        for category, indicators in [
            ('business', business_indicators),
            ('technical', technical_indicators),
            ('creative', creative_indicators),
            ('academic', academic_indicators)
        ]:
            score = sum(1 for indicator in indicators if indicator in text_lower)
            scores[category] = score / len(indicators)
        
        # Determine primary type
        primary_type = max(scores, key=scores.get)
        
        # Formality level
        formal_indicators = ['therefore', 'furthermore', 'consequently', 'however', 'moreover']
        informal_indicators = ['hey', 'yeah', 'cool', 'awesome', 'totally']
        
        formal_score = sum(1 for indicator in formal_indicators if indicator in text_lower)
        informal_score = sum(1 for indicator in informal_indicators if indicator in text_lower)
        
        if formal_score > informal_score:
            formality = "formal"
        elif informal_score > formal_score * 2:
            formality = "informal"
        else:
            formality = "neutral"
        
        return {
            'type_scores': scores,
            'primary_type': primary_type,
            'formality': formality
        }
    
    def analyze_corpus(self, directory: str, pattern: str = "*.txt") -> Dict[str, Any]:
        """Analyze entire corpus directory"""
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        # Analyze all files
        file_analyses = []
        for file_path in directory_path.glob(pattern):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                analysis = self.analyze_text(content)
                analysis['file_path'] = str(file_path)
                file_analyses.append(analysis)
            except Exception as e:
                file_analyses.append({
                    'file_path': str(file_path),
                    'error': str(e)
                })
        
        # Aggregate statistics
        valid_analyses = [a for a in file_analyses if 'error' not in a]
        
        if not valid_analyses:
            return {'error': 'No valid files to analyze'}
        
        # Calculate corpus-level metrics
        corpus_stats = self._calculate_corpus_stats(valid_analyses)
        
        # HRV analysis
        hrv_analysis = self._analyze_corpus_hrv(valid_analyses)
        
        # Content type distribution
        content_distribution = self._analyze_content_distribution(valid_analyses)
        
        # Recommendations
        recommendations = self._generate_recommendations(valid_analyses)
        
        return {
            'file_count': len(file_analyses),
            'valid_files': len(valid_analyses),
            'corpus_stats': corpus_stats,
            'hrv_analysis': hrv_analysis,
            'content_distribution': content_distribution,
            'recommendations': recommendations,
            'file_analyses': file_analyses
        }
    
    def _calculate_corpus_stats(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate corpus-level statistics"""
        total_words = sum(a['basic_stats']['word_count'] for a in analyses)
        total_sentences = sum(a['basic_stats']['sentence_count'] for a in analyses)
        
        avg_word_count = total_words / len(analyses)
        avg_sentence_count = total_sentences / len(analyses)
        
        # Readability distribution
        reading_levels = Counter(a['readability']['reading_level'] for a in analyses)
        
        # Content type distribution
        content_types = Counter(a['content_classification']['primary_type'] for a in analyses)
        
        # Formality distribution
        formality_levels = Counter(a['content_classification']['formality'] for a in analyses)
        
        return {
            'total_words': total_words,
            'total_sentences': total_sentences,
            'avg_words_per_document': avg_word_count,
            'avg_sentences_per_document': avg_sentence_count,
            'reading_level_distribution': dict(reading_levels),
            'content_type_distribution': dict(content_types),
            'formality_distribution': dict(formality_levels)
        }
    
    def _analyze_corpus_hrv(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze HRV patterns across corpus"""
        hrv_vectors = [a['hrv_vector'] for a in analyses]
        
        # Calculate statistics for each dimension
        dimension_stats = {}
        for i, dimension in enumerate(['sentence_variance', 'emotional_valence', 'emotional_intensity', 
                                     'assertiveness_index', 'curiosity_index', 'metaphor_density', 
                                     'storytelling_index', 'active_voice_ratio']):
            values = [v[i] for v in hrv_vectors]
            dimension_stats[dimension] = {
                'mean': sum(values) / len(values),
                'min': min(values),
                'max': max(values),
                'std': math.sqrt(sum((x - sum(values)/len(values))**2 for x in values) / len(values)),
                'range': max(values) - min(values)
            }
        
        # Identify outliers and patterns
        outliers = self._identify_hrv_outliers(hrv_vectors)
        patterns = self._identify_hrv_patterns(hrv_vectors)
        
        return {
            'dimension_statistics': dimension_stats,
            'outliers': outliers,
            'patterns': patterns,
            'diversity_score': self._calculate_hrv_diversity(hrv_vectors)
        }
    
    def _identify_hrv_outliers(self, hrv_vectors: List[List[float]]) -> List[Dict[str, Any]]:
        """Identify HRV outliers in the corpus"""
        outliers = []
        
        for i, vector in enumerate(hrv_vectors):
            # Calculate distance from mean
            mean_vector = [sum(dim[i] for dim in hrv_vectors) / len(hrv_vectors) for i in range(8)]
            distance = sum(abs(v - m) for v, m in zip(vector, mean_vector))
            
            # Mark as outlier if distance is high
            if distance > 2.0:  # Threshold can be adjusted
                outliers.append({
                    'index': i,
                    'distance_from_mean': distance,
                    'vector': vector
                })
        
        return outliers
    
    def _identify_hrv_patterns(self, hrv_vectors: List[List[float]]) -> List[str]:
        """Identify common patterns in HRV vectors"""
        patterns = []
        
        # Check for clustering
        if self._has_clustering(hrv_vectors):
            patterns.append("HRV vectors show clustering patterns")
        
        # Check for high variance in specific dimensions
        for i, dimension in enumerate(['sentence_variance', 'emotional_valence', 'emotional_intensity', 
                                     'assertiveness_index', 'curiosity_index', 'metaphor_density', 
                                     'storytelling_index', 'active_voice_ratio']):
            values = [v[i] for v in hrv_vectors]
            if max(values) - min(values) > 0.8:
                patterns.append(f"High variance in {dimension}")
        
        # Check for uniform vectors
        uniform_vectors = sum(1 for v in hrv_vectors if max(v) - min(v) < 0.1)
        if uniform_vectors > len(hrv_vectors) * 0.3:
            patterns.append("Many uniform HRV vectors detected")
        
        return patterns
    
    def _has_clustering(self, hrv_vectors: List[List[float]]) -> bool:
        """Simple clustering detection"""
        if len(hrv_vectors) < 3:
            return False
        
        # Calculate pairwise distances
        distances = []
        for i in range(len(hrv_vectors)):
            for j in range(i + 1, len(hrv_vectors)):
                distance = sum(abs(a - b) for a, b in zip(hrv_vectors[i], hrv_vectors[j]))
                distances.append(distance)
        
        # If most distances are small, there's clustering
        avg_distance = sum(distances) / len(distances)
        return avg_distance < 1.0
    
    def _calculate_hrv_diversity(self, hrv_vectors: List[List[float]]) -> float:
        """Calculate HRV diversity score"""
        if len(hrv_vectors) < 2:
            return 0.0
        
        # Calculate average pairwise distance
        total_distance = 0
        count = 0
        
        for i in range(len(hrv_vectors)):
            for j in range(i + 1, len(hrv_vectors)):
                distance = sum(abs(a - b) for a, b in zip(hrv_vectors[i], hrv_vectors[j]))
                total_distance += distance
                count += 1
        
        avg_distance = total_distance / count
        return min(avg_distance / 4.0, 1.0)  # Normalize to 0-1
    
    def _analyze_content_distribution(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content type and style distribution"""
        content_types = Counter(a['content_classification']['primary_type'] for a in analyses)
        formality_levels = Counter(a['content_classification']['formality'] for a in analyses)
        reading_levels = Counter(a['readability']['reading_level'] for a in analyses)
        
        return {
            'content_types': dict(content_types),
            'formality_levels': dict(formality_levels),
            'reading_levels': dict(reading_levels),
            'dominant_style': {
                'content_type': content_types.most_common(1)[0][0] if content_types else None,
                'formality': formality_levels.most_common(1)[0][0] if formality_levels else None,
                'reading_level': reading_levels.most_common(1)[0][0] if reading_levels else None
            }
        }
    
    def _generate_recommendations(self, analyses: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on corpus analysis"""
        recommendations = []
        
        # HRV-based recommendations
        hrv_vectors = [a['hrv_vector'] for a in analyses]
        avg_hrv = [sum(dim[i] for dim in hrv_vectors) / len(hrv_vectors) for i in range(8)]
        
        # Check for low emotional valence
        if avg_hrv[1] < -0.2:
            recommendations.append("Consider adding more positive language to improve emotional valence")
        
        # Check for low assertiveness
        if avg_hrv[3] < 0.3:
            recommendations.append("Consider using more assertive language to strengthen messaging")
        
        # Check for low curiosity
        if avg_hrv[4] < 0.3:
            recommendations.append("Consider adding questions and curiosity-inducing elements")
        
        # Check for low storytelling
        if avg_hrv[6] < 0.3:
            recommendations.append("Consider incorporating more storytelling elements")
        
        # Readability recommendations
        avg_flesch = sum(a['readability']['flesch_score'] for a in analyses) / len(analyses)
        if avg_flesch < 60:
            recommendations.append("Consider simplifying language to improve readability")
        elif avg_flesch > 80:
            recommendations.append("Consider adding more complex content for variety")
        
        # Content diversity recommendations
        content_types = Counter(a['content_classification']['primary_type'] for a in analyses)
        if len(content_types) == 1:
            recommendations.append("Consider diversifying content types for broader appeal")
        
        # Sentence length recommendations
        avg_sentence_length = sum(a['basic_stats']['avg_sentence_length'] for a in analyses) / len(analyses)
        if avg_sentence_length > 25:
            recommendations.append("Consider using shorter sentences for better readability")
        elif avg_sentence_length < 10:
            recommendations.append("Consider using longer, more complex sentences for variety")
        
        return recommendations


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='ResonanceOS Corpus Analyzer')
    parser.add_argument('command', choices=['analyze', 'single'], help='Command to execute')
    parser.add_argument('--input', required=True, help='Input file or directory')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--pattern', default='*.txt', help='File pattern for directory analysis')
    
    args = parser.parse_args()
    
    analyzer = CorpusAnalyzer()
    
    try:
        if args.command == 'analyze':
            result = analyzer.analyze_corpus(args.input, args.pattern)
        elif args.command == 'single':
            with open(args.input, 'r', encoding='utf-8') as f:
                content = f.read()
            result = analyzer.analyze_text(content)
            result['file_path'] = args.input
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Analysis results saved to {args.output}")
        else:
            print(json.dumps(result, indent=2))
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
