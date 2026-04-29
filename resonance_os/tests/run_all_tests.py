#!/usr/bin/env python3
"""
Comprehensive Test Runner for ResonanceOS v6
"""

import unittest
import sys
import os
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def discover_and_run_tests():
    """Discover and run all tests in the test directory"""
    
    print("🚀 ResonanceOS v6 Comprehensive Test Suite")
    print("=" * 60)
    
    # Discover all test modules
    test_dir = Path(__file__).parent
    loader = unittest.TestLoader()
    
    # Discover all test files
    test_suite = loader.discover(str(test_dir), pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=True,
        failfast=False
    )
    
    print(f"📁 Test Directory: {test_dir}")
    print(f"🔍 Discovering tests...")
    
    # Count tests before running
    test_count = test_suite.countTestCases()
    print(f"📊 Found {test_count} test cases")
    print()
    
    # Run the tests
    start_time = time.time()
    result = runner.run(test_suite)
    end_time = time.time()
    
    # Print summary
    print()
    print("=" * 60)
    print("📈 Test Results Summary")
    print("=" * 60)
    print(f"⏱️  Total Time: {end_time - start_time:.2f} seconds")
    print(f"📊 Tests Run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"🚫 Errors: {len(result.errors)}")
    print(f"⏭️  Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print()
        print("❌ Test Failures:")
        print("-" * 30)
        for test, traceback in result.failures:
            print(f"❌ {test}")
            # Print only the first line of traceback for brevity
            first_line = traceback.split('\n')[0]
            print(f"   {first_line}")
    
    if result.errors:
        print()
        print("🚫 Test Errors:")
        print("-" * 30)
        for test, traceback in result.errors:
            print(f"🚫 {test}")
            # Print only the first line of traceback for brevity
            first_line = traceback.split('\n')[0]
            print(f"   {first_line}")
    
    print()
    if result.wasSuccessful():
        print("🎉 All tests passed! ResonanceOS v6 is fully functional.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the failures above.")
        return False

def run_specific_test_module(module_name):
    """Run a specific test module"""
    try:
        print(f"🎯 Running specific test module: {module_name}")
        print("=" * 60)
        
        # Import and run the specific test
        module = __import__(f"resonance_os.tests.{module_name}", fromlist=[module_name])
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"❌ Could not import test module {module_name}: {e}")
        return False

def run_category_tests():
    """Run tests by category"""
    categories = {
        "Core": ["test_core_hrv_constants", "test_core_hrv_types"],
        "Profiles": ["test_profiles_hrv_extractor", "test_profiles_multi_tenant_hr_profiles"],
        "Generation": ["test_generation_hrf_model", "test_generation_planner_layer", 
                      "test_generation_sentence_layer", "test_generation_refiner_layer",
                      "test_generation_human_resonant_writer"],
        "API": ["test_api_hr_server"],
        "CLI": ["test_cli_hr_main"],
        "Integration": ["test_integration"],
        "Edge Cases": ["test_edge_cases"],
        "Performance": ["test_performance"]
    }
    
    print("📂 Test Categories Available:")
    print("=" * 40)
    for i, category in enumerate(categories.keys(), 1):
        test_count = len(categories[category])
        print(f"{i}. {category} ({test_count} test files)")
    
    print()
    choice = input("Select category number (or press Enter for all tests): ").strip()
    
    if choice and choice.isdigit() and 1 <= int(choice) <= len(categories):
        category_name = list(categories.keys())[int(choice) - 1]
        test_modules = categories[category_name]
        
        print(f"\n🎯 Running {category_name} tests...")
        print("=" * 60)
        
        # Run all modules in the category
        all_passed = True
        for module_name in test_modules:
            passed = run_specific_test_module(module_name)
            if not passed:
                all_passed = False
            print()
        
        return all_passed
    else:
        return discover_and_run_tests()

def main():
    """Main test runner"""
    print("ResonanceOS v6 Test Runner")
    print("=" * 30)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--category":
            success = run_category_tests()
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python run_all_tests.py              - Run all tests")
            print("  python run_all_tests.py --category   - Run tests by category")
            print("  python run_all_tests.py <module>     - Run specific test module")
            print()
            print("Available modules:")
            test_dir = Path(__file__).parent
            for test_file in sorted(test_dir.glob("test_*.py")):
                if test_file.name != "run_all_tests.py":
                    print(f"  {test_file.stem}")
            return
        else:
            # Run specific module
            module_name = sys.argv[1]
            if module_name.startswith("test_"):
                module_name = module_name[5:]  # Remove "test_" prefix
            success = run_specific_test_module(module_name)
    else:
        success = discover_and_run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
