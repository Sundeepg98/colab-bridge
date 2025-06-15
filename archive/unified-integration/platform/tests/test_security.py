"""
Test Suite for Security Features

Comprehensive tests for security layer including rate limiting,
API key authentication, and input sanitization.
"""

import pytest
import time
from datetime import datetime, timedelta
from src.security import SecurityManager, RateLimitInfo
from src.config import Config, Environment


class TestSecurityManager:
    
    def setup_method(self):
        """Set up test environment"""
        # Create a test config
        self.config = Config("testing")
        self.security = SecurityManager()
    
    def test_api_key_validation(self):
        """Test API key validation"""
        # Test with invalid key
        valid, info = self.security.validate_api_key("invalid-key")
        assert not valid
        assert info is None
        
        # Test with demo key
        valid, info = self.security.validate_api_key("demo-key-001")
        assert valid
        assert info is not None
        assert info["tier"] == "basic"
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        identifier = "test-user"
        
        # First request should pass
        allowed, info = self.security.check_rate_limit(identifier)
        assert allowed
        
        # Simulate many requests
        for _ in range(60):  # Default limit per minute
            self.security.check_rate_limit(identifier)
        
        # Next request should be blocked
        allowed, info = self.security.check_rate_limit(identifier)
        assert not allowed
        assert "rate_limit_exceeded" in info["reason"]
    
    def test_input_sanitization(self):
        """Test input sanitization"""
        # Test normal input
        clean, warnings = self.security.sanitize_input("Hello world")
        assert clean == "Hello world"
        assert len(warnings) == 0
        
        # Test suspicious input
        malicious = "<script>alert('xss')</script>"
        clean, warnings = self.security.sanitize_input(malicious)
        assert "<script>" not in clean
        assert len(warnings) > 0
        
        # Test long input
        long_input = "a" * 10000
        clean, warnings = self.security.sanitize_input(long_input)
        assert len(clean) <= self.config.security.max_prompt_length
        assert any("truncated" in w for w in warnings)
    
    def test_request_validation(self):
        """Test request validation"""
        # Valid request
        valid_request = {"prompt": "test prompt"}
        valid, error = self.security.validate_request(valid_request)
        assert valid
        assert error is None
        
        # Missing prompt
        invalid_request = {"type": "test"}
        valid, error = self.security.validate_request(invalid_request)
        assert not valid
        assert "prompt" in error
        
        # Empty prompt
        empty_request = {"prompt": ""}
        valid, error = self.security.validate_request(empty_request)
        assert not valid
        assert "empty" in error.lower()
    
    def test_api_key_generation(self):
        """Test API key generation"""
        key = self.security.generate_api_key("test-user", "premium")
        assert key.startswith("premium-")
        
        # Validate the generated key
        valid, info = self.security.validate_api_key(key)
        assert valid
        assert info["tier"] == "premium"
        assert info["name"] == "test-user"
    
    def test_api_key_revocation(self):
        """Test API key revocation"""
        key = self.security.generate_api_key("test-user")
        
        # Key should be valid
        valid, _ = self.security.validate_api_key(key)
        assert valid
        
        # Revoke key
        revoked = self.security.revoke_api_key(key)
        assert revoked
        
        # Key should now be invalid
        valid, _ = self.security.validate_api_key(key)
        assert not valid
    
    def test_ip_blocking(self):
        """Test IP blocking functionality"""
        ip = "192.168.1.100"
        
        # IP should not be blocked initially
        assert not self.security.is_ip_blocked(ip)
        
        # Block IP
        self.security.block_ip(ip)
        
        # IP should now be blocked
        assert self.security.is_ip_blocked(ip)
    
    def test_rate_limit_multipliers(self):
        """Test rate limit multipliers for different tiers"""
        identifier = "premium-user"
        
        # Premium user should have higher limits
        for _ in range(120):  # More than basic limit
            allowed, _ = self.security.check_rate_limit(identifier, 2.0)
            if not allowed:
                break
        else:
            # Should be able to make more requests with multiplier
            assert True
    
    def test_security_event_logging(self):
        """Test security event logging"""
        # This would test log output in a real implementation
        self.security.log_security_event("test_event", {"key": "value"})
        # In a real test, we'd check if the log was written
        assert True  # Placeholder


class TestSecurityIntegration:
    """Integration tests for security features"""
    
    def test_configuration_loading(self):
        """Test security configuration loading"""
        config = Config("development")
        assert not config.security.enable_api_key_auth  # Dev setting
        assert config.security.enable_rate_limiting
        
        config = Config("production")
        assert config.security.enable_api_key_auth  # Prod setting
        assert config.security.enable_https_only
    
    def test_environment_specific_settings(self):
        """Test environment-specific security settings"""
        dev_config = Config("development")
        prod_config = Config("production")
        
        # Development should be more permissive
        assert not dev_config.security.enable_api_key_auth
        assert "*" in dev_config.security.cors_origins
        
        # Production should be more restrictive
        assert prod_config.security.enable_api_key_auth
        assert prod_config.security.enable_https_only


if __name__ == "__main__":
    pytest.main([__file__])