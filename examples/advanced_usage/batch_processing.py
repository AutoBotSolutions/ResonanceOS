#!/usr/bin/env python3
"""
Advanced Batch Processing Example

This example demonstrates advanced batch processing capabilities in ResonanceOS v6,
including parallel processing, performance optimization, and large-scale operations.
"""

import sys
import os
import json
import time
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.api.hr_server import SimpleRequest, hr_generate


@dataclass
class BatchRequest:
    """Data class for batch processing requests"""
    id: str
    prompt: str
    tenant: str = "default"
    profile_name: str = "neutral_professional"
    metadata: Dict[str, Any] = None


@dataclass
class BatchResult:
    """Data class for batch processing results"""
    id: str
    success: bool
    content: str = None
    hrv_vector: List[float] = None
    error: str = None
    processing_time: float = 0.0
    metadata: Dict[str, Any] = None


class BatchProcessor:
    """Advanced batch processor for ResonanceOS v6"""
    
    def __init__(self, max_workers: int = 4, batch_size: int = 32):
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.writer = HumanResonantWriter()
        self.extractor = HRVExtractor()
        self.profile_manager = HRVProfileManager("./data/profiles/hr_profiles")
        
    def process_single_request(self, request: BatchRequest) -> BatchResult:
        """Process a single batch request"""
        start_time = time.time()
        
        try:
            # Generate content
            content = self.writer.generate(request.prompt)
            
            # Extract HRV
            hrv_vector = self.extractor.extract(content)
            
            processing_time = time.time() - start_time
            
            return BatchResult(
                id=request.id,
                success=True,
                content=content,
                hrv_vector=hrv_vector,
                processing_time=processing_time,
                metadata=request.metadata
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            return BatchResult(
                id=request.id,
                success=False,
                error=str(e),
                processing_time=processing_time,
                metadata=request.metadata
            )
    
    def process_batch_sequential(self, requests: List[BatchRequest]) -> List[BatchResult]:
        """Process batch requests sequentially"""
        print(f"Processing {len(requests)} requests sequentially...")
        start_time = time.time()
        
        results = []
        for i, request in enumerate(requests, 1):
            print(f"Processing {i}/{len(requests)}: {request.id}")
            result = self.process_single_request(request)
            results.append(result)
            
            if result.success:
                print(f"✅ {request.id}: {len(result.content)} chars, HRV: {sum(result.hrv_vector)/len(result.hrv_vector):.3f}")
            else:
                print(f"❌ {request.id}: {result.error}")
        
        total_time = time.time() - start_time
        print(f"Sequential processing completed in {total_time:.2f} seconds")
        
        return results
    
    def process_batch_parallel(self, requests: List[BatchRequest]) -> List[BatchResult]:
        """Process batch requests in parallel"""
        print(f"Processing {len(requests)} requests in parallel with {self.max_workers} workers...")
        start_time = time.time()
        
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all requests
            future_to_request = {
                executor.submit(self.process_single_request, request): request
                for request in requests
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_request):
                request = future_to_request[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result.success:
                        print(f"✅ {request.id}: {len(result.content)} chars, HRV: {sum(result.hrv_vector)/len(result.hrv_vector):.3f}")
                    else:
                        print(f"❌ {request.id}: {result.error}")
                        
                except Exception as e:
                    error_result = BatchResult(
                        id=request.id,
                        success=False,
                        error=f"Processing error: {e}",
                        metadata=request.metadata
                    )
                    results.append(error_result)
                    print(f"❌ {request.id}: Processing error: {e}")
        
        total_time = time.time() - start_time
        print(f"Parallel processing completed in {total_time:.2f} seconds")
        
        return results
    
    def process_batch_chunked(self, requests: List[BatchRequest]) -> List[BatchResult]:
        """Process batch requests in chunks for memory efficiency"""
        print(f"Processing {len(requests)} requests in chunks of {self.batch_size}...")
        start_time = time.time()
        
        all_results = []
        
        for i in range(0, len(requests), self.batch_size):
            chunk = requests[i:i + self.batch_size]
            print(f"Processing chunk {i//self.batch_size + 1}/{(len(requests) + self.batch_size - 1)//self.batch_size}")
            
            # Process chunk in parallel
            chunk_results = self.process_batch_parallel(chunk)
            all_results.extend(chunk_results)
        
        total_time = time.time() - start_time
        print(f"Chunked processing completed in {total_time:.2f} seconds")
        
        return all_results


def create_sample_requests() -> List[BatchRequest]:
    """Create sample batch requests"""
    prompts = [
        "The future of artificial intelligence in healthcare",
        "Sustainable technology solutions for urban development",
        "Digital transformation strategies for traditional businesses",
        "The impact of remote work on organizational culture",
        "Innovative approaches to customer experience management",
        "Blockchain applications beyond cryptocurrency",
        "The role of data science in modern marketing",
        "Cybersecurity best practices for small businesses",
        "Machine learning applications in financial services",
        "The evolution of cloud computing architecture",
        "Social media marketing trends for 2024",
        "Supply chain optimization using AI and IoT",
        "The importance of user experience design",
        "Data privacy regulations and compliance",
        "Emerging technologies in education",
        "The future of work in the AI era",
        "Sustainable business models for the 21st century",
        "The psychology of consumer decision making",
        "Innovation management in large organizations",
        "The impact of 5G on IoT applications"
    ]
    
    requests = []
    for i, prompt in enumerate(prompts):
        request = BatchRequest(
            id=f"req_{i+1:03d}",
            prompt=prompt,
            tenant=f"tenant_{(i % 3) + 1}",
            profile_name=["neutral_professional", "creative_storytelling", "technical_academic"][i % 3],
            metadata={"category": ["business", "technology", "marketing"][i % 3]}
        )
        requests.append(request)
    
    return requests


def analyze_batch_results(results: List[BatchResult]) -> Dict[str, Any]:
    """Analyze batch processing results"""
    if not results:
        return {}
    
    success_count = sum(1 for r in results if r.success)
    error_count = len(results) - success_count
    
    if success_count > 0:
        successful_results = [r for r in results if r.success]
        avg_processing_time = sum(r.processing_time for r in successful_results) / len(successful_results)
        avg_content_length = sum(len(r.content) for r in successful_results) / len(successful_results)
        
        # HRV statistics
        all_hrv_vectors = [r.hrv_vector for r in successful_results]
        avg_hrv_scores = [sum(vector) / len(vector) for vector in all_hrv_vectors]
        overall_avg_hrv = sum(avg_hrv_scores) / len(avg_hrv_scores)
        
        # Dimension statistics
        dimension_stats = []
        for i in range(8):
            values = [vector[i] for vector in all_hrv_vectors]
            dimension_stats.append({
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values)
            })
    else:
        avg_processing_time = 0
        avg_content_length = 0
        overall_avg_hrv = 0
        dimension_stats = []
    
    return {
        "total_requests": len(results),
        "successful_requests": success_count,
        "failed_requests": error_count,
        "success_rate": success_count / len(results),
        "avg_processing_time": avg_processing_time,
        "avg_content_length": avg_content_length,
        "overall_avg_hrv": overall_avg_hrv,
        "dimension_stats": dimension_stats,
        "errors": [r.error for r in results if not r.success]
    }


def performance_comparison_example():
    """Compare performance of different processing methods"""
    print("🚀 Performance Comparison Example")
    print("=" * 60)
    
    # Create sample requests
    requests = create_sample_requests()[:10]  # Use subset for comparison
    
    print(f"Comparing processing methods with {len(requests)} requests...")
    print()
    
    processor = BatchProcessor(max_workers=2, batch_size=5)
    
    # Sequential processing
    print("📊 Sequential Processing:")
    sequential_results = processor.process_batch_sequential(requests)
    sequential_stats = analyze_batch_results(sequential_results)
    print(f"Time: {sum(r.processing_time for r in sequential_results):.2f}s")
    print(f"Success Rate: {sequential_stats['success_rate']:.1%}")
    print()
    
    # Parallel processing
    print("📊 Parallel Processing:")
    parallel_results = processor.process_batch_parallel(requests)
    parallel_stats = analyze_batch_results(parallel_results)
    print(f"Time: {sum(r.processing_time for r in parallel_results):.2f}s")
    print(f"Success Rate: {parallel_stats['success_rate']:.1%}")
    print()
    
    # Performance comparison
    sequential_time = sum(r.processing_time for r in sequential_results)
    parallel_time = sum(r.processing_time for r in parallel_results)
    
    if parallel_time > 0:
        speedup = sequential_time / parallel_time
        print(f"🏆 Performance Improvement: {speedup:.2f}x faster with parallel processing")
    
    return sequential_stats, parallel_stats


def large_scale_processing_example():
    """Demonstrate large-scale batch processing"""
    print("\n📦 Large-Scale Batch Processing Example")
    print("=" * 60)
    
    # Create larger batch
    large_requests = create_sample_requests()
    
    print(f"Processing {len(large_requests)} requests...")
    print()
    
    # Configure processor for large scale
    processor = BatchProcessor(max_workers=4, batch_size=8)
    
    # Process in chunks
    results = processor.process_batch_chunked(large_requests)
    
    # Analyze results
    stats = analyze_batch_results(results)
    
    print("\n📊 Large-Scale Processing Results:")
    print("-" * 40)
    print(f"Total Requests: {stats['total_requests']}")
    print(f"Successful: {stats['successful_requests']}")
    print(f"Failed: {stats['failed_requests']}")
    print(f"Success Rate: {stats['success_rate']:.1%}")
    print(f"Avg Processing Time: {stats['avg_processing_time']:.3f}s")
    print(f"Avg Content Length: {stats['avg_content_length']:.0f} chars")
    print(f"Overall HRV Score: {stats['overall_avg_hrv']:.3f}")
    
    if stats['errors']:
        print(f"\n⚠️  Errors encountered: {len(stats['errors'])}")
        for error in stats['errors'][:3]:  # Show first 3 errors
            print(f"  - {error}")
    
    return stats


def multi_tenant_batch_example():
    """Demonstrate multi-tenant batch processing"""
    print("\n🏢 Multi-Tenant Batch Processing Example")
    print("=" * 60)
    
    # Create multi-tenant requests
    tenants = ["tech_corp", "marketing_agency", "research_university"]
    profiles = {
        "tech_corp": "technical_academic",
        "marketing_agency": "marketing_enthusiastic",
        "research_university": "neutral_professional"
    }
    
    multi_tenant_requests = []
    for i, tenant in enumerate(tenants):
        for j in range(5):  # 5 requests per tenant
            request = BatchRequest(
                id=f"{tenant}_req_{j+1}",
                prompt=f"Sample prompt for {tenant} - request {j+1}",
                tenant=tenant,
                profile_name=profiles[tenant],
                metadata={"tenant_type": tenant}
            )
            multi_tenant_requests.append(request)
    
    print(f"Processing {len(multi_tenant_requests)} multi-tenant requests...")
    print()
    
    # Process multi-tenant batch
    processor = BatchProcessor(max_workers=3)
    results = processor.process_batch_parallel(multi_tenant_requests)
    
    # Analyze by tenant
    tenant_stats = {}
    for tenant in tenants:
        tenant_results = [r for r in results if r.metadata and r.metadata.get("tenant_type") == tenant]
        tenant_stats[tenant] = analyze_batch_results(tenant_results)
    
    print("📊 Multi-Tenant Results:")
    print("-" * 40)
    for tenant, stats in tenant_stats.items():
        print(f"{tenant}:")
        print(f"  Requests: {stats['total_requests']}")
        print(f"  Success Rate: {stats['success_rate']:.1%}")
        print(f"  Avg HRV: {stats['overall_avg_hrv']:.3f}")
        print()
    
    return tenant_stats


def quality_filtering_example():
    """Demonstrate quality-based filtering in batch processing"""
    print("\n🔍 Quality Filtering Example")
    print("=" * 60)
    
    # Create requests with expected quality variations
    quality_requests = [
        BatchRequest("high_quality_1", "Comprehensive analysis of market trends reveals significant opportunities for growth and innovation in emerging sectors."),
        BatchRequest("medium_quality_1", "This is a simple text about market trends and business opportunities."),
        BatchRequest("low_quality_1", "bad text"),
        BatchRequest("high_quality_2", "The strategic implementation of advanced technologies enables organizations to achieve competitive advantage through operational excellence and innovation."),
        BatchRequest("medium_quality_2", "Technology helps businesses improve their operations and achieve better results."),
        BatchRequest("low_quality_2", "simple text only")
    ]
    
    print("Processing requests with quality filtering...")
    print()
    
    processor = BatchProcessor()
    results = processor.process_batch_parallel(quality_requests)
    
    # Filter by quality
    high_quality_threshold = 0.7
    medium_quality_threshold = 0.5
    
    high_quality = []
    medium_quality = []
    low_quality = []
    
    for result in results:
        if result.success:
            hrv_score = sum(result.hrv_vector) / len(result.hrv_vector)
            if hrv_score >= high_quality_threshold:
                high_quality.append(result)
            elif hrv_score >= medium_quality_threshold:
                medium_quality.append(result)
            else:
                low_quality.append(result)
    
    print("📊 Quality Distribution Results:")
    print("-" * 40)
    print(f"High Quality (≥0.7): {len(high_quality)} requests")
    print(f"Medium Quality (0.5-0.7): {len(medium_quality)} requests")
    print(f"Low Quality (<0.5): {len(low_quality)} requests")
    print()
    
    # Show examples
    if high_quality:
        print("🏆 High Quality Example:")
        result = high_quality[0]
        hrv_score = sum(result.hrv_vector) / len(result.hrv_vector)
        print(f"  {result.id}: HRV {hrv_score:.3f}")
        print(f"  Content: {result.content[:100]}...")
        print()
    
    if low_quality:
        print("⚠️  Low Quality Example:")
        result = low_quality[0]
        hrv_score = sum(result.hrv_vector) / len(result.hrv_vector)
        print(f"  {result.id}: HRV {hrv_score:.3f}")
        print(f"  Content: {result.content}")
        print()
    
    return high_quality, medium_quality, low_quality


def export_results_example(results: List[BatchResult], filename: str = "batch_results.json"):
    """Export batch results to JSON file"""
    print(f"\n💾 Exporting Results to {filename}")
    print("-" * 40)
    
    # Convert results to exportable format
    export_data = {
        "export_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_requests": len(results),
        "successful_requests": sum(1 for r in results if r.success),
        "failed_requests": sum(1 for r in results if not r.success),
        "results": []
    }
    
    for result in results:
        result_data = {
            "id": result.id,
            "success": result.success,
            "processing_time": result.processing_time,
            "metadata": result.metadata
        }
        
        if result.success:
            result_data.update({
                "content_length": len(result.content),
                "hrv_vector": result.hrv_vector,
                "hrv_score": sum(result.hrv_vector) / len(result.hrv_vector),
                "content_preview": result.content[:100] + "..." if len(result.content) > 100 else result.content
            })
        else:
            result_data["error"] = result.error
        
        export_data["results"].append(result_data)
    
    # Save to file
    output_path = Path(__file__).parent / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Results exported to {output_path}")
    print(f"📊 Export summary:")
    print(f"  Total requests: {export_data['total_requests']}")
    print(f"  Successful: {export_data['successful_requests']}")
    print(f"  Failed: {export_data['failed_requests']}")
    
    return output_path


def main():
    """Run all advanced batch processing examples"""
    print("🎯 ResonanceOS v6 - Advanced Batch Processing Examples")
    print("=" * 60)
    print("This example demonstrates advanced batch processing capabilities.")
    print("You'll learn how to:")
    print("- Process batches sequentially and in parallel")
    print("- Optimize performance with chunked processing")
    print("- Handle large-scale operations")
    print("- Manage multi-tenant processing")
    print("- Filter results by quality")
    print("- Export results for analysis")
    print()
    
    try:
        # Run examples
        seq_stats, par_stats = performance_comparison_example()
        large_stats = large_scale_processing_example()
        tenant_stats = multi_tenant_batch_example()
        high_q, med_q, low_q = quality_filtering_example()
        
        # Export comprehensive results
        all_results = []
        processor = BatchProcessor()
        sample_requests = create_sample_requests()[:5]
        sample_results = processor.process_batch_parallel(sample_requests)
        all_results.extend(sample_results)
        
        export_file = export_results_example(all_results, "advanced_batch_results.json")
        
        print("\n🎉 All advanced batch processing examples completed successfully!")
        print("\nKey Takeaways:")
        print("- Parallel processing provides significant performance improvements")
        print("- Chunked processing enables memory-efficient large-scale operations")
        print("- Multi-tenant processing supports enterprise use cases")
        print("- Quality filtering ensures content standards")
        print("- Export capabilities enable downstream analysis")
        print(f"\n📁 Results exported to: {export_file}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")


if __name__ == "__main__":
    main()
