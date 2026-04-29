#!/usr/bin/env python3
"""
Profile Generator for ResonanceOS v6

This script creates and manages HRV profiles for different writing styles,
brands, and use cases.
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import argparse
import random

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager


class ProfileGenerator:
    """Profile generation and management utility"""
    
    def __init__(self, profiles_dir: str = None):
        """Initialize the profile generator"""
        if profiles_dir:
            self.profiles_dir = Path(profiles_dir)
        else:
            self.profiles_dir = Path("./profiles/hr_profiles")
        
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.manager = HRVProfileManager(self.profiles_dir)
        
        # Load dimension names
        self.dimensions = [
            'sentence_variance',
            'emotional_valence',
            'emotional_intensity',
            'assertiveness_index',
            'curiosity_index',
            'metaphor_density',
            'storytelling_index',
            'active_voice_ratio'
        ]
    
    def create_profile_from_vector(self, name: str, description: str, hrv_vector: List[float], 
                                  metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a profile from HRV vector"""
        if len(hrv_vector) != 8:
            raise ValueError("HRV vector must have exactly 8 dimensions")
        
        profile = {
            'name': name,
            'description': description,
            'hrv_vector': hrv_vector,
            'metadata': {
                'created_at': '2026-03-09T00:00:00Z',
                'updated_at': '2026-03-09T00:00:00Z',
                'version': '1.0',
                'created_by': 'ProfileGenerator'
            }
        }
        
        if metadata:
            profile['metadata'].update(metadata)
        
        return profile
    
    def generate_adaptive_profile(self, base_profile: Dict[str, Any], adjustments: Dict[str, float]) -> Dict[str, Any]:
        """Generate an adapted profile based on adjustments"""
        base_vector = base_profile['hrv_vector']
        adapted_vector = []
        
        for i, dimension in enumerate(self.dimensions):
            base_value = base_vector[i]
            adjustment = adjustments.get(dimension, 0.0)
            new_value = max(0.0, min(1.0, base_value + adjustment))
            adapted_vector.append(new_value)
        
        adapted_profile = base_profile.copy()
        adapted_profile['hrv_vector'] = adapted_vector
        adapted_profile['metadata']['updated_at'] = '2026-03-09T00:00:00Z'
        adapted_profile['metadata']['version'] = str(float(adapted_profile['metadata']['version']) + 0.1)
        
        if 'adapted_from' not in adapted_profile['metadata']:
            adapted_profile['metadata']['adapted_from'] = base_profile['name']
        
        return adapted_profile
    
    def blend_profiles(self, profile1: Dict[str, Any], profile2: Dict[str, Any], 
                      weight1: float = 0.5, weight2: float = 0.5) -> Dict[str, Any]:
        """Blend two profiles with specified weights"""
        if abs(weight1 + weight2 - 1.0) > 0.001:
            raise ValueError("Weights must sum to 1.0")
        
        vector1 = profile1['hrv_vector']
        vector2 = profile2['hrv_vector']
        
        blended_vector = [
            weight1 * v1 + weight2 * v2 
            for v1, v2 in zip(vector1, vector2)
        ]
        
        blended_profile = {
            'name': f"Blend_{profile1['name']}_and_{profile2['name']}",
            'description': f"Blend of {profile1['name']} ({weight1:.1f}) and {profile2['name']} ({weight2:.1f})",
            'hrv_vector': blended_vector,
            'metadata': {
                'created_at': '2026-03-09T00:00:00Z',
                'version': '1.0',
                'created_by': 'ProfileGenerator',
                'source_profiles': [profile1['name'], profile2['name']],
                'blend_weights': {'weight1': weight1, 'weight2': weight2}
            }
        }
        
        return blended_profile
    
    def generate_random_profile(self, name: str, description: str = "", 
                               constraints: Dict[str, Tuple[float, float]] = None) -> Dict[str, Any]:
        """Generate a random profile within constraints"""
        vector = []
        
        for i, dimension in enumerate(self.dimensions):
            if constraints and dimension in constraints:
                min_val, max_val = constraints[dimension]
                value = random.uniform(min_val, max_val)
            else:
                value = random.uniform(0.0, 1.0)
            vector.append(value)
        
        if not description:
            description = f"Randomly generated profile for {name}"
        
        return self.create_profile_from_vector(name, description, vector)
    
    def save_profile(self, tenant: str, profile_name: str, profile: Dict[str, Any]):
        """Save profile to storage"""
        self.manager.save_profile(tenant, profile_name, profile['hrv_vector'])
        
        # Save full profile metadata
        profile_dir = self.profiles_dir / tenant / "metadata"
        profile_dir.mkdir(parents=True, exist_ok=True)
        
        metadata_file = profile_dir / f"{profile_name}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
    
    def load_profile(self, tenant: str, profile_name: str) -> Dict[str, Any]:
        """Load profile with metadata"""
        # Load HRV vector
        hrv_vector = self.manager.load_profile(tenant, profile_name)
        
        # Load metadata
        metadata_file = self.profiles_dir / tenant / "metadata" / f"{profile_name}.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                profile = json.load(f)
        else:
            # Create basic profile if metadata doesn't exist
            profile = {
                'name': profile_name,
                'description': f'Profile for {tenant}/{profile_name}',
                'hrv_vector': hrv_vector,
                'metadata': {
                    'created_at': '2026-03-09T00:00:00Z',
                    'version': '1.0'
                }
            }
        
        return profile
    
    def list_profiles(self, tenant: str) -> List[str]:
        """List all profiles for a tenant"""
        return self.manager.list_profiles(tenant)
    
    def analyze_profile_differences(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze differences between two profiles"""
        vector1 = profile1['hrv_vector']
        vector2 = profile2['hrv_vector']
        
        differences = []
        total_difference = 0.0
        
        for i, dimension in enumerate(self.dimensions):
            diff = abs(vector1[i] - vector2[i])
            differences.append({
                'dimension': dimension,
                'profile1_value': vector1[i],
                'profile2_value': vector2[i],
                'difference': diff
            })
            total_difference += diff
        
        # Sort by difference (most different first)
        differences.sort(key=lambda x: x['difference'], reverse=True)
        
        return {
            'profile1_name': profile1['name'],
            'profile2_name': profile2['name'],
            'total_difference': total_difference,
            'average_difference': total_difference / 8,
            'dimension_differences': differences,
            'similarity_score': max(0.0, 1.0 - total_difference / 8)
        }
    
    def export_profile_batch(self, tenant: str, output_file: str):
        """Export all profiles for a tenant"""
        profiles = {}
        profile_names = self.list_profiles(tenant)
        
        for profile_name in profile_names:
            profile = self.load_profile(tenant, profile_name)
            profiles[profile_name] = profile
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
    
    def import_profile_batch(self, tenant: str, input_file: str):
        """Import profiles from file"""
        with open(input_file, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        
        for profile_name, profile in profiles.items():
            self.save_profile(tenant, profile_name, profile)


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='ResonanceOS Profile Generator')
    parser.add_argument('command', choices=['create', 'blend', 'adapt', 'random', 'list', 'analyze', 'export', 'import'], 
                       help='Command to execute')
    parser.add_argument('--tenant', required=True, help='Tenant name')
    parser.add_argument('--name', help='Profile name')
    parser.add_argument('--description', help='Profile description')
    parser.add_argument('--vector', help='HRV vector (comma-separated values)')
    parser.add_argument('--profile1', help='First profile name for blend/analyze')
    parser.add_argument('--profile2', help='Second profile name for blend/analyze')
    parser.add_argument('--weight1', type=float, default=0.5, help='Weight for first profile in blend')
    parser.add_argument('--weight2', type=float, default=0.5, help='Weight for second profile in blend')
    parser.add_argument('--adjustments', help='Adjustments for adapt (dimension:value,dimension:value)')
    parser.add_argument('--constraints', help='Constraints for random (dimension:min:max,dimension:min:max)')
    parser.add_argument('--input', help='Input file for import/export')
    parser.add_argument('--output', help='Output file for export')
    parser.add_argument('--profiles-dir', help='Profiles directory path')
    
    args = parser.parse_args()
    
    generator = ProfileGenerator(args.profiles_dir)
    
    try:
        if args.command == 'create':
            if not args.name or not args.vector:
                print("Error: --name and --vector required for create command")
                return 1
            
            vector = [float(x.strip()) for x in args.vector.split(',')]
            description = args.description or f"Profile for {args.name}"
            
            profile = generator.create_profile_from_vector(args.name, description, vector)
            generator.save_profile(args.tenant, args.name, profile)
            print(f"Profile '{args.name}' created for tenant '{args.tenant}'")
        
        elif args.command == 'blend':
            if not args.profile1 or not args.profile2:
                print("Error: --profile1 and --profile2 required for blend command")
                return 1
            
            profile1 = generator.load_profile(args.tenant, args.profile1)
            profile2 = generator.load_profile(args.tenant, args.profile2)
            
            blended = generator.blend_profiles(profile1, profile2, args.weight1, args.weight2)
            generator.save_profile(args.tenant, blended['name'], blended)
            print(f"Blended profile '{blended['name']}' created")
        
        elif args.command == 'adapt':
            if not args.name or not args.profile1 or not args.adjustments:
                print("Error: --name, --profile1, and --adjustments required for adapt command")
                return 1
            
            base_profile = generator.load_profile(args.tenant, args.profile1)
            adjustments = {}
            for adj in args.adjustments.split(','):
                dim, val = adj.split(':')
                adjustments[dim.strip()] = float(val.strip())
            
            adapted = generator.generate_adaptive_profile(base_profile, adjustments)
            generator.save_profile(args.tenant, args.name, adapted)
            print(f"Adapted profile '{args.name}' created from '{args.profile1}'")
        
        elif args.command == 'random':
            if not args.name:
                print("Error: --name required for random command")
                return 1
            
            constraints = {}
            if args.constraints:
                for constraint in args.constraints.split(','):
                    dim, range_str = constraint.split(':')
                    min_val, max_val = range_str.split('-')
                    constraints[dim.strip()] = (float(min_val.strip()), float(max_val.strip()))
            
            profile = generator.generate_random_profile(args.name, args.description, constraints)
            generator.save_profile(args.tenant, args.name, profile)
            print(f"Random profile '{args.name}' created")
        
        elif args.command == 'list':
            profiles = generator.list_profiles(args.tenant)
            print(f"Profiles for tenant '{args.tenant}':")
            for profile_name in profiles:
                print(f"  - {profile_name}")
        
        elif args.command == 'analyze':
            if not args.profile1 or not args.profile2:
                print("Error: --profile1 and --profile2 required for analyze command")
                return 1
            
            profile1 = generator.load_profile(args.tenant, args.profile1)
            profile2 = generator.load_profile(args.tenant, args.profile2)
            
            analysis = generator.analyze_profile_differences(profile1, profile2)
            print(json.dumps(analysis, indent=2))
        
        elif args.command == 'export':
            output_file = args.output or f"{args.tenant}_profiles.json"
            generator.export_profile_batch(args.tenant, output_file)
            print(f"Profiles exported to {output_file}")
        
        elif args.command == 'import':
            if not args.input:
                print("Error: --input required for import command")
                return 1
            
            generator.import_profile_batch(args.tenant, args.input)
            print(f"Profiles imported from {args.input}")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
