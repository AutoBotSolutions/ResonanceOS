#!/usr/bin/env python3
"""
HRV Profile Validator

This script provides comprehensive validation utilities for HRV profiles,
including structural validation, HRV vector analysis, and performance
prediction capabilities.
"""

import json
import sys
import os
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import argparse

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.generation.human_resonant_writer import HumanResonantWriter


class HRVProfileValidator:
    """Comprehensive HRV profile validation and analysis"""
    
    def __init__(self, profiles_dir: str = None):
        self.profiles_dir = profiles_dir or str(Path(__file__).parent)
        self.extractor = HRVExtractor()
        self.writer = HumanResonantWriter()
        
        # Load configuration
        self.config = self._load_config()
        
        # HRV dimension names and descriptions
        self.dimensions = [
            ("sentence_variance", "Variety in sentence lengths and structures", [0.0, 1.0]),
            ("emotional_valence", "Positive/negative sentiment balance", [-1.0, 1.0]),
            ("emotional_intensity", "Strength of emotional content", [0.0, 1.0]),
            ("assertiveness_index", "Confidence and directness", [0.0, 1.0]),
            ("curiosity_index", "Question and curiosity elements", [0.0, 1.0]),
            ("metaphor_density", "Metaphorical language usage", [0.0, 1.0]),
            ("storytelling_index", "Narrative and storytelling elements", [0.0, 1.0]),
            ("active_voice_ratio", "Active vs passive voice", [0.0, 1.0])
        ]
    
    def _load_config(self) -> Dict[str, Any]:
        """Load profile system configuration"""
        config_path = Path(self.profiles_dir) / "config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def validate_profile_structure(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate profile structure and required fields"""
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        # Check required top-level fields
        required_fields = ["name", "version", "description", "target_hrv"]
        for field in required_fields:
            if field not in profile_data:
                validation_result["errors"].append(f"Missing required field: {field}")
                validation_result["valid"] = False
        
        # Validate HRV vector
        if "target_hrv" in profile_data:
            hrv_validation = self._validate_hrv_vector(profile_data["target_hrv"])
            validation_result["errors"].extend(hrv_validation["errors"])
            validation_result["warnings"].extend(hrv_validation["warnings"])
            validation_result["info"].extend(hrv_validation["info"])
            
            if not hrv_validation["valid"]:
                validation_result["valid"] = False
        
        # Validate metadata
        if "metadata" in profile_data:
            metadata_validation = self._validate_metadata(profile_data["metadata"])
            validation_result["errors"].extend(metadata_validation["errors"])
            validation_result["warnings"].extend(metadata_validation["warnings"])
        
        # Validate HRV dimensions details
        if "hrv_dimensions" in profile_data:
            dimensions_validation = self._validate_hrv_dimensions(profile_data["hrv_dimensions"])
            validation_result["errors"].extend(dimensions_validation["errors"])
            validation_result["warnings"].extend(dimensions_validation["warnings"])
        
        # Validate generation guidelines
        if "generation_guidelines" in profile_data:
            guidelines_validation = self._validate_generation_guidelines(profile_data["generation_guidelines"])
            validation_result["warnings"].extend(guidelines_validation["warnings"])
        
        return validation_result
    
    def _validate_hrv_vector(self, hrv_vector: List[float]) -> Dict[str, Any]:
        """Validate HRV vector format and values"""
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        # Check type
        if not isinstance(hrv_vector, list):
            validation_result["errors"].append("HRV vector must be a list")
            validation_result["valid"] = False
            return validation_result
        
        # Check length
        if len(hrv_vector) != 8:
            validation_result["errors"].append(f"HRV vector must have 8 dimensions, got {len(hrv_vector)}")
            validation_result["valid"] = False
            return validation_result
        
        # Check each dimension
        for i, (dimension_name, description, valid_range) in enumerate(self.dimensions):
            if i >= len(hrv_vector):
                break
            
            value = hrv_vector[i]
            
            # Check type
            if not isinstance(value, (int, float)):
                validation_result["errors"].append(f"Dimension {i} ({dimension_name}) must be numeric, got {type(value)}")
                validation_result["valid"] = False
                continue
            
            # Check range
            if not (valid_range[0] <= value <= valid_range[1]):
                validation_result["errors"].append(
                    f"Dimension {i} ({dimension_name}) value {value} outside valid range {valid_range}"
                )
                validation_result["valid"] = False
            else:
                # Check for extreme values (warnings)
                tolerance = 0.05
                if abs(value - valid_range[0]) < tolerance or abs(value - valid_range[1]) < tolerance:
                    validation_result["warnings"].append(
                        f"Dimension {i} ({dimension_name}) value {value:.3f} is very close to range limit"
                    )
        
        # Calculate and report statistics
        if validation_result["valid"]:
            avg_hrv = np.mean(hrv_vector)
            std_hrv = np.std(hrv_vector)
            
            validation_result["info"].append(f"Average HRV score: {avg_hrv:.3f}")
            validation_result["info"].append(f"HRV standard deviation: {std_hrv:.3f}")
            
            # Check for balance
            if std_hrv < 0.1:
                validation_result["warnings"].append("HRV vector has very low variance - may be too balanced")
            elif std_hrv > 0.4:
                validation_result["warnings"].append("HRV vector has very high variance - may be too extreme")
        
        return validation_result
    
    def _validate_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metadata structure"""
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required metadata fields
        required_fields = ["created_at", "created_by"]
        for field in required_fields:
            if field not in metadata:
                validation_result["errors"].append(f"Missing required metadata field: {field}")
                validation_result["valid"] = False
        
        # Validate timestamp format
        if "created_at" in metadata:
            try:
                datetime.fromisoformat(metadata["created_at"].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                validation_result["errors"].append("Invalid created_at timestamp format")
                validation_result["valid"] = False
        
        # Check for missing recommended fields
        recommended_fields = ["updated_at", "tags", "use_case", "target_audience"]
        for field in recommended_fields:
            if field not in metadata:
                validation_result["warnings"].append(f"Missing recommended metadata field: {field}")
        
        return validation_result
    
    def _validate_hrv_dimensions(self, hrv_dimensions: Dict[str, Any]) -> Dict[str, Any]:
        """Validate HRV dimensions details"""
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check that all dimensions are present
        for dimension_name, _, _ in self.dimensions:
            if dimension_name not in hrv_dimensions:
                validation_result["warnings"].append(f"Missing dimension details for: {dimension_name}")
        
        # Validate each dimension detail
        for dimension_name, details in hrv_dimensions.items():
            if not isinstance(details, dict):
                validation_result["errors"].append(f"Dimension details for {dimension_name} must be a dictionary")
                validation_result["valid"] = False
                continue
            
            # Check required fields in dimension details
            if "value" not in details:
                validation_result["errors"].append(f"Missing value in dimension details for {dimension_name}")
                validation_result["valid"] = False
            
            if "description" not in details:
                validation_result["warnings"].append(f"Missing description in dimension details for {dimension_name}")
        
        return validation_result
    
    def _validate_generation_guidelines(self, guidelines: Dict[str, Any]) -> Dict[str, Any]:
        """Validate generation guidelines"""
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check for recommended guideline sections
        recommended_sections = ["sentence_length", "paragraph_length", "vocabulary", "tone", "style"]
        for section in recommended_sections:
            if section not in guidelines:
                validation_result["warnings"].append(f"Missing guideline section: {section}")
        
        # Validate sentence length guidelines
        if "sentence_length" in guidelines:
            sentence_guidelines = guidelines["sentence_length"]
            if not isinstance(sentence_guidelines, dict):
                validation_result["warnings"].append("sentence_length guidelines should be a dictionary")
            elif "average" not in sentence_guidelines:
                validation_result["warnings"].append("Missing average in sentence_length guidelines")
        
        return validation_result
    
    def analyze_profile_performance(self, profile_data: Dict[str, Any], 
                                  sample_prompts: List[str] = None) -> Dict[str, Any]:
        """Analyze expected profile performance with test generation"""
        
        print(f"🔍 Analyzing performance for profile '{profile_data.get('name', 'unknown')}'...")
        
        if sample_prompts is None:
            sample_prompts = [
                "The importance of innovation in modern business",
                "How to implement effective team collaboration",
                "The future of artificial intelligence in society",
                "Strategies for sustainable business growth",
                "Building customer relationships in digital age"
            ]
        
        target_hrv = profile_data["target_hrv"]
        generated_results = []
        
        # Generate sample content
        for i, prompt in enumerate(sample_prompts):
            print(f"   Generating sample {i+1}/{len(sample_prompts)}...")
            
            try:
                content = self.writer.generate(prompt)
                actual_hrv = self.extractor.extract(content)
                
                # Calculate similarity to target
                similarity = self._calculate_cosine_similarity(target_hrv, actual_hrv)
                
                generated_results.append({
                    "prompt": prompt,
                    "content_length": len(content),
                    "target_hrv": target_hrv,
                    "actual_hrv": actual_hrv,
                    "similarity": similarity,
                    "content_preview": content[:100] + "..." if len(content) > 100 else content
                })
                
            except Exception as e:
                generated_results.append({
                    "prompt": prompt,
                    "error": str(e),
                    "similarity": 0.0
                })
        
        # Calculate performance metrics
        performance_analysis = self._calculate_performance_metrics(generated_results, target_hrv)
        
        return {
            "profile_name": profile_data.get("name", "unknown"),
            "target_hrv": target_hrv,
            "sample_results": generated_results,
            "performance_metrics": performance_analysis,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two HRV vectors"""
        
        vec1_array = np.array(vec1)
        vec2_array = np.array(vec2)
        
        # Handle emotional_valence range difference
        vec1_array[1] = (vec1_array[1] + 1) / 2  # Convert from [-1,1] to [0,1]
        vec2_array[1] = (vec2_array[1] + 1) / 2
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1_array, vec2_array)
        norm1 = np.linalg.norm(vec1_array)
        norm2 = np.linalg.norm(vec2_array)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _calculate_performance_metrics(self, results: List[Dict[str, Any]], 
                                     target_hrv: List[float]) -> Dict[str, Any]:
        """Calculate performance metrics from generation results"""
        
        successful_results = [r for r in results if "error" not in r]
        
        if not successful_results:
            return {
                "success_rate": 0.0,
                "average_similarity": 0.0,
                "similarity_std": 0.0,
                "dimension_achievements": {},
                "performance_grade": "F",
                "recommendations": ["Profile generation failed completely"]
            }
        
        similarities = [r["similarity"] for r in successful_results]
        
        # Calculate dimension-wise achievements
        dimension_achievements = {}
        for i, (dimension_name, _, _) in enumerate(self.dimensions):
            target_values = [r["target_hrv"][i] for r in successful_results]
            actual_values = [r["actual_hrv"][i] for r in successful_results]
            
            # Calculate mean absolute error for this dimension
            mae = np.mean([abs(t - a) for t, a in zip(target_values, actual_values)])
            achievement = max(0, 1 - mae)  # Convert error to achievement score
            
            dimension_achievements[dimension_name] = {
                "target_mean": np.mean(target_values),
                "actual_mean": np.mean(actual_values),
                "mae": mae,
                "achievement": achievement
            }
        
        # Overall performance metrics
        success_rate = len(successful_results) / len(results)
        average_similarity = np.mean(similarities)
        similarity_std = np.std(similarities)
        
        # Performance grading
        if average_similarity >= 0.9:
            grade = "A+"
        elif average_similarity >= 0.8:
            grade = "A"
        elif average_similarity >= 0.7:
            grade = "B"
        elif average_similarity >= 0.6:
            grade = "C"
        elif average_similarity >= 0.5:
            grade = "D"
        else:
            grade = "F"
        
        # Generate recommendations
        recommendations = self._generate_performance_recommendations(
            dimension_achievements, average_similarity, similarity_std
        )
        
        return {
            "success_rate": success_rate,
            "average_similarity": average_similarity,
            "similarity_std": similarity_std,
            "dimension_achievements": dimension_achievements,
            "performance_grade": grade,
            "recommendations": recommendations
        }
    
    def _generate_performance_recommendations(self, dimension_achievements: Dict[str, Any],
                                           avg_similarity: float, similarity_std: float) -> List[str]:
        """Generate performance improvement recommendations"""
        
        recommendations = []
        
        # Overall similarity recommendations
        if avg_similarity < 0.6:
            recommendations.append("Consider significant profile adjustment - low overall similarity")
        elif avg_similarity < 0.8:
            recommendations.append("Profile may need fine-tuning for better alignment")
        
        # Consistency recommendations
        if similarity_std > 0.2:
            recommendations.append("High variability in results - consider profile stabilization")
        
        # Dimension-specific recommendations
        low_achievements = [
            (dim, data["achievement"]) 
            for dim, data in dimension_achievements.items() 
            if data["achievement"] < 0.6
        ]
        
        if low_achievements:
            worst_dimension = min(low_achievements, key=lambda x: x[1])
            recommendations.append(f"Focus on improving {worst_dimension[0]} (achievement: {worst_dimension[1]:.2f})")
        
        # High-achieving dimensions
        high_achievements = [
            (dim, data["achievement"]) 
            for dim, data in dimension_achievements.items() 
            if data["achievement"] > 0.9
        ]
        
        if high_achievements:
            best_dimension = max(high_achievements, key=lambda x: x[1])
            recommendations.append(f"{best_dimension[0]} is well-optimized (achievement: {best_dimension[1]:.2f})")
        
        return recommendations
    
    def compare_profiles(self, profile1_data: Dict[str, Any], profile2_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two profiles comprehensively"""
        
        name1 = profile1_data.get("name", "Profile 1")
        name2 = profile2_data.get("name", "Profile 2")
        
        print(f"🔍 Comparing profiles '{name1}' and '{name2}'...")
        
        hrv1 = profile1_data["target_hrv"]
        hrv2 = profile2_data["target_hrv"]
        
        # Calculate similarity between profiles
        similarity = self._calculate_cosine_similarity(hrv1, hrv2)
        
        # Dimension-wise comparison
        dimension_comparison = {}
        for i, (dimension_name, description, _) in enumerate(self.dimensions):
            val1 = hrv1[i]
            val2 = hrv2[i]
            difference = val1 - val2
            
            dimension_comparison[dimension_name] = {
                "profile1_value": val1,
                "profile2_value": val2,
                "difference": difference,
                "similarity": 1 - abs(difference),  # Simple similarity metric
                "description": description
            }
        
        # Overall assessment
        if similarity > 0.9:
            relationship = "Very Similar"
        elif similarity > 0.7:
            relationship = "Similar"
        elif similarity > 0.5:
            relationship = "Moderately Different"
        else:
            relationship = "Very Different"
        
        # Find most and least similar dimensions
        dimension_similarities = [(dim, data["similarity"]) for dim, data in dimension_comparison.items()]
        most_similar = max(dimension_similarities, key=lambda x: x[1])
        least_similar = min(dimension_similarities, key=lambda x: x[1])
        
        return {
            "profile1_name": name1,
            "profile2_name": name2,
            "overall_similarity": similarity,
            "relationship": relationship,
            "dimension_comparison": dimension_comparison,
            "most_similar_dimension": most_similar,
            "least_similar_dimension": least_similar,
            "comparison_timestamp": datetime.now().isoformat()
        }
    
    def validate_profile_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a profile file from disk"""
        
        try:
            with open(file_path, 'r') as f:
                profile_data = json.load(f)
            
            validation_result = self.validate_profile_structure(profile_data)
            
            return {
                "file_path": file_path,
                "validation_result": validation_result,
                "profile_name": profile_data.get("name", "unknown"),
                "validation_timestamp": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            return {
                "file_path": file_path,
                "validation_result": {
                    "valid": False,
                    "errors": [f"Invalid JSON: {str(e)}"],
                    "warnings": [],
                    "info": []
                },
                "profile_name": "unknown",
                "validation_timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "file_path": file_path,
                "validation_result": {
                    "valid": False,
                    "errors": [f"File read error: {str(e)}"],
                    "warnings": [],
                    "info": []
                },
                "profile_name": "unknown",
                "validation_timestamp": datetime.now().isoformat()
            }


def main():
    """Command line interface for profile validator"""
    
    parser = argparse.ArgumentParser(description="HRV Profile Validator")
    parser.add_argument("--action", choices=["validate", "analyze", "compare", "batch_validate"], 
                       required=True, help="Action to perform")
    parser.add_argument("--tenant", default="default", help="Tenant name")
    parser.add_argument("--profile", help="Profile name")
    parser.add_argument("--profile1", help="First profile for comparison")
    parser.add_argument("--profile2", help="Second profile for comparison")
    parser.add_argument("--file", help="Profile file path")
    parser.add_argument("--directory", help="Directory for batch validation")
    parser.add_argument("--samples", type=int, default=5, help="Number of sample prompts for analysis")
    
    args = parser.parse_args()
    
    validator = HRVProfileValidator()
    
    if args.action == "validate":
        if args.file:
            # Validate specific file
            result = validator.validate_profile_file(args.file)
            
            print(f"📋 Validation result for: {result['file_path']}")
            print(f"   Profile: {result['profile_name']}")
            print(f"   Valid: {result['validation_result']['valid']}")
            
            if result['validation_result']['errors']:
                print("   Errors:")
                for error in result['validation_result']['errors']:
                    print(f"     - {error}")
            
            if result['validation_result']['warnings']:
                print("   Warnings:")
                for warning in result['validation_result']['warnings']:
                    print(f"     - {warning}")
        
        elif args.profile:
            # Load and validate profile
            profile_path = Path(validator.profiles_dir) / args.tenant / f"{args.profile}.json"
            result = validator.validate_profile_file(str(profile_path))
            
            if result['validation_result']['valid']:
                print(f"✅ Profile '{args.profile}' is valid")
            else:
                print(f"❌ Profile '{args.profile}' has validation errors:")
                for error in result['validation_result']['errors']:
                    print(f"   - {error}")
        else:
            print("❌ Either --file or --profile required for validation")
    
    elif args.action == "analyze":
        if not args.profile:
            print("❌ --profile required for analysis")
            return
        
        # Load profile
        profile_path = Path(validator.profiles_dir) / args.tenant / f"{args.profile}.json"
        
        if not profile_path.exists():
            print(f"❌ Profile not found: {profile_path}")
            return
        
        with open(profile_path, 'r') as f:
            profile_data = json.load(f)
        
        # Analyze performance
        analysis = validator.analyze_profile_performance(profile_data)
        
        print(f"📊 Performance Analysis for '{analysis['profile_name']}'")
        print(f"   Success Rate: {analysis['performance_metrics']['success_rate']:.1%}")
        print(f"   Average Similarity: {analysis['performance_metrics']['average_similarity']:.3f}")
        print(f"   Performance Grade: {analysis['performance_metrics']['performance_grade']}")
        
        if analysis['performance_metrics']['recommendations']:
            print("   Recommendations:")
            for rec in analysis['performance_metrics']['recommendations']:
                print(f"     - {rec}")
    
    elif args.action == "compare":
        if not args.profile1 or not args.profile2:
            print("❌ Both --profile1 and --profile2 required for comparison")
            return
        
        # Load profiles
        profile1_path = Path(validator.profiles_dir) / args.tenant / f"{args.profile1}.json"
        profile2_path = Path(validator.profiles_dir) / args.tenant / f"{args.profile2}.json"
        
        if not profile1_path.exists() or not profile2_path.exists():
            print("❌ One or both profiles not found")
            return
        
        with open(profile1_path, 'r') as f:
            profile1_data = json.load(f)
        
        with open(profile2_path, 'r') as f:
            profile2_data = json.load(f)
        
        # Compare profiles
        comparison = validator.compare_profiles(profile1_data, profile2_data)
        
        print(f"🔍 Profile Comparison")
        print(f"   {comparison['profile1_name']} vs {comparison['profile2_name']}")
        print(f"   Overall Similarity: {comparison['overall_similarity']:.3f}")
        print(f"   Relationship: {comparison['relationship']}")
        print(f"   Most Similar: {comparison['most_similar_dimension'][0]} ({comparison['most_similar_dimension'][1]:.3f})")
        print(f"   Least Similar: {comparison['least_similar_dimension'][0]} ({comparison['least_similar_dimension'][1]:.3f})")
    
    elif args.action == "batch_validate":
        if not args.directory:
            print("❌ --directory required for batch validation")
            return
        
        directory_path = Path(args.directory)
        if not directory_path.exists():
            print(f"❌ Directory not found: {directory_path}")
            return
        
        # Find all JSON files
        json_files = list(directory_path.glob("*.json"))
        
        if not json_files:
            print(f"❌ No JSON files found in {directory_path}")
            return
        
        print(f"📋 Batch validating {len(json_files)} files...")
        
        valid_count = 0
        invalid_count = 0
        
        for file_path in json_files:
            result = validator.validate_profile_file(str(file_path))
            
            if result['validation_result']['valid']:
                valid_count += 1
                print(f"✅ {file_path.name}")
            else:
                invalid_count += 1
                print(f"❌ {file_path.name} - {len(result['validation_result']['errors'])} errors")
        
        print(f"\n📊 Batch Validation Results:")
        print(f"   Valid: {valid_count}")
        print(f"   Invalid: {invalid_count}")
        print(f"   Success Rate: {valid_count/len(json_files):.1%}")


if __name__ == "__main__":
    main()
