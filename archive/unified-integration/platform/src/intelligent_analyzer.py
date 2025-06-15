from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re
from collections import Counter


class ContentSensitivity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class OptimizationStrategy(Enum):
    STANDARD = "standard"
    MODERATE = "moderate"
    DEEP_ELABORATION = "deep_elaboration"
    MAXIMUM_CONTEXT = "maximum_context"


@dataclass
class PromptAnalysis:
    original_prompt: str
    detected_themes: List[str]
    sensitivity_level: ContentSensitivity
    recommended_strategy: OptimizationStrategy
    detected_issues: List[str]
    auto_detected_context: str
    confidence_score: float
    specific_recommendations: List[str]


class IntelligentPromptAnalyzer:
    def __init__(self):
        # Sensitivity indicators with weights
        self.sensitivity_patterns = {
            "extreme": {
                "patterns": [
                    r'\b(explicit|graphic|extreme|intense)\b',
                    r'\b(violence|violent|gore|brutal)\b',
                    r'\b(disturbing|shocking|horrific)\b'
                ],
                "weight": 1.0
            },
            "high": {
                "patterns": [
                    r'\b(fight|combat|battle|war)\b',
                    r'\b(blood|injury|wound|hurt)\b',
                    r'\b(controversial|sensitive|taboo)\b',
                    r'\b(age\s*(gap|difference)|older.*younger)\b',
                    r'\b(religious|spiritual|ritual|sacred)\b'
                ],
                "weight": 0.8
            },
            "medium": {
                "patterns": [
                    r'\b(action|conflict|tension)\b',
                    r'\b(dramatic|intense|emotional)\b',
                    r'\b(challenging|difficult|complex)\b',
                    r'\b(romance|love|relationship)\b'
                ],
                "weight": 0.5
            },
            "low": {
                "patterns": [
                    r'\b(peaceful|calm|serene)\b',
                    r'\b(beautiful|scenic|landscape)\b',
                    r'\b(educational|informative|documentary)\b'
                ],
                "weight": 0.2
            }
        }
        
        # Theme detection patterns
        self.theme_patterns = {
            "violence_action": [
                r'\b(fight|combat|battle|war|violence|weapon|gun|sword)\b',
                r'\b(punch|kick|attack|shoot|strike|hit)\b'
            ],
            "romance_relationship": [
                r'\b(romance|love|kiss|relationship|couple|marriage)\b',
                r'\b(date|romantic|affection|passion)\b'
            ],
            "age_related": [
                r'\b(age|older|younger|elderly|youth|generation)\b',
                r'\b(mentor|student|teacher|gap)\b'
            ],
            "spiritual_religious": [
                r'\b(spiritual|religious|sacred|divine|holy|prayer)\b',
                r'\b(ritual|ceremony|worship|devotion|faith)\b'
            ],
            "experimental_artistic": [
                r'\b(surreal|abstract|experimental|avant-garde|bold)\b',
                r'\b(glitch|distort|morph|transform|reality-bending)\b'
            ],
            "medical_anatomical": [
                r'\b(medical|anatomy|surgery|patient|doctor|hospital)\b',
                r'\b(blood|organ|procedure|treatment)\b'
            ],
            "controversial_social": [
                r'\b(controversial|political|social|protest|rebellion)\b',
                r'\b(taboo|forbidden|censored|sensitive)\b'
            ]
        }
        
        # Context recommendations based on themes
        self.context_recommendations = {
            "violence_action": {
                "context": "cinematic",
                "framing": ["choreographed sequences", "professional stunt work", "theatrical performance"],
                "additional": ["safety protocols", "trained professionals", "controlled environment"]
            },
            "romance_relationship": {
                "context": "artistic",
                "framing": ["literary adaptation", "classic narrative", "emotional storytelling"],
                "additional": ["professional actors", "artistic expression", "cultural significance"]
            },
            "age_related": {
                "context": "educational",
                "framing": ["generational dynamics", "mentorship themes", "wisdom exchange"],
                "additional": ["literary traditions", "cultural documentation", "scholarly examination"]
            },
            "spiritual_religious": {
                "context": "documentary",
                "framing": ["cultural practices", "spiritual traditions", "religious documentation"],
                "additional": ["respectful portrayal", "educational purpose", "cultural advisors"]
            },
            "experimental_artistic": {
                "context": "artistic",
                "framing": ["avant-garde expression", "experimental techniques", "artistic innovation"],
                "additional": ["museum quality", "critical theory", "institutional support"]
            }
        }
    
    def analyze_prompt(self, prompt: str) -> PromptAnalysis:
        """Perform comprehensive analysis of the prompt"""
        prompt_lower = prompt.lower()
        
        # Detect themes
        detected_themes = self._detect_themes(prompt_lower)
        
        # Calculate sensitivity level
        sensitivity_level, sensitivity_score = self._calculate_sensitivity(prompt_lower)
        
        # Detect specific issues
        detected_issues = self._detect_issues(prompt_lower)
        
        # Determine optimization strategy
        recommended_strategy = self._determine_strategy(
            sensitivity_level, 
            detected_themes, 
            detected_issues
        )
        
        # Auto-detect best context
        auto_context = self._auto_detect_context(detected_themes, prompt_lower)
        
        # Generate specific recommendations
        recommendations = self._generate_recommendations(
            detected_themes, 
            sensitivity_level, 
            detected_issues
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(
            sensitivity_level,
            recommended_strategy,
            len(recommendations)
        )
        
        return PromptAnalysis(
            original_prompt=prompt,
            detected_themes=detected_themes,
            sensitivity_level=sensitivity_level,
            recommended_strategy=recommended_strategy,
            detected_issues=detected_issues,
            auto_detected_context=auto_context,
            confidence_score=confidence_score,
            specific_recommendations=recommendations
        )
    
    def _detect_themes(self, prompt_lower: str) -> List[str]:
        """Detect themes present in the prompt"""
        detected = []
        
        for theme, patterns in self.theme_patterns.items():
            for pattern in patterns:
                if re.search(pattern, prompt_lower):
                    detected.append(theme)
                    break
        
        return list(set(detected))
    
    def _calculate_sensitivity(self, prompt_lower: str) -> Tuple[ContentSensitivity, float]:
        """Calculate sensitivity level and score"""
        total_score = 0.0
        matches = 0
        
        for level, data in self.sensitivity_patterns.items():
            for pattern in data["patterns"]:
                if re.search(pattern, prompt_lower):
                    total_score += data["weight"]
                    matches += 1
        
        # Determine level based on score
        if total_score >= 2.0 or matches >= 3:
            return ContentSensitivity.EXTREME, total_score
        elif total_score >= 1.5 or matches >= 2:
            return ContentSensitivity.HIGH, total_score
        elif total_score >= 0.8 or matches >= 1:
            return ContentSensitivity.MEDIUM, total_score
        else:
            return ContentSensitivity.LOW, total_score
    
    def _detect_issues(self, prompt_lower: str) -> List[str]:
        """Detect specific issues in the prompt"""
        issues = []
        
        # Check for vague language
        if len(prompt_lower.split()) < 5:
            issues.append("too_brief")
        
        # Check for generic terms
        generic_terms = ["person", "someone", "something", "somewhere"]
        for term in generic_terms:
            if term in prompt_lower:
                issues.append(f"generic_term:{term}")
        
        # Check for potentially problematic combinations
        if "age" in prompt_lower and "romance" in prompt_lower:
            issues.append("sensitive_combination:age_romance")
        
        if "violence" in prompt_lower or "fight" in prompt_lower:
            issues.append("action_content")
        
        # Check for missing context
        context_indicators = ["professional", "artistic", "educational", "documentary"]
        if not any(indicator in prompt_lower for indicator in context_indicators):
            issues.append("missing_context")
        
        return issues
    
    def _determine_strategy(self, 
                          sensitivity: ContentSensitivity, 
                          themes: List[str], 
                          issues: List[str]) -> OptimizationStrategy:
        """Determine the best optimization strategy"""
        
        # Extreme sensitivity always needs maximum context
        if sensitivity == ContentSensitivity.EXTREME:
            return OptimizationStrategy.MAXIMUM_CONTEXT
        
        # High sensitivity or multiple themes need deep elaboration
        if sensitivity == ContentSensitivity.HIGH or len(themes) >= 2:
            return OptimizationStrategy.DEEP_ELABORATION
        
        # Specific sensitive combinations
        if "sensitive_combination:age_romance" in issues:
            return OptimizationStrategy.MAXIMUM_CONTEXT
        
        # Experimental/artistic themes benefit from deep elaboration
        if "experimental_artistic" in themes:
            return OptimizationStrategy.DEEP_ELABORATION
        
        # Medium sensitivity or single theme
        if sensitivity == ContentSensitivity.MEDIUM or len(themes) == 1:
            return OptimizationStrategy.MODERATE
        
        # Default to standard
        return OptimizationStrategy.STANDARD
    
    def _auto_detect_context(self, themes: List[str], prompt_lower: str) -> str:
        """Auto-detect the best context based on themes"""
        
        # Priority order for context selection
        if "medical_anatomical" in themes:
            return "educational"
        elif "spiritual_religious" in themes:
            return "documentary"
        elif "experimental_artistic" in themes or "bold" in prompt_lower:
            return "bold"
        elif "violence_action" in themes:
            return "cinematic"
        elif "romance_relationship" in themes or "age_related" in themes:
            return "romance"
        elif "controversial_social" in themes:
            return "controversial"
        
        # Default based on keywords
        if any(word in prompt_lower for word in ["learn", "teach", "study", "educational"]):
            return "educational"
        elif any(word in prompt_lower for word in ["art", "creative", "aesthetic"]):
            return "artistic"
        
        return "general"
    
    def _generate_recommendations(self, 
                                themes: List[str], 
                                sensitivity: ContentSensitivity,
                                issues: List[str]) -> List[str]:
        """Generate specific recommendations"""
        recommendations = []
        
        # Theme-based recommendations
        for theme in themes:
            if theme in self.context_recommendations:
                rec = self.context_recommendations[theme]
                recommendations.append(f"Add {rec['framing'][0]} context")
                recommendations.append(f"Include {rec['additional'][0]}")
        
        # Sensitivity-based recommendations
        if sensitivity in [ContentSensitivity.HIGH, ContentSensitivity.EXTREME]:
            recommendations.append("Apply maximum contextual elaboration")
            recommendations.append("Add multiple layers of professional framing")
            recommendations.append("Include institutional endorsements")
        
        # Issue-based recommendations
        if "too_brief" in issues:
            recommendations.append("Expand with specific details and context")
        
        if "missing_context" in issues:
            recommendations.append("Add professional or artistic context")
        
        if any("generic_term" in issue for issue in issues):
            recommendations.append("Replace generic terms with specific descriptions")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _calculate_confidence(self, 
                            sensitivity: ContentSensitivity,
                            strategy: OptimizationStrategy,
                            num_recommendations: int) -> float:
        """Calculate confidence in successful optimization"""
        
        base_confidence = {
            ContentSensitivity.LOW: 0.95,
            ContentSensitivity.MEDIUM: 0.85,
            ContentSensitivity.HIGH: 0.75,
            ContentSensitivity.EXTREME: 0.65
        }
        
        strategy_boost = {
            OptimizationStrategy.STANDARD: 0.0,
            OptimizationStrategy.MODERATE: 0.05,
            OptimizationStrategy.DEEP_ELABORATION: 0.10,
            OptimizationStrategy.MAXIMUM_CONTEXT: 0.15
        }
        
        confidence = base_confidence.get(sensitivity, 0.8)
        confidence += strategy_boost.get(strategy, 0.0)
        
        # Adjust based on recommendations
        if num_recommendations > 3:
            confidence -= 0.05
        
        return min(confidence, 0.95)


class AutoOptimizer:
    def __init__(self):
        self.analyzer = IntelligentPromptAnalyzer()
    
    def auto_optimize(self, prompt: str) -> Dict[str, any]:
        """Automatically analyze and optimize a prompt"""
        
        # Analyze the prompt
        analysis = self.analyzer.analyze_prompt(prompt)
        
        # Build optimization parameters
        optimization_params = {
            "prompt": prompt,
            "detected_themes": analysis.detected_themes,
            "sensitivity_level": analysis.sensitivity_level.value,
            "strategy": analysis.recommended_strategy.value,
            "auto_context": analysis.auto_detected_context,
            "issues": analysis.detected_issues,
            "recommendations": analysis.specific_recommendations,
            "confidence_before": analysis.confidence_score
        }
        
        # Determine optimization approach
        if analysis.recommended_strategy == OptimizationStrategy.MAXIMUM_CONTEXT:
            optimization_params["type"] = "elaborate"
            optimization_params["theme"] = analysis.auto_detected_context
            optimization_params["depth"] = "maximum"
        elif analysis.recommended_strategy == OptimizationStrategy.DEEP_ELABORATION:
            optimization_params["type"] = "elaborate"
            optimization_params["theme"] = analysis.auto_detected_context
            optimization_params["depth"] = "advanced"
        else:
            optimization_params["type"] = "standard"
            optimization_params["theme"] = analysis.auto_detected_context
        
        return optimization_params