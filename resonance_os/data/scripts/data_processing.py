#!/usr/bin/env python3
"""
Data Processing Utilities for ResonanceOS v6

This script provides utilities for processing text corpora, extracting HRV features,
and preparing data for training and analysis.
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager


class DataProcessor:
    """Main data processing class for ResonanceOS"""
    
    def __init__(self, config_path: str = None):
        """Initialize the data processor"""
        self.hrv_extractor = HRVExtractor()
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from file"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def process_text_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single text file and extract HRV features"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract HRV features
            hrv_vector = self.hrv_extractor.extract(content)
            
            # Get basic statistics
            words = content.split()
            sentences = [s.strip() for s in content.split('.') if s.strip()]
            
            return {
                'file_path': str(file_path),
                'word_count': len(words),
                'sentence_count': len(sentences),
                'avg_sentence_length': sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0,
                'hrv_vector': hrv_vector,
                'content_preview': content[:200] + "..." if len(content) > 200 else content
            }
        except Exception as e:
            return {'file_path': str(file_path), 'error': str(e)}
    
    def process_directory(self, directory: str, pattern: str = "*.txt") -> List[Dict[str, Any]]:
        """Process all text files in a directory"""
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        results = []
        for file_path in directory_path.glob(pattern):
            result = self.process_text_file(file_path)
            results.append(result)
        
        return results
    
    def create_corpus_profile(self, results: List[Dict[str, Any]], profile_name: str) -> Dict[str, Any]:
        """Create an HRV profile from corpus analysis results"""
        valid_results = [r for r in results if 'hrv_vector' in r and 'error' not in r]
        
        if not valid_results:
            raise ValueError("No valid results to create profile")
        
        # Calculate average HRV vector
        hrv_vectors = [r['hrv_vector'] for r in valid_results]
        avg_hrv = [sum(dim[i] for dim in hrv_vectors) / len(hrv_vectors) for i in range(8)]
        
        # Calculate corpus statistics
        total_words = sum(r['word_count'] for r in valid_results)
        total_sentences = sum(r['sentence_count'] for r in valid_results)
        avg_sentence_length = sum(r['avg_sentence_length'] for r in valid_results) / len(valid_results)
        
        return {
            'name': profile_name,
            'description': f'Profile generated from {len(valid_results)} documents',
            'hrv_vector': avg_hrv,
            'metadata': {
                'source_documents': len(valid_results),
                'total_words': total_words,
                'total_sentences': total_sentences,
                'avg_sentence_length': avg_sentence_length,
                'created_at': '2026-03-09T00:00:00Z',
                'version': '1.0',
                'corpus_type': 'generated'
            }
        }
    
    def export_results(self, results: List[Dict[str, Any]], output_path: str, format: str = 'json'):
        """Export processing results"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if format.lower() == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        elif format.lower() == 'csv':
            import csv
            if results:
                fieldnames = set()
                for result in results:
                    fieldnames.update(result.keys())
                
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=list(fieldnames))
                    writer.writeheader()
                    for result in results:
                        # Flatten HRV vector for CSV
                        flattened = result.copy()
                        if 'hrv_vector' in flattened:
                            for i, value in enumerate(flattened['hrv_vector']):
                                flattened[f'hrv_dim_{i}'] = value
                            del flattened['hrv_vector']
                        writer.writerow(flattened)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def analyze_corpus_quality(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze corpus quality and provide insights"""
        valid_results = [r for r in results if 'hrv_vector' in r and 'error' not in r]
        
        if not valid_results:
            return {'error': 'No valid results to analyze'}
        
        # HRV statistics
        hrv_vectors = [r['hrv_vector'] for r in valid_results]
        hrv_stats = {}
        for i in range(8):
            values = [dim[i] for dim in hrv_vectors]
            hrv_stats[f'dimension_{i}'] = {
                'mean': sum(values) / len(values),
                'min': min(values),
                'max': max(values),
                'std': (sum((x - sum(values)/len(values))**2 for x in values) / len(values))**0.5
            }
        
        # Document statistics
        word_counts = [r['word_count'] for r in valid_results]
        sentence_counts = [r['sentence_count'] for r in valid_results]
        
        return {
            'document_count': len(valid_results),
            'total_words': sum(word_counts),
            'total_sentences': sum(sentence_counts),
            'avg_words_per_document': sum(word_counts) / len(word_counts),
            'avg_sentences_per_document': sum(sentence_counts) / len(sentence_counts),
            'hrv_statistics': hrv_stats,
            'quality_score': self._calculate_quality_score(valid_results)
        }
    
    def _calculate_quality_score(self, results: List[Dict[str, Any]]) -> float:
        """Calculate overall corpus quality score"""
        if not results:
            return 0.0
        
        # Factors for quality score
        avg_word_count = sum(r['word_count'] for r in results) / len(results)
        avg_sentence_count = sum(r['sentence_count'] for r in results) / len(results)
        
        # Score based on document length and variety
        length_score = min(avg_word_count / 500, 1.0)  # Ideal around 500 words
        sentence_score = min(avg_sentence_count / 20, 1.0)  # Ideal around 20 sentences
        
        # HRV variety score
        hrv_vectors = [r['hrv_vector'] for r in results]
        variety_score = self._calculate_hrv_variety(hrv_vectors)
        
        return (length_score + sentence_score + variety_score) / 3
    
    def _calculate_hrv_variety(self, hrv_vectors: List[List[float]]) -> float:
        """Calculate HRV variety score"""
        if len(hrv_vectors) < 2:
            return 0.0
        
        # Calculate average pairwise distance
        distances = []
        for i in range(len(hrv_vectors)):
            for j in range(i + 1, len(hrv_vectors)):
                distance = sum(abs(a - b) for a, b in zip(hrv_vectors[i], hrv_vectors[j]))
                distances.append(distance)
        
        avg_distance = sum(distances) / len(distances)
        return min(avg_distance / 4.0, 1.0)  # Normalize to 0-1


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='ResonanceOS Data Processing Utility')
    parser.add_argument('command', choices=['process', 'analyze', 'profile'], help='Command to execute')
    parser.add_argument('--input', required=True, help='Input file or directory')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Output format')
    parser.add_argument('--profile-name', help='Name for generated profile')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--pattern', default='*.txt', help='File pattern for directory processing')
    
    args = parser.parse_args()
    
    processor = DataProcessor(args.config)
    
    try:
        if args.command == 'process':
            if Path(args.input).is_file():
                results = [processor.process_text_file(args.input)]
            else:
                results = processor.process_directory(args.input, args.pattern)
            
            if args.output:
                processor.export_results(results, args.output, args.format)
                print(f"Results exported to {args.output}")
            else:
                print(json.dumps(results, indent=2))
        
        elif args.command == 'analyze':
            if Path(args.input).is_file():
                results = [processor.process_text_file(args.input)]
            else:
                results = processor.process_directory(args.input, args.pattern)
            
            analysis = processor.analyze_corpus_quality(results)
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(analysis, f, indent=2)
                print(f"Analysis exported to {args.output}")
            else:
                print(json.dumps(analysis, indent=2))
        
        elif args.command == 'profile':
            if not args.profile_name:
                print("Error: --profile-name required for profile command")
                return 1
            
            if Path(args.input).is_file():
                results = [processor.process_text_file(args.input)]
            else:
                results = processor.process_directory(args.input, args.pattern)
            
            profile = processor.create_corpus_profile(results, args.profile_name)
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(profile, f, indent=2)
                print(f"Profile exported to {args.output}")
            else:
                print(json.dumps(profile, indent=2))
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
