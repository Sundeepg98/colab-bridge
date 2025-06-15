# Prompt Optimization Guide

## Overview

This guide explains how to use the prompt optimization features to improve success rates for challenging prompts.

## Key Principles

### 1. Professional Language
- Replace casual terms with professional equivalents
- Use industry-standard terminology
- Specify "performers" or "actors" instead of generic people

### 2. Context Framing
- Add educational, artistic, or documentary context
- Specify professional production environments
- Include safety and supervision details

### 3. Technical Specifications
- Include production details (lighting, cameras, crew)
- Mention safety protocols when appropriate
- Add post-production context

## Using the Optimizer

### Command Line Usage

```bash
# Basic optimization
python src/main.py optimize -i "your prompt here"

# With specific context
python src/main.py optimize -i "action scene" -c artistic

# Verbose mode for details
python src/main.py optimize -i "dramatic scene" -v
```

### Context Options

- `artistic` - For creative and artistic projects
- `educational` - For teaching and training content
- `documentary` - For factual documentation
- `cinematic` - For film production
- `scientific` - For research visualization
- `historical` - For historical recreation

## Optimization Examples

### Example 1: Action Scene
**Original**: "Person fighting in a dark alley"
**Optimized**: "Professional film production scene depicting: Professional performer performing choreographed combat sequences in a dark alley, using industry-standard safety protocols"

### Example 2: Medical Content
**Original**: "Doctor treating injured patient"
**Optimized**: "For medical education and training purposes: Doctor treating portrayed individual in medical training facility, adhering to professional medical standards"

### Example 3: Historical Content
**Original**: "Medieval battle scene"
**Optimized**: "Historical documentation recreating: Medieval choreographed combat sequences in historical recreation set, based on documented historical events"

## Best Practices

1. **Be Specific**: Vague prompts are harder to optimize
2. **Add Context Early**: Include your intended use in the original prompt
3. **Use Professional Terms**: Start with professional language when possible
4. **Include Safety**: Mention controlled environments for action content

## Success Factors

The optimizer considers:
- Presence of professional terminology
- Clear context and purpose
- Safety considerations
- Technical production details
- Educational or artistic framing

## Tips for Maximum Success

1. **Layer Contexts**: Combine multiple contexts (e.g., "educational" + "historical")
2. **Specify Professionals**: Always use "actor/performer" instead of generic terms
3. **Add Production Value**: Include technical details about filming
4. **Frame Sensitively**: Convert potentially problematic content to professional alternatives

## Common Transformations

| Original Term | Professional Alternative |
|--------------|-------------------------|
| Person | Professional performer |
| Fighting | Choreographed sequence |
| Violent | Dramatic action |
| Dangerous | Controlled stunt |
| Blood | Special effects |
| Weapon | Prop |
| Scary | Suspenseful |
| Disturbing | Thought-provoking |