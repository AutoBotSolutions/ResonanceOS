#!/usr/bin/env python3
"""
HRV Profile Generator

This script provides utilities for creating, managing, and optimizing HRV profiles
for ResonanceOS v6. It includes profile generation from sample content, profile
optimization based on performance metrics, and profile validation utilities.
"""

import json
import sys
import os
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import argparse

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.generation.human_resonant_writer import HumanResonantWriter


class HRVProfileGenerator:
    """Advanced HRV profile generation and management"""
    
    def __init__(self, profiles_dir: str = None):
        self.profiles_dir = profiles_dir or str(Path(__file__).parent)
        self.extractor = HRVExtractor()
        self.writer = HumanResonantWriter()
        
        # Load configuration
        self.config = self._load_config()
        
        # HRV dimension names
        self.dimensions = [
            "sentence_variance", "emotional_valence", "emotional_intensity",
            "assertiveness_index", "curiosity_index", "metaphor_density",
            "storytelling_index", "active_voice_ratio"
        ]
    
    def _load_config(self) -> Dict[str, Any]:
        """Load profile system configuration"""
        config_path = Path(self.profiles_dir) / "config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def create_profile_from_sample(self, sample_text: str, profile_name: str,
                                  tenant: str = "default", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create HRV profile from sample text"""
        
        print(f"🎯 Creating profile '{profile_name}' from sample text...")
        
        # Extract HRV from sample text
        hrv_vector = self.extractor.extract(sample_text)
        
        # Analyze text characteristics
        text_analysis = self._analyze_text_characteristics(sample_text)
        
        # Create profile data
        profile_data = {
            "name": profile_name,
            "version": "1.0",
            "description": f"Profile generated from sample text on {datetime.now().isoformat()}",
            "target_hrv": hrv_vector,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "created_by": "profile_generator",
                "source": "sample_text",
                "text_analysis": text_analysis,
                "sample_length": len(sample_text),
                **(metadata or {})
            },
            "hrv_dimensions": self._create_dimension_details(hrv_vector),
            "generation_guidelines": self._generate_guidelines(hrv_vector, text_analysis),
            "quality_metrics": self._estimate_quality_metrics(hrv_vector),
            "compatibility": {
                "resonance_os_version": "v6.0+",
                "api_version": "1.0+",
                "dependencies": []
            }
        }
        
        # Validate profile
        validation_result = self.validate_profile(profile_data)
        if not validation_result["valid"]:
            print(f"❌ Profile validation failed: {validation_result['errors']}")
            return None
        
        print(f"✅ Profile '{profile_name}' created successfully")
        print(f"   HRV Vector: {[round(x, 3) for x in hrv_vector]}")
        print(f"   Average HRV Score: {np.mean(hrv_vector):.3f}")
        
        return profile_data
    
    def optimize_profile(self, profile_data: Dict[str, Any], 
                        optimization_goals: Dict[str, float]) -> Dict[str, Any]:
        """Optimize existing profile based on goals"""
        
        print(f"🔧 Optimizing profile '{profile_data['name']}'...")
        
        current_hrv = profile_data["target_hrv"]
        optimized_hrv = current_hrv.copy()
        
        # Apply optimization based on goals
        for goal, target_value in optimization_goals.items():
            if goal in self.dimensions:
                dimension_index = self.dimensions.index(goal)
                current_value = optimized_hrv[dimension_index]
                
                # Gradual adjustment towards target
                adjustment_factor = 0.3  # Adjust by 30% of difference
                optimized_hrv[dimension_index] = current_value + (target_value - current_value) * adjustment_factor
                
                # Ensure value stays within valid range
                dimension_config = self.config.get("hrv_dimensions", {}).get(goal, {})
                valid_range = dimension_config.get("range", [0.0, 1.0])
                optimized_hrv[dimension_index] = np.clip(optimized_hrv[dimension_index], valid_range[0], valid_range[1])
        
        # Create optimized profile
        optimized_profile = profile_data.copy()
        optimized_profile["target_hrv"] = optimized_hrv
        optimized_profile["version"] = str(float(profile_data["version"]) + 0.1)
        optimized_profile["metadata"]["updated_at"] = datetime.now().isoformat()
        optimized_profile["metadata"]["optimization_goals"] = optimization_goals
        optimized_profile["metadata"]["original_hrv"] = current_hrv
        
        print(f"✅ Profile optimized successfully")
        print(f"   Original HRV: {[round(x, 3) for x in current_hrv]}")
        print(f"   Optimized HRV: {[round(x, 3) for x in optimized_hrv]}")
        
        return optimized_profile
    
    def blend_profiles(self, profile1_data: Dict[str, Any], profile2_data: Dict[str, Any],
                      weight1: float = 0.5, blend_name: str = None) -> Dict[str, Any]:
        """Blend two profiles to create a hybrid"""
        
        name1 = profile1_data["name"]
        name2 = profile2_data["name"]
        blend_name = blend_name or f"blend_{name1}_{name2}"
        
        print(f"🔀 Blending profiles '{name1}' and '{name2}'...")
        
        hrv1 = np.array(profile1_data["target_hrv"])
        hrv2 = np.array(profile2_data["target_hrv"])
        
        # Weighted blend
        blended_hrv = hrv1 * weight1 + hrv2 * (1 - weight1)
        
        # Create blended profile
        blended_profile = {
            "name": blend_name,
            "version": "1.0",
            "description": f"Blend of {name1} ({weight1:.1%}) and {name2} ({1-weight1:.1%})",
            "target_hrv": blended_hrv.tolist(),
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "created_by": "profile_generator",
                "source_profiles": [name1, name2],
                "blend_weights": {"profile1": weight1, "profile2": 1 - weight1},
                "parent_profiles": {
                    "profile1": {
                        "name": name1,
                        "version": profile1_data.get("version", "1.0"),
                        "hrv": profile1_data["target_hrv"]
                    },
                    "profile2": {
                        "name": name2,
                        "version": profile2_data.get("version", "1.0"),
                        "hrv": profile2_data["target_hrv"]
                    }
                }
            },
            "hrv_dimensions": self._create_dimension_details(blended_hrv.tolist()),
            "generation_guidelines": self._generate_guidelines(blended_hrv.tolist()),
            "quality_metrics": self._estimate_quality_metrics(blended_hrv.tolist()),
            "compatibility": profile1_data.get("compatibility", {
                "resonance_os_version": "v6.0+",
                "api_version": "1.0+",
                "dependencies": []
            })
        }
        
        print(f"✅ Profile blend created successfully")
        print(f"   Blended HRV: {[round(x, 3) for x in blended_hrv]}")
        
        return blended_profile
    
    def validate_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate profile structure and data"""
        
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = self.config.get("profile_validation", {}).get("required_fields", [])
        for field in required_fields:
            if field not in profile_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate HRV vector
        if "target_hrv" in profile_data:
            hrv = profile_data["target_hrv"]
            
            # Check vector length
            expected_length = self.config.get("profile_validation", {}).get("hrv_validation", {}).get("vector_length", 8)
            if len(hrv) != expected_length:
                errors.append(f"HRV vector length must be {expected_length}, got {len(hrv)}")
            
            # Check dimension ranges
            dimension_ranges = self.config.get("profile_validation", {}).get("hrv_validation", {}).get("dimension_ranges", {})
            for i, (dimension, value) in enumerate(zip(self.dimensions, hrv)):
                if dimension in dimension_ranges:
                    valid_range = dimension_ranges[dimension]
                    if not (valid_range[0] <= value <= valid_range[1]):
                        errors.append(f"{dimension} value {value} outside valid range {valid_range}")
        
        # Validate metadata
        if "metadata" in profile_data:
            metadata = profile_data["metadata"]
            required_metadata = self.config.get("profile_validation", {}).get("metadata_schema", {}).get("required", [])
            for field in required_metadata:
                if field not in metadata:
                    errors.append(f"Missing required metadata field: {field}")
        
        # Check for potential issues
        if "target_hrv" in profile_data:
            hrv = profile_data["target_hrv"]
            
            # Check for extreme values
            for i, (dimension, value) in enumerate(zip(self.dimensions, hrv)):
                if abs(value) > 0.95:
                    warnings.append(f"{dimension} value {value:.3f} is very close to extreme")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "validation_time": datetime.now().isoformat()
        }
    
    def save_profile(self, profile_data: Dict[str, Any], tenant: str = "default") -> str:
        """Save profile to file"""
        
        profile_name = profile_data["name"]
        tenant_dir = Path(self.profiles_dir) / tenant
        tenant_dir.mkdir(exist_ok=True)
        
        profile_path = tenant_dir / f"{profile_name}.json"
        
        with open(profile_path, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        print(f"💾 Profile saved to: {profile_path}")
        return str(profile_path)
    
    def load_profile(self, tenant: str, profile_name: str) -> Optional[Dict[str, Any]]:
        """Load profile from file"""
        
        profile_path = Path(self.profiles_dir) / tenant / f"{profile_name}.json"
        
        if not profile_path.exists():
            print(f"❌ Profile not found: {profile_path}")
            return None
        
        with open(profile_path, 'r') as f:
            profile_data = json.load(f)
        
        return profile_data
    
    def list_profiles(self, tenant: str = "default") -> List[str]:
        """List available profiles for tenant"""
        
        tenant_dir = Path(self.profiles_dir) / tenant
        if not tenant_dir.exists():
            return []
        
        profiles = []
        for file_path in tenant_dir.glob("*.json"):
            if file_path.name != "config.json":
                profiles.append(file_path.stem)
        
        return sorted(profiles)
    
    def _analyze_text_characteristics(self, text: str) -> Dict[str, Any]:
        """Analyze text characteristics for profile generation"""
        
        words = text.split()
        sentences = text.split('.')
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Basic statistics
        word_count = len(words)
        sentence_count = len([s for s in sentences if s.strip()])
        paragraph_count = len(paragraphs)
        
        # Average lengths
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        
        # Vocabulary richness (unique words / total words)
        unique_words = len(set(word.lower() for word in words))
        vocabulary_richness = unique_words / word_count if word_count > 0 else 0
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "avg_sentence_length": avg_sentence_length,
            "avg_word_length": avg_word_length,
            "vocabulary_richness": vocabulary_richness,
            "readability_estimate": self._estimate_readability(avg_sentence_length, avg_word_length)
        }
    
    def _estimate_readability(self, avg_sentence_length: float, avg_word_length: float) -> str:
        """Estimate readability level"""
        
        # Simple readability estimation
        if avg_sentence_length < 15 and avg_word_length < 5:
            return "Easy"
        elif avg_sentence_length < 20 and avg_word_length < 6:
            return "Medium"
        else:
            return "Difficult"
    
    def _create_dimension_details(self, hrv_vector: List[float]) -> Dict[str, Any]:
        """Create detailed dimension information"""
        
        dimension_details = {}
        
        for i, (dimension, value) in enumerate(zip(self.dimensions, hrv_vector)):
            dimension_config = self.config.get("hrv_dimensions", {}).get(dimension, {})
            
            dimension_details[dimension] = {
                "value": value,
                "description": dimension_config.get("description", ""),
                "target_range": dimension_config.get("range", [0.0, 1.0]),
                "impact": dimension_config.get("impact", "")
            }
        
        return dimension_details
    
    def _generate_guidelines(self, hrv_vector: List[float], text_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate content guidelines based on HRV vector"""
        
        guidelines = {
            "sentence_length": {},
            "paragraph_length": {},
            "vocabulary": "",
            "tone": "",
            "style": ""
        }
        
        # Sentence length guidelines
        sentence_variance = hrv_vector[0]
        if sentence_variance > 0.7:
            guidelines["sentence_length"] = {
                "average": "12-18 words",
                "range": "5-40 words"
            }
        elif sentence_variance > 0.4:
            guidelines["sentence_length"] = {
                "average": "15-20 words",
                "range": "8-30 words"
            }
        else:
            guidelines["sentence_length"] = {
                "average": "18-25 words",
                "range": "10-35 words"
            }
        
        # Paragraph length guidelines
        storytelling = hrv_vector[6]
        if storytelling > 0.7:
            guidelines["paragraph_length"] = {
                "average": "4-6 sentences",
                "range": "2-10 sentences"
            }
        else:
            guidelines["paragraph_length"] = {
                "average": "3-5 sentences",
                "range": "2-7 sentences"
            }
        
        # Vocabulary and tone guidelines
        emotional_valence = hrv_vector[1]
        assertiveness = hrv_vector[3]
        
        if emotional_valence > 0.5:
            guidelines["tone"] = "Positive and optimistic"
        elif emotional_valence < -0.5:
            guidelines["tone"] = "Negative or critical"
        else:
            guidelines["tone"] = "Neutral and balanced"
        
        if assertiveness > 0.7:
            guidelines["style"] = "Confident and direct"
        elif assertiveness > 0.4:
            guidelines["style"] = "Moderate and balanced"
        else:
            guidelines["style"] = "Cautious and indirect"
        
        return guidelines
    
    def _estimate_quality_metrics(self, hrv_vector: List[float]) -> Dict[str, Any]:
        """Estimate quality metrics based on HRV vector"""
        
        avg_hrv = np.mean(hrv_vector)
        
        # Estimate readability based on sentence variance and active voice
        readability_estimate = 60 + (hrv_vector[0] * 10) + (hrv_vector[7] * 10)
        readability_estimate = np.clip(readability_estimate, 30, 90)
        
        # Estimate engagement based on emotional and curiosity factors
        engagement_estimate = 50 + (hrv_vector[2] * 20) + (hrv_vector[4] * 20) + (hrv_vector[6] * 10)
        engagement_estimate = np.clip(engagement_estimate, 40, 95)
        
        # Estimate completion based on overall HRV balance
        completion_estimate = 70 + (avg_hrv * 20)
        completion_estimate = np.clip(completion_estimate, 50, 95)
        
        return {
            "readability_score": f"Target: {readability_estimate:.0f} (Flesch-Kincaid)",
            "engagement_rate": f"Target: {engagement_estimate:.0f}%",
            "completion_rate": f"Target: {completion_estimate:.0f}%"
        }


def main():
    """Command line interface for profile generator"""
    
    parser = argparse.ArgumentParser(description="HRV Profile Generator")
    parser.add_argument("--action", choices=["create", "optimize", "blend", "list", "validate"], 
                       required=True, help="Action to perform")
    parser.add_argument("--tenant", default="default", help="Tenant name")
    parser.add_argument("--profile", help="Profile name")
    parser.add_argument("--sample", help="Sample text file for profile creation")
    parser.add_argument("--text", help="Sample text for profile creation")
    parser.add_argument("--output", help="Output profile name")
    parser.add_argument("--profile1", help="First profile for blending")
    parser.add_argument("--profile2", help="Second profile for blending")
    parser.add_argument("--weight", type=float, default=0.5, help="Blend weight for profile1")
    
    args = parser.parse_args()
    
    generator = HRVProfileGenerator()
    
    if args.action == "create":
        if args.sample:
            with open(args.sample, 'r') as f:
                sample_text = f.read()
        elif args.text:
            sample_text = args.text
        else:
            print("❌ Either --sample or --text required for profile creation")
            return
        
        profile_name = args.output or f"generated_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        profile_data = generator.create_profile_from_sample(sample_text, profile_name, args.tenant)
        if profile_data:
            generator.save_profile(profile_data, args.tenant)
    
    elif args.action == "list":
        profiles = generator.list_profiles(args.tenant)
        print(f"📋 Profiles for tenant '{args.tenant}':")
        for profile in profiles:
            print(f"   - {profile}")
    
    elif args.action == "validate":
        if not args.profile:
            print("❌ --profile required for validation")
            return
        
        profile_data = generator.load_profile(args.tenant, args.profile)
        if profile_data:
            validation = generator.validate_profile(profile_data)
            if validation["valid"]:
                print(f"✅ Profile '{args.profile}' is valid")
            else:
                print(f"❌ Profile '{args.profile}' has errors:")
                for error in validation["errors"]:
                    print(f"   - {error}")
            
            if validation["warnings"]:
                print(f"⚠️  Profile '{args.profile}' has warnings:")
                for warning in validation["warnings"]:
                    print(f"   - {warning}")
    
    elif args.action == "blend":
        if not args.profile1 or not args.profile2:
            print("❌ Both --profile1 and --profile2 required for blending")
            return
        
        profile1_data = generator.load_profile(args.tenant, args.profile1)
        profile2_data = generator.load_profile(args.tenant, args.profile2)
        
        if profile1_data and profile2_data:
            blend_name = args.output or f"blend_{args.profile1}_{args.profile2}"
            blended_profile = generator.blend_profiles(profile1_data, profile2_data, args.weight, blend_name)
            generator.save_profile(blended_profile, args.tenant)


if __name__ == "__main__":
    main()
