#!/usr/bin/env python3
"""
Creative Story Generation Example

This example demonstrates how ResonanceOS v6 can be used for creative writing
applications, including story generation, narrative development, and creative content.
"""

import sys
import os
import json
import random
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.hrv_extractor import HRVExtractor
from resonance_os.api.hr_server import SimpleRequest, hr_generate


class CreativeStoryGenerator:
    """Creative story generator using ResonanceOS v6"""
    
    def __init__(self):
        self.writer = HumanResonantWriter()
        self.extractor = HRVExtractor()
        
        # Creative writing profiles
        self.profiles = {
            "fantasy": "creative_storytelling",
            "scifi": "creative_storytelling",
            "mystery": "creative_storytelling",
            "romance": "creative_storytelling",
            "thriller": "creative_storytelling"
        }
        
        # Story elements
        self.genres = {
            "fantasy": ["magic", "dragons", "wizards", "kingdoms", "quests", "ancient_prophecies"],
            "scifi": ["spaceships", "aliens", "planets", "technology", "future", "artificial_intelligence"],
            "mystery": ["detectives", "clues", "suspects", "evidence", "investigation", "secrets"],
            "romance": ["love", "relationships", "emotions", "connections", "heart", "passion"],
            "thriller": ["suspense", "danger", "mystery", "action", "adventure", "conflict"]
        }
    
    def generate_short_story(self, genre: str, theme: str, length: str = "short") -> str:
        """Generate a short story in specified genre"""
        print(f"📖 Generating {genre} short story: {theme}")
        print(f"Length: {length}")
        print("-" * 50)
        
        # Get genre elements
        genre_elements = self.genres.get(genre, ["story", "characters", "plot"])
        
        # Create story prompt
        if length == "short":
            word_count = "500-800"
            paragraphs = "3-4"
        elif length == "medium":
            word_count = "1000-1500"
            paragraphs = "5-7"
        else:  # long
            word_count = "2000-3000"
            paragraphs = "8-10"
        
        prompt = f"""
        Write a {genre} short story about {theme}. The story should:
        - Include elements like {', '.join(random.sample(genre_elements, 3))}
        - Be approximately {word_count} words
        - Have {paragraphs} paragraphs
        - Include engaging characters and plot development
        - Have a clear beginning, middle, and end
        - Be emotionally engaging and memorable
        - Use creative and descriptive language
        """
        
        try:
            # Generate story
            story = self.writer.generate(prompt)
            
            # Extract HRV for analysis
            hrv_vector = self.extractor.extract(story)
            
            # Display results
            print(f"✅ {genre} story generated successfully!")
            print(f"Length: {len(story)} characters")
            print(f"HRV Score: {sum(hrv_vector)/len(hrv_vector):.3f}")
            print(f"Story preview: {story[:150]}...")
            print()
            
            return story
            
        except Exception as e:
            print(f"❌ Error generating {genre} story: {e}")
            return None
    
    def generate_story_outline(self, genre: str, concept: str) -> dict:
        """Generate a story outline structure"""
        print(f"📋 Generating {genre} story outline: {concept}")
        print("-" * 50)
        
        prompt = f"""
        Create a detailed story outline for a {genre} story about {concept}.
        Include:
        - Title suggestions
        - Character descriptions
        - Setting details
        - Plot structure (beginning, middle, end)
        - Key scenes or chapters
        - Themes and motifs
        - Conflict and resolution
        """
        
        try:
            outline = self.writer.generate(prompt)
            hrv_vector = self.extractor.extract(outline)
            
            # Parse outline into structured format
            structured_outline = {
                "genre": genre,
                "concept": concept,
                "outline": outline,
                "hrv_score": sum(hrv_vector)/len(hrv_vector),
                "generated_at": "2026-03-09"
            }
            
            print(f"✅ Story outline generated successfully!")
            print(f"HRV Score: {structured_outline['hrv_score']:.3f}")
            print(f"Outline preview: {outline[:200]}...")
            print()
            
            return structured_outline
            
        except Exception as e:
            print(f"❌ Error generating story outline: {e}")
            return None
    
    def generate_character_profiles(self, story_type: str, character_count: int = 3) -> list:
        """Generate character profiles for stories"""
        print(f"👥 Generating {character_count} character profiles for {story_type}")
        print("-" * 50)
        
        characters = []
        
        for i in range(character_count):
            character_type = ["protagonist", "antagonist", "supporting", "mentor", "love_interest"][i % 5]
            
            prompt = f"""
            Create a detailed character profile for a {character_type} in a {story_type} story.
            Include:
            - Name and background
            - Physical description
            - Personality traits
            - Motivations and goals
            - Strengths and weaknesses
            - Character arc development
            """
            
            try:
                profile = self.writer.generate(prompt)
                hrv_vector = self.extractor.extract(profile)
                
                character_data = {
                    "character_type": character_type,
                    "profile": profile,
                    "hrv_score": sum(hrv_vector)/len(hrv_vector)
                }
                
                characters.append(character_data)
                
                print(f"✅ {character_type.title()} profile generated (HRV: {character_data['hrv_score']:.3f})")
                
            except Exception as e:
                print(f"❌ Error generating {character_type} profile: {e}")
        
        print(f"\n📊 Character Generation Summary: {len(characters)} profiles created")
        return characters
    
    def generate_dialogue_scene(self, characters: list, setting: str, situation: str) -> str:
        """Generate a dialogue scene between characters"""
        print(f"💬 Generating dialogue scene")
        print(f"Characters: {len(characters)}")
        print(f"Setting: {setting}")
        print(f"Situation: {situation}")
        print("-" * 50)
        
        character_names = [f"Character_{i+1}" for i in range(len(characters))]
        
        prompt = f"""
        Write a dialogue scene between {len(characters)} characters in {setting}.
        Situation: {situation}
        Characters: {', '.join(character_names)}
        
        The dialogue should:
        - Reveal character personalities
        - Advance the plot
        - Include natural conversation flow
        - Show emotions and reactions
        - Have clear beginning and end
        - Be approximately 300-500 words
        """
        
        try:
            dialogue = self.writer.generate(prompt)
            hrv_vector = self.extractor.extract(dialogue)
            
            print(f"✅ Dialogue scene generated successfully!")
            print(f"Length: {len(dialogue)} characters")
            print(f"HRV Score: {sum(hrv_vector)/len(hrv_vector):.3f}")
            print(f"Dialogue preview: {dialogue[:150]}...")
            print()
            
            return dialogue
            
        except Exception as e:
            print(f"❌ Error generating dialogue scene: {e}")
            return None
    
    def generate_world_building(self, genre: str, world_type: str) -> dict:
        """Generate world-building details"""
        print(f"🌍 Generating {genre} world: {world_type}")
        print("-" * 50)
        
        prompt = f"""
        Create detailed world-building for a {genre} {world_type}.
        Include:
        - Geography and environment
        - Culture and society
        - History and timeline
        - Rules and systems (magic, technology, etc.)
        - Factions and groups
        - Unique features and landmarks
        """
        
        try:
            world_info = self.writer.generate(prompt)
            hrv_vector = self.extractor.extract(world_info)
            
            world_data = {
                "genre": genre,
                "world_type": world_type,
                "world_info": world_info,
                "hrv_score": sum(hrv_vector)/len(hrv_vector)
            }
            
            print(f"✅ World-building generated successfully!")
            print(f"HRV Score: {world_data['hrv_score']:.3f}")
            print(f"World preview: {world_info[:200]}...")
            print()
            
            return world_data
            
        except Exception as e:
            print(f"❌ Error generating world-building: {e}")
            return None
    
    def generate_story_series_outline(self, series_concept: str, book_count: int = 3) -> dict:
        """Generate outline for a story series"""
        print(f"📚 Generating story series outline")
        print(f"Concept: {series_concept}")
        print(f"Books: {book_count}")
        print("-" * 50)
        
        series_outline = {
            "series_concept": series_concept,
            "book_count": book_count,
            "books": []
        }
        
        for book_num in range(1, book_count + 1):
            print(f"Generating Book {book_num} outline...")
            
            prompt = f"""
            Create an outline for Book {book_num} in a series about {series_concept}.
            Include:
            - Book title
            - Main plot points
            - Character development
            - Key conflicts
            - Setting evolution
            - Cliffhanger elements
            """
            
            try:
                book_outline = self.writer.generate(prompt)
                hrv_vector = self.extractor.extract(book_outline)
                
                book_data = {
                    "book_number": book_num,
                    "outline": book_outline,
                    "hrv_score": sum(hrv_vector)/len(hrv_vector)
                }
                
                series_outline["books"].append(book_data)
                
                print(f"✅ Book {book_num} outline generated (HRV: {book_data['hrv_score']:.3f})")
                
            except Exception as e:
                print(f"❌ Error generating Book {book_num} outline: {e}")
        
        print(f"\n📊 Series Outline Summary: {len(series_outline['books'])} books outlined")
        return series_outline
    
    def analyze_creative_writing(self, content: str) -> dict:
        """Analyze creative writing quality"""
        print("🔍 Analyzing creative writing quality...")
        print("-" * 30)
        
        hrv_vector = self.extractor.extract(content)
        
        # Creative writing assessment
        avg_score = sum(hrv_vector) / len(hrv_vector)
        
        # Creative dimensions
        creative_scores = {
            "storytelling": hrv_vector[6],  # Storytelling Index
            "emotion": hrv_vector[1] + hrv_vector[2],  # Emotional Valence + Intensity
            "creativity": hrv_vector[4] + hrv_vector[5],  # Curiosity + Metaphor
            "engagement": avg_score
        }
        
        # Quality assessment
        if avg_score > 0.8:
            quality = "Exceptional"
            feedback = "Outstanding creative writing with strong engagement"
        elif avg_score > 0.7:
            quality = "Excellent"
            feedback = "High-quality creative writing with good engagement"
        elif avg_score > 0.6:
            quality = "Good"
            feedback = "Solid creative writing with room for improvement"
        else:
            quality = "Needs Work"
            feedback = "Creative writing requires significant improvements"
        
        analysis = {
            "overall_score": avg_score,
            "quality": quality,
            "feedback": feedback,
            "creative_scores": creative_scores,
            "recommendations": []
        }
        
        # Generate recommendations
        if creative_scores["storytelling"] < 0.6:
            analysis["recommendations"].append("Strengthen narrative structure and storytelling elements")
        
        if creative_scores["emotion"] < 1.0:
            analysis["recommendations"].append("Increase emotional depth and reader engagement")
        
        if creative_scores["creativity"] < 1.0:
            analysis["recommendations"].append("Add more creative elements and metaphors")
        
        if hrv_vector[0] < 0.5:  # Sentence Variance
            analysis["recommendations"].append("Vary sentence structure for better flow")
        
        print(f"Quality Assessment: {quality}")
        print(f"Overall Score: {avg_score:.3f}")
        print(f"Feedback: {feedback}")
        
        if analysis["recommendations"]:
            print("Recommendations:")
            for rec in analysis["recommendations"]:
                print(f"- {rec}")
        
        return analysis


def interactive_story_example():
    """Interactive story generation example"""
    print("\n🎮 Interactive Story Generation")
    print("=" * 60)
    
    generator = CreativeStoryGenerator()
    
    # Interactive story creation
    print("Let's create an interactive story together!")
    print()
    
    # Get user preferences (simulated for example)
    story_preferences = {
        "genre": "fantasy",
        "theme": "a young wizard's first adventure",
        "length": "short",
        "include_dialogue": True,
        "include_world_building": True
    }
    
    print(f"Genre: {story_preferences['genre']}")
    print(f"Theme: {story_preferences['theme']}")
    print(f"Length: {story_preferences['length']}")
    print()
    
    # Generate main story
    main_story = generator.generate_short_story(
        story_preferences['genre'],
        story_preferences['theme'],
        story_preferences['length']
    )
    
    if main_story:
        # Generate characters
        characters = generator.generate_character_profiles(
            story_preferences['genre'],
            3
        )
        
        # Generate dialogue scene
        if story_preferences['include_dialogue'] and characters:
            dialogue = generator.generate_dialogue_scene(
                characters[:2],
                "magical forest",
                "discovering an ancient artifact"
            )
        
        # Generate world building
        if story_preferences['include_world_building']:
            world_info = generator.generate_world_building(
                story_preferences['genre'],
                "magical kingdom"
            )
        
        # Analyze the creative writing
        analysis = generator.analyze_creative_writing(main_story)
        
        print("\n🎉 Interactive Story Creation Completed!")
        print(f"Story Quality: {analysis['quality']}")
        print(f"Overall Score: {analysis['overall_score']:.3f}")
    
    return main_story


def genre_comparison_example():
    """Compare story generation across different genres"""
    print("\n📚 Genre Comparison Example")
    print("=" * 60)
    
    generator = CreativeStoryGenerator()
    
    # Test same theme across different genres
    theme = "a journey of self-discovery"
    genres = ["fantasy", "scifi", "mystery", "romance"]
    
    genre_results = {}
    
    for genre in genres:
        print(f"Generating {genre} story...")
        story = generator.generate_short_story(genre, theme, "short")
        
        if story:
            analysis = generator.analyze_creative_writing(story)
            genre_results[genre] = {
                "story": story[:200] + "...",
                "analysis": analysis
            }
    
    # Compare results
    print("\n📊 Genre Comparison Results:")
    print("-" * 40)
    
    for genre, result in genre_results.items():
        analysis = result['analysis']
        print(f"{genre:<10}: Score {analysis['overall_score']:.3f} ({analysis['quality']})")
    
    # Creative scores comparison
    print("\n🎨 Creative Scores Comparison:")
    print("-" * 40)
    
    creative_dimensions = ["storytelling", "emotion", "creativity", "engagement"]
    
    for dimension in creative_dimensions:
        print(f"\n{dimension.title()}:")
        for genre, result in genre_results.items():
            score = result['analysis']['creative_scores'][dimension]
            print(f"  {genre:<10}: {score:.3f}")
    
    return genre_results


def collaborative_writing_example():
    """Demonstrate collaborative writing features"""
    print("\n🤝 Collaborative Writing Example")
    print("=" * 60)
    
    generator = CreativeStoryGenerator()
    
    # Multiple authors contributing to a story
    story_sections = []
    
    print("Creating collaborative story with multiple 'authors'...")
    print()
    
    # Section 1: Opening
    print("Author 1: Writing opening section...")
    opening_prompt = "Write the opening of a mystery story set in a Victorian mansion. Introduce the main character and the initial mystery."
    opening = generator.writer.generate(opening_prompt)
    story_sections.append(opening)
    print("✅ Opening section completed")
    
    # Section 2: Development
    print("\nAuthor 2: Writing development section...")
    dev_prompt = "Continue the mystery story. Develop the plot with new clues and introduce a compelling subplot."
    development = generator.writer.generate(dev_prompt)
    story_sections.append(development)
    print("✅ Development section completed")
    
    # Section 3: Climax
    print("\nAuthor 3: Writing climax section...")
    climax_prompt = "Write the climax of the mystery story. Reveal the truth behind the mystery and create maximum tension."
    climax = generator.writer.generate(climax_prompt)
    story_sections.append(climax)
    print("✅ Climax section completed")
    
    # Section 4: Resolution
    print("\nAuthor 4: Writing resolution section...")
    resolution_prompt = "Write the resolution of the mystery story. Tie up loose ends and provide a satisfying conclusion."
    resolution = generator.writer.generate(resolution_prompt)
    story_sections.append(resolution)
    print("✅ Resolution section completed")
    
    # Combine sections
    collaborative_story = "\n\n".join(story_sections)
    
    # Analyze the collaborative work
    analysis = generator.analyze_creative_writing(collaborative_story)
    
    print(f"\n📊 Collaborative Story Results:")
    print(f"Total Length: {len(collaborative_story)} characters")
    print(f"Sections: {len(story_sections)}")
    print(f"Quality: {analysis['quality']}")
    print(f"Overall Score: {analysis['overall_score']:.3f}")
    
    return collaborative_story, analysis


def main():
    """Run all creative writing examples"""
    print("🎯 ResonanceOS v6 - Creative Story Generation Examples")
    print("=" * 60)
    print("This example demonstrates creative writing applications.")
    print("You'll learn how to:")
    print("- Generate short stories in different genres")
    print("- Create story outlines and structures")
    print("- Develop character profiles")
    print("- Write dialogue scenes")
    print("- Build fictional worlds")
    print("- Plan story series")
    print("- Analyze creative writing quality")
    print("- Create interactive stories")
    print("- Compare genres and styles")
    print("- Enable collaborative writing")
    print()
    
    try:
        # Run examples
        interactive_story = interactive_story_example()
        genre_comparison = genre_comparison_example()
        collaborative_story, collab_analysis = collaborative_writing_example()
        
        print("\n🎉 All creative writing examples completed successfully!")
        print("\nKey Takeaways:")
        print("- ResonanceOS excels at creative content generation")
        print("- Different genres can be achieved with profile selection")
        print("- HRV analysis ensures creative quality")
        print("- Collaborative writing becomes systematic")
        print("- Story structure and character development are supported")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your ResonanceOS installation and configuration")


if __name__ == "__main__":
    main()
