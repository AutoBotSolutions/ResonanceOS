#!/usr/bin/env python3
"""
ResonanceOS v6 Profiles Setup Script

This script sets up the profiles directory structure, initializes default profiles,
and configures the profile management system for ResonanceOS v6.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class ProfilesSetup:
    """Setup and configuration for ResonanceOS v6 profiles"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.profiles_dir = self.base_dir / "hr_profiles"
        self.setup_log = []
    
    def log(self, message: str, level: str = "INFO"):
        """Log setup message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.setup_log.append(log_entry)
        print(log_entry)
    
    def setup_directory_structure(self) -> bool:
        """Create the profiles directory structure"""
        
        self.log("Setting up directory structure...")
        
        try:
            # Create main profiles directory
            self.profiles_dir.mkdir(exist_ok=True)
            self.log(f"Created profiles directory: {self.profiles_dir}")
            
            # Create default tenant directory
            default_dir = self.profiles_dir / "default"
            default_dir.mkdir(exist_ok=True)
            self.log(f"Created default tenant directory: {default_dir}")
            
            # Create example tenant directories
            example_tenants = ["tenant_a", "tenant_b", "enterprise"]
            for tenant in example_tenants:
                tenant_dir = self.profiles_dir / tenant
                tenant_dir.mkdir(exist_ok=True)
                self.log(f"Created example tenant directory: {tenant_dir}")
            
            return True
            
        except Exception as e:
            self.log(f"Failed to create directory structure: {e}", "ERROR")
            return False
    
    def create_default_profiles(self) -> bool:
        """Create default HRV profiles"""
        
        self.log("Creating default HRV profiles...")
        
        default_profiles = {
            "neutral_professional": {
                "name": "neutral_professional",
                "version": "1.0",
                "description": "Balanced professional tone suitable for business documents, reports, and formal communications",
                "target_hrv": [0.6, 0.3, 0.4, 0.7, 0.5, 0.3, 0.4, 0.8],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "created_by": "setup_script",
                    "tags": ["professional", "business", "formal", "balanced"],
                    "use_case": "Business documentation and reports"
                }
            },
            "creative_storytelling": {
                "name": "creative_storytelling",
                "version": "1.0",
                "description": "Creative and narrative-focused profile ideal for storytelling, creative writing, and engaging content",
                "target_hrv": [0.8, 0.5, 0.7, 0.4, 0.8, 0.8, 0.9, 0.6],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "created_by": "setup_script",
                    "tags": ["creative", "storytelling", "narrative", "engaging"],
                    "use_case": "Creative writing and storytelling"
                }
            },
            "marketing_enthusiastic": {
                "name": "marketing_enthusiastic",
                "version": "1.0",
                "description": "High-energy marketing profile designed for persuasive content, campaigns, and promotional materials",
                "target_hrv": [0.7, 0.6, 0.8, 0.6, 0.7, 0.6, 0.7, 0.8],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "created_by": "setup_script",
                    "tags": ["marketing", "enthusiastic", "persuasive", "high-energy"],
                    "use_case": "Marketing campaigns and promotional content"
                }
            },
            "tech_startup": {
                "name": "tech_startup",
                "version": "1.0",
                "description": "Technology and innovation focused profile for startups, tech companies, and digital products",
                "target_hrv": [0.5, 0.4, 0.5, 0.8, 0.6, 0.4, 0.5, 0.9],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "created_by": "setup_script",
                    "tags": ["technology", "startup", "innovation", "technical"],
                    "use_case": "Technology documentation and startup content"
                }
            },
            "persuasive_sales": {
                "name": "persuasive_sales",
                "version": "1.0",
                "description": "Sales and conversion focused profile designed to persuade, convert, and drive action",
                "target_hrv": [0.6, 0.7, 0.8, 0.9, 0.5, 0.5, 0.6, 0.9],
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "created_by": "setup_script",
                    "tags": ["sales", "persuasive", "conversion", "action-oriented"],
                    "use_case": "Sales content and conversion optimization"
                }
            }
        }
        
        try:
            default_dir = self.profiles_dir / "default"
            
            for profile_name, profile_data in default_profiles.items():
                profile_path = default_dir / f"{profile_name}.json"
                
                with open(profile_path, 'w') as f:
                    json.dump(profile_data, f, indent=2)
                
                self.log(f"Created default profile: {profile_path}")
            
            return True
            
        except Exception as e:
            self.log(f"Failed to create default profiles: {e}", "ERROR")
            return False
    
    def create_config_file(self) -> bool:
        """Create the profile system configuration file"""
        
        self.log("Creating configuration file...")
        
        config_data = {
            "profile_system": {
                "version": "1.0",
                "description": "HRV Profile Configuration for ResonanceOS v6",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "hrv_dimensions": {
                "sentence_variance": {
                    "name": "Sentence Variance",
                    "description": "Variety in sentence lengths and structures",
                    "range": [0.0, 1.0],
                    "impact": "Readability and engagement"
                },
                "emotional_valence": {
                    "name": "Emotional Valence",
                    "description": "Positive/negative sentiment balance",
                    "range": [-1.0, 1.0],
                    "impact": "Reader emotional response"
                },
                "emotional_intensity": {
                    "name": "Emotional Intensity",
                    "description": "Strength of emotional content",
                    "range": [0.0, 1.0],
                    "impact": "Emotional engagement"
                },
                "assertiveness_index": {
                    "name": "Assertiveness Index",
                    "description": "Confidence and directness",
                    "range": [0.0, 1.0],
                    "impact": "Authority and credibility"
                },
                "curiosity_index": {
                    "name": "Curiosity Index",
                    "description": "Question and curiosity elements",
                    "range": [0.0, 1.0],
                    "impact": "Reader engagement and interest"
                },
                "metaphor_density": {
                    "name": "Metaphor Density",
                    "description": "Metaphorical language usage",
                    "range": [0.0, 1.0],
                    "impact": "Creativity and memorability"
                },
                "storytelling_index": {
                    "name": "Storytelling Index",
                    "description": "Narrative and storytelling elements",
                    "range": [0.0, 1.0],
                    "impact": "Narrative engagement"
                },
                "active_voice_ratio": {
                    "name": "Active Voice Ratio",
                    "description": "Active vs passive voice",
                    "range": [0.0, 1.0],
                    "impact": "Directness and dynamism"
                }
            },
            "profile_validation": {
                "required_fields": ["name", "version", "description", "target_hrv"],
                "hrv_validation": {
                    "vector_length": 8,
                    "dimension_ranges": {
                        "sentence_variance": [0.0, 1.0],
                        "emotional_valence": [-1.0, 1.0],
                        "emotional_intensity": [0.0, 1.0],
                        "assertiveness_index": [0.0, 1.0],
                        "curiosity_index": [0.0, 1.0],
                        "metaphor_density": [0.0, 1.0],
                        "storytelling_index": [0.0, 1.0],
                        "active_voice_ratio": [0.0, 1.0]
                    }
                },
                "metadata_schema": {
                    "required": ["created_at", "created_by"],
                    "optional": ["updated_at", "tags", "use_case", "target_audience"]
                }
            },
            "tenant_management": {
                "default_tenant": "default",
                "tenant_isolation": True,
                "max_profiles_per_tenant": 100,
                "profile_versioning": True,
                "backup_retention_days": 30
            },
            "performance_settings": {
                "cache_enabled": True,
                "cache_ttl_seconds": 300,
                "max_cache_size": 1000,
                "lazy_loading": True
            },
            "api_settings": {
                "rate_limiting": {
                    "enabled": True,
                    "requests_per_minute": 1000,
                    "burst_size": 100
                },
                "authentication": {
                    "required": False,
                    "methods": ["api_key", "bearer_token"]
                }
            }
        }
        
        try:
            config_path = self.profiles_dir / "config.json"
            
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            self.log(f"Created configuration file: {config_path}")
            return True
            
        except Exception as e:
            self.log(f"Failed to create configuration file: {e}", "ERROR")
            return False
    
    def create_example_tenant_profiles(self) -> bool:
        """Create example profiles for demonstration tenants"""
        
        self.log("Creating example tenant profiles...")
        
        example_profiles = {
            "tenant_a": {
                "brand_voice": {
                    "name": "brand_voice",
                    "version": "1.0",
                    "description": "Custom brand voice profile for Tenant A",
                    "target_hrv": [0.7, 0.5, 0.6, 0.8, 0.6, 0.5, 0.6, 0.8],
                    "metadata": {
                        "created_at": datetime.now().isoformat(),
                        "created_by": "setup_script",
                        "tenant": "tenant_a",
                        "tags": ["brand", "corporate", "professional"],
                        "use_case": "Brand communications and marketing"
                    }
                }
            },
            "tenant_b": {
                "technical_docs": {
                    "name": "technical_docs",
                    "version": "1.0",
                    "description": "Technical documentation profile for Tenant B",
                    "target_hrv": [0.4, 0.2, 0.3, 0.9, 0.4, 0.2, 0.3, 0.9],
                    "metadata": {
                        "created_at": datetime.now().isoformat(),
                        "created_by": "setup_script",
                        "tenant": "tenant_b",
                        "tags": ["technical", "documentation", "precise"],
                        "use_case": "Technical documentation and manuals"
                    }
                }
            },
            "enterprise": {
                "executive_summary": {
                    "name": "executive_summary",
                    "version": "1.0",
                    "description": "Executive communication profile for enterprise tenant",
                    "target_hrv": [0.5, 0.4, 0.5, 0.9, 0.3, 0.3, 0.4, 0.9],
                    "metadata": {
                        "created_at": datetime.now().isoformat(),
                        "created_by": "setup_script",
                        "tenant": "enterprise",
                        "tags": ["executive", "corporate", "formal"],
                        "use_case": "Executive summaries and reports"
                    }
                }
            }
        }
        
        try:
            for tenant_name, profiles in example_profiles.items():
                tenant_dir = self.profiles_dir / tenant_name
                
                for profile_name, profile_data in profiles.items():
                    profile_path = tenant_dir / f"{profile_name}.json"
                    
                    with open(profile_path, 'w') as f:
                        json.dump(profile_data, f, indent=2)
                    
                    self.log(f"Created example profile: {profile_path}")
            
            return True
            
        except Exception as e:
            self.log(f"Failed to create example tenant profiles: {e}", "ERROR")
            return False
    
    def create_utility_scripts(self) -> bool:
        """Create utility scripts for profile management"""
        
        self.log("Creating utility scripts...")
        
        # These scripts are already created in the main setup
        # Just verify they exist and are executable
        required_scripts = [
            "profile_generator.py",
            "profile_validator.py"
        ]
        
        try:
            for script_name in required_scripts:
                script_path = self.profiles_dir / script_name
                if script_path.exists():
                    # Make executable
                    os.chmod(script_path, 0o755)
                    self.log(f"Made script executable: {script_path}")
                else:
                    self.log(f"Warning: Script not found: {script_path}", "WARNING")
            
            return True
            
        except Exception as e:
            self.log(f"Failed to create utility scripts: {e}", "ERROR")
            return False
    
    def create_documentation(self) -> bool:
        """Create documentation files"""
        
        self.log("Creating documentation...")
        
        try:
            # Main README is already created
            # Profiles README is already created
            
            # Create quick start guide
            quick_start_content = """# Quick Start Guide

## Load a Profile
```python
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager

manager = HRVProfileManager("./profiles/hr_profiles")
profile = manager.load_profile("default", "neutral_professional")
```

## Generate Content with Profile
```python
from resonance_os.generation.human_resonant_writer import HumanResonantWriter

writer = HumanResonantWriter()
content = writer.generate("Your prompt here", profile=profile)
```

## Create Custom Profile
```bash
cd profiles/hr_profiles
python profile_generator.py --action create --text "Sample text" --output my_profile
```

## Validate Profile
```bash
python profile_validator.py --action validate --profile my_profile
```
"""
            
            quick_start_path = self.profiles_dir / "QUICK_START.md"
            with open(quick_start_path, 'w') as f:
                f.write(quick_start_content)
            
            self.log(f"Created quick start guide: {quick_start_path}")
            return True
            
        except Exception as e:
            self.log(f"Failed to create documentation: {e}", "ERROR")
            return False
    
    def verify_setup(self) -> bool:
        """Verify that the setup was successful"""
        
        self.log("Verifying setup...")
        
        verification_results = {
            "directories": {},
            "files": {},
            "profiles": {},
            "overall": True
        }
        
        # Check directories
        required_dirs = ["hr_profiles", "hr_profiles/default", "hr_profiles/tenant_a", "hr_profiles/tenant_b", "hr_profiles/enterprise"]
        
        for dir_path in required_dirs:
            full_path = self.base_dir / dir_path
            exists = full_path.exists()
            verification_results["directories"][dir_path] = exists
            if not exists:
                verification_results["overall"] = False
                self.log(f"Missing directory: {full_path}", "ERROR")
        
        # Check files
        required_files = [
            "hr_profiles/config.json",
            "hr_profiles/profile_generator.py",
            "hr_profiles/profile_validator.py",
            "hr_profiles/README.md",
            "hr_profiles/QUICK_START.md"
        ]
        
        for file_path in required_files:
            full_path = self.base_dir / file_path
            exists = full_path.exists()
            verification_results["files"][file_path] = exists
            if not exists:
                verification_results["overall"] = False
                self.log(f"Missing file: {full_path}", "ERROR")
        
        # Check default profiles
        default_profiles = ["neutral_professional", "creative_storytelling", "marketing_enthusiastic", "tech_startup", "persuasive_sales"]
        
        for profile_name in default_profiles:
            profile_path = self.base_dir / "hr_profiles/default" / f"{profile_name}.json"
            exists = profile_path.exists()
            verification_results["profiles"][profile_name] = exists
            if not exists:
                verification_results["overall"] = False
                self.log(f"Missing default profile: {profile_path}", "ERROR")
        
        if verification_results["overall"]:
            self.log("✅ Setup verification successful!")
        else:
            self.log("❌ Setup verification failed!", "ERROR")
        
        return verification_results["overall"]
    
    def save_setup_log(self) -> bool:
        """Save the setup log to a file"""
        
        try:
            log_path = self.profiles_dir / "setup_log.txt"
            
            with open(log_path, 'w') as f:
                f.write("ResonanceOS v6 Profiles Setup Log\n")
                f.write("=" * 50 + "\n")
                f.write(f"Setup Date: {datetime.now().isoformat()}\n")
                f.write(f"Base Directory: {self.base_dir}\n")
                f.write(f"Profiles Directory: {self.profiles_dir}\n")
                f.write("=" * 50 + "\n\n")
                
                for log_entry in self.setup_log:
                    f.write(log_entry + "\n")
            
            self.log(f"Setup log saved to: {log_path}")
            return True
            
        except Exception as e:
            self.log(f"Failed to save setup log: {e}", "ERROR")
            return False
    
    def run_setup(self) -> bool:
        """Run the complete setup process"""
        
        self.log("Starting ResonanceOS v6 Profiles Setup...")
        self.log(f"Base directory: {self.base_dir}")
        self.log(f"Profiles directory: {self.profiles_dir}")
        
        setup_steps = [
            ("Directory Structure", self.setup_directory_structure),
            ("Default Profiles", self.create_default_profiles),
            ("Configuration File", self.create_config_file),
            ("Example Tenant Profiles", self.create_example_tenant_profiles),
            ("Utility Scripts", self.create_utility_scripts),
            ("Documentation", self.create_documentation),
            ("Setup Verification", self.verify_setup),
            ("Save Setup Log", self.save_setup_log)
        ]
        
        for step_name, step_function in setup_steps:
            self.log(f"Executing: {step_name}")
            
            if not step_function():
                self.log(f"Failed: {step_name}", "ERROR")
                return False
            
            self.log(f"Completed: {step_name}")
        
        self.log("🎉 ResonanceOS v6 Profiles setup completed successfully!")
        self.log("\nNext steps:")
        self.log("1. Review the profiles in hr_profiles/default/")
        self.log("2. Test profile generation with: python profile_generator.py --action list")
        self.log("3. Validate profiles with: python profile_validator.py --action batch_validate --directory hr_profiles/default")
        self.log("4. Read the documentation in hr_profiles/README.md")
        
        return True


def main():
    """Main setup function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="ResonanceOS v6 Profiles Setup")
    parser.add_argument("--base-dir", help="Base directory for profiles setup")
    parser.add_argument("--skip-examples", action="store_true", help="Skip example tenant profiles")
    parser.add_argument("--verify-only", action="store_true", help="Only verify existing setup")
    
    args = parser.parse_args()
    
    setup = ProfilesSetup(args.base_dir)
    
    if args.verify_only:
        success = setup.verify_setup()
        if success:
            print("✅ Setup verification passed!")
        else:
            print("❌ Setup verification failed!")
            sys.exit(1)
    else:
        success = setup.run_setup()
        if not success:
            print("❌ Setup failed!")
            sys.exit(1)


if __name__ == "__main__":
    main()
