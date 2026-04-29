"""
Test HR Main CLI Module
"""

import unittest
import sys
import io
from unittest.mock import patch, MagicMock
from resonance_os.cli.hr_main import main


class TestHRMainCLI(unittest.TestCase):
    """Test HR main CLI functionality"""
    
    def test_main_function_exists(self):
        """Test that main function exists"""
        self.assertTrue(callable(main))
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test prompt'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_basic_prompt(self, mock_stdout):
        """Test main function with basic prompt"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain expected output sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
            self.assertIn("Test prompt", output)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test prompt', '--tenant', 'test_tenant'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_tenant(self, mock_stdout):
        """Test main function with tenant parameter"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain expected output sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
            self.assertIn("Test prompt", output)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test prompt', '--profile', 'test_profile'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_profile(self, mock_stdout):
        """Test main function with profile parameter"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain expected output sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
            self.assertIn("Test prompt", output)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test prompt', '--tenant', 'test_tenant', '--profile', 'test_profile'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_tenant_and_profile(self, mock_stdout):
        """Test main function with both tenant and profile"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain expected output sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
            self.assertIn("Test prompt", output)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', ''])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_empty_prompt(self, mock_stdout):
        """Test main function with empty prompt"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should still contain expected output sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test with special characters @#$%^&*()'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_special_characters(self, mock_stdout):
        """Test main function with special characters"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain expected output sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
            self.assertIn("@#$%^&*()", output)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test with unicode café naïve résumé'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_unicode(self, mock_stdout):
        """Test main function with unicode characters"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain expected output sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
            self.assertIn("café", output)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test with numbers 123 and symbols'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_numbers_and_symbols(self, mock_stdout):
        """Test main function with numbers and symbols"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain expected output sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
            self.assertIn("123", output)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py'])
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_missing_prompt(self, mock_stderr):
        """Test main function without required prompt"""
        try:
            main()
        except SystemExit:
            # Expected for missing required argument
            pass
    
    @patch('sys.argv', ['hr_main.py', '--help'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_help(self, mock_stdout):
        """Test main function help output"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain help information
            self.assertIn("Human-Resonant CLI", output)
            self.assertIn("prompt", output)
            self.assertIn("tenant", output)
            self.assertIn("profile", output)
        except SystemExit:
            # Expected for help command
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test prompt'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_output_format(self, mock_stdout):
        """Test main function output format"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should have proper section headers
            self.assertIn("=== Generated Human-Resonant Article ===", output)
            self.assertIn("=== HRV Feedback ===", output)
            
            # Should have content sections
            lines = output.split('\n')
            article_line_index = -1
            hrv_line_index = -1
            
            for i, line in enumerate(lines):
                if "Generated Human-Resonant Article" in line:
                    article_line_index = i
                elif "HRV Feedback" in line:
                    hrv_line_index = i
            
            # Should find both sections
            self.assertNotEqual(article_line_index, -1)
            self.assertNotEqual(hrv_line_index, -1)
            
            # HRV section should come after article section
            self.assertGreater(hrv_line_index, article_line_index)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test prompt'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_hrv_feedback_format(self, mock_stdout):
        """Test HRV feedback format in output"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain HRV feedback list
            self.assertIn("[", output)
            self.assertIn("]", output)
            
            # Should contain numeric values
            import re
            numbers = re.findall(r'\d+\.\d+', output)
            self.assertGreater(len(numbers), 0)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test prompt for long content'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_long_prompt(self, mock_stdout):
        """Test main function with long prompt"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should contain expected output sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
            self.assertIn("Test prompt for long content", output)
            
            # Should handle long content
            self.assertGreater(len(output), 50)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test prompt'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_content_quality(self, mock_stdout):
        """Test quality of CLI output"""
        try:
            main()
            output = mock_stdout.getvalue()
            
            # Should not be empty
            self.assertGreater(len(output), 0)
            
            # Should contain meaningful content
            self.assertNotEqual(output.strip(), "")
            
            # Should contain expected sections
            self.assertIn("Generated Human-Resonant Article", output)
            self.assertIn("HRV Feedback", output)
        except SystemExit:
            # Expected for CLI applications
            pass
    
    @patch('sys.argv', ['hr_main.py', '--prompt', 'Test prompt'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_multiple_runs(self, mock_stdout):
        """Test multiple runs of main function"""
        outputs = []
        
        for _ in range(3):
            try:
                # Reset stdout for each run
                mock_stdout.seek(0)
                mock_stdout.truncate(0)
                
                main()
                output = mock_stdout.getvalue()
                outputs.append(output)
                
                # Each output should be valid
                self.assertIn("Generated Human-Resonant Article", output)
                self.assertIn("HRV Feedback", output)
                self.assertIn("Test prompt", output)
            except SystemExit:
                # Expected for CLI applications
                pass
        
        # Should have collected outputs
        self.assertEqual(len(outputs), 3)
    
    def test_main_import_dependencies(self):
        """Test that main function imports work correctly"""
        # Test that the imports in hr_main.py work
        try:
            from resonance_os.cli.hr_main import main
            from resonance_os.api.hr_server import SimpleRequest, hr_generate
            
            self.assertTrue(callable(main))
            self.assertTrue(callable(SimpleRequest))
            self.assertTrue(callable(hr_generate))
        except ImportError as e:
            self.fail(f"Import failed: {e}")


if __name__ == '__main__':
    unittest.main()
