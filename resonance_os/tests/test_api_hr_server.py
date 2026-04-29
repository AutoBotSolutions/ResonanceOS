"""
Test HR Server API Module
"""

import unittest
from resonance_os.api.hr_server import SimpleRequest, SimpleResponse, hr_generate, app


class TestHRServerAPI(unittest.TestCase):
    """Test HR server API functionality"""
    
    def test_simple_request_initialization(self):
        """Test SimpleRequest initialization"""
        # Test with all parameters
        request = SimpleRequest(prompt="Test prompt", tenant="test_tenant", profile_name="test_profile")
        
        self.assertEqual(request.prompt, "Test prompt")
        self.assertEqual(request.tenant, "test_tenant")
        self.assertEqual(request.profile_name, "test_profile")
        
        # Test with default parameters
        request_default = SimpleRequest(prompt="Test prompt")
        
        self.assertEqual(request_default.prompt, "Test prompt")
        self.assertIsNone(request_default.tenant)
        self.assertIsNone(request_default.profile_name)
    
    def test_simple_request_attributes(self):
        """Test SimpleRequest attributes"""
        request = SimpleRequest(prompt="Test prompt")
        
        self.assertTrue(hasattr(request, 'prompt'))
        self.assertTrue(hasattr(request, 'tenant'))
        self.assertTrue(hasattr(request, 'profile_name'))
        
        self.assertIsInstance(request.prompt, str)
        # tenant and profile_name can be None
        self.assertTrue(request.tenant is None or isinstance(request.tenant, str))
        self.assertTrue(request.profile_name is None or isinstance(request.profile_name, str))
    
    def test_simple_response_initialization(self):
        """Test SimpleResponse initialization"""
        article = "Generated article content"
        hrv_feedback = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        response = SimpleResponse(article=article, hrv_feedback=hrv_feedback)
        
        self.assertEqual(response.article, article)
        self.assertEqual(response.hrv_feedback, hrv_feedback)
    
    def test_simple_response_attributes(self):
        """Test SimpleResponse attributes"""
        article = "Test article"
        hrv_feedback = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        response = SimpleResponse(article=article, hrv_feedback=hrv_feedback)
        
        self.assertTrue(hasattr(response, 'article'))
        self.assertTrue(hasattr(response, 'hrv_feedback'))
        
        self.assertIsInstance(response.article, str)
        self.assertIsInstance(response.hrv_feedback, list)
        self.assertEqual(len(response.hrv_feedback), 8)
    
    def test_hr_generate_basic(self):
        """Test basic hr_generate function"""
        request = SimpleRequest(prompt="Test prompt")
        response = hr_generate(request)
        
        self.assertIsInstance(response, SimpleResponse)
        self.assertIsInstance(response.article, str)
        self.assertIsInstance(response.hrv_feedback, list)
        self.assertEqual(len(response.hrv_feedback), 8)
    
    def test_hr_generate_different_prompts(self):
        """Test hr_generate with different prompts"""
        prompts = [
            "Short prompt",
            "This is a longer prompt with more content",
            "Test with special characters @#$%^&*()",
            "Test with unicode café naïve résumé",
            ""  # Empty prompt
        ]
        
        for prompt in prompts:
            request = SimpleRequest(prompt=prompt)
            response = hr_generate(request)
            
            self.assertIsInstance(response, SimpleResponse)
            self.assertIsInstance(response.article, str)
            self.assertIsInstance(response.hrv_feedback, list)
            self.assertEqual(len(response.hrv_feedback), 8)
            
            # Article should contain the prompt (if not empty)
            if prompt:
                self.assertIn(prompt, response.article)
    
    def test_hr_generate_with_tenant_and_profile(self):
        """Test hr_generate with tenant and profile"""
        request = SimpleRequest(
            prompt="Test prompt",
            tenant="test_tenant",
            profile_name="test_profile"
        )
        
        response = hr_generate(request)
        
        self.assertIsInstance(response, SimpleResponse)
        self.assertIsInstance(response.article, str)
        self.assertIsInstance(response.hrv_feedback, list)
        self.assertEqual(len(response.hrv_feedback), 8)
    
    def test_hr_generate_hrv_feedback_ranges(self):
        """Test that HRV feedback is in valid ranges"""
        request = SimpleRequest(prompt="Test prompt")
        response = hr_generate(request)
        
        self.assertIsInstance(response.hrv_feedback, list)
        self.assertEqual(len(response.hrv_feedback), 8)
        
        # All HRV values should be between 0 and 1 (random generation)
        for value in response.hrv_feedback:
            self.assertIsInstance(value, (int, float))
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)
    
    def test_hr_generate_consistency(self):
        """Test hr_generate consistency"""
        request = SimpleRequest(prompt="Test prompt for consistency")
        
        response1 = hr_generate(request)
        response2 = hr_generate(request)
        
        # Both should be valid responses
        self.assertIsInstance(response1, SimpleResponse)
        self.assertIsInstance(response2, SimpleResponse)
        
        # Articles should be similar (though HRV feedback may differ due to randomness)
        self.assertIsInstance(response1.article, str)
        self.assertIsInstance(response2.article, str)
        self.assertIn(request.prompt, response1.article)
        self.assertIn(request.prompt, response2.article)
    
    def test_hr_generate_multiple_calls(self):
        """Test multiple calls to hr_generate"""
        request = SimpleRequest(prompt="Test prompt for multiple calls")
        
        for _ in range(10):
            response = hr_generate(request)
            
            self.assertIsInstance(response, SimpleResponse)
            self.assertIsInstance(response.article, str)
            self.assertIsInstance(response.hrv_feedback, list)
            self.assertEqual(len(response.hrv_feedback), 8)
    
    def test_app_initialization(self):
        """Test app initialization"""
        self.assertIsNotNone(app)
        self.assertTrue(hasattr(app, 'routes'))
        self.assertIsInstance(app.routes, dict)
    
    def test_app_routes(self):
        """Test app routes"""
        self.assertIn("/hr_generate", app.routes)
        self.assertEqual(len(app.routes), 1)
    
    def test_app_route_function(self):
        """Test that app route function is callable"""
        route_function = app.routes["/hr_generate"]
        self.assertTrue(callable(route_function))
    
    def test_hr_generate_none_prompt(self):
        """Test hr_generate with None prompt"""
        try:
            request = SimpleRequest(prompt=None)
            response = hr_generate(request)
            
            self.assertIsInstance(response, SimpleResponse)
            self.assertIsInstance(response.article, str)
            self.assertIsInstance(response.hrv_feedback, list)
        except (TypeError, AttributeError):
            # Expected behavior for None input
            pass
    
    def test_hr_generate_numeric_prompt(self):
        """Test hr_generate with numeric prompt"""
        try:
            request = SimpleRequest(prompt=123)
            response = hr_generate(request)
            
            self.assertIsInstance(response, SimpleResponse)
            self.assertIsInstance(response.article, str)
            self.assertIsInstance(response.hrv_feedback, list)
        except (TypeError, ValueError):
            # Expected behavior for numeric input
            pass
    
    def test_hr_generate_long_prompt(self):
        """Test hr_generate with very long prompt"""
        long_prompt = "This is a very long prompt. " * 1000
        request = SimpleRequest(prompt=long_prompt)
        
        response = hr_generate(request)
        
        self.assertIsInstance(response, SimpleResponse)
        self.assertIsInstance(response.article, str)
        self.assertIsInstance(response.hrv_feedback, list)
        self.assertEqual(len(response.hrv_feedback), 8)
        
        # Should handle long prompts
        self.assertIn(long_prompt, response.article)
    
    def test_hr_generate_special_characters(self):
        """Test hr_generate with special characters"""
        special_prompt = "Test with @#$%^&*() special characters!"
        request = SimpleRequest(prompt=special_prompt)
        
        response = hr_generate(request)
        
        self.assertIsInstance(response, SimpleResponse)
        self.assertIsInstance(response.article, str)
        self.assertIsInstance(response.hrv_feedback, list)
        self.assertEqual(len(response.hrv_feedback), 8)
        
        # Should handle special characters
        self.assertIn("@#$%^&*()", response.article)
    
    def test_hr_generate_unicode(self):
        """Test hr_generate with unicode characters"""
        unicode_prompt = "Test with café naïve résumé unicode"
        request = SimpleRequest(prompt=unicode_prompt)
        
        response = hr_generate(request)
        
        self.assertIsInstance(response, SimpleResponse)
        self.assertIsInstance(response.article, str)
        self.assertIsInstance(response.hrv_feedback, list)
        self.assertEqual(len(response.hrv_feedback), 8)
        
        # Should handle unicode characters
        self.assertIn("café", response.article)
    
    def test_hr_generate_performance(self):
        """Test hr_generate performance"""
        import time
        
        request = SimpleRequest(prompt="Test prompt for performance")
        
        start_time = time.time()
        
        # Generate multiple times to check performance
        for _ in range(10):
            response = hr_generate(request)
            self.assertIsInstance(response, SimpleResponse)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should complete in reasonable time
        self.assertLess(total_time, 10.0)  # 10 seconds for 10 generations
    
    def test_api_integration(self):
        """Test API integration with other components"""
        # Test that the API properly integrates with the writer
        request = SimpleRequest(prompt="Integration test prompt")
        response = hr_generate(request)
        
        # Response should have structure from HumanResonantWriter
        self.assertIn("Paragraph outline", response.article)
        self.assertIn("HRV feedback", response.article)
        
        # HRV feedback should be properly formatted
        self.assertEqual(len(response.hrv_feedback), 8)
        self.assertTrue(all(isinstance(x, (int, float)) for x in response.hrv_feedback))


if __name__ == '__main__':
    unittest.main()
