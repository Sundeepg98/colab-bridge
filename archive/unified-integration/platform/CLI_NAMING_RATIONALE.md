# CLI Naming Rationale

## Why Not "Sora"?

You're absolutely right to question the "Sora" naming! Here's why it doesn't make sense:

### Original Context
- **Sora** = OpenAI's text-to-video model (not even released yet)
- Project started as "Sora AI Exploration"
- But evolved into a **Generic AI Simulator Platform**

### Current Reality
The platform now supports:
- **Multiple Chatbots**: OpenAI GPT, Claude, Cohere, LLaMA
- **Multiple Simulators**: Stable Diffusion, DALL-E, Midjourney, RunwayML
- **Not Sora-specific at all!**

## Better Naming Options

### 1. **AI Platform CLI** (Current Choice)
```bash
# Commands
aiplatform health check
aip maintenance run    # Short alias
```
**Pros**: Clear, generic, professional
**Cons**: Maybe too generic

### 2. **Fusion CLI**
```bash
fusion health check
fusion integrations list
```
**Pros**: Suggests merging multiple AI services
**Cons**: Might conflict with other tools

### 3. **Orchestrate CLI**
```bash
orchestrate health check
orch maintenance run
```
**Pros**: Describes what it does (orchestrates AI services)
**Cons**: Long name

### 4. **AIHub CLI**
```bash
aihub health check
aihub costs analyze
```
**Pros**: Short, memorable, clear purpose
**Cons**: Many "hub" products exist

### 5. **Prism CLI**
```bash
prism health check
prism monitor dashboard
```
**Pros**: Suggests refracting one request to many services
**Cons**: Abstract naming

### 6. **Bridge CLI**
```bash
bridge health check
bridge integrations add
```
**Pros**: Connects users to AI services
**Cons**: Very generic

## Recommendation

Given that this is a **Generic AI Simulator Platform** that:
- Manages multiple AI services
- Handles both chatbots and simulators  
- Provides unified interface

The current choice of **AI Platform CLI** (`aiplatform`/`aip`) is appropriate because:
1. **Descriptive**: Clearly states it's for AI platform management
2. **Professional**: Suitable for enterprise use
3. **Memorable**: `aip` is a short, easy alias
4. **Unambiguous**: No confusion with specific models

## Usage Examples

```bash
# Long form
aiplatform health check
aiplatform integrations list
aiplatform costs analyze

# Short form  
aip health check
aip monitor dashboard
aip maintenance run cleanup

# Interactive
aip interactive
platform> health check
platform> costs analyze --by-service
```

## Summary

The name change from "Sora CLI" to "AI Platform CLI" correctly reflects that this tool manages a **generic platform** supporting **multiple AI services**, not just Sora (which isn't even integrated yet!).

This prevents confusion and accurately represents the tool's purpose.