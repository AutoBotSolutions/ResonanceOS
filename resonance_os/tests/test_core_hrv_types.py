"""
Test HRV Types Module
"""

import unittest
from resonance_os.core.hrv_types import HRVVector, HRVProfile


class TestHRVTypes(unittest.TestCase):
    """Test HRV type definitions"""
    
    def test_hrv_vector_type_exists(self):
        """Test that HRVVector type is defined"""
        self.assertIsNotNone(HRVVector)
    
    def test_hrv_vector_type_annotation(self):
        """Test that HRVVector is properly typed"""
        # HRVVector should be List[float] - check that it's compatible with list
        import typing
        self.assertEqual(HRVVector, typing.List[float])
        # Also verify it works as a list
        test_vector: HRVVector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        self.assertIsInstance(test_vector, list)
    
    def test_hrv_profile_type_exists(self):
        """Test that HRVProfile type is defined"""
        self.assertIsNotNone(HRVProfile)
    
    def test_hrv_profile_type_annotation(self):
        """Test that HRVProfile is properly typed"""
        # HRVProfile should be Dict[str, Union[float, List[float], str]]
        import typing
        self.assertEqual(HRVProfile, typing.Dict[str, typing.Union[float, typing.List[float], str]])
        # Also verify it works as a dict
        test_profile: HRVProfile = {
            'name': 'Test Profile',
            'hrv_vector': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            'metadata': 'test profile data'
        }
        self.assertIsInstance(test_profile, dict)
    
    def test_hrv_vector_usage(self):
        """Test HRVVector type usage"""
        test_vector: HRVVector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        self.assertIsInstance(test_vector, list)
        self.assertEqual(len(test_vector), 8)
        self.assertTrue(all(isinstance(x, (int, float)) for x in test_vector))
    
    def test_hrv_profile_usage(self):
        """Test HRVProfile type usage"""
        test_profile: HRVProfile = {
            'name': 'Test Profile',
            'hrv_vector': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            'metadata': 'test profile data'
        }
        self.assertIsInstance(test_profile, dict)
        self.assertIn('name', test_profile)
        self.assertIn('hrv_vector', test_profile)


if __name__ == '__main__':
    unittest.main()
