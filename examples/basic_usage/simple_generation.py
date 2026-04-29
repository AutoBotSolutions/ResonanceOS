#!/usr/bin/env python3
"""
Simple Content Generation Example

This example demonstrates basic content generation using ResonanceOS v6.
It shows how to generate content with different profiles and analyze the results.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.api.hr_server import SimpleRequest, hr_generate


def simple_generation_example():
    """Demonstrate basic content generation"""
    print("🚀 ResonanceOS v6 - Simple Content Generation Example")
    print("=" * 60)
    
    # Initialize the writer
    writer = HumanResonantWriter()
    extractor = HRVExtractor()
    
    # Example prompts
    prompts = [
        "The future of artificial intelligence in business",
        "Sustainable technology solutions for climate change",
        "Innovative approaches to remote work productivity",
        "The impact of blockchain on supply chain management"
    ]
    
    print(f"Generating content for {len(prompts)} prompts...")
    print()
    
    for i, prompt in enumerate(prompts, 1):
        print(f"📝 Prompt {i}: {prompt}")
        print("-" * 50)
        
        try:
            # Generate content
            content = writer.generate(prompt)
            
            # Extract HRV from generated content
            hrv_vector = extractor.extract(content)
            
            # Display results
            print(f"Generated Content ({len(content)} characters):")
            print(content[:200] + "..." if len(content) > 200 else content)
            print()
            print(f"HRV Vector: {[round(x, 3) for x in hrv_vector]}")
            print(f"Average HRV Score: {sum(hrv_vector) / len(hrv_vector):.3f}")
            print()
            
        except Exception as e:
            print(f"❌ Error generating content: {e}")
            print()
    
    print("✅ Simple generation example completed!")


def profile_based_generation():
    """Demonstrate generation with different profiles"""
    print("\n🎨 Profile-Based Content Generation")
    print("=" * 60)
    
    # Available profiles (from default_profiles.json)
    profiles = [
        "neutral_professional",
        "creative_storytelling", 
        "technical_academic",
        "marketing_enthusiastic"
    ]
    
    prompt = "The importance of data-driven decision making"
    
    print(f"Generating content for prompt: '{prompt}'")
    print("Using different profiles to show style variation:")
    print()
    
    for profile_name in profiles:
        print(f"📊 Profile: {profile_name}")
        print("-" * 30)
        
        try:
            # Generate content with specific profile
            request = SimpleRequest(prompt=prompt, profile_name=profile_name)
            response = hr_generate(request)
            
            # Extract HRV from generated content
            extractor = HRVExtractor()
            hrv_vector = extractor.extract(response.article)
            
            # Display results
            print(f"Content Preview: {response.article[:150]}...")
            print(f"HRV Feedback: {response.hrv_feedback:.3f}")
            print(f"HRV Vector: {[round(x, 3) for x in hrv_vector]}")
            print()
            
        except Exception as e:
            print(f"❌ Error with profile {profile_name}: {e}")
            print()


def batch_generation_example():
    """Demonstrate batch content generation"""
    print("\n📦 Batch Content Generation")
    print("=" * 60)
    
    # Batch of prompts
    batch_prompts = [
        "Introduction to machine learning",
        "Benefits of cloud computing",
        "Cybersecurity best practices",
        "Digital transformation strategies",
        "Customer experience optimization"
    ]
    
    print(f"Processing batch of {len(batch_prompts)} prompts...")
    print()
    
    results = []
    writer = HumanResonantWriter()
    extractor = HRVExtractor()
    
    for i, prompt in enumerate(batch_prompts, 1):
        try:
            # Generate content
            content = writer.generate(prompt)
            hrv_vector = extractor.extract(content)
            
            # Store results
            result = {
                "prompt": prompt,
                "content": content,
                "hrv_vector": hrv_vector,
                "word_count": len(content.split()),
                "char_count": len(content)
            }
            results.append(result)
            
            print(f"✅ Generated {i}/{len(batch_prompts)}: {prompt[:30]}...")
            
        except Exception as e:
            print(f"❌ Failed to generate: {prompt[:30]}... - {e}")
    
    # Display batch statistics
    print("\n📊 Batch Generation Statistics:")
    print("-" * 30)
    print(f"Total Prompts: {len(batch_prompts)}")
    print(f"Successful: {len(results)}")
    print(f"Success Rate: {len(results)/len(batch_prompts)*100:.1f}%")
    
    if results:
        avg_words = sum(r["word_count"] for r in results) / len(results)
        avg_chars = sum(r["char_count"] for r in results) / len(results)
        avg_hrv = sum(sum(r["hrv_vector"]) / len(r["hrv_vector"]) for r in results) / len(results)
        
        print(f"Average Word Count: {avg_words:.1f}")
        print(f"Average Character Count: {avg_chars:.1f}")
        print(f"Average HRV Score: {avg_hrv:.3f}")
    
    print("\n✅ Batch generation example completed!")


def quality_assessment_example():
    """Demonstrate content quality assessment"""
    print("\n🔍 Content Quality Assessment")
    print("=" * 60)
    
    # Test content with different quality levels
    test_contents = [
        "This is a simple test sentence for quality assessment.",
        "The revolutionary impact of artificial intelligence on modern business operations represents a paradigm shift in how organizations approach decision-making processes and strategic planning initiatives.",
        "In the rapidly evolving landscape of digital transformation, companies must leverage cutting-edge technologies and data-driven insights to maintain competitive advantage and drive sustainable growth in an increasingly complex global marketplace.",
        "AI transforms business through data-driven insights, enabling organizations to make informed decisions, optimize operations, and enhance customer experiences while maintaining competitive advantage in dynamic markets."
    ]
    
    extractor = HRVExtractor()
    
    for i, content in enumerate(test_contents, 1):
        print(f"📄 Content Sample {i}:")
        print(f"Text: {content}")
        print("-" * 50)
        
        # Extract HRV
        hrv_vector = extractor.extract(content)
        
        # Calculate quality metrics
        word_count = len(content.split())
        avg_sentence_length = word_count / content.count('.') if '.' in content else word_count
        hrv_score = sum(hrv_vector) / len(hrv_vector)
        
        # Quality assessment
        if hrv_score > 0.7:
            quality = "Excellent"
        elif hrv_score > 0.6:
            quality = "Good"
        elif hrv_score > 0.5:
            quality = "Acceptable"
        else:
            quality = "Needs Improvement"
        
        print(f"Word Count: {word_count}")
        print(f"Average Sentence Length: {avg_sentence_length:.1f}")
        print(f"HRV Vector: {[round(x, 3) for x in hrv_vector]}")
        print(f"HRV Score: {hrv_score:.3f}")
        print(f"Quality Assessment: {quality}")
        print()


def main():
    """Run all simple generation examples"""
    print("🎯 ResonanceOS v6 - Basic Usage Examples")
    print("=" * 60)
    print("This example demonstrates basic content generation capabilities.")
    print("You'll learn how to:")
    print("- Generate content with default settings")
    print("- Use different profiles for style variation")
    print("- Process batches of prompts")
    print("- Assess content quality")
    print()
    
    try:
        # Run examples
        simple_generation_example()
        profile_based_generation()
        batch_generation_example()
        quality_assessment_example()
        
        print("\n🎉 All basic usage examples completed successfully!")
        print("\nNext Steps:")
        print("1. Try modifying the prompts and profiles")
        print("2. Explore advanced examples in ../advanced_usage/")
        print("3. Check integration examples in ../integration_examples/")
        print("4. Review business scenarios in ../business_scenarios/")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")


if __name__ == "__main__":
    main()
