"""
Encryption utilities for secure storage of API keys and sensitive data.
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets


class EncryptionManager:
    """Manages encryption and decryption of sensitive data."""
    
    def __init__(self, master_key: str = None):
        """
        Initialize encryption manager with master key.
        
        Args:
            master_key: Master encryption key. If not provided, uses environment variable.
        """
        if master_key is None:
            master_key = os.environ.get('ENCRYPTION_MASTER_KEY')
            
        if not master_key:
            # Generate a new key if none exists (for development only)
            master_key = secrets.token_urlsafe(32)
            print(f"WARNING: Generated new master key. Save this for production: {master_key}")
        
        self.fernet = self._create_fernet(master_key)
    
    def _create_fernet(self, master_key: str) -> Fernet:
        """Create Fernet instance from master key."""
        # Derive a proper key from the master key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'ai-platform-salt',  # In production, use a random salt per user
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(master_key.encode())
        )
        return Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt a string.
        
        Args:
            data: String to encrypt
            
        Returns:
            Base64 encoded encrypted string
        """
        if not data:
            return ""
        
        encrypted = self.fernet.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt an encrypted string.
        
        Args:
            encrypted_data: Base64 encoded encrypted string
            
        Returns:
            Decrypted string
        """
        if not encrypted_data:
            return ""
        
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.fernet.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure API key."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """
        Create a hash of an API key for lookup purposes.
        
        Args:
            api_key: API key to hash
            
        Returns:
            SHA-256 hash of the API key
        """
        import hashlib
        return hashlib.sha256(api_key.encode()).hexdigest()


# Global encryption manager instance
encryption_manager = EncryptionManager()


# Utility functions for easy access
def encrypt_api_key(api_key: str) -> str:
    """Encrypt an API key for storage."""
    return encryption_manager.encrypt(api_key)


def decrypt_api_key(encrypted_api_key: str) -> str:
    """Decrypt an API key from storage."""
    return encryption_manager.decrypt(encrypted_api_key)


def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(length)


# Example usage in models
"""
from src.auth.encryption import encrypt_api_key, decrypt_api_key

# When storing an API key
user_integration.api_key_encrypted = encrypt_api_key(api_key)

# When retrieving an API key
api_key = decrypt_api_key(user_integration.api_key_encrypted)
"""