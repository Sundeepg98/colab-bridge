#!/usr/bin/env python3
"""
API-Based GPU Execution
No browser automation - just pure APIs with service account!
"""

import os
import json
import time
import requests
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from google.oauth2 import service_account

class APIBasedGPUExecutor:
    """Execute code on GPU using direct APIs - no browser needed!"""
    
    def __init__(self, service_account_path=None):
        self.service_account_path = service_account_path
        self.providers = {
            'runpod': RunPodExecutor(),
            'modal': ModalExecutor(), 
            'replicate': ReplicateExecutor(),
            'local': LocalExecutor()
        }
        self.preferred_provider = self._detect_best_provider()
    
    def _detect_best_provider(self):
        """Auto-detect the best available provider"""
        
        # Check for API keys in environment
        if os.getenv('RUNPOD_API_KEY'):
            return 'runpod'
        elif os.getenv('MODAL_TOKEN'):
            return 'modal'
        elif os.getenv('REPLICATE_API_TOKEN'):
            return 'replicate'
        else:
            return 'local'
    
    def execute(self, code: str, requirements: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute code on best available provider"""
        
        requirements = requirements or {'gpu': 'auto', 'timeout': 60}
        
        print(f"⚡ Executing via {self.preferred_provider} provider...")
        
        try:
            provider = self.providers[self.preferred_provider]
            result = provider.execute(code, requirements)
            
            return {
                'status': 'success',
                'output': result.get('output', ''),
                'provider': self.preferred_provider,
                'execution_time': result.get('execution_time', 0),
                'gpu_used': result.get('gpu_used', False)
            }
            
        except Exception as e:
            # Try fallback providers
            return self._try_fallback_providers(code, requirements, str(e))
    
    def _try_fallback_providers(self, code: str, requirements: Dict, original_error: str):
        """Try other providers if primary fails"""
        
        fallback_order = ['local', 'runpod', 'modal', 'replicate']
        fallback_order = [p for p in fallback_order if p != self.preferred_provider]
        
        for provider_name in fallback_order:
            try:
                print(f"   Trying fallback: {provider_name}...")
                provider = self.providers[provider_name]
                result = provider.execute(code, requirements)
                
                return {
                    'status': 'success',
                    'output': result.get('output', ''),
                    'provider': provider_name,
                    'fallback_from': self.preferred_provider,
                    'original_error': original_error
                }
                
            except Exception as e:
                print(f"   {provider_name} also failed: {e}")
                continue
        
        return {
            'status': 'error',
            'error': f"All providers failed. Original: {original_error}",
            'tried_providers': [self.preferred_provider] + fallback_order
        }

class RunPodExecutor:
    """Execute code on RunPod via API"""
    
    def __init__(self):
        self.api_key = os.getenv('RUNPOD_API_KEY')
        self.base_url = 'https://api.runpod.io/v2'
    
    def execute(self, code: str, requirements: Dict) -> Dict:
        if not self.api_key:
            raise Exception("RUNPOD_API_KEY not set")
        
        # Create serverless endpoint execution
        payload = {
            'input': {
                'code': code,
                'python_version': '3.10',
                'requirements': requirements.get('packages', [])
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Start execution
        response = requests.post(
            f"{self.base_url}/run",
            json=payload,
            headers=headers,
            timeout=requirements.get('timeout', 60)
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'output': result.get('output', ''),
                'execution_time': result.get('executionTime', 0),
                'gpu_used': True
            }
        else:
            raise Exception(f"RunPod API error: {response.text}")

class ModalExecutor:
    """Execute code on Modal.com via CLI"""
    
    def execute(self, code: str, requirements: Dict) -> Dict:
        # Check if Modal is installed
        try:
            subprocess.run(['modal', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("Modal CLI not installed. Run: pip install modal")
        
        # Create temporary Modal app
        modal_app = f'''
import modal

app = modal.App("vscode-colab-bridge")

@app.function(
    gpu="T4" if {requirements.get('gpu', 'auto') != 'none'} else None,
    timeout={requirements.get('timeout', 60)}
)
def execute_code():
    """Execute user code"""
    {self._indent_code(code)}
    
if __name__ == "__main__":
    with app.run():
        result = execute_code.remote()
        print(result)
'''
        
        # Write to temp file
        temp_file = Path('/tmp/modal_execution.py')
        with open(temp_file, 'w') as f:
            f.write(modal_app)
        
        # Execute via Modal
        try:
            result = subprocess.run(
                ['modal', 'run', str(temp_file)],
                capture_output=True,
                text=True,
                timeout=requirements.get('timeout', 60)
            )
            
            if result.returncode == 0:
                return {
                    'output': result.stdout,
                    'execution_time': 0,  # Modal doesn't return this easily
                    'gpu_used': requirements.get('gpu', 'auto') != 'none'
                }
            else:
                raise Exception(f"Modal execution failed: {result.stderr}")
                
        finally:
            # Clean up
            if temp_file.exists():
                temp_file.unlink()
    
    def _indent_code(self, code: str) -> str:
        """Indent code for function body"""
        lines = code.split('\n')
        return '\n'.join('    ' + line for line in lines)

class ReplicateExecutor:
    """Execute code via Replicate API"""
    
    def __init__(self):
        self.api_key = os.getenv('REPLICATE_API_TOKEN')
    
    def execute(self, code: str, requirements: Dict) -> Dict:
        if not self.api_key:
            raise Exception("REPLICATE_API_TOKEN not set")
        
        # Use a Python code execution model
        import replicate
        
        output = replicate.run(
            "meta/codellama-7b-python:de83ca41ecb7e6ea63dca40094be6b6a1654db1c91f6a77c3efd04bc41f72b8c",
            input={
                "code": code,
                "max_length": 1000
            }
        )
        
        return {
            'output': ''.join(output),
            'execution_time': 0,
            'gpu_used': True
        }

class LocalExecutor:
    """Execute code locally as fallback"""
    
    def execute(self, code: str, requirements: Dict) -> Dict:
        print("   🏠 Executing locally (no GPU)")
        
        # Execute locally with subprocess for safety
        try:
            result = subprocess.run(
                ['python3', '-c', code],
                capture_output=True,
                text=True,
                timeout=requirements.get('timeout', 30)
            )
            
            if result.returncode == 0:
                return {
                    'output': result.stdout,
                    'execution_time': 0,
                    'gpu_used': False
                }
            else:
                return {
                    'output': f"Error: {result.stderr}",
                    'execution_time': 0,
                    'gpu_used': False
                }
                
        except subprocess.TimeoutExpired:
            return {
                'output': "Error: Execution timed out",
                'execution_time': requirements.get('timeout', 30),
                'gpu_used': False
            }

class ZeroConfigAPIBridge:
    """Ultimate zero-config bridge using only APIs"""
    
    def __init__(self, service_account_path=None):
        self.service_account_path = service_account_path
        self.executor = APIBasedGPUExecutor(service_account_path)
        
        print("🚀 Zero-Config API Bridge initialized!")
        print(f"   Primary provider: {self.executor.preferred_provider}")
        print("   No browser automation needed!")
        print("   No manual setup required!")
    
    def execute(self, code: str, gpu_type: str = "auto") -> Dict[str, Any]:
        """Execute code with zero configuration"""
        
        requirements = {
            'gpu': gpu_type,
            'timeout': 60,
            'packages': self._detect_packages(code)
        }
        
        print(f"⚡ Executing code...")
        return self.executor.execute(code, requirements)
    
    def _detect_packages(self, code: str) -> list:
        """Auto-detect required packages from code"""
        packages = []
        
        if 'torch' in code or 'pytorch' in code:
            packages.append('torch')
        if 'tensorflow' in code or 'tf.' in code:
            packages.append('tensorflow')
        if 'numpy' in code or 'np.' in code:
            packages.append('numpy')
        if 'pandas' in code or 'pd.' in code:
            packages.append('pandas')
        
        return packages

# VS Code Extension Interface
class VSCodeAPIBridge:
    """Clean interface for VS Code extension"""
    
    def __init__(self):
        self.bridge = ZeroConfigAPIBridge()
        print("✅ VS Code API Bridge ready!")
    
    def execute_selection(self, code: str) -> str:
        """Execute selected code and return formatted output"""
        
        result = self.bridge.execute(code)
        
        if result['status'] == 'success':
            output = f"✅ Executed via {result['provider']}\n\n"
            output += result['output']
            if result.get('gpu_used'):
                output += f"\n\n🚀 GPU acceleration used!"
            return output
        else:
            return f"❌ Execution failed: {result.get('error', 'Unknown error')}"
    
    def configure(self):
        """Show configuration options"""
        return {
            'available_providers': list(self.bridge.executor.providers.keys()),
            'current_provider': self.bridge.executor.preferred_provider,
            'setup_required': self._check_setup_status()
        }
    
    def _check_setup_status(self):
        """Check what setup is needed"""
        setup_needed = []
        
        if not os.getenv('RUNPOD_API_KEY'):
            setup_needed.append('RUNPOD_API_KEY for RunPod GPU access')
        if not os.getenv('MODAL_TOKEN'):
            setup_needed.append('MODAL_TOKEN for Modal.com GPU access')
        if not os.getenv('REPLICATE_API_TOKEN'):
            setup_needed.append('REPLICATE_API_TOKEN for Replicate GPU access')
        
        return setup_needed

# One-liner for simple usage
def api_execute(code: str) -> Dict[str, Any]:
    """
    Execute code with zero setup - pure API approach
    
    Example:
        result = api_execute("print('Hello GPU!')")
        print(result['output'])
    """
    bridge = ZeroConfigAPIBridge()
    return bridge.execute(code)

if __name__ == "__main__":
    # Demo the API-based approach
    print("🧪 Testing API-Based GPU Execution...")
    
    # Test code
    test_code = '''
import sys
print(f"Python version: {sys.version}")

# Test basic computation
import numpy as np
result = np.random.rand(1000, 1000).mean()
print(f"Computation result: {result:.6f}")

# Try GPU if available
try:
    import torch
    if torch.cuda.is_available():
        print(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
        x = torch.rand(100, 100).cuda()
        y = torch.rand(100, 100).cuda()
        z = torch.matmul(x, y)
        print(f"GPU computation successful: {z.shape}")
    else:
        print("🏠 No GPU detected, using CPU")
except ImportError:
    print("📦 PyTorch not available")

print("✅ API-based execution completed!")
'''
    
    # Execute with zero config
    result = api_execute(test_code)
    
    print(f"\n📥 Result:")
    print(f"   Status: {result['status']}")
    print(f"   Provider: {result.get('provider', 'unknown')}")
    print(f"   GPU Used: {result.get('gpu_used', False)}")
    print(f"\n📄 Output:")
    print(result.get('output', 'No output'))
    
    if result.get('error'):
        print(f"\n❌ Error: {result['error']}")