"""
Test Planner Layer Module
"""

import unittest
from resonance_os.generation.planner_layer import PlannerLayer


class TestPlannerLayer(unittest.TestCase):
    """Test planner layer functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.planner = PlannerLayer()
    
    def test_planner_initialization(self):
        """Test that PlannerLayer initializes correctly"""
        self.assertIsInstance(self.planner, PlannerLayer)
    
    def test_plan_paragraphs_default(self):
        """Test planning paragraphs with default parameters"""
        prompt = "Test prompt for planning"
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt)
        
        self.assertIsInstance(paragraphs, list)
        self.assertIsInstance(target_hrvs, list)
        self.assertEqual(len(paragraphs), 3)  # Default num_paragraphs
        self.assertEqual(len(target_hrvs), 3)
        
        # Check paragraph content
        for paragraph in paragraphs:
            self.assertIsInstance(paragraph, str)
            self.assertIn(prompt, paragraph)
        
        # Check HRV vectors
        for hrv in target_hrvs:
            self.assertIsInstance(hrv, list)
            self.assertEqual(len(hrv), 8)
            self.assertTrue(all(isinstance(x, (int, float)) for x in hrv))
    
    def test_plan_paragraphs_custom_count(self):
        """Test planning paragraphs with custom paragraph count"""
        prompt = "Test prompt for custom planning"
        num_paragraphs = 5
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt, num_paragraphs)
        
        self.assertEqual(len(paragraphs), num_paragraphs)
        self.assertEqual(len(target_hrvs), num_paragraphs)
    
    def test_plan_paragraphs_single(self):
        """Test planning single paragraph"""
        prompt = "Test prompt for single paragraph"
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt, 1)
        
        self.assertEqual(len(paragraphs), 1)
        self.assertEqual(len(target_hrvs), 1)
        
        self.assertIsInstance(paragraphs[0], str)
        self.assertIsInstance(target_hrvs[0], list)
        self.assertEqual(len(target_hrvs[0]), 8)
    
    def test_plan_paragraphs_zero(self):
        """Test planning zero paragraphs"""
        prompt = "Test prompt for zero paragraphs"
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt, 0)
        
        self.assertEqual(len(paragraphs), 0)
        self.assertEqual(len(target_hrvs), 0)
    
    def test_plan_paragraphs_large_count(self):
        """Test planning large number of paragraphs"""
        prompt = "Test prompt for large planning"
        num_paragraphs = 100
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt, num_paragraphs)
        
        self.assertEqual(len(paragraphs), num_paragraphs)
        self.assertEqual(len(target_hrvs), num_paragraphs)
    
    def test_plan_paragraphs_empty_prompt(self):
        """Test planning with empty prompt"""
        prompt = ""
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt)
        
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(len(target_hrvs), 3)
        
        # Should still contain the prompt (even if empty)
        for paragraph in paragraphs:
            self.assertIsInstance(paragraph, str)
    
    def test_plan_paragraphs_long_prompt(self):
        """Test planning with long prompt"""
        prompt = "This is a very long prompt " * 100
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt)
        
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(len(target_hrvs), 3)
        
        # Should handle long prompts gracefully
        for paragraph in paragraphs:
            self.assertIsInstance(paragraph, str)
            self.assertGreater(len(paragraph), 0)
    
    def test_plan_paragraphs_special_characters(self):
        """Test planning with special characters"""
        prompt = "Test with @#$%^&*() special characters!"
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt)
        
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(len(target_hrvs), 3)
        
        # Should handle special characters
        for paragraph in paragraphs:
            self.assertIsInstance(paragraph, str)
            self.assertIn("@#$%^&*()", paragraph)
    
    def test_plan_paragraphs_unicode(self):
        """Test planning with unicode characters"""
        prompt = "Test with café naïve résumé unicode"
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt)
        
        self.assertEqual(len(paragraphs), 3)
        self.assertEqual(len(target_hrvs), 3)
        
        # Should handle unicode characters
        for paragraph in paragraphs:
            self.assertIsInstance(paragraph, str)
            self.assertIn("café", paragraph)
    
    def test_plan_paragraphs_hrv_ranges(self):
        """Test that HRV vectors are in valid ranges"""
        prompt = "Test prompt for HRV range validation"
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt)
        
        for hrv in target_hrvs:
            self.assertEqual(len(hrv), 8)
            # All values should be between 0 and 1 (random generation)
            for value in hrv:
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 1.0)
    
    def test_plan_paragraphs_consistency(self):
        """Test that planning is consistent for same input"""
        prompt = "Test prompt for consistency"
        
        # Plan multiple times
        result1 = self.planner.plan_paragraphs(prompt)
        result2 = self.planner.plan_paragraphs(prompt)
        
        # Results should have same structure
        self.assertEqual(len(result1[0]), len(result2[0]))
        self.assertEqual(len(result1[1]), len(result2[1]))
        
        # Content should be similar (though HRV values may differ due to randomness)
        for p1, p2 in zip(result1[0], result2[0]):
            self.assertEqual(p1, p2)  # Paragraph outlines should be identical
    
    def test_plan_paragraphs_return_types(self):
        """Test return types are correct"""
        prompt = "Test prompt for type checking"
        paragraphs, target_hrvs = self.planner.plan_paragraphs(prompt)
        
        # Check return type annotation
        self.assertIsInstance(paragraphs, list)
        self.assertIsInstance(target_hrvs, list)
        self.assertIsInstance(paragraphs[0], str)
        self.assertIsInstance(target_hrvs[0], list)


if __name__ == '__main__':
    unittest.main()
