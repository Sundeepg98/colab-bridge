"""
Claude Enhancer - Advanced Prompt Enhancement using Claude API

This module fully exploits Claude's capabilities to provide:
- Deep prompt analysis and understanding
- Multiple creative variations using different Claude models
- Prompt evaluation and scoring
- Story narrative generation
- Sensitive content handling with nuanced understanding
- Artistic and cinematographic detail generation
- Complex theme understanding and appropriate reframing
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import anthropic
from anthropic import AsyncAnthropic
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancementMode(Enum):
    """Different enhancement modes for various use cases"""
    CREATIVE = "creative"
    TECHNICAL = "technical"
    NARRATIVE = "narrative"
    CINEMATIC = "cinematic"
    ARTISTIC = "artistic"
    SENSITIVE = "sensitive"
    COMPREHENSIVE = "comprehensive"


@dataclass
class EnhancementResult:
    """Container for enhancement results"""
    original_prompt: str
    enhanced_prompt: str
    variations: List[str]
    analysis: Dict[str, Any]
    scores: Dict[str, float]
    narrative_context: Optional[str]
    artistic_details: Optional[str]
    cinematography: Optional[str]
    content_warnings: List[str]
    themes: List[str]
    mode: EnhancementMode


class ClaudeEnhancer:
    """Advanced prompt enhancer leveraging Claude's full capabilities"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Claude API key"""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Claude API key not found. Set ANTHROPIC_API_KEY environment variable.")
        
        # Initialize both sync and async clients
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.async_client = AsyncAnthropic(api_key=self.api_key)
        
        # Model configurations for different purposes
        self.models = {
            'analysis': 'claude-3-5-sonnet-20241022',  # Best available for analysis
            'creative': 'claude-3-5-sonnet-20241022',  # Latest Sonnet for creativity
            'quick': 'claude-3-haiku-20240307',  # Fast iterations
            'evaluation': 'claude-3-5-sonnet-20241022'  # Best available for evaluation
        }
    
    async def enhance_prompt(self, prompt: str, mode: EnhancementMode = EnhancementMode.COMPREHENSIVE) -> EnhancementResult:
        """Main enhancement method that orchestrates all capabilities"""
        logger.info(f"Enhancing prompt with mode: {mode.value}")
        
        # Run all enhancement tasks in parallel for maximum efficiency
        tasks = [
            self._analyze_prompt(prompt),
            self._generate_variations(prompt, mode),
            self._evaluate_prompt(prompt),
            self._generate_narrative(prompt),
            self._generate_artistic_details(prompt),
            self._analyze_themes(prompt),
            self._handle_sensitive_content(prompt)
        ]
        
        results = await asyncio.gather(*tasks)
        
        analysis, variations, scores, narrative, artistic, themes, content_analysis = results
        
        # Generate final enhanced prompt based on all insights
        enhanced_prompt = await self._create_enhanced_prompt(
            prompt, analysis, narrative, artistic, themes, mode
        )
        
        # Extract cinematography if in cinematic mode
        cinematography = None
        if mode in [EnhancementMode.CINEMATIC, EnhancementMode.COMPREHENSIVE]:
            cinematography = await self._generate_cinematography(enhanced_prompt)
        
        return EnhancementResult(
            original_prompt=prompt,
            enhanced_prompt=enhanced_prompt,
            variations=variations,
            analysis=analysis,
            scores=scores,
            narrative_context=narrative,
            artistic_details=artistic,
            cinematography=cinematography,
            content_warnings=content_analysis['warnings'],
            themes=themes,
            mode=mode
        )
    
    async def _analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Deep analysis of prompt structure, intent, and potential"""
        analysis_prompt = f"""Analyze this video generation prompt in extreme detail:

"{prompt}"

Provide a comprehensive analysis including:
1. Core Subject/Action: What is being depicted
2. Visual Elements: Objects, characters, settings
3. Mood/Atmosphere: Emotional tone and feeling
4. Technical Aspects: Camera work, lighting, effects implied
5. Narrative Elements: Story, progression, context
6. Artistic Style: Visual style, genre, influences
7. Strengths: What works well
8. Weaknesses: What could be improved
9. Missing Elements: What would enhance the prompt
10. Potential Issues: Ambiguities or problems

Format as JSON with these exact keys."""

        response = await self.async_client.messages.create(
            model=self.models['analysis'],
            max_tokens=2000,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": analysis_prompt
            }]
        )
        
        try:
            # Extract JSON from response
            json_str = response.content[0].text
            if '```json' in json_str:
                json_str = json_str.split('```json')[1].split('```')[0]
            return json.loads(json_str)
        except:
            # Fallback to text analysis
            return {"raw_analysis": response.content[0].text}
    
    async def _generate_variations(self, prompt: str, mode: EnhancementMode) -> List[str]:
        """Generate multiple creative variations using different approaches"""
        variation_prompt = f"""Generate 5 highly creative variations of this video prompt, each with a different approach:

Original: "{prompt}"

Enhancement Mode: {mode.value}

Create variations that:
1. Dramatic/Cinematic version - Add drama, tension, cinematic flair
2. Artistic/Stylized version - Emphasize unique visual style and artistry
3. Detailed/Technical version - Add technical camera and lighting details
4. Narrative/Story version - Enhance story and emotional elements
5. Experimental/Avant-garde version - Push creative boundaries

Each variation should be a complete, standalone prompt that could generate an amazing video.
Number each variation and make them substantially different from each other."""

        response = await self.async_client.messages.create(
            model=self.models['creative'],
            max_tokens=3000,
            temperature=0.8,
            messages=[{
                "role": "user",
                "content": variation_prompt
            }]
        )
        
        # Parse variations from response
        text = response.content[0].text
        variations = []
        
        # Extract numbered variations
        lines = text.split('\n')
        current_variation = []
        
        for line in lines:
            if line.strip() and any(line.strip().startswith(f"{i}.") for i in range(1, 6)):
                if current_variation:
                    variations.append(' '.join(current_variation).strip())
                current_variation = [line.split('.', 1)[1].strip()]
            elif current_variation and line.strip():
                current_variation.append(line.strip())
        
        if current_variation:
            variations.append(' '.join(current_variation).strip())
        
        return variations[:5]  # Ensure we have max 5 variations
    
    async def _evaluate_prompt(self, prompt: str) -> Dict[str, float]:
        """Evaluate and score the prompt on multiple dimensions"""
        eval_prompt = f"""Evaluate this video generation prompt on multiple dimensions:

"{prompt}"

Score each dimension from 0.0 to 1.0:
1. Clarity: How clear and unambiguous is the prompt
2. Creativity: How creative and original
3. Visual_Richness: How visually detailed and rich
4. Technical_Feasibility: How feasible to generate
5. Emotional_Impact: Potential emotional resonance
6. Narrative_Coherence: Story/sequence clarity
7. Artistic_Merit: Artistic and aesthetic value
8. Uniqueness: How unique compared to common prompts
9. Completeness: How complete the description is
10. Overall_Quality: Overall prompt quality

Provide scores as JSON with dimension names as keys and scores as float values.
Also include a "total_score" that averages all dimensions."""

        response = await self.async_client.messages.create(
            model=self.models['evaluation'],
            max_tokens=1000,
            temperature=0.2,
            messages=[{
                "role": "user",
                "content": eval_prompt
            }]
        )
        
        try:
            json_str = response.content[0].text
            if '```json' in json_str:
                json_str = json_str.split('```json')[1].split('```')[0]
            scores = json.loads(json_str)
            
            # Calculate total if not present
            if 'total_score' not in scores:
                scores['total_score'] = sum(scores.values()) / len(scores)
            
            return scores
        except:
            # Fallback scores
            return {
                "clarity": 0.5,
                "creativity": 0.5,
                "visual_richness": 0.5,
                "technical_feasibility": 0.5,
                "emotional_impact": 0.5,
                "narrative_coherence": 0.5,
                "artistic_merit": 0.5,
                "uniqueness": 0.5,
                "completeness": 0.5,
                "overall_quality": 0.5,
                "total_score": 0.5
            }
    
    async def _generate_narrative(self, prompt: str) -> str:
        """Generate rich narrative context and story elements"""
        narrative_prompt = f"""Create a rich narrative context for this video prompt:

"{prompt}"

Develop:
1. Backstory: What led to this moment
2. Setting: Detailed world-building and environment
3. Characters: Who/what is involved and their motivations
4. Emotional Journey: The emotional arc of the video
5. Symbolic Meaning: Deeper themes and symbolism
6. Moment Significance: Why this particular moment matters

Write this as an evocative, cinematic narrative description that would help a video generator understand the deeper context and create something meaningful."""

        response = await self.async_client.messages.create(
            model=self.models['creative'],
            max_tokens=1500,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": narrative_prompt
            }]
        )
        
        return response.content[0].text
    
    async def _generate_artistic_details(self, prompt: str) -> str:
        """Generate detailed artistic and aesthetic descriptions"""
        artistic_prompt = f"""Create rich artistic details for this video prompt:

"{prompt}"

Describe:
1. Visual Style: Specific artistic style, influences, aesthetic
2. Color Palette: Detailed color choices and their emotional impact
3. Lighting: Specific lighting setup and mood
4. Composition: Frame composition, rule of thirds, visual balance
5. Texture and Materials: Surface qualities, materials, tactile elements
6. Movement and Rhythm: How elements move, pacing, visual rhythm
7. Atmospheric Effects: Fog, particles, environmental effects
8. Artistic References: Similar works, artistic movements, inspiration

Write as detailed artistic direction that would result in a visually stunning video."""

        response = await self.async_client.messages.create(
            model=self.models['creative'],
            max_tokens=1500,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": artistic_prompt
            }]
        )
        
        return response.content[0].text
    
    async def _generate_cinematography(self, prompt: str) -> str:
        """Generate detailed cinematographic instructions"""
        cinema_prompt = f"""Create detailed cinematographic instructions for this video:

"{prompt}"

Include:
1. Camera Movement: Specific camera moves (dolly, crane, handheld, etc.)
2. Shot Types: Wide, medium, close-up, extreme close-up progression
3. Lens Choice: Focal length and its effect (wide angle distortion, telephoto compression)
4. Depth of Field: What's in focus, bokeh quality
5. Frame Rate: Standard, slow motion, time-lapse considerations
6. Transitions: How shots connect, cutting rhythm
7. Special Techniques: Unique cinematographic techniques
8. Visual Storytelling: How cinematography enhances the narrative

Write as professional cinematography notes."""

        response = await self.async_client.messages.create(
            model=self.models['creative'],
            max_tokens=1200,
            temperature=0.6,
            messages=[{
                "role": "user",
                "content": cinema_prompt
            }]
        )
        
        return response.content[0].text
    
    async def _analyze_themes(self, prompt: str) -> List[str]:
        """Analyze and extract deep themes from the prompt"""
        theme_prompt = f"""Analyze the deep themes in this video prompt:

"{prompt}"

Identify:
1. Primary themes (main ideas being explored)
2. Secondary themes (supporting ideas)
3. Symbolic themes (metaphorical meanings)
4. Emotional themes (feelings being evoked)
5. Universal themes (human experiences being touched on)
6. Cultural themes (cultural elements or commentary)
7. Philosophical themes (deeper questions being raised)

List all themes as a simple array of theme names."""

        response = await self.async_client.messages.create(
            model=self.models['analysis'],
            max_tokens=800,
            temperature=0.4,
            messages=[{
                "role": "user",
                "content": theme_prompt
            }]
        )
        
        # Extract themes from response
        text = response.content[0].text
        themes = []
        
        for line in text.split('\n'):
            line = line.strip()
            if line and not any(char in line for char in [':', '(', ')']):
                # Clean up common prefixes
                for prefix in ['- ', '• ', '* ', '1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ']:
                    if line.startswith(prefix):
                        line = line[len(prefix):]
                if line:
                    themes.append(line)
        
        return themes[:15]  # Limit to 15 most relevant themes
    
    async def _handle_sensitive_content(self, prompt: str) -> Dict[str, Any]:
        """Analyze and handle potentially sensitive content with nuance"""
        sensitive_prompt = f"""Analyze this video prompt for sensitive content that needs careful handling:

"{prompt}"

Consider:
1. Violence/Conflict: Level and context
2. Mature Themes: Adult situations or themes
3. Cultural Sensitivity: Potential cultural issues
4. Mental Health: Psychological elements
5. Social Issues: Political or social commentary
6. Graphic Content: Potentially disturbing visuals
7. Age Appropriateness: Suitable age ranges

For each area:
- Identify specific concerns
- Suggest how to handle appropriately
- Recommend alternative framings if needed
- Note if content is artistic/educational vs gratuitous

Provide balanced analysis that respects artistic expression while noting genuine concerns.
Format as JSON with "warnings" array and "recommendations" object."""

        response = await self.async_client.messages.create(
            model=self.models['analysis'],
            max_tokens=1500,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": sensitive_prompt
            }]
        )
        
        try:
            json_str = response.content[0].text
            if '```json' in json_str:
                json_str = json_str.split('```json')[1].split('```')[0]
            return json.loads(json_str)
        except:
            # Fallback
            return {
                "warnings": [],
                "recommendations": {}
            }
    
    async def _create_enhanced_prompt(
        self, 
        original: str, 
        analysis: Dict[str, Any],
        narrative: str,
        artistic: str,
        themes: List[str],
        mode: EnhancementMode
    ) -> str:
        """Create the final enhanced prompt combining all insights"""
        
        enhancement_prompt = f"""Create an enhanced video generation prompt based on this comprehensive analysis:

Original Prompt: "{original}"

Mode: {mode.value}

Analysis Insights:
{json.dumps(analysis, indent=2)}

Narrative Context:
{narrative[:500]}...

Artistic Details:
{artistic[:500]}...

Key Themes: {', '.join(themes[:5])}

Create a single, powerful, cohesive prompt that:
1. Incorporates the best insights from the analysis
2. Adds rich visual and atmospheric details
3. Maintains clarity while adding depth
4. Enhances the emotional and artistic impact
5. Ensures technical feasibility
6. Respects the original intent while elevating it

The enhanced prompt should be detailed but not overwhelming, typically 2-4 sentences that paint a vivid picture."""

        response = await self.async_client.messages.create(
            model=self.models['creative'],
            max_tokens=1000,
            temperature=0.6,
            messages=[{
                "role": "user",
                "content": enhancement_prompt
            }]
        )
        
        return response.content[0].text.strip()
    
    def enhance_prompt_sync(self, prompt: str, mode: EnhancementMode = EnhancementMode.COMPREHENSIVE) -> EnhancementResult:
        """Synchronous version of enhance_prompt"""
        return asyncio.run(self.enhance_prompt(prompt, mode))
    
    async def batch_enhance(self, prompts: List[str], mode: EnhancementMode = EnhancementMode.COMPREHENSIVE) -> List[EnhancementResult]:
        """Enhance multiple prompts in parallel for efficiency"""
        tasks = [self.enhance_prompt(prompt, mode) for prompt in prompts]
        return await asyncio.gather(*tasks)
    
    def get_quick_enhancement(self, prompt: str) -> str:
        """Quick enhancement using fast model for real-time applications"""
        response = self.client.messages.create(
            model=self.models['quick'],
            max_tokens=500,
            temperature=0.6,
            messages=[{
                "role": "user",
                "content": f"Enhance this video prompt with rich visual details in 2-3 sentences: '{prompt}'"
            }]
        )
        
        return response.content[0].text.strip()
    
    async def evaluate_and_improve(self, prompt: str, target_score: float = 0.8) -> Tuple[str, Dict[str, float]]:
        """Iteratively improve a prompt until it reaches target quality score"""
        current_prompt = prompt
        iterations = 0
        max_iterations = 3
        
        while iterations < max_iterations:
            scores = await self._evaluate_prompt(current_prompt)
            
            if scores.get('total_score', 0) >= target_score:
                return current_prompt, scores
            
            # Identify weakest areas
            weak_areas = sorted(
                [(k, v) for k, v in scores.items() if k != 'total_score'],
                key=lambda x: x[1]
            )[:3]
            
            # Create improvement prompt
            improvement_prompt = f"""Improve this video prompt specifically in these areas:
            
Prompt: "{current_prompt}"

Weak areas to improve:
{', '.join([f"{area[0]} (score: {area[1]:.2f})" for area in weak_areas])}

Create an improved version that addresses these weaknesses while maintaining all strengths."""

            response = await self.async_client.messages.create(
                model=self.models['creative'],
                max_tokens=800,
                temperature=0.6,
                messages=[{
                    "role": "user",
                    "content": improvement_prompt
                }]
            )
            
            current_prompt = response.content[0].text.strip()
            iterations += 1
        
        # Return best attempt with final scores
        final_scores = await self._evaluate_prompt(current_prompt)
        return current_prompt, final_scores


# Example usage and testing
if __name__ == "__main__":
    # Example of how to use the enhancer
    async def test_enhancer():
        # Initialize with API key
        enhancer = ClaudeEnhancer()
        
        # Test prompt
        test_prompt = "A robot walking through a city"
        
        # Enhance with different modes
        print("Testing Claude Enhancer...\n")
        
        # Comprehensive enhancement
        result = await enhancer.enhance_prompt(test_prompt, EnhancementMode.COMPREHENSIVE)
        
        print(f"Original: {result.original_prompt}")
        print(f"\nEnhanced: {result.enhanced_prompt}")
        print(f"\nScores: {json.dumps(result.scores, indent=2)}")
        print(f"\nThemes: {', '.join(result.themes)}")
        print(f"\nVariations: {len(result.variations)} generated")
        
        # Quick enhancement
        quick = enhancer.get_quick_enhancement(test_prompt)
        print(f"\nQuick Enhancement: {quick}")
    
    # Run test
    # asyncio.run(test_enhancer())