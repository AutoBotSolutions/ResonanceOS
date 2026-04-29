# CLI Systems Guide - ResonanceOS v6

## Overview

The CLI Systems module provides a command-line interface for ResonanceOS v6, enabling direct access to human-resonant content generation from terminal environments. This module offers a simple, scriptable interface for automation and batch processing workflows.

## System Architecture

```
CLI Systems
├── hr_main.py (Main CLI Entry Point)
└── Argument Parser
```

## System Components

### 1. HR Main (`hr_main.py`)

The primary command-line interface for human-resonant content generation.

#### Architecture

```python
def main():
    parser = argparse.ArgumentParser(description="Human-Resonant CLI")
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--tenant", type=str, default=None)
    parser.add_argument("--profile", type=str, default=None)
    args = parser.parse_args()

    req = SimpleRequest(prompt=args.prompt, tenant=args.tenant, profile_name=args.profile)
    resp = hr_generate(req)
    print("=== Generated Human-Resonant Article ===")
    print(resp.article)
    print("=== HRV Feedback ===")
    print(resp.hrv_feedback)
```

#### Command-Line Arguments

- `--prompt` (required): Content generation prompt
- `--tenant` (optional): Tenant identifier for multi-tenant profile management
- `--profile` (optional): Profile name for HRV targeting

## Usage

### Basic Usage

```bash
python -m resonance_os.cli.hr_main --prompt "The future of artificial intelligence"
```

### With Profile

```bash
python -m resonance_os.cli.hr_main --prompt "Climate change solutions" --profile professional
```

### With Tenant

```bash
python -m resonance_os.cli.hr_main --prompt "Machine learning applications" --tenant company_a --profile brand_voice
```

### Output Format

```
=== Generated Human-Resonant Article ===
[Generated content appears here...]

=== HRV Feedback ===
[0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
```

## Integration Patterns

### Shell Script Integration

```bash
#!/bin/bash
# generate_content.sh

PROMPT="$1"
PROFILE="${2:-professional}"

python -m resonance_os.cli.hr_main \
    --prompt "$PROMPT" \
    --profile "$PROFILE"
```

### Batch Processing

```bash
#!/bin/bash
# batch_generate.sh

while IFS= read -r prompt; do
    python -m resonance_os.cli.hr_main --prompt "$prompt" --profile professional
    echo "---"
done < prompts.txt
```

### Integration with Other Tools

```bash
# Generate content and save to file
python -m resonance_os.cli.hr_main \
    --prompt "AI in healthcare" \
    --profile academic \
    > healthcare_ai.txt

# Generate and post-process
python -m resonance_os.cli.hr_main \
    --prompt "Sustainable technology" \
    --profile environmental \
    | grep -v "===" \
    | sed 's/\[Refined.*\]//g' \
    > final_content.txt
```

## Advanced Usage

### Custom Profile Selection

```bash
# List available profiles
ls profiles/hr_profiles/default/

# Use specific profile
python -m resonance_os.cli.hr_main \
    --prompt "Marketing content" \
    --profile enthusiastic_marketer
```

### Multi-Tenant Workflow

```bash
# Generate for different tenants
for tenant in company_a company_b company_c; do
    python -m resonance_os.cli.hr_main \
        --prompt "Annual report summary" \
        --tenant "$tenant" \
        --profile corporate \
        > "${tenant}_report.txt"
done
```

### Output Formatting

```bash
# JSON output (requires modification)
python -m resonance_os.cli.hr_main \
    --prompt "Technical documentation" \
    --profile technical \
    | python -c "import sys, json; print(json.dumps({'content': sys.stdin.read()}))"
```

## Integration Points

The CLI Systems module integrates with:

- **API Systems**: Uses SimpleRequest and hr_generate functions
- **Generation Systems**: Leverages HumanResonantWriter for content generation
- **Profile Systems**: Uses profile management for HRV targeting

## Configuration

### Default Profile

If no profile is specified, the CLI uses the default profile. This can be customized by modifying the initialization:

```python
# In hr_main.py
profile_name = args.profile if args.profile else "default"
```

### Custom Output Format

The output format can be customized by modifying the print statements in the main function:

```python
# Custom format
print(f"Content: {resp.article}")
print(f"HRV: {', '.join(map(str, resp.hrv_feedback))}")
```

## Performance Considerations

- **Fast startup**: Minimal initialization overhead
- **Low memory**: No persistent state between calls
- **Scriptable**: Suitable for automation and batch processing
- **No dependencies**: Uses only standard library and resonance_os modules

## Best Practices

1. **Use profiles**: Leverage profile system for consistent results
2. **Validate prompts**: Check prompt quality before generation
3. **Handle errors**: Implement error handling in shell scripts
4. **Log usage**: Track CLI usage for monitoring
5. **Batch efficiently**: Use batch processing for multiple prompts

## Common Issues

**Issue**: Missing required argument
**Solution**: Ensure `--prompt` is provided with valid content

**Issue**: Profile not found
**Solution**: Verify profile exists in the profiles directory

**Issue**: Permission denied
**Solution**: Ensure Python executable has execute permissions

**Issue**: Import errors
**Solution**: Ensure resonance_os is properly installed

## Troubleshooting

**Issue**: Command not found
**Solution**: Use full path or ensure resonance_os is in Python path

**Issue**: Empty output
**Solution**: Check prompt quality and ensure generation components work

**Issue**: HRV feedback not showing
**Solution**: Verify API integration is working correctly

## Future Enhancements

- **Interactive Mode**: Interactive prompt-based generation
- **File Input**: Read prompts from files
- **Output Options**: Multiple output formats (JSON, Markdown, plain text)
- **Progress Indicators**: Show generation progress
- **Profile Management**: CLI commands for profile operations
- **Batch Mode**: Built-in batch processing
- **Configuration File**: Support for configuration files

## Scripting Examples

### Python Script Integration

```python
import subprocess

def generate_content(prompt: str, profile: str = None) -> str:
    cmd = [
        "python", "-m", "resonance_os.cli.hr_main",
        "--prompt", prompt
    ]
    if profile:
        cmd.extend(["--profile", profile])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

# Usage
content = generate_content("AI applications", "professional")
print(content)
```

### Makefile Integration

```makefile
# Makefile

.PHONY: generate

generate:
    python -m resonance_os.cli.hr_main --prompt "$(PROMPT)" --profile "$(PROFILE)"

.PHONY: batch

batch:
    for prompt in $$(cat prompts.txt); do \
        make generate PROMPT="$$prompt" PROFILE="professional"; \
    done
```

## Exit Codes

- `0`: Success
- `1`: Error (invalid arguments, missing profile, etc.)

## Environment Variables

Currently, the CLI does not use environment variables. Future versions may support:

- `RESONANCE_PROFILE_PATH`: Custom profile directory
- `RESONANCE_DEFAULT_PROFILE`: Default profile name
- `RESONANCE_TENANT`: Default tenant identifier

## References

- [API Systems Guide](./api-systems-guide.md)
- [Generation Systems Guide](./generation-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
