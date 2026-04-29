# Tests Systems Guide - ResonanceOS v6

## Overview

The Tests Systems module provides comprehensive testing infrastructure for ResonanceOS v6, including unit tests, integration tests, performance tests, and edge case testing. This module ensures system reliability, correctness, and performance through automated testing.

## System Architecture

```
Tests Systems
├── run_all_tests.py (Test Runner)
├── test_core_hrv_constants.py (Core Constants Tests)
├── test_core_hrv_types.py (Core Types Tests)
├── test_generation_hrf_model.py (HRF Model Tests)
├── test_generation_human_resonant_writer.py (Writer Tests)
├── test_generation_planner_layer.py (Planner Tests)
├── test_generation_refiner_layer.py (Refiner Tests)
├── test_generation_sentence_layer.py (Sentence Tests)
├── test_profiles_hrv_extractor.py (Extractor Tests)
├── test_profiles_multi_tenant_hr_profiles.py (Profile Manager Tests)
├── test_api_hr_server.py (API Tests)
├── test_cli_hr_main.py (CLI Tests)
├── test_integration.py (Integration Tests)
├── test_edge_cases.py (Edge Case Tests)
└── test_performance.py (Performance Tests)
```

## System Components

### 1. Test Runner (`run_all_tests.py`)

Main test runner that executes all test suites and generates comprehensive reports.

#### Architecture

```python
def run_all_tests():
    """Run all test suites"""
    # Core tests
    # Generation tests
    # Profile tests
    # API tests
    # CLI tests
    # Integration tests
    # Performance tests
    # Edge case tests
```

#### Usage

```bash
# Run all tests
python -m resonance_os.tests.run_all_tests

# Run specific test module
python -m pytest resonance_os/tests/test_core_hrv_constants.py

# Run with coverage
pytest --cov=resonance_os resonance_os/tests/
```

#### Test Categories

**Core Tests**
- HRV constants validation
- Type definitions verification
- Configuration management

**Generation Tests**
- HRF model functionality
- Human resonant writer
- Planner, sentence, refiner layers

**Profile Tests**
- HRV extraction accuracy
- Multi-tenant profile management
- Profile persistence

**API Tests**
- Endpoint functionality
- Request/response handling
- Error handling

**CLI Tests**
- Command-line interface
- Argument parsing
- Output formatting

**Integration Tests**
- End-to-end workflows
- Component interaction
- System integration

**Performance Tests**
- Generation speed
- Extraction performance
- Memory usage

**Edge Case Tests**
- Boundary conditions
- Error scenarios
- Invalid inputs

### 2. Core Tests

#### HRV Constants Tests (`test_core_hrv_constants.py`)

Tests the HRV dimension definitions and system constants.

```python
def test_hrv_dimensions():
    """Test HRV dimensions are defined correctly"""
    assert len(HRV_DIMENSIONS) == 8
    assert "sentence_variance" in HRV_DIMENSIONS
    # ... more assertions

def test_default_thresholds():
    """Test default threshold values"""
    assert DEFAULT_RESONANCE_THRESHOLD == 0.92
    assert DEFAULT_DRIFT_THRESHOLD == 0.05
```

#### HRV Types Tests (`test_core_hrv_types.py`)

Tests type definitions and data structures.

```python
def test_resonance_vector_creation():
    """Test ResonanceVector creation"""
    vector = ResonanceVector(
        values=[0.5, 0.6, 0.7, 0.8, 0.5, 0.4, 0.6, 0.7],
        dimensions=HRV_DIMENSIONS
    )
    assert len(vector.values) == 8
    assert vector.confidence == 1.0
```

### 3. Generation Tests

#### HRF Model Tests (`test_generation_hrf_model.py`)

Tests the Human-Resonance Feedback model.

```python
def test_hrf_predict():
    """Test HRF prediction returns valid score"""
    hrf = HRFModel()
    score = hrf.predict("Test sentence")
    assert 0.0 <= score <= 1.0

def test_hrf_empty_text():
    """Test HRF handles empty text"""
    hrf = HRFModel()
    score = hrf.predict("")
    assert 0.0 <= score <= 1.0
```

#### Human Resonant Writer Tests (`test_generation_human_resonant_writer.py`)

Tests the main generation orchestrator.

```python
def test_writer_generate():
    """Test content generation"""
    writer = HumanResonantWriter()
    content = writer.generate("Test prompt")
    assert isinstance(content, str)
    assert len(content) > 0

def test_writer_with_profile():
    """Test generation with profile"""
    writer = HumanResonantWriter()
    # Test with profile integration
```

#### Layer Tests

**Planner Layer Tests (`test_generation_planner_layer.py`)**
```python
def test_planner_plan_paragraphs():
    """Test paragraph planning"""
    planner = PlannerLayer()
    paragraphs, hrvs = planner.plan_paragraphs("Test prompt", num_paragraphs=3)
    assert len(paragraphs) == 3
    assert len(hrvs) == 3
```

**Sentence Layer Tests (`test_generation_sentence_layer.py`)**
```python
def test_sentence_generate():
    """Test sentence generation"""
    layer = SentenceLayer()
    sentences = layer.generate_sentences("Test outline", [0.5]*8)
    assert len(sentences) > 0
```

**Refiner Layer Tests (`test_generation_refiner_layer.py`)**
```python
def test_refiner_refine():
    """Test sentence refinement"""
    refiner = RefinerLayer()
    refined = refiner.refine("Original sentence", 0.7)
    assert "Refined" in refined
```

### 4. Profile Tests

#### HRV Extractor Tests (`test_profiles_hrv_extractor.py`)

Tests HRV extraction functionality.

```python
def test_extract_basic():
    """Test basic HRV extraction"""
    extractor = HRVExtractor()
    hrv = extractor.extract("Test sentence.")
    assert len(hrv) == 8
    assert all(isinstance(x, (int, float)) for x in hrv)

def test_extract_empty():
    """Test extraction from empty text"""
    extractor = HRVExtractor()
    hrv = extractor.extract("")
    assert len(hrv) == 8
```

#### Multi-Tenant Profile Manager Tests (`test_profiles_multi_tenant_hr_profiles.py`)

Tests profile management with multi-tenant support.

```python
def test_save_load_profile():
    """Test profile save and load"""
    manager = HRVProfileManager(temp_dir)
    hrv = [0.5, 0.6, 0.7, 0.8, 0.5, 0.4, 0.6, 0.7]
    manager.save_profile("tenant", "profile", hrv)
    loaded = manager.load_profile("tenant", "profile")
    assert loaded == hrv

def test_list_profiles():
    """Test profile listing"""
    manager = HRVProfileManager(temp_dir)
    profiles = manager.list_profiles("tenant")
    assert isinstance(profiles, list)
```

### 5. API Tests (`test_api_hr_server.py`)

Tests API endpoint functionality.

```python
def test_hr_generate():
    """Test generation endpoint"""
    req = SimpleRequest(prompt="Test prompt")
    resp = hr_generate(req)
    assert hasattr(resp, 'article')
    assert hasattr(resp, 'hrv_feedback')

def test_api_with_profile():
    """Test API with profile"""
    req = SimpleRequest(prompt="Test", profile_name="professional")
    resp = hr_generate(req)
    assert resp.article is not None
```

### 6. CLI Tests (`test_cli_hr_main.py`)

Tests command-line interface functionality.

```python
def test_cli_basic():
    """Test basic CLI execution"""
    # Test CLI with basic arguments
    pass

def test_cli_with_profile():
    """Test CLI with profile argument"""
    # Test CLI with profile
    pass
```

### 7. Integration Tests (`test_integration.py`)

Tests end-to-end system integration.

```python
def test_end_to_end_generation():
    """Test complete generation workflow"""
    extractor = HRVExtractor()
    writer = HumanResonantWriter()
    
    content = writer.generate("Test prompt")
    hrv = extractor.extract(content)
    
    assert len(hrv) == 8
    assert len(content) > 0

def test_profile_based_generation():
    """Test generation with profiles"""
    # Test complete profile-based workflow
    pass
```

### 8. Edge Case Tests (`test_edge_cases.py`)

Tests boundary conditions and error scenarios.

```python
def test_very_long_text():
    """Test extraction from very long text"""
    extractor = HRVExtractor()
    long_text = "word " * 10000
    hrv = extractor.extract(long_text)
    assert len(hrv) == 8

def test_special_characters():
    """Test handling of special characters"""
    extractor = HRVExtractor()
    text = "Text with @#$%^&*() special chars!"
    hrv = extractor.extract(text)
    assert len(hrv) == 8

def test_unicode_text():
    """Test handling of unicode text"""
    extractor = HRVExtractor()
    text = "Text with émojis 🎉 and unicode"
    hrv = extractor.extract(text)
    assert len(hrv) == 8
```

### 9. Performance Tests (`test_performance.py`)

Tests system performance characteristics.

```python
def test_generation_speed():
    """Test generation speed"""
    writer = HumanResonantWriter()
    start = time.time()
    content = writer.generate("Test prompt")
    duration = time.time() - start
    assert duration < 5.0  # Should complete in under 5 seconds

def test_extraction_speed():
    """Test extraction speed"""
    extractor = HRVExtractor()
    text = "Test sentence for performance."
    start = time.time()
    hrv = extractor.extract(text)
    duration = time.time() - start
    assert duration < 0.1  # Should complete in under 100ms

def test_memory_usage():
    """Test memory efficiency"""
    # Test memory usage for operations
    pass
```

## Usage Patterns

### Running All Tests

```bash
# Run all tests
python -m resonance_os.tests.run_all_tests

# Run with pytest
pytest resonance_os/tests/

# Run with coverage
pytest --cov=resonance_os --cov-report=html resonance_os/tests/
```

### Running Specific Tests

```bash
# Run core tests
pytest resonance_os/tests/test_core_*.py

# Run generation tests
pytest resonance_os/tests/test_generation_*.py

# Run specific test file
pytest resonance_os/tests/test_profiles_hrv_extractor.py

# Run specific test function
pytest resonance_os/tests/test_core_hrv_constants.py::test_hrv_dimensions
```

### Running Tests with Options

```bash
# Verbose output
pytest -v resonance_os/tests/

# Stop on first failure
pytest -x resonance_os/tests/

# Show local variables on failure
pytest -l resonance_os/tests/

# Run failed tests only
pytest --lf resonance_os/tests/
```

## Best Practices

1. **Write tests first**: Follow TDD principles when possible
2. **Test boundaries**: Test edge cases and boundary conditions
3. **Keep tests isolated**: Each test should be independent
4. **Use descriptive names**: Test names should describe what they test
5. **Mock external dependencies**: Mock external services and APIs
6. **Test error cases**: Test both success and failure scenarios
7. **Maintain test speed**: Keep tests fast for frequent execution
8. **Update tests with code**: Keep tests synchronized with code changes

## Common Issues

**Issue**: Tests fail due to missing dependencies
**Solution**: Install all required dependencies including test dependencies

**Issue**: Tests fail in CI but pass locally
**Solution**: Check environment differences and dependency versions

**Issue**: Flaky tests (intermittent failures)
**Solution**: Add retry logic or fix race conditions

**Issue**: Tests too slow
**Solution**: Use mocking, parallel execution, or optimize test data

## Test Coverage

### Current Coverage Areas

- **Core Systems**: ~90% coverage
- **Generation Systems**: ~85% coverage
- **Profile Systems**: ~90% coverage
- **API Systems**: ~80% coverage
- **CLI Systems**: ~75% coverage
- **Integration**: ~70% coverage

### Target Coverage

- **Critical paths**: 100% coverage
- **Core functionality**: 95%+ coverage
- **Edge cases**: 80%+ coverage
- **Error handling**: 90%+ coverage

## Integration Points

The Tests Systems module integrates with:

- **All Systems**: Tests all system components
- **CI/CD**: Integrates with continuous integration pipelines
- **Code Quality**: Supports code quality tools (coverage, linting)
- **Documentation**: Generates test documentation

## Future Enhancements

- **Property-based testing**: Add property-based testing with Hypothesis
- **Mutation testing**: Add mutation testing with mutmut
- **Load testing**: Add load testing for API endpoints
- **Visual testing**: Add visual regression testing for UI
- **Contract testing**: Add contract testing for API contracts
- **Chaos testing**: Add chaos engineering tests

## Dependencies

```bash
# Test dependencies
pip install pytest pytest-cov pytest-mock pytest-asyncio
pip install hypothesis  # Property-based testing
pip install mutmut  # Mutation testing
```

## References

- [Core Systems Guide](./core-systems-guide.md)
- [Generation Systems Guide](./generation-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
- [API Systems Guide](./api-systems-guide.md)
