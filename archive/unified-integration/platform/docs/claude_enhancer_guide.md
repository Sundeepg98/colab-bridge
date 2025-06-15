# Claude Enhancer Guide

## Overview

The Claude Enhancer is a powerful module that leverages Anthropic's Claude API to provide advanced prompt enhancement capabilities. It goes far beyond simple text manipulation by using Claude's deep understanding to analyze, enhance, and optimize prompts for video generation.

## Key Features

### 1. **Deep Prompt Analysis**
- Comprehensive analysis of prompt structure, intent, and potential
- Identifies strengths, weaknesses, and missing elements
- Provides detailed insights into visual elements, mood, and technical aspects

### 2. **Multiple Enhancement Modes**
- **Creative**: Emphasizes imagination and artistic expression
- **Technical**: Focuses on precise technical details and specifications
- **Narrative**: Develops story elements and emotional journeys
- **Cinematic**: Adds professional cinematography and film techniques
- **Artistic**: Enhances artistic style and aesthetic qualities
- **Sensitive**: Handles potentially sensitive content with nuance
- **Comprehensive**: Combines all approaches for maximum enhancement

### 3. **Intelligent Variation Generation**
- Creates multiple creative variations of each prompt
- Each variation takes a different approach (dramatic, artistic, technical, etc.)
- Allows exploration of different creative directions

### 4. **Prompt Scoring and Evaluation**
- Evaluates prompts on 10 dimensions:
  - Clarity
  - Creativity
  - Visual Richness
  - Technical Feasibility
  - Emotional Impact
  - Narrative Coherence
  - Artistic Merit
  - Uniqueness
  - Completeness
  - Overall Quality

### 5. **Narrative and Context Generation**
- Creates rich backstories and world-building
- Develops character motivations and emotional journeys
- Adds symbolic meaning and thematic depth

### 6. **Artistic and Cinematographic Details**
- Generates specific visual style recommendations
- Provides detailed color palette and lighting setups
- Includes camera movement and shot composition details
- References artistic movements and influences

### 7. **Sensitive Content Handling**
- Analyzes content for potential sensitivities
- Provides balanced recommendations
- Suggests appropriate reframings when needed
- Respects artistic expression while noting concerns

### 8. **Iterative Improvement**
- Can improve prompts iteratively to reach quality targets
- Identifies and addresses weakest aspects first
- Continues until desired quality score is achieved

## Installation and Setup

### 1. Install Dependencies
```bash
pip install anthropic>=0.18.0
```

### 2. Set API Key
```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key-here'
```

Or add to your `.env` file:
```
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

## Basic Usage

### Simple Enhancement
```python
from src.claude_enhancer import ClaudeEnhancer, EnhancementMode

# Initialize enhancer
enhancer = ClaudeEnhancer()

# Enhance a prompt
result = enhancer.enhance_prompt_sync(
    "A robot walking through a city",
    mode=EnhancementMode.COMPREHENSIVE
)

print(f"Enhanced: {result.enhanced_prompt}")
print(f"Score: {result.scores['total_score']}")
```

### Async Usage
```python
import asyncio

async def enhance_prompt():
    enhancer = ClaudeEnhancer()
    result = await enhancer.enhance_prompt(
        "Sunset over mountains",
        mode=EnhancementMode.CINEMATIC
    )
    return result

result = asyncio.run(enhance_prompt())
```

### Quick Enhancement
For real-time applications where speed is critical:
```python
enhancer = ClaudeEnhancer()
quick_result = enhancer.get_quick_enhancement("A simple landscape")
```

## Advanced Usage

### Using Different Enhancement Modes

```python
# Cinematic mode for film-like results
cinematic_result = await enhancer.enhance_prompt(
    "A chase scene through narrow alleys",
    mode=EnhancementMode.CINEMATIC
)

# Artistic mode for stylized outputs
artistic_result = await enhancer.enhance_prompt(
    "A portrait of an elderly person",
    mode=EnhancementMode.ARTISTIC
)

# Narrative mode for story-driven content
narrative_result = await enhancer.enhance_prompt(
    "A hero's journey begins",
    mode=EnhancementMode.NARRATIVE
)
```

### Batch Processing
Process multiple prompts efficiently:
```python
prompts = [
    "A futuristic cityscape",
    "An underwater scene",
    "A magical forest"
]

results = await enhancer.batch_enhance(
    prompts,
    mode=EnhancementMode.CREATIVE
)
```

### Iterative Improvement
Improve a prompt until it reaches a quality target:
```python
improved_prompt, scores = await enhancer.evaluate_and_improve(
    "A car driving",  # Simple prompt
    target_score=0.85  # Target quality score
)
```

### Integration with Existing System
```python
from src.claude_integration import ClaudeIntegratedOptimizer

optimizer = ClaudeIntegratedOptimizer()

# Combine with existing optimization
result = await optimizer.optimize_with_claude(
    prompt="A mysterious forest",
    use_existing_optimization=True,
    enhancement_mode=EnhancementMode.COMPREHENSIVE
)

print(f"Final prompt: {result['final_prompt']}")
print(f"Variations: {len(result['variations'])}")
```

## Enhancement Result Structure

The `EnhancementResult` object contains:

```python
result = EnhancementResult(
    original_prompt="...",      # Original input
    enhanced_prompt="...",      # Main enhanced version
    variations=[...],           # List of creative variations
    analysis={...},            # Detailed analysis dictionary
    scores={...},              # Quality scores (0-1)
    narrative_context="...",   # Story and context
    artistic_details="...",    # Artistic specifications
    cinematography="...",      # Camera and shot details
    content_warnings=[...],    # Any content concerns
    themes=[...],              # Identified themes
    mode=EnhancementMode.X     # Mode used
)
```

## Best Practices

### 1. Choose the Right Mode
- Use `COMPREHENSIVE` for general enhancement
- Use `CINEMATIC` for video/film projects
- Use `ARTISTIC` for stylized or creative outputs
- Use `SENSITIVE` when dealing with potentially sensitive topics

### 2. Leverage Variations
- The system generates 5 variations per prompt
- Each variation explores a different creative direction
- Use these to explore possibilities before settling on final version

### 3. Use Scores for Quality Control
- Set minimum score thresholds for production use
- Use iterative improvement for low-scoring prompts
- Pay attention to specific dimension scores to identify areas for improvement

### 4. Combine with Existing Tools
- Use `ClaudeIntegratedOptimizer` to combine with existing optimization
- This provides the best of both systems

### 5. Handle API Limits
- Use batch processing for multiple prompts
- Implement caching for repeated prompts
- Use quick enhancement for real-time needs

## Examples

### Example 1: Complete Enhancement Pipeline
```python
async def full_enhancement_pipeline(prompt):
    enhancer = ClaudeEnhancer()
    
    # 1. Analyze current prompt
    analysis = await enhancer._analyze_prompt(prompt)
    print(f"Weaknesses: {analysis.get('weaknesses', [])}")
    
    # 2. Generate enhanced version
    result = await enhancer.enhance_prompt(
        prompt,
        mode=EnhancementMode.COMPREHENSIVE
    )
    
    # 3. Check if it meets quality standards
    if result.scores['total_score'] < 0.8:
        # 4. Improve iteratively
        improved, scores = await enhancer.evaluate_and_improve(
            result.enhanced_prompt,
            target_score=0.8
        )
        return improved
    
    return result.enhanced_prompt
```

### Example 2: Mode Selection Based on Content
```python
from src.claude_integration import ClaudeIntegratedOptimizer

optimizer = ClaudeIntegratedOptimizer()

# Automatically suggest best mode
prompt = "A dramatic movie scene with explosions"
suggested_mode = optimizer.suggest_mode(prompt)  # Returns CINEMATIC

result = await optimizer.optimize_with_claude(
    prompt,
    enhancement_mode=suggested_mode
)
```

### Example 3: Content-Aware Enhancement
```python
async def content_aware_enhancement(prompt):
    enhancer = ClaudeEnhancer()
    
    # First, analyze for sensitive content
    content_analysis = await enhancer._handle_sensitive_content(prompt)
    
    if content_analysis['warnings']:
        # Use sensitive mode for careful handling
        result = await enhancer.enhance_prompt(
            prompt,
            mode=EnhancementMode.SENSITIVE
        )
    else:
        # Use comprehensive mode
        result = await enhancer.enhance_prompt(
            prompt,
            mode=EnhancementMode.COMPREHENSIVE
        )
    
    return result
```

## Testing

Run the comprehensive test suite:

```bash
python test_claude_enhancer.py
```

This will test:
- All enhancement modes
- Batch processing
- Iterative improvement
- Sensitive content handling
- Integration with existing system

## Performance Considerations

1. **API Calls**: Each enhancement makes multiple API calls for comprehensive analysis
2. **Batch Processing**: Use batch methods to process multiple prompts efficiently
3. **Caching**: Consider implementing caching for repeated prompts
4. **Model Selection**: Different Claude models are used for different tasks:
   - Opus for deep analysis and evaluation
   - Sonnet for creative generation
   - Haiku for quick enhancements

## Error Handling

The module includes comprehensive error handling:

```python
try:
    result = await enhancer.enhance_prompt(prompt)
except ValueError as e:
    # Handle API key issues
    print(f"API key error: {e}")
except Exception as e:
    # Handle other errors
    print(f"Enhancement error: {e}")
```

## Conclusion

The Claude Enhancer provides a powerful, comprehensive solution for prompt enhancement that leverages Claude's advanced language understanding. By combining deep analysis, creative generation, and intelligent evaluation, it can transform simple prompts into rich, detailed descriptions that result in superior video generation outputs.