"""
Tone evolver for ResonanceOS
"""

import numpy as np
import random
from typing import Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
import statistics
from datetime import datetime
import json

from ..core.types import StyleProfile, ResonanceVector, GenerationResult
from ..core.constants import RESONANCE_DIMENSIONS, EVOLUTION_GENERATIONS, EVOLUTION_POPULATION_SIZE
from ..core.logging import get_logger, log_performance
from .reward_model import RewardModel, RewardBreakdown

logger = get_logger(__name__)


class EvolutionStrategy(str, Enum):
    """Evolution strategies"""
    GENETIC_ALGORITHM = "genetic_algorithm"
    PARTICLE_SWARM = "particle_swarm"
    SIMULATED_ANNEALING = "simulated_annealing"
    BAYESIAN_OPTIMIZATION = "bayesian_optimization"


class SelectionMethod(str, Enum):
    """Selection methods for evolution"""
    TOURNAMENT = "tournament"
    ROULETTE = "roulette"
    RANK = "rank"
    ELITISM = "elitism"


@dataclass
class EvolutionConfig:
    """Configuration for tone evolution"""
    generations: int = EVOLUTION_GENERATIONS
    population_size: int = EVOLUTION_POPULATION_SIZE
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    elite_size: int = 2
    strategy: EvolutionStrategy = EvolutionStrategy.GENETIC_ALGORITHM
    selection_method: SelectionMethod = SelectionMethod.TOURNAMENT
    convergence_threshold: float = 0.001
    max_stagnant_generations: int = 20


@dataclass
class Individual:
    """Individual in evolution population"""
    resonance_vector: ResonanceVector
    fitness: float
    generation: int
    parent_ids: List[int]
    mutations: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'resonance_vector': self.resonance_vector.dict(),
            'fitness': self.fitness,
            'generation': self.generation,
            'parent_ids': self.parent_ids,
            'mutations': self.mutations
        }


class ToneEvolver:
    """Evolves tone profiles using genetic algorithms and other optimization methods"""
    
    def __init__(
        self,
        reward_model: Optional[RewardModel] = None,
        config: Optional[EvolutionConfig] = None
    ):
        self.reward_model = reward_model or RewardModel()
        self.config = config or EvolutionConfig()
        
        # Evolution state
        self.population: List[Individual] = []
        self.generation_count = 0
        self.best_individual: Optional[Individual] = None
        self.evolution_history: List[Dict] = []
        
        # Convergence tracking
        self.fitness_history: List[float] = []
        self.stagnant_count = 0
        self.converged = False
        
        # Callback for fitness evaluation
        self.fitness_evaluator: Optional[Callable] = None
    
    def set_fitness_evaluator(self, evaluator: Callable):
        """Set external fitness evaluation function"""
        self.fitness_evaluator = evaluator
        logger.info("Set external fitness evaluator")
    
    @log_performance
    def evolve_profile(
        self,
        initial_profile: StyleProfile,
        target_topics: List[str],
        progress_callback: Optional[Callable] = None
    ) -> StyleProfile:
        """Evolve a profile to improve performance on target topics"""
        
        logger.info(f"Starting evolution of profile '{initial_profile.name}'")
        
        # Initialize population
        self._initialize_population(initial_profile)
        
        # Evolution loop
        for generation in range(self.config.generations):
            self.generation_count = generation + 1
            
            # Evaluate fitness
            self._evaluate_population(target_topics)
            
            # Track best individual
            current_best = max(self.population, key=lambda ind: ind.fitness)
            if self.best_individual is None or current_best.fitness > self.best_individual.fitness:
                self.best_individual = current_best
                self.stagnant_count = 0
            else:
                self.stagnant_count += 1
            
            # Check convergence
            if self._check_convergence():
                logger.info(f"Evolution converged at generation {generation + 1}")
                break
            
            # Selection
            selected = self._selection()
            
            # Crossover and mutation
            new_population = self._crossover_and_mutation(selected)
            
            # Replace population
            self.population = new_population
            
            # Record generation statistics
            self._record_generation_stats()
            
            # Progress callback
            if progress_callback:
                progress_callback({
                    'generation': generation + 1,
                    'best_fitness': self.best_individual.fitness,
                    'average_fitness': statistics.mean([ind.fitness for ind in self.population]),
                    'stagnant_count': self.stagnant_count
                })
        
        # Create evolved profile
        evolved_profile = self._create_evolved_profile(initial_profile)
        
        logger.info(f"Evolution completed: {self.generation_count} generations, best fitness: {self.best_individual.fitness:.3f}")
        
        return evolved_profile
    
    def _initialize_population(self, initial_profile: StyleProfile):
        """Initialize evolution population"""
        
        self.population = []
        
        # Create initial individual (exact copy of initial profile)
        initial_individual = Individual(
            resonance_vector=initial_profile.resonance_vector,
            fitness=0.0,
            generation=0,
            parent_ids=[],
            mutations=[]
        )
        self.population.append(initial_individual)
        
        # Create random variations
        for i in range(1, self.config.population_size):
            mutated_vector = self._mutate_vector(initial_profile.resonance_vector, mutation_strength=0.2)
            
            individual = Individual(
                resonance_vector=mutated_vector,
                fitness=0.0,
                generation=0,
                parent_ids=[0],  # All start from initial
                mutations=[f"initial_mutation_{i}"]
            )
            self.population.append(individual)
        
        logger.info(f"Initialized population with {len(self.population)} individuals")
    
    def _evaluate_population(self, target_topics: List[str]):
        """Evaluate fitness of all individuals"""
        
        for individual in self.population:
            if self.fitness_evaluator:
                # Use external evaluator
                try:
                    fitness = self.fitness_evaluator(individual.resonance_vector, target_topics)
                    individual.fitness = fitness
                except Exception as e:
                    logger.error(f"External fitness evaluation failed: {str(e)}")
                    individual.fitness = self._default_fitness_evaluation(individual.resonance_vector)
            else:
                # Use default evaluation
                individual.fitness = self._default_fitness_evaluation(individual.resonance_vector)
    
    def _default_fitness_evaluation(self, resonance_vector: ResonanceVector) -> float:
        """Default fitness evaluation when no external evaluator provided"""
        
        # Simple fitness based on vector properties
        values = np.array(resonance_vector.values)
        
        # Reward balanced vectors (not too extreme)
        balance_score = 1.0 - np.std(values)
        
        # reward diversity (not all the same)
        diversity_score = np.std(values)
        
        # Reward reasonable values (not all 0 or 1)
        zero_ratio = np.sum(values == 0) / len(values)
        one_ratio = np.sum(values == 1) / len(values)
        reasonable_score = 1.0 - (zero_ratio + one_ratio)
        
        # Combine scores
        fitness = (balance_score * 0.4) + (diversity_score * 0.3) + (reasonable_score * 0.3)
        
        return max(0.0, min(1.0, fitness))
    
    def _selection(self) -> List[Individual]:
        """Select individuals for reproduction"""
        
        if self.config.selection_method == SelectionMethod.TOURNAMENT:
            return self._tournament_selection()
        elif self.config.selection_method == SelectionMethod.ROULETTE:
            return self._roulette_selection()
        elif self.config.selection_method == SelectionMethod.RANK:
            return self._rank_selection()
        elif self.config.selection_method == SelectionMethod.ELITISM:
            return self._elitism_selection()
        else:
            return self._tournament_selection()
    
    def _tournament_selection(self) -> List[Individual]:
        """Tournament selection"""
        
        selected = []
        tournament_size = 3
        
        # Select elite individuals
        elite_count = min(self.config.elite_size, len(self.population))
        elite = sorted(self.population, key=lambda ind: ind.fitness, reverse=True)[:elite_count]
        selected.extend(elite)
        
        # Fill remaining slots with tournament winners
        while len(selected) < self.config.population_size:
            tournament = random.sample(self.population, min(tournament_size, len(self.population)))
            winner = max(tournament, key=lambda ind: ind.fitness)
            selected.append(winner)
        
        return selected[:self.config.population_size]
    
    def _roulette_selection(self) -> List[Individual]:
        """Roulette wheel selection"""
        
        # Calculate selection probabilities
        total_fitness = sum(ind.fitness for ind in self.population)
        if total_fitness == 0:
            # All have zero fitness, use uniform selection
            probabilities = [1.0 / len(self.population)] * len(self.population)
        else:
            probabilities = [ind.fitness / total_fitness for ind in self.population]
        
        # Select individuals
        selected = []
        for _ in range(self.config.population_size):
            selected_idx = np.random.choice(len(self.population), p=probabilities)
            selected.append(self.population[selected_idx])
        
        return selected
    
    def _rank_selection(self) -> List[Individual]:
        """Rank-based selection"""
        
        # Sort by fitness
        sorted_population = sorted(self.population, key=lambda ind: ind.fitness, reverse=True)
        
        # Assign ranks and probabilities
        ranks = list(range(1, len(sorted_population) + 1))
        total_ranks = sum(ranks)
        probabilities = [rank / total_ranks for rank in ranks]
        
        # Select individuals
        selected = []
        for _ in range(self.config.population_size):
            selected_idx = np.random.choice(len(sorted_population), p=probabilities)
            selected.append(sorted_population[selected_idx])
        
        return selected
    
    def _elitism_selection(self) -> List[Individual]:
        """Elitism selection (keep best individuals)"""
        
        # Sort by fitness and select top individuals
        sorted_population = sorted(self.population, key=lambda ind: ind.fitness, reverse=True)
        elite_size = min(self.config.elite_size, len(sorted_population))
        
        elite = sorted_population[:elite_size]
        
        # Fill remaining with copies of elite (with small mutations)
        selected = list(elite)
        while len(selected) < self.config.population_size:
            elite_copy = random.choice(elite)
            mutated_vector = self._mutate_vector(elite_copy.resonance_vector, mutation_strength=0.05)
            
            mutated_individual = Individual(
                resonance_vector=mutated_vector,
                fitness=0.0,
                elite_copy.generation,
                parent_ids=[id(elite_copy)],
                mutations=["elitism_mutation"]
            )
            selected.append(mutated_individual)
        
        return selected[:self.config.population_size]
    
    def _crossover_and_mutation(self, selected: List[Individual]) -> List[Individual]:
        """Perform crossover and mutation to create new generation"""
        
        new_population = []
        
        # Keep elite individuals
        elite_count = min(self.config.elite_size, len(selected))
        elite = sorted(selected, key=lambda ind: ind.fitness, reverse=True)[:elite_count]
        
        for elite_individual in elite:
            new_individual = Individual(
                resonance_vector=elite_individual.resonance_vector,
                fitness=0.0,
                generation=self.generation_count,
                parent_ids=[id(elite_individual)],
                mutations=[]
            )
            new_population.append(new_individual)
        
        # Create offspring through crossover
        while len(new_population) < self.config.population_size:
            if random.random() < self.config.crossover_rate and len(selected) >= 2:
                # Crossover
                parent1, parent2 = random.sample(selected, 2)
                child_vector = self._crossover_vectors(parent1.resonance_vector, parent2.resonance_vector)
                
                child = Individual(
                    resonance_vector=child_vector,
                    fitness=0.0,
                    generation=self.generation_count,
                    parent_ids=[id(parent1), id(parent2)],
                    mutations=["crossover"]
                )
            else:
                # Just mutation
                parent = random.choice(selected)
                child_vector = self._mutate_vector(parent.resonance_vector)
                
                child = Individual(
                    resonance_vector=child_vector,
                    fitness=0.0,
                    generation=self.generation_count,
                    parent_ids=[id(parent)],
                    mutations=["mutation"]
                )
            
            new_population.append(child)
        
        return new_population[:self.config.population_size]
    
    def _crossover_vectors(
        self,
        vector1: ResonanceVector,
        vector2: ResonanceVector
    ) -> ResonanceVector:
        """Crossover two resonance vectors"""
        
        values1 = np.array(vector1.values)
        values2 = np.array(vector2.values)
        
        # Uniform crossover
        mask = np.random.random(len(values1)) < 0.5
        child_values = np.where(mask, values1, values2)
        
        # Blend some values (averaging)
        blend_mask = np.random.random(len(values1)) < 0.1
        child_values = np.where(blend_mask, (values1 + values2) / 2, child_values)
        
        return ResonanceVector(
            values=child_values.tolist(),
            dimensions=vector1.dimensions,
            confidence=(vector1.confidence + vector2.confidence) / 2
        )
    
    def _mutate_vector(
        self,
        vector: ResonanceVector,
        mutation_strength: Optional[float] = None
    ) -> ResonanceVector:
        """Mutate a resonance vector"""
        
        if mutation_strength is None:
            mutation_strength = self.config.mutation_rate
        
        values = np.array(vector.values)
        
        # Random mutation
        mutation_mask = np.random.random(len(values)) < mutation_strength
        
        # Apply mutations
        for i in range(len(values)):
            if mutation_mask[i]:
                # Random walk mutation
                mutation = np.random.normal(0, 0.1)
                values[i] += mutation
                
                # Clamp to [0, 1]
                values[i] = max(0.0, min(1.0, values[i]))
        
        return ResonanceVector(
            values=values.tolist(),
            dimensions=vector.dimensions,
            confidence=vector.confidence * 0.95  # Slightly reduce confidence
        )
    
    def _check_convergence(self) -> bool:
        """Check if evolution has converged"""
        
        if len(self.population) == 0:
            return False
        
        # Check fitness convergence
        current_fitnesses = [ind.fitness for ind in self.population]
        avg_fitness = statistics.mean(current_fitnesses)
        
        if len(self.fitness_history) > 0:
            fitness_change = abs(avg_fitness - self.fitness_history[-1])
            if fitness_change < self.config.convergence_threshold:
                return True
        
        self.fitness_history.append(avg_fitness)
        
        # Check stagnation
        if self.stagnant_count >= self.config.max_stagnant_generations:
            return True
        
        return False
    
    def _record_generation_stats(self):
        """Record statistics for current generation"""
        
        fitnesses = [ind.fitness for ind in self.population]
        
        stats = {
            'generation': self.generation_count,
            'best_fitness': max(fitnesses),
            'average_fitness': statistics.mean(fitnesses),
            'worst_fitness': min(fitnesses),
            'fitness_std': statistics.stdev(fitnesses) if len(fitnesses) > 1 else 0.0,
            'population_size': len(self.population),
            'stagnant_count': self.stagnant_count,
            'converged': self.converged
        }
        
        self.evolution_history.append(stats)
    
    def _create_evolved_profile(self, original_profile: StyleProfile) -> StyleProfile:
        """Create evolved profile from best individual"""
        
        if not self.best_individual:
            logger.warning("No best individual found, returning original profile")
            return original_profile
        
        # Create evolved profile
        evolved_profile = StyleProfile(
            name=f"{original_profile.name}_evolved",
            description=f"Evolved from {original_profile.name} over {self.generation_count} generations",
            resonance_vector=self.best_individual.resonance_vector,
            emotional_curve=original_profile.emotional_curve.copy(),
            cadence_pattern=original_profile.cadence_pattern.copy(),
            abstraction_preference=original_profile.abstraction_preference,
            metadata={
                **original_profile.metadata,
                'evolution': {
                    'generations': self.generation_count,
                    'final_fitness': self.best_individual.fitness,
                    'parent_ids': self.best_individual.parent_ids,
                    'mutations': self.best_individual.mutations,
                    'evolved_at': datetime.now().isoformat()
                }
            },
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return evolved_profile
    
    def get_evolution_statistics(self) -> Dict[str, Union[int, float, List, Dict]]:
        """Get comprehensive evolution statistics"""
        
        if not self.evolution_history:
            return {
                'total_generations': 0,
                'final_fitness': 0.0,
                'best_fitness': 0.0,
                'convergence_generation': None,
                'fitness_history': []
            }
        
        fitness_history = [stats['average_fitness'] for stats in self.evolution_history]
        
        return {
            'total_generations': self.generation_count,
            'final_fitness': fitness_history[-1] if fitness_history else 0.0,
            'best_fitness': max(stats['best_fitness'] for stats in self.evolution_history),
            'worst_fitness': min(stats['worst_fitness'] for stats in self.evolution_history),
            'convergence_generation': len(self.evolution_history) if self.converged else None,
            'fitness_history': fitness_history,
            'fitness_improvement': fitness_history[-1] - fitness_history[0] if len(fitness_history) > 1 else 0.0,
            'average_fitness_std': statistics.mean([stats['fitness_std'] for stats in self.evolution_history]),
            'best_individual': self.best_individual.to_dict() if self.best_individual else None,
            'config': {
                'generations': self.config.generations,
                'population_size': self.config.population_size,
                'mutation_rate': self.config.mutation_rate,
                'crossover_rate': self.config.crossover_rate,
                'strategy': self.config.strategy.value,
                'selection_method': self.config.selection_method.value
            }
        }
    
    def export_evolution_data(self) -> Dict[str, Union[Dict, List]]:
        """Export complete evolution data"""
        
        return {
            'statistics': self.get_evolution_statistics(),
            'population': [ind.to_dict() for ind in self.population],
            'evolution_history': self.evolution_history,
            'config': {
                'generations': self.config.generations,
                'population_size': self.config.population_size,
                'mutation_rate': self.config.mutation_rate,
                'crossover_rate': self.config.crossover_rate,
                'elite_size': self.config.elite_size,
                'strategy': self.config.strategy.value,
                'selection_method': self.config.selection_method.value,
                'convergence_threshold': self.config.convergence_threshold,
                'max_stagnant_generations': self.config.max_stagnant_generations
            }
        }
    
    def save_evolution_state(self, file_path: str):
        """Save evolution state to file"""
        
        data = self.export_evolution_data()
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Saved evolution state to {file_path}")
    
    def load_evolution_state(self, file_path: str):
        """Load evolution state from file"""
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Restore configuration
        if 'config' in data:
            config_dict = data['config']
            self.config = EvolutionConfig(
                generations=config_dict.get('generations', EVOLUTION_GENERATIONS),
                population_size=config_dict.get('population_size', EVOLUTION_POPULATION_SIZE),
                mutation_rate=config_dict.get('mutation_rate', 0.1),
                crossover_rate=config_dict.get('crossover_rate', 0.8),
                elite_size=config_dict.get('elite_size', 2),
                strategy=EvolutionStrategy(config_dict.get('strategy', 'genetic_algorithm')),
                selection_method=SelectionMethod(config_dict.get('selection_method', 'tournament')),
                convergence_threshold=config_dict.get('convergence_threshold', 0.001),
                max_stagnant_generations=config_dict.get('max_stagnant_generations', 20)
            )
        
        # Restore population
        if 'population' in data:
            self.population = []
            for ind_dict in data['population']:
                vector_dict = ind_dict['resonance_vector']
                resonance_vector = ResonanceVector(**vector_dict)
                
                individual = Individual(
                    resonance_vector=resonance_vector,
                    fitness=ind_dict['fitness'],
                    generation=ind_dict['generation'],
                    parent_ids=ind_dict['parent_ids'],
                    mutations=ind_dict['mutations']
                )
                self.population.append(individual)
        
        # Restore history
        self.evolution_history = data.get('evolution_history', [])
        self.generation_count = data.get('statistics', {}).get('total_generations', 0)
        
        # Restore best individual
        if data.get('statistics', {}).get('best_individual'):
            best_dict = data['statistics']['best_individual']
            vector_dict = best_dict['resonance_vector']
            resonance_vector = ResonanceVector(**vector_dict)
            
            self.best_individual = Individual(
                resonance_vector=resonance_vector,
                fitness=best_dict['fitness'],
                generation=best_dict['generation'],
                parent_ids=best_dict['parent_ids'],
                mutations=best_dict['mutations']
            )
        
        logger.info(f"Loaded evolution state from {file_path}")


class MultiObjectiveEvolver(ToneEvolver):
    """Multi-objective evolution for optimizing multiple criteria simultaneously"""
    
    def __init__(self, objectives: List[str], **kwargs):
        super().__init__(**kwargs)
        self.objectives = objectives
        self.pareto_front: List[Individual] = []
    
    def _evaluate_population(self, target_topics: List[str]):
        """Evaluate fitness for multiple objectives"""
        
        for individual in self.population:
            if self.fitness_evaluator:
                # External evaluator should return dict of objective scores
                try:
                    scores = self.fitness_evaluator(individual.resonance_vector, target_topics)
                    if isinstance(scores, dict):
                        # Multi-objective evaluation
                        individual.fitness = self._calculate_pareto_fitness(scores)
                        individual.objective_scores = scores
                    else:
                        # Single objective
                        individual.fitness = scores
                except Exception as e:
                    logger.error(f"Multi-objective evaluation failed: {str(e)}")
                    individual.fitness = self._default_fitness_evaluation(individual.resonance_vector)
            else:
                individual.fitness = self._default_fitness_evaluation(individual.resonance_vector)
        
        # Update Pareto front
        self._update_pareto_front()
    
    def _calculate_pareto_fitness(self, scores: Dict[str, float]) -> float:
        """Calculate fitness from multi-objective scores"""
        
        # Simple weighted sum (could be replaced with Pareto ranking)
        return statistics.mean(scores.values())
    
    def _update_pareto_front(self):
        """Update Pareto front of non-dominated solutions"""
        
        if not hasattr(self.population[0], 'objective_scores'):
            return
        
        # Clear current front
        self.pareto_front = []
        
        # Find non-dominated individuals
        for individual in self.population:
            dominated = False
            
            for other in self.population:
                if self._dominates(other, individual):
                    dominated = True
                    break
            
            if not dominated:
                self.pareto_front.append(individual)
        
        # Sort Pareto front by fitness
        self.pareto_front.sort(key=lambda ind: ind.fitness, reverse=True)
    
    def _dominates(self, individual1: Individual, individual2: Individual) -> bool:
        """Check if individual1 dominates individual2"""
        
        scores1 = getattr(individual1, 'objective_scores', {})
        scores2 = getattr(individual2, 'objective_scores', {})
        
        # Individual1 dominates if it's better in all objectives
        for objective in self.objectives:
            if objective in scores1 and objective in scores2:
                if scores1[objective] < scores2[objective]:
                    return False
            elif objective in scores1:
                # Individual2 missing this objective
                return False
        
        return len(scores1) > 0
