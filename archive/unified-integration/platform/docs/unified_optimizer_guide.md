# Unified Optimizer Guide

## Overview

The Unified Optimizer combines the best of both worlds:
1. **Guideline-Aware Optimization**: Handles sensitive content with appropriate reframing and professional context
2. **Smart AI Optimization**: Applies advanced pattern learning, contextual understanding, and multi-stage enhancement

This unified approach ensures your prompts are both safe for acceptance and creatively enhanced for maximum quality.

## How It Works

### 1. Content Analysis

The unified optimizer first analyzes your prompt to determine:
- Whether it contains sensitive content requiring guideline handling
- What AI patterns and opportunities for enhancement exist
- The best optimization strategy to apply

### 2. Strategy Selection

Based on the analysis, one of four strategies is applied:

#### **Guideline-First Strategy**
- Used when sensitive content is detected
- First applies professional reframing to ensure safety
- Then enhances with AI optimization while preserving safety

#### **AI-First Strategy**
- Used for safe content with rich optimization potential
- Applies advanced AI enhancement first
- Then verifies guideline compliance

#### **Parallel Strategy**
- Used for complex prompts with both sensitive content and enhancement opportunities
- Runs both optimizations independently
- Intelligently merges results for best of both worlds

#### **Adaptive Strategy**
- Automatically selects the best approach based on content
- Default strategy for auto-optimization

### 3. Optimization Process

The unified optimizer:
1. **Reframes sensitive terms** (e.g., "violent" → "choreographed action sequence")
2. **Adds professional context** (e.g., "For educational purposes", "Professional film production")
3. **Enhances with AI patterns** (adds cinematic details, lighting, composition)
4. **Enriches context** (temporal, spatial, emotional layers)
5. **Polishes for quality** (ensures coherence and technical excellence)

## API Endpoints

### 1. Auto-Optimize (Recommended)
```
POST /api/auto-optimize
```
Automatically analyzes and optimizes with the best strategy.

**Request:**
```json
{
  "prompt": "Your prompt here"
}
```

**Response includes:**
- Optimized prompt
- Safety and quality scores
- Alternative versions
- Applied optimizations

### 2. Smart Optimize
```
POST /api/smart-optimize
```
Uses AI-first approach with customizable parameters.

**Request:**
```json
{
  "prompt": "Your prompt here",
  "mode": "auto",  // or "enhance", "transform", "stylize", etc.
  "target_style": "cinematic"  // optional
}
```

### 3. Unified Optimize (Advanced)
```
POST /api/unified-optimize
```
Full control over optimization strategy and parameters.

**Request:**
```json
{
  "prompt": "Your prompt here",
  "strategy": "adaptive",  // or "guideline_first", "ai_first", "parallel"
  "ai_mode": "enhance",
  "target_style": "cinematic",
  "enhancement_level": 0.7
}
```

### 4. Analyze
```
POST /api/analyze
```
Get detailed analysis of your prompt before optimization.

## Examples

### Example 1: Sensitive Content
**Original:** "A violent fight scene in a dark alley"

**Optimized:** "Professional film production scene depicting choreographed action sequence in a dark alley, with dramatic lighting and cinematic composition, ultra high definition"

**What happened:**
- "violent fight" → "choreographed action sequence"
- Added professional film context
- Enhanced with cinematic details

### Example 2: Safe Creative Content
**Original:** "Beautiful sunset over the ocean"

**Optimized:** "During golden hour, Beautiful sunset over the ocean, with vibrant color palette and ethereal atmosphere, creating a sense of tranquility, ultra high definition"

**What happened:**
- Added temporal context (golden hour)
- Enhanced with visual and atmospheric details
- Preserved original beauty while adding depth

### Example 3: Educational Content
**Original:** "Medical procedure showing surgical techniques"

**Optimized:** "For medical education and training purposes: Professional footage of surgical techniques demonstration, with clear visibility and educational framing, adhering to medical documentation standards"

**What happened:**
- Added educational context for legitimacy
- Framed as professional documentation
- Emphasized educational purpose

## Scoring System

Each optimization receives three scores:

1. **Unified Confidence Score** (0-1)
   - Overall likelihood of success
   - Combines safety and quality factors

2. **Safety Score** (0-1)
   - How well sensitive content was handled
   - 1.0 = no sensitive content or perfectly handled

3. **Quality Score** (0-1)
   - Creative and technical enhancement quality
   - Based on patterns, context, and coherence

## Best Practices

1. **For Sensitive Content:**
   - Let the system auto-detect and handle
   - Review suggested reframings
   - Consider educational or artistic context

2. **For Creative Enhancement:**
   - Start with clear, specific subjects
   - Allow AI to add technical and atmospheric details
   - Review alternative versions for options

3. **For Maximum Quality:**
   - Use descriptive initial prompts
   - Enable higher enhancement levels
   - Consider style transfer options

## Tips for Success

1. **Be Specific:** The more detailed your initial prompt, the better the optimization
2. **Trust the Analysis:** The system accurately detects sensitivity levels
3. **Review Alternatives:** Alternative versions often provide great options
4. **Iterate:** Use the analysis to understand how to improve your prompts

## Advanced Features

### Style Transfer
Transform your prompt into specific styles:
- Cinematic
- Documentary
- Minimalist
- Artistic
- Maximalist

### Context Enhancement
Automatically adds missing contexts:
- Temporal (time of day, era)
- Spatial (location, environment)
- Emotional (mood, atmosphere)
- Technical (camera, lighting)

### Pattern Learning
The system learns from successful patterns:
- Structural patterns (shot types, composition)
- Semantic patterns (emotions, concepts)
- Stylistic patterns (aesthetics, moods)
- Narrative patterns (storytelling elements)

## Troubleshooting

**Issue:** Prompt seems over-optimized
**Solution:** Use lower enhancement level or minimalist style

**Issue:** Sensitive content not properly handled
**Solution:** Use guideline_first strategy explicitly

**Issue:** Lost original meaning
**Solution:** Check alternative versions or use parallel strategy

## API Response Reference

### Success Response Structure
```json
{
  "success": true,
  "original": "Original prompt",
  "optimized": "Optimized prompt",
  "confidence": 0.75,
  "safety_score": 0.9,
  "quality_score": 0.8,
  "alternatives": [
    {
      "type": "minimalist",
      "prompt": "Alternative version",
      "description": "Style description",
      "confidence": 0.7
    }
  ],
  "optimization_steps": ["Step 1", "Step 2"],
  "suggestions": ["Suggestion 1", "Suggestion 2"]
}
```

### Error Response Structure
```json
{
  "success": false,
  "error": "Error message"
}
```

## Integration Guide

### Python Example
```python
import requests

def optimize_prompt(prompt):
    response = requests.post(
        'http://localhost:5000/api/auto-optimize',
        json={'prompt': prompt}
    )
    result = response.json()
    return result['optimized'] if result['success'] else None
```

### JavaScript Example
```javascript
async function optimizePrompt(prompt) {
    const response = await fetch('/api/auto-optimize', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt})
    });
    const result = await response.json();
    return result.success ? result.optimized : null;
}
```

## Conclusion

The Unified Optimizer provides a powerful, balanced approach to prompt optimization. It ensures your creative vision is both safely expressed and maximally enhanced. Whether you're dealing with sensitive content or seeking creative excellence, the unified system adapts to deliver the best results.