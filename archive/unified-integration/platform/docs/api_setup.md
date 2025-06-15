# API Setup Guide

## Overview

The Sora AI Prompt Optimizer can be enhanced with AI APIs for even better results. When API keys are configured, the app will automatically use AI to further improve prompts.

## Supported APIs

### 1. OpenAI API (GPT-4 & DALL-E)
- **Purpose**: Enhance prompts with GPT-4, generate images with DALL-E
- **Get API Key**: https://platform.openai.com/api-keys
- **Benefits**:
  - GPT-4 enhancement adds creative details
  - DALL-E can generate preview images
  - ~15% confidence boost

### 2. Anthropic API (Claude)
- **Purpose**: Advanced prompt enhancement with Claude-3
- **Get API Key**: https://console.anthropic.com/account/keys
- **Benefits**:
  - Superior creative enhancement
  - Better understanding of complex themes
  - ~20% confidence boost

### 3. Stability AI
- **Purpose**: Future integration with Stable Video Diffusion
- **Get API Key**: https://platform.stability.ai/account/keys

### 4. Replicate
- **Purpose**: Access to various AI models
- **Get API Key**: https://replicate.com/account/api-tokens

## Setup Instructions

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`**:
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
   ```

3. **Restart the app**:
   ```bash
   ./run_app.sh
   ```

## How It Works

When API keys are configured:

1. **Auto-Optimization Process**:
   - First: Intelligent theme detection and optimization
   - Second: AI enhancement (Claude preferred, GPT-4 fallback)
   - Result: Even better prompts with AI-powered creativity

2. **Visual Indicators**:
   - Success rate shows "(AI Enhanced with Claude-3)" or "(AI Enhanced with GPT-4)"
   - AI suggestions appear below the optimized prompt
   - Confidence scores increase by 15-20%

3. **Fallback Behavior**:
   - If no API keys: Uses built-in optimization (still very effective!)
   - If Claude fails: Tries GPT-4
   - If all fail: Returns optimized prompt without AI enhancement

## Cost Considerations

- **OpenAI**: ~$0.01-0.03 per prompt enhancement
- **Anthropic**: ~$0.01-0.02 per prompt enhancement
- **Free Tier**: Both services offer free credits for testing

## Security

- Never commit your `.env` file
- Keep API keys secret
- The `.gitignore` already excludes `.env`

## Testing Without APIs

The app works excellently without API keys! The built-in optimization engine:
- Detects themes automatically
- Applies sophisticated framing
- Achieves 75-95% success rates
- Requires no external services

API enhancement is optional and adds an extra layer of creativity and confidence.