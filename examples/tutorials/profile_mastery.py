#!/usr/bin/env python3
"""
Profile Mastery Tutorial

This advanced tutorial covers comprehensive HRV profile management,
including creation, optimization, analysis, and advanced techniques.
"""

import sys
import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.api.hr_server import SimpleRequest, hr_generate


class ProfileMaster:
    """Advanced profile management and optimization"""
    
    def __init__(self):
        self.writer = HumanResonantWriter()
        self.extractor = HRVExtractor()
        
        # Initialize profile manager
        profiles_dir = project_root / "data" / "profiles" / "hr_profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)
        self.manager = HRVProfileManager(str(profiles_dir))
        
        # HRV dimension names
        self.dimensions = [
            "sentence_variance", "emotional_valence", "emotional_intensity",
            "assertiveness_index", "curiosity_index", "metaphor_density",
            "storytelling_index", "active_voice_ratio"
        ]
    
    def understand_hrv_dimensions(self):
        """Deep dive into HRV dimensions"""
        print("🧠 Deep Dive: Understanding HRV Dimensions")
        print("=" * 60)
        print()
        
        dimension_details = {
            "sentence_variance": {
                "range": "0.0-1.0",
                "description": "Variety in sentence lengths and structures",
                "low": "Monotonous, repetitive sentence patterns",
                "high": "Diverse, engaging sentence structures",
                "impact": "Readability and engagement"
            },
            "emotional_valence": {
                "range": "-1.0 to 1.0",
                "description": "Positive/negative sentiment balance",
                "low": "Negative or neutral tone",
                "high": "Positive, optimistic tone",
                "impact": "Reader emotional response"
            },
            "emotional_intensity": {
                "range": "0.0-1.0",
                "description": "Strength of emotional content",
                "low": "Reserved, understated emotion",
                "high": "Passionate, intense emotion",
                "impact": "Emotional engagement"
            },
            "assertiveness_index": {
                "range": "0.0-1.0",
                "description": "Confidence and directness",
                "low": "Hesitant, passive language",
                "high": "Confident, direct statements",
                "impact": "Authority and credibility"
            },
            "curiosity_index": {
                "range": "0.0-1.0",
                "description": "Question and curiosity elements",
                "low": "Declarative, factual content",
                "high": "Inquisitive, thought-provoking",
                "impact": "Reader engagement and interest"
            },
            "metaphor_density": {
                "range": "0.0-1.0",
                "description": "Metaphorical language usage",
                "low": "Literal, straightforward language",
                "high": "Rich, metaphorical expressions",
                "impact": "Creativity and memorability"
            },
            "storytelling_index": {
                "range": "0.0-1.0",
                "description": "Narrative and storytelling elements",
                "low": "Informational, factual content",
                "high": "Story-driven, narrative content",
                "impact": "Narrative engagement"
            },
            "active_voice_ratio": {
                "range": "0.0-1.0",
                "description": "Active vs passive voice usage",
                "low": "Passive voice dominant",
                "high": "Active voice dominant",
                "impact": "Clarity and directness"
            }
        }
        
        for dim_name, details in dimension_details.items():
            print(f"📊 {dim_name.replace('_', ' ').title()}")
            print(f"   Range: {details['range']}")
            print(f"   Description: {details['description']}")
            print(f"   Low Value: {details['low']}")
            print(f"   High Value: {details['high']}")
            print(f"   Impact: {details['impact']}")
            print()
    
    def create_specialized_profiles(self):
        """Create specialized profiles for different use cases"""
        print("🎨 Creating Specialized Profiles")
        print("=" * 60)
        print()
        
        tenant = "profile_mastery"
        specialized_profiles = []
        
        # Profile definitions
        profile_definitions = [
            {
                "name": "executive_leadership",
                "description": "Authoritative, inspiring leadership communication",
                "hrv_vector": [0.4, 0.3, 0.6, 0.9, 0.3, 0.2, 0.4, 0.85],
                "use_cases": ["executive_communications", "leadership_messages", "vision_statements"]
            },
            {
                "name": "empathetic_support",
                "description": "Caring, supportive customer service tone",
                "hrv_vector": [0.5, 0.7, 0.8, 0.2, 0.6, 0.3, 0.5, 0.7],
                "use_cases": ["customer_support", "help_desk", "user_guidance"]
            },
            {
                "name": "academic_research",
                "description": "Formal, precise academic writing",
                "hrv_vector": [0.3, 0.1, 0.2, 0.8, 0.4, 0.1, 0.2, 0.9],
                "use_cases": ["research_papers", "academic_articles", "theses"]
            },
            {
                "name": "creative_branding",
                "description": "Innovative, engaging brand storytelling",
                "hrv_vector": [0.8, 0.6, 0.9, 0.5, 0.8, 0.7, 0.9, 0.6],
                "use_cases": ["brand_stories", "marketing_content", "creative_campaigns"]
            },
            {
                "name": "technical_instruction",
                "description": "Clear, precise technical documentation",
                "hrv_vector": [0.4, 0.0, 0.3, 0.7, 0.5, 0.2, 0.3, 0.8],
                "use_cases": ["technical_manuals", "user_guides", "documentation"]
            }
        ]
        
        for profile_def in profile_definitions:
            print(f"🎯 Creating: {profile_def['name']}")
            print(f"   Description: {profile_def['description']}")
            print(f"   HRV Vector: {[round(x, 3) for x in profile_def['hrv_vector']]}")
            print(f"   Use Cases: {', '.join(profile_def['use_cases'])}")
            print()
            
            try:
                # Save profile
                self.manager.save_profile(tenant, profile_def['name'], profile_def['hrv_vector'])
                specialized_profiles.append(profile_def['name'])
                print(f"✅ Profile saved successfully")
                print()
            except Exception as e:
                print(f"❌ Error saving profile: {e}")
                print()
        
        return specialized_profiles
    
    def analyze_profile_effectiveness(self, profile_name: str, test_prompts: List[str]) -> Dict[str, Any]:
        """Analyze profile effectiveness with test content"""
        print(f"🔍 Analyzing Profile: {profile_name}")
        print("=" * 50)
        print()
        
        results = []
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"Test {i}/{len(test_prompts)}: {prompt[:50]}...")
            
            try:
                # Generate content with profile
                request = SimpleRequest(prompt=prompt, profile_name=profile_name)
                response = hr_generate(request)
                
                content = response.article
                hrv_vector = self.extractor.extract(content)
                
                # Calculate metrics
                avg_score = sum(hrv_vector) / len(hrv_vector)
                content_length = len(content)
                
                # Calculate alignment with target profile
                target_hrv = self.manager.load_profile("profile_mastery", profile_name)
                alignment_score = self.calculate_profile_alignment(hrv_vector, target_hrv)
                
                result = {
                    "prompt": prompt,
                    "content_length": content_length,
                    "hrv_vector": hrv_vector,
                    "avg_score": avg_score,
                    "alignment_score": alignment_score,
                    "success": True
                }
                
                results.append(result)
                
                print(f"✅ Generated {content_length} chars, HRV: {avg_score:.3f}, Alignment: {alignment_score:.3f}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({
                    "prompt": prompt,
                    "error": str(e),
                    "success": False
                })
        
        # Calculate overall effectiveness
        successful_results = [r for r in results if r.get("success")]
        
        if successful_results:
            avg_score = sum(r["avg_score"] for r in successful_results) / len(successful_results)
            avg_alignment = sum(r["alignment_score"] for r in successful_results) / len(successful_results)
            avg_length = sum(r["content_length"] for r in successful_results) / len(successful_results)
            
            effectiveness = {
                "profile_name": profile_name,
                "total_tests": len(test_prompts),
                "successful_tests": len(successful_results),
                "success_rate": len(successful_results) / len(test_prompts),
                "avg_hrv_score": avg_score,
                "avg_alignment_score": avg_alignment,
                "avg_content_length": avg_length,
                "effectiveness_grade": self.calculate_effectiveness_grade(avg_score, avg_alignment)
            }
            
            print(f"\n📊 Profile Effectiveness Analysis:")
            print(f"   Success Rate: {effectiveness['success_rate']:.1%}")
            print(f"   Avg HRV Score: {effectiveness['avg_hrv_score']:.3f}")
            print(f"   Avg Alignment: {effectiveness['avg_alignment_score']:.3f}")
            print(f"   Avg Length: {effectiveness['avg_content_length']:.0f} chars")
            print(f"   Effectiveness Grade: {effectiveness['effectiveness_grade']}")
            
            return effectiveness
        else:
            print("❌ No successful tests")
            return {"error": "All tests failed"}
    
    def calculate_profile_alignment(self, generated_hrv: List[float], target_hrv: List[float]) -> float:
        """Calculate alignment between generated and target HRV vectors"""
        if len(generated_hrv) != len(target_hrv):
            return 0.0
        
        # Calculate cosine similarity
        dot_product = sum(g * t for g, t in zip(generated_hrv, target_hrv))
        norm_generated = sum(g ** 2 for g in generated_hrv) ** 0.5
        norm_target = sum(t ** 2 for t in target_hrv) ** 0.5
        
        if norm_generated == 0 or norm_target == 0:
            return 0.0
        
        return dot_product / (norm_generated * norm_target)
    
    def calculate_effectiveness_grade(self, avg_score: float, alignment_score: float) -> str:
        """Calculate overall effectiveness grade"""
        combined_score = (avg_score + alignment_score) / 2
        
        if combined_score > 0.85:
            return "A+ (Excellent)"
        elif combined_score > 0.75:
            return "A (Very Good)"
        elif combined_score > 0.65:
            return "B (Good)"
        elif combined_score > 0.55:
            return "C (Fair)"
        else:
            return "D (Needs Improvement)"
    
    def optimize_profile_vector(self, profile_name: str, target_improvements: Dict[str, float]) -> List[float]:
        """Optimize HRV vector based on target improvements"""
        print(f"⚙️ Optimizing Profile: {profile_name}")
        print("=" * 50)
        print()
        
        # Load current profile
        current_hrv = self.manager.load_profile("profile_mastery", profile_name)
        
        print(f"Current HRV Vector: {[round(x, 3) for x in current_hrv]}")
        print(f"Target Improvements: {target_improvements}")
        print()
        
        # Apply optimizations
        optimized_hrv = current_hrv.copy()
        
        for dimension, adjustment in target_improvements.items():
            if dimension in self.dimensions:
                dim_index = self.dimensions.index(dimension)
                current_value = optimized_hrv[dim_index]
                new_value = max(0.0, min(1.0, current_value + adjustment))
                optimized_hrv[dim_index] = new_value
                
                print(f"   {dimension}: {current_value:.3f} → {new_value:.3f} ({adjustment:+.2f})")
        
        print(f"\nOptimized HRV Vector: {[round(x, 3) for x in optimized_hrv]}")
        
        # Save optimized profile
        optimized_name = f"{profile_name}_optimized"
        self.manager.save_profile("profile_mastery", optimized_name, optimized_hrv)
        
        print(f"✅ Optimized profile saved as: {optimized_name}")
        
        return optimized_hrv
    
    def compare_profiles(self, profile_names: List[str]) -> Dict[str, Any]:
        """Compare multiple profiles"""
        print("📊 Profile Comparison Analysis")
        print("=" * 60)
        print()
        
        profiles_data = {}
        
        for profile_name in profile_names:
            try:
                hrv_vector = self.manager.load_profile("profile_mastery", profile_name)
                profiles_data[profile_name] = hrv_vector
            except Exception as e:
                print(f"❌ Error loading {profile_name}: {e}")
        
        if len(profiles_data) < 2:
            print("❌ Need at least 2 profiles for comparison")
            return {}
        
        # Create comparison matrix
        print("📈 Comparison Matrix:")
        print("-" * 50)
        
        # Header
        header = f"{'Profile':<20}"
        for profile_name in profiles_data.keys():
            header += f"{profile_name:<15}"
        print(header)
        print("-" * len(header))
        
        # Similarity scores
        for profile1_name, hrv1 in profiles_data.items():
            row = f"{profile1_name:<20}"
            for profile2_name, hrv2 in profiles_data.items():
                similarity = self.calculate_profile_alignment(hrv1, hrv2)
                row += f"{similarity:<15.3f}"
            print(row)
        
        # Dimension analysis
        print(f"\n📐 Dimension Analysis:")
        print("-" * 30)
        
        for i, dimension in enumerate(self.dimensions):
            print(f"\n{dimension.replace('_', ' ').title()}:")
            for profile_name, hrv_vector in profiles_data.items():
                value = hrv_vector[i]
                indicator = "🔴" if value < 0.3 else "🟡" if value < 0.7 else "🟢"
                print(f"  {indicator} {profile_name:<20}: {value:.3f}")
        
        return profiles_data
    
    def create_adaptive_profiles(self):
        """Create adaptive profiles for different contexts"""
        print("🔨 Creating Adaptive Profiles")
        print("=" * 60)
        print()
        
        base_profiles = {
            "professional_base": [0.5, 0.2, 0.4, 0.6, 0.4, 0.3, 0.3, 0.7],
            "creative_base": [0.7, 0.6, 0.8, 0.4, 0.7, 0.6, 0.8, 0.6]
        }
        
        adaptive_scenarios = [
            {
                "name": "professional_formal",
                "base": "professional_base",
                "context": "Formal business communication",
                "adjustments": {
                    "emotional_valence": -0.1,
                    "assertiveness_index": 0.2,
                    "active_voice_ratio": 0.1
                }
            },
            {
                "name": "professional_casual",
                "base": "professional_base",
                "context": "Casual team communication",
                "adjustments": {
                    "emotional_valence": 0.2,
                    "curiosity_index": 0.2,
                    "storytelling_index": 0.1
                }
            },
            {
                "name": "creative_marketing",
                "base": "creative_base",
                "context": "Marketing content",
                "adjustments": {
                    "emotional_valence": 0.2,
                    "assertiveness_index": 0.1,
                    "metaphor_density": 0.1
                }
            },
            {
                "name": "creative_educational",
                "base": "creative_base",
                "context": "Educational content",
                "adjustments": {
                    "curiosity_index": 0.2,
                    "storytelling_index": -0.1,
                    "active_voice_ratio": 0.1
                }
            }
        ]
        
        tenant = "profile_mastery"
        created_profiles = []
        
        for scenario in adaptive_scenarios:
            print(f"🎯 Creating: {scenario['name']}")
            print(f"   Context: {scenario['context']}")
            print(f"   Base Profile: {scenario['base']}")
            print(f"   Adjustments: {scenario['adjustments']}")
            
            # Apply adjustments
            base_hrv = base_profiles[scenario['base']]
            adaptive_hrv = base_hrv.copy()
            
            for dimension, adjustment in scenario['adjustments'].items():
                if dimension in self.dimensions:
                    dim_index = self.dimensions.index(dimension)
                    current_value = adaptive_hrv[dim_index]
                    new_value = max(0.0, min(1.0, current_value + adjustment))
                    adaptive_hrv[dim_index] = new_value
            
            print(f"   Resulting HRV: {[round(x, 3) for x in adaptive_hrv]}")
            print()
            
            try:
                # Save adaptive profile
                self.manager.save_profile(tenant, scenario['name'], adaptive_hrv)
                created_profiles.append(scenario['name'])
                print(f"✅ Adaptive profile saved")
                print()
            except Exception as e:
                print(f"❌ Error saving adaptive profile: {e}")
                print()
        
        return created_profiles
    
    def profile_performance_benchmarking(self):
        """Benchmark profile performance"""
        print("🏆 Profile Performance Benchmarking")
        print("=" * 60)
        print()
        
        # Test prompts for benchmarking
        benchmark_prompts = [
            "The importance of innovation in business",
            "Building effective teams for success",
            "Digital transformation strategies",
            "Customer experience optimization",
            "Sustainable business practices"
        ]
        
        # Profiles to benchmark
        benchmark_profiles = [
            "neutral_professional",
            "creative_storytelling",
            "executive_leadership",
            "empathetic_support",
            "professional_formal"
        ]
        
        benchmark_results = {}
        
        for profile_name in benchmark_profiles:
            print(f"🏃 Benchmarking: {profile_name}")
            print("-" * 40)
            
            try:
                effectiveness = self.analyze_profile_effectiveness(profile_name, benchmark_prompts)
                benchmark_results[profile_name] = effectiveness
                print(f"   Grade: {effectiveness.get('effectiveness_grade', 'N/A')}")
                print(f"   Success Rate: {effectiveness.get('success_rate', 0):.1%}")
                print()
            except Exception as e:
                print(f"❌ Error benchmarking {profile_name}: {e}")
                print()
        
        # Rank profiles by performance
        if benchmark_results:
            print("🏆 Performance Rankings:")
            print("-" * 30)
            
            sorted_profiles = sorted(
                [(name, data) for name, data in benchmark_results.items() if 'avg_hrv_score' in data],
                key=lambda x: x[1]['avg_hrv_score'],
                reverse=True
            )
            
            for rank, (profile_name, data) in enumerate(sorted_profiles, 1):
                print(f"{rank}. {profile_name:<25} - {data['effectiveness_grade']} ({data['avg_hrv_score']:.3f})")
            
            return benchmark_results
        
        return {}
    
    def profile_recommendations(self) -> List[str]:
        """Generate profile recommendations based on use cases"""
        print("💡 Profile Recommendations")
        print("=" * 50)
        print()
        
        recommendations = [
            {
                "use_case": "Business Reports",
                "recommended_profiles": ["professional_business", "executive_leadership", "professional_formal"],
                "reasoning": "These profiles provide the formal, authoritative tone needed for business reports"
            },
            {
                "use_case": "Marketing Content",
                "recommended_profiles": ["marketing_enthusiastic", "creative_branding", "creative_storytelling"],
                "reasoning": "These profiles offer the engaging, persuasive tone for marketing materials"
            },
            {
                "use_case": "Customer Support",
                "recommended_profiles": ["empathetic_support", "neutral_professional"],
                "reasoning": "These profiles provide the caring, helpful tone for customer interactions"
            },
            {
                "use_case": "Technical Documentation",
                "recommended_profiles": ["technical_academic", "technical_instruction", "professional_business"],
                "reasoning": "These profiles ensure clarity, precision, and formal tone for technical content"
            },
            {
                "use_case": "Creative Writing",
                "recommended_profiles": ["creative_storytelling", "creative_branding"],
                "reasoning": "These profiles enhance creativity, storytelling, and engagement"
            },
            {
                "use_case": "Educational Content",
                "recommended_profiles": ["educational_tutorial", "empathetic_support", "creative_storytelling"],
                "reasoning": "These profiles balance clarity with engagement for learning materials"
            }
        ]
        
        for rec in recommendations:
            print(f"📚 {rec['use_case']}:")
            print(f"   Recommended: {', '.join(rec['recommended_profiles'])}")
            print(f"   Reasoning: {rec['reasoning']}")
            print()
        
        return [rec['recommended_profiles'] for rec in recommendations]


def main():
    """Run the profile mastery tutorial"""
    print("🎯 ResonanceOS v6 - Profile Mastery Tutorial")
    print("=" * 60)
    print("This advanced tutorial covers comprehensive HRV profile management.")
    print("You'll learn how to:")
    print("- Deep understanding of HRV dimensions")
    print("- Create specialized profiles")
    print("- Analyze profile effectiveness")
    print("- Optimize profile vectors")
    print("- Compare and benchmark profiles")
    print("- Create adaptive profiles")
    print("- Get profile recommendations")
    print()
    
    try:
        master = ProfileMaster()
        
        # Run tutorial sections
        master.understand_hrv_dimensions()
        specialized_profiles = master.create_specialized_profiles()
        
        if specialized_profiles:
            # Test one specialized profile
            test_prompts = [
                "The future of workplace collaboration",
                "Innovative approaches to problem solving",
                "Building sustainable business models"
            ]
            
            effectiveness = master.analyze_profile_effectiveness(
                specialized_profiles[0], 
                test_prompts
            )
            
            # Optimize the profile
            optimizations = {
                "storytelling_index": 0.1,
                "curiosity_index": 0.1,
                "metaphor_density": 0.05
            }
            
            master.optimize_profile_vector(specialized_profiles[0], optimizations)
        
        # Compare profiles
        comparison_profiles = ["neutral_professional", "creative_storytelling"]
        if len(specialized_profiles) >= 2:
            comparison_profiles.extend(specialized_profiles[:2])
        
        master.compare_profiles(comparison_profiles)
        
        # Create adaptive profiles
        adaptive_profiles = master.create_adaptive_profiles()
        
        # Benchmark performance
        master.profile_performance_benchmarking()
        
        # Get recommendations
        master.profile_recommendations()
        
        print("\n🎉 Profile Mastery Tutorial Completed!")
        print("\nKey Achievements:")
        print("- ✅ Deep understanding of HRV dimensions")
        print("- ✅ Created specialized profiles")
        print("- ✅ Analyzed profile effectiveness")
        print("- ✅ Optimized profile vectors")
        print("- ✅ Compared multiple profiles")
        print("- ✅ Created adaptive profiles")
        print("- ✅ Benchmarked performance")
        print("- ✅ Got personalized recommendations")
        print("\nYou're now a profile master! 🎨🏆")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Tutorial interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")


if __name__ == "__main__":
    main()
