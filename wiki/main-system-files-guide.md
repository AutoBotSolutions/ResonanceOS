# Main System Files Guide - ResonanceOS v6

## Overview

The Main System Files module provides the primary entry points and orchestration scripts for ResonanceOS v6. These files serve as the main interfaces for system demonstration, complete system running, and comprehensive testing.

## System Architecture

```
Main System Files
├── demo.py (System Demonstration)
├── system_runner.py (System Orchestration)
└── test_runner.py (Comprehensive Testing)
```

## System Components

### 1. Demo (`demo.py`)

A comprehensive demonstration script showcasing all major ResonanceOS v6 capabilities.

#### Architecture

```python
def demo_complete_system():
    """Demonstrate the complete ResonanceOS v6 system"""
    
    # 1. HRV Extraction Demo
    # 2. Content Generation Demo
    # 3. HRV Analysis of Generated Content
    # 4. Profile Management Demo
    # 5. API Demo
    # 6. System Summary
```

#### Demo Components

**1. HRV Vector Extraction**
- Demonstrates HRV extraction from sample text
- Shows 8-dimensional HRV vector output
- Displays vector length verification

**2. Human-Resonant Content Generation**
- Shows content generation from prompts
- Demonstrates HumanResonantWriter functionality
- Displays generated content

**3. HRV Analysis of Generated Content**
- Extracts HRV from generated content
- Compares with original extraction
- Shows consistency of HRV system

**4. Multi-Tenant Profile Management**
- Creates profiles for different tenants
- Demonstrates save/load functionality
- Shows profile listing capability

**5. API Interface Demo**
- Demonstrates API request/response
- Shows SimpleRequest and hr_generate usage
- Displays HRV feedback from API

**6. System Summary**
- Provides status check for all components
- Confirms system operational status
- Shows readiness for production

#### Usage

```bash
# Run the complete demo
python demo.py
```

#### Expected Output

```
🚀 ResonanceOS v6 - Complete System Demo
============================================================

1. HRV Vector Extraction
------------------------------
Input text: 'This is an amazing and wonderful example...'
HRV Vector: ['0.123', '0.456', ...]
Dimensions: 8

2. Human-Resonant Content Generation
----------------------------------------
Prompt: 'The future of sustainable energy'
Generated Content: [Generated text appears here]

...

🎉 ResonanceOS v6 System Status: FULLY OPERATIONAL
📊 All 8 HRV dimensions working correctly
🔧 Modular architecture verified
🚀 Ready for production deployment
```

### 2. System Runner (`system_runner.py`)

Complete system orchestration and integration testing framework.

#### Architecture

```python
class ResonanceOSSystemRunner:
    """Complete system runner for ResonanceOS v6"""
    
    def __init__(self):
        # Initialize system components
        self.writer = HumanResonantWriter()
        self.hrf_model = HRFModel()
        self.extractor = HRVExtractor()
        self.profile_manager = HRVProfileManager(...)
    
    def run_system_diagnostics(self) -> Dict[str, Any]
    def run_complete_system_test(self) -> Dict[str, Any]
    def run_performance_benchmark(self) -> Dict[str, Any]
    def generate_system_report(self) -> Dict[str, Any]
    def run_cli_interface(self, args: Optional[List[str]] = None)
    def start_api_server(self, host: str = "localhost", port: int = 8000)
```

#### Key Features

**System Diagnostics**
- Tests all core components
- Verifies data directory structure
- Provides health status assessment
- Generates diagnostic report

**Complete System Test**
- End-to-end content generation
- Profile-based generation
- Multi-profile comparison
- Data processing pipeline
- Comprehensive test reporting

**Performance Benchmarking**
- Content generation speed
- HRV extraction speed
- HRF model speed
- Overall performance assessment

**System Report Generation**
- Comprehensive system information
- Diagnostic results
- Test results
- Benchmark results
- JSON export capability

**CLI Interface**
- Integrated CLI execution
- Argument passing
- Help display

**API Server**
- API server startup
- Configuration options
- Health check endpoints
- Documentation access

#### Usage

```bash
# Run system diagnostics
python system_runner.py --diagnostics

# Run complete system tests
python system_runner.py --test

# Run performance benchmarks
python system_runner.py --benchmark

# Generate comprehensive system report
python system_runner.py --report

# Run CLI interface
python system_runner.py --cli --prompt "Test prompt"

# Start API server
python system_runner.py --serve --host localhost --port 8000

# Run everything
python system_runner.py --all
```

#### Command-Line Arguments

- `--diagnostics`: Run system diagnostics
- `--test`: Run complete system tests
- `--benchmark`: Run performance benchmarks
- `--report`: Generate comprehensive system report
- `--cli [args...]`: Run CLI interface with optional arguments
- `--serve`: Start API server
- `--host HOST`: API server host (default: localhost)
- `--port PORT`: API server port (default: 8000)
- `--all`: Run all checks and generate report

#### System Diagnostics Output

```
🔍 Running System Diagnostics
============================================================

📊 Testing HRF Model...
✅ HRF Model: Score 0.523

🧠 Testing HRV Extractor...
✅ HRV Extractor: Vector 8 dimensions

✍️ Testing Human Resonant Writer...
✅ Writer: Generated 150 characters

📁 Testing Profile Manager...
✅ Profile Manager: Save/Load test passed

🌐 Testing API Integration...
✅ API Integration: Response received

📂 Checking Data Directories...
✅ config: Exists with files
✅ samples: Exists with files
...

🎉 System Health: HEALTHY
```

#### Performance Benchmark Output

```
⚡ Running Performance Benchmarks
============================================================

📝 Benchmarking Content Generation Speed...
   AI technology benefits...: 0.234s (120 chars)
   Business strategy overview...: 0.189s (145 chars)
   Innovation in healthcare...: 0.256s (138 chars)

🧠 Benchmarking HRV Extraction Speed...
   12 chars: 0.002s
   78 chars: 0.003s
   156 chars: 0.004s

📊 Benchmarking HRF Model Speed...
   Score 0.678: 0.001s
   Score 0.234: 0.001s
   Score 0.891: 0.001s

📊 Performance Summary:
   Generation: 0.226s avg
   Extraction: 0.003s avg
   HRF Model: 0.001s avg
   Overall: excellent
```

### 3. Test Runner (`test_runner.py`)

Comprehensive testing framework with unit tests, integration tests, and performance tests.

#### Architecture

```python
def test_hrf_model()
def test_hrv_extractor()
def test_human_resonant_writer()
def test_profile_manager()
def test_cli_functionality()

def run_integration_tests() -> bool
def run_performance_tests() -> bool

def run_all_tests() -> bool
```

#### Test Categories

**Basic Component Tests**
- HRF Model: Validates score range [0, 1]
- HRV Extractor: Validates vector length and types
- Human Resonant Writer: Validates output type and content
- Profile Manager: Validates save/load/list operations
- CLI Functionality: Validates API integration

**Integration Tests**
- API Integration: Tests request/response flow
- Multi-component Workflow: Tests end-to-end pipeline
- Component Interaction: Validates system integration

**Performance Tests**
- Generation Performance: Validates speed (< 5.0s average)
- Extraction Performance: Validates speed (< 0.1s average)
- HRF Model Performance: Validates speed (< 0.1s average)

**Unit Tests**
- Comprehensive unit test suite
- Detailed component testing
- Edge case coverage

#### Usage

```bash
# Run all tests
python test_runner.py

# Run basic tests only
python test_runner.py --basic

# Run integration tests only
python test_runner.py --integration

# Run performance tests only
python test_runner.py --performance

# Run unit tests only
python test_runner.py --unit

# Verbose output
python test_runner.py --verbose
```

#### Test Output

```
🧪 Running ResonanceOS v6 Complete Test Suite
============================================================

📊 Basic Component Tests
----------------------------------------
✓ HRF Model test passed
✓ HRV Extractor test passed
✓ Human Resonant Writer test passed
✓ HRV Profile Manager test passed
✓ CLI functionality test passed

🔗 Integration Tests
----------------------------------------
✓ API Integration test passed
✓ Multi-component workflow test passed

⚡ Performance Tests
----------------------------------------
✓ Generation performance: 0.223s average
✓ Extraction performance: 0.003s average
✓ HRF model performance: 0.001s average

🔬 Comprehensive Unit Tests
----------------------------------------
Running unit tests...
...

============================================================
📊 Test Results Summary
============================================================
Total Tests: 8
Passed: 8
Failed: 0
Success Rate: 100.0%

💾 Results saved to: resonance_os/data/exports/reports/test_results_20240115_143052.json

🎉 All tests passed! ResonanceOS v6 is working correctly.
✅ System is ready for production use!
```

#### Test Results Format

```json
{
  "timestamp": "2024-01-15 14:30:52",
  "tests": {
    "HRF Model": {"status": "passed", "error": null},
    "HRV Extractor": {"status": "passed", "error": null},
    "Human Resonant Writer": {"status": "passed", "error": null},
    "Profile Manager": {"status": "passed", "error": null},
    "CLI Functionality": {"status": "passed", "error": null},
    "Integration": {"status": "passed", "error": null},
    "Performance": {"status": "passed", "error": null},
    "Unit_Tests": {
      "status": "passed",
      "total": 15,
      "failures": 0,
      "errors": 0,
      "error": null
    }
  },
  "summary": {
    "total_tests": 8,
    "passed": 8,
    "failed": 0,
    "success_rate": 100.0,
    "overall_status": "passed"
  }
}
```

## Integration Points

The Main System Files module integrates with:

- **Core Systems**: Uses HRV types and constants
- **Generation Systems**: Uses HumanResonantWriter and HRFModel
- **Profile Systems**: Uses HRVProfileManager
- **API Systems**: Uses SimpleRequest and hr_generate
- **CLI Systems**: Uses CLI main function
- **Data Systems**: Uses data directories for reports

## Usage Patterns

### Quick System Check

```bash
# Run demo to verify system operation
python demo.py

# Run diagnostics for detailed check
python system_runner.py --diagnostics
```

### Comprehensive Testing

```bash
# Run all tests
python test_runner.py

# Run complete system check
python system_runner.py --all
```

### Development Workflow

```bash
# 1. Run quick demo
python demo.py

# 2. Run diagnostics
python system_runner.py --diagnostics

# 3. Run tests
python test_runner.py

# 4. Run benchmarks
python system_runner.py --benchmark

# 5. Generate report
python system_runner.py --report
```

### Production Deployment

```bash
# 1. Run comprehensive checks
python system_runner.py --all

# 2. Run full test suite
python test_runner.py

# 3. Start API server
python system_runner.py --serve --host 0.0.0.0 --port 8000
```

## Best Practices

1. **Run demo first**: Use demo.py for quick system verification
2. **Regular diagnostics**: Run diagnostics periodically to monitor system health
3. **Comprehensive testing**: Run full test suite before deployment
4. **Performance monitoring**: Run benchmarks to track performance over time
5. **Report generation**: Generate reports for documentation and analysis

## Common Issues

**Issue**: Import errors when running scripts
**Solution**: Ensure resonance_os is in Python path and dependencies are installed

**Issue**: Data directory not found
**Solution**: Run system_runner.py with --diagnostics to create directories

**Issue**: Tests failing
**Solution**: Check test output for specific error messages and fix accordingly

**Issue**: API server won't start
**Solution**: Install uvicorn: `pip install uvicorn`

## Performance Considerations

- **Demo**: Fast (< 5 seconds)
- **Diagnostics**: Moderate (< 30 seconds)
- **Tests**: Moderate (< 2 minutes)
- **Benchmarks**: Moderate (< 1 minute)
- **Report**: Moderate (< 2 minutes)

## Dependencies

All main system files require:

- Python 3.7+
- resonance_os package
- Standard library modules (sys, os, json, time, argparse, pathlib)
- For API server: uvicorn
- For comprehensive tests: unittest

## Future Enhancements

- **Web interface**: Web-based system dashboard
- **Scheduled testing**: Automated test scheduling
- **Performance monitoring**: Continuous performance tracking
- **Alert system**: Automated alerts for system issues
- **Docker support**: Containerized deployment scripts
- **Cloud deployment**: Cloud deployment automation

## Troubleshooting

**Issue**: Module not found errors
**Solution**: Ensure project root is in Python path

**Issue**: Permission denied
**Solution**: Check file permissions on data directories

**Issue**: Port already in use
**Solution**: Use different port with --port argument

**Issue**: Tests timeout
**Solution**: Increase timeout or check system resources

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Generation Systems Guide](./generation-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [API Systems Guide](./api-systems-guide.md)
