"""
Test HRV Constants Module
"""

import unittest
from resonance_os.core.hrv_constants import HRV_DIMENSIONS


class TestHRVConstants(unittest.TestCase):
    """Test HRV dimension constants"""
    
    def test_hrv_dimensions_exists(self):
        """Test that HRV_DIMENSIONS is defined"""
        self.assertIsNotNone(HRV_DIMENSIONS)
    
    def test_hrv_dimensions_is_list(self):
        """Test that HRV_DIMENSIONS is a list"""
        self.assertIsInstance(HRV_DIMENSIONS, list)
    
    def test_hrv_dimensions_length(self):
        """Test that HRV_DIMENSIONS has 8 dimensions"""
        self.assertEqual(len(HRV_DIMENSIONS), 8)
    
    def test_hrv_dimensions_content(self):
        """Test that HRV_DIMENSIONS contains expected dimensions"""
        expected_dimensions = [
            'sentence_variance',
            'emotional_valence', 
            'emotional_intensity',
            'assertiveness_index',
            'curiosity_index',
            'metaphor_density',
            'storytelling_index',
            'active_voice_ratio'
        ]
        self.assertEqual(HRV_DIMENSIONS, expected_dimensions)
    
    def test_hrv_dimensions_all_strings(self):
        """Test that all HRV dimensions are strings"""
        self.assertTrue(all(isinstance(dim, str) for dim in HRV_DIMENSIONS))
    
    def test_hrv_dimensions_unique(self):
        """Test that all HRV dimensions are unique"""
        self.assertEqual(len(HRV_DIMENSIONS), len(set(HRV_DIMENSIONS)))


if __name__ == '__main__':
    unittest.main()
