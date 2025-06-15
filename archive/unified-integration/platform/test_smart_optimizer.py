#!/usr/bin/env python3
"""
Test script for the Smart Optimizer module
Demonstrates the advanced prompt optimization capabilities
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from smart_optimizer import SmartOptimizer, OptimizationProfile, OptimizationMode


def test_smart_optimizer():
    """Test various smart optimization features"""
    print("=== Smart Optimizer Test Suite ===\n")
    
    # Initialize optimizer
    optimizer = SmartOptimizer()
    
    # Test prompts
    test_prompts = [
        {
            "prompt": "A cat sitting on a window",
            "description": "Simple prompt - should enhance with details"
        },
        {
            "prompt": "Beautiful sunset over the ocean with birds flying",
            "description": "Scenic prompt - should add cinematic elements"
        },
        {
            "prompt": "Abstract representation of time and memory",
            "description": "Conceptual prompt - should add artistic depth"
        },
        {
            "prompt": "A person walking through a dark forest at night",
            "description": "Atmospheric prompt - should enhance mood and tension"
        },
        {
            "prompt": "Scientific visualization of DNA replication process",
            "description": "Technical prompt - should add clarity and precision"
        }
    ]
    
    for test_case in test_prompts:
        print(f"\n{'='*60}")
        print(f"TEST: {test_case['description']}")
        print(f"Original: {test_case['prompt']}")
        print("-" * 60)
        
        # Auto-optimization
        result = optimizer.optimize(test_case['prompt'])
        
        print(f"\nOptimized: {result.optimized_prompt}")
        print(f"\nScores:")
        print(f"  - Confidence: {result.confidence_score:.2%}")
        print(f"  - Semantic: {result.semantic_score:.2%}")
        print(f"  - Style: {result.style_score:.2%}")
        
        print(f"\nOptimization Mode: {result.optimization_profile.mode.value}")
        print(f"Transformations Applied: {len(result.transformations_applied)}")
        
        if result.patterns_detected:
            print(f"\nTop Patterns Detected:")
            for pattern in result.patterns_detected[:3]:
                print(f"  - {pattern.pattern_type.value}: '{pattern.match_text}' (confidence: {pattern.confidence:.2f})")
        
        if result.alternative_versions:
            print(f"\nAlternative Versions:")
            for i, alt in enumerate(result.alternative_versions, 1):
                print(f"  {i}. {alt}")
    
    # Test specific optimization modes
    print(f"\n\n{'='*60}")
    print("TESTING SPECIFIC OPTIMIZATION MODES")
    print("="*60)
    
    test_prompt = "A dancer performing on stage"
    
    modes = [
        OptimizationMode.ENHANCE,
        OptimizationMode.TRANSFORM,
        OptimizationMode.STYLIZE,
        OptimizationMode.CONTEXTUALIZE
    ]
    
    for mode in modes:
        print(f"\n\nMode: {mode.value}")
        print("-" * 40)
        
        profile = OptimizationProfile(
            mode=mode,
            target_style="cinematic" if mode == OptimizationMode.STYLIZE else None,
            enhancement_level=0.8
        )
        
        result = optimizer.optimize(test_prompt, profile)
        print(f"Result: {result.optimized_prompt}")
    
    # Test style transfer
    print(f"\n\n{'='*60}")
    print("TESTING STYLE TRANSFER")
    print("="*60)
    
    original = "A cityscape at night with neon lights"
    styles = ["cinematic", "documentary", "artistic", "minimalist", "maximalist"]
    
    for style in styles:
        print(f"\n\nTarget Style: {style}")
        print("-" * 40)
        styled = optimizer.style_engine.transfer_style(original, style)
        print(f"Result: {styled}")
    
    # Test context analysis
    print(f"\n\n{'='*60}")
    print("TESTING CONTEXT ANALYSIS")
    print("="*60)
    
    analyze_prompt = "A warrior battles a dragon in an ancient castle"
    analysis = optimizer.context_engine.analyze_context(analyze_prompt)
    
    print(f"\nPrompt: {analyze_prompt}")
    print(f"Primary Theme: {analysis['primary_theme']}")
    print(f"Missing Contexts: {', '.join(analysis['missing_contexts'])}")
    print(f"Suggestions: {', '.join(analysis['context_suggestions'])}")
    
    # Test semantic enhancement
    print(f"\n\n{'='*60}")
    print("TESTING SEMANTIC ENHANCEMENT")
    print("="*60)
    
    semantic_prompt = "A small bird flies over a big mountain"
    print(f"\nOriginal: {semantic_prompt}")
    
    strategies = ["specificity", "vividness", "depth"]
    for strategy in strategies:
        enhanced = optimizer.semantic_enhancer.enhance_semantically(semantic_prompt, strategy)
        print(f"\n{strategy.capitalize()} Enhancement: {enhanced}")


if __name__ == "__main__":
    test_smart_optimizer()