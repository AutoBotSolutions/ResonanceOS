#!/usr/bin/env python3
"""
HRV Vector Extraction Example

This example demonstrates how to extract Human-Resonant Value (HRV) vectors
from text content using ResonanceOS v6. HRV vectors capture 8 dimensions
of human response to text.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.profiles.hrv_extractor import HRVExtractor


def basic_extraction_example():
    """Demonstrate basic HRV extraction from simple text"""
    print("🔍 Basic HRV Extraction Example")
    print("=" * 50)
    
    # Initialize HRV extractor
    extractor = HRVExtractor()
    
    # Sample texts for analysis
    sample_texts = [
        "This is a simple test sentence.",
        "The revolutionary impact of artificial intelligence transforms modern business operations through data-driven insights and strategic decision-making processes.",
        "In the rapidly evolving landscape of digital transformation, companies must leverage cutting-edge technologies to maintain competitive advantage and drive sustainable growth.",
        "Once upon a time, in a magical forest where sunlight danced through emerald leaves like golden fairies, there existed a place that maps forgot and time overlooked."
    ]
    
    print("Analyzing sample texts:")
    print()
    
    for i, text in enumerate(sample_texts, 1):
        print(f"📄 Text {i}:")
        print(f"Content: {text}")
        print("-" * 40)
        
        try:
            # Extract HRV vector
            hrv_vector = extractor.extract(text)
            
            # Display results
            print(f"HRV Vector: {[round(x, 3) for x in hrv_vector]}")
            print(f"Average Score: {sum(hrv_vector) / len(hrv_vector):.3f}")
            
            # Interpret results
            interpretation = interpret_hrv_vector(hrv_vector)
            print(f"Interpretation: {interpretation}")
            print()
            
        except Exception as e:
            print(f"❌ Error extracting HRV: {e}")
            print()


def interpret_hrv_vector(hrv_vector):
    """Interpret HRV vector characteristics"""
    dimensions = [
        "Sentence Variance", "Emotional Valence", "Emotional Intensity",
        "Assertiveness", "Curiosity", "Metaphor Density", 
        "Storytelling", "Active Voice"
    ]
    
    interpretations = []
    
    for i, (dimension, value) in enumerate(zip(dimensions, hrv_vector)):
        if value > 0.7:
            interpretations.append(f"High {dimension.lower().replace(' ', '_')}")
        elif value < 0.3:
            interpretations.append(f"Low {dimension.lower().replace(' ', '_')}")
    
    return ", ".join(interpretations) if interpretations else "Balanced"


def detailed_analysis_example():
    """Demonstrate detailed HRV analysis with multiple metrics"""
    print("\n📊 Detailed HRV Analysis")
    print("=" * 50)
    
    extractor = HRVExtractor()
    
    # Complex text for detailed analysis
    analysis_text = """
    The integration of artificial intelligence into enterprise operations represents a paradigm 
    shift in how organizations approach strategic decision-making and operational efficiency. 
    By leveraging machine learning algorithms and advanced analytics, companies can now process 
    vast amounts of data to uncover insights that were previously hidden in complex patterns. 
    This technological revolution not only enhances productivity but also creates new opportunities 
    for innovation and growth in an increasingly competitive global marketplace.
    """
    
    print("Analyzing complex business text:")
    print(f"Text: {analysis_text.strip()}")
    print("-" * 50)
    
    try:
        # Extract HRV vector
        hrv_vector = extractor.extract(analysis_text)
        
        # Detailed analysis
        dimensions = [
            "Sentence Variance", "Emotional Valence", "Emotional Intensity",
            "Assertiveness", "Curiosity", "Metaphor Density", 
            "Storytelling", "Active Voice"
        ]
        
        print("Detailed HRV Analysis:")
        print("-" * 30)
        
        for i, (dimension, value) in enumerate(zip(dimensions, hrv_vector)):
            # Determine level
            if value > 0.7:
                level = "High"
                indicator = "🟢"
            elif value > 0.4:
                level = "Medium"
                indicator = "🟡"
            else:
                level = "Low"
                indicator = "🔴"
            
            print(f"{indicator} {dimension:<20}: {value:.3f} ({level})")
        
        # Overall assessment
        avg_score = sum(hrv_vector) / len(hrv_vector)
        print(f"\nOverall HRV Score: {avg_score:.3f}")
        
        # Quality assessment
        if avg_score > 0.7:
            quality = "Excellent"
        elif avg_score > 0.6:
            quality = "Good"
        elif avg_score > 0.5:
            quality = "Acceptable"
        else:
            quality = "Needs Improvement"
        
        print(f"Content Quality: {quality}")
        
        # Recommendations
        recommendations = generate_recommendations(hrv_vector)
        print(f"\nRecommendations: {recommendations}")
        
    except Exception as e:
        print(f"❌ Error in detailed analysis: {e}")


def generate_recommendations(hrv_vector):
    """Generate recommendations based on HRV analysis"""
    recommendations = []
    
    # Analyze each dimension
    if hrv_vector[0] < 0.4:  # Sentence Variance
        recommendations.append("Vary sentence lengths for better readability")
    
    if hrv_vector[1] < 0.3:  # Emotional Valence
        recommendations.append("Add more positive elements to engage readers")
    elif hrv_vector[1] > 0.7:
        recommendations.append("Balance emotional content with neutral information")
    
    if hrv_vector[2] < 0.4:  # Emotional Intensity
        recommendations.append("Increase emotional impact through stronger language")
    
    if hrv_vector[3] < 0.5:  # Assertiveness
        recommendations.append("Use more confident and direct language")
    
    if hrv_vector[4] < 0.4:  # Curiosity
        recommendations.append("Add questions or curiosity-inducing elements")
    
    if hrv_vector[5] < 0.3:  # Metaphor Density
        recommendations.append("Consider adding metaphors for better engagement")
    
    if hrv_vector[6] < 0.4:  # Storytelling
        recommendations.append("Incorporate storytelling elements for better connection")
    
    if hrv_vector[7] < 0.6:  # Active Voice
        recommendations.append("Use more active voice for clearer communication")
    
    return "; ".join(recommendations) if recommendations else "Content is well-balanced"


def batch_extraction_example():
    """Demonstrate batch HRV extraction from multiple texts"""
    print("\n📦 Batch HRV Extraction")
    print("=" * 50)
    
    extractor = HRVExtractor()
    
    # Batch of texts to analyze
    batch_texts = {
        "business_report": """
            Q3 2024 Financial Performance Report. Revenue increased by 23% compared to 
            the previous quarter, reaching a record high of $45.2 million. Operating 
            expenses were carefully managed, resulting in an improved profit margin.
        """,
        "creative_story": """
            In a world where dreams and reality intertwine, a young artist discovers 
            a magical paintbrush that brings her imagination to life. Each stroke creates 
            vibrant landscapes that dance with color and emotion, transforming the canvas 
            into a portal to another dimension.
        """,
        "technical_documentation": """
            The system architecture consists of three primary components: the data 
            processing layer, the business logic layer, and the presentation layer. 
            Each component communicates through RESTful APIs and follows established 
            design patterns for scalability and maintainability.
        """,
        "marketing_content": """
            Transform your business with our revolutionary AI-powered solutions! Experience 
            unprecedented growth and efficiency as our cutting-edge technology unlocks 
            new possibilities and drives your success to extraordinary heights!
        """
    }
    
    print(f"Processing {len(batch_texts)} texts for HRV extraction...")
    print()
    
    results = {}
    
    for text_type, text in batch_texts.items():
        print(f"📄 Processing: {text_type}")
        print("-" * 30)
        
        try:
            # Extract HRV
            hrv_vector = extractor.extract(text.strip())
            results[text_type] = hrv_vector
            
            # Display results
            print(f"HRV Vector: {[round(x, 3) for x in hrv_vector]}")
            print(f"Average Score: {sum(hrv_vector) / len(hrv_vector):.3f}")
            print()
            
        except Exception as e:
            print(f"❌ Error processing {text_type}: {e}")
            print()
    
    # Compare results
    print("📊 Batch Analysis Comparison:")
    print("-" * 40)
    print(f"{'Content Type':<20} {'Avg Score':<10} {'Style':<20}")
    print("-" * 40)
    
    for text_type, hrv_vector in results.items():
        avg_score = sum(hrv_vector) / len(hrv_vector)
        
        # Determine style
        if hrv_vector[1] > 0.5 and hrv_vector[6] > 0.5:
            style = "Creative"
        elif hrv_vector[3] > 0.6 and hrv_vector[7] > 0.6:
            style = "Professional"
        elif hrv_vector[4] > 0.5 and hrv_vector[5] > 0.4:
            style = "Engaging"
        else:
            style = "Balanced"
        
        print(f"{text_type:<20} {avg_score:<10.3f} {style:<20}")


def comparative_analysis_example():
    """Demonstrate comparative analysis between texts"""
    print("\n🔍 Comparative HRV Analysis")
    print("=" * 50)
    
    extractor = HRVExtractor()
    
    # Texts for comparison
    comparison_texts = [
        ("Formal Business", "The quarterly financial report indicates significant growth in revenue streams, with particular emphasis on digital transformation initiatives and operational efficiency improvements."),
        ("Casual Blog", "Hey everyone! I'm super excited to share some amazing news about our latest project. It's been an incredible journey, and I can't wait to tell you all about it!"),
        ("Technical Manual", "Initialize the system by executing the configuration script. Ensure all dependencies are installed and the database connection parameters are correctly configured."),
        ("Creative Writing", "As dawn broke over the misty mountains, Sarah discovered a hidden path that seemed to whisper secrets of ancient civilizations long forgotten by time.")
    ]
    
    print("Comparative Analysis of Different Writing Styles:")
    print()
    
    results = []
    
    for style_name, text in comparison_texts:
        try:
            hrv_vector = extractor.extract(text)
            results.append((style_name, hrv_vector))
            
            print(f"📄 {style_name}:")
            print(f"HRV: {[round(x, 3) for x in hrv_vector]}")
            print(f"Score: {sum(hrv_vector) / len(hrv_vector):.3f}")
            print()
            
        except Exception as e:
            print(f"❌ Error analyzing {style_name}: {e}")
    
    # Create comparison table
    if results:
        dimensions = [
            "Sent Var", "Emo Val", "Emo Int", "Assert", 
            "Curious", "Metaphor", "Story", "Active"
        ]
        
        print("📊 Comparison Table:")
        print("-" * 70)
        print(f"{'Style':<15} {'Score':<8} " + " ".join(f"{dim:<8}" for dim in dimensions))
        print("-" * 70)
        
        for style_name, hrv_vector in results:
            avg_score = sum(hrv_vector) / len(hrv_vector)
            values = [f"{x:<8.3f}" for x in hrv_vector]
            print(f"{style_name:<15} {avg_score:<8.3f} " + " ".join(values))
        
        # Find most different dimensions
        print("\n🔍 Style Differences:")
        print("-" * 30)
        
        if len(results) >= 2:
            for i in range(8):
                values = [hrv_vector[i] for _, hrv_vector in results]
                max_val = max(values)
                min_val = min(values)
                difference = max_val - min_val
                
                if difference > 0.3:  # Significant difference
                    max_style = results[values.index(max_val)][0]
                    min_style = results[values.index(min_val)][0]
                    print(f"{dimensions[i]}: {max_style} ({max_val:.3f}) vs {min_style} ({min_val:.3f})")


def quality_assessment_example():
    """Demonstrate content quality assessment using HRV"""
    print("\n🏆 Content Quality Assessment")
    print("=" * 50)
    
    extractor = HRVExtractor()
    
    # Texts with different quality levels
    quality_texts = [
        ("Poor Quality", "bad text not good"),
        ("Fair Quality", "This is a simple text with basic information."),
        ("Good Quality", "This document provides important information about the project. It includes several key points that readers should understand."),
        ("Excellent Quality", "The comprehensive analysis reveals significant insights into market dynamics, highlighting strategic opportunities for growth and innovation in an increasingly competitive landscape.")
    ]
    
    print("Quality Assessment Results:")
    print("-" * 40)
    
    for quality_name, text in quality_texts:
        try:
            hrv_vector = extractor.extract(text)
            avg_score = sum(hrv_vector) / len(hrv_vector)
            
            # Quality classification
            if avg_score > 0.7:
                grade = "A"
                assessment = "Excellent"
            elif avg_score > 0.6:
                grade = "B"
                assessment = "Good"
            elif avg_score > 0.5:
                grade = "C"
                assessment = "Fair"
            else:
                grade = "D"
                assessment = "Poor"
            
            print(f"{quality_name:<15} {grade:<5} {avg_score:<8.3f} {assessment}")
            
        except Exception as e:
            print(f"❌ Error assessing {quality_name}: {e}")


def main():
    """Run all HRV extraction examples"""
    print("🎯 ResonanceOS v6 - HRV Vector Extraction Examples")
    print("=" * 60)
    print("This example demonstrates HRV extraction capabilities.")
    print("You'll learn how to:")
    print("- Extract HRV vectors from text")
    print("- Interpret HRV dimensions")
    print("- Perform detailed analysis")
    print("- Process batches of texts")
    print("- Compare different writing styles")
    print("- Assess content quality")
    print()
    
    try:
        # Run examples
        basic_extraction_example()
        detailed_analysis_example()
        batch_extraction_example()
        comparative_analysis_example()
        quality_assessment_example()
        
        print("\n🎉 All HRV extraction examples completed successfully!")
        print("\nNext Steps:")
        print("1. Try extracting HRV from your own text content")
        print("2. Experiment with different text types and styles")
        print("3. Use HRV analysis for content optimization")
        print("4. Explore advanced usage examples in ../advanced_usage/")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")


if __name__ == "__main__":
    main()
