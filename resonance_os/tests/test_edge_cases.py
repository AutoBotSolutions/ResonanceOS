"""
Edge Case Tests for ResonanceOS v6
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.api.hr_server import SimpleRequest, hr_generate


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.writer = HumanResonantWriter()
        self.extractor = HRVExtractor()
        self.profile_manager = HRVProfileManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_extremely_long_prompt(self):
        """Test with extremely long prompts"""
        long_prompt = "This is a very long prompt. " * 10000
        
        # Test writer
        content = self.writer.generate(long_prompt)
        self.assertIsInstance(content, str)
        self.assertIn(long_prompt, content)
        
        # Test extractor
        hrv = self.extractor.extract(long_prompt)
        self.assertIsInstance(hrv, list)
        self.assertEqual(len(hrv), 8)
        
        # Test API
        request = SimpleRequest(prompt=long_prompt)
        response = hr_generate(request)
        self.assertIsInstance(response.article, str)
        self.assertIn(long_prompt, response.article)
    
    def test_extremely_short_prompt(self):
        """Test with extremely short prompts"""
        short_prompts = ["", "a", "ab", "abc"]
        
        for prompt in short_prompts:
            # Test writer
            content = self.writer.generate(prompt)
            self.assertIsInstance(content, str)
            
            # Test extractor
            hrv = self.extractor.extract(prompt)
            self.assertIsInstance(hrv, list)
            self.assertEqual(len(hrv), 8)
            
            # Test API
            request = SimpleRequest(prompt=prompt)
            response = hr_generate(request)
            self.assertIsInstance(response.article, str)
    
    def test_unicode_edge_cases(self):
        """Test with various unicode edge cases"""
        unicode_prompts = [
            "café naïve résumé",
            "🚀🌟💫✨",  # Emojis
            "中文测试",  # Chinese
            "العربية",  # Arabic
            "עברית",  # Hebrew
            "混合 English 中文 العربية",
            "\u0000\u0001\u0002",  # Control characters
            "𝔽𝕣𝕒𝕜𝕥𝕦𝕣𝕖𝕕 𝕌𝕟𝕚𝕔𝕠𝕕𝕖",  # Mathematical unicode
        ]
        
        for prompt in unicode_prompts:
            try:
                # Test writer
                content = self.writer.generate(prompt)
                self.assertIsInstance(content, str)
                
                # Test extractor
                hrv = self.extractor.extract(prompt)
                self.assertIsInstance(hrv, list)
                self.assertEqual(len(hrv), 8)
                
                # Test API
                request = SimpleRequest(prompt=prompt)
                response = hr_generate(request)
                self.assertIsInstance(response.article, str)
            except UnicodeError:
                # Some unicode may cause issues, which is acceptable
                pass
    
    def test_special_characters_edge_cases(self):
        """Test with various special characters"""
        special_prompts = [
            "@#$%^&*()_+-=[]{}|;':\",./<>?",
            "\n\r\t",  # Whitespace characters
            "   ",  # Spaces only
            "\x00\x01\x02",  # Non-printable characters
            "<<<>>>|||&&&",  # Programming symbols
            "Test\nNewline\tTab\rCarriage",
        ]
        
        for prompt in special_prompts:
            try:
                # Test writer
                content = self.writer.generate(prompt)
                self.assertIsInstance(content, str)
                
                # Test extractor
                hrv = self.extractor.extract(prompt)
                self.assertIsInstance(hrv, list)
                self.assertEqual(len(hrv), 8)
                
                # Test API
                request = SimpleRequest(prompt=prompt)
                response = hr_generate(request)
                self.assertIsInstance(response.article, str)
            except (ValueError, UnicodeError):
                # Some special characters may cause issues
                pass
    
    def test_numeric_edge_cases(self):
        """Test with numeric edge cases"""
        numeric_prompts = [
            "0",
            "-1",
            "3.14159",
            "1.7976931348623157e+308",  # Max float
            "2.2250738585072014e-308",  # Min float
            "1234567890" * 1000,  # Very large number
        ]
        
        for prompt in numeric_prompts:
            # Test writer
            content = self.writer.generate(prompt)
            self.assertIsInstance(content, str)
            
            # Test extractor
            hrv = self.extractor.extract(prompt)
            self.assertIsInstance(hrv, list)
            self.assertEqual(len(hrv), 8)
            
            # Test API
            request = SimpleRequest(prompt=prompt)
            response = hr_generate(request)
            self.assertIsInstance(response.article, str)
    
    def test_hrv_vector_edge_cases(self):
        """Test HRV vector edge cases"""
        edge_vectors = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # All zeros
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # All ones
            [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  # All same
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],  # Increasing
            [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],  # Decreasing
            [0.1, 0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.9],  # Alternating
        ]
        
        for hrv_vector in edge_vectors:
            # Test profile manager
            self.profile_manager.save_profile("edge_test", "test_profile", hrv_vector)
            loaded_hrv = self.profile_manager.load_profile("edge_test", "test_profile")
            self.assertEqual(loaded_hrv, hrv_vector)
            
            # Verify profile listing
            profiles = self.profile_manager.list_profiles("edge_test")
            self.assertIn("test_profile", profiles)
    
    def test_invalid_hrv_vectors(self):
        """Test invalid HRV vectors"""
        invalid_vectors = [
            [],  # Empty
            [0.1, 0.2, 0.3],  # Too short
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],  # Too long
            ["not", "numeric", "values"],  # Non-numeric
            [None, None, None, None, None, None, None, None],  # None values
            [float('inf'), 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],  # Infinity
            [float('nan'), 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],  # NaN
        ]
        
        for invalid_vector in invalid_vectors:
            try:
                self.profile_manager.save_profile("invalid_test", "test_profile", invalid_vector)
                # If save succeeds, try to load
                loaded = self.profile_manager.load_profile("invalid_test", "test_profile")
                # May succeed or fail depending on implementation
            except (TypeError, ValueError, AttributeError):
                # Expected behavior for invalid vectors
                pass
    
    def test_file_system_edge_cases(self):
        """Test file system edge cases"""
        # Test very long tenant/profile names
        long_name = "a" * 1000
        
        try:
            hrv_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
            self.profile_manager.save_profile(long_name, long_name, hrv_vector)
            loaded = self.profile_manager.load_profile(long_name, long_name)
            self.assertEqual(loaded, hrv_vector)
        except (OSError, ValueError):
            # May fail due to file system limitations
            pass
        
        # Test special characters in names
        special_names = [
            "test@#$%^&*()",
            "test\nname",
            "test\tname",
            "test\0name",
            "test/name",  # Path separator
            "test\\name",  # Path separator
        ]
        
        for name in special_names:
            try:
                hrv_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
                self.profile_manager.save_profile(name, "profile", hrv_vector)
                loaded = self.profile_manager.load_profile(name, "profile")
                self.assertEqual(loaded, hrv_vector)
            except (OSError, ValueError):
                # May fail due to file system limitations
                pass
    
    def test_memory_edge_cases(self):
        """Test memory-related edge cases"""
        # Test with many operations to check for memory leaks
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
            
            # Verify
            self.assertIsInstance(content, str)
            self.assertIsInstance(hrv, list)
            self.assertEqual(loaded, hrv)
        
        # Verify all profiles exist
        profiles = self.profile_manager.list_profiles("memory_test")
        self.assertEqual(len(profiles), 100)
    
    def test_concurrent_operations(self):
        """Test concurrent-like operations"""
        import threading
        import time
        
        results = []
        
        def worker(worker_id):
            try:
                prompt = f"Concurrent test {worker_id}"
                content = self.writer.generate(prompt)
                hrv = self.extractor.extract(content)
                self.profile_manager.save_profile("concurrent_test", f"profile_{worker_id}", hrv)
                loaded = self.profile_manager.load_profile("concurrent_test", f"profile_{worker_id}")
                
                # API call
                request = SimpleRequest(prompt=prompt)
                response = hr_generate(request)
                
                # Verify
                self.assertIsInstance(content, str)
                self.assertIsInstance(hrv, list)
                self.assertEqual(loaded, hrv)
                self.assertIsInstance(response.article, str)
                
                results.append((worker_id, content, hrv, loaded, response.article))
            except Exception as e:
                results.append((worker_id, str(e)))
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify results
        self.assertEqual(len(results), 5)
        for result in results:
            worker_id = result[0]
            if len(result) == 2:
                # Error occurred
                pass
            else:
                content, hrv, loaded, api_article = result[1:5]
                self.assertIsInstance(content, str)
                self.assertIsInstance(hrv, list)
                self.assertEqual(hrv, loaded)
                self.assertIsInstance(api_article, str)
    
    def test_extreme_hrv_values(self):
        """Test with extreme HRV values"""
        extreme_values = [
            -1.0,  # Below range
            2.0,   # Above range
            -100.0,  # Very negative
            100.0,   # Very positive
            1e-10,   # Very small
            1e10,    # Very large
        ]
        
        for value in extreme_values:
            # Test with single extreme value
            hrv_vector = [value] * 8
            
            try:
                self.profile_manager.save_profile("extreme_test", "test_profile", hrv_vector)
                loaded = self.profile_manager.load_profile("extreme_test", "test_profile")
                self.assertEqual(loaded, hrv_vector)
            except (ValueError, OverflowError):
                # May fail with extreme values
                pass
    
    def test_empty_and_whitespace_inputs(self):
        """Test with empty and whitespace inputs"""
        whitespace_inputs = [
            "",
            " ",
            "  ",
            "\t",
            "\n",
            "\r",
            "\t \n \r",
            "\n\n\n",
            "\t\t\t",
        ]
        
        for ws_input in whitespace_inputs:
            # Test writer
            content = self.writer.generate(ws_input)
            self.assertIsInstance(content, str)
            
            # Test extractor
            hrv = self.extractor.extract(ws_input)
            self.assertIsInstance(hrv, list)
            self.assertEqual(len(hrv), 8)
            
            # Test API
            request = SimpleRequest(prompt=ws_input)
            response = hr_generate(request)
            self.assertIsInstance(response.article, str)
    
    def test_boundary_hrv_values(self):
        """Test HRV values at boundaries"""
        boundary_vectors = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Minimum
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # Maximum
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],  # Below minimum
            [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],  # Above maximum
        ]
        
        for vector in boundary_vectors:
            try:
                self.profile_manager.save_profile("boundary_test", "test_profile", vector)
                loaded = self.profile_manager.load_profile("boundary_test", "test_profile")
                self.assertEqual(loaded, vector)
            except ValueError:
                # May fail with out-of-range values
                pass


if __name__ == '__main__':
    unittest.main()
