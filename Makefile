# ResonanceOS v6 Makefile
# Complete system automation and management

.PHONY: help install setup test clean serve docs benchmark report all

# Default target
help:
	@echo "🎯 ResonanceOS v6 - Available Commands"
	@echo "======================================"
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  make install     - Complete system setup"
	@echo "  make setup       - Alternative setup command"
	@echo "  make clean       - Clean temporary files"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  make test        - Run all tests"
	@echo "  make test-basic  - Run basic tests only"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-performance - Run performance tests"
	@echo ""
	@echo "🚀 System Operations:"
	@echo "  make serve       - Start API server"
	@echo "  make benchmark   - Run performance benchmarks"
	@echo "  make report      - Generate system report"
	@echo "  make diagnostics - Run system diagnostics"
	@echo ""
	@echo "📚 Documentation & Examples:"
	@echo "  make docs        - View documentation"
	@echo "  make examples    - Run examples"
	@echo "  make tutorial    - Run getting started tutorial"
	@echo ""
	@echo "🔧 System Management:"
	@echo "  make all         - Run complete system check"
	@echo "  make status      - Show system status"
	@echo "  make verify      - Verify installation"

# Installation & Setup
install:
	@echo "📦 Installing ResonanceOS v6..."
	python setup.py

setup:
	@echo "🔧 Setting up ResonanceOS v6..."
	python setup.py

# Testing
test:
	@echo "🧪 Running complete test suite..."
	python test_runner.py

test-basic:
	@echo "🧪 Running basic tests..."
	python test_runner.py --basic

test-integration:
	@echo "🔗 Running integration tests..."
	python test_runner.py --integration

test-performance:
	@echo "⚡ Running performance tests..."
	python test_runner.py --performance

test-unit:
	@echo "🔬 Running unit tests..."
	python test_runner.py --unit

# System Operations
serve:
	@echo "🌐 Starting API server..."
	python system_runner.py --serve

benchmark:
	@echo "⚡ Running performance benchmarks..."
	python system_runner.py --benchmark

report:
	@echo "📋 Generating system report..."
	python system_runner.py --report

diagnostics:
	@echo "🔍 Running system diagnostics..."
	python system_runner.py --diagnostics

# Documentation & Examples
docs:
	@echo "📚 Opening documentation..."
	@echo "Main README: open README.md"
	@echo "Data Directory: open resonance_os/data/README.md"
	@echo "Examples: open examples/README.md"

examples:
	@echo "📚 Running examples..."
	python examples/tutorials/getting_started.py

tutorial:
	@echo "🎓 Running getting started tutorial..."
	python examples/tutorials/getting_started.py

# System Management
all:
	@echo "🎯 Running complete system check..."
	python system_runner.py --all

status:
	@echo "📊 System Status:"
	@echo "=================="
	@echo "Python Version: $$(python --version)"
	@echo "Working Directory: $$(pwd)"
	@echo "Project Structure:"
	@echo "  - Core modules: $$(find resonance_os -name "*.py" | wc -l)"
	@echo "  - Test files: $$(find tests -name "*.py" | wc -l)"
	@echo "  - Examples: $$(find examples -name "*.py" | wc -l)"
	@echo "  - Data files: $$(find resonance_os/data -type f | wc -l)"

verify:
	@echo "🔍 Verifying installation..."
	python setup.py --check-only

# Development Commands
dev-setup:
	@echo "🛠️ Development setup..."
	python setup.py
	python test_runner.py --basic
	python system_runner.py --diagnostics

dev-test:
	@echo "🧪 Development test cycle..."
	python test_runner.py --basic
	python system_runner.py --benchmark

dev-serve:
	@echo "🌐 Development server..."
	python system_runner.py --serve --host localhost --port 8000

# Cleanup
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	@echo "✅ Cleanup completed"

# Advanced Commands
profile-analysis:
	@echo "📊 Running profile analysis..."
	python examples/tutorials/profile_mastery.py

corpus-analysis:
	@echo "📚 Running corpus analysis..."
	python examples/data_science_examples/corpus_analysis.py

api-test:
	@echo "🌐 Testing API integration..."
	python examples/integration_examples/api_integration.py

batch-test:
	@echo "📦 Running batch processing test..."
	python examples/advanced_usage/batch_processing.py

# Production Commands
prod-setup:
	@echo "🏭 Production setup..."
	python setup.py
	python test_runner.py
	python system_runner.py --all

prod-deploy:
	@echo "🚀 Production deployment preparation..."
	python system_runner.py --report
	python test_runner.py --performance
	@echo "✅ Production deployment ready"

# Monitoring
monitor:
	@echo "📈 System monitoring..."
	@echo "CPU Usage: $$(top -bn1 | grep "Cpu(s)" | awk '{print $$2}' | cut -d'%' -f1)"
	@echo "Memory Usage: $$(free -m | awk 'NR==2{printf "%.1f%%", $$3*100/$$2 }')"
	@echo "Disk Usage: $$(df -h . | awk 'NR==2{print $$5}')"

# Quick Start Commands
quick-start:
	@echo "🚀 Quick start sequence..."
	python setup.py
	python test_runner.py --basic
	python examples/tutorials/getting_started.py
	@echo "✅ Quick start completed!"

quick-test:
	@echo "⚡ Quick system test..."
	python test_runner.py --basic
	python system_runner.py --diagnostics
	@echo "✅ Quick test completed!"

# Backup Commands
backup:
	@echo "💾 Creating backup..."
	mkdir -p backups
	tar -czf "backups/resonanceos_backup_$$(date +%Y%m%d_%H%M%S).tar.gz" \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.git' \
		--exclude='backups' \
		resonance_os/ examples/ tests/ *.py *.md
	@echo "✅ Backup created in backups/ directory"

restore:
	@echo "📥 Restore from backup (manual process)"
	@echo "Available backups:"
	@ls -la backups/ || echo "No backups found"
	@echo "To restore: tar -xzf backups/backup_file.tar.gz"

# Version Information
version:
	@echo "📋 ResonanceOS v6 Information"
	@echo "==============================="
	@echo "Version: 6.0.0"
	@echo "Python: $$(python --version)"
	@echo "Platform: $$(uname -s)"
	@echo "Architecture: $$(uname -m)"
	@echo "Install Date: $$(date)"

# Help for specific areas
help-testing:
	@echo "🧪 Testing Commands Help"
	@echo "======================="
	@echo "make test          - Run all tests"
	@echo "make test-basic    - Basic component tests"
	@echo "make test-integration - Integration tests"
	@echo "make test-performance - Performance tests"
	@echo "make test-unit     - Unit tests only"

help-development:
	@echo "🛠️ Development Commands Help"
	@echo "=============================="
	@echo "make dev-setup     - Development environment setup"
	@echo "make dev-test      - Development test cycle"
	@echo "make dev-serve     - Development server"
	@echo "make clean         - Clean temporary files"

help-production:
	@echo "🏭 Production Commands Help"
	@echo "==============================="
	@echo "make prod-setup    - Production setup"
	@echo "make prod-deploy   - Deployment preparation"
	@echo "make backup        - Create backup"
	@echo "make monitor       - System monitoring"
