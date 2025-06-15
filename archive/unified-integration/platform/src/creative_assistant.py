"""
Creative Assistant System

An AI-powered assistant that helps users express their creative vision
through natural conversation and intelligent suggestions.

This is not about "optimization" - it's about understanding what users
want to create and helping them articulate their vision clearly.
"""

import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class CreativeIntent(Enum):
    """What the user wants to create"""
    STORYTELLING = "storytelling"
    ARTISTIC_EXPRESSION = "artistic_expression"
    COMMERCIAL_CONTENT = "commercial_content"
    EDUCATIONAL_MATERIAL = "educational_material"
    PERSONAL_MEMORY = "personal_memory"
    EXPERIMENTAL_ART = "experimental_art"
    DOCUMENTARY_STYLE = "documentary_style"
    ENTERTAINMENT = "entertainment"


class AssistanceLevel(Enum):
    """How much help the user wants"""
    MINIMAL = "minimal"  # Just enhance what they give
    COLLABORATIVE = "collaborative"  # Work together
    GUIDED = "guided"  # Lead them through process
    COMPREHENSIVE = "comprehensive"  # Full creative partnership


@dataclass
class CreativeSession:
    """A single creative session with the user"""
    session_id: str
    user_id: str
    started_at: datetime
    intent: Optional[CreativeIntent] = None
    assistance_level: AssistanceLevel = AssistanceLevel.COLLABORATIVE
    
    # Conversation history
    user_inputs: List[str] = field(default_factory=list)
    assistant_responses: List[str] = field(default_factory=list)
    
    # Creative elements gathered
    subject_elements: List[str] = field(default_factory=list)
    mood_keywords: List[str] = field(default_factory=list)
    visual_style: Optional[str] = None
    narrative_arc: Optional[str] = None
    
    # Generated content
    initial_vision: Optional[str] = None
    enhanced_vision: Optional[str] = None
    alternative_approaches: List[str] = field(default_factory=list)
    
    # User feedback
    satisfaction_rating: Optional[float] = None
    user_preferences_learned: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserCreativeProfile:
    """Authentic learning about user's creative preferences"""
    user_id: str
    created_at: datetime
    last_updated: datetime
    
    # Genuine preferences learned over time
    preferred_subjects: Dict[str, float] = field(default_factory=dict)  # subject -> interest_score
    preferred_moods: Dict[str, float] = field(default_factory=dict)     # mood -> preference_score
    preferred_styles: Dict[str, float] = field(default_factory=dict)    # style -> affinity_score
    
    # Communication preferences
    likes_detailed_questions: bool = True
    prefers_voice_input: bool = False
    wants_step_by_step_guidance: bool = True
    enjoys_creative_suggestions: bool = True
    
    # Creative patterns
    typical_session_length: float = 0.0  # minutes
    common_creative_goals: List[CreativeIntent] = field(default_factory=list)
    frequently_used_words: Dict[str, int] = field(default_factory=dict)
    
    # Learning metrics
    sessions_completed: int = 0
    average_satisfaction: float = 0.0
    improvement_areas: List[str] = field(default_factory=list)


class CreativeAssistant:
    """AI Assistant that helps users create better content through conversation"""
    
    def __init__(self, profiles_dir: str = "/var/projects/ai-integration-platform/creative_profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(exist_ok=True)
        
        # Creative conversation patterns
        self.conversation_starters = {
            "new_user": [
                "Hi! I'm here to help bring your creative vision to life. What would you like to create today?",
                "Welcome! I'd love to help you express your ideas. What's inspiring you right now?",
                "Hello! Ready to create something amazing? Tell me what's on your mind."
            ],
            "returning_user": [
                "Great to see you again! Ready for another creative session?",
                "Welcome back! What new ideas are you excited to explore?",
                "Hi! I remember you like {preference}. Want to build on that or try something new?"
            ]
        }
        
        # Question patterns for understanding user needs
        self.discovery_questions = {
            "intent_clarification": [
                "What feeling do you want people to have when they see this?",
                "Is this for a specific purpose or just creative expression?",
                "Who is your audience for this creation?"
            ],
            "visual_exploration": [
                "When you imagine this, what's the first thing you see?",
                "What colors or lighting come to mind?",
                "Should this feel intimate or grand?"
            ],
            "narrative_development": [
                "What's the story you want to tell?",
                "Is there a moment of change or emotion you want to capture?",
                "What happens before and after this scene?"
            ]
        }
        
    def start_creative_session(self, user_id: str, initial_input: str = "", 
                             voice_input: bool = False) -> CreativeSession:
        """Begin a new creative session with the user"""
        session = CreativeSession(
            session_id=f"{user_id}_{int(time.time())}",
            user_id=user_id,
            started_at=datetime.now()
        )
        
        # Load user profile for personalization
        profile = self.load_user_profile(user_id)
        
        if initial_input:
            session.user_inputs.append(initial_input)
            
            # Analyze initial input to understand intent
            session.intent = self._detect_creative_intent(initial_input)
            session.assistance_level = self._determine_assistance_level(initial_input, profile)
            
            # Generate appropriate response
            response = self._generate_contextual_response(session, profile)
            session.assistant_responses.append(response)
        
        return session
    
    def continue_conversation(self, session: CreativeSession, user_input: str, 
                            voice_input: bool = False) -> str:
        """Continue the creative conversation"""
        session.user_inputs.append(user_input)
        profile = self.load_user_profile(session.user_id)
        
        # Extract creative elements from input
        self._extract_creative_elements(user_input, session)
        
        # Generate helpful response
        response = self._generate_helpful_response(session, user_input, profile)
        session.assistant_responses.append(response)
        
        # Learn from this interaction
        self._learn_from_interaction(session, profile, user_input, response)
        
        return response
    
    def _detect_creative_intent(self, text: str) -> CreativeIntent:
        """Understand what the user wants to create"""
        text_lower = text.lower()
        
        # Pattern matching for creative intent
        if any(word in text_lower for word in ['story', 'narrative', 'character', 'plot']):
            return CreativeIntent.STORYTELLING
        elif any(word in text_lower for word in ['art', 'artistic', 'abstract', 'expression']):
            return CreativeIntent.ARTISTIC_EXPRESSION
        elif any(word in text_lower for word in ['commercial', 'business', 'product', 'marketing']):
            return CreativeIntent.COMMERCIAL_CONTENT
        elif any(word in text_lower for word in ['teach', 'explain', 'educational', 'learn']):
            return CreativeIntent.EDUCATIONAL_MATERIAL
        elif any(word in text_lower for word in ['memory', 'personal', 'family', 'remember']):
            return CreativeIntent.PERSONAL_MEMORY
        elif any(word in text_lower for word in ['experiment', 'try', 'explore', 'unusual']):
            return CreativeIntent.EXPERIMENTAL_ART
        elif any(word in text_lower for word in ['documentary', 'real', 'actual', 'documentary']):
            return CreativeIntent.DOCUMENTARY_STYLE
        else:
            return CreativeIntent.ENTERTAINMENT
    
    def _determine_assistance_level(self, text: str, profile: UserCreativeProfile) -> AssistanceLevel:
        """Determine how much help the user wants"""
        text_lower = text.lower()
        
        # Check for explicit requests
        if any(phrase in text_lower for phrase in ['help me create', 'guide me', 'walk me through']):
            return AssistanceLevel.GUIDED
        elif any(phrase in text_lower for phrase in ['just improve', 'enhance this', 'make better']):
            return AssistanceLevel.MINIMAL
        elif any(phrase in text_lower for phrase in ['work together', 'collaborate', 'let\\'s build']):
            return AssistanceLevel.COLLABORATIVE
        elif any(phrase in text_lower for phrase in ['need lots of help', 'not sure', 'struggling']):
            return AssistanceLevel.COMPREHENSIVE
        
        # Use profile preferences
        if profile and profile.wants_step_by_step_guidance:
            return AssistanceLevel.GUIDED
        
        return AssistanceLevel.COLLABORATIVE
    
    def _extract_creative_elements(self, text: str, session: CreativeSession):
        """Extract creative elements from user input"""
        text_lower = text.lower()
        
        # Extract subjects/objects
        subjects = self._extract_subjects(text)
        session.subject_elements.extend(subjects)
        
        # Extract mood/emotion words
        moods = self._extract_moods(text)
        session.mood_keywords.extend(moods)
        
        # Extract style indicators
        style = self._extract_style(text)
        if style:
            session.visual_style = style
    
    def _extract_subjects(self, text: str) -> List[str]:
        """Extract main subjects from text"""
        # Simple keyword extraction - could be enhanced with NLP
        subjects = []
        
        # Common subject patterns
        subject_keywords = [
            'person', 'people', 'man', 'woman', 'child', 'family',
            'animal', 'cat', 'dog', 'bird', 'nature', 'forest', 'ocean',
            'building', 'house', 'city', 'landscape', 'mountain',
            'car', 'technology', 'art', 'music', 'dance'
        ]
        
        for keyword in subject_keywords:
            if keyword in text.lower():
                subjects.append(keyword)
        
        return subjects
    
    def _extract_moods(self, text: str) -> List[str]:
        """Extract mood and emotion indicators"""
        moods = []
        
        mood_keywords = [
            'happy', 'joyful', 'excited', 'peaceful', 'calm', 'serene',
            'dramatic', 'intense', 'mysterious', 'romantic', 'playful',
            'serious', 'contemplative', 'energetic', 'melancholic',
            'uplifting', 'inspiring', 'nostalgic', 'futuristic'
        ]
        
        for mood in mood_keywords:
            if mood in text.lower():
                moods.append(mood)
        
        return moods
    
    def _extract_style(self, text: str) -> Optional[str]:
        """Extract visual style preferences"""
        text_lower = text.lower()
        
        style_patterns = {
            'cinematic': ['cinematic', 'movie-like', 'film'],
            'documentary': ['documentary', 'realistic', 'natural'],
            'artistic': ['artistic', 'creative', 'expressive'],
            'minimalist': ['simple', 'clean', 'minimal'],
            'dramatic': ['dramatic', 'intense', 'powerful'],
            'vintage': ['vintage', 'retro', 'classic'],
            'modern': ['modern', 'contemporary', 'current']
        }
        
        for style, keywords in style_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return style
        
        return None
    
    def _generate_contextual_response(self, session: CreativeSession, 
                                    profile: UserCreativeProfile) -> str:
        """Generate an appropriate response based on context"""
        
        if not session.user_inputs:
            # First interaction
            if profile and profile.sessions_completed > 0:
                return self._get_returning_user_greeting(profile)
            else:
                return self._get_new_user_greeting()
        
        # Analyze what we've learned so far
        latest_input = session.user_inputs[-1]
        
        if session.assistance_level == AssistanceLevel.MINIMAL:
            return self._generate_enhancement_response(session)
        elif session.assistance_level == AssistanceLevel.GUIDED:
            return self._generate_guided_response(session)
        elif session.assistance_level == AssistanceLevel.COMPREHENSIVE:
            return self._generate_comprehensive_response(session)
        else:  # COLLABORATIVE
            return self._generate_collaborative_response(session)
    
    def _generate_helpful_response(self, session: CreativeSession, user_input: str,
                                 profile: UserCreativeProfile) -> str:
        """Generate a helpful response to continue the conversation"""
        
        # Determine what type of help to provide
        if len(session.user_inputs) <= 2:
            # Early in conversation - ask clarifying questions
            return self._ask_discovery_question(session, profile)
        elif len(session.subject_elements) < 3:
            # Need more creative elements
            return self._ask_for_more_details(session)
        else:
            # Ready to help create
            return self._offer_creative_assistance(session)
    
    def _ask_discovery_question(self, session: CreativeSession, 
                              profile: UserCreativeProfile) -> str:
        """Ask questions to understand user needs better"""
        
        if session.intent == CreativeIntent.STORYTELLING:
            questions = self.discovery_questions["narrative_development"]
        elif not session.mood_keywords:
            questions = [
                "What feeling or mood do you want to capture?",
                "How do you want people to feel when they see this?",
                "What emotion is at the heart of your vision?"
            ]
        elif not session.visual_style:
            questions = self.discovery_questions["visual_exploration"]
        else:
            questions = self.discovery_questions["intent_clarification"]
        
        import random
        return random.choice(questions)
    
    def _ask_for_more_details(self, session: CreativeSession) -> str:
        """Ask for more creative details"""
        responses = [
            "That's a great start! Can you tell me more about the setting or environment?",
            "I love that idea! What other elements would make this scene come alive?",
            "Interesting! What details would make this feel more vivid or real?",
            "Nice! What's happening around the main focus that adds to the story?"
        ]
        
        import random
        return random.choice(responses)
    
    def _offer_creative_assistance(self, session: CreativeSession) -> str:
        """Offer to help create the final vision"""
        
        # Create initial vision based on gathered elements
        vision = self._synthesize_creative_vision(session)
        session.initial_vision = vision
        
        return f"Based on our conversation, I can see you want to create: {vision}. " \
               f"Would you like me to enhance this vision with more cinematic details, " \
               f"or would you prefer to adjust anything first?"
    
    def _synthesize_creative_vision(self, session: CreativeSession) -> str:
        """Create a coherent vision from gathered elements"""
        
        vision_parts = []
        
        # Add subjects
        if session.subject_elements:
            subjects = ", ".join(session.subject_elements[:3])
            vision_parts.append(subjects)
        
        # Add action or interaction
        if session.intent == CreativeIntent.STORYTELLING:
            vision_parts.append("engaged in a meaningful interaction")
        elif session.intent == CreativeIntent.ARTISTIC_EXPRESSION:
            vision_parts.append("captured in an expressive moment")
        else:
            vision_parts.append("in a compelling scene")
        
        # Add mood
        if session.mood_keywords:
            mood = session.mood_keywords[0]
            vision_parts.append(f"with a {mood} atmosphere")
        
        # Add style
        if session.visual_style:
            vision_parts.append(f"in a {session.visual_style} style")
        
        return " ".join(vision_parts)
    
    def _learn_from_interaction(self, session: CreativeSession, 
                              profile: UserCreativeProfile, 
                              user_input: str, assistant_response: str):
        """Learn from this interaction to improve future assistance"""
        
        # Track word frequency
        words = user_input.lower().split()
        for word in words:
            if len(word) > 3:  # Skip short words
                profile.frequently_used_words[word] = profile.frequently_used_words.get(word, 0) + 1
        
        # Track preferences
        for subject in session.subject_elements:
            current_score = profile.preferred_subjects.get(subject, 0.5)
            profile.preferred_subjects[subject] = min(1.0, current_score + 0.1)
        
        for mood in session.mood_keywords:
            current_score = profile.preferred_moods.get(mood, 0.5)
            profile.preferred_moods[mood] = min(1.0, current_score + 0.1)
        
        if session.visual_style:
            current_score = profile.preferred_styles.get(session.visual_style, 0.5)
            profile.preferred_styles[session.visual_style] = min(1.0, current_score + 0.1)
        
        # Update communication preferences based on response patterns
        if len(user_input) > 100:
            profile.likes_detailed_questions = True
        
        profile.last_updated = datetime.now()
        self.save_user_profile(profile)
    
    def _get_new_user_greeting(self) -> str:
        """Get greeting for new users"""
        import random
        return random.choice(self.conversation_starters["new_user"])
    
    def _get_returning_user_greeting(self, profile: UserCreativeProfile) -> str:
        """Get personalized greeting for returning users"""
        import random
        templates = self.conversation_starters["returning_user"]
        
        # Personalize based on preferences
        if profile.preferred_subjects:
            most_liked = max(profile.preferred_subjects.items(), key=lambda x: x[1])
            template = random.choice(templates)
            return template.format(preference=most_liked[0])
        
        return random.choice(templates)
    
    def load_user_profile(self, user_id: str) -> UserCreativeProfile:
        """Load or create user profile"""
        profile_file = self.profiles_dir / f"{user_id}_creative.json"
        
        if profile_file.exists():
            try:
                with open(profile_file, 'r') as f:
                    data = json.load(f)
                    
                # Convert datetime strings back to datetime objects
                data['created_at'] = datetime.fromisoformat(data['created_at'])
                data['last_updated'] = datetime.fromisoformat(data['last_updated'])
                
                # Convert enum strings back to enums
                if 'common_creative_goals' in data:
                    data['common_creative_goals'] = [
                        CreativeIntent(goal) for goal in data['common_creative_goals']
                    ]
                
                return UserCreativeProfile(**data)
            except Exception as e:
                logger.error(f"Error loading profile for {user_id}: {e}")
        
        # Create new profile
        return UserCreativeProfile(
            user_id=user_id,
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
    
    def save_user_profile(self, profile: UserCreativeProfile):
        """Save user profile"""
        profile_file = self.profiles_dir / f"{profile.user_id}_creative.json"
        
        try:
            # Convert to JSON-serializable format
            data = {
                'user_id': profile.user_id,
                'created_at': profile.created_at.isoformat(),
                'last_updated': profile.last_updated.isoformat(),
                'preferred_subjects': profile.preferred_subjects,
                'preferred_moods': profile.preferred_moods,
                'preferred_styles': profile.preferred_styles,
                'likes_detailed_questions': profile.likes_detailed_questions,
                'prefers_voice_input': profile.prefers_voice_input,
                'wants_step_by_step_guidance': profile.wants_step_by_step_guidance,
                'enjoys_creative_suggestions': profile.enjoys_creative_suggestions,
                'typical_session_length': profile.typical_session_length,
                'common_creative_goals': [goal.value for goal in profile.common_creative_goals],
                'frequently_used_words': profile.frequently_used_words,
                'sessions_completed': profile.sessions_completed,
                'average_satisfaction': profile.average_satisfaction,
                'improvement_areas': profile.improvement_areas
            }
            
            with open(profile_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving profile for {profile.user_id}: {e}")
    
    def complete_session(self, session: CreativeSession, satisfaction_rating: float = None):
        """Complete a creative session and update user profile"""
        profile = self.load_user_profile(session.user_id)
        
        # Update session statistics
        profile.sessions_completed += 1
        
        if satisfaction_rating:
            session.satisfaction_rating = satisfaction_rating
            # Update average satisfaction
            current_avg = profile.average_satisfaction
            total_sessions = profile.sessions_completed
            profile.average_satisfaction = ((current_avg * (total_sessions - 1)) + satisfaction_rating) / total_sessions
        
        # Calculate session length
        session_length = (datetime.now() - session.started_at).total_seconds() / 60
        if profile.typical_session_length == 0:
            profile.typical_session_length = session_length
        else:
            profile.typical_session_length = (profile.typical_session_length + session_length) / 2
        
        # Update common goals
        if session.intent and session.intent not in profile.common_creative_goals:
            profile.common_creative_goals.append(session.intent)
        
        self.save_user_profile(profile)
        return profile


def get_creative_assistant() -> CreativeAssistant:
    """Get creative assistant instance"""
    return CreativeAssistant()


if __name__ == "__main__":
    # Example usage
    assistant = get_creative_assistant()
    
    # Start a session
    session = assistant.start_creative_session(
        "test_user", 
        "I want to create something about a family gathering"
    )
    
    print("Assistant:", session.assistant_responses[-1])
    
    # Continue conversation
    response = assistant.continue_conversation(
        session, 
        "It should feel warm and nostalgic, maybe during holidays"
    )
    
    print("Assistant:", response)