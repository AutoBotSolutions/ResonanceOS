"""
ResonanceOS v6 - Human-Resonant AI Writing Engine
"""

__version__ = "6.0.0"
__author__ = "ResonanceOS Team"

# Core imports
from .core.hrv_constants import HRV_DIMENSIONS
from .core.hrv_types import HRVVector, HRVProfile

# Main components
from .generation.human_resonant_writer import HumanResonantWriter
from .profiles.multi_tenant_hr_profiles import HRVProfileManager
from .profiles.hrv_extractor import HRVExtractor

__all__ = [
    "HRV_DIMENSIONS",
    "HRVVector", 
    "HRVProfile",
    "HumanResonantWriter",
    "HRVProfileManager",
    "HRVExtractor"
]
