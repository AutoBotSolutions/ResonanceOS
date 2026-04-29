"""
Test HRV Extractor Module
"""

import unittest
from resonance_os.profiles.hrv_extractor import HRVExtractor


class TestHRVExtractor(unittest.TestCase):
    """Test HRV extraction functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = HRVExtractor()
    
    def test_extractor_initialization(self):
        """Test that HRVExtractor initializes correctly"""
        self.assertIsInstance(self.extractor, HRVExtractor)
    
    def test_extract_basic_text(self):
        """Test basic HRV extraction from simple text"""
        text = "This is a simple test sentence."
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
        self.assertTrue(all(isinstance(x, (int, float)) for x in hrv_vector))
    
    def test_extract_empty_text(self):
        """Test HRV extraction from empty text"""
        text = ""
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
    
    def test_extract_single_sentence(self):
        """Test HRV extraction from single sentence"""
        text = "This is a single sentence."
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
    
    def test_extract_multiple_sentences(self):
        """Test HRV extraction from multiple sentences"""
        text = "First sentence. Second sentence. Third sentence."
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
    
    def test_extract_positive_sentiment(self):
        """Test HRV extraction from positive sentiment text"""
        text = "This is amazing and wonderful and great!"
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
        # Emotional valence should be positive
        self.assertGreater(hrv_vector[1], 0)
    
    def test_extract_negative_sentiment(self):
        """Test HRV extraction from negative sentiment text"""
        text = "This is terrible and awful and horrible!"
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
        # Emotional valence should be negative
        self.assertLess(hrv_vector[1], 0)
    
    def test_extract_neutral_sentiment(self):
        """Test HRV extraction from neutral sentiment text"""
        text = "This is a statement about facts and information."
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
        # Emotional valence should be near zero
        self.assertAlmostEqual(hrv_vector[1], 0, delta=0.5)
    
    def test_extract_sentence_variance(self):
        """Test sentence variance calculation"""
        # Text with varying sentence lengths
        text = "Short. This is a medium length sentence. This is a much longer sentence with many more words to test variance calculation."
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
        # Sentence variance should be positive
        self.assertGreaterEqual(hrv_vector[0], 0)
    
    def test_extract_lexical_diversity(self):
        """Test lexical diversity calculation"""
        # Text with repeated words
        text = "test test test test test test test test"
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
    
    def test_extract_long_text(self):
        """Test HRV extraction from long text"""
        text = "This is a very long text. " * 100
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
    
    def test_extract_special_characters(self):
        """Test HRV extraction with special characters"""
        text = "This has @#$%^&*() special characters!"
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
    
    def test_extract_unicode_text(self):
        """Test HRV extraction with unicode characters"""
        text = "This has émojis 😀 and ünicode chárácters."
        hrv_vector = self.extractor.extract(text)
        
        self.assertIsInstance(hrv_vector, list)
        self.assertEqual(len(hrv_vector), 8)
    
    def test_extract_consistency(self):
        """Test that extraction is consistent for same input"""
        text = "This is a test for consistency."
        hrv_vector1 = self.extractor.extract(text)
        hrv_vector2 = self.extractor.extract(text)
        
        self.assertEqual(hrv_vector1, hrv_vector2)
    
    def test_extract_dimension_ranges(self):
        """Test that HRV dimensions are within expected ranges"""
        text = "This is a test sentence for range validation."
        hrv_vector = self.extractor.extract(text)
        
        # Test reasonable ranges for each dimension
        self.assertGreaterEqual(hrv_vector[0], 0)  # sentence_variance >= 0
        self.assertGreaterEqual(hrv_vector[1], -1)  # emotional_valence >= -1
        self.assertLessEqual(hrv_vector[1], 1)  # emotional_valence <= 1
        self.assertGreaterEqual(hrv_vector[2], 0)  # emotional_intensity >= 0


if __name__ == '__main__':
    unittest.main()
