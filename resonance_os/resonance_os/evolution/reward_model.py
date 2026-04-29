"""
Reward model for ResonanceOS evolution
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import statistics
from datetime import datetime

from ..core.types import ResonanceVector, StyleProfile, GenerationResult
from ..core.constants import DEFAULT_REWARD_SCALE, DEFAULT_PENALTY_SCALE
from ..core.logging import get_logger, log_performance

logger = get_logger(__name__)


class RewardType(str, Enum):
    """Types of reward components"""
    SIMILARITY = "similarity"
    ORIGINALITY = "originality"
    COHERENCE = "coherence"
    ENGAGEMENT = "engagement"
    DRIFT_CONTROL = "drift_control"
    LENGTH_APPROPRIATENESS = "length_appropriateness"
    TOPIC_RELEVANCE = "topic_relevance"


@dataclass
class RewardComponent:
    """Individual reward component"""
    reward_type: RewardType
    value: float
    weight: float
    description: str


@dataclass
class RewardBreakdown:
    """Detailed breakdown of reward calculation"""
    total_reward: float
    components: List[RewardComponent]
    similarity_score: float
    originality_score: float
    penalties: List[str]
    bonuses: List[str]
    timestamp: datetime


class RewardModel:
    """Calculates rewards for reinforcement learning and evolution"""
    
    def __init__(
        self,
        reward_scale: float = DEFAULT_REWARD_SCALE,
        penalty_scale: float = DEFAULT_PENALTY_SCALE
    ):
        self.reward_scale = reward_scale
        self.penalty_scale = penalty_scale
        
        # Default reward weights
        self.reward_weights = {
            RewardType.SIMILARITY: 0.4,
            RewardType.ORIGINALITY: 0.2,
            RewardType.COHERENCE: 0.15,
            RewardType.ENGAGEMENT: 0.1,
            RewardType.DRIFT_CONTROL: 0.1,
            RewardType.LENGTH_APPROPRIATENESS: 0.05
        }
        
        # Reward history for analysis
        self.reward_history: List[RewardBreakdown] = []
        
        # Thresholds for different reward types
        self.thresholds = {
            'similarity_good': 0.9,
            'similarity_excellent': 0.95,
            'originality_good': 0.7,
            'coherence_good': 0.8,
            'engagement_good': 0.6,
            'drift_acceptable': 0.05
        }
    
    @log_performance
    def calculate_reward(
        self,
        result: GenerationResult,
        target_profile: StyleProfile,
        reference_texts: Optional[List[str]] = None,
        engagement_metrics: Optional[Dict[str, float]] = None
    ) -> RewardBreakdown:
        """Calculate comprehensive reward for generation result"""
        
        components = []
        penalties = []
        bonuses = []
        
        # 1. Similarity reward (primary component)
        similarity_reward = self._calculate_similarity_reward(
            result.metrics.similarity_score, result.metrics.target_similarity
        )
        components.append(similarity_reward)
        
        # 2. Originality reward
        originality_reward = self._calculate_originality_reward(
            result.content, reference_texts or []
        )
        components.append(originality_reward)
        
        # 3. Coherence reward
        coherence_reward = self._calculate_coherence_reward(result.content)
        components.append(coherence_reward)
        
        # 4. Engagement reward
        engagement_reward = self._calculate_engagement_reward(
            result.content, engagement_metrics or {}
        )
        components.append(engagement_reward)
        
        # 5. Drift control reward
        drift_reward = self._calculate_drift_control_reward(result.metrics.drift_rate)
        components.append(drift_reward)
        
        # 6. Length appropriateness reward
        length_reward = self._calculate_length_reward(
            result.tokens_generated, result.config.max_tokens
        )
        components.append(length_reward)
        
        # 7. Topic relevance reward
        topic_reward = self._calculate_topic_relevance_reward(
            result.content, result.config.topic
        )
        components.append(topic_reward)
        
        # Calculate total weighted reward
        total_reward = sum(
            comp.value * comp.weight * self.reward_scale 
            for comp in components
        )
        
        # Apply penalties
        total_penalty = sum(
            self.penalty_scale * self._get_penalty_severity(penalty)
            for penalty in penalties
        )
        
        # Apply bonuses
        total_bonus = sum(
            self.reward_scale * self._get_bonus_amount(bonus)
            for bonus in bonuses
        )
        
        final_reward = total_reward - total_penalty + total_bonus
        
        # Create breakdown
        breakdown = RewardBreakdown(
            total_reward=final_reward,
            components=components,
            similarity_score=result.metrics.similarity_score,
            originality_score=originality_reward.value,
            penalties=penalties,
            bonuses=bonuses,
            timestamp=datetime.now()
        )
        
        # Store in history
        self.reward_history.append(breakdown)
        
        logger.debug(f"Reward calculated: {final_reward:.3f} (similarity: {result.metrics.similarity_score:.3f})")
        
        return breakdown
    
    def _calculate_similarity_reward(
        self,
        similarity_score: float,
        target_similarity: float
    ) -> RewardComponent:
        """Calculate similarity-based reward"""
        
        if similarity_score >= target_similarity:
            # Exceeded target - bonus reward
            reward = 1.0 + (similarity_score - target_similarity) * 2
            description = f"Excellent similarity ({similarity_score:.3f} >= {target_similarity:.3f})"
        elif similarity_score >= self.thresholds['similarity_good']:
            # Good similarity
            reward = similarity_score / target_similarity
            description = f"Good similarity ({similarity_score:.3f})"
        else:
            # Poor similarity - reduced reward
            reward = similarity_score / target_similarity * 0.5
            description = f"Poor similarity ({similarity_score:.3f} < {self.thresholds['similarity_good']:.3f})"
        
        return RewardComponent(
            reward_type=RewardType.SIMILARITY,
            value=min(2.0, max(0.0, reward)),
            weight=self.reward_weights[RewardType.SIMILARITY],
            description=description
        )
    
    def _calculate_originality_reward(
        self,
        content: str,
        reference_texts: List[str]
    ) -> RewardComponent:
        """Calculate originality reward"""
        
        if not reference_texts:
            # No reference texts - assume good originality
            return RewardComponent(
                reward_type=RewardType.ORIGINALITY,
                value=0.8,
                weight=self.reward_weights[RewardType.ORIGINALITY],
                description="No reference texts available"
            )
        
        # Simple originality calculation based on n-gram overlap
        originality_score = self._calculate_ngram_originality(content, reference_texts)
        
        if originality_score >= self.thresholds['originality_good']:
            reward = originality_score
            description = f"Good originality ({originality_score:.3f})"
        else:
            reward = originality_score * 0.7  # Penalty for low originality
            description = f"Low originality ({originality_score:.3f})"
        
        return RewardComponent(
            reward_type=RewardType.ORIGINALITY,
            value=max(0.0, min(1.0, reward)),
            weight=self.reward_weights[RewardType.ORIGINALITY],
            description=description
        )
    
    def _calculate_ngram_originality(self, content: str, reference_texts: List[str]) -> float:
        """Calculate originality based on n-gram overlap"""
        
        # Extract 3-grams from content
        content_ngrams = self._extract_ngrams(content, n=3)
        
        if not content_ngrams:
            return 1.0
        
        # Extract 3-grams from reference texts
        reference_ngrams = set()
        for ref_text in reference_texts:
            reference_ngrams.update(self._extract_ngrams(ref_text, n=3))
        
        # Calculate overlap
        overlapping_ngrams = len(content_ngrams.intersection(reference_ngrams))
        total_content_ngrams = len(content_ngrams)
        
        if total_content_ngrams == 0:
            return 1.0
        
        overlap_ratio = overlapping_ngrams / total_content_ngrams
        originality = 1.0 - overlap_ratio
        
        return max(0.0, originality)
    
    def _extract_ngrams(self, text: str, n: int) -> set:
        """Extract n-grams from text"""
        
        words = text.lower().split()
        ngrams = set()
        
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.add(ngram)
        
        return ngrams
    
    def _calculate_coherence_reward(self, content: str) -> RewardComponent:
        """Calculate coherence reward based on text structure"""
        
        # Simple coherence metrics
        sentences = content.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return RewardComponent(
                reward_type=RewardType.COHERENCE,
                value=0.5,
                weight=self.reward_weights[RewardType.COHERENCE],
                description="Too short for coherence analysis"
            )
        
        # Calculate sentence length variance (lower is more coherent)
        sentence_lengths = [len(s.split()) for s in sentences]
        length_variance = statistics.variance(sentence_lengths) if len(sentence_lengths) > 1 else 0
        
        # Normalize variance score (lower variance = higher coherence)
        max_variance = 100.0  # Arbitrary maximum
        coherence_score = 1.0 - (length_variance / max_variance)
        coherence_score = max(0.0, min(1.0, coherence_score))
        
        # Check for transition words
        transition_words = {'however', 'therefore', 'furthermore', 'moreover', 'consequently', 'meanwhile'}
        transition_count = sum(1 for s in sentences if any(word in s.lower() for word in transition_words))
        transition_ratio = transition_count / len(sentences)
        
        # Combine metrics
        final_coherence = (coherence_score * 0.7) + (transition_ratio * 0.3)
        
        if final_coherence >= self.thresholds['coherence_good']:
            description = f"Good coherence ({final_coherence:.3f})"
        else:
            description = f"Poor coherence ({final_coherence:.3f})"
        
        return RewardComponent(
            reward_type=RewardType.COHERENCE,
            value=final_coherence,
            weight=self.reward_weights[RewardType.COHERENCE],
            description=description
        )
    
    def _calculate_engagement_reward(
        self,
        content: str,
        engagement_metrics: Dict[str, float]
    ) -> RewardComponent:
        """Calculate engagement reward"""
        
        if not engagement_metrics:
            # Fallback engagement calculation
            engagement_score = self._calculate_fallback_engagement(content)
        else:
            # Use provided metrics
            engagement_score = statistics.mean(engagement_metrics.values())
        
        if engagement_score >= self.thresholds['engagement_good']:
            description = f"Good engagement ({engagement_score:.3f})"
        else:
            description = f"Poor engagement ({engagement_score:.3f})"
        
        return RewardComponent(
            reward_type=RewardType.ENGAGEMENT,
            value=max(0.0, min(1.0, engagement_score)),
            weight=self.reward_weights[RewardType.ENGAGEMENT],
            description=description
        )
    
    def _calculate_fallback_engagement(self, content: str) -> float:
        """Calculate engagement score when no metrics provided"""
        
        # Simple engagement indicators
        sentences = content.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Question engagement
        questions = sum(1 for s in sentences if '?' in s)
        question_ratio = questions / len(sentences)
        
        # Exclamation engagement
        exclamations = sum(1 for s in sentences if '!' in s)
        exclamation_ratio = exclamations / len(sentences)
        
        # Average sentence length (shorter = more engaging)
        avg_length = statistics.mean([len(s.split()) for s in sentences])
        length_score = max(0.0, 1.0 - (avg_length / 20.0))  # Normalize to 20 words max
        
        # Combine metrics
        engagement = (question_ratio * 0.3) + (exclamation_ratio * 0.2) + (length_score * 0.5)
        
        return max(0.0, min(1.0, engagement))
    
    def _calculate_drift_control_reward(self, drift_rate: float) -> RewardComponent:
        """Calculate drift control reward"""
        
        if drift_rate <= self.thresholds['drift_acceptable']:
            reward = 1.0
            description = f"Excellent drift control ({drift_rate:.3f})"
        elif drift_rate <= self.thresholds['drift_acceptable'] * 2:
            reward = 0.7
            description = f"Acceptable drift ({drift_rate:.3f})"
        else:
            reward = max(0.0, 1.0 - (drift_rate / 0.2))  # Penalty for high drift
            description = f"Poor drift control ({drift_rate:.3f})"
        
        return RewardComponent(
            reward_type=RewardType.DRIFT_CONTROL,
            value=reward,
            weight=self.reward_weights[RewardType.DRIFT_CONTROL],
            description=description
        )
    
    def _calculate_length_reward(self, tokens_generated: int, max_tokens: int) -> RewardComponent:
        """Calculate length appropriateness reward"""
        
        if tokens_generated == 0:
            return RewardComponent(
                reward_type=RewardType.LENGTH_APPROPRIATENESS,
                value=0.0,
                weight=self.reward_weights[RewardType.LENGTH_APPROPRIATENESS],
                description="No content generated"
            )
        
        # Ideal range is 70-90% of max tokens
        ideal_min = max_tokens * 0.7
        ideal_max = max_tokens * 0.9
        
        if ideal_min <= tokens_generated <= ideal_max:
            reward = 1.0
            description = f"Ideal length ({tokens_generated} tokens)"
        elif tokens_generated < ideal_min:
            reward = tokens_generated / ideal_min
            description = f"Too short ({tokens_generated} tokens)"
        else:
            reward = max(0.0, 1.0 - ((tokens_generated - ideal_max) / (max_tokens - ideal_max)))
            description = f"Too long ({tokens_generated} tokens)"
        
        return RewardComponent(
            reward_type=RewardType.LENGTH_APPROPRIATENESS,
            value=reward,
            weight=self.reward_weights[RewardType.LENGTH_APPROPRIATENESS],
            description=description
        )
    
    def _calculate_topic_relevance_reward(self, content: str, topic: str) -> RewardComponent:
        """Calculate topic relevance reward"""
        
        # Simple keyword matching for relevance
        topic_words = set(topic.lower().split())
        content_words = set(content.lower().split())
        
        if not topic_words:
            return RewardComponent(
                reward_type=RewardType.TOPIC_RELEVANCE,
                value=0.5,
                weight=0.0,  # Not weighted in total
                description="No topic words identified"
            )
        
        # Calculate overlap
        overlapping_words = len(topic_words.intersection(content_words))
        relevance_score = overlapping_words / len(topic_words)
        
        # Bonus for multiple mentions
        topic_mentions = sum(content.lower().count(word) for word in topic_words)
        mention_bonus = min(0.3, topic_mentions / len(content.split()) * 10)
        
        final_relevance = min(1.0, relevance_score + mention_bonus)
        
        return RewardComponent(
            reward_type=RewardType.TOPIC_RELEVANCE,
            value=final_relevance,
            weight=0.0,  # Not weighted in total
            description=f"Topic relevance ({final_relevance:.3f})"
        )
    
    def _get_penalty_severity(self, penalty: str) -> float:
        """Get penalty severity for different penalty types"""
        
        penalty_severities = {
            'low_similarity': 0.5,
            'high_drift': 0.3,
            'plagiarism_risk': 1.0,
            'incoherent': 0.4,
            'off_topic': 0.3,
            'too_short': 0.2,
            'too_long': 0.1
        }
        
        return penalty_severities.get(penalty, 0.2)
    
    def _get_bonus_amount(self, bonus: str) -> float:
        """Get bonus amount for different bonus types"""
        
        bonus_amounts = {
            'excellent_similarity': 0.3,
            'perfect_originality': 0.2,
            'high_engagement': 0.2,
            'perfect_coherence': 0.1,
            'zero_drift': 0.1,
            'ideal_length': 0.05
        }
        
        return bonus_amounts.get(bonus, 0.05)
    
    def get_reward_statistics(self) -> Dict[str, Union[float, int, List]]:
        """Get statistics about reward calculations"""
        
        if not self.reward_history:
            return {
                'total_rewards': 0,
                'average_reward': 0.0,
                'max_reward': 0.0,
                'min_reward': 0.0,
                'reward_distribution': [],
                'component_averages': {}
            }
        
        rewards = [r.total_reward for r in self.reward_history]
        
        # Calculate component averages
        component_sums = {}
        component_counts = {}
        
        for breakdown in self.reward_history:
            for component in breakdown.components:
                comp_type = component.reward_type.value
                component_sums[comp_type] = component_sums.get(comp_type, 0.0) + component.value
                component_counts[comp_type] = component_counts.get(comp_type, 0) + 1
        
        component_averages = {
            comp_type: component_sums[comp_type] / component_counts[comp_type]
            for comp_type in component_sums
        }
        
        return {
            'total_rewards': len(self.reward_history),
            'average_reward': statistics.mean(rewards),
            'max_reward': max(rewards),
            'min_reward': min(rewards),
            'reward_distribution': rewards,
            'component_averages': component_averages,
            'recent_average': statistics.mean(rewards[-10:]) if len(rewards) >= 10 else statistics.mean(rewards)
        }
    
    def update_weights(self, new_weights: Dict[RewardType, float]):
        """Update reward weights"""
        
        # Validate weights sum to 1.0
        total_weight = sum(new_weights.values())
        if abs(total_weight - 1.0) > 0.01:
            logger.warning(f"Weights sum to {total_weight:.3f}, normalizing to 1.0")
            new_weights = {
                comp_type: weight / total_weight 
                for comp_type, weight in new_weights.items()
            }
        
        self.reward_weights = new_weights
        logger.info("Updated reward weights")
    
    def export_reward_model(self) -> Dict[str, Union[Dict, List]]:
        """Export reward model configuration and data"""
        
        return {
            'configuration': {
                'reward_scale': self.reward_scale,
                'penalty_scale': self.penalty_scale,
                'reward_weights': {
                    comp_type.value: weight 
                    for comp_type, weight in self.reward_weights.items()
                },
                'thresholds': self.thresholds
            },
            'statistics': self.get_reward_statistics(),
            'recent_rewards': [
                {
                    'total_reward': r.total_reward,
                    'similarity_score': r.similarity_score,
                    'originality_score': r.originality_score,
                    'timestamp': r.timestamp.isoformat()
                }
                for r in self.reward_history[-20:]  # Last 20 rewards
            ]
        }
    
    def import_reward_model(self, config: Dict[str, Union[Dict, List]]) -> bool:
        """Import reward model configuration"""
        
        try:
            if 'configuration' in config:
                config_dict = config['configuration']
                
                # Import scales
                if 'reward_scale' in config_dict:
                    self.reward_scale = config_dict['reward_scale']
                if 'penalty_scale' in config_dict:
                    self.penalty_scale = config_dict['penalty_scale']
                
                # Import weights
                if 'reward_weights' in config_dict:
                    weights = config_dict['reward_weights']
                    new_weights = {}
                    for comp_name, weight in weights.items():
                        try:
                            comp_type = RewardType(comp_name)
                            new_weights[comp_type] = weight
                        except ValueError:
                            logger.warning(f"Unknown reward type: {comp_name}")
                    
                    if new_weights:
                        self.update_weights(new_weights)
                
                # Import thresholds
                if 'thresholds' in config_dict:
                    self.thresholds.update(config_dict['thresholds'])
            
            logger.info("Successfully imported reward model configuration")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import reward model: {str(e)}")
            return False
