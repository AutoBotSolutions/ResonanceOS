# ResonanceOS v6 Test Suite

This directory contains comprehensive tests for the ResonanceOS v6 Human-Resonant AI Writing System.

## Test Structure

### Core Module Tests
- `test_core_hrv_constants.py` - Tests HRV dimension constants
- `test_core_hrv_types.py` - Tests HRV type definitions

### Profile Management Tests
- `test_profiles_hrv_extractor.py` - Tests HRV vector extraction
- `test_profiles_multi_tenant_hr_profiles.py` - Tests multi-tenant profile management

### Generation Module Tests
- `test_generation_hrf_model.py` - Tests Human Resonance Feedback model
- `test_generation_planner_layer.py` - Tests content planning layer
- `test_generation_sentence_layer.py` - Tests sentence generation layer
- `test_generation_refiner_layer.py` - Tests content refinement layer
- `test_generation_human_resonant_writer.py` - Tests main writer integration

### API Tests
- `test_api_hr_server.py` - Tests FastAPI server and endpoints

### CLI Tests
- `test_cli_hr_main.py` - Tests command-line interface

### Integration Tests
- `test_integration.py` - Tests cross-component integration

### Specialized Tests
- `test_edge_cases.py` - Tests edge cases and boundary conditions
- `test_performance.py` - Tests performance characteristics

## Running Tests

### Run All Tests
```bash
cd /home/giganutt/artificial_intelligence/mimic
python -m resonance_os.tests.run_all_tests
```

### Run Tests by Category
```bash
python -m resonance_os.tests.run_all_tests --category
```

### Run Specific Test Module
```bash
python -m resonance_os.tests.run_all_tests test_core_hrv_constants
```

### Run Individual Test File
```bash
cd /home/giganutt/artificial_intelligence/mimic
python -m resonance_os.tests.test_core_hrv_constants
```

## Test Coverage

The test suite provides comprehensive coverage of:

- **Functionality Testing**: All core functions and methods
- **Integration Testing**: Cross-component interactions
- **Edge Case Testing**: Boundary conditions and error scenarios
- **Performance Testing**: Speed and memory usage
- **Error Handling**: Invalid inputs and exception scenarios

## Test Categories

### 1. Core Tests
Verify fundamental constants and type definitions:
- HRV dimension definitions
- Type annotations and aliases
- Data structure validation

### 2. Profile Tests
Test profile management functionality:
- HRV vector extraction from text
- Multi-tenant profile storage/retrieval
- Profile persistence and consistency

### 3. Generation Tests
Validate content generation pipeline:
- HRF model predictions
- Planning layer functionality
- Sentence generation with HRV targeting
- Content refinement with feedback
- End-to-end writer integration

### 4. API Tests
Test REST API functionality:
- Request/response handling
- Parameter validation
- Integration with core components

### 5. CLI Tests
Validate command-line interface:
- Argument parsing
- Output formatting
- Integration with API layer

### 6. Integration Tests
Test system-wide integration:
- Full pipeline workflows
- Component interaction
- Data flow validation

### 7. Edge Case Tests
Test boundary conditions:
- Extreme input values
- Unicode and special characters
- Empty/null inputs
- File system limitations

### 8. Performance Tests
Validate performance characteristics:
- Response times
- Memory usage
- Scalability
- Concurrent operations

## Test Data

Tests use:
- Temporary directories for file operations
- Mock data for HRV vectors
- Sample prompts for generation
- Edge case inputs for robustness

## Expected Results

All tests should pass with:
- 100% functionality verified
- No critical errors
- Performance within acceptable thresholds
- Proper error handling

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Python path includes project root
2. **File Permissions**: Tests use temporary directories
3. **Memory Issues**: Large tests may require sufficient memory
4. **Performance**: Some tests may be slow on limited hardware

### Debug Mode

Run tests with verbose output:
```bash
python -m resonance_os.tests.run_all_tests -v
```

### Individual Test Debugging

Run specific test with detailed output:
```bash
python -m unittest resonance_os.tests.test_module_name.TestClassName.test_method_name -v
```

## Test Metrics

The test suite validates:
- **8 HRV Dimensions**: All dimensions properly measured
- **Multi-Tenancy**: Profile isolation and management
- **Generation Pipeline**: End-to-end content creation
- **API Integration**: Request/response handling
- **CLI Functionality**: Command-line operations
- **Performance**: Sub-second response times
- **Robustness**: Error handling and edge cases

## Continuous Integration

These tests are designed for:
- Automated CI/CD pipelines
- Pre-deployment validation
- Regression testing
- Performance monitoring

## Extending Tests

To add new tests:

1. Follow existing naming conventions (`test_*.py`)
2. Use `unittest` framework
3. Include setup/teardown for resources
4. Test both success and failure cases
5. Add performance benchmarks where relevant
6. Update this README

## Test Best Practices

- Use descriptive test names
- Test one thing per test method
- Use assertions with clear messages
- Clean up resources in tearDown
- Mock external dependencies
- Test edge cases and error conditions
- Include performance benchmarks

This comprehensive test suite ensures ResonanceOS v6 maintains high quality and reliability across all components.
