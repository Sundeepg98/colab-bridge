"""
Database models for the AI platform authentication and tracking system.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class ServiceType(enum.Enum):
    """Supported AI service types."""
    CLAUDE = "claude"
    OPENAI = "openai"
    GEMINI = "gemini"
    LLAMA = "llama"
    CUSTOM = "custom"


class BillingStatus(enum.Enum):
    """Billing status types."""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class User(Base):
    """User model for authentication and account management."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Additional fields for enhanced security and functionality
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String(255), unique=True, nullable=True)
    reset_token = Column(String(255), unique=True, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    
    # Relationships
    integrations = relationship("UserIntegration", back_populates="user", cascade="all, delete-orphan")
    usage_tracking = relationship("UsageTracking", back_populates="user", cascade="all, delete-orphan")
    billing = relationship("Billing", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_active={self.is_active})>"


class UserIntegration(Base):
    """User's API integrations with various AI services."""
    __tablename__ = 'user_integrations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    service_name = Column(String(50), nullable=False)
    api_key_encrypted = Column(Text, nullable=False)  # Encrypted API key
    status = Column(String(50), default='active', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Additional fields for integration management
    display_name = Column(String(255), nullable=True)  # User-friendly name
    endpoint_url = Column(String(500), nullable=True)  # Custom endpoint URL
    rate_limit = Column(Integer, nullable=True)  # Rate limit per minute
    monthly_quota = Column(Integer, nullable=True)  # Monthly token/credit quota
    current_usage = Column(Integer, default=0, nullable=False)  # Current month usage
    last_used = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="integrations")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_service', 'user_id', 'service_name'),
        Index('idx_status', 'status'),
    )
    
    def __repr__(self):
        return f"<UserIntegration(id={self.id}, user_id={self.user_id}, service='{self.service_name}')>"


class UsageTracking(Base):
    """Track API usage for billing and analytics."""
    __tablename__ = 'usage_tracking'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    service = Column(String(50), nullable=False)
    tokens_used = Column(Integer, default=0, nullable=False)
    credits_used = Column(Float, default=0.0, nullable=False)
    cost = Column(Float, default=0.0, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Additional tracking fields
    request_id = Column(String(255), unique=True, nullable=True)  # Unique request identifier
    model_name = Column(String(100), nullable=True)  # Specific model used
    request_type = Column(String(50), nullable=True)  # completion, chat, embedding, etc.
    response_time_ms = Column(Integer, nullable=True)  # Response time in milliseconds
    status_code = Column(Integer, nullable=True)  # HTTP status code
    error_message = Column(Text, nullable=True)  # Error details if any
    request_metadata = Column(Text, nullable=True)  # JSON metadata for additional info
    
    # Relationships
    user = relationship("User", back_populates="usage_tracking")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_service_timestamp', 'service', 'timestamp'),
        Index('idx_user_service_timestamp', 'user_id', 'service', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<UsageTracking(id={self.id}, user_id={self.user_id}, service='{self.service}', cost={self.cost})>"


class Billing(Base):
    """Billing records for users."""
    __tablename__ = 'billing'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), default='pending', nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Additional billing fields
    invoice_number = Column(String(100), unique=True, nullable=True)
    payment_method = Column(String(50), nullable=True)  # card, paypal, crypto, etc.
    transaction_id = Column(String(255), unique=True, nullable=True)
    currency = Column(String(3), default='USD', nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, nullable=False)  # amount + tax - discount
    due_date = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    payment_details = Column(Text, nullable=True)  # JSON for additional payment info
    notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="billing")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_period', 'user_id', 'period_start', 'period_end'),
        Index('idx_status_due', 'status', 'due_date'),
    )
    
    def __repr__(self):
        return f"<Billing(id={self.id}, user_id={self.user_id}, amount={self.total_amount}, status='{self.status}')>"


class UserSession(Base):
    """Track user sessions for security and analytics."""
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String(45), nullable=True)  # Support IPv6
    user_agent = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_active', 'user_id', 'is_active'),
        Index('idx_expires', 'expires_at'),
    )
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, is_active={self.is_active})>"