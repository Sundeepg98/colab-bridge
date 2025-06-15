# UI Classification Guide: Chatbots vs Simulators

## Overview

The UI has been updated to clearly distinguish between **Chatbots** (text generation services) and **Simulators** (media generation services) throughout the platform.

## Integration Quickstart Page Updates

### 1. Category Tabs
At the top of the integration quickstart page, users can now filter services by type:
- **All Services** - Shows all available integrations
- **Chatbots** - Shows only text generation services
- **Simulators** - Shows only media generation services

### 2. Service Type Badges
Each integration card now displays a colored badge indicating its type:
- **CHATBOT** badge (blue) - For text generation services
- **SIMULATOR** badge (purple) - For media generation services  
- **BOTH** badge (green) - For services that support multiple modalities

### 3. Updated Service Descriptions
Service descriptions now clearly indicate their primary function:
- Claude: "Conversational AI"
- GPT-4: "Text Generation"
- Stable Diffusion: "Image Generation"
- RunwayML: "Video Generation"
- ElevenLabs: "Voice & Audio Generation"

### 4. Visual Classification

**Chatbot Services (💬):**
- OpenAI GPT-4/GPT-3.5
- Anthropic Claude
- Cohere Command
- Meta LLaMA

**Simulator Services (🎨):**
- Stable Diffusion (Image)
- DALL-E 3 (Image)
- Midjourney (Image)
- RunwayML (Video)
- Sora (Video - Coming Soon)
- ElevenLabs (Audio)

**Multi-Modal Services (🔄):**
- Replicate (Text & Image)
- Hugging Face (Text & Image)

## Admin Dashboard Updates

### 1. Integration Status Section
The integrations page now includes:
- Service type summary boxes showing the three categories
- Color-coded integration cards with borders:
  - Blue border for chatbots
  - Purple border for simulators
  - Green border for multi-modal services
- Type icons next to each service name

### 2. Visual Indicators
Each integration card displays:
- A circular icon with emoji (💬 for chatbots, 🎨 for simulators, 🔄 for both)
- Gradient background matching the service type
- Clear labeling of the service category

## Benefits of UI Classification

1. **Quick Identification** - Users can instantly see which services are conversational vs. content generation
2. **Better Organization** - Services are grouped logically by their primary function
3. **Easier Selection** - Filtering helps users find the right service for their needs
4. **Cost Understanding** - Different service types have different pricing models clearly indicated
5. **Workflow Clarity** - Users understand which services to use for text enhancement vs. media generation

## Technical Implementation

The classification is implemented through:
- `data-category` attributes on platform cards
- CSS classes for visual styling (`.chatbot`, `.simulator`, `.both`)
- JavaScript filtering functions
- Service type mapping in the integration display logic

## User Experience Flow

1. User visits Integration Quickstart page
2. Sees clear tabs to filter by service type
3. Each card shows a badge and description indicating its category
4. User can quickly identify and add the right type of service
5. In the admin dashboard, services are visually grouped and color-coded
6. Clear distinction helps with cost optimization and routing decisions

This UI update directly addresses the need to distinguish between conversational AI services (chatbots) and content generation services (simulators), making the platform more intuitive and user-friendly.