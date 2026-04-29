#!/usr/bin/env python3
"""
Getting Started Tutorial

This tutorial provides a comprehensive introduction to ResonanceOS v6,
covering basic concepts, setup, and first steps in using the system.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.api.hr_server import SimpleRequest, hr_generate


def welcome_to_resonanceos():
    """Welcome and introduction to ResonanceOS v6"""
    print("🎉 Welcome to ResonanceOS v6!")
    print("=" * 60)
    print()
    print("ResonanceOS v6 is a Human-Resonant AI Writing System that creates")
    print("content with quantifiable human engagement metrics.")
    print()
    print("Key Features:")
    print("📊 8-dimensional HRV (Human-Resonant Value) vectors")
    print("🎯 Real-time feedback and optimization")
    print("👥 Multi-tenant profile management")
    print("🔧 Zero external dependencies for core functionality")
    print("🚀 Production-ready architecture")
    print()
    print("This tutorial will guide you through your first steps.")
    print()


def understanding_hrv_system():
    """Explain the HRV system"""
    print("🧠 Understanding the HRV System")
    print("=" * 50)
    print()
    print("HRV (Human-Resonant Value) is the core innovation of ResonanceOS v6.")
    print("It measures 8 dimensions of human response to text:")
    print()
    
    dimensions = [
        ("Sentence Variance", "Variety in sentence lengths and structures"),
        ("Emotional Valence", "Positive/negative sentiment balance (-1.0 to 1.0)"),
        ("Emotional Intensity", "Strength of emotional content (0.0 to 1.0)"),
        ("Assertiveness Index", "Confidence and directness (0.0 to 1.0)"),
        ("Curiosity Index", "Question and curiosity elements (0.0 to 1.0)"),
        ("Metaphor Density", "Metaphorical language usage (0.0 to 1.0)"),
        ("Storytelling Index", "Narrative and storytelling elements (0.0 to 1.0)"),
        ("Active Voice Ratio", "Active vs passive voice (0.0 to 1.0)")
    ]
    
    for name, description in dimensions:
        print(f"• {name}: {description}")
    
    print()
    print("💡 How HRV Works:")
    print("1. Each text gets an 8-dimensional HRV vector")
    print("2. Profiles define target HRV characteristics")
    print("3. System generates content to match target HRV")
    print("4. Real-time feedback optimizes for human resonance")
    print()


def first_content_generation():
    """Generate first content with ResonanceOS"""
    print("✨ Your First Content Generation")
    print("=" * 50)
    print()
    print("Let's generate your first content using ResonanceOS!")
    print()
    
    # Initialize the writer
    writer = HumanResonantWriter()
    
    # Simple prompt
    prompt = "The importance of innovation in modern business"
    
    print(f"📝 Prompt: {prompt}")
    print()
    
    try:
        # Generate content
        content = writer.generate(prompt)
        
        print("🎉 Content Generated Successfully!")
        print("-" * 30)
        print(content)
        print()
        
        # Extract HRV for analysis
        extractor = HRVExtractor()
        hrv_vector = extractor.extract(content)
        
        print("📊 HRV Analysis:")
        print("-" * 20)
        print(f"HRV Vector: {[round(x, 3) for x in hrv_vector]}")
        print(f"Average Score: {sum(hrv_vector)/len(hrv_vector):.3f}")
        print(f"Content Length: {len(content)} characters")
        print()
        
        return content, hrv_vector
        
    except Exception as e:
        print(f"❌ Error generating content: {e}")
        return None, None


def exploring_profiles():
    """Explore different HRV profiles"""
    print("🎨 Exploring HRV Profiles")
    print("=" * 50)
    print()
    print("Profiles define the style and tone of generated content.")
    print("Let's try different profiles with the same prompt!")
    print()
    
    # Test prompt
    prompt = "The future of technology in education"
    
    # Different profiles to try
    profiles_to_test = [
        ("neutral_professional", "Professional and balanced"),
        ("creative_storytelling", "Creative and engaging"),
        ("technical_academic", "Technical and formal"),
        ("marketing_enthusiastic", "Enthusiastic and persuasive")
    ]
    
    writer = HumanResonantWriter()
    extractor = HRVExtractor()
    
    for profile_name, description in profiles_to_test:
        print(f"📊 Profile: {profile_name}")
        print(f"Description: {description}")
        print("-" * 40)
        
        try:
            # Generate with specific profile (using API simulation)
            request = SimpleRequest(prompt=prompt, profile_name=profile_name)
            response = hr_generate(request)
            
            content = response.article
            hrv_vector = extractor.extract(content)
            
            print(f"Content Preview: {content[:100]}...")
            print(f"HRV Score: {sum(hrv_vector)/len(hrv_vector):.3f}")
            print()
            
        except Exception as e:
            print(f"❌ Error with profile {profile_name}: {e}")
            print()


def creating_custom_profiles():
    """Create custom HRV profiles"""
    print("🛠️ Creating Custom HRV Profiles")
    print("=" * 50)
    print()
    print("Let's create a custom profile tailored to your needs!")
    print()
    
    # Initialize profile manager
    profiles_dir = project_root / "data" / "profiles" / "hr_profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    
    manager = HRVProfileManager(str(profiles_dir))
    
    # Custom profile example
    tenant = "tutorial_user"
    profile_name = "my_first_profile"
    description = "My custom profile for balanced, engaging content"
    
    # HRV vector - let's create something balanced but engaging
    custom_hrv = [0.6, 0.4, 0.7, 0.6, 0.5, 0.4, 0.5, 0.7]
    
    print(f"🎯 Creating Profile: {profile_name}")
    print(f"Description: {description}")
    print(f"HRV Vector: {[round(x, 3) for x in custom_hrv]}")
    print()
    
    print("HRV Vector Breakdown:")
    print(f"• Sentence Variance: {custom_hrv[0]:.1f} - Moderate variety")
    print(f"• Emotional Valence: {custom_hrv[1]:.1f} - Slightly positive")
    print(f"• Emotional Intensity: {custom_hrv[2]:.1f} - Moderately emotional")
    print(f"• Assertiveness: {custom_hrv[3]:.1f} - Confident tone")
    print(f"• Curiosity: {custom_hrv[4]:.1f} - Some curiosity elements")
    print(f"• Metaphor Density: {custom_hrv[5]:.1f} - Light metaphor use")
    print(f"• Storytelling: {custom_hrv[6]:.1f} - Some storytelling")
    print(f"• Active Voice: {custom_hrv[7]:.1f} - Mostly active voice")
    print()
    
    try:
        # Save the profile
        manager.save_profile(tenant, profile_name, custom_hrv)
        print("✅ Profile saved successfully!")
        
        # Verify it was saved
        loaded_vector = manager.load_profile(tenant, profile_name)
        print(f"✅ Profile verified: {[round(x, 3) for x in loaded_vector]}")
        
        return tenant, profile_name, custom_hrv
        
    except Exception as e:
        print(f"❌ Error creating profile: {e}")
        return None, None, None


def testing_custom_profile(tenant, profile_name):
    """Test the custom profile we created"""
    if not tenant or not profile_name:
        print("⏭️  Skipping custom profile test (not created)")
        return
    
    print("🧪 Testing Your Custom Profile")
    print("=" * 50)
    print()
    
    prompt = "Building successful teams in the modern workplace"
    
    print(f"📝 Prompt: {prompt}")
    print(f"Profile: {profile_name}")
    print()
    
    try:
        # Generate content with custom profile
        request = SimpleRequest(prompt=prompt, tenant=tenant, profile_name=profile_name)
        response = hr_generate(request)
        
        content = response.article
        extractor = HRVExtractor()
        hrv_vector = extractor.extract(content)
        
        print("🎉 Custom Profile Test Results:")
        print("-" * 30)
        print(content[:200] + "..." if len(content) > 200 else content)
        print()
        print("📊 Analysis:")
        print(f"Content Length: {len(content)} characters")
        print(f"HRV Score: {sum(hrv_vector)/len(hrv_vector):.3f}")
        print(f"Profile Used: {profile_name}")
        print()
        
    except Exception as e:
        print(f"❌ Error testing custom profile: {e}")


def understanding_quality_metrics():
    """Understand content quality metrics"""
    print("📏 Understanding Quality Metrics")
    print("=" * 50)
    print()
    print("ResonanceOS provides multiple ways to assess content quality:")
    print()
    
    # Sample content at different quality levels
    quality_examples = [
        ("Poor Quality", "bad text not good"),
        ("Fair Quality", "This is a simple text with basic information."),
        ("Good Quality", "This document provides important information about the project with several key points."),
        ("Excellent Quality", "The comprehensive analysis reveals significant insights into market dynamics, highlighting strategic opportunities for growth and innovation in an increasingly competitive landscape.")
    ]
    
    extractor = HRVExtractor()
    
    for quality_name, content in quality_examples:
        print(f"📊 {quality_name} Example:")
        print(f"Content: {content}")
        print("-" * 40)
        
        hrv_vector = extractor.extract(content)
        avg_score = sum(hrv_vector) / len(hrv_vector)
        
        # Quality classification
        if avg_score > 0.7:
            grade = "A (Excellent)"
        elif avg_score > 0.6:
            grade = "B (Good)"
        elif avg_score > 0.5:
            grade = "C (Fair)"
        else:
            grade = "D (Poor)"
        
        print(f"HRV Score: {avg_score:.3f}")
        print(f"Quality Grade: {grade}")
        print()
    
    print("💡 Quality Tips:")
    print("• Aim for HRV scores above 0.6 for good quality")
    print("• Use variety in sentence structure")
    print("• Include emotional elements for engagement")
    print("• Add storytelling and metaphors for richness")
    print("• Use active voice for clarity")
    print()


def practical_applications():
    """Show practical applications"""
    print("🚀 Practical Applications")
    print("=" * 50)
    print()
    print("ResonanceOS v6 can be used for various applications:")
    print()
    
    applications = [
        ("Business Content", ["Reports", "Proposals", "Emails", "Documentation"]),
        ("Marketing Materials", ["Blog posts", "Social media", "Ads", "Campaigns"]),
        ("Creative Writing", ["Stories", "Articles", "Scripts", "Poetry"]),
        ("Technical Writing", ["Manuals", "Documentation", "Tutorials", "Guides"]),
        ("Educational Content", ["Courses", "Textbooks", "Tutorials", "Explanations"])
    ]
    
    for category, examples in applications:
        print(f"📂 {category}:")
        for example in examples:
            print(f"  • {example}")
        print()
    
    print("💡 Application Tips:")
    print("• Choose the right profile for your content type")
    print("• Adjust HRV vectors to match your brand voice")
    print("• Use quality metrics to ensure consistency")
    print("• Experiment with different prompts and styles")
    print()


def next_steps():
    """Provide next steps and resources"""
    print("🎯 Next Steps")
    print("=" * 50)
    print()
    print("Congratulations! You've completed the Getting Started tutorial.")
    print()
    print("Here's what to do next:")
    print()
    print("📚 Explore More Examples:")
    print("• ../basic_usage/ - Basic usage examples")
    print("• ../advanced_usage/ - Advanced features")
    print("• ../business_scenarios/ - Real-world applications")
    print("• ../creative_applications/ - Creative writing")
    print()
    print("🔧 Advanced Topics:")
    print("• Multi-tenant profile management")
    print("• Batch processing and automation")
    print("• API integration")
    print("• Performance optimization")
    print()
    print("📖 Documentation:")
    print("• /data/README.md - Data directory guide")
    print("• /data/config/ - Configuration options")
    print("• /tests/README.md - Testing information")
    print()
    print("🛠️ Tools:")
    print("• data/scripts/ - Utility scripts")
    print("• data/profiles/ - Profile management")
    print("• data/exports/ - Analytics and reports")
    print()
    print("💡 Pro Tips:")
    print("• Start with simple prompts and profiles")
    print("• Experiment with HRV vector adjustments")
    print("• Use quality metrics to improve your content")
    print("• Join the community for support and ideas")
    print()


def tutorial_summary():
    """Provide a summary of what was learned"""
    print("📋 Tutorial Summary")
    print("=" * 50)
    print()
    print("In this tutorial, you learned:")
    print()
    print("✅ ResonanceOS v6 Fundamentals:")
    print("   • Understanding HRV (Human-Resonant Value) system")
    print("   • 8-dimensional content analysis")
    print("   • Real-time feedback and optimization")
    print()
    print("✅ Basic Operations:")
    print("   • Generating your first content")
    print("   • Using different profiles")
    print("   • Creating custom profiles")
    print("   • Analyzing content quality")
    print()
    print("✅ Practical Skills:")
    print("   • Setting up the system")
    print("   • Working with HRV vectors")
    print("   • Quality assessment")
    print("   • Profile management")
    print()
    print("✅ Key Concepts:")
    print("   • HRV dimensions and their meanings")
    print("   • Profile-based content generation")
    print("   • Quality metrics and assessment")
    print("   • Multi-tenant architecture")
    print()
    print("🎉 You're now ready to explore more advanced features!")
    print()


def main():
    """Run the complete getting started tutorial"""
    print("🎯 ResonanceOS v6 - Getting Started Tutorial")
    print("=" * 60)
    print("This tutorial will guide you through your first steps with ResonanceOS v6.")
    print("No prior experience required!")
    print()
    
    try:
        # Run tutorial sections
        welcome_to_resonanceos()
        understanding_hrv_system()
        content, hrv = first_content_generation()
        exploring_profiles()
        tenant, profile, custom_hrv = creating_custom_profiles()
        testing_custom_profile(tenant, profile)
        understanding_quality_metrics()
        practical_applications()
        next_steps()
        tutorial_summary()
        
        print("\n🎉 Tutorial Completed Successfully!")
        print("You're now ready to start using ResonanceOS v6!")
        print("\nHappy writing! 📝✨")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Tutorial interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")
        print("\nTroubleshooting:")
        print("1. Ensure ResonanceOS is properly installed")
        print("2. Check Python path configuration")
        print("3. Verify all dependencies are available")
        print("4. Check file permissions")


if __name__ == "__main__":
    main()
