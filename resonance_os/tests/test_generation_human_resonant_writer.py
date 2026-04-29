"""
Test Human Resonant Writer Module
"""

import unittest
from resonance_os.generation.human_resonant_writer import HumanResonantWriter


class TestHumanResonantWriter(unittest.TestCase):
    """Test human resonant writer functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.writer = HumanResonantWriter()
    
    def test_writer_initialization(self):
        """Test that HumanResonantWriter initializes correctly"""
        self.assertIsInstance(self.writer, HumanResonantWriter)
        self.assertIsNotNone(self.writer.planner)
        self.assertIsNotNone(self.writer.sentence_layer)
        self.assertIsNotNone(self.writer.refiner)
        self.assertIsNotNone(self.writer.hrf)
    
    def test_generate_basic(self):
        """Test basic content generation"""
        prompt = "Test prompt for generation"
        result = self.writer.generate(prompt)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_generate_empty_prompt(self):
        """Test generation with empty prompt"""
        prompt = ""
        result = self.writer.generate(prompt)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_generate_long_prompt(self):
        """Test generation with long prompt"""
        prompt = "This is a very long prompt " * 100
        result = self.writer.generate(prompt)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_generate_special_characters(self):
        """Test generation with special characters"""
        prompt = "Test with @#$%^&*() special characters!"
        result = self.writer.generate(prompt)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        # Should contain the special characters
        self.assertIn("@#$%^&*()", result)
    
    def test_generate_unicode(self):
        """Test generation with unicode characters"""
        prompt = "Test with café naïve résumé unicode"
        result = self.writer.generate(prompt)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        # Should contain unicode characters
        self.assertIn("café", result)
    
    def test_generate_structure(self):
        """Test that generated content has expected structure"""
        prompt = "Test prompt for structure"
        result = self.writer.generate(prompt)
        
        self.assertIsInstance(result, str)
        
        # Should contain refined sentences
        self.assertIn("[Refined with HRV feedback", result)
        
        # Should contain paragraph outlines
        self.assertIn("Paragraph outline", result)
        
        # Should contain the original prompt
        self.assertIn(prompt, result)
    
    def test_generate_multiple_paragraphs(self):
        """Test that generation produces multiple paragraphs"""
        prompt = "Test prompt for multiple paragraphs"
        result = self.writer.generate(prompt)
        
        self.assertIsInstance(result, str)
        
        # Should have multiple paragraph outlines
        outline_count = result.count("Paragraph outline")
        self.assertGreaterEqual(outline_count, 3)  # Default is 3 paragraphs
    
    def test_generate_consistency(self):
        """Test that generation is consistent for same input"""
        prompt = "Test prompt for consistency"
        
        result1 = self.writer.generate(prompt)
        result2 = self.writer.generate(prompt)
        
        # Results should be similar (though HRV values may differ due to randomness)
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)
        self.assertGreater(len(result1), 0)
        self.assertGreater(len(result2), 0)
        
        # Both should contain the prompt
        self.assertIn(prompt, result1)
        self.assertIn(prompt, result2)
    
    def test_generate_multiple_calls(self):
        """Test multiple calls to generate"""
        prompt = "Test prompt for multiple calls"
        
        for _ in range(5):
            result = self.writer.generate(prompt)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            self.assertIn(prompt, result)
    
    def test_generate_different_prompts(self):
        """Test generation with different prompts"""
        prompts = [
            "Short",
            "This is a medium length prompt",
            "This is a much longer prompt with more details and specific instructions for content generation",
            "Test with numbers 123 and symbols @#$",
            "Test with unicode café naïve résumé"
        ]
        
        for prompt in prompts:
            result = self.writer.generate(prompt)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            self.assertIn(prompt, result)
    
    def test_generate_none_prompt(self):
        """Test generation with None prompt"""
        try:
            result = self.writer.generate(None)
            self.assertIsInstance(result, str)
        except (TypeError, AttributeError):
            # Expected behavior for None input
            pass
    
    def test_generate_numeric_prompt(self):
        """Test generation with numeric prompt"""
        try:
            result = self.writer.generate(123)
            self.assertIsInstance(result, str)
        except (TypeError, ValueError):
            # Expected behavior for numeric input
            pass
    
    def test_generate_content_quality(self):
        """Test quality of generated content"""
        prompt = "Test prompt for quality"
        result = self.writer.generate(prompt)
        
        # Should not be empty
        self.assertGreater(len(result), 0)
        
        # Should contain meaningful content
        self.assertNotEqual(result.strip(), "")
        
        # Should contain HRV feedback indicators
        self.assertIn("HRV feedback", result)
        
        # Should contain paragraph structure
        self.assertIn("Paragraph outline", result)
    
    def test_generate_feedback_integration(self):
        """Test that HRF feedback is integrated"""
        prompt = "Test prompt for feedback integration"
        result = self.writer.generate(prompt)
        
        # Should contain feedback refinement indicators
        feedback_count = result.count("HRV feedback")
        self.assertGreater(feedback_count, 0)
        
        # Each paragraph should have refined sentences
        refined_count = result.count("[Refined with HRV feedback")
        self.assertGreater(refined_count, 0)
    
    def test_generate_sentence_structure(self):
        """Test sentence structure in generated content"""
        prompt = "Test prompt for sentence structure"
        result = self.writer.generate(prompt)
        
        # Should contain sentence-like structures
        sentences = result.split('.')
        self.assertGreater(len(sentences), 1)
        
        # Should have varied sentence lengths (due to HRV targeting)
        sentence_lengths = [len(s.strip()) for s in sentences if s.strip()]
        if len(sentence_lengths) > 1:
            # Should have some variance in sentence lengths
            length_variance = max(sentence_lengths) - min(sentence_lengths)
            self.assertGreater(length_variance, 0)
    
    def test_generate_hrv_targeting(self):
        """Test that HRV targeting is evident in generation"""
        prompt = "Test prompt for HRV targeting"
        result = self.writer.generate(prompt)
        
        # Should contain HRV-related content
        self.assertIn("valence", result.lower())
        
        # Should have HRV feedback values
        import re
        hrv_values = re.findall(r'\[Refined with HRV feedback [\d.]+\]', result)
        self.assertGreater(len(hrv_values), 0)
    
    def test_generate_return_type(self):
        """Test that return type is correct"""
        prompt = "Test prompt for type checking"
        result = self.writer.generate(prompt)
        
        self.assertIsInstance(result, str)
    
    def test_generate_performance(self):
        """Test generation performance"""
        import time
        
        prompt = "Test prompt for performance"
        start_time = time.time()
        
        # Generate multiple times to check performance
        for _ in range(10):
            result = self.writer.generate(prompt)
            self.assertIsInstance(result, str)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should complete in reasonable time (adjust threshold as needed)
        self.assertLess(total_time, 10.0)  # 10 seconds for 10 generations
    
    def test_writer_components_integration(self):
        """Test that all writer components are properly integrated"""
        # Check that all components exist
        self.assertIsNotNone(self.writer.planner)
        self.assertIsNotNone(self.writer.sentence_layer)
        self.assertIsNotNone(self.writer.refiner)
        self.assertIsNotNone(self.writer.hrf)
        
        # Check that components are of correct type
        from resonance_os.generation.planner_layer import PlannerLayer
        from resonance_os.generation.sentence_layer import SentenceLayer
        from resonance_os.generation.refiner_layer import RefinerLayer
        from resonance_os.generation.hrf_model import HRFModel
        
        self.assertIsInstance(self.writer.planner, PlannerLayer)
        self.assertIsInstance(self.writer.sentence_layer, SentenceLayer)
        self.assertIsInstance(self.writer.refiner, RefinerLayer)
        self.assertIsInstance(self.writer.hrf, HRFModel)


if __name__ == '__main__':
    unittest.main()
