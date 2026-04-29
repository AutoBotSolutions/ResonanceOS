"""
Test Refiner Layer Module
"""

import unittest
from resonance_os.generation.refiner_layer import RefinerLayer


class TestRefinerLayer(unittest.TestCase):
    """Test refiner layer functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.refiner = RefinerLayer()
    
    def test_refiner_initialization(self):
        """Test that RefinerLayer initializes correctly"""
        self.assertIsInstance(self.refiner, RefinerLayer)
    
    def test_refine_basic_sentence(self):
        """Test basic sentence refinement"""
        sentence = "This is a test sentence."
        hrv_feedback = 0.5
        
        refined = self.refiner.refine(sentence, hrv_feedback)
        
        self.assertIsInstance(refined, str)
        self.assertGreater(len(refined), len(sentence))
        self.assertIn(sentence, refined)
        self.assertIn(str(hrv_feedback), refined)
    
    def test_refine_different_feedback_values(self):
        """Test refinement with different feedback values"""
        sentence = "Test sentence"
        feedback_values = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        for feedback in feedback_values:
            refined = self.refiner.refine(sentence, feedback)
            self.assertIsInstance(refined, str)
            self.assertIn(sentence, refined)
            self.assertIn(str(feedback), refined)
    
    def test_refine_empty_sentence(self):
        """Test refinement of empty sentence"""
        sentence = ""
        hrv_feedback = 0.5
        
        refined = self.refiner.refine(sentence, hrv_feedback)
        
        self.assertIsInstance(refined, str)
        self.assertIn(str(hrv_feedback), refined)
    
    def test_refine_long_sentence(self):
        """Test refinement of long sentence"""
        sentence = "This is a very long sentence " * 100
        hrv_feedback = 0.5
        
        refined = self.refiner.refine(sentence, hrv_feedback)
        
        self.assertIsInstance(refined, str)
        self.assertGreater(len(refined), len(sentence))
        self.assertIn(sentence, refined)
    
    def test_refine_special_characters(self):
        """Test refinement with special characters"""
        sentence = "Test with @#$%^&*() special characters!"
        hrv_feedback = 0.5
        
        refined = self.refiner.refine(sentence, hrv_feedback)
        
        self.assertIsInstance(refined, str)
        self.assertIn("@#$%^&*()", refined)
        self.assertIn(str(hrv_feedback), refined)
    
    def test_refine_unicode_characters(self):
        """Test refinement with unicode characters"""
        sentence = "Test with café naïve résumé unicode"
        hrv_feedback = 0.5
        
        refined = self.refiner.refine(sentence, hrv_feedback)
        
        self.assertIsInstance(refined, str)
        self.assertIn("café", refined)
        self.assertIn(str(hrv_feedback), refined)
    
    def test_refine_extreme_feedback_values(self):
        """Test refinement with extreme feedback values"""
        sentence = "Test sentence"
        extreme_values = [-1.0, -0.5, 2.0, 1.5]
        
        for feedback in extreme_values:
            refined = self.refiner.refine(sentence, feedback)
            self.assertIsInstance(refined, str)
            self.assertIn(sentence, refined)
            self.assertIn(str(feedback), refined)
    
    def test_refine_decimal_feedback(self):
        """Test refinement with decimal feedback values"""
        sentence = "Test sentence"
        decimal_values = [0.123, 0.456, 0.789, 0.999]
        
        for feedback in decimal_values:
            refined = self.refiner.refine(sentence, feedback)
            self.assertIsInstance(refined, str)
            self.assertIn(sentence, refined)
            # Check for rounded value (2 decimal places)
            rounded_feedback = round(feedback, 2)
            self.assertIn(str(rounded_feedback), refined)
    
    def test_refine_none_inputs(self):
        """Test refinement with None inputs"""
        # Test with None sentence
        try:
            refined = self.refiner.refine(None, 0.5)
            self.assertIsInstance(refined, str)
        except (TypeError, AttributeError):
            # Expected behavior for None input
            pass
        
        # Test with None feedback
        try:
            refined = self.refiner.refine("Test sentence", None)
            self.assertIsInstance(refined, str)
        except (TypeError, ValueError):
            # Expected behavior for None input
            pass
    
    def test_refine_non_string_sentence(self):
        """Test refinement with non-string sentence"""
        non_string_inputs = [123, 45.67, True, [1, 2, 3], {"key": "value"}]
        
        for input_val in non_string_inputs:
            try:
                refined = self.refiner.refine(input_val, 0.5)
                self.assertIsInstance(refined, str)
            except (TypeError, ValueError):
                # Expected behavior for non-string input
                pass
    
    def test_refine_non_numeric_feedback(self):
        """Test refinement with non-numeric feedback"""
        sentence = "Test sentence"
        non_numeric_feedback = ["not_numeric", True, None, [1, 2, 3]]
        
        for feedback in non_numeric_feedback:
            try:
                refined = self.refiner.refine(sentence, feedback)
                self.assertIsInstance(refined, str)
            except (TypeError, ValueError):
                # Expected behavior for non-numeric input
                pass
    
    def test_refine_consistency(self):
        """Test that refinement is consistent for same input"""
        sentence = "Test sentence for consistency"
        hrv_feedback = 0.5
        
        refined1 = self.refiner.refine(sentence, hrv_feedback)
        refined2 = self.refiner.refine(sentence, hrv_feedback)
        
        self.assertEqual(refined1, refined2)
    
    def test_refine_multiple_calls(self):
        """Test multiple calls to refine"""
        sentence = "Test sentence for multiple calls"
        hrv_feedback = 0.5
        
        for _ in range(10):
            refined = self.refiner.refine(sentence, hrv_feedback)
            self.assertIsInstance(refined, str)
            self.assertIn(sentence, refined)
            self.assertIn(str(hrv_feedback), refined)
    
    def test_refine_return_type(self):
        """Test that return type is correct"""
        sentence = "Test sentence for type checking"
        hrv_feedback = 0.5
        
        refined = self.refiner.refine(sentence, hrv_feedback)
        
        self.assertIsInstance(refined, str)
    
    def test_refine_format_consistency(self):
        """Test that refinement format is consistent"""
        sentence = "Test sentence"
        hrv_feedback = 0.5
        
        refined = self.refiner.refine(sentence, hrv_feedback)
        
        # Should follow the expected format: sentence + " [Refined with HRV feedback X.XX]"
        expected_suffix = f" [Refined with HRV feedback {hrv_feedback:.2f}]"
        self.assertTrue(refined.endswith(expected_suffix))
    
    def test_refine_feedback_precision(self):
        """Test feedback value precision in output"""
        sentence = "Test sentence"
        hrv_feedback = 0.123456789
        
        refined = self.refiner.refine(sentence, hrv_feedback)
        
        # Should format to 2 decimal places
        self.assertIn("0.12", refined)  # Rounded to 2 decimal places
    
    def test_refine_whitespace_handling(self):
        """Test refinement with various whitespace"""
        test_sentences = [
            "  Leading whitespace",
            "Trailing whitespace  ",
            "  Both whitespace  ",
            "Multiple\nlines\ntext",
            "Tabs\tand\tspaces"
        ]
        
        for sentence in test_sentences:
            refined = self.refiner.refine(sentence, 0.5)
            self.assertIsInstance(refined, str)
            self.assertIn(sentence.strip(), refined)  # Should contain original content


if __name__ == '__main__':
    unittest.main()
