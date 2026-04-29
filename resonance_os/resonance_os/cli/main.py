"""
Main CLI interface for ResonanceOS
"""

import click
import asyncio
import json
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

from ..core.config import get_config
from ..core.logging import get_logger, setup_logging
from ..profiling.corpus_loader import CorpusLoader
from ..profiling.style_vector_builder import StyleVectorBuilder
from ..profiling.profile_persistence import ProfilePersistence
from ..generation.adaptive_writer import AdaptiveWriter
from ..evolution.tone_evolver import ToneEvolver

logger = get_logger(__name__)
console = Console()


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.pass_context
def cli(ctx, verbose, config):
    """ResonanceOS - Adaptive Stylistic Alignment Engine"""
    
    # Setup logging
    log_level = 'DEBUG' if verbose else 'INFO'
    setup_logging(level=log_level)
    
    # Load configuration
    if config:
        # TODO: Load custom config
        pass
    
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
    console.print(Panel(
        Text("ResonanceOS - Adaptive Stylistic Alignment Engine", style="bold blue"),
        subtitle="Advanced AI writing with real-time tonal alignment"
    ))


@cli.command()
@click.option('--name', '-n', required=True, help='Profile name')
@click.option('--corpus', '-c', required=True, type=click.Path(exists=True), help='Corpus directory path')
@click.option('--description', '-d', help='Profile description')
@click.option('--tier', '-t', type=click.IntRange(1, 3), default=1, help='Analysis tier (1-3)')
@click.option('--output', '-o', type=click.Path(), help='Output file for profile data')
@click.pass_context
def profile(ctx, name, corpus, description, tier, output):
    """Create a style profile from corpus"""
    
    console.print(f"[bold green]Creating profile '{name}' from corpus: {corpus}[/bold green]")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Load corpus
            task = progress.add_task("Loading corpus...", total=None)
            loader = CorpusLoader()
            documents = loader.load_corpus(corpus)
            progress.update(task, description=f"Loaded {len(documents)} documents")
            
            if not documents:
                console.print("[bold red]No documents found in corpus[/bold red]")
                return
            
            # Build resonance vector
            task = progress.add_task("Analyzing style...", total=None)
            vector_builder = StyleVectorBuilder(tier)
            resonance_vector = vector_builder.build_vector(documents)
            progress.update(task, description="Style analysis complete")
            
            # Create profile
            from ..core.types import StyleProfile
            profile = StyleProfile(
                name=name,
                description=description,
                resonance_vector=resonance_vector,
                emotional_curve=[0.5] * 5,
                cadence_pattern=[0.5] * 4,
                abstraction_preference=0.5,
                metadata={"corpus_path": str(corpus), "tier": tier}
            )
            
            # Save profile
            task = progress.add_task("Saving profile...", total=None)
            persistence = ProfilePersistence()
            file_path = persistence.save_profile(profile)
            progress.update(task, description=f"Profile saved to {file_path}")
        
        # Display results
        console.print(Panel(
            f"[bold green]Profile '{name}' created successfully![/bold green]\n\n"
            f"Confidence: {resonance_vector.confidence:.3f}\n"
            f"Documents analyzed: {len(documents)}\n"
            f"Analysis tier: {tier}\n"
            f"Saved to: {file_path}",
            title="Profile Creation Complete"
        ))
        
        # Save to output file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(profile.dict(), f, indent=2, default=str)
            console.print(f"[green]Profile data saved to: {output}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]Error creating profile: {str(e)}[/bold red]")
        if ctx.obj['verbose']:
            raise


@cli.command()
@click.option('--topic', '-t', required=True, help='Topic or prompt for generation')
@click.option('--profile', '-p', required=True, help='Profile name to use')
@click.option('--output', '-o', type=click.Path(), help='Output file for generated text')
@click.option('--tokens', type=int, default=2048, help='Maximum tokens to generate')
@click.option('--similarity', type=float, default=0.92, help='Target similarity threshold')
@click.option('--temperature', type=float, default=0.7, help='Generation temperature')
@click.option('--corrections', type=int, default=3, help='Maximum correction attempts')
@click.pass_context
def generate(ctx, topic, profile, output, tokens, similarity, temperature, corrections):
    """Generate text with style alignment"""
    
    console.print(f"[bold green]Generating text about '{topic}' using profile '{profile}'[/bold green]")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Load profile
            task = progress.add_task("Loading profile...", total=None)
            persistence = ProfilePersistence()
            style_profile = persistence.load_profile_by_name(profile)
            
            if not style_profile:
                console.print(f"[bold red]Profile '{profile}' not found[/bold red]")
                return
            
            progress.update(task, description=f"Profile '{profile}' loaded")
            
            # Setup generation
            from ..core.types import GenerationConfig
            config = GenerationConfig(
                topic=topic,
                target_profile=style_profile,
                max_tokens=tokens,
                similarity_threshold=similarity,
                temperature=temperature,
                max_corrections=corrections,
                enable_feedback=True,
                enable_drift_detection=True
            )
            
            # Generate text
            task = progress.add_task("Generating text...", total=None)
            writer = AdaptiveWriter()
            
            def progress_callback(progress_data):
                progress.update(task, description=f"Paragraph {progress_data['paragraph']} - {progress_data['corrections']} corrections")
            
            result = asyncio.run(writer.generate_article(config, progress_callback))
            progress.update(task, description="Generation complete")
        
        # Display results
        console.print(Panel(
            result.content[:500] + "..." if len(result.content) > 500 else result.content,
            title=f"Generated Text (Similarity: {result.metrics.similarity_score:.3f})"
        ))
        
        console.print(f"[green]Generation completed:[/green]")
        console.print(f"  Similarity score: {result.metrics.similarity_score:.3f}")
        console.print(f"  Corrections made: {result.corrections_made}")
        console.print(f"  Tokens generated: {result.tokens_generated}")
        console.print(f"  Generation time: {result.generation_time:.2f}s")
        
        # Save to output file if requested
        if output:
            with open(output, 'w') as f:
                f.write(result.content)
            console.print(f"[green]Generated text saved to: {output}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]Error generating text: {str(e)}[/bold red]")
        if ctx.obj['verbose']:
            raise


@cli.command()
@click.option('--profiles', '-p', multiple=True, help='Profile names to compare')
@click.option('--method', type=click.Choice(['cosine', 'euclidean', 'manhattan', 'pearson', 'spearman']), default='cosine', help='Similarity method')
@click.pass_context
def compare(ctx, profiles, method):
    """Compare similarity between profiles"""
    
    if len(profiles) < 2:
        console.print("[bold red]At least 2 profiles required for comparison[/bold red]")
        return
    
    console.print(f"[bold green]Comparing {len(profiles)} profiles using {method} similarity[/bold green]")
    
    try:
        from ..similarity.metrics import SimilarityCalculator, SimilarityMethod
        
        # Load profiles
        persistence = ProfilePersistence()
        loaded_profiles = []
        
        for profile_name in profiles:
            profile = persistence.load_profile_by_name(profile_name)
            if not profile:
                console.print(f"[bold red]Profile '{profile_name}' not found[/bold red]")
                return
            loaded_profiles.append(profile)
        
        # Calculate similarities
        calculator = SimilarityCalculator(SimilarityMethod(method))
        
        # Create similarity table
        table = Table(title=f"Profile Similarity Matrix ({method})")
        table.add_column("", style="bold")
        
        for profile_name in profiles:
            table.add_column(profile_name, justify="center")
        
        for i, profile1_name in enumerate(profiles):
            row = [profile1_name]
            for j, profile2_name in enumerate(profiles):
                if i == j:
                    similarity = 1.0
                else:
                    similarity = calculator.calculate_similarity(
                        loaded_profiles[i].resonance_vector,
                        loaded_profiles[j].resonance_vector
                    )
                row.append(f"{similarity:.3f}")
            table.add_row(*row)
        
        console.print(table)
        
        # Find most/least similar pairs
        max_similarity = 0.0
        min_similarity = 1.0
        most_similar = None
        least_similar = None
        
        for i in range(len(loaded_profiles)):
            for j in range(i + 1, len(loaded_profiles)):
                similarity = calculator.calculate_similarity(
                    loaded_profiles[i].resonance_vector,
                    loaded_profiles[j].resonance_vector
                )
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar = (profiles[i], profiles[j])
                
                if similarity < min_similarity:
                    min_similarity = similarity
                    least_similar = (profiles[i], profiles[j])
        
        console.print(f"\n[bold]Most similar pair:[/bold] {most_similar[0]} & {most_similar[1]} ({max_similarity:.3f})")
        console.print(f"[bold]Least similar pair:[/bold] {least_similar[0]} & {least_similar[1]} ({min_similarity:.3f})")
        
    except Exception as e:
        console.print(f"[bold red]Error comparing profiles: {str(e)}[/bold red]")
        if ctx.obj['verbose']:
            raise


@cli.command()
@click.option('--profile', '-p', required=True, help='Profile name to evolve')
@click.option('--topics', '-t', multiple=True, required=True, help='Target topics for optimization')
@click.option('--generations', '-g', type=int, default=100, help='Number of evolution generations')
@click.option('--population', type=int, default=50, help='Population size')
@click.option('--output', '-o', type=click.Path(), help='Output file for evolved profile')
@click.pass_context
def evolve(ctx, profile, topics, generations, population, output):
    """Evolve a profile to improve performance"""
    
    topics_list = list(topics)
    console.print(f"[bold green]Evolving profile '{profile}' for topics: {', '.join(topics_list)}[/bold green]")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Load profile
            task = progress.add_task("Loading profile...", total=None)
            persistence = ProfilePersistence()
            initial_profile = persistence.load_profile_by_name(profile)
            
            if not initial_profile:
                console.print(f"[bold red]Profile '{profile}' not found[/bold red]")
                return
            
            progress.update(task, description=f"Profile '{profile}' loaded")
            
            # Setup evolution
            from ..evolution.tone_evolver import EvolutionConfig
            config = EvolutionConfig(
                generations=generations,
                population_size=population
            )
            
            evolver = ToneEvolver(config=config)
            
            def fitness_evaluator(resonance_vector, target_topics):
                # Simple fitness evaluation
                values = resonance_vector.values
                balance_score = 1.0 - (max(values) - min(values))
                topic_score = 0.8  # Placeholder
                return (balance_score + topic_score) / 2
            
            evolver.set_fitness_evaluator(fitness_evaluator)
            
            # Evolution progress
            def progress_callback(progress_data):
                gen = progress_data['generation']
                fitness = progress_data['best_fitness']
                progress.update(task, description=f"Generation {gen} - Fitness: {fitness:.3f}")
            
            # Evolve profile
            evolved_profile = evolver.evolve_profile(initial_profile, topics_list, progress_callback)
            progress.update(task, description="Evolution complete")
        
        # Display results
        stats = evolver.get_evolution_statistics()
        
        console.print(Panel(
            f"[bold green]Profile evolution completed![/bold green]\n\n"
            f"Original profile: {profile}\n"
            f"Evolved profile: {evolved_profile.name}\n"
            f"Generations: {stats['total_generations']}\n"
            f"Final fitness: {stats['best_fitness']:.3f}\n"
            f"Fitness improvement: {stats.get('fitness_improvement', 0):.3f}",
            title="Evolution Results"
        ))
        
        # Save evolved profile
        persistence.save_profile(evolved_profile)
        console.print(f"[green]Evolved profile saved as '{evolved_profile.name}'[/green]")
        
        # Save to output file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(evolved_profile.dict(), f, indent=2, default=str)
            console.print(f"[green]Evolution data saved to: {output}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]Error evolving profile: {str(e)}[/bold red]")
        if ctx.obj['verbose']:
            raise


@cli.command()
@click.option('--format', type=click.Choice(['table', 'json']), default='table', help='Output format')
def list(format):
    """List all available profiles"""
    
    try:
        persistence = ProfilePersistence()
        profiles = persistence.list_profiles()
        
        if not profiles:
            console.print("[yellow]No profiles found[/yellow]")
            return
        
        if format == 'table':
            table = Table(title="Available Profiles")
            table.add_column("Name", style="bold")
            table.add_column("Description")
            table.add_column("Confidence", justify="center")
            table.add_column("Created", justify="center")
            table.add_column("Format", justify="center")
            
            for profile_info in profiles:
                created = profile_info.get('created_at', 'Unknown')[:10] if profile_info.get('created_at') else 'Unknown'
                table.add_row(
                    profile_info['name'],
                    profile_info.get('description', 'No description')[:30] + '...' if len(profile_info.get('description', '')) > 30 else profile_info.get('description', 'No description'),
                    f"{profile_info.get('confidence', 0):.3f}",
                    created,
                    profile_info.get('format', 'json')
                )
            
            console.print(table)
        
        elif format == 'json':
            console.print(json.dumps(profiles, indent=2, default=str))
        
    except Exception as e:
        console.print(f"[bold red]Error listing profiles: {str(e)}[/bold red]")


@cli.command()
@click.argument('profile_name')
def delete(profile_name):
    """Delete a profile"""
    
    try:
        persistence = ProfilePersistence()
        success = persistence.delete_profile(profile_name)
        
        if success:
            console.print(f"[green]Profile '{profile_name}' deleted successfully[/green]")
        else:
            console.print(f"[bold red]Profile '{profile_name}' not found[/bold red]")
        
    except Exception as e:
        console.print(f"[bold red]Error deleting profile: {str(e)}[/bold red]")


@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
@click.option('--workers', default=1, help='Number of worker processes')
@click.option('--reload', is_flag=True, help='Enable auto-reload for development')
def serve(host, port, workers, reload):
    """Start the ResonanceOS API server"""
    
    console.print(f"[bold green]Starting ResonanceOS API server[/bold green]")
    console.print(f"Host: {host}")
    console.print(f"Port: {port}")
    console.print(f"Workers: {workers}")
    console.print(f"Reload: {reload}")
    
    try:
        from ..api.fastapi_server import run_server
        run_server(host=host, port=port, workers=workers, reload=reload)
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Error starting server: {str(e)}[/bold red]")


@cli.command()
def stats():
    """Show system statistics"""
    
    try:
        console.print("[bold green]ResonanceOS System Statistics[/bold green]")
        
        # Profile statistics
        persistence = ProfilePersistence()
        profile_stats = persistence.get_profile_statistics()
        
        console.print(f"\n[bold]Profiles:[/bold]")
        console.print(f"  Total: {profile_stats['total_profiles']}")
        console.print(f"  Average confidence: {profile_stats['average_confidence']:.3f}")
        console.print(f"  Newest: {profile_stats['newest_profile']}")
        console.print(f"  Oldest: {profile_stats['oldest_profile']}")
        
        # Generation statistics
        writer = AdaptiveWriter()
        gen_stats = writer.get_generation_statistics()
        
        console.print(f"\n[bold]Generation:[/bold]")
        console.print(f"  Total generations: {gen_stats['total_generations']}")
        console.print(f"  Success rate: {gen_stats['success_rate']:.3f}")
        console.print(f"  Average similarity: {gen_stats['average_similarity']:.3f}")
        console.print(f"  Average corrections: {gen_stats['average_corrections']:.3f}")
        
        # Drift statistics
        drift_stats = writer.drift_detector.get_drift_statistics()
        
        console.print(f"\n[bold]Drift Detection:[/bold]")
        console.print(f"  Total measurements: {drift_stats['total_measurements']}")
        console.print(f"  Current similarity: {drift_stats['current_similarity']:.3f}")
        console.print(f"  Average drift rate: {drift_stats['average_drift_rate']:.3f}")
        console.print(f"  Drift episodes: {drift_stats['drift_episodes']}")
        
    except Exception as e:
        console.print(f"[bold red]Error getting statistics: {str(e)}[/bold red]")


@cli.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for backup')
def backup(output):
    """Create a backup of all profiles"""
    
    try:
        persistence = ProfilePersistence()
        
        if output:
            # Backup to specific file
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = Path(output)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            profiles = persistence.list_profiles()
            backup_data = {
                'backup_timestamp': timestamp,
                'total_profiles': len(profiles),
                'profiles': profiles
            }
            
            with open(backup_path, 'w') as f:
                json.dump(backup_data, f, indent=2, default=str)
            
            console.print(f"[green]Backup created: {backup_path}[/green]")
        else:
            # Create automatic backup
            backup_path = persistence.create_profile_backup()
            console.print(f"[green]Backup created: {backup_path}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]Error creating backup: {str(e)}[/bold red]")


@cli.command()
@click.argument('backup_file', type=click.Path(exists=True))
def restore(backup_file):
    """Restore profiles from backup"""
    
    try:
        persistence = ProfilePersistence()
        imported_count = persistence.import_profiles(Path(backup_file))
        
        console.print(f"[green]Restored {imported_count} profiles from {backup_file}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]Error restoring backup: {str(e)}[/bold red]")


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()
