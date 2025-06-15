"""
Google Colab Configuration
Handles authentication and connection to your Colab notebooks
"""

import os
import requests
from typing import Optional, Dict, Any
import logging
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)

@dataclass
class ColabConfig:
    """Configuration for Google Colab integration"""
    notebook_url: str = "https://colab.research.google.com/drive/1EwfBj0nC9St-2hB1bv2zGWWDTcS4slsx"
    secret_key_name: str = "sun_colab"
    api_endpoint: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    ngrok_url: Optional[str] = None  # Auto-detected from Colab

class ColabAuthenticator:
    """Handles authentication with Google Colab"""
    
    def __init__(self, config: Optional[ColabConfig] = None):
        self.config = config or ColabConfig()
        self._api_key = None
        self._session = None
        
    @property
    def api_key(self) -> Optional[str]:
        """Get API key from environment or Colab secrets"""
        if self._api_key is None:
            # Try to get from environment
            self._api_key = os.getenv(self.config.secret_key_name.upper())
            
            # If not in environment, try Colab secrets
            if not self._api_key:
                try:
                    from google.colab import userdata
                    self._api_key = userdata.get(self.config.secret_key_name)
                except:
                    logger.warning(f"Could not retrieve {self.config.secret_key_name} from Colab secrets")
                    
        return self._api_key
    
    @property
    def session(self):
        """Get authenticated session"""
        if self._session is None:
            self._session = requests.Session()
            if self.api_key:
                self._session.headers.update({
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                })
        return self._session
    
    def validate_connection(self) -> bool:
        """Validate connection to Colab notebook"""
        if not self.config.api_endpoint:
            logger.error("No API endpoint configured")
            return False
            
        try:
            response = self.session.get(
                f"{self.config.api_endpoint}/health",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection validation failed: {e}")
            return False
    
    def make_request(self, method: str, endpoint: str, 
                    data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make authenticated request to Colab API"""
        if not self.config.api_endpoint:
            logger.error("No API endpoint configured")
            return None
            
        url = f"{self.config.api_endpoint}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=self.config.timeout)
            elif method.upper() == 'POST':
                response = self.session.post(
                    url, 
                    json=data, 
                    timeout=self.config.timeout
                )
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

# Global authenticator instance
_authenticator = None

def get_colab_auth() -> ColabAuthenticator:
    """Get global Colab authenticator"""
    global _authenticator
    if _authenticator is None:
        _authenticator = ColabAuthenticator()
    return _authenticator

def setup_colab_connection(api_endpoint: str) -> bool:
    """Setup connection to Colab notebook"""
    auth = get_colab_auth()
    auth.config.api_endpoint = api_endpoint
    
    if auth.validate_connection():
        logger.info(f"Successfully connected to Colab at {api_endpoint}")
        return True
    else:
        logger.error(f"Failed to connect to Colab at {api_endpoint}")
        return False

# Colab-specific utilities
def run_in_colab(func):
    """Decorator to ensure function runs only in Colab environment"""
    def wrapper(*args, **kwargs):
        try:
            import google.colab
            return func(*args, **kwargs)
        except ImportError:
            logger.warning(f"{func.__name__} can only run in Google Colab environment")
            return None
    return wrapper

@run_in_colab
def mount_drive():
    """Mount Google Drive in Colab"""
    from google.colab import drive
    drive.mount('/content/drive')
    logger.info("Google Drive mounted successfully")

@run_in_colab
def get_colab_secret(secret_name: str) -> Optional[str]:
    """Get secret from Colab secrets"""
    try:
        from google.colab import userdata
        return userdata.get(secret_name)
    except Exception as e:
        logger.error(f"Failed to get secret {secret_name}: {e}")
        return None

@run_in_colab
def setup_colab_gpu():
    """Setup and verify GPU in Colab"""
    import tensorflow as tf
    import torch
    
    gpu_info = {
        'tensorflow_gpus': len(tf.config.list_physical_devices('GPU')),
        'pytorch_cuda': torch.cuda.is_available(),
        'pytorch_device': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        'memory_gb': torch.cuda.get_device_properties(0).total_memory / 1e9 if torch.cuda.is_available() else 0
    }
    
    logger.info(f"GPU Setup: {gpu_info}")
    return gpu_info