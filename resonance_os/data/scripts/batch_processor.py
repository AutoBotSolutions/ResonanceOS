#!/usr/bin/env python3
"""
Batch Processor for ResonanceOS v6

This script provides batch processing capabilities for large-scale
content generation, profile management, and data analysis.
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import cpu_count

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.api.hr_server import SimpleRequest, hr_generate


class BatchProcessor:
    """High-performance batch processing utility"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the batch processor"""
        self.config = config or {}
        self.writer = HumanResonantWriter()
        self.extractor = HRVExtractor()
        self.profiles_dir = Path(self.config.get('profiles_dir', './profiles/hr_profiles'))
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.profile_manager = HRVProfileManager(self.profiles_dir)
        
        # Performance settings
        self.max_workers = self.config.get('max_workers', min(cpu_count(), 8))
        self.batch_size = self.config.get('batch_size', 32)
        self.use_multiprocessing = self.config.get('use_multiprocessing', True)
    
    def batch_generate_content(self, prompts: List[str], tenant: str = None, 
                             profile_name: str = None) -> List[Dict[str, Any]]:
        """Generate content for multiple prompts in batch"""
        results = []
        
        if self.use_multiprocessing and len(prompts) > self.batch_size:
            # Use process pool for large batches
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                for prompt in prompts:
                    future = executor.submit(self._generate_single_content, prompt, tenant, profile_name)
                    futures.append(future)
                
                for future in futures:
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append({'error': str(e)})
        else:
            # Use thread pool or sequential processing
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                for prompt in prompts:
                    future = executor.submit(self._generate_single_content, prompt, tenant, profile_name)
                    futures.append(future)
                
                for future in futures:
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append({'error': str(e)})
        
        return results
    
    def _generate_single_content(self, prompt: str, tenant: str = None, profile_name: str = None) -> Dict[str, Any]:
        """Generate content for a single prompt"""
        try:
            start_time = time.time()
            
            # Generate content
            content = self.writer.generate(prompt)
            
            # Extract HRV
            hrv_vector = self.extractor.extract(content)
            
            # API call for comparison
            request = SimpleRequest(prompt=prompt, tenant=tenant, profile_name=profile_name)
            api_response = hr_generate(request)
            
            end_time = time.time()
            
            return {
                'prompt': prompt,
                'content': content,
                'hrv_vector': hrv_vector,
                'api_response': {
                    'article': api_response.article,
                    'hrv_feedback': api_response.hrv_feedback
                },
                'tenant': tenant,
                'profile_name': profile_name,
                'generation_time': end_time - start_time,
                'word_count': len(content.split()),
                'success': True
            }
        except Exception as e:
            return {
                'prompt': prompt,
                'error': str(e),
                'tenant': tenant,
                'profile_name': profile_name,
                'success': False
            }
    
    def batch_extract_hrv(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Extract HRV vectors from multiple texts"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for i, text in enumerate(texts):
                future = executor.submit(self._extract_single_hrv, text, i)
                futures.append(future)
            
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({'error': str(e)})
        
        return results
    
    def _extract_single_hrv(self, text: str, index: int) -> Dict[str, Any]:
        """Extract HRV from a single text"""
        try:
            start_time = time.time()
            hrv_vector = self.extractor.extract(text)
            end_time = time.time()
            
            return {
                'index': index,
                'hrv_vector': hrv_vector,
                'text_length': len(text),
                'word_count': len(text.split()),
                'extraction_time': end_time - start_time,
                'success': True
            }
        except Exception as e:
            return {
                'index': index,
                'error': str(e),
                'success': False
            }
    
    def batch_create_profiles(self, profiles_data: List[Dict[str, Any]], tenant: str) -> List[Dict[str, Any]]:
        """Create multiple profiles in batch"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for profile_data in profiles_data:
                future = executor.submit(self._create_single_profile, profile_data, tenant)
                futures.append(future)
            
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({'error': str(e)})
        
        return results
    
    def _create_single_profile(self, profile_data: Dict[str, Any], tenant: str) -> Dict[str, Any]:
        """Create a single profile"""
        try:
            start_time = time.time()
            
            name = profile_data['name']
            hrv_vector = profile_data['hrv_vector']
            description = profile_data.get('description', f'Profile for {name}')
            
            # Save HRV vector
            self.profile_manager.save_profile(tenant, name, hrv_vector)
            
            # Save full metadata
            metadata_dir = self.profiles_dir / tenant / "metadata"
            metadata_dir.mkdir(parents=True, exist_ok=True)
            
            metadata_file = metadata_dir / f"{name}.json"
            full_profile = {
                'name': name,
                'description': description,
                'hrv_vector': hrv_vector,
                'metadata': {
                    'created_at': '2026-03-09T00:00:00Z',
                    'tenant': tenant,
                    'created_by': 'BatchProcessor'
                }
            }
            
            if 'metadata' in profile_data:
                full_profile['metadata'].update(profile_data['metadata'])
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(full_profile, f, indent=2, ensure_ascii=False)
            
            end_time = time.time()
            
            return {
                'name': name,
                'tenant': tenant,
                'hrv_vector': hrv_vector,
                'creation_time': end_time - start_time,
                'success': True
            }
        except Exception as e:
            return {
                'name': profile_data.get('name', 'unknown'),
                'tenant': tenant,
                'error': str(e),
                'success': False
            }
    
    def batch_analyze_content(self, contents: List[str]) -> List[Dict[str, Any]]:
        """Analyze multiple contents for quality metrics"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for i, content in enumerate(contents):
                future = executor.submit(self._analyze_single_content, content, i)
                futures.append(future)
            
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({'error': str(e)})
        
        return results
    
    def _analyze_single_content(self, content: str, index: int) -> Dict[str, Any]:
        """Analyze a single content"""
        try:
            start_time = time.time()
            
            # Basic metrics
            words = content.split()
            sentences = [s.strip() for s in content.split('.') if s.strip()]
            
            # HRV analysis
            hrv_vector = self.extractor.extract(content)
            
            # Quality metrics
            quality_score = self._calculate_quality_score(content, hrv_vector)
            
            end_time = time.time()
            
            return {
                'index': index,
                'word_count': len(words),
                'sentence_count': len(sentences),
                'avg_sentence_length': sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0,
                'hrv_vector': hrv_vector,
                'quality_score': quality_score,
                'analysis_time': end_time - start_time,
                'success': True
            }
        except Exception as e:
            return {
                'index': index,
                'error': str(e),
                'success': False
            }
    
    def _calculate_quality_score(self, content: str, hrv_vector: List[float]) -> float:
        """Calculate quality score for content"""
        if not content or not hrv_vector:
            return 0.0
        
        # Factors for quality score
        words = content.split()
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        # Length score (ideal around 200-500 words)
        word_count = len(words)
        if 200 <= word_count <= 500:
            length_score = 1.0
        elif word_count < 200:
            length_score = word_count / 200
        else:
            length_score = max(0.5, 500 / word_count)
        
        # Sentence variety score
        sentence_lengths = [len(s.split()) for s in sentences]
        if len(sentence_lengths) > 1:
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((x - avg_length) ** 2 for x in sentence_lengths) / len(sentence_lengths)
            variety_score = min(variance / 25, 1.0)  # Normalize
        else:
            variety_score = 0.0
        
        # HRV balance score
        hrv_balance = 1.0 - sum(abs(x - 0.5) for x in hrv_vector) / 4.0  # Ideal around 0.5
        
        # Readability score (simplified)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        if 10 <= avg_sentence_length <= 20:
            readability_score = 1.0
        elif avg_sentence_length < 10:
            readability_score = avg_sentence_length / 10
        else:
            readability_score = max(0.5, 20 / avg_sentence_length)
        
        # Weighted combination
        quality_score = (
            length_score * 0.2 +
            variety_score * 0.3 +
            hrv_balance * 0.3 +
            readability_score * 0.2
        )
        
        return min(1.0, max(0.0, quality_score))
    
    def process_batch_file(self, input_file: str, output_file: str, operation: str, **kwargs) -> bool:
        """Process batch from file and save results"""
        try:
            # Load input data
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Process based on operation
            if operation == 'generate':
                prompts = data.get('prompts', [])
                tenant = kwargs.get('tenant')
                profile_name = kwargs.get('profile_name')
                results = self.batch_generate_content(prompts, tenant, profile_name)
            
            elif operation == 'extract_hrv':
                texts = data.get('texts', [])
                results = self.batch_extract_hrv(texts)
            
            elif operation == 'create_profiles':
                profiles_data = data.get('profiles', [])
                tenant = kwargs.get('tenant')
                if not tenant:
                    raise ValueError("Tenant required for create_profiles operation")
                results = self.batch_create_profiles(profiles_data, tenant)
            
            elif operation == 'analyze':
                contents = data.get('contents', [])
                results = self.batch_analyze_content(contents)
            
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            # Save results
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"Error processing batch file: {e}")
            return False
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        return {
            'max_workers': self.max_workers,
            'batch_size': self.batch_size,
            'use_multiprocessing': self.use_multiprocessing,
            'cpu_count': cpu_count(),
            'profiles_directory': str(self.profiles_dir),
            'system_status': 'operational'
        }


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='ResonanceOS Batch Processor')
    parser.add_argument('command', choices=['generate', 'extract_hrv', 'create_profiles', 'analyze', 'metrics'], 
                       help='Command to execute')
    parser.add_argument('--input', help='Input file path')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--tenant', help='Tenant name')
    parser.add_argument('--profile', help='Profile name')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--workers', type=int, help='Number of workers')
    parser.add_argument('--batch-size', type=int, help='Batch size')
    parser.add_argument('--use-threads', action='store_true', help='Use threads instead of processes')
    
    args = parser.parse_args()
    
    # Load configuration
    config = {}
    if args.config and Path(args.config).exists():
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # Override config with command line arguments
    if args.workers:
        config['max_workers'] = args.workers
    if args.batch_size:
        config['batch_size'] = args.batch_size
    if args.use_threads:
        config['use_multiprocessing'] = False
    
    processor = BatchProcessor(config)
    
    try:
        if args.command == 'metrics':
            metrics = processor.get_performance_metrics()
            print(json.dumps(metrics, indent=2))
        
        elif args.command in ['generate', 'extract_hrv', 'create_profiles', 'analyze']:
            if not args.input or not args.output:
                print("Error: --input and --output required for batch operations")
                return 1
            
            kwargs = {}
            if args.tenant:
                kwargs['tenant'] = args.tenant
            if args.profile:
                kwargs['profile_name'] = args.profile
            
            success = processor.process_batch_file(args.input, args.output, args.command, **kwargs)
            
            if success:
                print(f"Batch {args.command} completed successfully")
                print(f"Results saved to {args.output}")
            else:
                print(f"Batch {args.command} failed")
                return 1
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
