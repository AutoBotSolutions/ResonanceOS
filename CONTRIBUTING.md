# Contributing to ResonanceOS v6

Thank you for your interest in contributing to ResonanceOS v6! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community for all contributors.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When reporting a bug, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Environment details (Python version, OS, etc.)
- Relevant code snippets or error messages
- Any relevant screenshots or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- A clear description of the proposed enhancement
- Motivation for the enhancement
- Potential implementation approach (if known)
- Any relevant examples or references

### Pull Requests

1. **Fork the repository** on GitHub
2. **Create a branch** for your feature or fix
3. **Make your changes** following the coding standards
4. **Write tests** for new functionality
5. **Update documentation** as needed
6. **Commit your changes** with clear, descriptive messages
7. **Push to your fork** and submit a pull request

### Coding Standards

- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Write tests for new features
- Update the README and documentation as needed

### Development Workflow

```bash
# Clone your fork
git clone https://github.com/your-username/mimic.git
cd mimic

# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Run tests
python test_runner.py

# Commit changes
git add .
git commit -m "Add your descriptive commit message"

# Push to your fork
git push origin feature/your-feature-name

# Create a pull request on GitHub
```

### Testing

Ensure all tests pass before submitting a pull request:

```bash
# Run all tests
python test_runner.py

# Run specific test categories
python test_runner.py --basic
python test_runner.py --integration
python test_runner.py --unit
```

### Documentation

- Keep documentation up-to-date with code changes
- Use clear and concise language
- Include examples for new features
- Update the README if needed

## Project Structure

```
resonance_os/
├── core/                    # Core constants and types
├── generation/              # Content generation pipeline
├── profiles/                # Profile management
├── api/                     # REST API
└── cli/                     # Command line interface
```

## Getting Help

- Check the [documentation](https://roberttrenaman.github.io/mimic/)
- Review existing issues and pull requests
- Open a new issue if you can't find an answer

## License

By contributing to ResonanceOS v6, you agree that your contributions will be licensed under the MPL-2.0 License.

## Recognition

Contributors will be acknowledged in the project documentation. Thank you for your contributions!

---

For questions about contributing, please open an issue or contact the maintainers.
