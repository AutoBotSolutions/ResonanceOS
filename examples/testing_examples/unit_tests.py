#!/usr/bin/env python3
"""
Unit Testing Examples

This example demonstrates comprehensive unit testing patterns for ResonanceOS v6,
including test structure, assertions, mocking, and best practices.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from typing import List, Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.api.hr_server import SimpleRequest, hr_generate


class TestHRVExtractor(unittest.TestCase):
    """Test cases for HRVExtractor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = HRVExtractor()
        self.sample_text = "This is a sample text for testing HRV extraction."
        self.empty_text = ""
        self.long_text = "This is a very long text that contains multiple sentences. " * 10
    
    def test_extract_basic(self):
        """Test basic HRV extraction"""
        print("🧪 Testing basic HRV extraction...")
        
        result = self.extractor.extract(self.sample_text)
        
        # Assertions
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 8, "HRV vector should have 8 dimensions")
        
        # Check value ranges
        for i, value in enumerate(result):
            self.assertIsInstance(value, (int, float), f"Dimension {i} should be numeric")
            self.assertTrue(0.0 <= value <= 1.0, f"Dimension {i} should be between 0.0 and 1.0")
        
        print(f"✅ Basic extraction test passed - HRV: {[round(x, 3) for x in result]}")
    
    def test_extract_empty_text(self):
        """Test HRV extraction with empty text"""
        print("🧪 Testing empty text handling...")
        
        result = self.extractor.extract(self.empty_text)
        
        # Should still return 8 dimensions
        self.assertEqual(len(result), 8)
        
        # Values should be reasonable (likely low for empty text)
        for value in result:
            self.assertIsInstance(value, (int, float))
            self.assertTrue(0.0 <= value <= 1.0)
        
        print("✅ Empty text test passed")
    
    def test_extract_long_text(self):
        """Test HRV extraction with long text"""
        print("🧪 Testing long text handling...")
        
        result = self.extractor.extract(self.long_text)
        
        self.assertEqual(len(result), 8)
        self.assertIsInstance(result, list)
        
        print(f"✅ Long text test passed - HRV: {[round(x, 3) for x in result]}")
    
    def test_extract_consistency(self):
        """Test that extraction is consistent for same input"""
        print("🧪 Testing extraction consistency...")
        
        result1 = self.extractor.extract(self.sample_text)
        result2 = self.extractor.extract(self.sample_text)
        
        # Results should be identical
        self.assertEqual(result1, result2, "Extraction should be consistent")
        
        print("✅ Consistency test passed")
    
    def test_extract_different_inputs(self):
        """Test extraction with different types of text"""
        print("🧪 Testing different text types...")
        
        texts = [
            "Formal business communication with professional tone.",
            "Exciting! Amazing! Wonderful! Lots of emotion here!",
            "Question? What about curiosity? How does this work?",
            "Once upon a time, in a magical forest far away..."
        ]
        
        for text in texts:
            result = self.extractor.extract(text)
            self.assertEqual(len(result), 8)
            self.assertIsInstance(result, list)
        
        print("✅ Different text types test passed")


class TestHumanResonantWriter(unittest.TestCase):
    """Test cases for HumanResonantWriter class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.writer = HumanResonantWriter()
        self.sample_prompt = "The future of artificial intelligence"
    
    def test_generate_basic(self):
        """Test basic content generation"""
        print("🧪 Testing basic content generation...")
        
        result = self.writer.generate(self.sample_prompt)
        
        # Assertions
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0, "Generated content should not be empty")
        self.assertIn(self.sample_prompt.lower(), result.lower(), 
                     "Generated content should reference the prompt")
        
        print(f"✅ Basic generation test passed - Length: {len(result)} chars")
    
    def test_generate_empty_prompt(self):
        """Test generation with empty prompt"""
        print("🧪 Testing empty prompt handling...")
        
        result = self.writer.generate("")
        
        self.assertIsInstance(result, str)
        # Should still generate some content even with empty prompt
        
        print("✅ Empty prompt test passed")
    
    def test_generate_consistency(self):
        """Test that generation is reasonable (not necessarily identical)"""
        print("🧪 Testing generation reasonableness...")
        
        result1 = self.writer.generate(self.sample_prompt)
        result2 = self.writer.generate(self.sample_prompt)
        
        # Both should be strings with reasonable length
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)
        self.assertGreater(len(result1), 10)
        self.assertGreater(len(result2), 10)
        
        print("✅ Generation reasonableness test passed")
    
    @patch('resonance_os.generation.human_resonant_writer.HumanResonantWriter._generate_internal')
    def test_generate_with_mock(self, mock_generate):
        """Test generation with mocked internal method"""
        print("🧪 Testing with mocked generation...")
        
        # Set up mock
        mock_generate.return_value = "Mocked generated content"
        
        result = self.writer.generate(self.sample_prompt)
        
        # Verify mock was called
        mock_generate.assert_called_once_with(self.sample_prompt)
        self.assertEqual(result, "Mocked generated content")
        
        print("✅ Mock generation test passed")


class TestHRVProfileManager(unittest.TestCase):
    """Test cases for HRVProfileManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path("/tmp/test_profiles")
        self.temp_dir.mkdir(exist_ok=True)
        self.manager = HRVProfileManager(str(self.temp_dir))
        
        self.tenant = "test_tenant"
        self.profile_name = "test_profile"
        self.hrv_vector = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_profile(self):
        """Test saving and loading profiles"""
        print("🧪 Testing save and load profile...")
        
        # Save profile
        self.manager.save_profile(self.tenant, self.profile_name, self.hrv_vector)
        
        # Load profile
        loaded_vector = self.manager.load_profile(self.tenant, self.profile_name)
        
        # Verify
        self.assertEqual(loaded_vector, self.hrv_vector)
        
        print("✅ Save and load test passed")
    
    def test_load_nonexistent_profile(self):
        """Test loading a profile that doesn't exist"""
        print("🧪 Testing nonexistent profile handling...")
        
        with self.assertRaises(FileNotFoundError):
            self.manager.load_profile(self.tenant, "nonexistent_profile")
        
        print("✅ Nonexistent profile test passed")
    
    def test_list_profiles(self):
        """Test listing profiles"""
        print("🧪 Testing profile listing...")
        
        # Save some profiles
        self.manager.save_profile(self.tenant, "profile1", [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
        self.manager.save_profile(self.tenant, "profile2", [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])
        
        # List profiles
        profiles = self.manager.list_profiles(self.tenant)
        
        # Verify
        self.assertIn("profile1", profiles)
        self.assertIn("profile2", profiles)
        self.assertEqual(len(profiles), 2)
        
        print("✅ Profile listing test passed")
    
    def test_invalid_hrv_vector(self):
        """Test handling of invalid HRV vectors"""
        print("🧪 Testing invalid HRV vector handling...")
        
        # Test wrong length
        with self.assertRaises(ValueError):
            self.manager.save_profile(self.tenant, "invalid_length", [0.5, 0.5, 0.5])
        
        # Test invalid values
        with self.assertRaises(ValueError):
            self.manager.save_profile(self.tenant, "invalid_values", [0.5, 0.5, 2.0, 0.5, 0.5, 0.5, 0.5, 0.5])
        
        print("✅ Invalid HRV vector test passed")


class TestAPIIntegration(unittest.TestCase):
    """Test cases for API integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_request = SimpleRequest(
            prompt="Test prompt for API",
            tenant="test_tenant",
            profile_name="test_profile"
        )
    
    def test_simple_request_creation(self):
        """Test SimpleRequest creation"""
        print("🧪 Testing SimpleRequest creation...")
        
        self.assertEqual(self.sample_request.prompt, "Test prompt for API")
        self.assertEqual(self.sample_request.tenant, "test_tenant")
        self.assertEqual(self.sample_request.profile_name, "test_profile")
        
        print("✅ SimpleRequest creation test passed")
    
    def test_simple_request_defaults(self):
        """Test SimpleRequest default values"""
        print("🧪 Testing SimpleRequest defaults...")
        
        request = SimpleRequest(prompt="Test prompt")
        
        self.assertEqual(request.prompt, "Test prompt")
        self.assertIsNone(request.tenant)
        self.assertIsNone(request.profile_name)
        
        print("✅ SimpleRequest defaults test passed")
    
    @patch('resonance_os.generation.human_resonant_writer.HumanResonantWriter.generate')
    def test_hr_generate_with_mock(self, mock_generate):
        """Test hr_generate function with mocked writer"""
        print("🧪 Testing hr_generate with mock...")
        
        # Set up mock
        mock_generate.return_value = "Generated content for testing"
        
        # Call function
        result = hr_generate(self.sample_request)
        
        # Verify
        self.assertIsNotNone(result)
        self.assertEqual(result.article, "Generated content for testing")
        mock_generate.assert_called_once_with(self.sample_request.prompt)
        
        print("✅ hr_generate mock test passed")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = HRVExtractor()
        self.writer = HumanResonantWriter()
    
    def test_unicode_text(self):
        """Test handling of unicode text"""
        print("🧪 Testing unicode text handling...")
        
        unicode_text = "测试中文文本 🚀 ñiño café résumé"
        
        # Should not raise an exception
        result = self.extractor.extract(unicode_text)
        self.assertEqual(len(result), 8)
        
        print("✅ Unicode text test passed")
    
    def test_very_long_text(self):
        """Test handling of very long text"""
        print("🧪 Testing very long text...")
        
        long_text = "This is a sentence. " * 1000  # Very long text
        
        # Should handle without issues
        result = self.extractor.extract(long_text)
        self.assertEqual(len(result), 8)
        
        print("✅ Very long text test passed")
    
    def test_special_characters(self):
        """Test handling of special characters"""
        print("🧪 Testing special characters...")
        
        special_text = "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        result = self.extractor.extract(special_text)
        self.assertEqual(len(result), 8)
        
        print("✅ Special characters test passed")
    
    def test_numeric_text(self):
        """Test handling of numeric-only text"""
        print("🧪 Testing numeric text...")
        
        numeric_text = "123 456 789 1000 2000 3000"
        
        result = self.extractor.extract(numeric_text)
        self.assertEqual(len(result), 8)
        
        print("✅ Numeric text test passed")


class TestPerformance(unittest.TestCase):
    """Performance-related tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = HRVExtractor()
        self.writer = HumanResonantWriter()
    
    def test_extraction_performance(self):
        """Test HRV extraction performance"""
        print("🧪 Testing extraction performance...")
        
        import time
        
        test_text = "This is a performance test text. " * 50
        
        # Measure time
        start_time = time.time()
        result = self.extractor.extract(test_text)
        end_time = time.time()
        
        extraction_time = end_time - start_time
        
        # Should complete within reasonable time (adjust threshold as needed)
        self.assertLess(extraction_time, 1.0, "Extraction should complete within 1 second")
        self.assertEqual(len(result), 8)
        
        print(f"✅ Extraction performance test passed - Time: {extraction_time:.3f}s")
    
    def test_generation_performance(self):
        """Test content generation performance"""
        print("🧪 Testing generation performance...")
        
        import time
        
        prompt = "Performance test prompt"
        
        # Measure time
        start_time = time.time()
        result = self.writer.generate(prompt)
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Should complete within reasonable time (adjust threshold as needed)
        self.assertLess(generation_time, 5.0, "Generation should complete within 5 seconds")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        
        print(f"✅ Generation performance test passed - Time: {generation_time:.3f}s")


class TestIntegration(unittest.TestCase):
    """Integration tests that test multiple components together"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = HRVExtractor()
        self.writer = HumanResonantWriter()
        self.temp_dir = Path("/tmp/test_integration")
        self.temp_dir.mkdir(exist_ok=True)
        self.manager = HRVProfileManager(str(self.temp_dir))
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """Test complete workflow: generate -> extract -> save -> load"""
        print("🧪 Testing full workflow...")
        
        # 1. Generate content
        prompt = "Integration test prompt"
        content = self.writer.generate(prompt)
        
        # 2. Extract HRV
        hrv_vector = self.extractor.extract(content)
        
        # 3. Save as profile
        self.manager.save_profile("integration_test", "generated_profile", hrv_vector)
        
        # 4. Load profile
        loaded_vector = self.manager.load_profile("integration_test", "generated_profile")
        
        # Verify
        self.assertEqual(hrv_vector, loaded_vector)
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)
        self.assertEqual(len(hrv_vector), 8)
        
        print("✅ Full workflow test passed")
    
    def test_profile_based_generation(self):
        """Test generation with profile-based approach"""
        print("🧪 Testing profile-based generation...")
        
        # Create a profile
        profile_vector = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
        self.manager.save_profile("test", "creative_profile", profile_vector)
        
        # Generate content
        content = self.writer.generate("Creative writing test")
        
        # Extract HRV from generated content
        extracted_hrv = self.extractor.extract(content)
        
        # Verify
        self.assertIsInstance(content, str)
        self.assertEqual(len(extracted_hrv), 8)
        
        print("✅ Profile-based generation test passed")


def run_test_suite():
    """Run the complete test suite"""
    print("🧪 Running ResonanceOS v6 Unit Test Suite")
    print("=" * 60)
    print()
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestHRVExtractor,
        TestHumanResonantWriter,
        TestHRVProfileManager,
        TestAPIIntegration,
        TestEdgeCases,
        TestPerformance,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Suite Summary:")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
    
    return result


def create_custom_test_example():
    """Example of creating a custom test"""
    print("\n🎯 Creating Custom Test Example")
    print("=" * 50)
    print()
    
    class CustomHRVTest(unittest.TestCase):
        """Custom test example"""
        
        def test_custom_hrv_calculation(self):
            """Custom test for HRV calculation logic"""
            print("🧪 Running custom HRV calculation test...")
            
            extractor = HRVExtractor()
            test_text = "This is a custom test for HRV calculation."
            
            result = extractor.extract(test_text)
            
            # Custom assertions
            self.assertEqual(len(result), 8)
            self.assertTrue(all(0.0 <= x <= 1.0 for x in result))
            
            # Custom logic test
            avg_score = sum(result) / len(result)
            self.assertGreater(avg_score, 0.0, "Average score should be positive")
            
            print("✅ Custom HRV calculation test passed")
        
        def test_custom_performance_metric(self):
            """Custom performance test"""
            print("🧪 Running custom performance test...")
            
            import time
            extractor = HRVExtractor()
            
            # Test multiple extractions
            times = []
            for _ in range(10):
                start = time.time()
                extractor.extract("Performance test text")
                end = time.time()
                times.append(end - start)
            
            avg_time = sum(times) / len(times)
            max_time = max(times)
            
            # Custom performance assertions
            self.assertLess(avg_time, 0.1, "Average time should be less than 0.1s")
            self.assertLess(max_time, 0.2, "Max time should be less than 0.2s")
            
            print(f"✅ Custom performance test passed - Avg: {avg_time:.3f}s, Max: {max_time:.3f}s")
    
    # Run custom test
    suite = unittest.TestLoader().loadTestsFromTestCase(CustomHRVTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def main():
    """Main function to run all examples"""
    print("🎯 ResonanceOS v6 - Unit Testing Examples")
    print("=" * 60)
    print("This example demonstrates comprehensive unit testing patterns.")
    print("You'll learn how to:")
    print("- Structure unit tests effectively")
    print("- Test different components")
    print("- Use mocking and patches")
    print("- Handle edge cases")
    print("- Test performance")
    print("- Create integration tests")
    print("- Build custom tests")
    print()
    
    try:
        # Run main test suite
        main_result = run_test_suite()
        
        # Run custom test example
        custom_result = create_custom_test_example()
        
        print("\n🎉 Unit Testing Examples Completed!")
        print("\nKey Learnings:")
        print("- ✅ Structured test organization")
        print("- ✅ Comprehensive component testing")
        print("- ✅ Effective use of mocking")
        print("- ✅ Edge case handling")
        print("- ✅ Performance testing")
        print("- ✅ Integration testing")
        print("- ✅ Custom test creation")
        print("\nBest Practices Demonstrated:")
        print("- Use descriptive test names")
        print("- Test both success and failure cases")
        print("- Use setUp/tearDown for fixtures")
        print("- Mock external dependencies")
        print("- Assert specific conditions")
        print("- Measure performance when relevant")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")


if __name__ == "__main__":
    main()
