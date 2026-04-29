"""
Drift detection for ResonanceOS
"""

import numpy as np
from typing import List, Dict, Optional, Tuple, Union
from collections import deque
from datetime import datetime, timedelta
import statistics

from ..core.types import ResonanceVector, DriftAnalysis, SimilarityMethod
from ..core.constants import DEFAULT_DRIFT_THRESHOLD
from ..core.logging import get_logger, log_performance
from .metrics import SimilarityCalculator

logger = get_logger(__name__)


class DriftDetector:
    """Detects and analyzes style drift in real-time"""
    
    def __init__(
        self,
        window_size: int = 10,
        drift_threshold: float = DEFAULT_DRIFT_THRESHOLD,
        similarity_method: SimilarityMethod = SimilarityMethod.COSINE
    ):
        self.window_size = window_size
        self.drift_threshold = drift_threshold
        self.similarity_method = similarity_method
        self.similarity_calculator = SimilarityCalculator(similarity_method)
        
        # History tracking
        self.similarity_history = deque(maxlen=window_size)
        self.vector_history = deque(maxlen=window_size)
        self.timestamp_history = deque(maxlen=window_size)
        
        # Baseline
        self.baseline_similarity: Optional[float] = None
        self.baseline_vector: Optional[ResonanceVector] = None
        self.baseline_set = False
    
    @log_performance
    def add_measurement(
        self,
        current_vector: ResonanceVector,
        target_vector: ResonanceVector,
        timestamp: Optional[datetime] = None
    ) -> DriftAnalysis:
        """Add new measurement and analyze drift"""
        
        timestamp = timestamp or datetime.now()
        
        # Calculate similarity
        similarity = self.similarity_calculator.calculate_similarity(
            current_vector, target_vector, self.similarity_method
        )
        
        # Add to history
        self.similarity_history.append(similarity)
        self.vector_history.append(current_vector)
        self.timestamp_history.append(timestamp)
        
        # Set baseline if not set
        if not self.baseline_set:
            self.baseline_similarity = similarity
            self.baseline_vector = current_vector
            self.baseline_set = True
        
        # Analyze drift
        drift_analysis = self._analyze_drift()
        
        logger.debug(f"Drift analysis: similarity={similarity:.3f}, drift_rate={drift_analysis.drift_rate:.3f}")
        
        return drift_analysis
    
    def _analyze_drift(self) -> DriftAnalysis:
        """Analyze current drift state"""
        
        if len(self.similarity_history) < 2:
            return DriftAnalysis(
                current_similarity=self.similarity_history[0] if self.similarity_history else 0.0,
                baseline_similarity=self.baseline_similarity or 0.0,
                drift_rate=0.0,
                drift_direction="stable",
                affected_dimensions=[],
                severity="low",
                recommendation="insufficient_data"
            )
        
        current_similarity = self.similarity_history[-1]
        
        # Calculate drift rate
        drift_rate = self._calculate_drift_rate()
        
        # Determine drift direction
        drift_direction = self._determine_drift_direction()
        
        # Identify affected dimensions
        affected_dimensions = self._identify_affected_dimensions()
        
        # Assess severity
        severity = self._assess_severity(drift_rate, current_similarity)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(severity, drift_rate)
        
        return DriftAnalysis(
            current_similarity=current_similarity,
            baseline_similarity=self.baseline_similarity or 0.0,
            drift_rate=drift_rate,
            drift_direction=drift_direction,
            affected_dimensions=affected_dimensions,
            severity=severity,
            recommendation=recommendation,
            timestamp=datetime.now()
        )
    
    def _calculate_drift_rate(self) -> float:
        """Calculate rate of drift"""
        
        if len(self.similarity_history) < 2:
            return 0.0
        
        # Calculate rate of change in similarity
        similarities = list(self.similarity_history)
        
        # Use linear regression to estimate trend
        x = np.arange(len(similarities))
        y = np.array(similarities)
        
        if len(x) < 2:
            return 0.0
        
        # Calculate slope (rate of change)
        slope = np.polyfit(x, y, 1)[0]
        
        # Normalize to [0, 1] range (absolute value)
        drift_rate = abs(slope)
        
        return min(1.0, drift_rate)
    
    def _determine_drift_direction(self) -> str:
        """Determine direction of drift"""
        
        if len(self.similarity_history) < 2:
            return "stable"
        
        # Compare recent to baseline
        current = self.similarity_history[-1]
        baseline = self.baseline_similarity or current
        
        if abs(current - baseline) < 0.01:
            return "stable"
        elif current > baseline:
            return "improving"
        else:
            return "declining"
    
    def _identify_affected_dimensions(self) -> List[str]:
        """Identify dimensions contributing most to drift"""
        
        if len(self.vector_history) < 2 or not self.baseline_vector:
            return []
        
        current_vector = self.vector_history[-1]
        baseline_vector = self.baseline_vector
        
        # Calculate deviation for each dimension
        deviations = []
        for i, (current_val, baseline_val) in enumerate(zip(current_vector.values, baseline_vector.values)):
            deviation = abs(current_val - baseline_val)
            deviations.append((i, deviation))
        
        # Sort by deviation and get top contributors
        deviations.sort(key=lambda x: x[1], reverse=True)
        
        # Return dimensions with significant deviations (> 0.1)
        affected = []
        for dim_idx, deviation in deviations[:3]:  # Top 3 dimensions
            if deviation > 0.1:
                if dim_idx < len(current_vector.dimensions):
                    affected.append(current_vector.dimensions[dim_idx])
        
        return affected
    
    def _assess_severity(self, drift_rate: float, current_similarity: float) -> str:
        """Assess drift severity"""
        
        # High severity: high drift rate OR low similarity
        if drift_rate > self.drift_threshold * 2 or current_similarity < 0.7:
            return "high"
        elif drift_rate > self.drift_threshold or current_similarity < 0.85:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendation(self, severity: str, drift_rate: float) -> str:
        """Generate recommendation based on drift analysis"""
        
        if severity == "high":
            return "immediate_correction_required"
        elif severity == "medium":
            return "monitor_and_adjust"
        elif drift_rate > 0.01:
            return "increase_monitoring"
        else:
            return "continue_monitoring"
    
    def get_drift_trend(self, lookback: Optional[int] = None) -> Dict[str, Union[List[float], str]]:
        """Get drift trend over time"""
        
        lookback = lookback or len(self.similarity_history)
        
        if len(self.similarity_history) < 2:
            return {
                'trend': 'insufficient_data',
                'similarities': list(self.similarity_history),
                'timestamps': [t.isoformat() for t in self.timestamp_history]
            }
        
        # Get recent similarities
        recent_similarities = list(self.similarity_history)[-lookback:]
        recent_timestamps = list(self.timestamp_history)[-lookback:]
        
        # Calculate trend
        if len(recent_similarities) >= 3:
            # Use last 3 points to determine trend
            recent_3 = recent_similarities[-3:]
            if recent_3[2] > recent_3[1] > recent_3[0]:
                trend = 'improving'
            elif recent_3[2] < recent_3[1] < recent_3[0]:
                trend = 'declining'
            else:
                trend = 'fluctuating'
        else:
            trend = 'insufficient_data'
        
        return {
            'trend': trend,
            'similarities': recent_similarities,
            'timestamps': [t.isoformat() for t in recent_timestamps],
            'average': statistics.mean(recent_similarities),
            'variance': statistics.variance(recent_similarities) if len(recent_similarities) > 1 else 0.0
        }
    
    def reset_baseline(self, new_baseline: Optional[ResonanceVector] = None):
        """Reset baseline for drift detection"""
        
        if new_baseline and self.similarity_history:
            # Calculate new baseline similarity
            if self.vector_history:
                current_vector = self.vector_history[-1]
                self.baseline_similarity = self.similarity_calculator.calculate_similarity(
                    current_vector, new_baseline, self.similarity_method
                )
            self.baseline_vector = new_baseline
        else:
            # Reset to current state
            if self.similarity_history:
                self.baseline_similarity = self.similarity_history[-1]
            if self.vector_history:
                self.baseline_vector = self.vector_history[-1]
        
        self.baseline_set = True
        logger.info("Baseline reset for drift detection")
    
    def get_drift_statistics(self) -> Dict[str, Union[float, int, str]]:
        """Get comprehensive drift statistics"""
        
        if not self.similarity_history:
            return {
                'total_measurements': 0,
                'current_similarity': 0.0,
                'baseline_similarity': 0.0,
                'average_drift_rate': 0.0,
                'max_drift_rate': 0.0,
                'drift_episodes': 0,
                'status': 'no_data'
            }
        
        similarities = list(self.similarity_history)
        
        # Calculate drift rates for each point (after the first)
        drift_rates = []
        for i in range(1, len(similarities)):
            rate = abs(similarities[i] - similarities[i-1])
            drift_rates.append(rate)
        
        # Count drift episodes (periods where drift exceeds threshold)
        drift_episodes = sum(1 for rate in drift_rates if rate > self.drift_threshold)
        
        return {
            'total_measurements': len(similarities),
            'current_similarity': similarities[-1],
            'baseline_similarity': self.baseline_similarity or 0.0,
            'average_drift_rate': statistics.mean(drift_rates) if drift_rates else 0.0,
            'max_drift_rate': max(drift_rates) if drift_rates else 0.0,
            'drift_episodes': drift_episodes,
            'drift_frequency': drift_episodes / max(len(similarities) - 1, 1),
            'status': 'active'
        }
    
    def predict_drift(self, steps_ahead: int = 5) -> Dict[str, Union[List[float], float, str]]:
        """Predict future drift based on current trend"""
        
        if len(self.similarity_history) < 3:
            return {
                'prediction': 'insufficient_data',
                'predicted_similarities': [],
                'confidence': 0.0
            }
        
        # Use linear regression to predict future values
        similarities = list(self.similarity_history)
        x = np.arange(len(similarities))
        y = np.array(similarities)
        
        # Fit linear model
        coeffs = np.polyfit(x, y, 1)
        trend_line = np.poly1d(coeffs)
        
        # Predict future values
        future_x = np.arange(len(similarities), len(similarities) + steps_ahead)
        predicted_similarities = trend_line(future_x)
        
        # Calculate confidence based on R²
        y_pred = trend_line(x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        confidence = max(0.0, r_squared)
        
        # Clip predictions to [0, 1] range
        predicted_similarities = np.clip(predicted_similarities, 0.0, 1.0)
        
        return {
            'prediction': 'trend_based',
            'predicted_similarities': predicted_similarities.tolist(),
            'confidence': confidence,
            'trend_slope': coeffs[0],
            'expected_drift_rate': abs(coeffs[0])
        }
    
    def export_drift_data(self) -> Dict[str, Union[List, Dict]]:
        """Export drift detection data for analysis"""
        
        return {
            'config': {
                'window_size': self.window_size,
                'drift_threshold': self.drift_threshold,
                'similarity_method': self.similarity_method.value
            },
            'baseline': {
                'similarity': self.baseline_similarity,
                'vector': self.baseline_vector.dict() if self.baseline_vector else None,
                'set': self.baseline_set
            },
            'history': {
                'similarities': list(self.similarity_history),
                'timestamps': [t.isoformat() for t in self.timestamp_history],
                'vectors': [v.dict() for v in self.vector_history] if self.vector_history else []
            },
            'statistics': self.get_drift_statistics(),
            'trend': self.get_drift_trend(),
            'prediction': self.predict_drift()
        }


class AdaptiveDriftDetector(DriftDetector):
    """Adaptive drift detector that adjusts thresholds based on patterns"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adaptive_threshold = self.drift_threshold
        self.threshold_history = deque(maxlen=50)
        self.false_positive_count = 0
        self.false_negative_count = 0
    
    def update_threshold(self, performance_feedback: Dict[str, Union[bool, float]]):
        """Update adaptive threshold based on performance feedback"""
        
        if performance_feedback.get('false_positive', False):
            self.false_positive_count += 1
            # Increase threshold to reduce false positives
            self.adaptive_threshold *= 1.1
        elif performance_feedback.get('false_negative', False):
            self.false_negative_count += 1
            # Decrease threshold to reduce false negatives
            self.adaptive_threshold *= 0.9
        
        # Keep threshold in reasonable bounds
        self.adaptive_threshold = max(0.01, min(0.5, self.adaptive_threshold))
        
        self.threshold_history.append(self.adaptive_threshold)
        
        logger.info(f"Updated adaptive threshold to {self.adaptive_threshold:.3f}")
    
    def get_adaptive_statistics(self) -> Dict[str, Union[float, int]]:
        """Get adaptive detector statistics"""
        
        return {
            'current_threshold': self.adaptive_threshold,
            'original_threshold': self.drift_threshold,
            'threshold_adjustment': self.adaptive_threshold / self.drift_threshold,
            'false_positives': self.false_positive_count,
            'false_negatives': self.false_negative_count,
            'total_adjustments': len(self.threshold_history)
        }
