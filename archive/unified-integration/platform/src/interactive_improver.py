from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import random


class QuestionCategory(Enum):
    VISUAL_DETAILS = "visual_details"
    EMOTIONAL_TONE = "emotional_tone"
    TECHNICAL_SPECS = "technical_specs"
    CONTEXT_SETTING = "context_setting"
    ARTISTIC_STYLE = "artistic_style"
    NARRATIVE_ELEMENTS = "narrative_elements"


@dataclass
class SmartQuestion:
    question: str
    category: QuestionCategory
    options: Optional[List[str]] = None
    why_asking: str = ""
    impact: str = ""


@dataclass
class PromptGaps:
    missing_visual_details: bool = False
    missing_emotional_context: bool = False
    missing_technical_specs: bool = False
    missing_setting_details: bool = False
    missing_style_direction: bool = False
    too_vague: bool = False
    needs_more_specificity: bool = False


class InteractivePromptImprover:
    def __init__(self):
        self.question_bank = {
            "visual_clarity": [
                SmartQuestion(
                    question="What time of day should this scene take place?",
                    category=QuestionCategory.VISUAL_DETAILS,
                    options=["Dawn/Sunrise", "Morning", "Noon", "Afternoon", "Sunset/Golden Hour", "Night", "Blue Hour"],
                    why_asking="Lighting dramatically affects mood and visual quality",
                    impact="Adds specific lighting conditions and atmosphere"
                ),
                SmartQuestion(
                    question="What's the primary color palette you envision?",
                    category=QuestionCategory.VISUAL_DETAILS,
                    options=["Warm (reds/oranges/yellows)", "Cool (blues/greens/purples)", "Monochromatic", "High contrast", "Pastel/Soft", "Vibrant/Saturated", "Dark/Moody"],
                    why_asking="Color strongly influences emotional response",
                    impact="Defines visual mood and artistic direction"
                ),
                SmartQuestion(
                    question="How close should the camera be to the subject?",
                    category=QuestionCategory.TECHNICAL_SPECS,
                    options=["Extreme close-up", "Close-up", "Medium shot", "Wide shot", "Extreme wide", "Aerial view"],
                    why_asking="Camera distance changes the viewer's relationship with the subject",
                    impact="Determines intimacy and scope of the scene"
                )
            ],
            "environment": [
                SmartQuestion(
                    question="Where specifically is this taking place?",
                    category=QuestionCategory.CONTEXT_SETTING,
                    options=["Urban/City", "Nature/Wilderness", "Indoor/Interior", "Fantasy/Imaginary", "Historical setting", "Futuristic", "Abstract space"],
                    why_asking="Location provides crucial context and visual elements",
                    impact="Grounds the scene in a specific environment"
                ),
                SmartQuestion(
                    question="What's the weather or atmospheric condition?",
                    category=QuestionCategory.CONTEXT_SETTING,
                    options=["Clear/Sunny", "Cloudy/Overcast", "Rainy", "Foggy/Misty", "Snowy", "Stormy", "Windy"],
                    why_asking="Weather adds drama and affects lighting",
                    impact="Creates atmosphere and mood"
                )
            ],
            "style": [
                SmartQuestion(
                    question="What artistic style should this emulate?",
                    category=QuestionCategory.ARTISTIC_STYLE,
                    options=["Photorealistic", "Cinematic", "Painterly", "Animated/Cartoon", "Surreal", "Minimalist", "Retro/Vintage", "Futuristic"],
                    why_asking="Style defines the overall aesthetic approach",
                    impact="Determines visual treatment and rendering style"
                ),
                SmartQuestion(
                    question="What emotional tone are you aiming for?",
                    category=QuestionCategory.EMOTIONAL_TONE,
                    options=["Dramatic/Intense", "Peaceful/Calm", "Mysterious", "Joyful/Upbeat", "Melancholic", "Tense/Suspenseful", "Romantic", "Epic/Grand"],
                    why_asking="Emotional tone guides all creative decisions",
                    impact="Influences lighting, color, and composition choices"
                )
            ],
            "technical": [
                SmartQuestion(
                    question="How should the camera move (if at all)?",
                    category=QuestionCategory.TECHNICAL_SPECS,
                    options=["Static/Fixed", "Slow pan", "Tracking/Following", "Zoom in", "Zoom out", "Rotating/Orbiting", "Handheld/Shaky"],
                    why_asking="Camera movement adds dynamism and guides attention",
                    impact="Creates kinetic energy and visual flow"
                ),
                SmartQuestion(
                    question="What aspect ratio would work best?",
                    category=QuestionCategory.TECHNICAL_SPECS,
                    options=["16:9 (Standard)", "21:9 (Cinematic)", "1:1 (Square)", "9:16 (Vertical)", "4:3 (Classic)"],
                    why_asking="Aspect ratio affects composition and platform compatibility",
                    impact="Determines framing and visual boundaries"
                )
            ],
            "narrative": [
                SmartQuestion(
                    question="What's the key action or moment happening?",
                    category=QuestionCategory.NARRATIVE_ELEMENTS,
                    why_asking="Specific actions create more dynamic scenes",
                    impact="Adds movement and purpose to the scene"
                ),
                SmartQuestion(
                    question="What's the story context or backstory?",
                    category=QuestionCategory.NARRATIVE_ELEMENTS,
                    why_asking="Context adds depth and meaning",
                    impact="Creates richer, more engaging narratives"
                )
            ]
        }
    
    def analyze_prompt_gaps(self, prompt: str) -> PromptGaps:
        """Identify what's missing from a prompt"""
        prompt_lower = prompt.lower()
        gaps = PromptGaps()
        
        # Check for visual details
        visual_keywords = ["color", "light", "bright", "dark", "shadow", "texture"]
        if not any(keyword in prompt_lower for keyword in visual_keywords):
            gaps.missing_visual_details = True
        
        # Check for emotional context
        emotion_keywords = ["mood", "feeling", "atmosphere", "tone", "emotion"]
        if not any(keyword in prompt_lower for keyword in emotion_keywords):
            gaps.missing_emotional_context = True
        
        # Check for technical specs
        tech_keywords = ["shot", "angle", "camera", "movement", "zoom", "pan"]
        if not any(keyword in prompt_lower for keyword in tech_keywords):
            gaps.missing_technical_specs = True
        
        # Check for setting details
        setting_keywords = ["location", "place", "environment", "setting", "where", "indoor", "outdoor"]
        if not any(keyword in prompt_lower for keyword in setting_keywords):
            gaps.missing_setting_details = True
        
        # Check for style
        style_keywords = ["style", "aesthetic", "look", "inspired", "artistic"]
        if not any(keyword in prompt_lower for keyword in style_keywords):
            gaps.missing_style_direction = True
        
        # Check for vagueness
        if len(prompt.split()) < 8:
            gaps.too_vague = True
        
        vague_terms = ["something", "someone", "somewhere", "somehow", "thing", "stuff"]
        if any(term in prompt_lower for term in vague_terms):
            gaps.needs_more_specificity = True
        
        return gaps
    
    def generate_smart_questions(self, prompt: str, max_questions: int = 3) -> List[SmartQuestion]:
        """Generate relevant questions based on what's missing"""
        gaps = self.analyze_prompt_gaps(prompt)
        questions = []
        
        # Prioritize questions based on gaps
        if gaps.missing_setting_details and "environment" in self.question_bank:
            questions.extend(random.sample(self.question_bank["environment"], min(1, len(self.question_bank["environment"]))))
        
        if gaps.missing_visual_details and "visual_clarity" in self.question_bank:
            questions.extend(random.sample(self.question_bank["visual_clarity"], min(1, len(self.question_bank["visual_clarity"]))))
        
        if gaps.missing_style_direction and "style" in self.question_bank:
            questions.extend(random.sample(self.question_bank["style"], min(1, len(self.question_bank["style"]))))
        
        if gaps.missing_technical_specs and "technical" in self.question_bank:
            questions.extend(random.sample(self.question_bank["technical"], min(1, len(self.question_bank["technical"]))))
        
        # Add narrative questions if prompt is too vague
        if gaps.too_vague and "narrative" in self.question_bank:
            questions.extend(self.question_bank["narrative"])
        
        # Limit to max_questions, prioritizing variety
        seen_categories = set()
        filtered_questions = []
        for q in questions:
            if q.category not in seen_categories and len(filtered_questions) < max_questions:
                filtered_questions.append(q)
                seen_categories.add(q.category)
        
        # If we need more questions, add any remaining
        for q in questions:
            if len(filtered_questions) < max_questions and q not in filtered_questions:
                filtered_questions.append(q)
        
        return filtered_questions[:max_questions]
    
    def apply_answer_to_prompt(self, original_prompt: str, question: SmartQuestion, answer: str) -> str:
        """Incorporate the answer into the prompt intelligently"""
        
        # Handle different question categories
        if question.category == QuestionCategory.VISUAL_DETAILS:
            if "time of day" in question.question.lower():
                return f"{original_prompt}, during {answer.lower()}"
            elif "color palette" in question.question.lower():
                return f"{original_prompt}, with {answer.lower()} color palette"
            elif "camera" in question.question.lower() and "close" in question.question.lower():
                return f"{answer} of {original_prompt}"
        
        elif question.category == QuestionCategory.CONTEXT_SETTING:
            if "where" in question.question.lower():
                return f"{original_prompt} in a {answer.lower()} setting"
            elif "weather" in question.question.lower():
                return f"{original_prompt}, {answer.lower()} conditions"
        
        elif question.category == QuestionCategory.ARTISTIC_STYLE:
            if "style" in question.question.lower():
                return f"{original_prompt}, {answer.lower()} style"
        
        elif question.category == QuestionCategory.EMOTIONAL_TONE:
            return f"{original_prompt}, {answer.lower()} mood"
        
        elif question.category == QuestionCategory.TECHNICAL_SPECS:
            if "camera move" in question.question.lower():
                return f"{original_prompt}, {answer.lower()} camera movement"
            elif "aspect ratio" in question.question.lower():
                return f"{original_prompt}, {answer} aspect ratio"
        
        elif question.category == QuestionCategory.NARRATIVE_ELEMENTS:
            # For open-ended narrative questions, append the answer
            return f"{original_prompt}. {answer}"
        
        # Default: append with comma
        return f"{original_prompt}, {answer}"
    
    def generate_improvement_suggestions(self, prompt: str) -> List[str]:
        """Generate specific suggestions for improving the prompt"""
        gaps = self.analyze_prompt_gaps(prompt)
        suggestions = []
        
        if gaps.missing_visual_details:
            suggestions.append("Add specific visual details like lighting, colors, or textures")
        
        if gaps.missing_emotional_context:
            suggestions.append("Include the emotional tone or mood you want to convey")
        
        if gaps.missing_setting_details:
            suggestions.append("Specify where this scene takes place")
        
        if gaps.missing_style_direction:
            suggestions.append("Mention an artistic style or aesthetic direction")
        
        if gaps.too_vague:
            suggestions.append("Expand your description with more specific details")
        
        if gaps.needs_more_specificity:
            suggestions.append("Replace vague terms with concrete descriptions")
        
        # Add some creative suggestions
        creative_suggestions = [
            "Consider adding a unique perspective or camera angle",
            "Think about the story behind this moment",
            "Add atmospheric elements like weather or time of day",
            "Include specific materials, textures, or surface qualities",
            "Mention the quality of light you envision"
        ]
        
        # Add 1-2 creative suggestions
        num_creative = min(2, 5 - len(suggestions))
        if num_creative > 0:
            suggestions.extend(random.sample(creative_suggestions, num_creative))
        
        return suggestions[:5]  # Limit to 5 suggestions


class PromptBuilderWizard:
    """Step-by-step prompt building wizard"""
    
    def __init__(self):
        self.steps = [
            {
                "title": "What's your main subject?",
                "description": "Describe the main focus of your scene",
                "examples": ["a warrior", "a futuristic city", "an abstract pattern", "a magical creature"]
            },
            {
                "title": "What's happening in the scene?",
                "description": "Describe the action or state",
                "examples": ["standing heroically", "bustling with activity", "morphing and shifting", "casting a spell"]
            },
            {
                "title": "Where does this take place?",
                "description": "Set the location or environment",
                "examples": ["on a mountaintop", "in a neon-lit street", "in abstract space", "in an enchanted forest"]
            },
            {
                "title": "What's the mood or atmosphere?",
                "description": "Define the emotional tone",
                "examples": ["epic and inspiring", "mysterious and noir", "calm and meditative", "whimsical and magical"]
            },
            {
                "title": "What visual style do you prefer?",
                "description": "Choose an artistic approach",
                "examples": ["photorealistic", "animated", "painterly", "surreal"]
            }
        ]
    
    def build_prompt_from_answers(self, answers: List[str]) -> str:
        """Combine wizard answers into a cohesive prompt"""
        if len(answers) < 3:
            return " ".join(answers)
        
        # Smart combination based on answer count
        if len(answers) >= 5:
            # Full prompt with all elements
            subject, action, location, mood, style = answers[:5]
            return f"{style} {mood} scene of {subject} {action} {location}"
        elif len(answers) == 4:
            subject, action, location, mood = answers[:4]
            return f"{mood} scene of {subject} {action} {location}"
        elif len(answers) == 3:
            subject, action, location = answers[:3]
            return f"{subject} {action} {location}"
        else:
            return " ".join(answers)