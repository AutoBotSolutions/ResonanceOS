"""
Parameter controller for ResonanceOS
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import statistics

from ..core.types import ResonanceVector, CorrectionAction, FeedbackMetrics
from ..core.constants import DEFAULT_TEMPERATURE, DEFAULT_TOP_P, MAX_CORRECTION_ATTEMPTS
from ..core.logging import get_logger, log_performance

logger = get_logger(__name__)


class ParameterType(str, Enum):
    """Types of controllable parameters"""
    TEMPERATURE = "temperature"
    TOP_P = "top_p"
    PRESENCE_PENALTY = "presence_penalty"
    FREQUENCY_PENALTY = "frequency_penalty"
    MAX_TOKENS = "max_tokens"
    SENTENCE_LENGTH_BIAS = "sentence_length_bias"
    EMOTIONAL_WEIGHT = "emotional_weight"
    VOCABULARY_CONSTRAINT = "vocabulary_constraint"
    CADENCE_TEMPLATE = "cadence_template"


@dataclass
class ParameterRange:
    """Valid range for a parameter"""
    min_value: float
    max_value: float
    default_value: float
    step_size: float = 0.01


class ParameterController:
    """Controls generation parameters based on resonance feedback"""
    
    def __init__(self):
        # Define parameter ranges
        self.parameter_ranges = {
            ParameterType.TEMPERATURE: ParameterRange(0.0, 2.0, DEFAULT_TEMPERATURE, 0.01),
            ParameterType.TOP_P: ParameterRange(0.0, 1.0, DEFAULT_TOP_P, 0.01),
            ParameterType.PRESENCE_PENALTY: ParameterRange(-2.0, 2.0, 0.0, 0.1),
            ParameterType.FREQUENCY_PENALTY: ParameterRange(-2.0, 2.0, 0.0, 0.1),
            ParameterType.MAX_TOKENS: ParameterRange(100, 8192, 2048, 100),
            ParameterType.SENTENCE_LENGTH_BIAS: ParameterRange(-1.0, 1.0, 0.0, 0.1),
            ParameterType.EMOTIONAL_WEIGHT: ParameterRange(0.0, 2.0, 1.0, 0.1),
            ParameterType.VOCABULARY_CONSTRAINT: ParameterRange(0.0, 1.0, 0.0, 0.1),
            ParameterType.CADENCE_TEMPLATE: ParameterRange(0.0, 1.0, 0.5, 0.1)
        }
        
        # Current parameter values
        self.current_parameters = {
            param: range.default_value 
            for param, range in self.parameter_ranges.items()
        }
        
        # Correction history
        self.correction_history: List[CorrectionAction] = []
        self.feedback_history: List[FeedbackMetrics] = []
        
        # Learning rates for different parameters
        self.learning_rates = {
            ParameterType.TEMPERATURE: 0.1,
            ParameterType.TOP_P: 0.1,
            ParameterType.PRESENCE_PENALTY: 0.2,
            ParameterType.FREQUENCY_PENALTY: 0.2,
            ParameterType.SENTENCE_LENGTH_BIAS: 0.15,
            ParameterType.EMOTIONAL_WEIGHT: 0.15,
            ParameterType.VOCABULARY_CONSTRAINT: 0.1,
            ParameterType.CADENCE_TEMPLATE: 0.1
        }
    
    @log_performance
    def calculate_corrections(
        self,
        current_metrics: FeedbackMetrics,
        target_similarity: float = 0.92
    ) -> List[CorrectionAction]:
        """Calculate parameter corrections based on feedback metrics"""
        
        self.feedback_history.append(current_metrics)
        
        corrections = []
        
        # Get deviation vector
        deviations = current_metrics.deviation_vector
        if not deviations:
            logger.warning("No deviation vector provided for correction calculation")
            return corrections
        
        # Analyze which dimensions need correction
        critical_dimensions = self._identify_critical_dimensions(deviations)
        
        # Calculate corrections for each affected parameter
        for dimension, deviation in zip(current_metrics.resonance_vector.dimensions, deviations):
            if abs(deviation) > 0.1:  # Only correct significant deviations
                param_corrections = self._map_dimension_to_parameters(dimension, deviation)
                corrections.extend(param_corrections)
        
        # Apply corrections to current parameters
        for correction in corrections:
            self._apply_correction(correction)
        
        # Limit number of corrections to avoid over-adjustment
        if len(corrections) > 5:
            # Keep only the most impactful corrections
            corrections.sort(key=lambda x: abs(x.adjustment), reverse=True)
            corrections = corrections[:5]
        
        self.correction_history.extend(corrections)
        
        logger.info(f"Calculated {len(corrections)} parameter corrections")
        return corrections
    
    def _identify_critical_dimensions(self, deviations: List[float]) -> List[Tuple[int, float]]:
        """Identify dimensions with largest deviations"""
        
        indexed_deviations = [(i, abs(dev)) for i, dev in enumerate(deviations)]
        indexed_deviations.sort(key=lambda x: x[1], reverse=True)
        
        # Return dimensions with deviation > 0.1
        critical = [(i, dev) for i, dev in indexed_deviations if dev > 0.1]
        
        return critical[:3]  # Top 3 critical dimensions
    
    def _map_dimension_to_parameters(
        self,
        dimension: str,
        deviation: float
    ) -> List[CorrectionAction]:
        """Map resonance dimension deviations to parameter corrections"""
        
        corrections = []
        
        # Mapping of dimensions to parameters
        dimension_param_map = {
            'lexical_density': [ParameterType.VOCABULARY_CONSTRAINT, ParameterType.SENTENCE_LENGTH_BIAS],
            'emotional_valence': [ParameterType.EMOTIONAL_WEIGHT],
            'cadence_variability': [ParameterType.CADENCE_TEMPLATE, ParameterType.SENTENCE_LENGTH_BIAS],
            'sentence_entropy': [ParameterType.TEMPERATURE, ParameterType.TOP_P],
            'metaphor_frequency': [ParameterType.TEMPERATURE, ParameterType.VOCABULARY_CONSTRAINT],
            'abstraction_level': [ParameterType.VOCABULARY_CONSTRAINT, ParameterType.SENTENCE_LENGTH_BIAS],
            'assertiveness_score': [ParameterType.PRESENCE_PENALTY, ParameterType.TEMPERATURE],
            'rhythm_signature': [ParameterType.CADENCE_TEMPLATE, ParameterType.TOP_P],
            'narrative_intensity_curve': [ParameterType.EMOTIONAL_WEIGHT, ParameterType.TEMPERATURE],
            'cognitive_load_index': [ParameterType.SENTENCE_LENGTH_BIAS, ParameterType.VOCABULARY_CONSTRAINT]
        }
        
        # Get parameters to adjust
        parameters_to_adjust = dimension_param_map.get(dimension, [])
        
        for param_type in parameters_to_adjust:
            correction = self._calculate_parameter_correction(param_type, deviation, dimension)
            if correction:
                corrections.append(correction)
        
        return corrections
    
    def _calculate_parameter_correction(
        self,
        param_type: ParameterType,
        deviation: float,
        source_dimension: str
    ) -> Optional[CorrectionAction]:
        """Calculate specific parameter correction"""
        
        current_value = self.current_parameters[param_type]
        param_range = self.parameter_ranges[param_type]
        learning_rate = self.learning_rates[param_type]
        
        # Calculate adjustment based on deviation and learning rate
        adjustment = -deviation * learning_rate  # Negative to correct the deviation
        
        # Apply different strategies based on parameter type
        if param_type == ParameterType.TEMPERATURE:
            # Increase temperature for more creativity if deviation is positive
            adjustment = deviation * learning_rate * 0.5
        elif param_type == ParameterType.EMOTIONAL_WEIGHT:
            # Direct mapping for emotional parameters
            adjustment = deviation * learning_rate
        elif param_type == ParameterType.VOCABULARY_CONSTRAINT:
            # Increase constraint for higher precision
            adjustment = abs(deviation) * learning_rate * 0.3
        elif param_type == ParameterType.CADENCE_TEMPLATE:
            # Adjust cadence based on rhythm deviations
            adjustment = deviation * learning_rate * 0.4
        
        # Calculate new value
        new_value = current_value + adjustment
        
        # Clamp to valid range
        new_value = max(param_range.min_value, min(param_range.max_value, new_value))
        
        # Only create correction if change is significant
        if abs(new_value - current_value) < param_range.step_size:
            return None
        
        reason = f"Correcting {source_dimension} deviation of {deviation:.3f}"
        
        return CorrectionAction(
            parameter=param_type.value,
            current_value=current_value,
            adjustment=adjustment,
            new_value=new_value,
            reason=reason
        )
    
    def _apply_correction(self, correction: CorrectionAction):
        """Apply correction to current parameters"""
        
        param_type = ParameterType(correction.parameter)
        self.current_parameters[param_type] = correction.new_value
        
        logger.debug(f"Applied correction: {correction.parameter} {correction.current_value:.3f} -> {correction.new_value:.3f}")
    
    def get_current_parameters(self) -> Dict[str, float]:
        """Get current parameter values"""
        
        return {param.value: value for param, value in self.current_parameters.items()}
    
    def reset_parameters(self):
        """Reset all parameters to default values"""
        
        for param_type, param_range in self.parameter_ranges.items():
            self.current_parameters[param_type] = param_range.default_value
        
        logger.info("Reset all parameters to default values")
    
    def get_parameter_statistics(self) -> Dict[str, Union[Dict, int, float]]:
        """Get statistics about parameter adjustments"""
        
        if not self.correction_history:
            return {
                'total_corrections': 0,
                'most_adjusted_parameter': None,
                'average_adjustment': 0.0,
                'parameter_adjustment_counts': {}
            }
        
        # Count adjustments per parameter
        adjustment_counts = {}
        total_adjustment = 0.0
        
        for correction in self.correction_history:
            param = correction.parameter
            adjustment_counts[param] = adjustment_counts.get(param, 0) + 1
            total_adjustment += abs(correction.adjustment)
        
        # Find most adjusted parameter
        most_adjusted = max(adjustment_counts.items(), key=lambda x: x[1])[0] if adjustment_counts else None
        
        return {
            'total_corrections': len(self.correction_history),
            'most_adjusted_parameter': most_adjusted,
            'average_adjustment': total_adjustment / len(self.correction_history) if self.correction_history else 0.0,
            'parameter_adjustment_counts': adjustment_counts,
            'unique_parameters_adjusted': len(adjustment_counts)
        }
    
    def optimize_parameters(
        self,
        feedback_history: List[FeedbackMetrics],
        optimization_target: str = "similarity"
    ) -> Dict[str, float]:
        """Optimize parameters based on historical feedback"""
        
        if len(feedback_history) < 5:
            logger.warning("Insufficient feedback history for optimization")
            return self.get_current_parameters()
        
        # Analyze which parameter adjustments led to better results
        successful_corrections = []
        
        for i, metrics in enumerate(feedback_history):
            if metrics.similarity_score >= 0.9:  # Good performance
                # Look at corrections that led to this
                if i > 0:
                    # Find corrections made before this measurement
                    relevant_corrections = [
                        corr for corr in self.correction_history
                        if abs(corr.adjustment) > 0.01
                    ]
                    successful_corrections.extend(relevant_corrections)
        
        if not successful_corrections:
            logger.info("No successful corrections found for optimization")
            return self.get_current_parameters()
        
        # Calculate optimal parameter values based on successful corrections
        optimized_parameters = self.current_parameters.copy()
        
        for param_type in self.parameter_ranges:
            param_corrections = [
                corr for corr in successful_corrections
                if corr.parameter == param_type.value
            ]
            
            if param_corrections:
                # Average the successful values
                successful_values = [corr.new_value for corr in param_corrections]
                optimized_value = statistics.mean(successful_values)
                
                # Clamp to valid range
                param_range = self.parameter_ranges[param_type]
                optimized_value = max(param_range.min_value, min(param_range.max_value, optimized_value))
                
                optimized_parameters[param_type] = optimized_value
        
        # Apply optimized parameters
        self.current_parameters = optimized_parameters
        
        logger.info(f"Optimized {len([p for p in successful_corrections])} parameters based on feedback")
        
        return self.get_current_parameters()
    
    def validate_parameters(self, parameters: Dict[str, float]) -> List[str]:
        """Validate parameter values"""
        
        errors = []
        
        for param_name, value in parameters.items():
            try:
                param_type = ParameterType(param_name)
                param_range = self.parameter_ranges[param_type]
                
                if value < param_range.min_value or value > param_range.max_value:
                    errors.append(
                        f"{param_name} value {value} outside range [{param_range.min_value}, {param_range.max_value}]"
                    )
            except ValueError:
                errors.append(f"Unknown parameter: {param_name}")
        
        return errors
    
    def export_configuration(self) -> Dict[str, Union[Dict, List]]:
        """Export current configuration"""
        
        return {
            'current_parameters': self.get_current_parameters(),
            'parameter_ranges': {
                param.value: {
                    'min_value': range.min_value,
                    'max_value': range.max_value,
                    'default_value': range.default_value,
                    'step_size': range.step_size
                }
                for param, range in self.parameter_ranges.items()
            },
            'learning_rates': {
                param.value: rate 
                for param, rate in self.learning_rates.items()
            },
            'correction_history': [
                {
                    'parameter': corr.parameter,
                    'current_value': corr.current_value,
                    'adjustment': corr.adjustment,
                    'new_value': corr.new_value,
                    'reason': corr.reason
                }
                for corr in self.correction_history[-20:]  # Last 20 corrections
            ],
            'statistics': self.get_parameter_statistics()
        }
    
    def import_configuration(self, config: Dict[str, Union[Dict, List]]) -> bool:
        """Import configuration from dict"""
        
        try:
            # Import parameters
            if 'current_parameters' in config:
                parameters = config['current_parameters']
                errors = self.validate_parameters(parameters)
                
                if errors:
                    logger.error(f"Invalid parameters in configuration: {errors}")
                    return False
                
                for param_name, value in parameters.items():
                    param_type = ParameterType(param_name)
                    self.current_parameters[param_type] = value
            
            # Import learning rates
            if 'learning_rates' in config:
                learning_rates = config['learning_rates']
                for param_name, rate in learning_rates.items():
                    param_type = ParameterType(param_name)
                    self.learning_rates[param_type] = rate
            
            logger.info("Successfully imported configuration")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import configuration: {str(e)}")
            return False
