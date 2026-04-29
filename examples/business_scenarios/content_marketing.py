#!/usr/bin/env python3
"""
Content Marketing Example

This example demonstrates how ResonanceOS v6 can be used for content marketing
applications, including blog posts, social media content, and marketing materials.
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.api.hr_server import SimpleRequest, hr_generate


class ContentMarketingGenerator:
    """Content marketing generator using ResonanceOS v6"""
    
    def __init__(self):
        self.writer = HumanResonantWriter()
        self.extractor = HRVExtractor()
        
        # Marketing content profiles
        self.profiles = {
            "blog_post": "creative_storytelling",
            "social_media": "marketing_enthusiastic", 
            "email_campaign": "persuasive_sales",
            "product_description": "tech_startup",
            "brand_story": "creative_storytelling"
        }
    
    def generate_blog_post(self, topic: str, tone: str = "professional") -> str:
        """Generate a blog post on a given topic"""
        print(f"📝 Generating blog post: {topic}")
        print("-" * 50)
        
        # Choose profile based on tone
        if tone == "professional":
            profile = "neutral_professional"
        elif tone == "creative":
            profile = "creative_storytelling"
        else:
            profile = "marketing_enthusiastic"
        
        # Create comprehensive prompt
        prompt = f"""
        Write a comprehensive blog post about {topic}. The post should:
        - Start with an engaging introduction
        - Include 3-4 main points with examples
        - Provide actionable insights
        - End with a compelling conclusion
        - Be approximately 800-1200 words
        - Use a {tone} tone appropriate for marketing
        """
        
        try:
            # Generate content
            content = self.writer.generate(prompt)
            
            # Extract HRV for analysis
            hrv_vector = self.extractor.extract(content)
            
            # Display results
            print(f"✅ Blog post generated successfully!")
            print(f"Length: {len(content)} characters")
            print(f"HRV Score: {sum(hrv_vector)/len(hrv_vector):.3f}")
            print(f"Profile used: {profile}")
            print()
            
            return content
            
        except Exception as e:
            print(f"❌ Error generating blog post: {e}")
            return None
    
    def generate_social_media_campaign(self, product: str, platform: str = "linkedin") -> list:
        """Generate social media content for a campaign"""
        print(f"📱 Generating social media campaign for: {product}")
        print(f"Platform: {platform}")
        print("-" * 50)
        
        # Platform-specific prompts
        platform_configs = {
            "linkedin": {
                "profile": "professional_business",
                "tone": "professional",
                "length": "professional",
                "hashtags": ["#innovation", "#business", "#technology"]
            },
            "twitter": {
                "profile": "marketing_enthusiastic", 
                "tone": "energetic",
                "length": "concise",
                "hashtags": ["#innovation", "#tech", "#startup"]
            },
            "instagram": {
                "profile": "creative_storytelling",
                "tone": "visual",
                "length": "engaging",
                "hashtags": ["#innovation", "#design", "#lifestyle"]
            }
        }
        
        config = platform_configs.get(platform, platform_configs["linkedin"])
        
        campaign_content = []
        
        # Generate multiple posts for campaign
        campaign_angles = [
            f"Introducing {product} - the future of innovation",
            f"Why {product} is changing the game",
            f"The story behind {product}",
            f"Customer success with {product}",
            f"Join the {product} revolution"
        ]
        
        for i, angle in enumerate(campaign_angles, 1):
            prompt = f"""
            Create a {config['length']} social media post for {platform} about {angle}.
            Make it {config['tone']} and engaging. Include relevant hashtags.
            """
            
            try:
                content = self.writer.generate(prompt)
                hrv_vector = self.extractor.extract(content)
                
                post_data = {
                    "platform": platform,
                    "angle": angle,
                    "content": content,
                    "hrv_score": sum(hrv_vector)/len(hrv_vector),
                    "hashtags": config["hashtags"]
                }
                
                campaign_content.append(post_data)
                
                print(f"✅ Post {i} generated (HRV: {post_data['hrv_score']:.3f})")
                
            except Exception as e:
                print(f"❌ Error generating post {i}: {e}")
        
        print(f"\n📊 Campaign Summary: {len(campaign_content)} posts generated")
        return campaign_content
    
    def generate_email_campaign(self, product: str, audience: str = "B2B") -> dict:
        """Generate email marketing campaign"""
        print(f"📧 Generating email campaign for: {product}")
        print(f"Target Audience: {audience}")
        print("-" * 50)
        
        campaign = {
            "product": product,
            "audience": audience,
            "emails": []
        }
        
        # Email sequence
        email_types = [
            ("announcement", "Product Announcement"),
            ("benefits", "Key Benefits"),
            ("social_proof", "Customer Success Stories"),
            ("urgency", "Limited Time Offer"),
            ("followup", "Follow-up")
        ]
        
        for email_type, email_title in email_types:
            print(f"Generating {email_title} email...")
            
            if audience == "B2B":
                tone = "professional"
                profile = "persuasive_sales"
            else:
                tone = "friendly"
                profile = "marketing_enthusiastic"
            
            prompt = f"""
            Write a {tone} marketing email for {email_title.lower()} about {product}.
            Target audience: {audience}. Include:
            - Compelling subject line
            - Personalized greeting
            - Key value propositions
            - Clear call-to-action
            - Professional signature
            """
            
            try:
                content = self.writer.generate(prompt)
                hrv_vector = self.extractor.extract(content)
                
                email_data = {
                    "type": email_type,
                    "title": email_title,
                    "content": content,
                    "hrv_score": sum(hrv_vector)/len(hrv_vector),
                    "subject": f"Exciting News About {product}!"
                }
                
                campaign["emails"].append(email_data)
                
                print(f"✅ {email_title} email generated (HRV: {email_data['hrv_score']:.3f})")
                
            except Exception as e:
                print(f"❌ Error generating {email_title} email: {e}")
        
        print(f"\n📊 Email Campaign Summary: {len(campaign['emails'])} emails generated")
        return campaign
    
    def generate_product_descriptions(self, product: str, features: list) -> dict:
        """Generate product descriptions for different contexts"""
        print(f"🛍️ Generating product descriptions for: {product}")
        print(f"Features: {', '.join(features)}")
        print("-" * 50)
        
        descriptions = {}
        
        # Different description types
        description_types = [
            ("short", "Short tagline for website header"),
            ("detailed", "Detailed description for product page"),
            ("technical", "Technical specifications for documentation"),
            ("marketing", "Marketing copy for advertisements"),
            ("social", "Social media friendly description")
        ]
        
        for desc_type, description_purpose in description_types:
            print(f"Generating {desc_type} description...")
            
            prompt = f"""
            Write a {desc_type} product description for {product}.
            Purpose: {description_purpose}
            Features: {', '.join(features)}
            Make it compelling and appropriate for {desc_type} use.
            """
            
            try:
                content = self.writer.generate(prompt)
                hrv_vector = self.extractor.extract(content)
                
                descriptions[desc_type] = {
                    "content": content,
                    "hrv_score": sum(hrv_vector)/len(hrv_vector),
                    "purpose": description_purpose
                }
                
                print(f"✅ {desc_type} description generated (HRV: {descriptions[desc_type]['hrv_score']:.3f})")
                
            except Exception as e:
                print(f"❌ Error generating {desc_type} description: {e}")
        
        print(f"\n📊 Product Descriptions Summary: {len(descriptions)} descriptions generated")
        return descriptions
    
    def generate_brand_story(self, company: str, values: list, mission: str) -> str:
        """Generate brand story and narrative"""
        print(f"🏢 Generating brand story for: {company}")
        print(f"Values: {', '.join(values)}")
        print(f"Mission: {mission}")
        print("-" * 50)
        
        prompt = f"""
        Write a compelling brand story for {company} that:
        - Incorporates the core values: {', '.join(values)}
        - Aligns with the mission: {mission}
        - Includes the company's origin story
        - Highlights key milestones
        - Looks toward the future vision
        - Is emotionally engaging and authentic
        - Approximately 600-800 words
        """
        
        try:
            content = self.writer.generate(prompt)
            hrv_vector = self.extractor.extract(content)
            
            print(f"✅ Brand story generated successfully!")
            print(f"Length: {len(content)} characters")
            print(f"HRV Score: {sum(hrv_vector)/len(hrv_vector):.3f}")
            
            return content
            
        except Exception as e:
            print(f"❌ Error generating brand story: {e}")
            return None
    
    def analyze_content_quality(self, content: str) -> dict:
        """Analyze content quality using HRV metrics"""
        print("🔍 Analyzing content quality...")
        print("-" * 30)
        
        hrv_vector = self.extractor.extract(content)
        
        # Quality assessment
        avg_score = sum(hrv_vector) / len(hrv_vector)
        
        if avg_score > 0.8:
            quality = "Excellent"
            recommendation = "Ready for publication"
        elif avg_score > 0.7:
            quality = "Good"
            recommendation = "Minor improvements recommended"
        elif avg_score > 0.6:
            quality = "Fair"
            recommendation = "Consider revisions before publication"
        else:
            quality = "Poor"
            recommendation = "Significant revisions needed"
        
        # Dimension analysis
        dimensions = [
            "Sentence Variance", "Emotional Valence", "Emotional Intensity",
            "Assertiveness", "Curiosity", "Metaphor Density", 
            "Storytelling", "Active Voice"
        ]
        
        analysis = {
            "overall_score": avg_score,
            "quality": quality,
            "recommendation": recommendation,
            "dimensions": {}
        }
        
        for i, dimension in enumerate(dimensions):
            value = hrv_vector[i]
            analysis["dimensions"][dimension] = {
                "value": value,
                "assessment": "Strong" if value > 0.7 else "Moderate" if value > 0.4 else "Weak"
            }
        
        print(f"Quality Assessment: {quality}")
        print(f"Overall Score: {avg_score:.3f}")
        print(f"Recommendation: {recommendation}")
        
        return analysis


def content_calendar_example():
    """Generate a content calendar example"""
    print("\n📅 Content Calendar Generation Example")
    print("=" * 60)
    
    generator = ContentMarketingGenerator()
    
    # Content calendar for a tech startup
    content_calendar = {
        "company": "TechInnovate AI",
        "period": "One Month",
        "themes": [
            "AI Innovation",
            "Digital Transformation", 
            "Customer Success",
            "Industry Insights",
            "Product Updates"
        ],
        "content": []
    }
    
    print(f"Generating content calendar for {content_calendar['company']}")
    print(f"Period: {content_calendar['period']}")
    print(f"Themes: {', '.join(content_calendar['themes'])}")
    print()
    
    # Generate content for each theme
    for week, theme in enumerate(content_calendar['themes'], 1):
        print(f"Week {week}: {theme}")
        print("-" * 30)
        
        # Blog post
        blog_content = generator.generate_blog_post(theme, "professional")
        
        # Social media posts
        social_posts = generator.generate_social_media_campaign(
            f"{content_calendar['company']} - {theme}", 
            "linkedin"
        )
        
        # Add to calendar
        week_content = {
            "week": week,
            "theme": theme,
            "blog_post": {
                "title": f"The Future of {theme}",
                "content": blog_content[:200] + "..." if blog_content else None
            },
            "social_media": {
                "posts": len(social_posts),
                "avg_hrv": sum(p['hrv_score'] for p in social_posts) / len(social_posts) if social_posts else 0
            }
        }
        
        content_calendar['content'].append(week_content)
        
        print(f"✅ Week {week} content generated")
        print()
    
    return content_calendar


def marketing_campaign_example():
    """Complete marketing campaign example"""
    print("\n🚀 Complete Marketing Campaign Example")
    print("=" * 60)
    
    generator = ContentMarketingGenerator()
    
    # Campaign details
    campaign = {
        "product": "AI-Powered Analytics Platform",
        "company": "DataInsight Pro",
        "duration": "4 weeks",
        "target_audience": "B2B technology companies"
    }
    
    print(f"Creating marketing campaign for {campaign['product']}")
    print(f"Company: {campaign['company']}")
    print(f"Duration: {campaign['duration']}")
    print(f"Target: {campaign['target_audience']}")
    print()
    
    campaign_results = {}
    
    # 1. Brand Story
    print("1. Creating Brand Story...")
    brand_story = generator.generate_brand_story(
        campaign['company'],
        ["Innovation", "Data-Driven", "Customer Success", "Excellence"],
        "Empowering businesses with AI-driven insights"
    )
    campaign_results['brand_story'] = brand_story
    
    # 2. Product Descriptions
    print("\n2. Creating Product Descriptions...")
    product_features = [
        "Real-time analytics",
        "AI-powered insights",
        "Customizable dashboards",
        "Predictive modeling",
        "Integration capabilities"
    ]
    product_descriptions = generator.generate_product_descriptions(
        campaign['product'],
        product_features
    )
    campaign_results['product_descriptions'] = product_descriptions
    
    # 3. Email Campaign
    print("\n3. Creating Email Campaign...")
    email_campaign = generator.generate_email_campaign(
        campaign['product'],
        "B2B"
    )
    campaign_results['email_campaign'] = email_campaign
    
    # 4. Social Media Campaign
    print("\n4. Creating Social Media Campaign...")
    social_campaign = generator.generate_social_media_campaign(
        campaign['product'],
        "linkedin"
    )
    campaign_results['social_campaign'] = social_campaign
    
    # 5. Blog Content
    print("\n5. Creating Blog Content...")
    blog_topics = [
        "The Future of AI in Business Analytics",
        "How Real-Time Data Drives Decision Making",
        "Maximizing ROI with AI-Powered Insights"
    ]
    
    blog_content = []
    for topic in blog_topics:
        content = generator.generate_blog_post(topic, "professional")
        blog_content.append({
            "topic": topic,
            "content": content[:300] + "..." if content else None
        })
    
    campaign_results['blog_content'] = blog_content
    
    # Campaign Summary
    print("\n📊 Campaign Summary:")
    print("-" * 40)
    print(f"Brand Story: {'✅ Generated' if brand_story else '❌ Failed'}")
    print(f"Product Descriptions: {len(product_descriptions)} generated")
    print(f"Email Campaign: {len(email_campaign['emails'])} emails")
    print(f"Social Media: {len(social_campaign)} posts")
    print(f"Blog Posts: {len(blog_content)} posts")
    
    # Calculate average HRV scores
    all_hrv_scores = []
    
    if social_campaign:
        all_hrv_scores.extend([p['hrv_score'] for p in social_campaign])
    
    if email_campaign and email_campaign['emails']:
        all_hrv_scores.extend([e['hrv_score'] for e in email_campaign['emails']])
    
    avg_hrv = sum(all_hrv_scores) / len(all_hrv_scores) if all_hrv_scores else 0
    
    print(f"Average HRV Score: {avg_hrv:.3f}")
    
    return campaign_results


def performance_analysis_example():
    """Analyze marketing content performance"""
    print("\n📈 Marketing Performance Analysis")
    print("=" * 60)
    
    generator = ContentMarketingGenerator()
    
    # Sample content for analysis
    sample_contents = {
        "high_performing": "Transform your business with our revolutionary AI platform that delivers unprecedented insights and drives exceptional growth through advanced machine learning algorithms and real-time data processing.",
        "medium_performing": "Our AI platform helps businesses analyze data and make better decisions. It includes features for real-time analytics and predictive modeling.",
        "low_performing": "AI platform for business. Has analytics. Good for data."
    }
    
    performance_results = {}
    
    for content_type, content in sample_contents.items():
        print(f"Analyzing {content_type} content...")
        
        analysis = generator.analyze_content_quality(content)
        performance_results[content_type] = analysis
        
        print(f"Quality: {analysis['quality']}")
        print(f"Score: {analysis['overall_score']:.3f}")
        print(f"Recommendation: {analysis['recommendation']}")
        print()
    
    # Performance comparison
    print("📊 Performance Comparison:")
    print("-" * 30)
    
    for content_type, analysis in performance_results.items():
        print(f"{content_type:<20}: {analysis['overall_score']:.3f} ({analysis['quality']})")
    
    # Recommendations for improvement
    print("\n💡 Performance Improvement Recommendations:")
    print("-" * 40)
    
    low_performing = performance_results.get("low_performing")
    if low_performing and low_performing['overall_score'] < 0.6:
        print("For low-performing content:")
        print("- Increase sentence variety")
        print("- Add emotional elements")
        print("- Use more active voice")
        print("- Include storytelling elements")
        print("- Add curiosity-inducing questions")
    
    return performance_results


def main():
    """Run all content marketing examples"""
    print("🎯 ResonanceOS v6 - Content Marketing Examples")
    print("=" * 60)
    print("This example demonstrates content marketing applications.")
    print("You'll learn how to:")
    print("- Generate blog posts and articles")
    print("- Create social media campaigns")
    print("- Develop email marketing campaigns")
    print("- Write product descriptions")
    print("- Create brand stories")
    print("- Analyze content quality")
    print("- Plan content calendars")
    print("- Execute complete marketing campaigns")
    print()
    
    try:
        # Run examples
        content_calendar = content_calendar_example()
        campaign_results = marketing_campaign_example()
        performance_analysis = performance_analysis_example()
        
        print("\n🎉 All content marketing examples completed successfully!")
        print("\nKey Takeaways:")
        print("- ResonanceOS can generate diverse marketing content types")
        print("- HRV analysis ensures content quality and engagement")
        print("- Different profiles enable various marketing tones")
        print("- Quality assessment helps optimize content performance")
        print("- Campaign planning becomes systematic and efficient")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")


if __name__ == "__main__":
    main()
