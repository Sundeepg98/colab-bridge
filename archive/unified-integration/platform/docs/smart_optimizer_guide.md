# Smart Optimizer Guide

## Overview

The Smart Optimizer module (`smart_optimizer.py`) implements advanced prompt optimization techniques using pattern-based learning, contextual understanding, style transfer capabilities, semantic enhancement algorithms, and a multi-stage optimization pipeline. This module integrates seamlessly with the existing Ai Integration Platform app to make prompt generation much smarter.

## Key Features

### 1. Pattern-Based Learning
- Learns from successful prompt patterns
- Detects and scores patterns across multiple categories:
  - **Structural**: Opening patterns, technical specifications, composition
  - **Semantic**: Emotion/mood, action/movement, conceptual patterns
  - **Stylistic**: Artistic styles, color/lighting patterns
  - **Contextual**: Setting/environment, cultural context
  - **Narrative**: Story structure, temporal patterns

### 2. Contextual Understanding (NLP Techniques)
- Identifies primary themes in prompts
- Extracts semantic fields (emotion, atmosphere, visual elements)
- Detects missing contextual elements
- Generates context-specific suggestions
- Enhances prompts with appropriate context (temporal, spatial, emotional, cultural)

### 3. Style Transfer Capabilities
- Detects current style of prompts
- Transfers prompts to target styles:
  - **Cinematic**: Film-like, dramatic, atmospheric
  - **Documentary**: Authentic, observational, raw
  - **Artistic**: Creative, expressive, interpretive
  - **Minimalist**: Simple, clean, focused
  - **Maximalist**: Elaborate, detailed, complex
- Preserves core elements while adapting style

### 4. Semantic Enhancement
- **Specificity**: Makes vague terms more specific
- **Vividness**: Adds sensory details and descriptors
- **Coherence**: Improves logical flow
- **Depth**: Adds layers of meaning and symbolism

### 5. Multi-Stage Optimization Pipeline
1. **Analysis**: Analyzes patterns, context, and style
2. **Pattern Enhancement**: Adds high-value patterns
3. **Contextual Enrichment**: Fills missing contexts
4. **Semantic Enhancement**: Improves language and meaning
5. **Style Application**: Applies requested style transfers
6. **Final Polish**: Ensures grammar, removes redundancies

## API Endpoints

### 1. Smart Optimize
**Endpoint**: `/api/smart-optimize`
**Method**: POST

Performs intelligent prompt optimization using all available techniques.

**Request Body**:
```json
{
  "prompt": "Your prompt text here",
  "mode": "auto",  // auto, enhance, transform, stylize, contextualize, hybridize
  "target_style": "cinematic",  // optional, for stylize mode
  "emphasis_areas": ["technical_details", "emotional_depth"],  // optional
  "enhancement_level": 0.7  // 0.0 to 1.0, default 0.7
}
```

**Response**:
```json
{
  "success": true,
  "original": "Original prompt",
  "optimized": "Optimized prompt with all enhancements",
  "alternatives": ["Alternative version 1", "Alternative version 2"],
  "confidence_score": 0.85,
  "semantic_score": 0.78,
  "style_score": 0.92,
  "optimization_mode": "enhance",
  "transformations": ["Applied analysis", "Applied pattern_enhancement", ...],
  "patterns_detected": [
    {
      "type": "structural",
      "match": "Beautiful sunset",
      "confidence": 0.85,
      "suggestions": ["Add technical details", "Enhance composition"]
    }
  ]
}
```

### 2. Smart Analyze
**Endpoint**: `/api/smart-analyze`
**Method**: POST

Provides detailed analysis of a prompt without optimization.

**Request Body**:
```json
{
  "prompt": "Your prompt text here"
}
```

**Response**:
```json
{
  "success": true,
  "analysis": {
    "primary_theme": "narrative",
    "current_style": "cinematic",
    "missing_contexts": ["temporal", "emotional"],
    "context_suggestions": ["Add time of day", "Include emotional tone"],
    "semantic_fields": {
      "emotion": ["joy", "excitement"],
      "atmosphere": ["energetic"]
    },
    "pattern_statistics": {
      "structural": 3,
      "semantic": 2
    },
    "total_patterns_found": 5,
    "top_patterns": [...]
  }
}
```

### 3. Smart Style Transfer
**Endpoint**: `/api/smart-style-transfer`
**Method**: POST

Transfers a prompt to a specific style.

**Request Body**:
```json
{
  "prompt": "Your prompt text here",
  "target_style": "minimalist"  // cinematic, documentary, artistic, minimalist, maximalist
}
```

**Response**:
```json
{
  "success": true,
  "original": "Original prompt",
  "styled": "Prompt in target style",
  "fully_optimized": "Fully optimized version with style",
  "detected_original_style": "cinematic",
  "target_style": "minimalist",
  "style_score": 0.95,
  "available_styles": ["cinematic", "documentary", "artistic", "minimalist", "maximalist"]
}
```

### 4. Smart Insights
**Endpoint**: `/api/smart-insights`
**Method**: GET

Provides insights and statistics about optimization patterns.

**Response**:
```json
{
  "success": true,
  "insights": {
    "total_optimizations": 42,
    "average_confidence": 0.82,
    "most_common_patterns": [
      ["structural", 15],
      ["semantic", 12],
      ["stylistic", 8]
    ],
    "optimization_trends": {
      "trend": "improving",
      "recent_avg_confidence": 0.87,
      "improvement": 0.05
    },
    "available_modes": ["enhance", "transform", "stylize", "contextualize", "hybridize"],
    "available_styles": ["cinematic", "documentary", "artistic", "minimalist", "maximalist"]
  }
}
```

## Optimization Modes

1. **ENHANCE**: Basic enhancement with details and improvements
2. **TRANSFORM**: Complete transformation while preserving core meaning
3. **STYLIZE**: Focus on style transfer to target aesthetic
4. **CONTEXTUALIZE**: Deep context addition for richer prompts
5. **HYBRIDIZE**: Combine multiple approaches for maximum impact

## Usage Examples

### Basic Enhancement
```python
# Request
{
  "prompt": "A cat on a roof",
  "mode": "auto"
}

# Result
"Cinematic shot of a graceful cat perched on a weathered rooftop during golden hour, 
with dramatic lighting creating long shadows, capturing a moment of feline contemplation, 
ultra high definition"
```

### Style Transfer
```python
# Request
{
  "prompt": "A busy street market",
  "mode": "stylize",
  "target_style": "documentary"
}

# Result
"Documentary footage capturing authentic street market atmosphere with handheld camera, 
natural lighting revealing the raw energy of vendors and shoppers in unscripted moments"
```

### Deep Contextualization
```python
# Request
{
  "prompt": "A dancer",
  "mode": "contextualize",
  "enhancement_level": 0.9
}

# Result
"During blue hour in an abandoned theater, a solitary dancer moves through shadows 
and light, their graceful movements evoking feelings of nostalgia through subtle 
body language, creating an atmosphere of melancholic beauty that symbolizes 
the passage of time, ultra high definition"
```

## Best Practices

1. **Start with Auto Mode**: Let the optimizer detect the best approach
2. **Use Specific Modes**: When you know what type of enhancement you need
3. **Adjust Enhancement Level**: Higher values (0.8-1.0) for more dramatic changes
4. **Review Alternatives**: The optimizer provides alternative versions
5. **Check Confidence Scores**: Higher scores indicate better optimization
6. **Iterate**: Use the analysis endpoint to understand your prompts better

## Integration with Existing Features

The Smart Optimizer integrates seamlessly with:
- Standard prompt optimization
- Context framing system
- Advanced context elaboration
- Narrative enhancement
- Bold concept handling
- Interactive improvement

It can be used as a standalone optimization tool or in combination with other features for maximum effectiveness.

## Technical Details

The module uses:
- Pattern matching with regex for successful prompt patterns
- Semantic field mapping for contextual understanding
- Style signature detection and application
- Multi-stage pipeline processing
- Confidence scoring algorithms
- History tracking for continuous improvement

All processing is done locally without external API calls, ensuring fast and private optimization.