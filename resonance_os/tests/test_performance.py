"""
Performance Tests for ResonanceOS v6
"""

import unittest
import time
import tempfile
import shutil
from pathlib import Path
from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.api.hr_server import SimpleRequest, hr_generate


class TestPerformance(unittest.TestCase):
    """Test performance characteristics"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.writer = HumanResonantWriter()
        self.extractor = HRVExtractor()
        self.profile_manager = HRVProfileManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_writer_performance(self):
        """Test writer performance"""
        prompts = [
            "Short prompt",
            "This is a medium length prompt with more details",
            "This is a very long prompt with extensive details and specific requirements for content generation testing and performance evaluation"
        ]
        
        for prompt in prompts:
            start_time = time.time()
            
            # Generate content multiple times
            for _ in range(10):
                content = self.writer.generate(prompt)
                self.assertIsInstance(content, str)
                self.assertGreater(len(content), 0)
            
            end_time = time.time()
            avg_time = (end_time - start_time) / 10
            
            # Should complete within reasonable time (adjust threshold as needed)
            self.assertLess(avg_time, 2.0, f"Writer generation too slow for prompt: {prompt[:50]}...")
    
    def test_extractor_performance(self):
        """Test HRV extractor performance"""
        test_texts = [
            "Short text",
            "This is a medium length text with more words and sentences for testing HRV extraction performance.",
            "This is a very long text. " * 100  # Long text with multiple sentences
        ]
        
        for text in test_texts:
            start_time = time.time()
            
            # Extract HRV multiple times
            for _ in range(50):
                hrv = self.extractor.extract(text)
                self.assertIsInstance(hrv, list)
                self.assertEqual(len(hrv), 8)
            
            end_time = time.time()
            avg_time = (end_time - start_time) / 50
            
            # Should complete within reasonable time
            self.assertLess(avg_time, 0.1, f"HRV extraction too slow for text length: {len(text)}")
    
    def test_profile_manager_performance(self):
        """Test profile manager performance"""
        # Test save performance
        hrv_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        start_time = time.time()
        
        # Save many profiles
        for i in range(100):
            self.profile_manager.save_profile("perf_test", f"profile_{i}", hrv_vector)
        
        end_time = time.time()
        save_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(save_time, 5.0, "Profile saving too slow")
        
        # Test load performance
        start_time = time.time()
        
        # Load all profiles
        for i in range(100):
            loaded = self.profile_manager.load_profile("perf_test", f"profile_{i}")
            self.assertEqual(loaded, hrv_vector)
        
        end_time = time.time()
        load_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(load_time, 5.0, "Profile loading too slow")
        
        # Test list performance
        start_time = time.time()
        
        for _ in range(50):
            profiles = self.profile_manager.list_profiles("perf_test")
            self.assertEqual(len(profiles), 100)
        
        end_time = time.time()
        list_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(list_time, 1.0, "Profile listing too slow")
    
    def test_api_performance(self):
        """Test API performance"""
        prompts = [
            "Short API test",
            "Medium length API test with more content",
            "Long API test with extensive content and details for performance testing"
        ]
        
        for prompt in prompts:
            start_time = time.time()
            
            # Make multiple API calls
            for _ in range(10):
                request = SimpleRequest(prompt=prompt)
                response = hr_generate(request)
                self.assertIsInstance(response.article, str)
                self.assertIsInstance(response.hrv_feedback, list)
                self.assertEqual(len(response.hrv_feedback), 8)
            
            end_time = time.time()
            avg_time = (end_time - start_time) / 10
            
            # Should complete within reasonable time
            self.assertLess(avg_time, 2.0, f"API response too slow for prompt: {prompt[:50]}...")
    
    def test_memory_usage(self):
        """Test memory usage patterns"""
        import gc
        
        # Test memory doesn't grow excessively with repeated operations
        initial_objects = len(gc.get_objects())
        
        # Perform many operations
        for i in range(100):
            prompt = f"Memory test {i}"
            
            # Generate content
            content = self.writer.generate(prompt)
            
            # Extract HRV
            hrv = self.extractor.extract(content)
            
            # Save profile
            self.profile_manager.save_profile("memory_test", f"profile_{i}", hrv)
            
            # Load profile
            loaded = self.profile_manager.load_profile("memory_test", f"profile_{i}")
            
            # API call
            request = SimpleRequest(prompt=prompt)
            response = hr_generate(request)
            
            # Verify operations
            self.assertIsInstance(content, str)
            self.assertIsInstance(hrv, list)
            self.assertEqual(loaded, hrv)
            self.assertIsInstance(response.article, str)
        
        # Force garbage collection
        gc.collect()
        
        final_objects = len(gc.get_objects())
        object_growth = final_objects - initial_objects
        
        # Object growth should be reasonable (adjust threshold as needed)
        self.assertLess(object_growth, 10000, "Excessive memory growth detected")
    
    def test_concurrent_performance(self):
        """Test performance under concurrent-like operations"""
        import threading
        
        results = []
        lock = threading.Lock()
        
        def worker(worker_id):
            start_time = time.time()
            
            # Perform operations
            for i in range(10):
                prompt = f"Concurrent test {worker_id}_{i}"
                
                # Generate content
                content = self.writer.generate(prompt)
                
                # Extract HRV
                hrv = self.extractor.extract(content)
                
                # Save profile
                self.profile_manager.save_profile("concurrent_perf", f"profile_{worker_id}_{i}", hrv)
                
                # Load profile
                loaded = self.profile_manager.load_profile("concurrent_perf", f"profile_{worker_id}_{i}")
                
                # API call
                request = SimpleRequest(prompt=prompt)
                response = hr_generate(request)
                
                # Verify
                self.assertIsInstance(content, str)
                self.assertIsInstance(hrv, list)
                self.assertEqual(loaded, hrv)
                self.assertIsInstance(response.article, str)
            
            end_time = time.time()
            
            with lock:
                results.append((worker_id, end_time - start_time))
        
        # Create multiple threads
        threads = []
        start_time = time.time()
        
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(total_time, 30.0, "Concurrent operations too slow")
        
        # Verify all workers completed
        self.assertEqual(len(results), 5)
        
        # Verify individual worker times
        for worker_id, worker_time in results:
            self.assertLess(worker_time, 20.0, f"Worker {worker_id} too slow")
    
    def test_scalability_performance(self):
        """Test scalability with increasing load"""
        # Test with increasing numbers of operations
        operation_counts = [1, 10, 50, 100]
        
        for count in operation_counts:
            start_time = time.time()
            
            # Perform operations
            for i in range(count):
                prompt = f"Scalability test {i}"
                
                # Generate content
                content = self.writer.generate(prompt)
                
                # Extract HRV
                hrv = self.extractor.extract(content)
                
                # Save profile
                self.profile_manager.save_profile("scalability_test", f"profile_{i}", hrv)
            
            end_time = time.time()
            total_time = end_time - start_time
            avg_time = total_time / count
            
            # Average time should not increase dramatically with count
            self.assertLess(avg_time, 1.0, f"Scalability issue at count {count}")
            
            # Clean up for next test
            shutil.rmtree(self.temp_dir / "scalability_test")
            self.temp_dir.mkdir(exist_ok=True)
    
    def test_large_data_performance(self):
        """Test performance with large data"""
        # Test with large text
        large_text = "This is a test sentence. " * 10000
        
        start_time = time.time()
        
        # Extract HRV from large text
        hrv = self.extractor.extract(large_text)
        
        end_time = time.time()
        extraction_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(extraction_time, 5.0, "Large text HRV extraction too slow")
        
        # Test with large prompt
        large_prompt = "This is a large prompt for generation testing. " * 1000
        
        start_time = time.time()
        
        # Generate content with large prompt
        content = self.writer.generate(large_prompt)
        
        end_time = time.time()
        generation_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(generation_time, 10.0, "Large prompt generation too slow")
        
        # Test API with large prompt
        start_time = time.time()
        
        request = SimpleRequest(prompt=large_prompt)
        response = hr_generate(request)
        
        end_time = time.time()
        api_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(api_time, 10.0, "Large prompt API response too slow")
    
    def test_batch_operations_performance(self):
        """Test performance of batch operations"""
        # Test batch profile operations
        profiles_data = []
        
        # Prepare test data
        for i in range(50):
            hrv_vector = [0.1 * (i % 10)] * 8
            profiles_data.append((f"tenant_{i % 5}", f"profile_{i}", hrv_vector))
        
        # Test batch save performance
        start_time = time.time()
        
        for tenant, profile, hrv in profiles_data:
            self.profile_manager.save_profile(tenant, profile, hrv)
        
        end_time = time.time()
        batch_save_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(batch_save_time, 5.0, "Batch save too slow")
        
        # Test batch load performance
        start_time = time.time()
        
        for tenant, profile, original_hrv in profiles_data:
            loaded_hrv = self.profile_manager.load_profile(tenant, profile)
            self.assertEqual(loaded_hrv, original_hrv)
        
        end_time = time.time()
        batch_load_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(batch_load_time, 5.0, "Batch load too slow")
        
        # Test batch list performance
        start_time = time.time()
        
        for tenant, _, _ in profiles_data:
            profiles = self.profile_manager.list_profiles(tenant)
            self.assertGreater(len(profiles), 0)
        
        end_time = time.time()
        batch_list_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(batch_list_time, 2.0, "Batch list too slow")
    
    def test_performance_regression(self):
        """Test for performance regressions"""
        # Establish baseline performance
        prompt = "Performance regression test"
        
        # Test writer baseline
        start_time = time.time()
        for _ in range(20):
            content = self.writer.generate(prompt)
        writer_baseline = time.time() - start_time
        
        # Test extractor baseline
        start_time = time.time()
        for _ in range(100):
            hrv = self.extractor.extract(prompt)
        extractor_baseline = time.time() - start_time
        
        # Test API baseline
        start_time = time.time()
        for _ in range(20):
            request = SimpleRequest(prompt=prompt)
            response = hr_generate(request)
        api_baseline = time.time() - start_time
        
        # Define performance thresholds (adjust based on baseline measurements)
        writer_threshold = writer_baseline * 1.5  # 50% slower than baseline
        extractor_threshold = extractor_baseline * 1.5
        api_threshold = api_baseline * 1.5
        
        # Test current performance
        start_time = time.time()
        for _ in range(20):
            content = self.writer.generate(prompt)
        writer_current = time.time() - start_time
        
        start_time = time.time()
        for _ in range(100):
            hrv = self.extractor.extract(prompt)
        extractor_current = time.time() - start_time
        
        start_time = time.time()
        for _ in range(20):
            request = SimpleRequest(prompt=prompt)
            response = hr_generate(request)
        api_current = time.time() - start_time
        
        # Check for regressions
        self.assertLess(writer_current, writer_threshold, "Writer performance regression detected")
        self.assertLess(extractor_current, extractor_threshold, "Extractor performance regression detected")
        self.assertLess(api_current, api_threshold, "API performance regression detected")


if __name__ == '__main__':
    unittest.main()
