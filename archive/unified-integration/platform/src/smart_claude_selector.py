"""
Smart Claude Model Selector

Intelligently selects the appropriate Claude model based on:
1. Request complexity
2. User tier/segment
3. Quality requirements
4. Budget constraints
5. Performance needs

Models (from cheapest to most expensive):
- claude-3-haiku: Fast, cheap, good for simple tasks
- claude-3-sonnet: Balanced, good for most tasks
- claude-3-opus: Premium, for complex creative tasks
"""

import re
import logging
from typing import Dict, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class ModelTier(Enum):
    """Claude model tiers"""
    HAIKU = "claude-3-haiku-20240307"  # $0.25 / 1M tokens
    SONNET = "claude-3-5-sonnet-20241022"  # $3 / 1M tokens - Updated to latest  
    OPUS = "claude-3-5-sonnet-20241022"  # Using Sonnet as highest tier


@dataclass
class ModelCosts:
    """Cost per million tokens"""
    input_cost: float
    output_cost: float
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost in dollars"""
        return (input_tokens * self.input_cost + output_tokens * self.output_cost) / 1_000_000


class ComplexityAnalyzer:
    """Analyzes prompt complexity to determine required model"""
    
    def __init__(self):
        # Complexity indicators
        self.simple_indicators = [
            "simple", "basic", "quick", "brief", "short",
            "list", "summarize", "translate", "convert"
        ]
        
        self.moderate_indicators = [
            "analyze", "explain", "compare", "describe",
            "creative", "story", "narrative", "detailed"
        ]
        
        self.complex_indicators = [
            "sophisticated", "intricate", "nuanced", "complex",
            "philosophical", "artistic", "cinematic", "profound",
            "multi-layered", "psychological", "emotional depth"
        ]
        
        # Length thresholds
        self.length_thresholds = {
            "simple": 50,  # < 50 words
            "moderate": 200,  # 50-200 words
            "complex": float('inf')  # > 200 words
        }
        
        # Special requirements that need better models
        self.quality_requirements = {
            "high_creativity": ["artistic", "creative", "innovative", "unique"],
            "emotional_depth": ["emotional", "psychological", "intimate", "profound"],
            "technical_accuracy": ["technical", "precise", "accurate", "detailed"],
            "narrative_quality": ["story", "narrative", "cinematic", "dramatic"]
        }
    
    def analyze_complexity(self, prompt: str) -> Tuple[str, float]:
        """
        Analyze prompt complexity
        Returns: (complexity_level, confidence_score)
        """
        prompt_lower = prompt.lower()
        word_count = len(prompt.split())
        
        # Initialize scores
        simple_score = 0
        moderate_score = 0
        complex_score = 0
        
        # Check indicators
        for indicator in self.simple_indicators:
            if indicator in prompt_lower:
                simple_score += 1
        
        for indicator in self.moderate_indicators:
            if indicator in prompt_lower:
                moderate_score += 1
        
        for indicator in self.complex_indicators:
            if indicator in prompt_lower:
                complex_score += 2  # Weight complex indicators more
        
        # Consider length
        if word_count < self.length_thresholds["simple"]:
            simple_score += 2
        elif word_count < self.length_thresholds["moderate"]:
            moderate_score += 2
        else:
            complex_score += 2
        
        # Check for special quality requirements
        quality_boost = 0
        for req_type, keywords in self.quality_requirements.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    quality_boost += 1
        
        # Apply quality boost to higher tiers
        moderate_score += quality_boost * 0.5
        complex_score += quality_boost
        
        # Determine complexity
        total_score = simple_score + moderate_score + complex_score
        if total_score == 0:
            return "simple", 0.5
        
        simple_ratio = simple_score / total_score
        moderate_ratio = moderate_score / total_score
        complex_ratio = complex_score / total_score
        
        if complex_ratio > 0.4:
            return "complex", complex_ratio
        elif moderate_ratio > 0.4:
            return "moderate", moderate_ratio
        else:
            return "simple", simple_ratio


class SmartClaudeSelector:
    """Intelligently selects Claude model based on multiple factors"""
    
    def __init__(self):
        self.complexity_analyzer = ComplexityAnalyzer()
        
        # Model capabilities and costs
        self.model_costs = {
            ModelTier.HAIKU: ModelCosts(0.25, 1.25),  # per 1M tokens
            ModelTier.SONNET: ModelCosts(3.0, 15.0),
            ModelTier.OPUS: ModelCosts(15.0, 75.0)
        }
        
        # Model selection rules
        self.selection_rules = {
            "simple": {
                "default": ModelTier.HAIKU,
                "quality_threshold": 0.8,  # Use better model if quality needed
                "upgrade_to": ModelTier.SONNET
            },
            "moderate": {
                "default": ModelTier.SONNET,
                "quality_threshold": 0.9,
                "upgrade_to": ModelTier.OPUS,
                "downgrade_to": ModelTier.HAIKU,
                "downgrade_threshold": 0.3
            },
            "complex": {
                "default": ModelTier.OPUS,
                "downgrade_to": ModelTier.SONNET,
                "downgrade_threshold": 0.5  # Only if really needed for cost
            }
        }
        
        # User segment preferences
        self.segment_preferences = {
            "creative_professional": {"min_model": ModelTier.SONNET, "prefer": ModelTier.OPUS},
            "content_creator": {"min_model": ModelTier.HAIKU, "prefer": ModelTier.SONNET},
            "researcher": {"min_model": ModelTier.HAIKU, "prefer": ModelTier.SONNET},
            "artist": {"min_model": ModelTier.SONNET, "prefer": ModelTier.OPUS},
            "filmmaker": {"min_model": ModelTier.SONNET, "prefer": ModelTier.OPUS},
            "casual_user": {"min_model": ModelTier.HAIKU, "prefer": ModelTier.HAIKU},
            "power_user": {"min_model": ModelTier.SONNET, "prefer": ModelTier.OPUS}
        }
    
    def select_model(self, 
                    prompt: str,
                    user_segment: str = "casual_user",
                    user_tier: str = "basic",
                    quality_required: float = 0.7,
                    budget_remaining: float = 10.0,
                    force_quality: bool = False) -> Dict[str, Any]:
        """
        Select the optimal Claude model
        
        Args:
            prompt: The user's prompt
            user_segment: User segment (from profile system)
            user_tier: Subscription tier (basic, premium, admin)
            quality_required: Required quality level (0-1)
            budget_remaining: Daily budget remaining in dollars
            force_quality: Force high quality for trial/demo
            
        Returns:
            {
                "model": ModelTier,
                "reasoning": str,
                "estimated_cost": float,
                "quality_score": float
            }
        """
        # Analyze prompt complexity
        complexity, confidence = self.complexity_analyzer.analyze_complexity(prompt)
        
        # Get base model from complexity
        rules = self.selection_rules[complexity]
        selected_model = rules["default"]
        
        # Consider user segment preferences
        if user_segment in self.segment_preferences:
            prefs = self.segment_preferences[user_segment]
            
            # Upgrade to minimum model for segment
            if self._model_rank(selected_model) < self._model_rank(prefs["min_model"]):
                selected_model = prefs["min_model"]
            
            # Upgrade to preferred if quality needed
            if quality_required > 0.8 and user_tier in ["premium", "admin"]:
                selected_model = prefs["prefer"]
        
        # Handle trial/demo forcing quality
        if force_quality:
            if complexity == "simple":
                selected_model = ModelTier.SONNET
            else:
                selected_model = ModelTier.OPUS
            reasoning = "Using premium model for trial/demo to showcase best quality"
        else:
            reasoning = f"Selected based on {complexity} complexity (confidence: {confidence:.2f})"
        
        # Budget check - downgrade if needed
        estimated_tokens = len(prompt.split()) * 10  # Rough estimate
        estimated_cost = self.model_costs[selected_model].estimate_cost(
            estimated_tokens, estimated_tokens * 2
        )
        
        if estimated_cost > budget_remaining * 0.1:  # Don't use more than 10% of remaining budget
            # Try to downgrade
            if complexity in ["moderate", "complex"] and "downgrade_to" in rules:
                downgrade_model = rules["downgrade_to"]
                downgrade_cost = self.model_costs[downgrade_model].estimate_cost(
                    estimated_tokens, estimated_tokens * 2
                )
                if downgrade_cost < budget_remaining * 0.05:
                    selected_model = downgrade_model
                    reasoning += f" (downgraded for budget: ${budget_remaining:.2f} remaining)"
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(selected_model, complexity, confidence)
        
        # Special handling for certain content
        if any(term in prompt.lower() for term in ["artistic", "cinematic", "profound", "sophisticated"]):
            if selected_model == ModelTier.HAIKU and quality_required > 0.6:
                selected_model = ModelTier.SONNET
                reasoning += " (upgraded for artistic content)"
        
        return {
            "model": selected_model.value,
            "model_tier": selected_model.name,
            "reasoning": reasoning,
            "estimated_cost": estimated_cost,
            "quality_score": quality_score,
            "complexity": complexity,
            "budget_safe": estimated_cost < budget_remaining * 0.1
        }
    
    def _model_rank(self, model: ModelTier) -> int:
        """Get model rank (higher is better)"""
        ranks = {
            ModelTier.HAIKU: 1,
            ModelTier.SONNET: 2,
            ModelTier.OPUS: 3
        }
        return ranks.get(model, 0)
    
    def _calculate_quality_score(self, model: ModelTier, complexity: str, confidence: float) -> float:
        """Calculate expected quality score"""
        base_scores = {
            ModelTier.HAIKU: 0.7,
            ModelTier.SONNET: 0.85,
            ModelTier.OPUS: 0.95
        }
        
        complexity_modifiers = {
            "simple": 1.0,
            "moderate": 0.95,
            "complex": 0.9
        }
        
        base = base_scores.get(model, 0.7)
        modifier = complexity_modifiers.get(complexity, 1.0)
        
        return min(1.0, base * modifier * (0.8 + confidence * 0.2))
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        for tier in ModelTier:
            if tier.value == model_name:
                return {
                    "name": tier.name,
                    "model_id": tier.value,
                    "costs": {
                        "input_per_1m": self.model_costs[tier].input_cost,
                        "output_per_1m": self.model_costs[tier].output_cost
                    },
                    "characteristics": self._get_model_characteristics(tier)
                }
        return {}
    
    def _get_model_characteristics(self, model: ModelTier) -> Dict[str, str]:
        """Get model characteristics"""
        characteristics = {
            ModelTier.HAIKU: {
                "speed": "Very fast",
                "quality": "Good for simple tasks",
                "cost": "Very economical",
                "best_for": "Quick responses, summaries, simple creative tasks"
            },
            ModelTier.SONNET: {
                "speed": "Fast",
                "quality": "Excellent for most tasks",
                "cost": "Balanced",
                "best_for": "Creative writing, analysis, complex reasoning"
            },
            ModelTier.OPUS: {
                "speed": "Moderate",
                "quality": "Best available quality",
                "cost": "Premium",
                "best_for": "Highly creative tasks, nuanced content, professional work"
            }
        }
        return characteristics.get(model, {})


# Global instance
_model_selector: Optional[SmartClaudeSelector] = None


def get_model_selector() -> SmartClaudeSelector:
    """Get global model selector instance"""
    global _model_selector
    if _model_selector is None:
        _model_selector = SmartClaudeSelector()
    return _model_selector