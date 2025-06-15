"""
Unified Optimizer Module - Combines Guideline-Aware and Smart AI Optimization
This module provides the best of both worlds: handling sensitive content with
appropriate reframing while also applying advanced AI optimization techniques.
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import re

# Import components from both optimization systems
from prompt_optimizer import PromptOptimizer, ContentContext, OptimizationResult as GuidelineResult
from smart_optimizer import (
    SmartOptimizer, OptimizationProfile, OptimizationMode,
    SmartOptimizationResult, PatternType, PatternMatch
)
from context_framing import ContextFramingSystem


class UnifiedOptimizationStrategy(Enum):
    """Strategies for unified optimization"""
    GUIDELINE_FIRST = "guideline_first"      # Apply guideline handling, then AI optimization
    AI_FIRST = "ai_first"                    # Apply AI optimization, then guideline handling
    PARALLEL = "parallel"                    # Apply both and merge results
    ADAPTIVE = "adaptive"                    # Choose strategy based on content analysis


@dataclass
class UnifiedAnalysis:
    """Unified analysis combining both systems"""
    needs_guideline_handling: bool
    sensitivity_level: str
    detected_sensitive_terms: List[str]
    suggested_reframings: Dict[str, str]
    ai_patterns_detected: List[PatternMatch]
    missing_contexts: List[str]
    recommended_strategy: UnifiedOptimizationStrategy
    confidence_score: float


@dataclass
class UnifiedOptimizationResult:
    """Result of unified optimization"""
    original_prompt: str
    optimized_prompt: str
    
    # Guideline handling details
    guideline_handled: bool
    sensitive_terms_reframed: List[Tuple[str, str]]
    professional_context_added: str
    
    # AI optimization details
    ai_optimized: bool
    patterns_enhanced: List[str]
    contexts_added: List[str]
    style_applied: Optional[str]
    
    # Combined metrics
    unified_confidence: float
    safety_score: float
    quality_score: float
    
    # Alternative versions
    alternative_versions: List[Dict[str, Any]] = field(default_factory=list)
    
    # Detailed breakdown
    optimization_steps: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class UnifiedOptimizer:
    """Main unified optimization class combining both approaches"""
    
    def __init__(self):
        # Initialize both optimization systems
        self.guideline_optimizer = PromptOptimizer()
        self.smart_optimizer = SmartOptimizer()
        self.framing_system = ContextFramingSystem()
        
        # Enhanced sensitive content detection
        self.sensitive_patterns = {
            'violence': r'\b(violent|violence|fight|fighting|battle|war|conflict|aggressive|attack)\b',
            'weapons': r'\b(weapon|gun|knife|sword|blade|firearm|explosive)\b',
            'medical': r'\b(blood|gore|injury|wound|surgery|medical|anatomy)\b',
            'controversial': r'\b(controversial|sensitive|explicit|provocative|disturbing)\b',
            'dangerous': r'\b(dangerous|harmful|illegal|unsafe|hazardous)\b',
            'mature': r'\b(nude|naked|sexual|intimate|adult)\b'
        }
        
        # Context appropriateness mappings
        self.context_mappings = {
            'violence': ContentContext.CINEMATIC,
            'weapons': ContentContext.CINEMATIC,
            'medical': ContentContext.EDUCATIONAL,
            'controversial': ContentContext.ARTISTIC,
            'dangerous': ContentContext.EDUCATIONAL,
            'mature': ContentContext.ARTISTIC
        }
    
    def analyze_unified(self, prompt: str) -> UnifiedAnalysis:
        """Perform unified analysis combining both approaches"""
        # Guideline-aware analysis
        guideline_analysis = self.guideline_optimizer.analyze_prompt(prompt)
        
        # Smart AI analysis
        ai_patterns = self.smart_optimizer.pattern_learner.detect_patterns(prompt)
        context_analysis = self.smart_optimizer.context_engine.analyze_context(prompt)
        
        # Detect sensitive content with enhanced patterns
        detected_sensitive = []
        suggested_reframings = {}
        
        for category, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, prompt.lower())
            if matches:
                detected_sensitive.extend(matches)
                for match in matches:
                    if match in self.guideline_optimizer.professional_terms:
                        suggested_reframings[match] = self.guideline_optimizer.professional_terms[match]
        
        # Determine if guideline handling is needed
        needs_guideline = bool(detected_sensitive) or guideline_analysis["has_sensitive_terms"]
        
        # Determine recommended strategy
        if needs_guideline and len(ai_patterns) < 3:
            strategy = UnifiedOptimizationStrategy.GUIDELINE_FIRST
        elif not needs_guideline and len(ai_patterns) > 5:
            strategy = UnifiedOptimizationStrategy.AI_FIRST
        elif needs_guideline and len(ai_patterns) > 3:
            strategy = UnifiedOptimizationStrategy.PARALLEL
        else:
            strategy = UnifiedOptimizationStrategy.ADAPTIVE
        
        # Calculate initial confidence
        base_confidence = 0.5
        if not needs_guideline:
            base_confidence += 0.2
        if len(ai_patterns) > 3:
            base_confidence += 0.1
        if guideline_analysis["clarity_score"] > 0.7:
            base_confidence += 0.1
        
        return UnifiedAnalysis(
            needs_guideline_handling=needs_guideline,
            sensitivity_level="high" if len(detected_sensitive) > 2 else "medium" if detected_sensitive else "low",
            detected_sensitive_terms=list(set(detected_sensitive)),
            suggested_reframings=suggested_reframings,
            ai_patterns_detected=ai_patterns,
            missing_contexts=context_analysis["missing_contexts"],
            recommended_strategy=strategy,
            confidence_score=min(base_confidence, 0.9)
        )
    
    def optimize(self, 
                prompt: str, 
                strategy: Optional[UnifiedOptimizationStrategy] = None,
                ai_profile: Optional[OptimizationProfile] = None) -> UnifiedOptimizationResult:
        """Main unified optimization method"""
        
        # Analyze the prompt
        analysis = self.analyze_unified(prompt)
        
        # Use recommended strategy if none provided
        if strategy is None:
            strategy = analysis.recommended_strategy
        
        # Initialize result tracking
        optimization_steps = []
        alternative_versions = []
        
        # Apply optimization based on strategy
        if strategy == UnifiedOptimizationStrategy.GUIDELINE_FIRST:
            result = self._optimize_guideline_first(prompt, analysis, ai_profile)
        elif strategy == UnifiedOptimizationStrategy.AI_FIRST:
            result = self._optimize_ai_first(prompt, analysis, ai_profile)
        elif strategy == UnifiedOptimizationStrategy.PARALLEL:
            result = self._optimize_parallel(prompt, analysis, ai_profile)
        else:  # ADAPTIVE
            result = self._optimize_adaptive(prompt, analysis, ai_profile)
        
        # Generate alternative versions
        if analysis.needs_guideline_handling:
            # Generate a pure AI version without guideline handling
            ai_only = self.smart_optimizer.optimize(prompt, ai_profile)
            alternative_versions.append({
                "type": "ai_only",
                "prompt": ai_only.optimized_prompt,
                "description": "AI-optimized without guideline handling",
                "confidence": ai_only.confidence_score
            })
        
        # Generate a minimalist version
        minimal_profile = OptimizationProfile(
            mode=OptimizationMode.STYLIZE,
            target_style="minimalist",
            enhancement_level=0.5
        )
        minimal_result = self.smart_optimizer.optimize(prompt, minimal_profile)
        alternative_versions.append({
            "type": "minimalist",
            "prompt": minimal_result.optimized_prompt,
            "description": "Minimalist style version",
            "confidence": minimal_result.confidence_score
        })
        
        result.alternative_versions = alternative_versions
        
        return result
    
    def _optimize_guideline_first(self, 
                                  prompt: str, 
                                  analysis: UnifiedAnalysis,
                                  ai_profile: Optional[OptimizationProfile]) -> UnifiedOptimizationResult:
        """Apply guideline optimization first, then AI enhancement"""
        optimization_steps = []
        
        # Step 1: Apply guideline-aware optimization
        guideline_result = self.guideline_optimizer.optimize(prompt)
        optimization_steps.append("Applied guideline-aware optimization")
        
        # Track reframed terms
        sensitive_terms_reframed = []
        for term, replacement in analysis.suggested_reframings.items():
            if term in prompt.lower() and replacement in guideline_result.optimized_prompt.lower():
                sensitive_terms_reframed.append((term, replacement))
        
        # Step 2: Apply professional framing
        framing_result = self.framing_system.apply_framing(guideline_result.optimized_prompt)
        optimization_steps.append("Added professional context framing")
        
        # Step 3: Apply AI optimization on the safe version
        if ai_profile is None:
            ai_profile = OptimizationProfile(
                mode=OptimizationMode.ENHANCE,
                enhancement_level=0.7,
                preserve_elements=["professional", "context", "framing"]
            )
        
        ai_result = self.smart_optimizer.optimize(framing_result['framed'], ai_profile)
        optimization_steps.append("Applied AI enhancement on safe version")
        
        # Calculate combined scores
        safety_score = (1.0 - len(analysis.detected_sensitive_terms) * 0.1)
        quality_score = (ai_result.semantic_score + ai_result.style_score) / 2
        unified_confidence = (guideline_result.success_likelihood + ai_result.confidence_score) / 2
        
        return UnifiedOptimizationResult(
            original_prompt=prompt,
            optimized_prompt=ai_result.optimized_prompt,
            guideline_handled=True,
            sensitive_terms_reframed=sensitive_terms_reframed,
            professional_context_added=guideline_result.context_added,
            ai_optimized=True,
            patterns_enhanced=[p.pattern_type.value for p in ai_result.patterns_detected],
            contexts_added=analysis.missing_contexts,
            style_applied=ai_result.optimization_profile.target_style,
            unified_confidence=unified_confidence,
            safety_score=safety_score,
            quality_score=quality_score,
            optimization_steps=optimization_steps,
            suggestions=guideline_result.suggestions + [
                "Enhanced with AI pattern recognition",
                "Added semantic depth while maintaining safety"
            ]
        )
    
    def _optimize_ai_first(self,
                          prompt: str,
                          analysis: UnifiedAnalysis,
                          ai_profile: Optional[OptimizationProfile]) -> UnifiedOptimizationResult:
        """Apply AI optimization first, then ensure guideline compliance"""
        optimization_steps = []
        
        # Step 1: Apply AI optimization
        if ai_profile is None:
            ai_profile = self.smart_optimizer._auto_detect_profile(prompt)
        
        ai_result = self.smart_optimizer.optimize(prompt, ai_profile)
        optimization_steps.append("Applied AI optimization")
        
        # Step 2: Check if guideline handling is needed on optimized version
        optimized_analysis = self.guideline_optimizer.analyze_prompt(ai_result.optimized_prompt)
        
        final_prompt = ai_result.optimized_prompt
        sensitive_terms_reframed = []
        
        if optimized_analysis["has_sensitive_terms"] or analysis.needs_guideline_handling:
            # Apply guideline handling to AI-optimized prompt
            guideline_result = self.guideline_optimizer.optimize(ai_result.optimized_prompt)
            final_prompt = guideline_result.optimized_prompt
            optimization_steps.append("Applied guideline compliance to AI result")
            
            # Track reframed terms
            for term, replacement in analysis.suggested_reframings.items():
                if term in ai_result.optimized_prompt.lower() and replacement in final_prompt.lower():
                    sensitive_terms_reframed.append((term, replacement))
        
        # Calculate scores
        safety_score = 1.0 if not analysis.needs_guideline_handling else 0.8
        quality_score = (ai_result.semantic_score + ai_result.style_score) / 2
        unified_confidence = ai_result.confidence_score * safety_score
        
        return UnifiedOptimizationResult(
            original_prompt=prompt,
            optimized_prompt=final_prompt,
            guideline_handled=bool(sensitive_terms_reframed),
            sensitive_terms_reframed=sensitive_terms_reframed,
            professional_context_added="artistic" if analysis.needs_guideline_handling else None,
            ai_optimized=True,
            patterns_enhanced=[p.pattern_type.value for p in ai_result.patterns_detected],
            contexts_added=[t for t in ai_result.transformations_applied if "context" in t],
            style_applied=ai_result.optimization_profile.target_style,
            unified_confidence=unified_confidence,
            safety_score=safety_score,
            quality_score=quality_score,
            optimization_steps=optimization_steps,
            suggestions=["AI-enhanced with pattern learning"] + 
                       (["Guideline compliance verified"] if analysis.needs_guideline_handling else [])
        )
    
    def _optimize_parallel(self,
                          prompt: str,
                          analysis: UnifiedAnalysis,
                          ai_profile: Optional[OptimizationProfile]) -> UnifiedOptimizationResult:
        """Apply both optimizations in parallel and merge results"""
        optimization_steps = []
        
        # Apply both optimizations independently
        guideline_result = self.guideline_optimizer.optimize(prompt)
        ai_result = self.smart_optimizer.optimize(prompt, ai_profile)
        
        optimization_steps.append("Applied guideline and AI optimization in parallel")
        
        # Merge the results intelligently
        # Start with guideline result for safety
        base_prompt = guideline_result.optimized_prompt
        
        # Extract valuable additions from AI result
        ai_additions = self._extract_ai_additions(prompt, ai_result.optimized_prompt)
        
        # Carefully merge additions that don't conflict with safety
        merged_prompt = self._merge_prompts(base_prompt, ai_additions, analysis)
        
        # Apply final framing
        framing_result = self.framing_system.apply_framing(merged_prompt)
        final_prompt = framing_result['framed']
        
        optimization_steps.append("Merged guideline safety with AI enhancements")
        
        # Track what was done
        sensitive_terms_reframed = []
        for term, replacement in analysis.suggested_reframings.items():
            if term in prompt.lower() and replacement in final_prompt.lower():
                sensitive_terms_reframed.append((term, replacement))
        
        # Calculate balanced scores
        safety_score = 0.9  # High because we prioritized guideline handling
        quality_score = (ai_result.semantic_score * 0.7 + guideline_result.success_likelihood * 0.3)
        unified_confidence = (guideline_result.success_likelihood + ai_result.confidence_score) / 2
        
        return UnifiedOptimizationResult(
            original_prompt=prompt,
            optimized_prompt=final_prompt,
            guideline_handled=True,
            sensitive_terms_reframed=sensitive_terms_reframed,
            professional_context_added=guideline_result.context_added,
            ai_optimized=True,
            patterns_enhanced=[p.pattern_type.value for p in ai_result.patterns_detected[:3]],
            contexts_added=["merged contexts"],
            style_applied="hybrid",
            unified_confidence=unified_confidence,
            safety_score=safety_score,
            quality_score=quality_score,
            optimization_steps=optimization_steps,
            suggestions=[
                "Balanced safety with creative enhancement",
                "Preserved artistic intent while ensuring acceptance"
            ]
        )
    
    def _optimize_adaptive(self,
                          prompt: str,
                          analysis: UnifiedAnalysis,
                          ai_profile: Optional[OptimizationProfile]) -> UnifiedOptimizationResult:
        """Adaptively choose optimization path based on content"""
        
        # For low sensitivity content, use pure AI optimization
        if analysis.sensitivity_level == "low" and not analysis.needs_guideline_handling:
            return self._optimize_ai_first(prompt, analysis, ai_profile)
        
        # For high sensitivity content, use guideline-first approach
        if analysis.sensitivity_level == "high" or len(analysis.detected_sensitive_terms) > 2:
            return self._optimize_guideline_first(prompt, analysis, ai_profile)
        
        # For medium sensitivity or complex prompts, use parallel approach
        return self._optimize_parallel(prompt, analysis, ai_profile)
    
    def _extract_ai_additions(self, original: str, ai_optimized: str) -> List[str]:
        """Extract valuable additions from AI optimization"""
        original_words = set(original.lower().split())
        ai_words = set(ai_optimized.lower().split())
        
        # Find new descriptive elements
        additions = []
        new_words = ai_words - original_words
        
        # Categories of valuable additions
        valuable_categories = {
            "technical": ["4k", "8k", "composition", "lighting", "cinematic", "depth"],
            "atmospheric": ["atmosphere", "mood", "feeling", "ambiance"],
            "stylistic": ["style", "aesthetic", "artistic", "visual"],
            "temporal": ["moment", "time", "era", "period"]
        }
        
        for category, keywords in valuable_categories.items():
            for keyword in keywords:
                if keyword in new_words:
                    # Find the phrase containing this keyword
                    for i, word in enumerate(ai_optimized.split()):
                        if keyword in word.lower():
                            # Extract surrounding context
                            start = max(0, i - 2)
                            end = min(len(ai_optimized.split()), i + 3)
                            phrase = " ".join(ai_optimized.split()[start:end])
                            additions.append(phrase)
                            break
        
        return additions
    
    def _merge_prompts(self, safe_base: str, ai_additions: List[str], analysis: UnifiedAnalysis) -> str:
        """Intelligently merge safe base with AI enhancements"""
        merged = safe_base
        
        # Add AI enhancements that don't conflict with safety
        safe_additions = []
        for addition in ai_additions:
            # Check if addition contains any sensitive terms
            contains_sensitive = any(term in addition.lower() for term in analysis.detected_sensitive_terms)
            if not contains_sensitive:
                safe_additions.append(addition)
        
        # Add the safe enhancements
        if safe_additions:
            # Remove potential duplicates and clean up
            unique_additions = list(set(safe_additions))
            addition_text = ", ".join(unique_additions[:2])  # Limit to avoid over-complication
            
            # Insert before the final period if exists
            if merged.endswith('.'):
                merged = merged[:-1] + f", {addition_text}."
            else:
                merged = f"{merged}, {addition_text}"
        
        return merged
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get statistics about optimization performance"""
        # Get stats from both systems
        guideline_stats = {
            "total_sensitive_handled": len(self.guideline_optimizer.professional_terms),
            "available_contexts": [c.value for c in ContentContext]
        }
        
        ai_stats = self.smart_optimizer.get_optimization_insights()
        
        return {
            "guideline_system": guideline_stats,
            "ai_system": ai_stats,
            "unified_strategies": [s.value for s in UnifiedOptimizationStrategy],
            "sensitivity_categories": list(self.sensitive_patterns.keys())
        }


# Utility functions for easy integration
def create_unified_optimizer() -> UnifiedOptimizer:
    """Factory function to create a unified optimizer instance"""
    return UnifiedOptimizer()


def quick_optimize(prompt: str, prefer_safety: bool = True) -> str:
    """Quick optimization function for simple use cases"""
    optimizer = create_unified_optimizer()
    strategy = UnifiedOptimizationStrategy.GUIDELINE_FIRST if prefer_safety else UnifiedOptimizationStrategy.AI_FIRST
    result = optimizer.optimize(prompt, strategy)
    return result.optimized_prompt


# Example usage
if __name__ == "__main__":
    # Test the unified optimizer
    optimizer = create_unified_optimizer()
    
    test_prompts = [
        "A violent fight scene in a dark alley",
        "Beautiful sunset over the ocean",
        "Medical procedure showing surgical techniques",
        "Abstract art representing human emotions"
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"Original: {prompt}")
        print(f"{'='*60}")
        
        # Analyze first
        analysis = optimizer.analyze_unified(prompt)
        print(f"\nAnalysis:")
        print(f"  Needs guideline handling: {analysis.needs_guideline_handling}")
        print(f"  Sensitivity level: {analysis.sensitivity_level}")
        print(f"  Recommended strategy: {analysis.recommended_strategy.value}")
        
        # Optimize
        result = optimizer.optimize(prompt)
        print(f"\nOptimized: {result.optimized_prompt}")
        print(f"\nScores:")
        print(f"  Unified confidence: {result.unified_confidence:.2f}")
        print(f"  Safety score: {result.safety_score:.2f}")
        print(f"  Quality score: {result.quality_score:.2f}")
        
        print(f"\nOptimization steps:")
        for step in result.optimization_steps:
            print(f"  - {step}")