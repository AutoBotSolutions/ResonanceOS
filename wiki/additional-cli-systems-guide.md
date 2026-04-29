# Additional CLI Systems Guide - ResonanceOS v6

## Overview

The Additional CLI Systems module provides a modern, feature-rich command-line interface built with Click and Rich for enhanced user experience. This module extends the base CLI systems with advanced profile management, generation capabilities, evolution tools, and system administration features.

## System Architecture

```
Additional CLI Systems
└── main.py (Main CLI Interface)
```

## System Components

### 1. Main CLI Interface (`main.py`)

A comprehensive CLI interface built with Click and Rich for profile creation, text generation, profile comparison, evolution, and system administration.

#### Architecture

```python
@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
def cli(ctx, verbose, config):
    """ResonanceOS - Adaptive Stylistic Alignment Engine"""
```

#### Key Features

- **Rich Terminal UI**: Beautiful tables, panels, and progress indicators
- **Progress Tracking**: Real-time progress for long-running operations
- **Profile Management**: Create, list, delete, and backup profiles
- **Text Generation**: Generate text with style alignment
- **Profile Comparison**: Compare profiles using multiple similarity methods
- **Profile Evolution**: Evolve profiles using genetic algorithms
- **System Administration**: Server management, statistics, backup/restore

#### Usage Examples

**Profile Creation**
```bash
# Create a profile from corpus
resonance profile \
    --name professional \
    --corpus /path/to/corpus \
    --description "Professional business writing" \
    --tier 2 \
    --output profile.json
```

**Text Generation**
```bash
# Generate text with style alignment
resonance generate \
    --topic "AI technology in healthcare" \
    --profile professional \
    --tokens 2048 \
    --similarity 0.92 \
    --temperature 0.7 \
    --corrections 3 \
    --output generated.txt
```

**Profile Comparison**
```bash
# Compare multiple profiles
resonance compare \
    --profiles professional creative technical \
    --method cosine
```

**Profile Evolution**
```bash
# Evolve a profile for specific topics
resonance evolve \
    --profile professional \
    --topics AI technology innovation \
    --generations 100 \
    --population 50 \
    --output evolved_profile.json
```

**List Profiles**
```bash
# List all profiles (table format)
resonance list --format table

# List all profiles (JSON format)
resonance list --format json
```

**Delete Profile**
```bash
# Delete a profile
resonance delete professional
```

**Start API Server**
```bash
# Start the API server
resonance serve \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --reload
```

**System Statistics**
```bash
# Show system statistics
resonance stats
```

**Backup Profiles**
```bash
# Create automatic backup
resonance backup

# Backup to specific file
resonance backup --output /path/to/backup.json
```

**Restore Profiles**
```bash
# Restore from backup
resonance restore /path/to/backup.json
```

#### Command Details

**profile** - Create Style Profile
- `--name, -n`: Profile name (required)
- `--corpus, -c`: Corpus directory path (required)
- `--description, -d`: Profile description
- `--tier, -t`: Analysis tier (1-3, default: 1)
- `--output, -o`: Output file for profile data

**generate** - Generate Text with Style Alignment
- `--topic, -t`: Topic or prompt (required)
- `--profile, -p`: Profile name to use (required)
- `--output, -o`: Output file for generated text
- `--tokens`: Maximum tokens (default: 2048)
- `--similarity`: Target similarity threshold (default: 0.92)
- `--temperature`: Generation temperature (default: 0.7)
- `--corrections`: Maximum correction attempts (default: 3)

**compare** - Compare Profile Similarity
- `--profiles, -p`: Profile names to compare (multiple, min 2 required)
- `--method`: Similarity method (cosine, euclidean, manhattan, pearson, spearman, default: cosine)

**evolve** - Evolve Profile
- `--profile, -p`: Profile name to evolve (required)
- `--topics, -t`: Target topics for optimization (multiple, required)
- `--generations, -g`: Number of generations (default: 100)
- `--population`: Population size (default: 50)
- `--output, -o`: Output file for evolved profile

**list** - List Profiles
- `--format`: Output format (table, json, default: table)

**delete** - Delete Profile
- `profile_name`: Profile name to delete (required argument)

**serve** - Start API Server
- `--host`: Host to bind to (default: 0.0.0.0)
- `--port`: Port to bind to (default: 8000)
- `--workers`: Number of worker processes (default: 1)
- `--reload`: Enable auto-reload for development

**stats** - Show System Statistics
- No arguments required

**backup** - Create Backup
- `--output, -o`: Output file for backup

**restore** - Restore from Backup
- `backup_file`: Backup file path (required argument)

#### Programmatic Usage

```python
from resonance_os.resonance_os.cli.main import cli
from click.testing import CliRunner

runner = CliRunner()

# Create profile
result = runner.invoke(cli, [
    'profile',
    '--name', 'professional',
    '--corpus', '/path/to/corpus',
    '--description', 'Professional writing',
    '--tier', '2'
])
print(result.output)

# Generate text
result = runner.invoke(cli, [
    'generate',
    '--topic', 'AI technology',
    '--profile', 'professional',
    '--tokens', 1024
])
print(result.output)

# Compare profiles
result = runner.invoke(cli, [
    'compare',
    '--profiles', 'professional', 'creative',
    '--method', 'cosine'
])
print(result.output)
```

#### Rich UI Components

**Progress Indicators**
```python
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    console=console
) as progress:
    task = progress.add_task("Loading corpus...", total=None)
    # ... processing ...
    progress.update(task, description="Corpus loaded")
```

**Tables**
```python
table = Table(title="Available Profiles")
table.add_column("Name", style="bold")
table.add_column("Description")
table.add_column("Confidence", justify="center")

for profile_info in profiles:
    table.add_row(
        profile_info['name'],
        profile_info['description'],
        f"{profile_info['confidence']:.3f}"
    )

console.print(table)
```

**Panels**
```python
console.print(Panel(
    f"[bold green]Profile '{name}' created successfully![/bold green]\n\n"
    f"Confidence: {confidence:.3f}\n"
    f"Documents: {count}",
    title="Profile Creation Complete"
))
```

#### Output Formats

**Table Format**
```
Available Profiles
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Name          ┃ Description              ┃ Confidence ┃ Created   ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ professional  │ Professional writing    │     0.850  │ 2026-03-09│
│ creative      │ Creative writing style  │     0.720  │ 2026-03-09│
└───────────────┴──────────────────────────┴────────────┴───────────┘
```

**JSON Format**
```json
[
  {
    "name": "professional",
    "description": "Professional writing",
    "confidence": 0.85,
    "created_at": "2026-03-09T00:00:00Z",
    "format": "json"
  }
]
```

## Integration Points

The Additional CLI Systems module integrates with:

- **Core Systems**: Uses config, logging, and types
- **Profiling Systems**: Uses corpus loader, style vector builder, profile persistence
- **Generation Systems**: Uses adaptive writer for text generation
- **Evolution Systems**: Uses tone evolver for profile optimization
- **Similarity Systems**: Uses similarity calculator for profile comparison
- **API Systems**: Uses FastAPI server for serve command

## Usage Patterns

### Complete Profile Workflow

```bash
# 1. Create profile from corpus
resonance profile \
    --name professional \
    --corpus /path/to/professional_writing \
    --description "Professional business style" \
    --tier 2

# 2. Test generation
resonance generate \
    --topic "Business strategy" \
    --profile professional \
    --output test.txt

# 3. Compare with other profiles
resonance compare \
    --profiles professional creative \
    --method cosine

# 4. Evolve for specific topics
resonance evolve \
    --profile professional \
    --topics business finance strategy \
    --generations 50

# 5. Backup
resonance backup --output professional_backup.json
```

### Batch Processing

```bash
# Create multiple profiles
for style in professional creative technical; do
    resonance profile \
        --name $style \
        --corpus /path/to/${style}_corpus \
        --description "${style} writing style"
done

# Generate content for each profile
for style in professional creative technical; do
    resonance generate \
        --topic "AI technology" \
        --profile $style \
        --output ${style}_output.txt
done
```

### Development Workflow

```bash
# Start server with auto-reload
resonance serve --host 0.0.0.0 --port 8000 --reload

# In another terminal, monitor statistics
resonance stats

# Create test profile
resonance profile --name test --corpus ./test_corpus --tier 1

# Generate test content
resonance generate --topic test --profile test --output test.txt
```

## Best Practices

1. **Use appropriate tiers**: Higher tiers provide better analysis but are slower
2. **Monitor progress**: Watch progress indicators for long operations
3. **Backup regularly**: Use backup command before major changes
4. **Compare profiles**: Use compare command to understand profile differences
5. **Evolve strategically**: Use evolution for specific topic optimization
6. **Check statistics**: Use stats command to monitor system health
7. **Use verbose mode**: Enable -v flag for debugging
8. **Save outputs**: Use output flags to save results for later analysis

## Common Issues

**Issue**: Profile creation fails
**Solution**: Verify corpus directory exists and contains valid text files

**Issue**: Generation too slow
**Solution**: Reduce tokens or similarity threshold, or use lower tier profile

**Issue**: Profile not found
**Solution**: Use list command to verify profile name, check case sensitivity

**Issue**: Evolution doesn't converge
**Solution**: Increase generations or population size, check fitness evaluator

**Issue**: Server won't start
**Solution**: Check if port is in use, verify dependencies are installed

## Performance Considerations

- **Tier 1**: Fast, basic analysis (good for quick testing)
- **Tier 2**: Moderate, advanced analysis (recommended for production)
- **Tier 3**: Slow, transformer-based (future, best quality)
- **Progress tracking**: Minimal overhead for UI updates
- **Server workers**: Increase workers for higher throughput
- **Memory usage**: Monitor for large corpora and generations

## Future Enhancements

- **Interactive mode**: Interactive profile creation and editing
- **Shell completion**: Tab completion for commands and profiles
- **Configuration files**: YAML/JSON configuration support
- **Plugin system**: Custom commands and extensions
- **Batch commands**: Native batch processing commands
- **Web UI**: Web-based interface alternative
- **Export formats**: More export format options (CSV, Excel)

## Dependencies

```bash
# Core dependencies
pip install click
pip install rich
pip install asyncio
```

## References

- [CLI Systems Guide](./cli-systems-guide.md)
- [Profiling Systems Guide](./profiling-systems-guide.md)
- [Generation Systems Guide](./generation-systems-guide.md)
- [Evolution Systems Guide](./evolution-systems-guide.md)
- [Similarity Systems Guide](./similarity-systems-guide.md)
- [API Systems Guide](./api-systems-guide.md)
