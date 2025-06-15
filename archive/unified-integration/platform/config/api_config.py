"""
API Configuration for Video Generation Services

This file contains configuration for various video/image generation APIs.
Update with your API keys when services become available.
"""

import os
from typing import Optional

class APIConfig:
    # OpenAI / Sora Configuration (Future)
    SORA_API_KEY: Optional[str] = os.getenv('SORA_API_KEY', None)
    SORA_API_ENDPOINT: str = "https://api.openai.com/v1/video/generations"  # Placeholder
    SORA_MODEL: str = "sora-1.0"  # Placeholder
    
    # OpenAI DALL-E (Currently Available)
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY', None)
    
    # Stable Diffusion / Stable Video
    STABILITY_API_KEY: Optional[str] = os.getenv('STABILITY_API_KEY', None)
    
    # Runway ML
    RUNWAY_API_KEY: Optional[str] = os.getenv('RUNWAY_API_KEY', None)
    
    # Replicate (for various models)
    REPLICATE_API_KEY: Optional[str] = os.getenv('REPLICATE_API_KEY', None)
    
    # Anthropic Claude API
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY', None)
    
    @classmethod
    def is_sora_available(cls) -> bool:
        """Check if Sora API is configured"""
        return cls.SORA_API_KEY is not None
    
    @classmethod
    def get_available_services(cls) -> list:
        """Get list of configured services"""
        services = []
        if cls.OPENAI_API_KEY:
            services.append("dalle")
        if cls.STABILITY_API_KEY:
            services.append("stable-diffusion")
        if cls.RUNWAY_API_KEY:
            services.append("runway")
        if cls.REPLICATE_API_KEY:
            services.append("replicate")
        if cls.SORA_API_KEY:
            services.append("sora")
        if cls.ANTHROPIC_API_KEY:
            services.append("claude")
        return services

# Example .env file content (create this file and add your keys):
"""
# .env file example (DO NOT COMMIT THIS FILE)
OPENAI_API_KEY=your-openai-api-key-here
SORA_API_KEY=your-sora-api-key-when-available
STABILITY_API_KEY=your-stability-ai-key
RUNWAY_API_KEY=your-runway-ml-key
REPLICATE_API_KEY=your-replicate-key
ANTHROPIC_API_KEY=your-anthropic-api-key-here
"""