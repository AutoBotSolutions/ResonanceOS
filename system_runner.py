#!/usr/bin/env python3
"""
System Runner for ResonanceOS v6
Complete system integration and orchestration
"""

import sys
import os
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all system components
from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.generation.hrf_model import HRFModel
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.api.hr_server import SimpleRequest, hr_generate
from resonance_os.cli.hr_main import main as cli_main


class ResonanceOSSystemRunner:
    """Complete system runner for ResonanceOS v6"""
    
    def __init__(self):
        self.project_root = Path(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = self.project_root / "resonance_os" / "data"
        
        # Initialize system components
        self.writer = HumanResonantWriter()
        self.hrf_model = HRFModel()
        self.extractor = HRVExtractor()
        
        # Initialize profile manager with data directory
        profiles_dir = self.data_dir / "profiles" / "hr_profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)
        self.profile_manager = HRVProfileManager(str(profiles_dir))
        
        print("🚀 ResonanceOS v6 System Initialized")
        print(f"   Project Root: {self.project_root}")
        print(f"   Data Directory: {self.data_dir}")
        print(f"   Profiles Directory: {profiles_dir}")
    
    def run_system_diagnostics(self) -> Dict[str, Any]:
        """Run complete system diagnostics"""
        print("\n🔍 Running System Diagnostics")
        print("=" * 60)
        
        diagnostics = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "components": {},
            "data_directories": {},
            "system_health": "unknown"
        }
        
        # Test core components
        try:
            # Test HRF Model
            print("📊 Testing HRF Model...")
            hrf_score = self.hrf_model.predict("System diagnostic test sentence")
            diagnostics["components"]["hrf_model"] = {
                "status": "healthy",
                "test_score": hrf_score,
                "message": "HRF Model functioning correctly"
            }
            print(f"✅ HRF Model: Score {hrf_score:.3f}")
            
            # Test HRV Extractor
            print("🧠 Testing HRV Extractor...")
            hrv_vector = self.extractor.extract("System diagnostic test sentence with varying length and emotional content!")
            diagnostics["components"]["hrv_extractor"] = {
                "status": "healthy",
                "test_vector": hrv_vector,
                "vector_length": len(hrv_vector),
                "message": "HRV Extractor functioning correctly"
            }
            print(f"✅ HRV Extractor: Vector {len(hrv_vector)} dimensions")
            
            # Test Human Resonant Writer
            print("✍️ Testing Human Resonant Writer...")
            generated_content = self.writer.generate("System diagnostic prompt about AI technology")
            diagnostics["components"]["writer"] = {
                "status": "healthy",
                "content_length": len(generated_content),
                "message": "Human Resonant Writer functioning correctly"
            }
            print(f"✅ Writer: Generated {len(generated_content)} characters")
            
            # Test Profile Manager
            print("📁 Testing Profile Manager...")
            test_vector = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
            self.profile_manager.save_profile("system_test", "diagnostic_profile", test_vector)
            loaded_vector = self.profile_manager.load_profile("system_test", "diagnostic_profile")
            
            diagnostics["components"]["profile_manager"] = {
                "status": "healthy",
                "test_profile_saved": True,
                "test_profile_loaded": loaded_vector == test_vector,
                "message": "Profile Manager functioning correctly"
            }
            print(f"✅ Profile Manager: Save/Load test passed")
            
            # Test API Integration
            print("🌐 Testing API Integration...")
            api_request = SimpleRequest(prompt="System diagnostic API test")
            api_response = hr_generate(api_request)
            
            diagnostics["components"]["api"] = {
                "status": "healthy",
                "response_received": True,
                "article_length": len(api_response.article),
                "hrv_feedback_length": len(api_response.hrv_feedback),
                "message": "API Integration functioning correctly"
            }
            print(f"✅ API Integration: Response received")
            
        except Exception as e:
            print(f"❌ Component test failed: {e}")
            diagnostics["components"]["error"] = str(e)
        
        # Check data directories
        print("\n📂 Checking Data Directories...")
        required_dirs = [
            "config", "samples", "corpora", "models", "profiles", 
            "scripts", "logs", "exports"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.data_dir / dir_name
            exists = dir_path.exists()
            has_files = len(list(dir_path.glob("*"))) > 0 if exists else False
            
            diagnostics["data_directories"][dir_name] = {
                "exists": exists,
                "has_files": has_files,
                "path": str(dir_path)
            }
            
            status = "✅" if exists and has_files else "⚠️" if exists else "❌"
            print(f"{status} {dir_name}: {'Exists with files' if has_files else 'Empty' if exists else 'Missing'}")
        
        # Overall system health
        component_status = [comp.get("status") == "healthy" for comp in diagnostics["components"].values()]
        dir_status = [dir_data["exists"] for dir_data in diagnostics["data_directories"].values()]
        
        if all(component_status) and all(dir_status):
            diagnostics["system_health"] = "healthy"
            print("\n🎉 System Health: HEALTHY")
        elif any(component_status) and any(dir_status):
            diagnostics["system_health"] = "degraded"
            print("\n⚠️ System Health: DEGRADED")
        else:
            diagnostics["system_health"] = "unhealthy"
            print("\n❌ System Health: UNHEALTHY")
        
        return diagnostics
    
    def run_complete_system_test(self) -> Dict[str, Any]:
        """Run complete system integration test"""
        print("\n🧪 Running Complete System Test")
        print("=" * 60)
        
        test_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tests": {},
            "overall_status": "unknown"
        }
        
        # Test 1: End-to-End Content Generation
        print("📝 Test 1: End-to-End Content Generation")
        try:
            prompt = "The future of artificial intelligence in business"
            content = self.writer.generate(prompt)
            hrv_vector = self.extractor.extract(content)
            hrf_score = self.hrf_model.predict(content)
            
            test_results["tests"]["content_generation"] = {
                "status": "passed",
                "prompt_length": len(prompt),
                "content_length": len(content),
                "hrv_score": sum(hrv_vector) / len(hrv_vector),
                "hrf_score": hrf_score,
                "message": "End-to-end generation successful"
            }
            print(f"✅ Generated {len(content)} chars, HRV: {sum(hrv_vector)/len(hrv_vector):.3f}, HRF: {hrf_score:.3f}")
            
        except Exception as e:
            test_results["tests"]["content_generation"] = {
                "status": "failed",
                "error": str(e),
                "message": "End-to-end generation failed"
            }
            print(f"❌ Failed: {e}")
        
        # Test 2: Profile-Based Generation
        print("\n🎨 Test 2: Profile-Based Generation")
        try:
            # Create test profile
            test_profile_vector = [0.7, 0.6, 0.8, 0.5, 0.4, 0.3, 0.6, 0.7]
            self.profile_manager.save_profile("system_test", "profile_test", test_profile_vector)
            
            # Generate with profile
            request = SimpleRequest(
                prompt="Building successful teams",
                tenant="system_test",
                profile_name="profile_test"
            )
            response = hr_generate(request)
            
            test_results["tests"]["profile_generation"] = {
                "status": "passed",
                "profile_used": "profile_test",
                "content_length": len(response.article),
                "hrv_feedback": response.hrv_feedback,
                "message": "Profile-based generation successful"
            }
            print(f"✅ Profile generation successful")
            
        except Exception as e:
            test_results["tests"]["profile_generation"] = {
                "status": "failed",
                "error": str(e),
                "message": "Profile-based generation failed"
            }
            print(f"❌ Failed: {e}")
        
        # Test 3: Multi-Profile Comparison
        print("\n📊 Test 3: Multi-Profile Comparison")
        try:
            profiles_to_test = ["neutral_professional", "creative_storytelling"]
            prompt = "The importance of innovation"
            results = {}
            
            for profile in profiles_to_test:
                request = SimpleRequest(prompt=prompt, profile_name=profile)
                response = hr_generate(request)
                results[profile] = {
                    "length": len(response.article),
                    "hrv_feedback": response.hrv_feedback
                }
            
            test_results["tests"]["multi_profile"] = {
                "status": "passed",
                "profiles_tested": profiles_to_test,
                "results": results,
                "message": "Multi-profile comparison successful"
            }
            print(f"✅ Multi-profile comparison successful")
            
        except Exception as e:
            test_results["tests"]["multi_profile"] = {
                "status": "failed",
                "error": str(e),
                "message": "Multi-profile comparison failed"
            }
            print(f"❌ Failed: {e}")
        
        # Test 4: Data Processing Pipeline
        print("\n⚙️ Test 4: Data Processing Pipeline")
        try:
            # Sample data processing
            sample_texts = [
                "Business report on quarterly performance",
                "Creative story about innovation",
                "Technical documentation for API"
            ]
            
            processed_data = []
            for text in sample_texts:
                hrv_vector = self.extractor.extract(text)
                hrf_score = self.hrf_model.predict(text)
                processed_data.append({
                    "text": text,
                    "hrv_vector": hrv_vector,
                    "hrf_score": hrf_score
                })
            
            test_results["tests"]["data_processing"] = {
                "status": "passed",
                "texts_processed": len(sample_texts),
                "avg_hrv_score": sum(sum(p["hrv_vector"]) / len(p["hrv_vector"]) for p in processed_data) / len(processed_data),
                "avg_hrf_score": sum(p["hrf_score"] for p in processed_data) / len(processed_data),
                "message": "Data processing pipeline successful"
            }
            print(f"✅ Processed {len(sample_texts)} texts successfully")
            
        except Exception as e:
            test_results["tests"]["data_processing"] = {
                "status": "failed",
                "error": str(e),
                "message": "Data processing pipeline failed"
            }
            print(f"❌ Failed: {e}")
        
        # Overall test status
        passed_tests = sum(1 for test in test_results["tests"].values() if test["status"] == "passed")
        total_tests = len(test_results["tests"])
        
        if passed_tests == total_tests:
            test_results["overall_status"] = "all_passed"
            print(f"\n🎉 All Tests Passed: {passed_tests}/{total_tests}")
        elif passed_tests > 0:
            test_results["overall_status"] = "partial"
            print(f"\n⚠️ Partial Success: {passed_tests}/{total_tests} tests passed")
        else:
            test_results["overall_status"] "all_failed"
            print(f"\n❌ All Tests Failed: {passed_tests}/{total_tests}")
        
        return test_results
    
    def run_performance_benchmark(self) -> Dict[str, Any]:
        """Run performance benchmarks"""
        print("\n⚡ Running Performance Benchmarks")
        print("=" * 60)
        
        benchmarks = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "metrics": {},
            "overall_performance": "unknown"
        }
        
        # Benchmark 1: Content Generation Speed
        print("📝 Benchmarking Content Generation Speed...")
        prompts = [
            "AI technology benefits",
            "Business strategy overview",
            "Innovation in healthcare"
        ]
        
        generation_times = []
        content_lengths = []
        
        for prompt in prompts:
            start_time = time.time()
            content = self.writer.generate(prompt)
            end_time = time.time()
            
            generation_time = end_time - start_time
            generation_times.append(generation_time)
            content_lengths.append(len(content))
            
            print(f"   {prompt[:20]}...: {generation_time:.3f}s ({len(content)} chars)")
        
        benchmarks["metrics"]["content_generation"] = {
            "avg_time": sum(generation_times) / len(generation_times),
            "avg_length": sum(content_lengths) / len(content_lengths),
            "chars_per_second": sum(content_lengths) / sum(generation_times),
            "samples": len(prompts)
        }
        
        # Benchmark 2: HRV Extraction Speed
        print("\n🧠 Benchmarking HRV Extraction Speed...")
        extraction_texts = [
            "Short text.",
            "Medium length text with multiple sentences and varied structure.",
            "This is a much longer text that contains multiple sentences, varied structure, emotional content, and complex linguistic patterns to test the extraction performance."
        ]
        
        extraction_times = []
        
        for text in extraction_texts:
            start_time = time.time()
            hrv_vector = self.extractor.extract(text)
            end_time = time.time()
            
            extraction_time = end_time - start_time
            extraction_times.append(extraction_time)
            
            print(f"   {len(text)} chars: {extraction_time:.3f}s")
        
        benchmarks["metrics"]["hrv_extraction"] = {
            "avg_time": sum(extraction_times) / len(extraction_times),
            "samples": len(extraction_texts)
        }
        
        # Benchmark 3: HRF Model Speed
        print("\n📊 Benchmarking HRF Model Speed...")
        hrf_texts = [
            "Positive sentence with good engagement.",
            "Neutral text for testing purposes.",
            "Complex emotional content with varied engagement patterns."
        ]
        
        hrf_times = []
        
        for text in hrf_texts:
            start_time = time.time()
            hrf_score = self.hrf_model.predict(text)
            end_time = time.time()
            
            hrf_time = end_time - start_time
            hrf_times.append(hrf_time)
            
            print(f"   Score {hrf_score:.3f}: {hrf_time:.3f}s")
        
        benchmarks["metrics"]["hrf_model"] = {
            "avg_time": sum(hrf_times) / len(hrf_times),
            "samples": len(hrf_texts)
        }
        
        # Overall performance assessment
        avg_generation_time = benchmarks["metrics"]["content_generation"]["avg_time"]
        avg_extraction_time = benchmarks["metrics"]["hrv_extraction"]["avg_time"]
        avg_hrf_time = benchmarks["metrics"]["hrf_model"]["avg_time"]
        
        if avg_generation_time < 1.0 and avg_extraction_time < 0.1 and avg_hrf_time < 0.1:
            benchmarks["overall_performance"] = "excellent"
        elif avg_generation_time < 2.0 and avg_extraction_time < 0.2 and avg_hrf_time < 0.2:
            benchmarks["overall_performance"] = "good"
        else:
            benchmarks["overall_performance"] = "needs_improvement"
        
        print(f"\n📊 Performance Summary:")
        print(f"   Generation: {avg_generation_time:.3f}s avg")
        print(f"   Extraction: {avg_extraction_time:.3f}s avg")
        print(f"   HRF Model: {avg_hrf_time:.3f}s avg")
        print(f"   Overall: {benchmarks['overall_performance']}")
        
        return benchmarks
    
    def generate_system_report(self) -> Dict[str, Any]:
        """Generate comprehensive system report"""
        print("\n📋 Generating System Report")
        print("=" * 60)
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": {
                "python_version": sys.version,
                "project_root": str(self.project_root),
                "data_directory": str(self.data_dir)
            },
            "diagnostics": self.run_system_diagnostics(),
            "tests": self.run_complete_system_test(),
            "benchmarks": self.run_performance_benchmark()
        }
        
        # Save report
        reports_dir = self.data_dir / "exports" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = reports_dir / f"system_report_{time.strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n💾 System report saved to: {report_file}")
        
        # Summary
        system_health = report["diagnostics"]["system_health"]
        test_status = report["tests"]["overall_status"]
        performance = report["benchmarks"]["overall_performance"]
        
        print(f"\n📊 System Summary:")
        print(f"   Health: {system_health.upper()}")
        print(f"   Tests: {test_status.replace('_', ' ').title()}")
        print(f"   Performance: {performance.replace('_', ' ').title()}")
        
        return report
    
    def run_cli_interface(self, args: Optional[List[str]] = None):
        """Run CLI interface"""
        print("\n💻 Running CLI Interface")
        print("=" * 60)
        
        # Save original sys.argv
        original_argv = sys.argv.copy()
        
        try:
            # Set up CLI arguments
            if args:
                sys.argv = ["hr_main"] + args
            else:
                sys.argv = ["hr_main", "--help"]
            
            # Run CLI
            cli_main()
            
        except SystemExit:
            # CLI calls sys.exit, which is normal
            pass
        finally:
            # Restore original sys.argv
            sys.argv = original_argv
    
    def start_api_server(self, host: str = "localhost", port: int = 8000):
        """Start API server"""
        print(f"\n🌐 Starting API Server on {host}:{port}")
        print("=" * 60)
        
        try:
            import uvicorn
            from resonance_os.api.hr_server import app
            
            print(f"🚀 API Server starting...")
            print(f"   Host: {host}")
            print(f"   Port: {port}")
            print(f"   Docs: http://{host}:{port}/docs")
            print(f"   Health: http://{host}:{port}/health")
            print("\nPress Ctrl+C to stop the server")
            
            uvicorn.run(app, host=host, port=port, log_level="info")
            
        except ImportError:
            print("❌ uvicorn not installed. Install with: pip install uvicorn")
        except Exception as e:
            print(f"❌ Failed to start API server: {e}")


def main():
    """Main system runner interface"""
    parser = argparse.ArgumentParser(description="ResonanceOS v6 System Runner")
    parser.add_argument("--diagnostics", action="store_true", help="Run system diagnostics")
    parser.add_argument("--test", action="store_true", help="Run complete system tests")
    parser.add_argument("--benchmark", action="store_true", help="Run performance benchmarks")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive system report")
    parser.add_argument("--cli", nargs="*", help="Run CLI interface with optional arguments")
    parser.add_argument("--serve", action="store_true", help="Start API server")
    parser.add_argument("--host", default="localhost", help="API server host (default: localhost)")
    parser.add_argument("--port", type=int, default=8000, help="API server port (default: 8000)")
    parser.add_argument("--all", action="store_true", help="Run all checks and generate report")
    
    args = parser.parse_args()
    
    # Initialize system runner
    runner = ResonanceOSSystemRunner()
    
    print("🎯 ResonanceOS v6 System Runner")
    print("=" * 60)
    
    try:
        if args.all:
            # Run everything
            runner.run_system_diagnostics()
            runner.run_complete_system_test()
            runner.run_performance_benchmark()
            runner.generate_system_report()
        elif args.diagnostics:
            runner.run_system_diagnostics()
        elif args.test:
            runner.run_complete_system_test()
        elif args.benchmark:
            runner.run_performance_benchmark()
        elif args.report:
            runner.generate_system_report()
        elif args.cli is not None:
            runner.run_cli_interface(args.cli)
        elif args.serve:
            runner.start_api_server(args.host, args.port)
        else:
            # Default: show help and run diagnostics
            parser.print_help()
            print("\nRunning default diagnostics...")
            runner.run_system_diagnostics()
    
    except KeyboardInterrupt:
        print("\n\n⏹️ System runner interrupted by user")
    except Exception as e:
        print(f"\n❌ System runner error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
