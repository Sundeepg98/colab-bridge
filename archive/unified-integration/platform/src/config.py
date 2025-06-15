"""
Enterprise Configuration Management

Centralized configuration for all system components with environment-based settings.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import logging
from datetime import timedelta


class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


@dataclass
class SecurityConfig:
    """Security configuration settings"""
    enable_rate_limiting: bool = True
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    enable_input_sanitization: bool = True
    max_prompt_length: int = 5000
    enable_content_filtering: bool = True
    blocked_patterns: list = None
    enable_api_key_auth: bool = True
    api_key_header: str = "X-API-Key"
    enable_cors: bool = True
    cors_origins: list = None
    enable_https_only: bool = True
    session_timeout: timedelta = timedelta(hours=24)
    
    def __post_init__(self):
        if self.blocked_patterns is None:
            self.blocked_patterns = []
        if self.cors_origins is None:
            self.cors_origins = ["*"] if os.getenv("ENVIRONMENT") == "development" else []


@dataclass
class PerformanceConfig:
    """Performance and optimization settings"""
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600
    enable_async_processing: bool = True
    max_workers: int = 4
    enable_request_queuing: bool = True
    queue_max_size: int = 1000
    enable_response_compression: bool = True
    enable_connection_pooling: bool = True
    pool_size: int = 10
    request_timeout_seconds: int = 300
    enable_batch_processing: bool = True
    batch_size: int = 10


@dataclass
class MonitoringConfig:
    """Monitoring and observability settings"""
    enable_metrics: bool = True
    metrics_port: int = 9090
    enable_logging: bool = True
    log_level: str = "INFO"
    log_format: str = "json"
    enable_tracing: bool = True
    trace_sample_rate: float = 0.1
    enable_health_checks: bool = True
    health_check_interval_seconds: int = 60
    enable_error_tracking: bool = True
    error_tracking_dsn: Optional[str] = None
    enable_audit_logging: bool = True
    audit_log_retention_days: int = 90


@dataclass
class AIConfig:
    """AI model and processing settings"""
    claude_api_key: Optional[str] = None
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_max_tokens: int = 4096
    claude_temperature: float = 0.7
    enable_fallback_models: bool = True
    fallback_timeout_seconds: int = 30
    enable_prompt_caching: bool = True
    cache_similar_threshold: float = 0.85
    enable_learning_system: bool = True
    learning_batch_size: int = 100
    enable_quality_scoring: bool = True
    min_quality_threshold: float = 0.7


@dataclass
class DatabaseConfig:
    """Database configuration"""
    enable_database: bool = True
    database_url: Optional[str] = None
    pool_size: int = 5
    max_overflow: int = 10
    enable_migrations: bool = True
    enable_backups: bool = True
    backup_interval_hours: int = 24
    enable_read_replicas: bool = False
    replica_urls: list = None
    
    def __post_init__(self):
        if self.replica_urls is None:
            self.replica_urls = []


class Config:
    """Main configuration class"""
    
    def __init__(self, environment: Optional[str] = None):
        self.environment = Environment(
            environment or os.getenv("ENVIRONMENT", "development")
        )
        
        # Load base configuration
        self.security = SecurityConfig()
        self.performance = PerformanceConfig()
        self.monitoring = MonitoringConfig()
        self.ai = AIConfig()
        self.database = DatabaseConfig()
        
        # Load environment-specific overrides
        self._load_environment_config()
        
        # Load from environment variables
        self._load_from_env()
        
        # Validate configuration
        self._validate()
    
    def _load_environment_config(self):
        """Load environment-specific configuration"""
        if self.environment == Environment.PRODUCTION:
            # Production settings
            self.security.enable_https_only = True
            self.security.enable_api_key_auth = True
            self.security.cors_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
            self.performance.enable_caching = True
            self.monitoring.log_level = "WARNING"
            self.monitoring.trace_sample_rate = 0.01
            
        elif self.environment == Environment.DEVELOPMENT:
            # Development settings
            self.security.enable_https_only = False
            self.security.enable_api_key_auth = False
            self.security.cors_origins = ["*"]
            self.monitoring.log_level = "DEBUG"
            self.monitoring.trace_sample_rate = 1.0
            
        elif self.environment == Environment.TESTING:
            # Testing settings
            self.security.enable_rate_limiting = False
            self.performance.enable_caching = False
            self.monitoring.enable_metrics = False
            self.database.database_url = "sqlite:///:memory:"
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Security
        self.security.enable_rate_limiting = self._get_bool_env(
            "ENABLE_RATE_LIMITING", self.security.enable_rate_limiting
        )
        self.security.rate_limit_per_minute = self._get_int_env(
            "RATE_LIMIT_PER_MINUTE", self.security.rate_limit_per_minute
        )
        
        # Performance
        self.performance.enable_caching = self._get_bool_env(
            "ENABLE_CACHING", self.performance.enable_caching
        )
        self.performance.max_workers = self._get_int_env(
            "MAX_WORKERS", self.performance.max_workers
        )
        
        # Monitoring
        self.monitoring.log_level = os.getenv(
            "LOG_LEVEL", self.monitoring.log_level
        )
        self.monitoring.error_tracking_dsn = os.getenv(
            "ERROR_TRACKING_DSN", self.monitoring.error_tracking_dsn
        )
        
        # AI
        self.ai.claude_api_key = os.getenv(
            "ANTHROPIC_API_KEY", self.ai.claude_api_key
        )
        self.ai.claude_model = os.getenv(
            "CLAUDE_MODEL", self.ai.claude_model
        )
        
        # Database
        self.database.database_url = os.getenv(
            "DATABASE_URL", 
            self.database.database_url or "postgresql://localhost/ai_integration_platform"
        )
    
    def _get_bool_env(self, key: str, default: bool) -> bool:
        """Get boolean from environment variable"""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")
    
    def _get_int_env(self, key: str, default: int) -> int:
        """Get integer from environment variable"""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            logging.warning(f"Invalid integer value for {key}: {value}")
            return default
    
    def _validate(self):
        """Validate configuration"""
        # Check required settings
        if self.environment == Environment.PRODUCTION:
            if not self.ai.claude_api_key:
                raise ValueError("ANTHROPIC_API_KEY is required in production")
            
            if not self.monitoring.error_tracking_dsn:
                logging.warning("Error tracking DSN not configured for production")
            
            if self.security.cors_origins == ["*"]:
                raise ValueError("CORS origins cannot be '*' in production")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "environment": self.environment.value,
            "security": self.security.__dict__,
            "performance": self.performance.__dict__,
            "monitoring": self.monitoring.__dict__,
            "ai": {k: v for k, v in self.ai.__dict__.items() if k != "claude_api_key"},
            "database": {k: v for k, v in self.database.__dict__.items() if "url" not in k}
        }
    
    def get_safe_config(self) -> Dict[str, Any]:
        """Get configuration safe for client exposure"""
        return {
            "environment": self.environment.value,
            "features": {
                "rate_limiting": self.security.enable_rate_limiting,
                "caching": self.performance.enable_caching,
                "async_processing": self.performance.enable_async_processing,
                "learning_system": self.ai.enable_learning_system,
            },
            "limits": {
                "max_prompt_length": self.security.max_prompt_length,
                "rate_limit_per_minute": self.security.rate_limit_per_minute,
                "request_timeout_seconds": self.performance.request_timeout_seconds,
            }
        }


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config(environment: Optional[str] = None):
    """Reload configuration with optional environment override"""
    global _config
    _config = Config(environment)
    return _config