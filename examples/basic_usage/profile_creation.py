#!/usr/bin/env python3
"""
HRV Profile Creation Example

This example demonstrates how to create, manage, and use HRV profiles
in ResonanceOS v6. Profiles define the tonal and stylistic characteristics
for content generation.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.generation.human_resonant_writer import HumanResonantWriter


def create_basic_profile():
    """Create a basic HRV profile from scratch"""
    print("🎨 Creating Basic HRV Profile")
    print("=" * 50)
    
    # Initialize profile manager
    profiles_dir = project_root / "data" / "profiles" / "hr_profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    
    manager = HRVProfileManager(str(profiles_dir))
    
    # Define profile parameters
    tenant = "example_organization"
    profile_name = "professional_modern"
    description = "Modern professional tone for business communications"
    
    # HRV vector (8 dimensions)
    # [sentence_variance, emotional_valence, emotional_intensity, 
    #  assertiveness_index, curiosity_index, metaphor_density, 
    #  storytelling_index, active_voice_ratio]
    hrv_vector = [0.45, 0.15, 0.35, 0.75, 0.40, 0.25, 0.30, 0.80]
    
    print(f"Creating profile '{profile_name}' for tenant '{tenant}'")
    print(f"Description: {description}")
    print(f"HRV Vector: {[round(x, 3) for x in hrv_vector]}")
    print()
    
    try:
        # Save profile
        manager.save_profile(tenant, profile_name, hrv_vector)
        print(f"✅ Profile saved successfully!")
        
        # Verify profile was saved
        loaded_vector = manager.load_profile(tenant, profile_name)
        print(f"✅ Profile verification: {[round(x, 3) for x in loaded_vector]}")
        
        return tenant, profile_name, hrv_vector
        
    except Exception as e:
        print(f"❌ Error creating profile: {e}")
        return None, None, None


def create_profile_from_text():
    """Create an HRV profile from existing text content"""
    print("\n📝 Creating Profile from Text Content")
    print("=" * 50)
    
    # Sample text content
    sample_text = """
    Executive Summary: The fourth quarter of 2024 demonstrated exceptional performance 
    across all key metrics. Revenue increased by 23% compared to the previous quarter, 
    reaching a record high of $45.2 million. This growth was primarily driven by our 
    expanded product line and successful market penetration in emerging regions.
    
    Strategic Initiatives: Our focus on digital transformation and operational excellence 
    has yielded significant results. The implementation of AI-powered analytics has 
    improved decision-making capabilities by 40%, while our customer satisfaction 
    scores have reached an all-time high of 4.6 out of 5.0.
    
    Market Position: We have strengthened our competitive position through strategic 
    partnerships and innovative product development. Our market share has increased 
    by 3.2 percentage points, solidifying our position as an industry leader.
    """
    
    print("Analyzing sample business text to extract HRV characteristics...")
    
    # Extract HRV from sample text
    extractor = HRVExtractor()
    hrv_vector = extractor.extract(sample_text)
    
    print(f"Extracted HRV Vector: {[round(x, 3) for x in hrv_vector]}")
    
    # Create profile from extracted HRV
    tenant = "example_organization"
    profile_name = "business_executive"
    description = "Executive business communication profile derived from sample text"
    
    print(f"\nCreating profile '{profile_name}' from extracted HRV...")
    
    try:
        # Initialize profile manager
        profiles_dir = project_root / "data" / "profiles" / "hr_profiles"
        manager = HRVProfileManager(str(profiles_dir))
        
        # Save profile
        manager.save_profile(tenant, profile_name, hrv_vector)
        print(f"✅ Profile created from text successfully!")
        
        return tenant, profile_name, hrv_vector
        
    except Exception as e:
        print(f"❌ Error creating profile from text: {e}")
        return None, None, None


def create_creative_profile():
    """Create a creative writing profile"""
    print("\n🎭 Creating Creative Writing Profile")
    print("=" * 50)
    
    # Creative writing HRV vector
    # Higher emotional content, storytelling, and metaphor
    creative_hrv = [0.75, 0.65, 0.85, 0.45, 0.80, 0.70, 0.90, 0.65]
    
    tenant = "example_organization"
    profile_name = "creative_storyteller"
    description = "Creative storytelling profile with high narrative and emotional content"
    
    print(f"Creating creative profile '{profile_name}'")
    print(f"HRV Vector: {[round(x, 3) for x in creative_hrv]}")
    print("Characteristics:")
    print("- High sentence variance (0.75)")
    print("- Strong emotional content (0.65, 0.85)")
    print("- Excellent storytelling (0.90)")
    print("- Rich metaphor usage (0.70)")
    print()
    
    try:
        # Initialize profile manager
        profiles_dir = project_root / "data" / "profiles" / "hr_profiles"
        manager = HRVProfileManager(str(profiles_dir))
        
        # Save profile
        manager.save_profile(tenant, profile_name, creative_hrv)
        print(f"✅ Creative profile created successfully!")
        
        return tenant, profile_name, creative_hrv
        
    except Exception as e:
        print(f"❌ Error creating creative profile: {e}")
        return None, None, None


def test_profile_generation(tenant, profile_name):
    """Test content generation with a specific profile"""
    print(f"\n🧪 Testing Profile: {profile_name}")
    print("=" * 50)
    
    if not tenant or not profile_name:
        print("❌ Invalid tenant or profile name")
        return
    
    # Test prompts
    test_prompts = [
        "The importance of innovation in business",
        "Building effective teams for success",
        "Digital transformation strategies"
    ]
    
    writer = HumanResonantWriter()
    extractor = HRVExtractor()
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Test {i}: {prompt}")
        print("-" * 30)
        
        try:
            # Generate content (using the profile would require API integration)
            content = writer.generate(prompt)
            
            # Extract HRV from generated content
            generated_hrv = extractor.extract(content)
            
            # Calculate similarity with target profile
            target_hrv = extractor.extract("This is a test sentence for profile comparison.")
            
            print(f"Generated content preview: {content[:100]}...")
            print(f"Generated HRV: {[round(x, 3) for x in generated_hrv]}")
            print(f"Average HRV Score: {sum(generated_hrv)/len(generated_hrv):.3f}")
            print()
            
        except Exception as e:
            print(f"❌ Error testing profile: {e}")
            print()


def compare_profiles():
    """Compare different profiles"""
    print("\n📊 Profile Comparison")
    print("=" * 50)
    
    # Profile definitions for comparison
    profiles_to_compare = {
        "professional_modern": [0.45, 0.15, 0.35, 0.75, 0.40, 0.25, 0.30, 0.80],
        "business_executive": [0.42, 0.18, 0.31, 0.78, 0.34, 0.21, 0.28, 0.85],
        "creative_storyteller": [0.75, 0.65, 0.85, 0.45, 0.80, 0.70, 0.90, 0.65],
        "technical_academic": [0.32, 0.12, 0.28, 0.81, 0.31, 0.18, 0.25, 0.82]
    }
    
    dimensions = [
        "Sentence Variance", "Emotional Valence", "Emotional Intensity",
        "Assertiveness", "Curiosity", "Metaphor Density", 
        "Storytelling", "Active Voice"
    ]
    
    print("Profile Comparison Matrix:")
    print("-" * 70)
    print(f"{'Profile':<20} {'Avg HRV':<8} {'Style':<30}")
    print("-" * 70)
    
    for profile_name, hrv_vector in profiles_to_compare.items():
        avg_score = sum(hrv_vector) / len(hrv_vector)
        
        # Determine style characteristics
        characteristics = []
        if hrv_vector[3] > 0.7:  # Assertiveness
            characteristics.append("Assertive")
        if hrv_vector[1] > 0.5:  # Emotional Valence
            characteristics.append("Emotional")
        if hrv_vector[6] > 0.7:  # Storytelling
            characteristics.append("Narrative")
        if hrv_vector[7] > 0.7:  # Active Voice
            characteristics.append("Direct")
        
        style = ", ".join(characteristics) if characteristics else "Balanced"
        
        print(f"{profile_name:<20} {avg_score:<8.3f} {style:<30}")
    
    print("\nDetailed Dimension Analysis:")
    print("-" * 70)
    
    for i, dimension in enumerate(dimensions):
        print(f"\n{dimension}:")
        for profile_name, hrv_vector in profiles_to_compare.items():
            value = hrv_vector[i]
            indicator = "🔴" if value < 0.3 else "🟡" if value < 0.7 else "🟢"
            print(f"  {indicator} {profile_name:<20}: {value:.3f}")


def create_adaptive_profile():
    """Create an adaptive profile based on context"""
    print("\n🔨 Creating Adaptive Profile")
    print("=" * 50)
    
    # Base profile
    base_profile = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    
    # Context adjustments
    contexts = {
        "formal_report": {
            "name": "formal_business",
            "adjustments": [0.1, -0.2, -0.1, 0.3, -0.1, -0.2, -0.1, 0.2],
            "description": "Formal business report style"
        },
        "creative_marketing": {
            "name": "marketing_creative",
            "adjustments": [0.3, 0.3, 0.4, 0.1, 0.2, 0.3, 0.4, 0.0],
            "description": "Creative marketing content style"
        },
        "technical_documentation": {
            "name": "technical_manual",
            "adjustments": [-0.2, -0.3, -0.2, 0.3, -0.1, -0.3, -0.2, 0.4],
            "description": "Technical documentation style"
        }
    }
    
    tenant = "example_organization"
    
    for context, config in contexts.items():
        print(f"\nContext: {context}")
        print(f"Profile: {config['name']}")
        print(f"Description: {config['description']}")
        
        # Apply adjustments
        adaptive_hrv = []
        for base, adjustment in zip(base_profile, config["adjustments"]):
            adjusted_value = max(0.0, min(1.0, base + adjustment))
            adaptive_hrv.append(adjusted_value)
        
        print(f"Adaptive HRV: {[round(x, 3) for x in adaptive_hrv]}")
        
        try:
            # Save adaptive profile
            profiles_dir = project_root / "data" / "profiles" / "hr_profiles"
            manager = HRVProfileManager(str(profiles_dir))
            manager.save_profile(tenant, config["name"], adaptive_hrv)
            print(f"✅ Adaptive profile saved: {config['name']}")
            
        except Exception as e:
            print(f"❌ Error saving adaptive profile: {e}")


def profile_management_demo():
    """Demonstrate profile management operations"""
    print("\n🗂️ Profile Management Demo")
    print("=" * 50)
    
    try:
        # Initialize profile manager
        profiles_dir = project_root / "data" / "profiles" / "hr_profiles"
        manager = HRVProfileManager(str(profiles_dir))
        
        tenant = "example_organization"
        
        # List all profiles
        profiles = manager.list_profiles(tenant)
        print(f"Profiles for tenant '{tenant}':")
        for profile in profiles:
            print(f"  - {profile}")
        
        if profiles:
            # Load and display a profile
            sample_profile = profiles[0]
            hrv_vector = manager.load_profile(tenant, sample_profile)
            print(f"\nLoaded profile '{sample_profile}':")
            print(f"HRV Vector: {[round(x, 3) for x in hrv_vector]}")
        
        print(f"\n✅ Profile management demo completed!")
        
    except Exception as e:
        print(f"❌ Error in profile management demo: {e}")


def main():
    """Run all profile creation examples"""
    print("🎯 ResonanceOS v6 - HRV Profile Creation Examples")
    print("=" * 60)
    print("This example demonstrates how to create and manage HRV profiles.")
    print("You'll learn how to:")
    print("- Create profiles from scratch")
    print("- Generate profiles from text content")
    print("- Create specialized profiles (creative, technical)")
    print("- Compare different profiles")
    print("- Create adaptive profiles for different contexts")
    print("- Manage profile operations")
    print()
    
    try:
        # Run examples
        tenant1, profile1, hrv1 = create_basic_profile()
        tenant2, profile2, hrv2 = create_profile_from_text()
        tenant3, profile3, hrv3 = create_creative_profile()
        
        # Test profile generation
        if tenant1 and profile1:
            test_profile_generation(tenant1, profile1)
        
        # Compare profiles
        compare_profiles()
        
        # Create adaptive profiles
        create_adaptive_profile()
        
        # Profile management demo
        profile_management_demo()
        
        print("\n🎉 All profile creation examples completed successfully!")
        print("\nNext Steps:")
        print("1. Try creating your own custom profiles")
        print("2. Experiment with different HRV vector values")
        print("3. Test profiles with your own content")
        print("4. Explore advanced profile management in ../advanced_usage/")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")


if __name__ == "__main__":
    main()
