"""
ResonanceOS - Adaptive Stylistic Alignment Engine
"""

__version__ = "0.1.0"
__author__ = "Trenaman"
__email__ = "trenaman@example.com"

from resonance_os.core.types import (
    ResonanceVector,
    StyleProfile,
    GenerationConfig,
    FeedbackMetrics,
)
from resonance_os.core.config import get_config
from resonance_os.core.constants import RESONANCE_DIMENSIONS

__all__ = [
    "ResonanceVector",
    "StyleProfile", 
    "GenerationConfig",
    "FeedbackMetrics",
    "get_config",
    "RESONANCE_DIMENSIONS",
]
