#!/usr/bin/env python3
"""
Corpus Analysis Example

This example demonstrates comprehensive text corpus analysis using ResonanceOS v6,
including HRV pattern analysis, statistical insights, and data-driven recommendations.
"""

import sys
import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager


class CorpusAnalyzer:
    """Advanced corpus analysis using ResonanceOS v6"""
    
    def __init__(self):
        self.writer = HumanResonantWriter()
        self.extractor = HRVExtractor()
        
        # HRV dimension names
        self.dimensions = [
            "sentence_variance", "emotional_valence", "emotional_intensity",
            "assertiveness_index", "curiosity_index", "metaphor_density",
            "storytelling_index", "active_voice_ratio"
        ]
    
    def analyze_single_document(self, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze a single document comprehensively"""
        print("📄 Analyzing Document...")
        print("-" * 30)
        
        # Extract HRV vector
        hrv_vector = self.extractor.extract(text)
        
        # Basic text statistics
        words = text.split()
        sentences = text.split('.')
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Calculate metrics
        analysis = {
            "hrv_vector": hrv_vector,
            "avg_hrv_score": sum(hrv_vector) / len(hrv_vector),
            "text_statistics": {
                "word_count": len(words),
                "sentence_count": len([s for s in sentences if s.strip()]),
                "paragraph_count": len(paragraphs),
                "avg_sentence_length": len(words) / len([s for s in sentences if s.strip()]) if sentences else 0,
                "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0
            },
            "quality_metrics": self.calculate_quality_metrics(hrv_vector),
            "style_analysis": self.analyze_writing_style(hrv_vector),
            "metadata": metadata or {}
        }
        
        print(f"✅ Analysis Complete")
        print(f"   Words: {analysis['text_statistics']['word_count']}")
        print(f"   HRV Score: {analysis['avg_hrv_score']:.3f}")
        print(f"   Quality: {analysis['quality_metrics']['overall_quality']}")
        
        return analysis
    
    def calculate_quality_metrics(self, hrv_vector: List[float]) -> Dict[str, Any]:
        """Calculate comprehensive quality metrics"""
        avg_score = sum(hrv_vector) / len(hrv_vector)
        
        # Quality assessment
        if avg_score > 0.8:
            overall_quality = "Excellent"
            quality_score = 95
        elif avg_score > 0.7:
            overall_quality = "Good"
            quality_score = 85
        elif avg_score > 0.6:
            overall_quality = "Fair"
            quality_score = 75
        else:
            overall_quality = "Poor"
            quality_score = 65
        
        # Dimension-specific quality
        dimension_quality = {}
        for i, dimension in enumerate(self.dimensions):
            value = hrv_vector[i]
            if value > 0.7:
                dimension_quality[dimension] = "Strong"
            elif value > 0.4:
                dimension_quality[dimension] = "Moderate"
            else:
                dimension_quality[dimension] = "Weak"
        
        # Engagement potential
        engagement_score = (hrv_vector[1] + hrv_vector[2] + hrv_vector[4] + hrv_vector[6]) / 4
        
        # Clarity score
        clarity_score = (hrv_vector[0] + hrv_vector[7]) / 2
        
        return {
            "overall_quality": overall_quality,
            "quality_score": quality_score,
            "avg_hrv_score": avg_score,
            "engagement_score": engagement_score,
            "clarity_score": clarity_score,
            "dimension_quality": dimension_quality,
            "recommendations": self.generate_quality_recommendations(hrv_vector)
        }
    
    def analyze_writing_style(self, hrv_vector: List[float]) -> Dict[str, Any]:
        """Analyze writing style characteristics"""
        style_characteristics = []
        
        # Analyze each dimension
        if hrv_vector[0] > 0.7:
            style_characteristics.append("Varied sentence structure")
        elif hrv_vector[0] < 0.3:
            style_characteristics.append("Monotonous sentence structure")
        
        if hrv_vector[1] > 0.5:
            style_characteristics.append("Positive tone")
        elif hrv_vector[1] < -0.5:
            style_characteristics.append("Negative tone")
        else:
            style_characteristics.append("Neutral tone")
        
        if hrv_vector[2] > 0.7:
            style_characteristics.append("Highly emotional")
        elif hrv_vector[2] < 0.3:
            style_characteristics.append("Reserved tone")
        
        if hrv_vector[3] > 0.7:
            style_characteristics.append("Assertive style")
        elif hrv_vector[3] < 0.3:
            style_characteristics.append("Passive style")
        
        if hrv_vector[4] > 0.6:
            style_characteristics.append("Inquisitive")
        
        if hrv_vector[5] > 0.6:
            style_characteristics.append("Metaphor-rich")
        
        if hrv_vector[6] > 0.7:
            style_characteristics.append("Story-driven")
        
        if hrv_vector[7] > 0.7:
            style_characteristics.append("Active voice dominant")
        elif hrv_vector[7] < 0.3:
            style_characteristics.append("Passive voice dominant")
        
        # Determine primary style
        if hrv_vector[6] > 0.6 and hrv_vector[5] > 0.5:
            primary_style = "Creative/Narrative"
        elif hrv_vector[3] > 0.6 and hrv_vector[7] > 0.6:
            primary_style = "Professional/Direct"
        elif hrv_vector[1] > 0.5 and hrv_vector[2] > 0.5:
            primary_style = "Emotional/Persuasive"
        elif hrv_vector[4] > 0.5:
            primary_style = "Inquisitive/Analytical"
        else:
            primary_style = "Balanced/Neutral"
        
        return {
            "primary_style": primary_style,
            "characteristics": style_characteristics,
            "formality_level": "Formal" if hrv_vector[3] > 0.6 else "Informal" if hrv_vector[3] < 0.4 else "Semi-formal",
            "engagement_level": "High" if sum(hrv_vector)/len(hrv_vector) > 0.7 else "Medium" if sum(hrv_vector)/len(hrv_vector) > 0.5 else "Low"
        }
    
    def generate_quality_recommendations(self, hrv_vector: List[float]) -> List[str]:
        """Generate improvement recommendations based on HRV analysis"""
        recommendations = []
        
        # Sentence variance
        if hrv_vector[0] < 0.4:
            recommendations.append("Vary sentence lengths for better readability")
        
        # Emotional valence
        if hrv_vector[1] < 0.3:
            recommendations.append("Add more positive elements to engage readers")
        elif hrv_vector[1] > 0.8:
            recommendations.append("Balance positive content with neutral information")
        
        # Emotional intensity
        if hrv_vector[2] < 0.4:
            recommendations.append("Increase emotional impact through stronger language")
        
        # Assertiveness
        if hrv_vector[3] < 0.5:
            recommendations.append("Use more confident and direct language")
        
        # Curiosity
        if hrv_vector[4] < 0.4:
            recommendations.append("Add questions or curiosity-inducing elements")
        
        # Metaphor density
        if hrv_vector[5] < 0.3:
            recommendations.append("Consider adding metaphors for better engagement")
        
        # Storytelling
        if hrv_vector[6] < 0.4:
            recommendations.append("Incorporate storytelling elements for better connection")
        
        # Active voice
        if hrv_vector[7] < 0.6:
            recommendations.append("Use more active voice for clearer communication")
        
        return recommendations if recommendations else ["Content is well-balanced"]
    
    def analyze_corpus_batch(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a batch of documents and generate corpus insights"""
        print(f"📚 Analyzing Corpus of {len(documents)} Documents")
        print("=" * 60)
        print()
        
        corpus_analyses = []
        
        for i, doc in enumerate(documents, 1):
            print(f"📄 Document {i}/{len(documents)}: {doc.get('title', f'Doc {i}')}")
            
            analysis = self.analyze_single_document(
                doc['content'], 
                doc.get('metadata', {})
            )
            analysis['document_id'] = doc.get('id', f'doc_{i}')
            analysis['title'] = doc.get('title', f'Document {i}')
            corpus_analyses.append(analysis)
        
        # Generate corpus-level insights
        corpus_insights = self.generate_corpus_insights(corpus_analyses)
        
        print(f"\n📊 Corpus Analysis Complete!")
        print(f"   Documents: {len(corpus_analyses)}")
        print(f"   Avg HRV Score: {corpus_insights['overall_statistics']['avg_hrv_score']:.3f}")
        print(f"   Quality Distribution: {corpus_insights['quality_distribution']}")
        
        return corpus_insights
    
    def generate_corpus_insights(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive corpus insights"""
        if not analyses:
            return {"error": "No analyses provided"}
        
        # Overall statistics
        hrv_scores = [a['avg_hrv_score'] for a in analyses]
        word_counts = [a['text_statistics']['word_count'] for a in analyses]
        
        overall_stats = {
            "total_documents": len(analyses),
            "total_words": sum(word_counts),
            "avg_words_per_doc": sum(word_counts) / len(word_counts),
            "avg_hrv_score": sum(hrv_scores) / len(hrv_scores),
            "hrv_score_std": np.std(hrv_scores),
            "min_hrv_score": min(hrv_scores),
            "max_hrv_score": max(hrv_scores)
        }
        
        # Quality distribution
        quality_counts = Counter(a['quality_metrics']['overall_quality'] for a in analyses)
        quality_distribution = {
            "Excellent": quality_counts.get("Excellent", 0),
            "Good": quality_counts.get("Good", 0),
            "Fair": quality_counts.get("Fair", 0),
            "Poor": quality_counts.get("Poor", 0)
        }
        
        # Dimension analysis
        dimension_stats = {}
        for i, dimension in enumerate(self.dimensions):
            values = [a['hrv_vector'][i] for a in analyses]
            dimension_stats[dimension] = {
                "mean": np.mean(values),
                "std": np.std(values),
                "min": min(values),
                "max": max(values),
                "median": np.median(values)
            }
        
        # Style distribution
        style_counts = Counter(a['style_analysis']['primary_style'] for a in analyses)
        style_distribution = dict(style_counts)
        
        # Top performing documents
        top_docs = sorted(analyses, key=lambda x: x['avg_hrv_score'], reverse=True)[:5]
        
        # Improvement opportunities
        improvement_areas = self.identify_improvement_areas(analyses)
        
        # Recommendations
        recommendations = self.generate_corpus_recommendations(overall_stats, dimension_stats)
        
        return {
            "overall_statistics": overall_stats,
            "quality_distribution": quality_distribution,
            "dimension_statistics": dimension_stats,
            "style_distribution": style_distribution,
            "top_performing_documents": [
                {
                    "title": doc['title'],
                    "hrv_score": doc['avg_hrv_score'],
                    "quality": doc['quality_metrics']['overall_quality']
                }
                for doc in top_docs
            ],
            "improvement_areas": improvement_areas,
            "recommendations": recommendations,
            "detailed_analyses": analyses
        }
    
    def identify_improvement_areas(self, analyses: List[Dict[str, Any]]) -> List[str]:
        """Identify common improvement areas across the corpus"""
        improvement_areas = []
        
        # Analyze dimension weaknesses
        dimension_avgs = {}
        for i, dimension in enumerate(self.dimensions):
            values = [a['hrv_vector'][i] for a in analyses]
            dimension_avgs[dimension] = sum(values) / len(values)
        
        # Identify dimensions that need improvement
        for dimension, avg_value in dimension_avgs.items():
            if avg_value < 0.4:
                improvement_areas.append(f"Low {dimension.replace('_', ' ')} (avg: {avg_value:.2f})")
        
        # Quality issues
        poor_quality_count = sum(1 for a in analyses if a['quality_metrics']['overall_quality'] == 'Poor')
        if poor_quality_count > len(analyses) * 0.2:  # More than 20% poor quality
            improvement_areas.append(f"High poor quality rate ({poor_quality_count}/{len(analyses)})")
        
        # Engagement issues
        low_engagement = sum(1 for a in analyses if a['quality_metrics']['engagement_score'] < 0.5)
        if low_engagement > len(analyses) * 0.3:  # More than 30% low engagement
            improvement_areas.append(f"Low engagement rate ({low_engagement}/{len(analyses)})")
        
        return improvement_areas if improvement_areas else ["No major improvement areas identified"]
    
    def generate_corpus_recommendations(self, overall_stats: Dict, dimension_stats: Dict) -> List[str]:
        """Generate corpus-level recommendations"""
        recommendations = []
        
        # Overall score recommendations
        if overall_stats['avg_hrv_score'] < 0.6:
            recommendations.append("Focus on improving overall content quality through better HRV balance")
        
        # Dimension-specific recommendations
        for dimension, stats in dimension_stats.items():
            if stats['mean'] < 0.4:
                recommendations.append(f"Improve {dimension.replace('_', ' ')} across the corpus")
            elif stats['std'] > 0.3:
                recommendations.append(f"Standardize {dimension.replace('_', ' ')} for consistency")
        
        # Length recommendations
        if overall_stats['avg_words_per_doc'] < 200:
            recommendations.append("Consider increasing document length for more comprehensive content")
        elif overall_stats['avg_words_per_doc'] > 2000:
            recommendations.append("Consider breaking down very long documents for better readability")
        
        # Diversity recommendations
        if overall_stats['hrv_score_std'] < 0.1:
            recommendations.append("Increase content diversity by varying HRV characteristics")
        
        return recommendations if recommendations else ["Corpus is well-balanced"]
    
    def create_sample_corpus(self) -> List[Dict[str, Any]]:
        """Create a sample corpus for demonstration"""
        sample_documents = [
            {
                "id": "doc_001",
                "title": "Business Strategy Overview",
                "content": """
                Executive Summary: Our comprehensive business strategy for 2024 focuses on digital transformation,
                customer experience enhancement, and operational excellence. The strategic initiatives outlined
                in this document represent our commitment to innovation and sustainable growth. We will leverage
                cutting-edge technologies to streamline processes and deliver exceptional value to our stakeholders.
                
                Market Analysis: Current market trends indicate significant opportunities in the AI and machine
                learning sectors. Our competitive advantage lies in our ability to adapt quickly to changing
                market conditions and our deep understanding of customer needs. We have identified three key
                growth areas that align with our core competencies.
                
                Implementation Plan: The strategy will be implemented in three phases over the next 18 months.
                Each phase includes specific milestones, resource allocations, and success metrics. Regular
                progress reviews will ensure we stay on track and can make necessary adjustments.
                """,
                "metadata": {
                    "category": "business",
                    "author": "Strategy Team",
                    "date": "2024-01-15",
                    "type": "strategic_plan"
                }
            },
            {
                "id": "doc_002",
                "title": "Creative Writing Sample",
                "content": """
                In the heart of the mystical forest, where sunlight danced through emerald leaves like
                golden fairies, there existed a place that maps forgot and time overlooked. Sarah discovered
                this hidden sanctuary on a misty Tuesday morning, when the world seemed to hold its breath
                in anticipation of something extraordinary.
                
                The ancient trees whispered secrets in languages older than memory, their gnarled branches
                reaching toward the sky like weathered hands seeking divine connection. Each step deeper
                into the forest revealed wonders that defied explanation and challenged the boundaries
                of imagination.
                
                As Sarah ventured further, she realized that this wasn't just a forest—it was a living,
                breathing entity that pulsed with the rhythm of countless stories waiting to be told.
                The air itself seemed to shimmer with possibility, and every shadow held the promise of
                adventure and discovery.
                """,
                "metadata": {
                    "category": "creative",
                    "author": "Creative Team",
                    "date": "2024-02-20",
                    "type": "narrative"
                }
            },
            {
                "id": "doc_003",
                "title": "Technical Documentation",
                "content": """
                System Architecture Overview: The ResonanceOS v6 architecture consists of three primary
                layers: the generation layer, the feedback layer, and the optimization layer. Each layer
                serves specific functions and communicates through well-defined APIs.
                
                Generation Layer: This layer is responsible for content creation using the Human-Resonant
                Value (HRV) system. It includes the Planner Module, Sentence Generator, and Refiner Module.
                The HRV vectors guide the generation process to ensure human resonance.
                
                Feedback Layer: The Human-Resonant Feedback (HRF) system provides real-time assessment
                of generated content. It evaluates content across 8 dimensions and provides feedback
                scores that inform the optimization process.
                
                Implementation Details: The system is implemented using Python 3.8+ with no external
                dependencies for core functionality. The modular architecture allows for easy extension
                and customization based on specific use cases.
                """,
                "metadata": {
                    "category": "technical",
                    "author": "Engineering Team",
                    "date": "2024-03-10",
                    "type": "documentation"
                }
            },
            {
                "id": "doc_004",
                "title": "Marketing Campaign Content",
                "content": """
                Transform Your Business with Revolutionary AI Technology!
                
                Are you ready to experience the future of content creation? Our cutting-edge AI platform
                delivers unprecedented results that will transform how you connect with your audience!
                Imagine having the power to generate engaging, high-quality content that resonates
                with your readers every single time!
                
                Why Choose Our Solution?
                🚀 Boost engagement by 300% with human-resonant content
                💡 Save 80% of content creation time
                🎯 Achieve perfect brand consistency across all channels
                📈 See measurable ROI within the first month
                
                Don't wait! Join thousands of satisfied customers who have already revolutionized
                their content strategy. Your success story starts here!
                """,
                "metadata": {
                    "category": "marketing",
                    "author": "Marketing Team",
                    "date": "2024-03-01",
                    "type": "campaign"
                }
            },
            {
                "id": "doc_005",
                "title": "Research Paper Abstract",
                "content": """
                Abstract: This paper presents a comprehensive analysis of human-resonant value (HRV)
                systems in artificial intelligence applications. We propose a novel 8-dimensional framework
                for measuring content resonance and demonstrate its effectiveness through extensive
                empirical studies.
                
                Methodology: Our research employed mixed-methods approach, combining quantitative analysis
                of content metrics with qualitative assessment of reader engagement. We analyzed over
                10,000 content samples across multiple domains and demographics.
                
                Results: The findings indicate significant correlation between HRV scores and reader
                engagement metrics. Content optimized using our framework demonstrated 45% higher
                engagement rates compared to control groups. The 8-dimensional model proved robust across
                different content types and audiences.
                
                Conclusion: This research validates the effectiveness of HRV systems in content
                generation and provides a foundation for future developments in human-AI collaboration.
                """,
                "metadata": {
                    "category": "academic",
                    "author": "Research Team",
                    "date": "2024-02-15",
                    "type": "research_paper"
                }
            }
        ]
        
        return sample_documents
    
    def export_analysis_results(self, insights: Dict[str, Any], filename: str = "corpus_analysis_results.json"):
        """Export analysis results to JSON file"""
        print(f"\n💾 Exporting Analysis Results to {filename}")
        print("-" * 50)
        
        # Prepare export data
        export_data = {
            "analysis_timestamp": datetime.now().isoformat(),
            "corpus_insights": insights,
            "summary": {
                "total_documents": insights['overall_statistics']['total_documents'],
                "avg_hrv_score": insights['overall_statistics']['avg_hrv_score'],
                "quality_distribution": insights['quality_distribution'],
                "top_style": max(insights['style_distribution'].items(), key=lambda x: x[1])[0] if insights['style_distribution'] else None
            }
        }
        
        # Save to file
        output_path = Path(__file__).parent / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Results exported to {output_path}")
        return output_path
    
    def generate_visualization_data(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data for visualizations"""
        print("\n📊 Generating Visualization Data")
        print("-" * 40)
        
        # Quality distribution chart data
        quality_data = {
            "labels": list(insights['quality_distribution'].keys()),
            "values": list(insights['quality_distribution'].values())
        }
        
        # Style distribution chart data
        style_data = {
            "labels": list(insights['style_distribution'].keys()),
            "values": list(insights['style_distribution'].values())
        }
        
        # Dimension radar chart data
        dimension_data = {
            "labels": [d.replace('_', ' ').title() for d in self.dimensions],
            "values": [insights['dimension_statistics'][d]['mean'] for d in self.dimensions]
        }
        
        # Top documents chart data
        top_docs_data = {
            "labels": [doc['title'][:30] + '...' if len(doc['title']) > 30 else doc['title'] for doc in insights['top_performing_documents']],
            "values": [doc['hrv_score'] for doc in insights['top_performing_documents']]
        }
        
        viz_data = {
            "quality_distribution": quality_data,
            "style_distribution": style_data,
            "dimension_radar": dimension_data,
            "top_documents": top_docs_data
        }
        
        print("✅ Visualization data generated")
        return viz_data


def main():
    """Run the corpus analysis example"""
    print("🎯 ResonanceOS v6 - Corpus Analysis Example")
    print("=" * 60)
    print("This example demonstrates comprehensive corpus analysis capabilities.")
    print("You'll learn how to:")
    print("- Analyze individual documents")
    print("- Process batch document analysis")
    print("- Generate corpus-level insights")
    print("- Identify improvement areas")
    print("- Create recommendations")
    print("- Export and visualize results")
    print()
    
    try:
        analyzer = CorpusAnalyzer()
        
        # Create sample corpus
        print("📚 Creating Sample Corpus...")
        sample_corpus = analyzer.create_sample_corpus()
        print(f"✅ Created corpus with {len(sample_corpus)} documents")
        print()
        
        # Analyze corpus
        corpus_insights = analyzer.analyze_corpus_batch(sample_corpus)
        
        # Display key insights
        print("\n🔍 Key Corpus Insights:")
        print("-" * 30)
        print(f"Total Documents: {corpus_insights['overall_statistics']['total_documents']}")
        print(f"Average HRV Score: {corpus_insights['overall_statistics']['avg_hrv_score']:.3f}")
        print(f"Quality Distribution: {corpus_insights['quality_distribution']}")
        print(f"Style Distribution: {corpus_insights['style_distribution']}")
        
        # Show top performing documents
        print("\n🏆 Top Performing Documents:")
        for i, doc in enumerate(corpus_insights['top_performing_documents'][:3], 1):
            print(f"{i}. {doc['title']} - HRV: {doc['hrv_score']:.3f} ({doc['quality']})")
        
        # Show improvement areas
        if corpus_insights['improvement_areas']:
            print("\n⚠️  Improvement Areas:")
            for area in corpus_insights['improvement_areas']:
                print(f"• {area}")
        
        # Show recommendations
        print("\n💡 Recommendations:")
        for rec in corpus_insights['recommendations']:
            print(f"• {rec}")
        
        # Export results
        export_file = analyzer.export_analysis_results(corpus_insights)
        
        # Generate visualization data
        viz_data = analyzer.generate_visualization_data(corpus_insights)
        
        # Save visualization data
        viz_file = Path(__file__).parent / "visualization_data.json"
        with open(viz_file, 'w') as f:
            json.dump(viz_data, f, indent=2)
        
        print(f"\n📊 Visualization data saved to {viz_file}")
        
        print("\n🎉 Corpus Analysis Example Completed!")
        print("\nKey Achievements:")
        print("- ✅ Analyzed 5 diverse documents")
        print("- ✅ Generated comprehensive corpus insights")
        print("- ✅ Identified quality patterns and improvement areas")
        print("- ✅ Created actionable recommendations")
        print("- ✅ Exported results for further analysis")
        print("- ✅ Generated visualization data")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")


if __name__ == "__main__":
    main()
