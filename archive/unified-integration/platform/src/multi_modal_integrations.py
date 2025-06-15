"""
Multi-Modal Integration System
Handles text enhancement + visual simulation for comprehensive prompt testing
"""

import os
import json
import asyncio
import logging
import tempfile
import base64
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
from pathlib import Path

try:
    import aiohttp
except ImportError:
    aiohttp = None

from src.integration_manager import IntegrationManager, IntegrationType, IntegrationConfig

logger = logging.getLogger(__name__)


class ModalityType(Enum):
    """Types of content modalities"""
    TEXT = "text"
    IMAGE = "image" 
    VIDEO = "video"
    AUDIO = "audio"


@dataclass
class GenerationRequest:
    """Request for multi-modal content generation"""
    prompt: str
    modalities: List[ModalityType]
    quality_level: float = 0.7
    preview_mode: bool = True
    collaboration_mode: str = "sequential"  # sequential, parallel, hybrid


@dataclass
class GenerationResult:
    """Result from multi-modal generation"""
    original_prompt: str
    enhanced_prompt: str
    text_enhancement_metadata: Dict[str, Any]
    generated_content: Dict[ModalityType, Any]
    generation_metadata: Dict[str, Any]
    total_cost: float
    generation_time: float
    quality_scores: Dict[ModalityType, float]


class MultiModalIntegrationManager:
    """Manages integration between text enhancement and visual generation APIs"""
    
    def __init__(self):
        self.base_integration_manager = IntegrationManager()
        self.visual_integrations = {}
        self.generation_cache = {}
        self.setup_visual_integrations()
    
    def setup_visual_integrations(self):
        """Setup visual generation integrations"""
        
        # Stable Diffusion (local or API)
        if os.getenv('STABILITY_API_KEY'):
            self.visual_integrations['stability'] = {
                'type': 'image',
                'api_key': os.getenv('STABILITY_API_KEY'),
                'base_url': 'https://api.stability.ai/v1',
                'models': ['stable-diffusion-xl-1024-v1-0', 'stable-diffusion-v1-6'],
                'cost_per_image': 0.04,  # $0.04 per image
                'capabilities': ['text-to-image', 'image-to-image']
            }
        
        # RunPod/Replicate for video
        if os.getenv('REPLICATE_API_TOKEN'):
            self.visual_integrations['replicate'] = {
                'type': 'video',
                'api_key': os.getenv('REPLICATE_API_TOKEN'),
                'base_url': 'https://api.replicate.com/v1',
                'models': ['stability-ai/stable-video-diffusion', 'meta/llama-2-70b-chat'],
                'cost_per_generation': 0.50,  # $0.50 per video
                'capabilities': ['text-to-video', 'image-to-video']
            }
        
        # DALL-E (OpenAI)
        if os.getenv('OPENAI_API_KEY'):
            self.visual_integrations['dalle'] = {
                'type': 'image',
                'api_key': os.getenv('OPENAI_API_KEY'),
                'base_url': 'https://api.openai.com/v1',
                'models': ['dall-e-3', 'dall-e-2'],
                'cost_per_image': 0.08,  # $0.08 per DALL-E 3 image
                'capabilities': ['text-to-image']
            }
        
        # Midjourney (via Discord API - if configured)
        if os.getenv('MIDJOURNEY_API_KEY'):
            self.visual_integrations['midjourney'] = {
                'type': 'image',
                'api_key': os.getenv('MIDJOURNEY_API_KEY'),
                'base_url': 'https://api.midjourney.com/v1',
                'models': ['midjourney-v6', 'midjourney-niji'],
                'cost_per_image': 0.10,  # $0.10 per image
                'capabilities': ['text-to-image', 'style-transfer']
            }
        
        # RunwayML for video
        if os.getenv('RUNWAY_API_KEY'):
            self.visual_integrations['runway'] = {
                'type': 'video',
                'api_key': os.getenv('RUNWAY_API_KEY'),
                'base_url': 'https://api.runwayml.com/v1',
                'models': ['gen-3-alpha', 'gen-2'],
                'cost_per_generation': 1.00,  # $1.00 per video
                'capabilities': ['text-to-video', 'image-to-video', 'video-editing']
            }
    
    async def collaborative_enhancement(self, request: GenerationRequest) -> GenerationResult:
        """Perform collaborative enhancement across text and visual modalities"""
        start_time = datetime.now()
        total_cost = 0.0
        
        # Step 1: Get optimal text enhancement
        text_integration, text_model, text_metadata = self.base_integration_manager.get_optimal_integration(
            "enhancement", request.prompt, request.quality_level
        )
        
        # Step 2: Enhance the prompt using the selected integration
        enhanced_prompt, enhancement_cost = await self._enhance_prompt_with_integration(
            request.prompt, text_integration, text_model
        )
        total_cost += enhancement_cost
        
        # Step 3: Generate visual content based on collaboration mode
        generated_content = {}
        quality_scores = {}
        
        if request.collaboration_mode == "sequential":
            # Sequential: Use enhanced prompt for all visual generation
            for modality in request.modalities:
                if modality in [ModalityType.IMAGE, ModalityType.VIDEO]:
                    content, cost, quality = await self._generate_visual_content(
                        enhanced_prompt, modality, request.preview_mode
                    )
                    generated_content[modality] = content
                    quality_scores[modality] = quality
                    total_cost += cost
                    
        elif request.collaboration_mode == "parallel":
            # Parallel: Generate multiple variants and compare
            tasks = []
            for modality in request.modalities:
                if modality in [ModalityType.IMAGE, ModalityType.VIDEO]:
                    tasks.append(self._generate_visual_content(
                        enhanced_prompt, modality, request.preview_mode
                    ))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(results):
                if not isinstance(result, Exception):
                    modality = list(request.modalities)[i]
                    content, cost, quality = result
                    generated_content[modality] = content
                    quality_scores[modality] = quality
                    total_cost += cost
                    
        elif request.collaboration_mode == "hybrid":
            # Hybrid: Enhance prompt iteratively based on visual feedback
            current_prompt = enhanced_prompt
            
            for modality in request.modalities:
                if modality in [ModalityType.IMAGE, ModalityType.VIDEO]:
                    # Generate initial content
                    content, cost, quality = await self._generate_visual_content(
                        current_prompt, modality, request.preview_mode
                    )
                    
                    # If quality is low, try to improve prompt
                    if quality < request.quality_level and quality < 0.8:
                        improved_prompt = await self._improve_prompt_based_on_visual_feedback(
                            current_prompt, modality, quality
                        )
                        if improved_prompt != current_prompt:
                            content, additional_cost, quality = await self._generate_visual_content(
                                improved_prompt, modality, request.preview_mode
                            )
                            cost += additional_cost
                            current_prompt = improved_prompt
                    
                    generated_content[modality] = content
                    quality_scores[modality] = quality
                    total_cost += cost
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        # Record usage for learning
        self._record_multi_modal_usage(request, enhanced_prompt, generated_content, 
                                     quality_scores, total_cost, generation_time)
        
        return GenerationResult(
            original_prompt=request.prompt,
            enhanced_prompt=enhanced_prompt,
            text_enhancement_metadata=text_metadata,
            generated_content=generated_content,
            generation_metadata={
                'collaboration_mode': request.collaboration_mode,
                'integrations_used': list(self.visual_integrations.keys()),
                'generation_time': generation_time
            },
            total_cost=total_cost,
            generation_time=generation_time,
            quality_scores=quality_scores
        )
    
    async def _enhance_prompt_with_integration(self, prompt: str, integration: str, model: str) -> Tuple[str, float]:
        """Enhance prompt using specified integration"""
        try:
            if integration == 'claude':
                return await self._enhance_with_claude(prompt, model)
            elif integration == 'openai':
                return await self._enhance_with_openai(prompt, model)
            else:
                return prompt, 0.0
        except Exception as e:
            logger.error(f"Enhancement failed with {integration}: {e}")
            return prompt, 0.0
    
    async def _enhance_with_claude(self, prompt: str, model: str) -> Tuple[str, float]:
        """Enhance prompt using Claude"""
        try:
            import anthropic
            client = anthropic.AsyncAnthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            
            enhancement_prompt = f"""Enhance this prompt for AI image/video generation. Make it more specific, visual, and descriptive while maintaining the original intent:

Original prompt: {prompt}

Enhanced prompt (focus on visual details, lighting, composition, style):"""

            response = await client.messages.create(
                model=model,
                max_tokens=300,
                temperature=0.7,
                messages=[{"role": "user", "content": enhancement_prompt}]
            )
            
            enhanced = response.content[0].text.strip()
            
            # Calculate cost
            input_tokens = len(enhancement_prompt.split()) * 1.3
            output_tokens = response.usage.output_tokens
            
            config = self.base_integration_manager.integrations.get('claude')
            if config and model in config.cost_per_1k_tokens:
                costs = config.cost_per_1k_tokens[model]
                cost = (input_tokens * costs['input'] + output_tokens * costs['output']) / 1000
            else:
                cost = 0.01  # Fallback estimate
            
            return enhanced, cost
            
        except Exception as e:
            logger.error(f"Claude enhancement failed: {e}")
            return prompt, 0.0
    
    async def _enhance_with_openai(self, prompt: str, model: str) -> Tuple[str, float]:
        """Enhance prompt using OpenAI"""
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating detailed prompts for AI image and video generation."},
                    {"role": "user", "content": f"Enhance this prompt for AI generation with specific visual details: {prompt}"}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            enhanced = response.choices[0].message.content.strip()
            
            # Estimate cost (rough calculation)
            cost = 0.002  # Rough estimate for GPT-3.5/4
            
            return enhanced, cost
            
        except Exception as e:
            logger.error(f"OpenAI enhancement failed: {e}")
            return prompt, 0.0
    
    async def _generate_visual_content(self, prompt: str, modality: ModalityType, preview_mode: bool) -> Tuple[Any, float, float]:
        """Generate visual content for specified modality"""
        if modality == ModalityType.IMAGE:
            return await self._generate_image(prompt, preview_mode)
        elif modality == ModalityType.VIDEO:
            return await self._generate_video(prompt, preview_mode)
        else:
            return None, 0.0, 0.0
    
    async def _generate_image(self, prompt: str, preview_mode: bool) -> Tuple[str, float, float]:
        """Generate image using best available integration"""
        
        # Priority order for image generation
        priority_order = ['stability', 'dalle', 'midjourney']
        
        for integration_name in priority_order:
            if integration_name in self.visual_integrations:
                try:
                    integration = self.visual_integrations[integration_name]
                    
                    if integration_name == 'stability':
                        return await self._generate_with_stability(prompt, preview_mode)
                    elif integration_name == 'dalle':
                        return await self._generate_with_dalle(prompt, preview_mode)
                    elif integration_name == 'midjourney':
                        return await self._generate_with_midjourney(prompt, preview_mode)
                        
                except Exception as e:
                    logger.error(f"Image generation failed with {integration_name}: {e}")
                    continue
        
        # Fallback: return placeholder
        return self._create_placeholder_image(prompt), 0.0, 0.5
    
    async def _generate_video(self, prompt: str, preview_mode: bool) -> Tuple[str, float, float]:
        """Generate video using best available integration"""
        
        # Priority order for video generation
        priority_order = ['runway', 'replicate']
        
        for integration_name in priority_order:
            if integration_name in self.visual_integrations:
                try:
                    integration = self.visual_integrations[integration_name]
                    
                    if integration_name == 'runway':
                        return await self._generate_with_runway(prompt, preview_mode)
                    elif integration_name == 'replicate':
                        return await self._generate_with_replicate(prompt, preview_mode)
                        
                except Exception as e:
                    logger.error(f"Video generation failed with {integration_name}: {e}")
                    continue
        
        # Fallback: return placeholder
        return self._create_placeholder_video(prompt), 0.0, 0.5
    
    async def _generate_with_stability(self, prompt: str, preview_mode: bool) -> Tuple[str, float, float]:
        """Generate image using Stability AI"""
        try:
            if not aiohttp:
                logger.warning("aiohttp not available, returning placeholder")
                return self._create_placeholder_image(prompt), 0.0, 0.5
                
            integration = self.visual_integrations['stability']
            
            # Use lower resolution for preview mode
            size = "512x512" if preview_mode else "1024x1024"
            cost = integration['cost_per_image'] * (0.5 if preview_mode else 1.0)
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f"Bearer {integration['api_key']}",
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'text_prompts': [{'text': prompt}],
                    'cfg_scale': 7,
                    'height': int(size.split('x')[1]),
                    'width': int(size.split('x')[0]),
                    'samples': 1,
                    'steps': 30 if not preview_mode else 20
                }
                
                async with session.post(
                    f"{integration['base_url']}/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Save image to temp file
                        image_data = base64.b64decode(result['artifacts'][0]['base64'])
                        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                        temp_file.write(image_data)
                        temp_file.close()
                        
                        # Calculate quality score based on prompt complexity
                        quality = self._calculate_image_quality_score(prompt, len(image_data))
                        
                        return temp_file.name, cost, quality
                    else:
                        logger.error(f"Stability API error: {response.status}")
                        return self._create_placeholder_image(prompt), 0.0, 0.3
                        
        except Exception as e:
            logger.error(f"Stability generation failed: {e}")
            return self._create_placeholder_image(prompt), 0.0, 0.3
    
    async def _generate_with_dalle(self, prompt: str, preview_mode: bool) -> Tuple[str, float, float]:
        """Generate image using DALL-E"""
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            integration = self.visual_integrations['dalle']
            model = "dall-e-2" if preview_mode else "dall-e-3"
            size = "512x512" if preview_mode else "1024x1024"
            cost = integration['cost_per_image'] * (0.5 if preview_mode else 1.0)
            
            response = await client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality="standard" if preview_mode else "hd",
                n=1
            )
            
            # Download and save image
            image_url = response.data[0].url
            if aiohttp:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as img_response:
                        if img_response.status == 200:
                            image_data = await img_response.read()
                            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                            temp_file.write(image_data)
                            temp_file.close()
                            
                            quality = self._calculate_image_quality_score(prompt, len(image_data))
                            return temp_file.name, cost, quality
            
            return self._create_placeholder_image(prompt), 0.0, 0.3
            
        except Exception as e:
            logger.error(f"DALL-E generation failed: {e}")
            return self._create_placeholder_image(prompt), 0.0, 0.3
    
    async def _generate_with_replicate(self, prompt: str, preview_mode: bool) -> Tuple[str, float, float]:
        """Generate video using Replicate"""
        try:
            integration = self.visual_integrations['replicate']
            cost = integration['cost_per_generation'] * (0.5 if preview_mode else 1.0)
            
            # For now, return placeholder since video generation takes time
            # In production, this would use async job polling
            placeholder_video = self._create_placeholder_video(prompt)
            quality = 0.7  # Assume good quality for Replicate
            
            return placeholder_video, cost, quality
            
        except Exception as e:
            logger.error(f"Replicate generation failed: {e}")
            return self._create_placeholder_video(prompt), 0.0, 0.3
    
    async def _generate_with_runway(self, prompt: str, preview_mode: bool) -> Tuple[str, float, float]:
        """Generate video using RunwayML"""
        try:
            integration = self.visual_integrations['runway']
            cost = integration['cost_per_generation'] * (0.5 if preview_mode else 1.0)
            
            # Placeholder implementation
            placeholder_video = self._create_placeholder_video(prompt)
            quality = 0.8  # Assume high quality for Runway
            
            return placeholder_video, cost, quality
            
        except Exception as e:
            logger.error(f"Runway generation failed: {e}")
            return self._create_placeholder_video(prompt), 0.0, 0.3
    
    def _create_placeholder_image(self, prompt: str) -> str:
        """Create a placeholder image with prompt text"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import os
            
            # Create a simple placeholder
            img = Image.new('RGB', (512, 512), color='lightgray')
            draw = ImageDraw.Draw(img)
            
            # Add prompt text
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Wrap text
            import textwrap
            wrapped_text = textwrap.fill(prompt[:100], width=40)  # Limit prompt length
            draw.text((10, 200), f"Preview Image:\n{wrapped_text}", fill='black', font=font)
            draw.text((10, 450), "Generated with Sora AI", fill='darkgray', font=font)
            
            # Save to temp file in generated content directory
            os.makedirs('/tmp/generated_content', exist_ok=True)
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix='.png', 
                dir='/tmp/generated_content'
            )
            img.save(temp_file.name)
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Placeholder creation failed: {e}")
            # Create minimal fallback
            import os
            os.makedirs('/tmp/generated_content', exist_ok=True)
            fallback_path = "/tmp/generated_content/placeholder.png"
            if not os.path.exists(fallback_path):
                try:
                    from PIL import Image
                    img = Image.new('RGB', (512, 512), color='lightgray')
                    img.save(fallback_path)
                except:
                    pass
            return fallback_path
    
    def _create_placeholder_video(self, prompt: str) -> str:
        """Create a placeholder video file"""
        import os
        
        # Create placeholder video path
        os.makedirs('/tmp/generated_content', exist_ok=True)
        placeholder_path = "/tmp/generated_content/placeholder_video.mp4"
        
        # For now, just return the path - in production this would create an actual video
        return placeholder_path
    
    def _calculate_image_quality_score(self, prompt: str, image_size_bytes: int) -> float:
        """Calculate quality score based on prompt complexity and image size"""
        base_score = 0.7
        
        # Adjust based on prompt complexity
        if len(prompt) > 100:
            base_score += 0.1
        if any(word in prompt.lower() for word in ['detailed', 'intricate', 'professional']):
            base_score += 0.1
        
        # Adjust based on image size (larger = potentially higher quality)
        if image_size_bytes > 1024 * 1024:  # > 1MB
            base_score += 0.1
        
        return min(1.0, base_score)
    
    async def _improve_prompt_based_on_visual_feedback(self, prompt: str, modality: ModalityType, 
                                                     current_quality: float) -> str:
        """Improve prompt based on visual generation quality feedback"""
        if current_quality < 0.5:
            # Add more descriptive terms
            improvements = [
                "highly detailed",
                "professional photography",
                "cinematic lighting",
                "8K resolution",
                "award-winning"
            ]
            return f"{prompt}, {', '.join(improvements[:2])}"
        elif current_quality < 0.7:
            # Add specific visual terms
            improvements = [
                "sharp focus",
                "vibrant colors",
                "dramatic composition"
            ]
            return f"{prompt}, {improvements[0]}"
        
        return prompt
    
    def _record_multi_modal_usage(self, request: GenerationRequest, enhanced_prompt: str,
                                generated_content: Dict, quality_scores: Dict,
                                total_cost: float, generation_time: float):
        """Record usage for learning and analytics"""
        # This would integrate with the learning engine
        usage_record = {
            'timestamp': datetime.now().isoformat(),
            'original_prompt': request.prompt,
            'enhanced_prompt': enhanced_prompt,
            'modalities': [m.value for m in request.modalities],
            'collaboration_mode': request.collaboration_mode,
            'quality_scores': {k.value: v for k, v in quality_scores.items()},
            'total_cost': total_cost,
            'generation_time': generation_time,
            'success': len(generated_content) > 0
        }
        
        logger.info(f"Multi-modal generation recorded: {usage_record}")
    
    def get_available_integrations(self) -> Dict[str, Any]:
        """Get all available integrations for dashboard"""
        return {
            'text_integrations': {
                name: {
                    'status': self.base_integration_manager.get_integration_status(name).value,
                    'models': config.models,
                    'type': config.type.value
                }
                for name, config in self.base_integration_manager.integrations.items()
            },
            'visual_integrations': {
                name: {
                    'status': 'healthy',  # Simplified for now
                    'type': integration['type'],
                    'models': integration['models'],
                    'capabilities': integration['capabilities']
                }
                for name, integration in self.visual_integrations.items()
            }
        }
    
    def get_collaboration_modes(self) -> List[Dict[str, Any]]:
        """Get available collaboration modes"""
        return [
            {
                'mode': 'sequential',
                'description': 'Enhance text first, then generate visuals',
                'best_for': 'Consistent quality, lower cost',
                'estimated_time': 'Fast'
            },
            {
                'mode': 'parallel',
                'description': 'Generate multiple variants simultaneously',
                'best_for': 'Comparison, A/B testing',
                'estimated_time': 'Medium'
            },
            {
                'mode': 'hybrid',
                'description': 'Iterative improvement based on visual feedback',
                'best_for': 'Highest quality, experimentation',
                'estimated_time': 'Slower, highest quality'
            }
        ]


# Global instance
_multi_modal_manager: Optional[MultiModalIntegrationManager] = None


def get_multi_modal_manager() -> MultiModalIntegrationManager:
    """Get global multi-modal manager instance"""
    global _multi_modal_manager
    if _multi_modal_manager is None:
        _multi_modal_manager = MultiModalIntegrationManager()
    return _multi_modal_manager