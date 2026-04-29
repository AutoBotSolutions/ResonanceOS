"""
Similarity metrics for ResonanceOS
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from scipy import stats
from scipy.spatial.distance import cosine, euclidean, cityblock
from sklearn.metrics.pairwise import cosine_similarity
import warnings

from ..core.types import ResonanceVector, SimilarityMethod
from ..core.constants import SIMILARITY_METHODS
from ..core.logging import get_logger, log_performance

logger = get_logger(__name__)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


class SimilarityCalculator:
    """Calculates similarity between resonance vectors"""
    
    def __init__(self, default_method: SimilarityMethod = SimilarityMethod.COSINE):
        self.default_method = default_method
        self._validate_method(default_method)
    
    def _validate_method(self, method: SimilarityMethod):
        """Validate similarity method"""
        if method not in SIMILARITY_METHODS:
            raise ValueError(f"Unsupported similarity method: {method}")
    
    @log_performance
    def calculate_similarity(
        self,
        vector1: Union[ResonanceVector, np.ndarray, List[float]],
        vector2: Union[ResonanceVector, np.ndarray, List[float]],
        method: Optional[SimilarityMethod] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> float:
        """Calculate similarity between two resonance vectors"""
        
        method = method or self.default_method
        self._validate_method(method)
        
        # Convert to numpy arrays
        arr1 = self._to_numpy(vector1)
        arr2 = self._to_numpy(vector2)
        
        # Validate dimensions
        if arr1.shape != arr2.shape:
            raise ValueError(f"Vector dimensions must match: {arr1.shape} vs {arr2.shape}")
        
        # Apply weights if provided
        if weights:
            arr1, arr2 = self._apply_weights(arr1, arr2, weights)
        
        # Calculate similarity based on method
        if method == SimilarityMethod.COSINE:
            return self._cosine_similarity(arr1, arr2)
        elif method == SimilarityMethod.EUCLIDEAN:
            return self._euclidean_similarity(arr1, arr2)
        elif method == SimilarityMethod.MANHATTAN:
            return self._manhattan_similarity(arr1, arr2)
        elif method == SimilarityMethod.PEARSON:
            return self._pearson_similarity(arr1, arr2)
        elif method == SimilarityMethod.SPEARMAN:
            return self._spearman_similarity(arr1, arr2)
        else:
            raise ValueError(f"Method {method} not implemented")
    
    def _to_numpy(self, vector: Union[ResonanceVector, np.ndarray, List[float]]) -> np.ndarray:
        """Convert vector to numpy array"""
        
        if isinstance(vector, ResonanceVector):
            return np.array(vector.values)
        elif isinstance(vector, list):
            return np.array(vector)
        elif isinstance(vector, np.ndarray):
            return vector
        else:
            raise ValueError(f"Unsupported vector type: {type(vector)}")
    
    def _apply_weights(
        self,
        arr1: np.ndarray,
        arr2: np.ndarray,
        weights: Dict[str, float]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Apply weights to vectors"""
        
        if isinstance(weights, dict):
            # Convert dict weights to array
            weight_values = list(weights.values())
            if len(weight_values) != len(arr1):
                raise ValueError(f"Weight count ({len(weight_values)}) must match vector dimensions ({len(arr1)})")
            weight_array = np.array(weight_values)
        else:
            weight_array = np.array(weights)
        
        # Apply weights
        weighted_arr1 = arr1 * weight_array
        weighted_arr2 = arr2 * weight_array
        
        return weighted_arr1, weighted_arr2
    
    def _cosine_similarity(self, arr1: np.ndarray, arr2: np.ndarray) -> float:
        """Calculate cosine similarity"""
        
        # Handle zero vectors
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(arr1, arr2) / (norm1 * norm2)
        
        # Ensure result is in [0, 1] range
        return max(0.0, min(1.0, similarity))
    
    def _euclidean_similarity(self, arr1: np.ndarray, arr2: np.ndarray) -> float:
        """Calculate euclidean distance similarity"""
        
        distance = euclidean(arr1, arr2)
        
        # Convert distance to similarity (inverse relationship)
        # Maximum possible distance is sqrt(n) where n is number of dimensions
        max_distance = np.sqrt(len(arr1))
        similarity = 1.0 - (distance / max_distance)
        
        return max(0.0, min(1.0, similarity))
    
    def _manhattan_similarity(self, arr1: np.ndarray, arr2: np.ndarray) -> float:
        """Calculate manhattan distance similarity"""
        
        distance = cityblock(arr1, arr2)
        
        # Convert distance to similarity
        # Maximum possible manhattan distance is 2 * n where n is number of dimensions (for [0,1] range)
        max_distance = 2.0 * len(arr1)
        similarity = 1.0 - (distance / max_distance)
        
        return max(0.0, min(1.0, similarity))
    
    def _pearson_similarity(self, arr1: np.ndarray, arr2: np.ndarray) -> float:
        """Calculate Pearson correlation similarity"""
        
        if len(arr1) < 2:
            return 0.0
        
        try:
            correlation, _ = stats.pearsonr(arr1, arr2)
            
            # Handle NaN results
            if np.isnan(correlation):
                return 0.0
            
            # Convert from [-1, 1] to [0, 1]
            similarity = (correlation + 1.0) / 2.0
            
            return max(0.0, min(1.0, similarity))
        
        except Exception as e:
            logger.warning(f"Pearson correlation failed: {str(e)}")
            return 0.0
    
    def _spearman_similarity(self, arr1: np.ndarray, arr2: np.ndarray) -> float:
        """Calculate Spearman correlation similarity"""
        
        if len(arr1) < 2:
            return 0.0
        
        try:
            correlation, _ = stats.spearmanr(arr1, arr2)
            
            # Handle NaN results
            if np.isnan(correlation):
                return 0.0
            
            # Convert from [-1, 1] to [0, 1]
            similarity = (correlation + 1.0) / 2.0
            
            return max(0.0, min(1.0, similarity))
        
        except Exception as e:
            logger.warning(f"Spearman correlation failed: {str(e)}")
            return 0.0
    
    def calculate_batch_similarity(
        self,
        target_vector: Union[ResonanceVector, np.ndarray, List[float]],
        candidate_vectors: List[Union[ResonanceVector, np.ndarray, List[float]]],
        method: Optional[SimilarityMethod] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> List[float]:
        """Calculate similarity between target vector and multiple candidates"""
        
        similarities = []
        
        for candidate in candidate_vectors:
            similarity = self.calculate_similarity(
                target_vector, candidate, method, weights
            )
            similarities.append(similarity)
        
        return similarities
    
    def find_most_similar(
        self,
        target_vector: Union[ResonanceVector, np.ndarray, List[float]],
        candidate_vectors: List[Union[ResonanceVector, np.ndarray, List[float]]],
        method: Optional[SimilarityMethod] = None,
        weights: Optional[Dict[str, float]] = None,
        top_k: int = 1
    ) -> List[Tuple[int, float]]:
        """Find most similar vectors to target"""
        
        similarities = self.calculate_batch_similarity(
            target_vector, candidate_vectors, method, weights
        )
        
        # Get indices of top-k most similar
        indexed_similarities = [(i, sim) for i, sim in enumerate(similarities)]
        indexed_similarities.sort(key=lambda x: x[1], reverse=True)
        
        return indexed_similarities[:top_k]
    
    def calculate_dimension_contributions(
        self,
        vector1: Union[ResonanceVector, np.ndarray, List[float]],
        vector2: Union[ResonanceVector, np.ndarray, List[float]],
        method: SimilarityMethod = SimilarityMethod.COSINE
    ) -> Dict[str, float]:
        """Calculate contribution of each dimension to overall similarity"""
        
        arr1 = self._to_numpy(vector1)
        arr2 = self._to_numpy(vector2)
        
        if arr1.shape != arr2.shape:
            raise ValueError("Vector dimensions must match")
        
        contributions = {}
        
        for i in range(len(arr1)):
            # Create vectors with only this dimension
            dim_arr1 = np.zeros_like(arr1)
            dim_arr2 = np.zeros_like(arr2)
            dim_arr1[i] = arr1[i]
            dim_arr2[i] = arr2[i]
            
            # Calculate similarity for this dimension only
            dim_similarity = self.calculate_similarity(
                dim_arr1, dim_arr2, method
            )
            
            contributions[f"dimension_{i}"] = dim_similarity
        
        return contributions
    
    def get_similarity_statistics(
        self,
        similarities: List[float]
    ) -> Dict[str, float]:
        """Calculate statistics for similarity scores"""
        
        if not similarities:
            return {
                'mean': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'median': 0.0,
                'count': 0
            }
        
        return {
            'mean': np.mean(similarities),
            'std': np.std(similarities),
            'min': np.min(similarities),
            'max': np.max(similarities),
            'median': np.median(similarities),
            'count': len(similarities)
        }
    
    def validate_similarity_threshold(
        self,
        similarity: float,
        threshold: float = 0.92
    ) -> bool:
        """Check if similarity meets threshold"""
        
        return similarity >= threshold
    
    def get_recommended_threshold(
        self,
        similarities: List[float],
        percentile: float = 90.0
    ) -> float:
        """Get recommended threshold based on similarity distribution"""
        
        if not similarities:
            return 0.92  # Default threshold
        
        return np.percentile(similarities, percentile)


class MultiMethodSimilarity:
    """Calculates similarity using multiple methods and combines results"""
    
    def __init__(self, methods: List[SimilarityMethod], weights: Optional[List[float]] = None):
        self.methods = methods
        self.weights = weights or [1.0 / len(methods)] * len(methods)
        
        if len(self.methods) != len(self.weights):
            raise ValueError("Methods and weights must have same length")
        
        if abs(sum(self.weights) - 1.0) > 0.001:
            raise ValueError("Weights must sum to 1.0")
        
        self.calculators = {method: SimilarityCalculator(method) for method in methods}
    
    def calculate_combined_similarity(
        self,
        vector1: Union[ResonanceVector, np.ndarray, List[float]],
        vector2: Union[ResonanceVector, np.ndarray, List[float]]
    ) -> Dict[str, Union[float, Dict[str, float]]]:
        """Calculate combined similarity using multiple methods"""
        
        results = {}
        
        # Calculate similarity for each method
        method_similarities = {}
        for method, calculator in self.calculators.items():
            similarity = calculator.calculate_similarity(vector1, vector2)
            method_similarities[method.value] = similarity
        
        # Calculate weighted average
        weighted_similarity = sum(
            similarity * weight 
            for similarity, weight in zip(method_similarities.values(), self.weights)
        )
        
        results['individual'] = method_similarities
        results['combined'] = weighted_similarity
        results['weights'] = {method.value: weight for method, weight in zip(self.methods, self.weights)}
        
        return results
    
    def get_method_consensus(
        self,
        vector1: Union[ResonanceVector, np.ndarray, List[float]],
        vector2: Union[ResonanceVector, np.ndarray, List[float]],
        threshold: float = 0.92
    ) -> Dict[str, Union[int, float, bool]]:
        """Get consensus among methods about whether similarity meets threshold"""
        
        results = self.calculate_combined_similarity(vector1, vector2)
        
        individual_results = results['individual']
        
        # Count methods that meet threshold
        methods_meeting_threshold = sum(
            1 for similarity in individual_results.values() 
            if similarity >= threshold
        )
        
        consensus = methods_meeting_threshold / len(self.methods)
        
        return {
            'methods_meeting_threshold': methods_meeting_threshold,
            'total_methods': len(self.methods),
            'consensus_ratio': consensus,
            'meets_threshold': consensus >= 0.5,  # Majority consensus
            'combined_score': results['combined']
        }
