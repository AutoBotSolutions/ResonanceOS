#!/usr/bin/env python3
"""
Setup Script for ResonanceOS v6
Complete system initialization and configuration
"""

import sys
import os
import json
import time
import shutil
from pathlib import Path
from typing import Dict, Any, List

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class ResonanceOSSetup:
    """Complete setup and initialization for ResonanceOS v6"""
    
    def __init__(self):
        self.project_root = Path(os.path.dirname(os.path.abspath(__file__)))
        self.resonance_os_dir = self.project_root / "resonance_os"
        self.data_dir = self.resonance_os_dir / "data"
        
        print("🚀 ResonanceOS v6 Setup")
        print("=" * 50)
        print(f"Project Root: {self.project_root}")
        print(f"ResonanceOS Directory: {self.resonance_os_dir}")
        print(f"Data Directory: {self.data_dir}")
    
    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        print("\n🐍 Checking Python Version...")
        print("-" * 30)
        
        version_info = sys.version_info
        required_version = (3, 8)
        
        if version_info >= required_version:
            print(f"✅ Python {version_info.major}.{version_info.minor}.{version_info.micro} (>= {required_version[0]}.{required_version[1]})")
            return True
        else:
            print(f"❌ Python {version_info.major}.{version_info.minor}.{version_info.micro} (< {required_version[0]}.{required_version[1]})")
            print(f"   Required: Python {required_version[0]}.{required_version[1]} or higher")
            return False
    
    def create_directory_structure(self):
        """Create complete directory structure"""
        print("\n📁 Creating Directory Structure...")
        print("-" * 40)
        
        directories = [
            "resonance_os/data/config",
            "resonance_os/data/samples/sample_texts",
            "resonance_os/data/samples/sample_profiles",
            "resonance_os/data/samples/example_outputs",
            "resonance_os/data/corpora/training",
            "resonance_os/data/corpora/validation",
            "resonance_os/data/corpora/test",
            "resonance_os/data/models/hrf_models",
            "resonance_os/data/models/embeddings",
            "resonance_os/data/models/checkpoints",
            "resonance_os/data/profiles/hr_profiles",
            "resonance_os/data/profiles/schemas",
            "resonance_os/data/profiles/templates",
            "resonance_os/data/profiles/examples",
            "resonance_os/data/scripts",
            "resonance_os/data/logs/generation",
            "resonance_os/data/logs/api",
            "resonance_os/data/logs/performance",
            "resonance_os/data/logs/errors",
            "resonance_os/data/logs/system",
            "resonance_os/data/exports/analytics",
            "resonance_os/data/exports/visualizations",
            "resonance_os/data/exports/backups",
            "resonance_os/data/exports/data_exports",
            "resonance_os/examples/basic_usage",
            "resonance_os/examples/advanced_usage",
            "resonance_os/examples/integration_examples",
            "resonance_os/examples/business_scenarios",
            "resonance_os/examples/creative_applications",
            "resonance_os/examples/data_science_examples",
            "resonance_os/examples/testing_examples",
            "resonance_os/examples/tutorials",
            "tests/unit",
            "tests/integration",
            "tests/performance",
            "tests/edge_cases"
        ]
        
        created_count = 0
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            if dir_path.exists():
                print(f"✅ {directory}")
                created_count += 1
            else:
                print(f"❌ {directory} (failed to create)")
        
        print(f"\n📊 Directory Structure: {created_count}/{len(directories)} directories created")
        return created_count == len(directories)
    
    def initialize_configurations(self):
        """Initialize configuration files"""
        print("\n⚙️ Initializing Configurations...")
        print("-" * 40)
        
        config_files = {
            "resonance_os/data/config/default_profiles.json": {
                "profiles": {
                    "neutral_professional": {
                        "name": "Neutral Professional",
                        "description": "Balanced professional tone for business communications",
                        "hrv_vector": [0.5, 0.0, 0.3, 0.6, 0.4, 0.2, 0.3, 0.7],
                        "metadata": {
                            "category": "business",
                            "formality": "professional",
                            "use_cases": ["reports", "emails", "documentation"]
                        }
                    },
                    "creative_storytelling": {
                        "name": "Creative Storytelling",
                        "description": "Engaging narrative style for creative content",
                        "hrv_vector": [0.7, 0.6, 0.8, 0.4, 0.7, 0.6, 0.9, 0.6],
                        "metadata": {
                            "category": "creative",
                            "formality": "casual",
                            "use_cases": ["stories", "blogs", "creative_content"]
                        }
                    },
                    "technical_academic": {
                        "name": "Technical Academic",
                        "description": "Formal academic and technical writing",
                        "hrv_vector": [0.3, 0.1, 0.2, 0.8, 0.3, 0.1, 0.2, 0.9],
                        "metadata": {
                            "category": "academic",
                            "formality": "formal",
                            "use_cases": ["papers", "documentation", "research"]
                        }
                    }
                }
            },
            "resonance_os/data/config/system_config.json": {
                "system": {
                    "name": "ResonanceOS v6",
                    "version": "6.0.0",
                    "debug": False,
                    "log_level": "INFO"
                },
                "hrv": {
                    "dimensions": 8,
                    "vector_range": [0.0, 1.0],
                    "emotional_valence_range": [-1.0, 1.0],
                    "default_threshold": 0.7
                },
                "api": {
                    "host": "0.0.0.0",
                    "port": 8000,
                    "workers": 4,
                    "timeout": 30
                },
                "profiles": {
                    "default_directory": "./data/profiles/hr_profiles",
                    "auto_save": True,
                    "backup_enabled": True
                },
                "generation": {
                    "default_paragraphs": 3,
                    "max_paragraph_length": 500,
                    "min_content_length": 100
                },
                "logging": {
                    "log_rotation": True,
                    "max_log_size": "100MB",
                    "max_log_files": 10,
                    "backup_count": 5
                },
                "performance": {
                    "cache_enabled": True,
                    "cache_size": "1GB",
                    "batch_processing": True,
                    "parallel_processing": True,
                    "max_workers": 4
                },
                "security": {
                    "encryption_enabled": False,
                    "tenant_isolation": True,
                    "audit_logging": True,
                    "rate_limiting": True
                }
            },
            "resonance_os/data/config/model_settings.json": {
                "hrf_model": {
                    "algorithm": "linear_regression_with_regularization",
                    "training_dataset": "internal_corpus_v1",
                    "regularization": "l2",
                    "regularization_strength": 0.01,
                    "learning_rate": 0.001,
                    "batch_size": 32,
                    "epochs": 100
                },
                "planner_layer": {
                    "max_paragraphs": 10,
                    "min_paragraphs": 1,
                    "content_strategy": "balanced"
                },
                "sentence_layer": {
                    "max_sentence_length": 100,
                    "min_sentence_length": 5,
                    "variance_factor": 0.5
                },
                "refiner_layer": {
                    "max_iterations": 3,
                    "convergence_threshold": 0.05,
                    "feedback_weight": 0.7
                },
                "hrv_extractor": {
                    "features": ["sentence_variance", "sentiment", "readability", "complexity"],
                    "normalization": "min_max",
                    "smoothing": True
                }
            }
        }
        
        created_files = 0
        for file_path, content in config_files.items():
            full_path = self.project_root / file_path
            
            try:
                with open(full_path, 'w') as f:
                    json.dump(content, f, indent=2)
                
                print(f"✅ {file_path}")
                created_files += 1
                
            except Exception as e:
                print(f"❌ {file_path} (failed: {e})")
        
        print(f"\n📊 Configuration Files: {created_files}/{len(config_files)} files created")
        return created_files == len(config_files)
    
    def create_sample_data(self):
        """Create sample data files"""
        print("\n📝 Creating Sample Data...")
        print("-" * 30)
        
        sample_files = {
            "resonance_os/data/samples/sample_texts/business_report.txt": 
                """Executive Summary: Q3 2024 Financial Performance Report
                
                The third quarter of 2024 demonstrated remarkable growth across all key performance indicators. 
                Revenue increased by 23% compared to the previous quarter, reaching a record high of $45.2 million. 
                This growth was primarily driven by our expanded product line and successful market penetration 
                in emerging regions.
                
                Key Highlights:
                - Revenue growth of 23% quarter-over-quarter
                - Profit margin improvement of 3.2 percentage points
                - Customer acquisition cost reduced by 15%
                - Customer retention rate increased to 92%
                
                Strategic Initiatives:
                Our focus on digital transformation and operational excellence has yielded significant results. 
                The implementation of AI-powered analytics has improved decision-making capabilities by 40%, 
                while our customer satisfaction scores have reached an all-time high of 4.6 out of 5.0.
                """,
            
            "resonance_os/data/samples/sample_texts/creative_story.txt":
                """The Enchanted Forest
                
                In the heart of the mystical forest, where sunlight danced through emerald leaves like golden fairies, 
                there existed a place that maps forgot and time overlooked. Sarah discovered this hidden sanctuary 
                on a misty Tuesday morning, when the world seemed to hold its breath in anticipation of something 
                extraordinary.
                
                The ancient trees whispered secrets in languages older than memory, their gnarled branches 
                reaching toward the sky like weathered hands seeking divine connection. Each step deeper into the 
                forest revealed wonders that defied explanation and challenged the boundaries of imagination.
                
                As Sarah ventured further, she realized that this wasn't just a forest—it was a living, breathing 
                entity that pulsed with the rhythm of countless stories waiting to be told. The air itself seemed 
                to shimmer with possibility, and every shadow held the promise of adventure and discovery.
                """,
            
            "resonance_os/data/samples/sample_texts/technical_article.txt":
                """Advanced Machine Learning Architecture for Real-Time Analytics
                
                Abstract: This paper presents a comprehensive analysis of modern machine learning architectures 
                designed for real-time data processing and analytics. We propose a novel approach that combines 
                edge computing with cloud-based processing to achieve optimal performance and scalability.
                
                Introduction: The increasing volume and velocity of data generated by modern applications 
                require innovative architectural solutions. Traditional batch processing approaches are 
                insufficient for real-time analytics, necessitating the development of stream processing 
                architectures that can handle data at scale.
                
                Methodology: Our research employs a hybrid architecture that leverages the strengths of both 
                edge and cloud computing. Edge devices handle initial data processing and filtering, while 
                cloud resources perform complex analytics and model training. This approach reduces latency 
                and bandwidth requirements while maintaining high accuracy.
                
                Results: Experimental results demonstrate that our hybrid architecture achieves 45% lower 
                latency compared to traditional cloud-only approaches, while maintaining 98% of the accuracy 
                of centralized systems. The system scales linearly with the number of edge devices and can 
                handle throughput of up to 1M events per second.
                """
        }
        
        created_files = 0
        for file_path, content in sample_files.items():
            full_path = self.project_root / file_path
            
            try:
                with open(full_path, 'w') as f:
                    f.write(content)
                
                print(f"✅ {file_path}")
                created_files += 1
                
            except Exception as e:
                print(f"❌ {file_path} (failed: {e})")
        
        print(f"\n📊 Sample Files: {created_files}/{len(sample_files)} files created")
        return created_files == len(sample_files)
    
    def setup_environment(self):
        """Setup environment variables and configuration"""
        print("\n🌍 Setting Up Environment...")
        print("-" * 30)
        
        # Create .env file
        env_file = self.project_root / ".env"
        env_content = """# ResonanceOS v6 Environment Configuration

# API Configuration
API_HOST=localhost
API_PORT=8000
API_WORKERS=4

# Data Directories
HRV_TENANT_DIR=./resonance_os/data/profiles/hr_profiles
DATA_DIR=./resonance_os/data
EXPORTS_DIR=./resonance_os/data/exports
LOGS_DIR=./resonance_os/data/logs

# System Configuration
DEBUG=false
LOG_LEVEL=INFO
CACHE_ENABLED=true
CACHE_SIZE=1GB

# Security
ENCRYPTION_ENABLED=false
TENANT_ISOLATION=true
AUDIT_LOGGING=true

# Performance
MAX_WORKERS=4
BATCH_SIZE=32
PARALLEL_PROCESSING=true

# Development
PYTHONPATH=./
"""
        
        try:
            with open(env_file, 'w') as f:
                f.write(env_content)
            
            print("✅ .env file created")
            
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
        
        # Set up Python path
        python_path = str(self.project_root)
        if python_path not in os.environ.get('PYTHONPATH', ''):
            os.environ['PYTHONPATH'] = python_path + ':' + os.environ.get('PYTHONPATH', '')
        
        print("✅ PYTHONPATH configured")
        return True
    
    def verify_installation(self) -> bool:
        """Verify the installation"""
        print("\n🔍 Verifying Installation...")
        print("-" * 30)
        
        verification_results = {
            "python_version": self.check_python_version(),
            "directories": self._check_directories(),
            "config_files": self._check_config_files(),
            "sample_data": self._check_sample_data(),
            "import_modules": self._check_import_modules()
        }
        
        all_passed = all(verification_results.values())
        
        for check_name, result in verification_results.items():
            status = "✅" if result else "❌"
            print(f"{status} {check_name.replace('_', ' ').title()}")
        
        return all_passed
    
    def _check_directories(self) -> bool:
        """Check if required directories exist"""
        required_dirs = [
            "resonance_os/data/config",
            "resonance_os/data/profiles",
            "resonance_os/data/scripts",
            "resonance_os/data/logs",
            "resonance_os/data/exports",
            "examples"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                return False
        
        return True
    
    def _check_config_files(self) -> bool:
        """Check if required config files exist"""
        required_files = [
            "resonance_os/data/config/default_profiles.json",
            "resonance_os/data/config/system_config.json",
            "resonance_os/data/config/model_settings.json"
        ]
        
        for file_name in required_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                return False
        
        return True
    
    def _check_sample_data(self) -> bool:
        """Check if sample data exists"""
        sample_files = [
            "resonance_os/data/samples/sample_texts/business_report.txt",
            "resonance_os/data/samples/sample_texts/creative_story.txt",
            "resonance_os/data/samples/sample_texts/technical_article.txt"
        ]
        
        for file_name in sample_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                return False
        
        return True
    
    def _check_import_modules(self) -> bool:
        """Check if core modules can be imported"""
        try:
            # Test core imports
            from resonance_os.generation.human_resonant_writer import HumanResonantWriter
            from resonance_os.profiles.hrv_extractor import HRVExtractor
            from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
            from resonance_os.api.hr_server import hr_generate
            
            print("✅ Core modules import successfully")
            return True
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False
    
    def run_initial_tests(self) -> bool:
        """Run initial tests to verify setup"""
        print("\n🧪 Running Initial Tests...")
        print("-" * 30)
        
        try:
            # Import test runner
            from test_runner import run_all_tests
            
            print("Running comprehensive test suite...")
            success = run_all_tests()
            
            return success
            
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            return False
    
    def generate_setup_report(self) -> Dict[str, Any]:
        """Generate setup completion report"""
        print("\n📋 Generating Setup Report...")
        print("-" * 30)
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "project_root": str(self.project_root),
            "setup_completed": True,
            "verification": self.verify_installation(),
            "next_steps": [
                "Run 'python system_runner.py --all' for comprehensive system check",
                "Run 'python test_runner.py' to verify all tests pass",
                "Start API server with 'python system_runner.py --serve'",
                "Try examples with 'python examples/tutorials/getting_started.py'"
            ]
        }
        
        # Save report
        reports_dir = self.data_dir / "exports" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = reports_dir / f"setup_report_{time.strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✅ Setup report saved to: {report_file}")
        return report
    
    def run_complete_setup(self):
        """Run complete setup process"""
        print("🎯 Starting Complete ResonanceOS v6 Setup")
        print("=" * 60)
        
        setup_steps = [
            ("Python Version Check", self.check_python_version),
            ("Directory Structure Creation", self.create_directory_structure),
            ("Configuration Initialization", self.initialize_configurations),
            ("Sample Data Creation", self.create_sample_data),
            ("Environment Setup", self.setup_environment)
        ]
        
        completed_steps = 0
        
        for step_name, step_func in setup_steps:
            print(f"\n{step_name}...")
            try:
                if step_func():
                    completed_steps += 1
                else:
                    print(f"❌ {step_name} failed")
                    return False
            except Exception as e:
                print(f"❌ {step_name} error: {e}")
                return False
        
        print(f"\n📊 Setup Progress: {completed_steps}/{len(setup_steps)} steps completed")
        
        # Verify installation
        if self.verify_installation():
            print("\n🎉 Setup Verification: PASSED")
            
            # Run initial tests
            if self.run_initial_tests():
                print("\n🎉 Initial Tests: PASSED")
                
                # Generate report
                self.generate_setup_report()
                
                print("\n" + "=" * 60)
                print("🎉 ResonanceOS v6 Setup Complete!")
                print("=" * 60)
                print("\n✅ System is ready for use!")
                print("\nNext Steps:")
                print("1. Run 'python system_runner.py --all' for comprehensive system check")
                print("2. Start API server: 'python system_runner.py --serve'")
                print("3. Try examples: 'python examples/tutorials/getting_started.py'")
                print("4. View documentation: 'open resonance_os/docs/README.md'")
                
                return True
            else:
                print("\n⚠️ Initial Tests: FAILED")
                print("\nPlease check the test output above for issues.")
                return False
        else:
            print("\n❌ Setup Verification: FAILED")
            print("\nPlease check the verification output above for issues.")
            return False


def main():
    """Main setup interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ResonanceOS v6 Setup Script")
    parser.add_argument("--check-only", action="store_true", help="Only check existing installation")
    parser.add_argument("--verify", action="store_true", help="Verify installation after setup")
    parser.add_argument("--force", action="store_true", help="Force recreation of existing files")
    
    args = parser.parse_args()
    
    setup = ResonanceOSSetup()
    
    try:
        if args.check_only:
            print("🔍 Checking Existing Installation...")
            print("=" * 50)
            
            if setup.verify_installation():
                print("\n🎉 Installation is complete and verified!")
            else:
                print("\n❌ Installation verification failed")
                print("Please run setup again: 'python setup.py'")
            
        elif args.verify:
            print("🔍 Verifying Installation...")
            print("=" * 30)
            
            if setup.verify_installation():
                print("\n🎉 Installation verified successfully!")
            else:
                print("\n❌ Installation verification failed")
        
        else:
            # Run complete setup
            success = setup.run_complete_setup()
            sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
