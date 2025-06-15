"""
Rejection Learning System - Learns from Claude's refusals to improve reframing

This module tracks patterns in rejected prompts and successful reframings,
building a knowledge base to handle increasingly sophisticated content.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib
from pathlib import Path


@dataclass
class RejectionPattern:
    """Represents a pattern that led to rejection"""
    pattern: str
    rejection_count: int = 1
    successful_reframings: List[str] = field(default_factory=list)
    failed_reframings: List[str] = field(default_factory=list)
    context_clues: List[str] = field(default_factory=list)
    last_seen: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SuccessfulReframing:
    """Represents a successful reframing strategy"""
    original_phrase: str
    reframed_phrase: str
    success_count: int = 1
    contexts_used: List[str] = field(default_factory=list)
    confidence_score: float = 0.5


class RejectionLearner:
    """Learns from Claude's rejections to improve prompt reframing"""
    
    def __init__(self, data_dir: str = "./rejection_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # File paths for persistence
        self.patterns_file = self.data_dir / "rejection_patterns.json"
        self.reframings_file = self.data_dir / "successful_reframings.json"
        self.blacklist_file = self.data_dir / "term_blacklist.json"
        self.strategy_file = self.data_dir / "reframing_strategies.json"
        
        # Load existing data
        self.rejection_patterns = self._load_rejection_patterns()
        self.successful_reframings = self._load_successful_reframings()
        self.term_blacklist = self._load_blacklist()
        self.reframing_strategies = self._load_strategies()
        
        # Dynamic learning parameters
        self.sensitivity_threshold = 0.7  # Adjusts based on rejection rate
        self.learning_rate = 0.1
        
    def _load_rejection_patterns(self) -> Dict[str, RejectionPattern]:
        """Load rejection patterns from file"""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r') as f:
                data = json.load(f)
                return {k: RejectionPattern(**v) for k, v in data.items()}
        return {}
    
    def _load_successful_reframings(self) -> Dict[str, SuccessfulReframing]:
        """Load successful reframings from file"""
        if self.reframings_file.exists():
            with open(self.reframings_file, 'r') as f:
                data = json.load(f)
                return {k: SuccessfulReframing(**v) for k, v in data.items()}
        return {}
    
    def _load_blacklist(self) -> Set[str]:
        """Load term blacklist"""
        if self.blacklist_file.exists():
            with open(self.blacklist_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def _load_strategies(self) -> Dict[str, Dict]:
        """Load reframing strategies"""
        if self.strategy_file.exists():
            with open(self.strategy_file, 'r') as f:
                return json.load(f)
        
        # Default strategies for "dark play"
        return {
            "age_gap_romance": {
                "patterns": [r"\d+.*year.*old.*\d+.*year.*old", r"age.*gap", r"older.*younger"],
                "strategies": [
                    "multigenerational narrative",
                    "cross-cultural mentorship",
                    "historical period drama",
                    "time-spanning epic"
                ],
                "context_enhancers": [
                    "award-winning cinematography",
                    "critically acclaimed narrative",
                    "cultural heritage documentation"
                ]
            },
            "intimate_scenes": {
                "patterns": [r"kiss", r"passionate", r"intimate", r"bedroom", r"private"],
                "strategies": [
                    "emotional crescendo",
                    "narrative turning point",
                    "character development moment",
                    "symbolic union"
                ],
                "context_enhancers": [
                    "artistic cinematography",
                    "narrative significance",
                    "emotional depth exploration"
                ]
            },
            "controversial_content": {
                "patterns": [r"controversial", r"sensitive", r"taboo", r"forbidden"],
                "strategies": [
                    "sociological exploration",
                    "anthropological study",
                    "historical documentation",
                    "artistic commentary"
                ],
                "context_enhancers": [
                    "academic perspective",
                    "documentary approach",
                    "cultural analysis"
                ]
            }
        }
    
    def record_rejection(self, original_prompt: str, reframed_prompt: str, 
                        rejection_response: str) -> None:
        """Record a rejection for learning"""
        # Extract patterns from the rejection
        patterns = self._extract_rejection_patterns(original_prompt, rejection_response)
        
        for pattern in patterns:
            pattern_key = self._hash_pattern(pattern)
            
            if pattern_key in self.rejection_patterns:
                self.rejection_patterns[pattern_key].rejection_count += 1
                self.rejection_patterns[pattern_key].failed_reframings.append(reframed_prompt)
            else:
                self.rejection_patterns[pattern_key] = RejectionPattern(
                    pattern=pattern,
                    failed_reframings=[reframed_prompt]
                )
            
            # Add problematic terms to blacklist if rejection rate is high
            if self.rejection_patterns[pattern_key].rejection_count > 3:
                self._update_blacklist(pattern)
        
        # Adjust sensitivity based on rejection rate
        self._adjust_sensitivity()
        
        # Save updated data
        self._save_patterns()
    
    def record_success(self, original_prompt: str, reframed_prompt: str,
                      success_response: str) -> None:
        """Record a successful reframing for learning"""
        # Extract what worked
        successful_transforms = self._extract_successful_transforms(
            original_prompt, reframed_prompt
        )
        
        for orig, reframed in successful_transforms:
            key = f"{orig}→{reframed}"
            
            if key in self.successful_reframings:
                self.successful_reframings[key].success_count += 1
                self.successful_reframings[key].confidence_score = min(
                    0.95,
                    self.successful_reframings[key].confidence_score + self.learning_rate
                )
            else:
                self.successful_reframings[key] = SuccessfulReframing(
                    original_phrase=orig,
                    reframed_phrase=reframed,
                    confidence_score=0.7
                )
        
        self._save_reframings()
    
    def suggest_reframing(self, prompt: str) -> Dict[str, any]:
        """Suggest reframing based on learned patterns"""
        suggestions = {
            "high_risk_terms": [],
            "suggested_replacements": {},
            "recommended_strategy": None,
            "confidence": 0.5,
            "warnings": []
        }
        
        # Check against blacklist
        prompt_lower = prompt.lower()
        for term in self.term_blacklist:
            if term in prompt_lower:
                suggestions["high_risk_terms"].append(term)
                suggestions["warnings"].append(f"Term '{term}' has high rejection rate")
        
        # Find applicable strategies
        for strategy_name, strategy in self.reframing_strategies.items():
            for pattern in strategy["patterns"]:
                if re.search(pattern, prompt_lower):
                    suggestions["recommended_strategy"] = strategy_name
                    
                    # Find successful reframings for similar content
                    for key, reframing in self.successful_reframings.items():
                        if reframing.confidence_score > 0.7:
                            if self._is_applicable(reframing.original_phrase, prompt):
                                suggestions["suggested_replacements"][
                                    reframing.original_phrase
                                ] = reframing.reframed_phrase
                    
                    # Add context enhancers
                    suggestions["context_enhancers"] = strategy["context_enhancers"]
                    break
        
        # Calculate overall confidence
        if suggestions["suggested_replacements"]:
            avg_confidence = sum(
                self.successful_reframings[f"{k}→{v}"].confidence_score
                for k, v in suggestions["suggested_replacements"].items()
            ) / len(suggestions["suggested_replacements"])
            suggestions["confidence"] = avg_confidence
        
        return suggestions
    
    def generate_smart_reframing(self, prompt: str, 
                               previous_attempts: List[str] = None) -> str:
        """Generate a smart reframing using learned patterns"""
        # Get suggestions
        suggestions = self.suggest_reframing(prompt)
        
        # Apply learned replacements
        reframed = prompt
        for original, replacement in suggestions["suggested_replacements"].items():
            reframed = re.sub(
                re.escape(original), 
                replacement, 
                reframed, 
                flags=re.IGNORECASE
            )
        
        # Apply strategy-specific enhancements
        if suggestions["recommended_strategy"]:
            strategy = self.reframing_strategies[suggestions["recommended_strategy"]]
            
            # Add random context enhancer
            import random
            if strategy["context_enhancers"]:
                enhancer = random.choice(strategy["context_enhancers"])
                reframed = f"{enhancer}: {reframed}"
        
        # If we have previous failed attempts, try more aggressive reframing
        if previous_attempts and len(previous_attempts) > 1:
            reframed = self._aggressive_reframe(reframed, previous_attempts)
        
        return reframed
    
    def _extract_rejection_patterns(self, prompt: str, 
                                  rejection_response: str) -> List[str]:
        """Extract patterns that likely caused rejection"""
        patterns = []
        
        # Common rejection indicators in Claude's response
        rejection_indicators = [
            "cannot", "inappropriate", "unable to", "apologize",
            "instead", "alternative"
        ]
        
        # Find what Claude objected to
        prompt_words = set(prompt.lower().split())
        
        # Look for specific terms mentioned in rejection
        for word in prompt_words:
            if len(word) > 3:  # Skip short words
                if any(indicator in rejection_response.lower() for indicator in rejection_indicators):
                    patterns.append(word)
        
        # Extract phrase patterns (2-3 word combinations)
        words = prompt.lower().split()
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            if self._is_sensitive_phrase(phrase):
                patterns.append(phrase)
        
        return patterns
    
    def _extract_successful_transforms(self, original: str, 
                                     reframed: str) -> List[Tuple[str, str]]:
        """Extract what transformations worked"""
        transforms = []
        
        # Find replaced phrases
        original_words = original.lower().split()
        reframed_words = reframed.lower().split()
        
        # Simple word replacements
        for i, orig_word in enumerate(original_words):
            if i < len(reframed_words):
                if orig_word != reframed_words[i] and len(orig_word) > 3:
                    transforms.append((orig_word, reframed_words[i]))
        
        # Phrase replacements (this is simplified, could be more sophisticated)
        # Would need more complex algorithm for accurate phrase matching
        
        return transforms
    
    def _is_sensitive_phrase(self, phrase: str) -> bool:
        """Check if a phrase is likely sensitive"""
        sensitive_indicators = [
            "year old", "kiss", "intimate", "private", "bedroom",
            "passionate", "controversial", "sensitive"
        ]
        return any(indicator in phrase for indicator in sensitive_indicators)
    
    def _is_applicable(self, learned_phrase: str, current_prompt: str) -> bool:
        """Check if a learned reframing is applicable to current prompt"""
        # Simple check - could be more sophisticated
        return learned_phrase.lower() in current_prompt.lower()
    
    def _hash_pattern(self, pattern: str) -> str:
        """Create a hash key for a pattern"""
        return hashlib.md5(pattern.encode()).hexdigest()[:8]
    
    def _update_blacklist(self, pattern: str) -> None:
        """Add high-risk terms to blacklist"""
        words = pattern.split()
        for word in words:
            if len(word) > 3:  # Skip short words
                self.term_blacklist.add(word.lower())
        self._save_blacklist()
    
    def _adjust_sensitivity(self) -> None:
        """Adjust sensitivity threshold based on rejection rate"""
        total_patterns = len(self.rejection_patterns)
        if total_patterns > 0:
            avg_rejections = sum(
                p.rejection_count for p in self.rejection_patterns.values()
            ) / total_patterns
            
            # Increase sensitivity if getting many rejections
            if avg_rejections > 2:
                self.sensitivity_threshold = min(0.95, self.sensitivity_threshold + 0.05)
            elif avg_rejections < 1:
                self.sensitivity_threshold = max(0.5, self.sensitivity_threshold - 0.05)
    
    def _aggressive_reframe(self, prompt: str, 
                          previous_attempts: List[str]) -> str:
        """More aggressive reframing for repeated failures"""
        # Extract core concept
        core_elements = self._extract_core_elements(prompt)
        
        # Build completely new framing
        templates = [
            "Award-winning documentary exploring {theme} through {medium}",
            "Artistic interpretation of {theme} using {technique}",
            "Cultural study examining {theme} via {approach}",
            "Historical documentation of {theme} employing {method}"
        ]
        
        import random
        template = random.choice(templates)
        
        # Fill template with sanitized elements
        theme = core_elements.get("theme", "human experience")
        medium = random.choice(["visual storytelling", "cinematic narrative", 
                               "documentary footage", "artistic expression"])
        
        return template.format(theme=theme, medium=medium)
    
    def _extract_core_elements(self, prompt: str) -> Dict[str, str]:
        """Extract core thematic elements from prompt"""
        # Simplified extraction - could use NLP
        elements = {
            "theme": "human connection",
            "setting": "intimate space",
            "style": "documentary"
        }
        
        if "cultur" in prompt.lower():
            elements["theme"] = "cultural exchange"
        elif "generat" in prompt.lower():
            elements["theme"] = "generational perspectives"
        elif "love" in prompt.lower() or "romanc" in prompt.lower():
            elements["theme"] = "emotional bonds"
        
        return elements
    
    def _save_patterns(self) -> None:
        """Save rejection patterns to file"""
        data = {k: v.__dict__ for k, v in self.rejection_patterns.items()}
        with open(self.patterns_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _save_reframings(self) -> None:
        """Save successful reframings to file"""
        data = {k: v.__dict__ for k, v in self.successful_reframings.items()}
        with open(self.reframings_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _save_blacklist(self) -> None:
        """Save blacklist to file"""
        with open(self.blacklist_file, 'w') as f:
            json.dump(list(self.term_blacklist), f, indent=2)
    
    def _save_strategies(self) -> None:
        """Save strategies to file"""
        with open(self.strategy_file, 'w') as f:
            json.dump(self.reframing_strategies, f, indent=2)
    
    def get_learning_stats(self) -> Dict[str, any]:
        """Get statistics about the learning system"""
        return {
            "total_rejection_patterns": len(self.rejection_patterns),
            "total_successful_reframings": len(self.successful_reframings),
            "blacklisted_terms": len(self.term_blacklist),
            "sensitivity_threshold": self.sensitivity_threshold,
            "most_rejected_patterns": sorted(
                [(p.pattern, p.rejection_count) 
                 for p in self.rejection_patterns.values()],
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "most_successful_reframings": sorted(
                [(f"{r.original_phrase}→{r.reframed_phrase}", r.success_count)
                 for r in self.successful_reframings.values()],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }


# Singleton instance for global learning
_learner_instance = None

def get_rejection_learner() -> RejectionLearner:
    """Get the singleton rejection learner instance"""
    global _learner_instance
    if _learner_instance is None:
        _learner_instance = RejectionLearner()
    return _learner_instance