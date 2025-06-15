"""
Enterprise Security Layer

Implements security features including rate limiting, API key authentication,
input sanitization, and request validation.
"""

import time
import hashlib
import secrets
import re
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging
from functools import wraps
from flask import request, jsonify, g
from src.config import get_config


logger = logging.getLogger(__name__)


@dataclass
class RateLimitInfo:
    """Rate limit information for a client"""
    requests: deque
    last_reset: datetime
    blocked_until: Optional[datetime] = None


class SecurityManager:
    """Manages all security aspects of the application"""
    
    def __init__(self):
        self.config = get_config()
        self.rate_limiters: Dict[str, RateLimitInfo] = {}
        self.api_keys: Dict[str, Dict[str, Any]] = {}
        self.blocked_ips: set = set()
        self.suspicious_patterns = self._load_suspicious_patterns()
        
        # Initialize with some demo API keys in non-production
        if self.config.environment.value != "production":
            self._initialize_demo_keys()
    
    def _initialize_demo_keys(self):
        """Initialize demo API keys for testing"""
        demo_keys = [
            {
                "key": "demo-key-001",
                "name": "Demo User 1",
                "tier": "basic",
                "rate_limit_multiplier": 1.0
            },
            {
                "key": "demo-key-002",
                "name": "Demo User 2",
                "tier": "premium",
                "rate_limit_multiplier": 2.0
            },
            {
                "key": "demo-key-admin",
                "name": "Demo Admin",
                "tier": "admin",
                "rate_limit_multiplier": 10.0
            }
        ]
        
        for key_info in demo_keys:
            hashed_key = self._hash_api_key(key_info["key"])
            self.api_keys[hashed_key] = {
                "name": key_info["name"],
                "tier": key_info["tier"],
                "rate_limit_multiplier": key_info["rate_limit_multiplier"],
                "created_at": datetime.now(),
                "last_used": None,
                "usage_count": 0
            }
    
    def _hash_api_key(self, key: str) -> str:
        """Hash API key for secure storage"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def _load_suspicious_patterns(self) -> list:
        """Load patterns that might indicate malicious input"""
        return [
            # SQL injection patterns
            r"('|(\-\-)|(;)|(\|\|)|(\/\*)|(\*\/))",
            r"(union|select|insert|update|delete|drop|create|alter|exec|execute)\s",
            
            # XSS patterns
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"onerror\s*=",
            r"onload\s*=",
            
            # Command injection patterns
            r"(\||&|;|\$|>|<|`|\\|\").*?(cat|ls|echo|nc|sh|bash)",
            
            # Path traversal
            r"\.\.[\\/]",
            
            # Excessive special characters
            r"[^\w\s]{20,}"
        ]
    
    def validate_api_key(self, api_key: Optional[str]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Validate API key and return key info if valid"""
        if not self.config.security.enable_api_key_auth:
            return True, None
        
        if not api_key:
            return False, None
        
        hashed_key = self._hash_api_key(api_key)
        key_info = self.api_keys.get(hashed_key)
        
        if key_info:
            # Update usage stats
            key_info["last_used"] = datetime.now()
            key_info["usage_count"] += 1
            return True, key_info
        
        return False, None
    
    def check_rate_limit(self, identifier: str, multiplier: float = 1.0) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Check if request is within rate limits"""
        if not self.config.security.enable_rate_limiting:
            return True, None
        
        now = datetime.now()
        
        # Get or create rate limiter for this identifier
        if identifier not in self.rate_limiters:
            self.rate_limiters[identifier] = RateLimitInfo(
                requests=deque(),
                last_reset=now
            )
        
        limiter = self.rate_limiters[identifier]
        
        # Check if currently blocked
        if limiter.blocked_until and now < limiter.blocked_until:
            remaining_seconds = (limiter.blocked_until - now).total_seconds()
            return False, {
                "reason": "rate_limit_exceeded",
                "retry_after": int(remaining_seconds),
                "message": f"Rate limit exceeded. Try again in {int(remaining_seconds)} seconds."
            }
        
        # Clear old requests (outside the window)
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        
        # Remove requests older than an hour
        while limiter.requests and limiter.requests[0] < hour_ago:
            limiter.requests.popleft()
        
        # Count requests in different windows
        minute_requests = sum(1 for req_time in limiter.requests if req_time > minute_ago)
        hour_requests = len(limiter.requests)
        
        # Apply multiplier to limits
        minute_limit = int(self.config.security.rate_limit_per_minute * multiplier)
        hour_limit = int(self.config.security.rate_limit_per_hour * multiplier)
        
        # Check limits
        if minute_requests >= minute_limit:
            # Block for increasing durations on repeated violations
            violation_count = getattr(limiter, 'violation_count', 0) + 1
            limiter.violation_count = violation_count
            block_duration = min(60 * violation_count, 3600)  # Max 1 hour
            limiter.blocked_until = now + timedelta(seconds=block_duration)
            
            return False, {
                "reason": "rate_limit_exceeded",
                "retry_after": block_duration,
                "message": f"Rate limit exceeded. Blocked for {block_duration} seconds."
            }
        
        if hour_requests >= hour_limit:
            return False, {
                "reason": "hourly_limit_exceeded",
                "retry_after": 3600,
                "message": "Hourly rate limit exceeded."
            }
        
        # Add current request
        limiter.requests.append(now)
        
        # Reset violation count on successful request
        if hasattr(limiter, 'violation_count'):
            limiter.violation_count = 0
        
        return True, {
            "requests_remaining": {
                "minute": minute_limit - minute_requests - 1,
                "hour": hour_limit - hour_requests - 1
            }
        }
    
    def sanitize_input(self, input_text: str) -> Tuple[str, list]:
        """Sanitize input and return cleaned text with warnings"""
        if not self.config.security.enable_input_sanitization:
            return input_text, []
        
        warnings = []
        cleaned = input_text
        
        # Check length
        if len(cleaned) > self.config.security.max_prompt_length:
            cleaned = cleaned[:self.config.security.max_prompt_length]
            warnings.append(f"Input truncated to {self.config.security.max_prompt_length} characters")
        
        # Check for suspicious patterns
        for pattern in self.suspicious_patterns:
            if re.search(pattern, cleaned, re.IGNORECASE):
                warnings.append(f"Suspicious pattern detected and neutralized")
                # Replace suspicious content with safe placeholder
                cleaned = re.sub(pattern, "[REDACTED]", cleaned, flags=re.IGNORECASE)
        
        # Remove null bytes and other control characters
        cleaned = ''.join(char for char in cleaned if char.isprintable() or char.isspace())
        
        # Normalize whitespace
        cleaned = ' '.join(cleaned.split())
        
        return cleaned, warnings
    
    def validate_request(self, request_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate request structure and content"""
        # Check required fields
        if 'prompt' not in request_data:
            return False, "Missing required field: prompt"
        
        # Check data types
        if not isinstance(request_data.get('prompt'), str):
            return False, "Invalid data type for prompt"
        
        # Check for empty prompt
        if not request_data['prompt'].strip():
            return False, "Prompt cannot be empty"
        
        # Validate optional fields
        optional_fields = {
            'type': str,
            'theme': str,
            'depth': (str, int),
            'mode': str,
            'strategy': str,
            'focus_theme': str,
            'intensity': str,
            'structure': str,
            'complexity': str
        }
        
        for field, expected_type in optional_fields.items():
            if field in request_data:
                value = request_data[field]
                if isinstance(expected_type, tuple):
                    if not any(isinstance(value, t) for t in expected_type):
                        return False, f"Invalid data type for {field}"
                else:
                    if not isinstance(value, expected_type):
                        return False, f"Invalid data type for {field}"
        
        return True, None
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security-related events"""
        logger.warning(f"Security event: {event_type}", extra={
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_api_key(self, name: str, tier: str = "basic") -> str:
        """Generate a new API key"""
        # Generate secure random key
        key = f"{tier}-{secrets.token_urlsafe(32)}"
        hashed_key = self._hash_api_key(key)
        
        # Store key info
        rate_multiplier = {
            "basic": 1.0,
            "premium": 2.0,
            "enterprise": 5.0,
            "admin": 10.0
        }.get(tier, 1.0)
        
        self.api_keys[hashed_key] = {
            "name": name,
            "tier": tier,
            "rate_limit_multiplier": rate_multiplier,
            "created_at": datetime.now(),
            "last_used": None,
            "usage_count": 0
        }
        
        return key
    
    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key"""
        hashed_key = self._hash_api_key(api_key)
        if hashed_key in self.api_keys:
            del self.api_keys[hashed_key]
            return True
        return False
    
    def block_ip(self, ip_address: str, duration_seconds: int = 3600):
        """Block an IP address temporarily"""
        self.blocked_ips.add(ip_address)
        # In production, this would persist to a database/cache
        # and schedule unblocking
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP is blocked"""
        return ip_address in self.blocked_ips
    
    def get_client_identifier(self, request) -> str:
        """Get unique identifier for the client"""
        # Use API key if available
        api_key = request.headers.get(self.config.security.api_key_header)
        if api_key:
            return f"key:{self._hash_api_key(api_key)}"
        
        # Otherwise use IP address
        return f"ip:{request.remote_addr}"


# Global security manager instance
_security_manager: Optional[SecurityManager] = None


def get_security_manager() -> SecurityManager:
    """Get global security manager instance"""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager


# Flask decorators for security
def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        config = get_config()
        if not config.security.enable_api_key_auth:
            return f(*args, **kwargs)
        
        security = get_security_manager()
        api_key = request.headers.get(config.security.api_key_header)
        
        valid, key_info = security.validate_api_key(api_key)
        if not valid:
            security.log_security_event("invalid_api_key", {
                "ip": request.remote_addr,
                "path": request.path
            })
            return jsonify({
                "success": False,
                "error": "Invalid or missing API key"
            }), 401
        
        # Store key info in request context
        g.api_key_info = key_info
        return f(*args, **kwargs)
    
    return decorated_function


def rate_limit(f):
    """Decorator to apply rate limiting"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        config = get_config()
        if not config.security.enable_rate_limiting:
            return f(*args, **kwargs)
        
        security = get_security_manager()
        
        # Check if IP is blocked
        if security.is_ip_blocked(request.remote_addr):
            return jsonify({
                "success": False,
                "error": "Access denied"
            }), 403
        
        # Get client identifier and rate limit multiplier
        identifier = security.get_client_identifier(request)
        multiplier = 1.0
        if hasattr(g, 'api_key_info') and g.api_key_info:
            multiplier = g.api_key_info.get('rate_limit_multiplier', 1.0)
        
        # Check rate limit
        allowed, limit_info = security.check_rate_limit(identifier, multiplier)
        
        if not allowed:
            security.log_security_event("rate_limit_exceeded", {
                "identifier": identifier,
                "info": limit_info
            })
            return jsonify({
                "success": False,
                "error": limit_info["message"],
                "retry_after": limit_info["retry_after"]
            }), 429
        
        # Execute the function
        response = f(*args, **kwargs)
        
        # Add rate limit headers if we have limit info
        if limit_info and "requests_remaining" in limit_info:
            from flask import make_response
            
            # Convert to response object if it's not already
            if not hasattr(response, 'headers'):
                response = make_response(response)
            
            response.headers["X-RateLimit-Remaining-Minute"] = str(
                limit_info["requests_remaining"]["minute"]
            )
            response.headers["X-RateLimit-Remaining-Hour"] = str(
                limit_info["requests_remaining"]["hour"]
            )
        
        return response
    
    return decorated_function


def sanitize_inputs(f):
    """Decorator to sanitize request inputs"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        config = get_config()
        if not config.security.enable_input_sanitization:
            return f(*args, **kwargs)
        
        security = get_security_manager()
        
        if request.method == "POST" and request.is_json:
            # Fix for Werkzeug bug - use direct JSON parsing
            try:
                import json
                data = json.loads(request.data) if request.data else {}
            except:
                data = {}
            
            # Validate request structure
            valid, error = security.validate_request(data)
            if not valid:
                return jsonify({
                    "success": False,
                    "error": error
                }), 400
            
            # Sanitize prompt
            if "prompt" in data:
                cleaned_prompt, warnings = security.sanitize_input(data["prompt"])
                data["prompt"] = cleaned_prompt
                
                if warnings:
                    security.log_security_event("input_sanitized", {
                        "warnings": warnings,
                        "ip": request.remote_addr
                    })
                
                # Store sanitized data back in request
                request._cached_json = data
                request._cached_data = data
        
        return f(*args, **kwargs)
    
    return decorated_function


def secure_endpoint(f):
    """Combined decorator for all security features"""
    @require_api_key
    @rate_limit
    @sanitize_inputs
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    
    return decorated_function