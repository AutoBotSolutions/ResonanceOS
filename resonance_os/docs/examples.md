# ResonanceOS Examples

This directory contains practical examples demonstrating ResonanceOS capabilities and usage patterns.

## Quick Start Examples

### 1. Basic Profile Creation

```python
# examples/basic_profile_creation.py
import asyncio
from pathlib import Path
from resonance_os.profiling import CorpusLoader, StyleVectorBuilder, ProfilePersistence
from resonance_os.core.types import StyleProfile

async def create_basic_profile():
    """Create a basic style profile from text files"""
    
    # Load corpus
    loader = CorpusLoader()
    documents = loader.load_corpus("./sample_corpus/")
    
    # Build resonance vector
    vector_builder = StyleVectorBuilder(tier=1)
    resonance_vector = vector_builder.build_vector(documents)
    
    # Create profile
    profile = StyleProfile(
        name="sample_writer",
        description="Sample writing style for demonstration",
        resonance_vector=resonance_vector,
        emotional_curve=[0.5, 0.6, 0.7, 0.6, 0.5],
        cadence_pattern=[0.4, 0.6, 0.8, 0.7],
        abstraction_preference=0.6
    )
    
    # Save profile
    persistence = ProfilePersistence()
    file_path = persistence.save_profile(profile)
    
    print(f"Profile created: {file_path}")
    print(f"Confidence: {resonance_vector.confidence:.3f}")
    print(f"Documents analyzed: {len(documents)}")

if __name__ == "__main__":
    asyncio.run(create_basic_profile())
```

### 2. Text Generation

```python
# examples/text_generation.py
import asyncio
from resonance_os.generation import AdaptiveWriter
from resonance_os.core.types import GenerationConfig
from resonance_os.profiling import ProfilePersistence

async def generate_text_example():
    """Generate text with style alignment"""
    
    # Load profile
    persistence = ProfilePersistence()
    profile = persistence.load_profile_by_name("sample_writer")
    
    if not profile:
        print("Profile not found. Create one first.")
        return
    
    # Configure generation
    config = GenerationConfig(
        topic="The future of artificial intelligence in creative industries",
        target_profile=profile,
        max_tokens=800,
        similarity_threshold=0.92,
        enable_feedback=True,
        enable_drift_detection=True
    )
    
    # Generate text
    writer = AdaptiveWriter()
    
    def progress_callback(progress):
        print(f"Paragraph {progress['paragraph']}: {progress['corrections']} corrections")
    
    result = await writer.generate_article(config, progress_callback)
    
    print(f"\nGenerated Text:")
    print("=" * 50)
    print(result.content)
    print("=" * 50)
    print(f"\nMetrics:")
    print(f"Similarity: {result.metrics.similarity_score:.3f}")
    print(f"Corrections: {result.corrections_made}")
    print(f"Tokens: {result.tokens_generated}")
    print(f"Time: {result.generation_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(generate_text_example())
```

### 3. Profile Comparison

```python
# examples/profile_comparison.py
from resonance_os.similarity import SimilarityCalculator, SimilarityMethod
from resonance_os.profiling import ProfilePersistence

def compare_profiles():
    """Compare similarity between multiple profiles"""
    
    # Load profiles
    persistence = ProfilePersistence()
    profiles = ["sample_writer", "professional", "creative"]
    
    loaded_profiles = {}
    for name in profiles:
        profile = persistence.load_profile_by_name(name)
        if profile:
            loaded_profiles[name] = profile
        else:
            print(f"Profile '{name}' not found")
            return
    
    # Calculate similarities
    calculator = SimilarityCalculator(SimilarityMethod.COSINE)
    
    print("Profile Similarity Matrix:")
    print("-" * 50)
    
    # Header
    header = "         " + "  ".join(f"{name:12}" for name in profiles)
    print(header)
    
    # Matrix
    for i, profile1_name in enumerate(profiles):
        if profile1_name not in loaded_profiles:
            continue
            
        row = [f"{profile1_name:12}"]
        for j, profile2_name in enumerate(profiles):
            if profile2_name not in loaded_profiles:
                continue
                
            if i == j:
                similarity = 1.0
            else:
                similarity = calculator.calculate_similarity(
                    loaded_profiles[profile1_name].resonance_vector,
                    loaded_profiles[profile2_name].resonance_vector
                )
            row.append(f"{similarity:12.3f}")
        
        print("  ".join(row))

if __name__ == "__main__":
    compare_profiles()
```

## Advanced Examples

### 4. Custom Fitness Evaluator for Evolution

```python
# examples/custom_evolution.py
import asyncio
import numpy as np
from resonance_os.evolution import ToneEvolver, EvolutionConfig
from resonance_os.profiling import ProfilePersistence

def custom_fitness_evaluator(resonance_vector, target_topics):
    """Custom fitness function for profile evolution"""
    
    values = np.array(resonance_vector.values)
    
    # Balance score - reward balanced vectors
    balance_score = 1.0 - np.std(values)
    
    # Topic relevance - simulate topic alignment
    topic_score = 0.8  # In real implementation, this would test actual generation
    
    # Complexity score - reward appropriate complexity
    complexity_score = 1.0 - abs(values.mean() - 0.6)  # Target mean around 0.6
    
    # Combine scores with weights
    fitness = (balance_score * 0.4) + (topic_score * 0.4) + (complexity_score * 0.2)
    
    return max(0.0, min(1.0, fitness))

async def evolve_profile_example():
    """Evolve a profile using custom fitness function"""
    
    # Load profile
    persistence = ProfilePersistence()
    profile = persistence.load_profile_by_name("sample_writer")
    
    if not profile:
        print("Profile not found")
        return
    
    # Configure evolution
    config = EvolutionConfig(
        generations=50,
        population_size=20,
        mutation_rate=0.15,
        crossover_rate=0.8
    )
    
    # Setup evolver
    evolver = ToneEvolver(config=config)
    evolver.set_fitness_evaluator(custom_fitness_evaluator)
    
    # Evolution progress
    def progress_callback(progress):
        gen = progress['generation']
        fitness = progress['best_fitness']
        print(f"Generation {gen:3d}: Fitness = {fitness:.3f}")
    
    # Evolve profile
    target_topics = ["artificial intelligence", "creative writing", "technology"]
    evolved_profile = evolver.evolve_profile(profile, target_topics, progress_callback)
    
    # Save evolved profile
    persistence.save_profile(evolved_profile)
    
    # Display results
    stats = evolver.get_evolution_statistics()
    print(f"\nEvolution Complete!")
    print(f"Generations: {stats['total_generations']}")
    print(f"Final fitness: {stats['best_fitness']:.3f}")
    print(f"Improvement: {stats.get('fitness_improvement', 0):.3f}")
    print(f"Evolved profile: {evolved_profile.name}")

if __name__ == "__main__":
    asyncio.run(evolve_profile_example())
```

### 5. Batch Processing

```python
# examples/batch_processing.py
import asyncio
from resonance_os.generation import AdaptiveWriter, BatchGenerator
from resonance_os.core.types import GenerationConfig
from resonance_os.profiling import ProfilePersistence

async def batch_generation_example():
    """Generate multiple articles in batch"""
    
    # Load profiles
    persistence = ProfilePersistence()
    profile = persistence.load_profile_by_name("sample_writer")
    
    if not profile:
        print("Profile not found")
        return
    
    # Create multiple generation configs
    topics = [
        "The impact of AI on education",
        "Machine learning in healthcare",
        "Future of autonomous vehicles",
        "AI ethics and governance",
        "Natural language processing advances"
    ]
    
    configs = []
    for topic in topics:
        config = GenerationConfig(
            topic=topic,
            target_profile=profile,
            max_tokens=600,
            similarity_threshold=0.90,
            enable_feedback=True
        )
        configs.append(config)
    
    # Generate in batch
    writer = AdaptiveWriter()
    batch_generator = BatchGenerator(writer)
    
    def progress_callback(batch_index, progress):
        print(f"Batch {batch_index + 1}: Paragraph {progress['paragraph']}")
    
    results = await batch_generator.generate_batch(
        configs, 
        max_concurrent=3,
        progress_callback=progress_callback
    )
    
    # Display results
    print(f"\nBatch Generation Results:")
    print("=" * 60)
    
    for i, (result, topic) in enumerate(zip(results, topics)):
        print(f"\n{i+1}. {topic}")
        print(f"   Similarity: {result.metrics.similarity_score:.3f}")
        print(f"   Corrections: {result.corrections_made}")
        print(f"   Content: {result.content[:100]}...")
    
    # Batch statistics
    stats = batch_generator.get_batch_statistics()
    print(f"\nBatch Statistics:")
    print(f"Total articles: {stats['total_articles']}")
    print(f"Average similarity: {stats['average_similarity']:.3f}")
    print(f"Average corrections: {stats['average_corrections']:.1f}")
    print(f"Total time: {stats['total_time']:.2f}s")

if __name__ == "__main__":
    asyncio.run(batch_generation_example())
```

### 6. Real-Time Analysis

```python
# examples/realtime_analysis.py
import asyncio
import time
from resonance_os.similarity import DriftDetector
from resonance_os.profiling import StyleVectorBuilder
from resonance_os.core.types import TextDocument

async def realtime_drift_analysis():
    """Demonstrate real-time drift detection"""
    
    # Initialize drift detector
    drift_detector = DriftDetector(window_size=10, drift_threshold=0.05)
    
    # Create sample target profile (simulated)
    from resonance_os.core.constants import RESONANCE_DIMENSIONS
    import numpy as np
    
    target_values = np.random.rand(len(RESONANCE_DIMENSIONS)) * 0.3 + 0.6  # Values around 0.6-0.9
    target_vector = StyleVectorBuilder(tier=1).build_vector([])
    target_vector.values = target_values.tolist()
    
    print("Real-Time Drift Analysis")
    print("=" * 40)
    print("Simulating content generation with drift...")
    
    # Simulate generation with gradual drift
    for i in range(15):
        # Create current vector with some drift
        drift_amount = i * 0.02  # Gradually increase drift
        noise = np.random.normal(0, drift_amount, len(target_values))
        current_values = target_values + noise
        current_values = np.clip(current_values, 0, 1)  # Keep in [0,1] range
        
        current_vector = StyleVectorBuilder(tier=1).build_vector([])
        current_vector.values = current_values.tolist()
        
        # Analyze drift
        drift_analysis = drift_detector.add_measurement(current_vector, target_vector)
        
        print(f"Step {i+1:2d}: Similarity={drift_analysis.current_similarity:.3f}, "
              f"Drift={drift_analysis.drift_rate:.3f}, "
              f"Severity={drift_analysis.severity}")
        
        if drift_analysis.severity == "high":
            print(f"  ⚠️  High drift detected! Recommendation: {drift_analysis.recommendation}")
        
        await asyncio.sleep(0.1)  # Simulate time between generations
    
    # Display drift statistics
    stats = drift_detector.get_drift_statistics()
    print(f"\nDrift Statistics:")
    print(f"Total measurements: {stats['total_measurements']}")
    print(f"Average drift rate: {stats['average_drift_rate']:.3f}")
    print(f"Drift episodes: {stats['drift_episodes']}")
    print(f"Drift frequency: {stats['drift_frequency']:.3f}")

if __name__ == "__main__":
    asyncio.run(realtime_drift_analysis())
```

## Integration Examples

### 7. Web Application Integration

```python
# examples/web_integration.py
from flask import Flask, request, jsonify
import asyncio
from resonance_os import ResonanceOS

app = Flask(__name__)
ros = ResonanceOS()

@app.route('/api/generate', methods=['POST'])
def generate_text():
    """Web API endpoint for text generation"""
    
    data = request.json
    topic = data.get('topic')
    profile_name = data.get('profile_name')
    
    if not topic or not profile_name:
        return jsonify({'error': 'topic and profile_name required'}), 400
    
    try:
        # Run async generation in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            ros.generate_text(topic, profile_name)
        )
        
        return jsonify({
            'content': result.content,
            'similarity_score': result.metrics.similarity_score,
            'corrections_made': result.corrections_made
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    """Web API endpoint for profile creation"""
    
    data = request.json
    name = data.get('name')
    text_content = data.get('text_content')
    
    if not name or not text_content:
        return jsonify({'error': 'name and text_content required'}), 400
    
    try:
        profile = ros.create_profile_from_text(name, text_content)
        return jsonify({
            'profile_name': profile.name,
            'confidence': profile.resonance_vector.confidence
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 8. Database Integration

```python
# examples/database_integration.py
import sqlite3
from contextlib import contextmanager
from resonance_os.profiling import ProfilePersistence
from resonance_os.generation import AdaptiveWriter
from resonance_os.core.types import GenerationConfig

class DatabaseManager:
    """Database integration for ResonanceOS"""
    
    def __init__(self, db_path="resonance_os.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS generations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    profile_name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    similarity_score REAL,
                    corrections_made INTEGER,
                    generation_time REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def save_generation(self, result):
        """Save generation result to database"""
        with self.get_connection() as conn:
            conn.execute('''
                INSERT INTO generations 
                (topic, profile_name, content, similarity_score, corrections_made, generation_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                result.config.topic,
                result.profile_used.name,
                result.content,
                result.metrics.similarity_score,
                result.corrections_made,
                result.generation_time
            ))
    
    def get_generation_history(self, limit=100):
        """Get generation history"""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM generations 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_profile_stats(self):
        """Get profile usage statistics"""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT 
                    profile_name,
                    COUNT(*) as generation_count,
                    AVG(similarity_score) as avg_similarity,
                    AVG(corrections_made) as avg_corrections
                FROM generations
                GROUP BY profile_name
            ''')
            return [dict(row) for row in cursor.fetchall()]

# Example usage
def database_integration_example():
    """Example of database integration"""
    
    # Initialize database manager
    db = DatabaseManager()
    
    # Load profile and generate text
    persistence = ProfilePersistence()
    profile = persistence.load_profile_by_name("sample_writer")
    
    if profile:
        config = GenerationConfig(
            topic="Database integration with AI",
            target_profile=profile,
            max_tokens=400
        )
        
        writer = AdaptiveWriter()
        result = asyncio.run(writer.generate_article(config))
        
        # Save to database
        db.save_generation(result)
        print(f"Generation saved to database")
        
        # Get history
        history = db.get_generation_history(limit=5)
        print(f"\nRecent generations:")
        for gen in history:
            print(f"- {gen['topic']} ({gen['similarity_score']:.3f})")
        
        # Get profile stats
        stats = db.get_profile_stats()
        print(f"\nProfile statistics:")
        for stat in stats:
            print(f"- {stat['profile_name']}: {stat['generation_count']} generations, "
                  f"avg similarity {stat['avg_similarity']:.3f}")

if __name__ == "__main__":
    database_integration_example()
```

## Performance Examples

### 9. Performance Benchmarking

```python
# examples/performance_benchmark.py
import time
import asyncio
import statistics
from resonance_os.generation import AdaptiveWriter
from resonance_os.core.types import GenerationConfig
from resonance_os.profiling import ProfilePersistence

async def benchmark_generation():
    """Benchmark text generation performance"""
    
    # Load profile
    persistence = ProfilePersistence()
    profile = persistence.load_profile_by_name("sample_writer")
    
    if not profile:
        print("Profile not found")
        return
    
    # Benchmark parameters
    num_runs = 10
    topics = [
        f"Benchmark topic {i+1}: AI and machine learning applications"
        for i in range(num_runs)
    ]
    
    # Run benchmark
    writer = AdaptiveWriter()
    times = []
    similarities = []
    corrections = []
    
    print("Running performance benchmark...")
    print(f"Generating {num_runs} articles...")
    
    for i, topic in enumerate(topics):
        start_time = time.time()
        
        config = GenerationConfig(
            topic=topic,
            target_profile=profile,
            max_tokens=500,
            similarity_threshold=0.90
        )
        
        result = await writer.generate_article(config)
        
        end_time = time.time()
        generation_time = end_time - start_time
        
        times.append(generation_time)
        similarities.append(result.metrics.similarity_score)
        corrections.append(result.corrections_made)
        
        print(f"Run {i+1:2d}: {generation_time:.2f}s, "
              f"similarity {result.metrics.similarity_score:.3f}, "
              f"corrections {result.corrections_made}")
    
    # Calculate statistics
    print(f"\nBenchmark Results:")
    print("=" * 50)
    print(f"Average time: {statistics.mean(times):.2f}s")
    print(f"Time std dev: {statistics.stdev(times):.2f}s")
    print(f"Min time: {min(times):.2f}s")
    print(f"Max time: {max(times):.2f}s")
    print(f"Average similarity: {statistics.mean(similarities):.3f}")
    print(f"Average corrections: {statistics.mean(corrections):.1f}")
    print(f"Total time: {sum(times):.2f}s")
    print(f"Throughput: {num_runs/sum(times):.2f} generations/second")

if __name__ == "__main__":
    asyncio.run(benchmark_generation())
```

### 10. Memory Usage Monitoring

```python
# examples/memory_monitoring.py
import psutil
import os
import gc
from resonance_os.profiling import StyleVectorBuilder
from resonance_os.generation import AdaptiveWriter

def monitor_memory_usage():
    """Monitor memory usage during ResonanceOS operations"""
    
    process = psutil.Process(os.getpid())
    
    def get_memory_info():
        """Get current memory usage"""
        memory_info = process.memory_info()
        return {
            'rss': memory_info.rss / 1024 / 1024,  # MB
            'vms': memory_info.vms / 1024 / 1024,  # MB
            'percent': process.memory_percent()
        }
    
    print("Memory Usage Monitoring")
    print("=" * 40)
    
    # Baseline memory
    baseline = get_memory_info()
    print(f"Baseline: {baseline['rss']:.1f} MB RSS, {baseline['percent']:.1f}%")
    
    # Profile creation memory
    print("\nCreating profile...")
    vector_builder = StyleVectorBuilder(tier=2)
    
    # Simulate profile creation with large corpus
    from resonance_os.core.types import TextDocument
    documents = [TextDocument(content="Sample text " * 1000, source="test")]
    
    before_profile = get_memory_info()
    resonance_vector = vector_builder.build_vector(documents)
    after_profile = get_memory_info()
    
    print(f"Profile creation: {after_profile['rss'] - before_profile['rss']:.1f} MB increase")
    
    # Generation memory
    print("\nText generation...")
    writer = AdaptiveWriter()
    
    # Simulate multiple generations
    for i in range(5):
        before_gen = get_memory_info()
        
        # Simulate generation (without actual LLM call)
        writer.current_profile = None  # Reset state
        gc.collect()  # Force garbage collection
        
        after_gen = get_memory_info()
        print(f"Generation {i+1}: {after_gen['rss']:.1f} MB RSS")
    
    # Cleanup
    print("\nCleanup...")
    del vector_builder
    del writer
    del resonance_vector
    gc.collect()
    
    final = get_memory_info()
    print(f"Final: {final['rss']:.1f} MB RSS, {final['percent']:.1f}%")
    print(f"Memory increase: {final['rss'] - baseline['rss']:.1f} MB")

if __name__ == "__main__":
    monitor_memory_usage()
```

## Running Examples

Each example can be run independently:

```bash
# Basic examples
python examples/basic_profile_creation.py
python examples/text_generation.py
python examples/profile_comparison.py

# Advanced examples
python examples/custom_evolution.py
python examples/batch_processing.py
python examples/realtime_analysis.py

# Integration examples
python examples/web_integration.py
python examples/database_integration.py

# Performance examples
python examples/performance_benchmark.py
python examples/memory_monitoring.py
```

## Sample Data

The `sample_corpus/` directory contains example text files for testing:

```
sample_corpus/
├── technical_writing.txt
├── creative_writing.txt
├── business_communication.txt
└── academic_papers.txt
```

These examples demonstrate various aspects of ResonanceOS functionality and can serve as starting points for your own implementations.
