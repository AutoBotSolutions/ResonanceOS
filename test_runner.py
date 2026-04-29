#!/usr/bin/env python3
"""
Enhanced Test Runner for ResonanceOS v6
Complete system testing with comprehensive coverage
"""

import sys
import os
import time
import json
import unittest
from pathlib import Path
from typing import Dict, Any, List

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from examples.testing_examples.unit_tests import run_test_suite

def test_hrf_model():
    """Test HRF model functionality"""
    from resonance_os.generation.hrf_model import HRFModel
    
    hrf = HRFModel()
    score = hrf.predict("Test sentence for HRF model")
    assert 0 <= score <= 1, f"HRF score {score} not in range [0,1]"
    print("✓ HRF Model test passed")

def test_hrv_extractor():
    """Test HRV extractor functionality"""
    from resonance_os.profiles.hrv_extractor import HRVExtractor
    
    extractor = HRVExtractor()
    vec = extractor.extract("This is a test sentence. It should vary in length!")
    assert len(vec) == 8, f"HRV vector length {len(vec)} != 8"
    assert all(isinstance(x, (int, float)) for x in vec), "HRV vector contains non-numeric values"
    print("✓ HRV Extractor test passed")

def test_human_resonant_writer():
    """Test Human Resonant Writer functionality"""
    from resonance_os.generation.human_resonant_writer import HumanResonantWriter
    
    writer = HumanResonantWriter()
    result = writer.generate("The benefits of AI technology")
    assert isinstance(result, str), "Writer should return string"
    assert len(result) > 0, "Writer should not return empty string"
    print("✓ Human Resonant Writer test passed")

def test_profile_manager():
    """Test HRV Profile Manager functionality"""
    from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
    from pathlib import Path
    import tempfile
    import shutil
    
    # Create temporary directory for testing
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        manager = HRVProfileManager(temp_dir)
        
        # Test saving and loading profiles
        test_vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        manager.save_profile("test_tenant", "test_profile", test_vector)
        
        loaded_vector = manager.load_profile("test_tenant", "test_profile")
        assert loaded_vector == test_vector, "Profile save/load mismatch"
        
        # Test listing profiles
        profiles = manager.list_profiles("test_tenant")
        assert "test_profile" in profiles, "Profile not found in list"
        
        print("✓ HRV Profile Manager test passed")
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

def test_cli_functionality():
    """Test CLI functionality"""
    from resonance_os.api.hr_server import SimpleRequest, hr_generate
    
    req = SimpleRequest(prompt="Test CLI functionality")
    resp = hr_generate(req)
    
    assert hasattr(resp, 'article'), "Response missing article attribute"
    assert hasattr(resp, 'hrv_feedback'), "Response missing hrv_feedback attribute"
    assert isinstance(resp.article, str), "Article should be string"
    assert isinstance(resp.hrv_feedback, list), "HRV feedback should be list"
    assert len(resp.hrv_feedback) == 8, "HRV feedback should have 8 dimensions"
    
    print("✓ CLI functionality test passed")

def run_integration_tests():
    """Run integration tests"""
    print("🔗 Running Integration Tests...")
    print("-" * 40)
    
    try:
        # Test API integration
        from resonance_os.api.hr_server import SimpleRequest, hr_generate
        
        req = SimpleRequest(prompt="Integration test prompt")
        resp = hr_generate(req)
        
        assert hasattr(resp, 'article'), "Response missing article attribute"
        assert hasattr(resp, 'hrv_feedback'), "Response missing hrv_feedback attribute"
        assert isinstance(resp.article, str), "Article should be string"
        assert isinstance(resp.hrv_feedback, list), "HRV feedback should be list"
        assert len(resp.hrv_feedback) == 8, "HRV feedback should have 8 dimensions"
        
        print("✓ API Integration test passed")
        
        # Test multi-component workflow
        from resonance_os.generation.human_resonant_writer import HumanResonantWriter
        from resonance_os.profiles.hrv_extractor import HRVExtractor
        
        writer = HumanResonantWriter()
        extractor = HRVExtractor()
        
        # Generate content
        content = writer.generate("Integration test content generation")
        assert isinstance(content, str), "Generated content should be string"
        assert len(content) > 0, "Generated content should not be empty"
        
        # Extract HRV
        hrv_vector = extractor.extract(content)
        assert len(hrv_vector) == 8, "HRV vector should have 8 dimensions"
        assert all(isinstance(x, (int, float)) for x in hrv_vector), "HRV vector should contain numeric values"
        
        print("✓ Multi-component workflow test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_performance_tests():
    """Run performance tests"""
    print("⚡ Running Performance Tests...")
    print("-" * 40)
    
    try:
        from resonance_os.generation.human_resonant_writer import HumanResonantWriter
        from resonance_os.profiles.hrv_extractor import HRVExtractor
        from resonance_os.generation.hrf_model import HRFModel
        
        writer = HumanResonantWriter()
        extractor = HRVExtractor()
        hrf_model = HRFModel()
        
        # Test generation performance
        prompts = ["Test prompt 1", "Test prompt 2", "Test prompt 3"]
        generation_times = []
        
        for prompt in prompts:
            start_time = time.time()
            content = writer.generate(prompt)
            end_time = time.time()
            generation_times.append(end_time - start_time)
        
        avg_generation_time = sum(generation_times) / len(generation_times)
        assert avg_generation_time < 5.0, f"Generation too slow: {avg_generation_time:.3f}s average"
        
        print(f"✓ Generation performance: {avg_generation_time:.3f}s average")
        
        # Test extraction performance
        test_text = "Performance test text with multiple sentences."
        extraction_times = []
        
        for _ in range(10):
            start_time = time.time()
            hrv_vector = extractor.extract(test_text)
            end_time = time.time()
            extraction_times.append(end_time - start_time)
        
        avg_extraction_time = sum(extraction_times) / len(extraction_times)
        assert avg_extraction_time < 0.1, f"Extraction too slow: {avg_extraction_time:.3f}s average"
        
        print(f"✓ Extraction performance: {avg_extraction_time:.3f}s average")
        
        # Test HRF model performance
        hrf_times = []
        
        for _ in range(10):
            start_time = time.time()
            score = hrf_model.predict(test_text)
            end_time = time.time()
            hrf_times.append(end_time - start_time)
        
        avg_hrf_time = sum(hrf_times) / len(hrf_times)
        assert avg_hrf_time < 0.1, f"HRF model too slow: {avg_hrf_time:.3f}s average"
        
        print(f"✓ HRF model performance: {avg_hrf_time:.3f}s average")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests with comprehensive reporting"""
    print("🧪 Running ResonanceOS v6 Complete Test Suite")
    print("=" * 60)
    
    test_results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tests": {},
        "summary": {}
    }
    
    all_passed = True
    
    # Run basic component tests
    print("\n📊 Basic Component Tests")
    print("-" * 40)
    
    basic_tests = [
        ("HRF Model", test_hrf_model),
        ("HRV Extractor", test_hrv_extractor),
        ("Human Resonant Writer", test_human_resonant_writer),
        ("Profile Manager", test_profile_manager),
        ("CLI Functionality", test_cli_functionality)
    ]
    
    for test_name, test_func in basic_tests:
        try:
            test_func()
            test_results["tests"][test_name] = {"status": "passed", "error": None}
        except Exception as e:
            test_results["tests"][test_name] = {"status": "failed", "error": str(e)}
            all_passed = False
    
    # Run integration tests
    print("\n🔗 Integration Tests")
    print("-" * 40)
    
    try:
        integration_passed = run_integration_tests()
        test_results["tests"]["Integration"] = {"status": "passed" if integration_passed else "failed", "error": None}
        if not integration_passed:
            all_passed = False
    except Exception as e:
        test_results["tests"]["Integration"] = {"status": "failed", "error": str(e)}
        all_passed = False
    
    # Run performance tests
    print("\n⚡ Performance Tests")
    print("-" * 40)
    
    try:
        performance_passed = run_performance_tests()
        test_results["tests"]["Performance"] = {"status": "passed" if performance_passed else "failed", "error": None}
        if not performance_passed:
            all_passed = False
    except Exception as e:
        test_results["tests"]["Performance"] = {"status": "failed", "error": str(e)}
        all_passed = False
    
    # Run comprehensive unit tests
    print("\n🔬 Comprehensive Unit Tests")
    print("-" * 40)
    
    try:
        unit_test_result = run_test_suite()
        test_results["tests"]["Unit_Tests"] = {
            "status": "passed" if unit_test_result.wasSuccessful() else "failed",
            "total": unit_test_result.testsRun,
            "failures": len(unit_test_result.failures),
            "errors": len(unit_test_result.errors),
            "error": None
        }
        
        if not unit_test_result.wasSuccessful():
            all_passed = False
            test_results["tests"]["Unit_Tests"]["error"] = f"{len(unit_test_result.failures)} failures, {len(unit_test_result.errors)} errors"
        
    except Exception as e:
        test_results["tests"]["Unit_Tests"] = {"status": "failed", "error": str(e)}
        all_passed = False
    
    # Calculate summary
    total_tests = len(test_results["tests"])
    passed_tests = sum(1 for test in test_results["tests"].values() if test["status"] == "passed")
    failed_tests = total_tests - passed_tests
    
    test_results["summary"] = {
        "total_tests": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
        "overall_status": "passed" if all_passed else "failed"
    }
    
    # Save test results
    results_dir = Path("resonance_os/data/exports/reports")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = results_dir / f"test_results_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2, default=str)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {test_results['summary']['success_rate']:.1f}%")
    
    if failed_tests > 0:
        print("\n❌ Failed Tests:")
        for test_name, result in test_results["tests"].items():
            if result["status"] == "failed":
                print(f"   • {test_name}: {result.get('error', 'Unknown error')}")
    
    print(f"\n💾 Results saved to: {results_file}")
    
    if all_passed:
        print("\n🎉 All tests passed! ResonanceOS v6 is working correctly.")
        print("✅ System is ready for production use!")
    else:
        print("\n⚠️ Some tests failed. Please review the errors above.")
        print("❌ System may need attention before production use.")
    
    return all_passed

def main():
    """Main test runner interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ResonanceOS v6 Test Runner")
    parser.add_argument("--basic", action="store_true", help="Run basic component tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--unit", action="store_true", help="Run comprehensive unit tests only")
    parser.add_argument("--report", action="store_true", help="Generate test report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        # Set verbose logging
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    try:
        if args.basic:
            # Run only basic tests
            print("🧪 Running Basic Component Tests Only")
            print("=" * 50)
            
            basic_tests = [
                test_hrf_model,
                test_hrv_extractor,
                test_human_resonant_writer,
                test_profile_manager,
                test_cli_functionality
            ]
            
            for test_func in basic_tests:
                test_func()
                
            print("\n🎉 Basic tests passed!")
            
        elif args.integration:
            run_integration_tests()
        elif args.performance:
            run_performance_tests()
        elif args.unit:
            run_test_suite()
        else:
            # Run all tests
            success = run_all_tests()
            sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Test runner interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test runner error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
