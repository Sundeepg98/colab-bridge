"""
User Profile System

Comprehensive user profiling that tracks:
1. User behavior patterns and preferences
2. Content creation intentions
3. Usage patterns and trends
4. Personalization preferences
5. Trust and reputation scores
"""

import json
import hashlib
import statistics
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)


class UserSegment(Enum):
    """User segments based on behavior"""
    CREATIVE_PROFESSIONAL = "creative_professional"
    CONTENT_CREATOR = "content_creator"
    RESEARCHER = "researcher"
    ARTIST = "artist"
    FILMMAKER = "filmmaker"
    EDUCATOR = "educator"
    EXPERIMENTER = "experimenter"
    CASUAL_USER = "casual_user"
    POWER_USER = "power_user"
    SUSPICIOUS = "suspicious"


class ContentCategory(Enum):
    """Content categories users create"""
    NATURE = "nature"
    URBAN = "urban"
    PORTRAIT = "portrait"
    ABSTRACT = "abstract"
    NARRATIVE = "narrative"
    DOCUMENTARY = "documentary"
    ARTISTIC = "artistic"
    COMMERCIAL = "commercial"
    EDUCATIONAL = "educational"
    EXPERIMENTAL = "experimental"


class IntentionType(Enum):
    """User intentions when creating content"""
    ARTISTIC_EXPRESSION = "artistic_expression"
    COMMERCIAL_PROJECT = "commercial_project"
    EDUCATIONAL_CONTENT = "educational_content"
    RESEARCH_EXPLORATION = "research_exploration"
    PERSONAL_PROJECT = "personal_project"
    PROFESSIONAL_WORK = "professional_work"
    TESTING_BOUNDARIES = "testing_boundaries"
    LEARNING_PLATFORM = "learning_platform"


@dataclass
class ContentRequest:
    """Record of a single content request"""
    timestamp: datetime
    prompt: str
    category: ContentCategory
    detected_intention: IntentionType
    quality_score: float
    used_advanced_features: bool
    response_time: float
    satisfaction_score: Optional[float] = None


@dataclass
class UserPreferences:
    """User preferences and settings"""
    preferred_style: str = "cinematic"
    preferred_quality: str = "high"
    preferred_categories: List[ContentCategory] = field(default_factory=list)
    favorite_themes: List[str] = field(default_factory=list)
    language: str = "en"
    timezone: str = "UTC"
    notification_preferences: Dict[str, bool] = field(default_factory=dict)
    privacy_level: str = "standard"


@dataclass
class BehaviorMetrics:
    """Metrics tracking user behavior"""
    avg_session_duration: float = 0.0
    avg_requests_per_session: float = 0.0
    peak_usage_hours: List[int] = field(default_factory=list)
    feature_usage: Dict[str, int] = field(default_factory=dict)
    error_rate: float = 0.0
    retry_rate: float = 0.0
    abandonment_rate: float = 0.0


@dataclass
class TrustMetrics:
    """Trust and reputation metrics"""
    trust_score: float = 0.5  # 0-1 scale
    content_quality_score: float = 0.5
    guideline_compliance_score: float = 1.0
    community_feedback_score: float = 0.5
    verified_professional: bool = False
    verification_date: Optional[datetime] = None


@dataclass
class UserProfile:
    """Comprehensive user profile"""
    user_id: str
    created_at: datetime
    last_active: datetime
    
    # Basic info
    tier: str = "basic"
    segment: UserSegment = UserSegment.CASUAL_USER
    primary_intention: IntentionType = IntentionType.PERSONAL_PROJECT
    
    # Activity tracking
    total_requests: int = 0
    successful_requests: int = 0
    content_history: List[ContentRequest] = field(default_factory=list)
    
    # Preferences and behavior
    preferences: UserPreferences = field(default_factory=UserPreferences)
    behavior_metrics: BehaviorMetrics = field(default_factory=BehaviorMetrics)
    trust_metrics: TrustMetrics = field(default_factory=TrustMetrics)
    
    # Pattern tracking
    content_patterns: Dict[str, int] = field(default_factory=dict)
    time_patterns: Dict[str, int] = field(default_factory=dict)
    theme_frequencies: Dict[str, int] = field(default_factory=dict)
    
    # Personalization
    recommended_features: List[str] = field(default_factory=list)
    suggested_improvements: List[str] = field(default_factory=list)
    learning_progress: Dict[str, float] = field(default_factory=dict)


class UserProfileSystem:
    """Manages user profiles and behavior analysis"""
    
    def __init__(self, profile_dir: str = "/var/projects/ai-integration-platform/user_profiles"):
        self.profile_dir = Path(profile_dir)
        self.profile_dir.mkdir(exist_ok=True)
        
        # Pattern detection thresholds
        self.pattern_thresholds = {
            "creative_professional": {
                "min_requests": 50,
                "quality_score": 0.8,
                "advanced_feature_usage": 0.6
            },
            "content_creator": {
                "min_requests": 20,
                "consistency": 0.7,
                "category_focus": 0.6
            },
            "researcher": {
                "experimentation_rate": 0.4,
                "category_diversity": 0.7,
                "learning_features_usage": 0.5
            }
        }
        
        # Theme keywords for categorization
        self.theme_keywords = {
            ContentCategory.NATURE: ["sunset", "ocean", "mountain", "forest", "sky", "landscape"],
            ContentCategory.URBAN: ["city", "building", "street", "urban", "architecture", "skyline"],
            ContentCategory.PORTRAIT: ["person", "face", "portrait", "people", "character", "human"],
            ContentCategory.ABSTRACT: ["abstract", "surreal", "conceptual", "geometric", "pattern"],
            ContentCategory.NARRATIVE: ["story", "scene", "dialogue", "plot", "character", "narrative"],
            ContentCategory.ARTISTIC: ["artistic", "creative", "aesthetic", "stylized", "expressive"],
        }
        
        # Intention indicators
        self.intention_indicators = {
            IntentionType.COMMERCIAL_PROJECT: ["client", "commercial", "product", "brand", "marketing"],
            IntentionType.EDUCATIONAL_CONTENT: ["tutorial", "educational", "teaching", "learning", "demonstration"],
            IntentionType.ARTISTIC_EXPRESSION: ["artistic", "creative", "experimental", "abstract", "expressive"],
            IntentionType.RESEARCH_EXPLORATION: ["test", "experiment", "research", "study", "analysis"],
        }
    
    def get_user_id(self, request_context: Dict[str, Any]) -> str:
        """Generate consistent user ID from request context"""
        if 'api_key' in request_context and request_context['api_key']:
            return hashlib.sha256(request_context['api_key'].encode()).hexdigest()
        
        identity_string = f"{request_context.get('ip', 'unknown')}:{request_context.get('user_agent', 'unknown')}"
        return hashlib.sha256(identity_string.encode()).hexdigest()
    
    def load_profile(self, user_id: str) -> UserProfile:
        """Load or create user profile"""
        profile_path = self.profile_dir / f"{user_id}_profile.json"
        
        if profile_path.exists():
            try:
                with open(profile_path, 'r') as f:
                    data = json.load(f)
                    
                # Reconstruct profile
                profile = UserProfile(
                    user_id=user_id,
                    created_at=datetime.fromisoformat(data['created_at']),
                    last_active=datetime.fromisoformat(data['last_active']),
                    tier=data.get('tier', 'basic'),
                    segment=UserSegment(data.get('segment', 'casual_user')),
                    primary_intention=IntentionType(data.get('primary_intention', 'personal_project')),
                    total_requests=data.get('total_requests', 0),
                    successful_requests=data.get('successful_requests', 0),
                    content_patterns=data.get('content_patterns', {}),
                    time_patterns=data.get('time_patterns', {}),
                    theme_frequencies=data.get('theme_frequencies', {}),
                    recommended_features=data.get('recommended_features', []),
                    suggested_improvements=data.get('suggested_improvements', []),
                    learning_progress=data.get('learning_progress', {})
                )
                
                # Load nested objects
                if 'preferences' in data:
                    profile.preferences = UserPreferences(**data['preferences'])
                if 'behavior_metrics' in data:
                    profile.behavior_metrics = BehaviorMetrics(**data['behavior_metrics'])
                if 'trust_metrics' in data:
                    profile.trust_metrics = TrustMetrics(
                        trust_score=data['trust_metrics']['trust_score'],
                        content_quality_score=data['trust_metrics']['content_quality_score'],
                        guideline_compliance_score=data['trust_metrics']['guideline_compliance_score'],
                        community_feedback_score=data['trust_metrics']['community_feedback_score'],
                        verified_professional=data['trust_metrics']['verified_professional']
                    )
                
                # Load content history (last 100 only)
                if 'content_history' in data:
                    for item in data['content_history'][-100:]:
                        profile.content_history.append(ContentRequest(
                            timestamp=datetime.fromisoformat(item['timestamp']),
                            prompt=item['prompt'],
                            category=ContentCategory(item['category']),
                            detected_intention=IntentionType(item['detected_intention']),
                            quality_score=item['quality_score'],
                            used_advanced_features=item['used_advanced_features'],
                            response_time=item['response_time'],
                            satisfaction_score=item.get('satisfaction_score')
                        ))
                
                return profile
            except Exception as e:
                logger.error(f"Error loading profile {user_id}: {e}")
        
        # Create new profile
        return UserProfile(
            user_id=user_id,
            created_at=datetime.now(),
            last_active=datetime.now()
        )
    
    def save_profile(self, profile: UserProfile):
        """Save user profile to disk"""
        profile_path = self.profile_dir / f"{profile.user_id}_profile.json"
        
        # Convert to serializable format
        data = {
            'user_id': profile.user_id,
            'created_at': profile.created_at.isoformat(),
            'last_active': profile.last_active.isoformat(),
            'tier': profile.tier,
            'segment': profile.segment.value,
            'primary_intention': profile.primary_intention.value,
            'total_requests': profile.total_requests,
            'successful_requests': profile.successful_requests,
            'content_patterns': profile.content_patterns,
            'time_patterns': profile.time_patterns,
            'theme_frequencies': profile.theme_frequencies,
            'recommended_features': profile.recommended_features,
            'suggested_improvements': profile.suggested_improvements,
            'learning_progress': profile.learning_progress,
            'preferences': {
                'preferred_style': profile.preferences.preferred_style,
                'preferred_quality': profile.preferences.preferred_quality,
                'preferred_categories': [c.value for c in profile.preferences.preferred_categories],
                'favorite_themes': profile.preferences.favorite_themes,
                'language': profile.preferences.language,
                'timezone': profile.preferences.timezone,
                'notification_preferences': profile.preferences.notification_preferences,
                'privacy_level': profile.preferences.privacy_level
            },
            'behavior_metrics': {
                'avg_session_duration': profile.behavior_metrics.avg_session_duration,
                'avg_requests_per_session': profile.behavior_metrics.avg_requests_per_session,
                'peak_usage_hours': profile.behavior_metrics.peak_usage_hours,
                'feature_usage': profile.behavior_metrics.feature_usage,
                'error_rate': profile.behavior_metrics.error_rate,
                'retry_rate': profile.behavior_metrics.retry_rate,
                'abandonment_rate': profile.behavior_metrics.abandonment_rate
            },
            'trust_metrics': {
                'trust_score': profile.trust_metrics.trust_score,
                'content_quality_score': profile.trust_metrics.content_quality_score,
                'guideline_compliance_score': profile.trust_metrics.guideline_compliance_score,
                'community_feedback_score': profile.trust_metrics.community_feedback_score,
                'verified_professional': profile.trust_metrics.verified_professional,
                'verification_date': profile.trust_metrics.verification_date.isoformat() if profile.trust_metrics.verification_date else None
            },
            'content_history': [
                {
                    'timestamp': req.timestamp.isoformat(),
                    'prompt': req.prompt[:200],  # Truncate for storage
                    'category': req.category.value,
                    'detected_intention': req.detected_intention.value,
                    'quality_score': req.quality_score,
                    'used_advanced_features': req.used_advanced_features,
                    'response_time': req.response_time,
                    'satisfaction_score': req.satisfaction_score
                }
                for req in profile.content_history[-100:]  # Keep last 100
            ]
        }
        
        with open(profile_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def categorize_content(self, prompt: str) -> ContentCategory:
        """Categorize content based on prompt"""
        prompt_lower = prompt.lower()
        category_scores = Counter()
        
        for category, keywords in self.theme_keywords.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    category_scores[category] += 1
        
        if category_scores:
            return category_scores.most_common(1)[0][0]
        return ContentCategory.ABSTRACT
    
    def detect_intention(self, prompt: str, user_history: List[ContentRequest]) -> IntentionType:
        """Detect user intention from prompt and history"""
        prompt_lower = prompt.lower()
        
        # Check prompt for intention indicators
        for intention, indicators in self.intention_indicators.items():
            for indicator in indicators:
                if indicator in prompt_lower:
                    return intention
        
        # Analyze history patterns
        if len(user_history) >= 5:
            recent_intentions = [req.detected_intention for req in user_history[-5:]]
            most_common = Counter(recent_intentions).most_common(1)
            if most_common and most_common[0][1] >= 3:
                return most_common[0][0]
        
        return IntentionType.PERSONAL_PROJECT
    
    def analyze_patterns(self, profile: UserProfile) -> Dict[str, Any]:
        """Analyze user patterns and behaviors"""
        analysis = {
            'content_consistency': 0.0,
            'usage_regularity': 0.0,
            'quality_trend': 'stable',
            'primary_categories': [],
            'usage_pattern': 'irregular',
            'skill_level': 'beginner'
        }
        
        if len(profile.content_history) < 5:
            return analysis
        
        # Content consistency
        recent_categories = [req.category for req in profile.content_history[-20:]]
        if recent_categories:
            category_counts = Counter(recent_categories)
            total = sum(category_counts.values())
            top_category_ratio = category_counts.most_common(1)[0][1] / total
            analysis['content_consistency'] = top_category_ratio
            analysis['primary_categories'] = [cat.value for cat, _ in category_counts.most_common(3)]
        
        # Usage regularity
        if len(profile.content_history) >= 10:
            timestamps = [req.timestamp for req in profile.content_history[-30:]]
            intervals = []
            for i in range(1, len(timestamps)):
                interval = (timestamps[i] - timestamps[i-1]).total_seconds() / 3600  # Hours
                intervals.append(interval)
            
            if intervals:
                avg_interval = statistics.mean(intervals)
                std_interval = statistics.stdev(intervals) if len(intervals) > 1 else 0
                
                if avg_interval < 24 and std_interval < 12:
                    analysis['usage_pattern'] = 'daily'
                elif avg_interval < 168 and std_interval < 48:
                    analysis['usage_pattern'] = 'weekly'
                elif std_interval / avg_interval < 0.5:
                    analysis['usage_pattern'] = 'regular'
        
        # Quality trend
        recent_quality = [req.quality_score for req in profile.content_history[-10:] if req.quality_score]
        if len(recent_quality) >= 5:
            first_half = statistics.mean(recent_quality[:len(recent_quality)//2])
            second_half = statistics.mean(recent_quality[len(recent_quality)//2:])
            
            if second_half > first_half * 1.1:
                analysis['quality_trend'] = 'improving'
            elif second_half < first_half * 0.9:
                analysis['quality_trend'] = 'declining'
        
        # Skill level assessment
        if profile.successful_requests > 100:
            if profile.behavior_metrics.feature_usage.get('advanced', 0) > 50:
                analysis['skill_level'] = 'expert'
            elif profile.successful_requests > 50:
                analysis['skill_level'] = 'advanced'
            else:
                analysis['skill_level'] = 'intermediate'
        
        return analysis
    
    def update_segment(self, profile: UserProfile):
        """Update user segment based on behavior"""
        patterns = self.analyze_patterns(profile)
        
        # Creative professional detection
        if (profile.total_requests >= self.pattern_thresholds['creative_professional']['min_requests'] and
            profile.trust_metrics.content_quality_score >= self.pattern_thresholds['creative_professional']['quality_score'] and
            patterns['skill_level'] in ['advanced', 'expert']):
            profile.segment = UserSegment.CREATIVE_PROFESSIONAL
        
        # Content creator detection
        elif (patterns['content_consistency'] >= self.pattern_thresholds['content_creator']['category_focus'] and
              patterns['usage_pattern'] in ['daily', 'regular']):
            profile.segment = UserSegment.CONTENT_CREATOR
        
        # Researcher detection
        elif len(set(profile.content_patterns.keys())) >= 5:  # Diverse interests
            profile.segment = UserSegment.RESEARCHER
        
        # Power user detection
        elif profile.total_requests > 200 and profile.successful_requests / profile.total_requests > 0.9:
            profile.segment = UserSegment.POWER_USER
        
        # Filmmaker detection
        elif ContentCategory.NARRATIVE in profile.preferences.preferred_categories:
            profile.segment = UserSegment.FILMMAKER
        
        # Artist detection
        elif ContentCategory.ARTISTIC in profile.preferences.preferred_categories:
            profile.segment = UserSegment.ARTIST
    
    def generate_recommendations(self, profile: UserProfile) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        patterns = self.analyze_patterns(profile)
        
        # Feature recommendations
        if profile.segment == UserSegment.CREATIVE_PROFESSIONAL:
            if 'batch_processing' not in profile.behavior_metrics.feature_usage:
                recommendations.append("Try batch processing for efficient workflow")
            if 'style_transfer' not in profile.behavior_metrics.feature_usage:
                recommendations.append("Explore style transfer for consistent branding")
        
        elif profile.segment == UserSegment.CONTENT_CREATOR:
            if patterns['content_consistency'] < 0.8:
                recommendations.append("Focus on your primary content category for better consistency")
            recommendations.append("Use templates to maintain your signature style")
        
        elif profile.segment == UserSegment.RESEARCHER:
            recommendations.append("Try A/B testing different prompt variations")
            recommendations.append("Use analytics to track performance metrics")
        
        # Quality improvements
        if patterns['quality_trend'] == 'declining':
            recommendations.append("Review successful prompts from your history")
            recommendations.append("Take a break to avoid creative fatigue")
        elif patterns['quality_trend'] == 'improving':
            recommendations.append("You're improving! Try more advanced techniques")
        
        # Usage pattern suggestions
        if patterns['usage_pattern'] == 'irregular':
            recommendations.append("Set a regular schedule for better results")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def track_request(self, user_id: str, prompt: str, response_data: Dict[str, Any], 
                     request_context: Dict[str, Any]) -> UserProfile:
        """Track a user request and update profile"""
        profile = self.load_profile(user_id)
        
        # Update basic counters
        profile.total_requests += 1
        profile.last_active = datetime.now()
        
        if response_data.get('success'):
            profile.successful_requests += 1
        
        # Categorize content
        category = self.categorize_content(prompt)
        intention = self.detect_intention(prompt, profile.content_history)
        
        # Create request record
        content_request = ContentRequest(
            timestamp=datetime.now(),
            prompt=prompt,
            category=category,
            detected_intention=intention,
            quality_score=response_data.get('confidence', 0.5),
            used_advanced_features='claude' in response_data.get('service_used', '').lower(),
            response_time=response_data.get('processing_time', 1.0),
            satisfaction_score=response_data.get('satisfaction_score')
        )
        
        profile.content_history.append(content_request)
        
        # Update patterns
        profile.content_patterns[category.value] = profile.content_patterns.get(category.value, 0) + 1
        hour_key = str(datetime.now().hour)
        profile.time_patterns[hour_key] = profile.time_patterns.get(hour_key, 0) + 1
        
        # Extract themes
        for word in prompt.lower().split():
            if len(word) > 4:  # Skip short words
                profile.theme_frequencies[word] = profile.theme_frequencies.get(word, 0) + 1
        
        # Update behavior metrics
        if 'claude' in response_data.get('service_used', '').lower():
            profile.behavior_metrics.feature_usage['claude'] = profile.behavior_metrics.feature_usage.get('claude', 0) + 1
        
        # Update trust scores
        if response_data.get('success'):
            # Gradually increase trust for successful requests
            profile.trust_metrics.trust_score = min(1.0, profile.trust_metrics.trust_score + 0.001)
            profile.trust_metrics.content_quality_score = (
                profile.trust_metrics.content_quality_score * 0.95 + 
                response_data.get('confidence', 0.5) * 0.05
            )
        
        # Update segment and generate recommendations
        self.update_segment(profile)
        profile.recommended_features = self.generate_recommendations(profile)
        
        # Save updated profile
        self.save_profile(profile)
        
        return profile
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about a user"""
        profile = self.load_profile(user_id)
        patterns = self.analyze_patterns(profile)
        
        # Calculate additional insights
        category_distribution = {}
        if profile.content_patterns:
            total = sum(profile.content_patterns.values())
            category_distribution = {
                cat: count/total for cat, count in profile.content_patterns.items()
            }
        
        # Peak hours
        peak_hours = []
        if profile.time_patterns:
            sorted_hours = sorted(profile.time_patterns.items(), 
                                key=lambda x: x[1], reverse=True)
            peak_hours = [int(hour) for hour, _ in sorted_hours[:3]]
        
        # Top themes
        top_themes = []
        if profile.theme_frequencies:
            sorted_themes = sorted(profile.theme_frequencies.items(), 
                                 key=lambda x: x[1], reverse=True)
            top_themes = [theme for theme, _ in sorted_themes[:10]]
        
        return {
            'user_id': user_id,
            'segment': profile.segment.value,
            'primary_intention': profile.primary_intention.value,
            'trust_level': self._get_trust_level(profile.trust_metrics.trust_score),
            'activity_summary': {
                'total_requests': profile.total_requests,
                'success_rate': profile.successful_requests / max(1, profile.total_requests),
                'last_active': profile.last_active.isoformat(),
                'account_age_days': (datetime.now() - profile.created_at).days
            },
            'content_insights': {
                'primary_categories': patterns['primary_categories'],
                'category_distribution': category_distribution,
                'content_consistency': patterns['content_consistency'],
                'quality_trend': patterns['quality_trend']
            },
            'behavior_insights': {
                'usage_pattern': patterns['usage_pattern'],
                'skill_level': patterns['skill_level'],
                'peak_hours': peak_hours,
                'preferred_features': list(profile.behavior_metrics.feature_usage.keys())
            },
            'personalization': {
                'recommended_features': profile.recommended_features,
                'suggested_improvements': profile.suggested_improvements,
                'top_themes': top_themes
            }
        }
    
    def _get_trust_level(self, trust_score: float) -> str:
        """Convert trust score to trust level"""
        if trust_score >= 0.9:
            return "excellent"
        elif trust_score >= 0.7:
            return "good"
        elif trust_score >= 0.5:
            return "moderate"
        elif trust_score >= 0.3:
            return "low"
        else:
            return "very_low"
    
    def get_segment_statistics(self) -> Dict[str, Any]:
        """Get statistics about all user segments"""
        segment_counts = Counter()
        intention_counts = Counter()
        total_users = 0
        
        for profile_file in self.profile_dir.glob("*_profile.json"):
            try:
                with open(profile_file, 'r') as f:
                    data = json.load(f)
                    segment_counts[data.get('segment', 'casual_user')] += 1
                    intention_counts[data.get('primary_intention', 'personal_project')] += 1
                    total_users += 1
            except:
                continue
        
        return {
            'total_users': total_users,
            'segment_distribution': dict(segment_counts),
            'intention_distribution': dict(intention_counts),
            'segments': {
                segment.value: {
                    'count': segment_counts.get(segment.value, 0),
                    'percentage': segment_counts.get(segment.value, 0) / max(1, total_users)
                }
                for segment in UserSegment
            }
        }


# Global instance
_profile_system: Optional[UserProfileSystem] = None


def get_profile_system() -> UserProfileSystem:
    """Get global user profile system instance"""
    global _profile_system
    if _profile_system is None:
        _profile_system = UserProfileSystem()
    return _profile_system


# Export UserProfileManager for compatibility
UserProfileManager = UserProfileSystem

# Export all classes
__all__ = ['UserProfileSystem', 'UserProfileManager', 'UserProfile', 'get_profile_system']