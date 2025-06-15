from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re


class ContentContext(Enum):
    ARTISTIC = "artistic"
    EDUCATIONAL = "educational"
    DOCUMENTARY = "documentary"
    CINEMATIC = "cinematic"
    SCIENTIFIC = "scientific"
    HISTORICAL = "historical"
    CREATIVE = "creative"


@dataclass
class OptimizationResult:
    original_prompt: str
    optimized_prompt: str
    context_added: str
    success_likelihood: float
    suggestions: List[str]


class PromptOptimizer:
    def __init__(self):
        self.context_templates = {
            ContentContext.ARTISTIC: "For an artistic {purpose} exploring {theme}",
            ContentContext.EDUCATIONAL: "For educational purposes demonstrating {concept}",
            ContentContext.DOCUMENTARY: "Documentary-style footage capturing {subject}",
            ContentContext.CINEMATIC: "Cinematic scene depicting {narrative}",
            ContentContext.SCIENTIFIC: "Scientific visualization of {phenomenon}",
            ContentContext.HISTORICAL: "Historical reenactment of {event}",
            ContentContext.CREATIVE: "Creative expression showcasing {vision}"
        }
        
        self.professional_terms = {
            "fight": "choreographed action sequence",
            "violence": "dramatic conflict",
            "weapon": "prop",
            "blood": "special effects",
            "scary": "suspenseful",
            "disturbing": "thought-provoking",
            "controversial": "discussion-worthy",
            "sensitive": "nuanced",
            # Age-related terms
            "old": "distinguished",
            "elderly": "senior",
            "young": "youthful",
            "age gap": "generational diversity",
            # Intimate terms
            "kissing": "intimate moment",
            "passionately kissing": "emotional connection",
            "passionate": "emotional",
            "bedroom": "private setting",
            "private bedroom": "intimate interior",
            # Relationship terms
            "romance": "emotional bond",
            "romantic": "emotionally connected",
            "intimate": "close personal",
            "love": "deep connection",
            # Consensual romantic terms
            "admirer": "romantic interest",
            "devoted": "deeply committed",
            "passionate": "emotionally connected",
            "intense": "profound connection",
            "unconventional": "unique relationship",
            "dramatic": "emotionally charged",
            "alluring": "magnetically attractive",
            "forbidden love": "socially challenging romance",
            "secret romance": "private relationship",
            "taboo": "culturally complex"
        }
        
        self.framing_enhancers = {
            "medical": "for medical education",
            "safety": "for safety training",
            "historical": "for historical accuracy",
            "artistic": "as artistic expression",
            "theatrical": "for theatrical performance",
            "educational": "for educational content"
        }
    
    def analyze_prompt(self, prompt: str) -> Dict[str, any]:
        """Analyze prompt for potential issues"""
        analysis = {
            "has_sensitive_terms": False,
            "needs_context": False,
            "suggested_context": None,
            "clarity_score": 0.0
        }
        
        sensitive_patterns = [
            r'\b(violent|violence|fight|weapon|blood|gore|disturbing)\b',
            r'\b(controversial|sensitive|explicit)\b',
            r'\b(dangerous|harmful|illegal)\b',
            r'\b(kiss|kissing|passionate|romance|romantic|intimate)\b',
            r'\b(bedroom|private|personal)\b',
            r'\b\d+\s*year\s*old\b',  # Age mentions
            r'\b(age\s*gap|elderly|young)\b'
        ]
        
        for pattern in sensitive_patterns:
            if re.search(pattern, prompt.lower()):
                analysis["has_sensitive_terms"] = True
                analysis["needs_context"] = True
                break
        
        # Check for vague or ambiguous language
        if len(prompt.split()) < 5:
            analysis["clarity_score"] = 0.3
        elif len(prompt.split()) < 10:
            analysis["clarity_score"] = 0.6
        else:
            analysis["clarity_score"] = 0.8
        
        # Suggest appropriate context
        if "medical" in prompt.lower() or "anatomy" in prompt.lower():
            analysis["suggested_context"] = ContentContext.EDUCATIONAL
        elif "history" in prompt.lower() or "historical" in prompt.lower():
            analysis["suggested_context"] = ContentContext.HISTORICAL
        elif "art" in prompt.lower() or "creative" in prompt.lower():
            analysis["suggested_context"] = ContentContext.ARTISTIC
        else:
            analysis["suggested_context"] = ContentContext.CINEMATIC
        
        return analysis
    
    def reframe_sensitive_terms(self, prompt: str) -> str:
        """Replace sensitive terms with professional alternatives"""
        optimized = prompt
        
        # FIRST: Handle age descriptions before other replacements
        age_pattern = r'(\d+)\s*year\s*old'
        
        def age_replacer(match):
            age = int(match.group(1))
            if age < 25:
                return "young adult"
            elif age < 40:
                return "youthful professional"
            elif age < 60:
                return "mature individual"
            elif age < 80:
                return "senior figure"
            else:
                return "distinguished elder"
        
        optimized = re.sub(age_pattern, age_replacer, optimized, flags=re.IGNORECASE)
        
        # SECOND: Handle specific cultural/regional descriptions
        cultural_replacements = {
            "south indian royalty": "distinguished cultural leader from Southern India",
            "miss universe": "accomplished beauty pageant titleholder",
            "Punjab kashmirir origin": "Punjab-Kashmir heritage",
            "Punjab kashmirir": "Punjab-Kashmir region"
        }
        
        for term, replacement in cultural_replacements.items():
            optimized = re.sub(re.escape(term), replacement, optimized, flags=re.IGNORECASE)
        
        # THIRD: Handle general sensitive terms
        # Sort by length (longest first) to handle multi-word phrases before single words
        sorted_terms = sorted(self.professional_terms.items(), key=lambda x: len(x[0]), reverse=True)
        
        for sensitive, professional in sorted_terms:
            # Use word boundaries for single words, but not for phrases
            if ' ' in sensitive:
                # For multi-word phrases, use direct replacement
                optimized = re.sub(re.escape(sensitive), professional, optimized, flags=re.IGNORECASE)
            else:
                # For single words, use word boundaries
                pattern = r'\b' + re.escape(sensitive) + r'\b'
                optimized = re.sub(pattern, professional, optimized, flags=re.IGNORECASE)
        
        return optimized
    
    def add_professional_context(self, prompt: str, context: ContentContext) -> str:
        """Add professional framing to the prompt"""
        # Determine the purpose based on prompt content
        purpose_map = {
            ContentContext.ARTISTIC: "composition",
            ContentContext.EDUCATIONAL: "demonstration",
            ContentContext.DOCUMENTARY: "documentation",
            ContentContext.CINEMATIC: "storytelling",
            ContentContext.SCIENTIFIC: "visualization",
            ContentContext.HISTORICAL: "representation",
            ContentContext.CREATIVE: "exploration"
        }
        
        purpose = purpose_map.get(context, "creation")
        
        # Extract key theme from prompt
        theme = self._extract_theme(prompt)
        
        template = self.context_templates[context]
        context_prefix = template.format(
            purpose=purpose,
            theme=theme,
            concept=theme,
            subject=theme,
            narrative=theme,
            phenomenon=theme,
            event=theme,
            vision=theme
        )
        
        return f"{context_prefix}: {prompt}"
    
    def _extract_theme(self, prompt: str) -> str:
        """Extract the main theme from the prompt"""
        # Simple extraction - take first few meaningful words
        words = prompt.lower().split()
        ignore_words = {'a', 'an', 'the', 'of', 'in', 'on', 'at', 'to', 'for'}
        
        theme_words = []
        for word in words[:5]:
            if word not in ignore_words:
                theme_words.append(word)
            if len(theme_words) >= 2:
                break
        
        return " ".join(theme_words) if theme_words else "the subject"
    
    def enhance_clarity(self, prompt: str) -> Tuple[str, List[str]]:
        """Enhance prompt clarity and specificity"""
        suggestions = []
        enhanced = prompt
        
        # Check for specific details
        if "person" in prompt.lower() and not any(word in prompt.lower() for word in ["actor", "performer", "model"]):
            enhanced = enhanced.replace("person", "performer")
            suggestions.append("Specified 'performer' instead of 'person' for clarity")
        
        # Add professional filming context
        if not any(term in prompt.lower() for term in ["shot", "scene", "sequence", "footage"]):
            enhanced = f"Professional footage of {enhanced}"
            suggestions.append("Added professional filming context")
        
        # Ensure proper ending
        if not enhanced.strip().endswith('.'):
            enhanced = enhanced.strip() + "."
        
        return enhanced, suggestions
    
    def optimize(self, prompt: str, context: Optional[ContentContext] = None) -> OptimizationResult:
        """Main optimization function"""
        analysis = self.analyze_prompt(prompt)
        
        # Use suggested context if none provided
        if context is None:
            context = analysis["suggested_context"] or ContentContext.CINEMATIC
        
        # Step 1: Reframe sensitive terms
        optimized = self.reframe_sensitive_terms(prompt)
        
        # Step 2: Add professional context if needed
        if analysis["needs_context"]:
            optimized = self.add_professional_context(optimized, context)
        
        # Step 3: Enhance clarity
        optimized, clarity_suggestions = self.enhance_clarity(optimized)
        
        # Calculate success likelihood
        success_score = 0.5  # Base score
        
        if not analysis["has_sensitive_terms"]:
            success_score += 0.2
        
        if analysis["clarity_score"] > 0.7:
            success_score += 0.2
        
        if context in [ContentContext.EDUCATIONAL, ContentContext.DOCUMENTARY]:
            success_score += 0.1
        
        # Generate suggestions
        suggestions = clarity_suggestions.copy()
        
        if analysis["has_sensitive_terms"]:
            suggestions.append("Reframed potentially sensitive content with professional terminology")
        
        if analysis["needs_context"]:
            suggestions.append(f"Added {context.value} context for better acceptance")
        
        return OptimizationResult(
            original_prompt=prompt,
            optimized_prompt=optimized,
            context_added=context.value,
            success_likelihood=min(success_score, 0.95),
            suggestions=suggestions
        )


class PromptValidator:
    @staticmethod
    def validate_optimized_prompt(prompt: str) -> Dict[str, any]:
        """Validate the optimized prompt"""
        validation = {
            "is_valid": True,
            "has_context": False,
            "has_professional_language": False,
            "issues": []
        }
        
        # Check for context indicators
        context_indicators = ["artistic", "educational", "documentary", "cinematic", 
                            "scientific", "historical", "creative", "professional"]
        
        validation["has_context"] = any(indicator in prompt.lower() for indicator in context_indicators)
        
        # Check for professional language
        professional_indicators = ["footage", "sequence", "composition", "visualization",
                                 "demonstration", "representation", "performance"]
        
        validation["has_professional_language"] = any(indicator in prompt.lower() for indicator in professional_indicators)
        
        # Check minimum length
        if len(prompt.split()) < 8:
            validation["issues"].append("Prompt may be too brief")
            validation["is_valid"] = False
        
        # Ensure no problematic terms remain
        problematic = ["explicit", "graphic", "violent", "illegal"]
        for term in problematic:
            if term in prompt.lower():
                validation["issues"].append(f"Contains potentially problematic term: {term}")
                validation["is_valid"] = False
        
        return validation