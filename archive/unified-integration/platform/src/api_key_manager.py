"""
Secure API Key Management System
Handles storage, validation, and management of 3rd party API keys
"""

import os
import json
import logging
from typing import Dict, Optional, List, Any
from datetime import datetime
from cryptography.fernet import Fernet
from pathlib import Path
import threading
import time

logger = logging.getLogger(__name__)


class APIKeyManager:
    """Manages API keys for all integrations with encryption and validation"""
    
    def __init__(self, storage_path: str = "/var/projects/ai-integration-platform/secure_keys"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True, parents=True)
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        self.api_keys: Dict[str, Dict[str, Any]] = {}
        self.validation_cache: Dict[str, Dict[str, Any]] = {}
        self._load_api_keys()
        
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for API key storage"""
        key_file = self.storage_path / ".encryption_key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            # Set restrictive permissions
            os.chmod(key_file, 0o600)
            return key
    
    def _load_api_keys(self):
        """Load encrypted API keys from storage"""
        keys_file = self.storage_path / "api_keys.enc"
        
        if keys_file.exists():
            try:
                with open(keys_file, 'rb') as f:
                    encrypted_data = f.read()
                
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self.api_keys = json.loads(decrypted_data.decode())
                logger.info(f"Loaded {len(self.api_keys)} API key configurations")
            except Exception as e:
                logger.error(f"Failed to load API keys: {e}")
                self.api_keys = {}
    
    def _save_api_keys(self):
        """Save encrypted API keys to storage"""
        try:
            keys_file = self.storage_path / "api_keys.enc"
            
            # Encrypt the data
            data = json.dumps(self.api_keys).encode()
            encrypted_data = self.cipher.encrypt(data)
            
            # Save to file
            with open(keys_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Set restrictive permissions
            os.chmod(keys_file, 0o600)
            logger.info("API keys saved securely")
            
        except Exception as e:
            logger.error(f"Failed to save API keys: {e}")
    
    def add_or_update_key(self, integration_name: str, key_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add or update an API key for an integration"""
        try:
            # Validate key data
            if 'api_key' not in key_data:
                return {'success': False, 'error': 'API key is required'}
            
            # Store key configuration
            self.api_keys[integration_name] = {
                'api_key': key_data['api_key'],
                'base_url': key_data.get('base_url'),
                'models': key_data.get('models', []),
                'enabled': key_data.get('enabled', True),
                'added_at': datetime.now().isoformat(),
                'last_validated': None,
                'validation_status': 'pending',
                'metadata': key_data.get('metadata', {})
            }
            
            # Save to disk
            self._save_api_keys()
            
            # Clear validation cache
            if integration_name in self.validation_cache:
                del self.validation_cache[integration_name]
            
            return {
                'success': True,
                'message': f'API key for {integration_name} saved successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to add/update API key: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_key(self, integration_name: str) -> Optional[str]:
        """Get decrypted API key for an integration"""
        if integration_name in self.api_keys:
            key_data = self.api_keys[integration_name]
            if key_data.get('enabled', True):
                return key_data.get('api_key')
        return None
    
    def get_all_keys_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all API keys (without exposing actual keys)"""
        result = {}
        
        for name, data in self.api_keys.items():
            result[name] = {
                'enabled': data.get('enabled', True),
                'added_at': data.get('added_at'),
                'last_validated': data.get('last_validated'),
                'validation_status': data.get('validation_status', 'unknown'),
                'models': data.get('models', []),
                'has_key': bool(data.get('api_key')),
                'key_preview': self._mask_key(data.get('api_key', ''))
            }
        
        return result
    
    def _mask_key(self, key: str) -> str:
        """Mask API key for display"""
        if not key:
            return 'Not Set'
        if len(key) < 8:
            return '***'
        return f"{key[:4]}...{key[-4:]}"
    
    def validate_key(self, integration_name: str) -> Dict[str, Any]:
        """Validate an API key by testing it"""
        if integration_name not in self.api_keys:
            return {
                'valid': False,
                'error': 'Integration not found',
                'status': 'not_configured'
            }
        
        # Check cache first
        if integration_name in self.validation_cache:
            cached = self.validation_cache[integration_name]
            if datetime.now().timestamp() - cached['timestamp'] < 300:  # 5 minute cache
                return cached['result']
        
        # Perform validation based on integration type
        key_data = self.api_keys[integration_name]
        api_key = key_data.get('api_key')
        
        if not api_key:
            result = {
                'valid': False,
                'error': 'No API key configured',
                'status': 'missing_key'
            }
        else:
            result = self._test_api_key(integration_name, api_key, key_data)
        
        # Update validation status
        self.api_keys[integration_name]['last_validated'] = datetime.now().isoformat()
        self.api_keys[integration_name]['validation_status'] = result['status']
        self._save_api_keys()
        
        # Cache result
        self.validation_cache[integration_name] = {
            'result': result,
            'timestamp': datetime.now().timestamp()
        }
        
        return result
    
    def _test_api_key(self, integration_name: str, api_key: str, key_data: Dict) -> Dict[str, Any]:
        """Test API key with actual API call"""
        try:
            if integration_name == 'claude' or integration_name == 'anthropic':
                return self._test_claude_key(api_key, key_data)
            elif integration_name == 'openai':
                return self._test_openai_key(api_key, key_data)
            elif integration_name == 'stability' or integration_name == 'stable_diffusion':
                return self._test_stability_key(api_key, key_data)
            elif integration_name == 'replicate':
                return self._test_replicate_key(api_key, key_data)
            else:
                return {
                    'valid': True,
                    'status': 'assumed_valid',
                    'message': f'Validation not implemented for {integration_name}'
                }
                
        except Exception as e:
            logger.error(f"API key validation failed for {integration_name}: {e}")
            return {
                'valid': False,
                'error': str(e),
                'status': 'error'
            }
    
    def _test_claude_key(self, api_key: str, key_data: Dict) -> Dict[str, Any]:
        """Test Claude/Anthropic API key"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            # Test with minimal API call
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=5,
                messages=[{"role": "user", "content": "Hi"}]
            )
            
            return {
                'valid': True,
                'status': 'active',
                'message': 'Claude API key is valid',
                'model_tested': 'claude-3-haiku-20240307'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'status': 'invalid'
            }
    
    def _test_openai_key(self, api_key: str, key_data: Dict) -> Dict[str, Any]:
        """Test OpenAI API key"""
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            
            # Test with minimal API call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            
            return {
                'valid': True,
                'status': 'active',
                'message': 'OpenAI API key is valid',
                'model_tested': 'gpt-3.5-turbo'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'status': 'invalid'
            }
    
    def _test_stability_key(self, api_key: str, key_data: Dict) -> Dict[str, Any]:
        """Test Stability AI API key"""
        try:
            import requests
            
            # Test with account info endpoint
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Accept': 'application/json'
            }
            
            response = requests.get(
                'https://api.stability.ai/v1/user/account',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'valid': True,
                    'status': 'active',
                    'message': 'Stability API key is valid',
                    'credits': response.json().get('credits', 'unknown')
                }
            else:
                return {
                    'valid': False,
                    'error': f'API returned status {response.status_code}',
                    'status': 'invalid'
                }
                
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'status': 'error'
            }
    
    def _test_replicate_key(self, api_key: str, key_data: Dict) -> Dict[str, Any]:
        """Test Replicate API key"""
        try:
            import requests
            
            headers = {
                'Authorization': f'Token {api_key}',
                'Content-Type': 'application/json'
            }
            
            # Test with account endpoint
            response = requests.get(
                'https://api.replicate.com/v1/account',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'valid': True,
                    'status': 'active',
                    'message': 'Replicate API key is valid'
                }
            else:
                return {
                    'valid': False,
                    'error': f'API returned status {response.status_code}',
                    'status': 'invalid'
                }
                
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'status': 'error'
            }
    
    def remove_key(self, integration_name: str) -> Dict[str, Any]:
        """Remove an API key"""
        if integration_name in self.api_keys:
            del self.api_keys[integration_name]
            self._save_api_keys()
            
            # Clear from cache
            if integration_name in self.validation_cache:
                del self.validation_cache[integration_name]
            
            return {
                'success': True,
                'message': f'API key for {integration_name} removed'
            }
        
        return {
            'success': False,
            'error': 'Integration not found'
        }
    
    def enable_disable_key(self, integration_name: str, enabled: bool) -> Dict[str, Any]:
        """Enable or disable an API key"""
        if integration_name in self.api_keys:
            self.api_keys[integration_name]['enabled'] = enabled
            self._save_api_keys()
            
            return {
                'success': True,
                'message': f'API key for {integration_name} {"enabled" if enabled else "disabled"}'
            }
        
        return {
            'success': False,
            'error': 'Integration not found'
        }
    
    def get_integration_config(self, integration_name: str) -> Optional[Dict[str, Any]]:
        """Get full configuration for an integration"""
        if integration_name in self.api_keys:
            config = self.api_keys[integration_name].copy()
            # Don't expose the actual key
            if 'api_key' in config:
                config['api_key'] = self._mask_key(config['api_key'])
            return config
        return None
    
    def export_config(self, include_keys: bool = False) -> Dict[str, Any]:
        """Export configuration (optionally without keys)"""
        export_data = {}
        
        for name, data in self.api_keys.items():
            export_data[name] = data.copy()
            if not include_keys and 'api_key' in export_data[name]:
                export_data[name]['api_key'] = self._mask_key(data['api_key'])
        
        return {
            'exported_at': datetime.now().isoformat(),
            'integrations': export_data,
            'keys_included': include_keys
        }


# Global instance
_api_key_manager: Optional[APIKeyManager] = None


def get_api_key_manager() -> APIKeyManager:
    """Get global API key manager instance"""
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = APIKeyManager()
    return _api_key_manager