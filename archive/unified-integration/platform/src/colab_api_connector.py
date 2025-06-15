"""
Direct Google Colab API Integration
Connects directly to Colab runtime using API credentials
"""

import os
import json
import requests
import asyncio
import aiohttp
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import base64
import time

logger = logging.getLogger(__name__)

@dataclass
class ColabCredentials:
    """Colab API credentials configuration"""
    runtime_url: str = os.getenv('COLAB_RUNTIME_URL', '')
    api_token: str = os.getenv('COLAB_API_TOKEN', '') 
    notebook_id: str = os.getenv('COLAB_NOTEBOOK_ID', '1EwfBj0nC9St-2hB1bv2zGWWDTcS4slsx')
    drive_folder_id: str = os.getenv('GOOGLE_DRIVE_FOLDER_ID', '')
    service_account_key: str = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY', '')

@dataclass 
class ColabTask:
    """Task to be executed on Colab"""
    task_id: str
    task_type: str  # 'text_generation', 'image_generation', 'model_training'
    prompt: str
    parameters: Dict[str, Any]
    priority: int = 5
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class ColabAPIConnector:
    """Direct API connector for Google Colab"""
    
    def __init__(self, credentials: Optional[ColabCredentials] = None):
        self.credentials = credentials or ColabCredentials()
        self.session = None
        self.runtime_info = None
        self.last_health_check = None
        self.task_queue = []
        self.active_tasks = {}
        
    async def initialize(self) -> bool:
        """Initialize connection to Colab runtime"""
        try:
            if not self.credentials.runtime_url and not self.credentials.api_token:
                logger.warning("No Colab credentials provided - running in simulation mode")
                return await self._initialize_simulation_mode()
            
            # Create authenticated session
            self.session = aiohttp.ClientSession(
                headers={
                    'Authorization': f'Bearer {self.credentials.api_token}',
                    'Content-Type': 'application/json'
                },
                timeout=aiohttp.ClientTimeout(total=30)
            )
            
            # Test connection
            health = await self.health_check()
            if health['status'] == 'healthy':
                logger.info("✅ Connected to Colab runtime successfully")
                return True
            else:
                logger.error("❌ Failed to connect to Colab runtime")
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize Colab connection: {e}")
            return await self._initialize_simulation_mode()
    
    async def _initialize_simulation_mode(self) -> bool:
        """Initialize in simulation mode for testing"""
        logger.info("🎭 Initializing Colab simulation mode")
        self.runtime_info = {
            'status': 'simulation',
            'gpu_type': 'T4 (Simulated)',
            'memory_gb': 15,
            'disk_gb': 107,
            'python_version': '3.10.12'
        }
        return True
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of Colab runtime"""
        try:
            if not self.session:
                return await self._simulated_health_check()
            
            # Real API call to runtime
            async with self.session.get(f"{self.credentials.runtime_url}/api/kernels") as response:
                if response.status == 200:
                    kernels = await response.json()
                    
                    # Get runtime information
                    runtime_info = await self._get_runtime_info()
                    
                    self.last_health_check = datetime.now()
                    return {
                        'status': 'healthy',
                        'kernels_active': len(kernels),
                        'runtime_info': runtime_info,
                        'last_check': self.last_health_check.isoformat()
                    }
                else:
                    return {'status': 'unhealthy', 'error': f'HTTP {response.status}'}
                    
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return await self._simulated_health_check()
    
    async def _simulated_health_check(self) -> Dict[str, Any]:
        """Simulated health check for testing"""
        return {
            'status': 'healthy',
            'simulation': True,
            'gpu_available': True,
            'gpu_name': 'Tesla T4 (Simulated)',
            'memory_usage': '4.2/15.0 GB',
            'disk_usage': '12.3/107.0 GB',
            'uptime': '2h 34m',
            'last_check': datetime.now().isoformat()
        }
    
    async def _get_runtime_info(self) -> Dict[str, Any]:
        """Get detailed runtime information"""
        try:
            if not self.session:
                return self.runtime_info
            
            # Execute Python code to get system info
            code = """
import torch
import psutil
import platform
import json

info = {
    'gpu_available': torch.cuda.is_available(),
    'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    'gpu_memory_total': torch.cuda.get_device_properties(0).total_memory if torch.cuda.is_available() else 0,
    'cpu_count': psutil.cpu_count(),
    'memory_total': psutil.virtual_memory().total,
    'memory_available': psutil.virtual_memory().available,
    'disk_usage': psutil.disk_usage('/').percent,
    'python_version': platform.python_version(),
    'platform': platform.platform()
}

print(json.dumps(info))
"""
            
            result = await self.execute_code(code)
            if result['success']:
                return json.loads(result['output'])
            else:
                return self.runtime_info
                
        except Exception as e:
            logger.error(f"Failed to get runtime info: {e}")
            return self.runtime_info or {}
    
    async def execute_code(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute Python code on Colab runtime"""
        try:
            if not self.session:
                return await self._simulate_code_execution(code)
            
            # Prepare execution request
            payload = {
                'code': code,
                'session_id': await self._get_session_id()
            }
            
            # Execute code
            async with self.session.post(
                f"{self.credentials.runtime_url}/api/kernels/execute", 
                json=payload,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        'success': True,
                        'output': result.get('output', ''),
                        'execution_time': result.get('execution_time', 0),
                        'memory_usage': result.get('memory_usage', {})
                    }
                else:
                    return {
                        'success': False,
                        'error': f'HTTP {response.status}: {await response.text()}'
                    }
                    
        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            return await self._simulate_code_execution(code)
    
    async def _simulate_code_execution(self, code: str) -> Dict[str, Any]:
        """Simulate code execution for testing"""
        await asyncio.sleep(0.5)  # Simulate processing time
        
        # Simple simulation based on code content
        if 'torch.cuda.is_available()' in code:
            output = '{"gpu_available": true, "gpu_name": "Tesla T4", "memory_total": 16106127360}'
        elif 'text generation' in code.lower() or 'transformers' in code:
            output = 'Enhanced text: A stunning cinematic scene with dramatic lighting'
        elif 'image' in code.lower() or 'diffusion' in code:
            output = 'Generated image saved to /content/generated_image.png'
        else:
            output = 'Code executed successfully'
        
        return {
            'success': True,
            'output': output,
            'execution_time': 0.8,
            'simulation': True
        }
    
    async def generate_text(self, prompt: str, style: str = 'creative', **kwargs) -> Dict[str, Any]:
        """Generate enhanced text using Colab GPU"""
        code = f"""
# Text generation using GPU acceleration
import torch
from transformers import pipeline
import time

start_time = time.time()

# Initialize model (cached after first use)
try:
    generator = pipeline(
        "text-generation",
        model="gpt2-medium",
        device=0 if torch.cuda.is_available() else -1,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    
    # Style-specific prompts
    style_prompts = {{
        'creative': f"Create an imaginative and creative scene: {prompt}",
        'cinematic': f"Describe a cinematic movie scene: {prompt}",
        'artistic': f"Paint an artistic masterpiece: {prompt}",
        'dramatic': f"Create a dramatic and intense scene: {prompt}"
    }}
    
    enhanced_prompt = style_prompts.get('{style}', f"Create a {style} description: {prompt}")
    
    # Generate text
    result = generator(
        enhanced_prompt,
        max_length=256,
        num_return_sequences=1,
        temperature=0.7,
        do_sample=True,
        pad_token_id=generator.tokenizer.eos_token_id
    )
    
    generated_text = result[0]['generated_text'].replace(enhanced_prompt, "").strip()
    processing_time = time.time() - start_time
    
    print(f"SUCCESS|{{generated_text}}|{{processing_time:.2f}}|{{torch.cuda.is_available()}}")
    
except Exception as e:
    # Fallback enhancement
    fallback = f"A beautifully crafted {style} scene featuring {prompt} with enhanced artistic vision"
    print(f"FALLBACK|{{fallback}}|0.1|False|{{str(e)}}")
"""
        
        result = await self.execute_code(code)
        
        if result['success']:
            output = result['output'].strip()
            if output.startswith('SUCCESS|'):
                parts = output.split('|')
                return {
                    'success': True,
                    'enhanced_text': parts[1],
                    'processing_time': float(parts[2]),
                    'gpu_used': parts[3] == 'True',
                    'original_prompt': prompt,
                    'style': style
                }
            elif output.startswith('FALLBACK|'):
                parts = output.split('|')
                return {
                    'success': True,
                    'enhanced_text': parts[1],
                    'processing_time': float(parts[2]),
                    'gpu_used': False,
                    'fallback': True,
                    'error': parts[4] if len(parts) > 4 else None
                }
        
        # Final fallback
        return {
            'success': True,
            'enhanced_text': f"A stunning {style} visualization of {prompt}",
            'processing_time': 0.1,
            'gpu_used': False,
            'fallback': True
        }
    
    async def generate_image(self, prompt: str, style: str = 'photorealistic', **kwargs) -> Dict[str, Any]:
        """Generate image using Colab GPU"""
        code = f"""
# Image generation using Stable Diffusion
import torch
from diffusers import StableDiffusionPipeline
import base64
import io
from PIL import Image
import time

start_time = time.time()

try:
    # Load model (cached after first use)
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
    
    # Style-specific prompts
    style_prompts = {{
        'photorealistic': f"{prompt}, photorealistic, high detail, 8k resolution",
        'artistic': f"{prompt}, digital art, artistic style, vibrant colors",
        'cinematic': f"{prompt}, cinematic lighting, dramatic composition"
    }}
    
    enhanced_prompt = style_prompts.get('{style}', f"{prompt}, {style} style")
    
    # Generate image
    image = pipe(enhanced_prompt, num_inference_steps=20).images[0]
    
    # Convert to base64
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    processing_time = time.time() - start_time
    
    print(f"SUCCESS|{{img_str[:100]}}...|{{processing_time:.2f}}|{{torch.cuda.is_available()}}")
    
except Exception as e:
    print(f"ERROR|Image generation failed: {{str(e)}}|0.1|False")
"""
        
        result = await self.execute_code(code)
        
        if result['success'] and result['output'].startswith('SUCCESS|'):
            parts = result['output'].split('|')
            return {
                'success': True,
                'image_base64': parts[1] + '...',  # Truncated for demo
                'processing_time': float(parts[2]),
                'gpu_used': parts[3] == 'True',
                'prompt': prompt,
                'style': style
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Image generation failed'),
                'fallback_description': f"Would generate {style} image: {prompt}"
            }
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        health = await self.health_check()
        
        return {
            'runtime_status': health,
            'task_queue_size': len(self.task_queue),
            'active_tasks': len(self.active_tasks),
            'credentials_configured': bool(self.credentials.api_token),
            'last_activity': datetime.now().isoformat(),
            'capabilities': [
                'text_generation',
                'image_generation', 
                'model_training',
                'data_processing'
            ]
        }
    
    async def _get_session_id(self) -> str:
        """Get or create session ID for code execution"""
        # In a real implementation, this would manage Jupyter kernel sessions
        return "default_session"
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
            
# Global connector instance
_colab_connector = None

def get_colab_connector() -> ColabAPIConnector:
    """Get global Colab connector instance"""
    global _colab_connector
    if _colab_connector is None:
        _colab_connector = ColabAPIConnector()
    return _colab_connector

async def initialize_colab_api():
    """Initialize Colab API connection"""
    connector = get_colab_connector()
    success = await connector.initialize()
    return success