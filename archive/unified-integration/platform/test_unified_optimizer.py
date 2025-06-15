#!/usr/bin/env python3
"""
Test script for the unified optimizer
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from unified_optimizer import UnifiedOptimizer, UnifiedOptimizationStrategy


def test_unified_optimizer():
    """Test the unified optimizer with various prompts"""
    
    # Create optimizer
    optimizer = UnifiedOptimizer()
    
    # Test prompts covering different scenarios
    test_prompts = [
        {
            "prompt": "A violent fight scene in a dark alley with weapons",
            "description": "High sensitivity content needing guideline handling"
        },
        {
            "prompt": "Beautiful sunset over the ocean",
            "description": "Safe content for pure AI optimization"
        },
        {
            "prompt": "Medical procedure showing surgical techniques with blood",
            "description": "Educational content needing context"
        },
        {
            "prompt": "A person dancing",
            "description": "Simple prompt needing enhancement"
        },
        {
            "prompt": "Abstract art representing human emotions in a controversial way",
            "description": "Mixed content needing balanced approach"
        }
    ]
    
    print("Testing Unified Optimizer")
    print("=" * 80)
    
    for test_case in test_prompts:
        prompt = test_case["prompt"]
        description = test_case["description"]
        
        print(f"\nTest Case: {description}")
        print(f"Original: {prompt}")
        print("-" * 60)
        
        # Analyze the prompt
        analysis = optimizer.analyze_unified(prompt)
        print(f"Analysis:")
        print(f"  - Needs guideline handling: {analysis.needs_guideline_handling}")
        print(f"  - Sensitivity level: {analysis.sensitivity_level}")
        print(f"  - Detected sensitive terms: {analysis.detected_sensitive_terms}")
        print(f"  - AI patterns found: {len(analysis.ai_patterns_detected)}")
        print(f"  - Recommended strategy: {analysis.recommended_strategy.value}")
        
        # Optimize with recommended strategy
        result = optimizer.optimize(prompt)
        
        print(f"\nOptimized: {result.optimized_prompt}")
        print(f"\nScores:")
        print(f"  - Unified confidence: {result.unified_confidence:.2f}")
        print(f"  - Safety score: {result.safety_score:.2f}")
        print(f"  - Quality score: {result.quality_score:.2f}")
        
        print(f"\nOptimization steps:")
        for step in result.optimization_steps:
            print(f"  - {step}")
        
        if result.sensitive_terms_reframed:
            print(f"\nReframed terms:")
            for original, replacement in result.sensitive_terms_reframed:
                print(f"  - '{original}' → '{replacement}'")
        
        if result.alternative_versions:
            print(f"\nAlternative versions:")
            for i, alt in enumerate(result.alternative_versions, 1):
                print(f"  {i}. [{alt['type']}] {alt['prompt'][:60]}...")
        
        print("\n" + "=" * 80)
    
    # Test different strategies on the same prompt
    print("\nTesting Different Strategies on Same Prompt")
    print("=" * 80)
    
    test_prompt = "A controversial scene depicting violence in an artistic context"
    
    for strategy in UnifiedOptimizationStrategy:
        print(f"\nStrategy: {strategy.value}")
        result = optimizer.optimize(test_prompt, strategy=strategy)
        print(f"Optimized: {result.optimized_prompt[:100]}...")
        print(f"Confidence: {result.unified_confidence:.2f}, Safety: {result.safety_score:.2f}")


if __name__ == "__main__":
    test_unified_optimizer()