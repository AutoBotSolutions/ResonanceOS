"""
Test suite for ResonanceOS v6
"""

import sys
import os

# Add the project root to Python path for testing
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
