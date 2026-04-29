"""
Test Sentence Layer Module
"""

import unittest
from resonance_os.generation.sentence_layer import SentenceLayer


class TestSentenceLayer(unittest.TestCase):
    """Test sentence layer functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sentence_layer = SentenceLayer()
    
    def test_sentence_layer_initialization(self):
        """Test that SentenceLayer initializes correctly"""
        self.assertIsInstance(self.sentence_layer, SentenceLayer)
    
    def test_generate_sentences_basic(self):
        """Test basic sentence generation"""
        outline = "Test outline for sentence generation"
        target_hrv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        sentences = self.sentence_layer.generate_sentences(outline, target_hrv)
        
        self.assertIsInstance(sentences, list)
        self.assertGreater(len(sentences), 0)
        
        # Check sentence content
        for sentence in sentences:
            self.assertIsInstance(sentence, str)
            self.assertGreater(len(sentence), 0)
    
    def test_generate_sentences_with_outline(self):
        """Test sentence generation with specific outline"""
        outline = "This is a specific outline for testing"
        target_hrv = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        
        sentences = self.sentence_layer.generate_sentences(outline, target_hrv)
        
        self.assertIsInstance(sentences, list)
        for sentence in sentences:
            self.assertIsInstance(sentence, str)
            # Should contain the outline
            self.assertIn(outline, sentence)
    
    def test_generate_sentences_different_hrv_values(self):
        """Test sentence generation with different HRV values"""
        outline = "Test outline"
        hrv_values = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [0.5, 0.7, 0.3, 0.8, 0.2, 0.9, 0.1, 0.6]
        ]
        
        for hrv in hrv_values:
            sentences = self.sentence_layer.generate_sentences(outline, hrv)
            self.assertIsInstance(sentences, list)
            self.assertGreater(len(sentences), 0)
            
            for sentence in sentences:
                self.assertIsInstance(sentence, str)
                # Should reference the HRV values
                self.assertIn(str(hrv[1]), sentence)  # emotional_valence
    
    def test_generate_sentences_empty_outline(self):
        """Test sentence generation with empty outline"""
        outline = ""
        target_hrv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        sentences = self.sentence_layer.generate_sentences(outline, target_hrv)
        
        self.assertIsInstance(sentences, list)
        for sentence in sentences:
            self.assertIsInstance(sentence, str)
    
    def test_generate_sentences_long_outline(self):
        """Test sentence generation with long outline"""
        outline = "This is a very long outline " * 100
        target_hrv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        sentences = self.sentence_layer.generate_sentences(outline, target_hrv)
        
        self.assertIsInstance(sentences, list)
        for sentence in sentences:
            self.assertIsInstance(sentence, str)
            self.assertIn(outline, sentence)
    
    def test_generate_sentences_special_characters(self):
        """Test sentence generation with special characters"""
        outline = "Test with @#$%^&*() special characters!"
        target_hrv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        sentences = self.sentence_layer.generate_sentences(outline, target_hrv)
        
        self.assertIsInstance(sentences, list)
        for sentence in sentences:
            self.assertIsInstance(sentence, str)
            self.assertIn("@#$%^&*()", sentence)
    
    def test_generate_sentences_unicode(self):
        """Test sentence generation with unicode characters"""
        outline = "Test with café naïve résumé unicode"
        target_hrv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        sentences = self.sentence_layer.generate_sentences(outline, target_hrv)
        
        self.assertIsInstance(sentences, list)
        for sentence in sentences:
            self.assertIsInstance(sentence, str)
            self.assertIn("café", sentence)
    
    def test_generate_sentences_invalid_hrv_length(self):
        """Test sentence generation with invalid HRV vector length"""
        outline = "Test outline"
        invalid_hrv = [0.1, 0.2, 0.3]  # Too short
        
        # Should handle gracefully (implementation dependent)
        try:
            sentences = self.sentence_layer.generate_sentences(outline, invalid_hrv)
            self.assertIsInstance(sentences, list)
        except (IndexError, ValueError):
            # Expected behavior for invalid HRV
            pass
    
    def test_generate_sentences_none_inputs(self):
        """Test sentence generation with None inputs"""
        # Test with None outline
        try:
            sentences = self.sentence_layer.generate_sentences(None, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
            self.assertIsInstance(sentences, list)
        except (TypeError, AttributeError):
            # Expected behavior for None input
            pass
        
        # Test with None HRV
        try:
            sentences = self.sentence_layer.generate_sentences("Test outline", None)
            self.assertIsInstance(sentences, list)
        except (TypeError, AttributeError):
            # Expected behavior for None input
            pass
    
    def test_generate_sentences_consistency(self):
        """Test that sentence generation is consistent for same input"""
        outline = "Test outline for consistency"
        target_hrv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        sentences1 = self.sentence_layer.generate_sentences(outline, target_hrv)
        sentences2 = self.sentence_layer.generate_sentences(outline, target_hrv)
        
        # Should produce similar results
        self.assertEqual(len(sentences1), len(sentences2))
        
        for s1, s2 in zip(sentences1, sentences2):
            self.assertEqual(s1, s2)
    
    def test_generate_sentences_multiple_calls(self):
        """Test multiple calls to generate_sentences"""
        outline = "Test outline for multiple calls"
        target_hrv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        for _ in range(10):
            sentences = self.sentence_layer.generate_sentences(outline, target_hrv)
            self.assertIsInstance(sentences, list)
            self.assertGreater(len(sentences), 0)
            
            for sentence in sentences:
                self.assertIsInstance(sentence, str)
                self.assertGreater(len(sentence), 0)
    
    def test_generate_sentences_return_type(self):
        """Test that return type is correct"""
        outline = "Test outline for type checking"
        target_hrv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        
        sentences = self.sentence_layer.generate_sentences(outline, target_hrv)
        
        self.assertIsInstance(sentences, list)
        if sentences:
            self.assertIsInstance(sentences[0], str)


if __name__ == '__main__':
    unittest.main()
