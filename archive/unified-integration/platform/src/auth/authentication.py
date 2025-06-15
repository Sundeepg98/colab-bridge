"""
Authentication system with JWT tokens and session management.
"""

import os
import secrets
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from functools import wraps
import bcrypt
from flask import request, jsonify, g
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from ..database.models import User, UserSession
from ..database.db_config import db_config

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get('REFRESH_TOKEN_EXPIRE_DAYS', '7'))
MAX_LOGIN_ATTEMPTS = int(os.environ.get('MAX_LOGIN_ATTEMPTS', '5'))
LOCKOUT_DURATION_MINUTES = int(os.environ.get('LOCKOUT_DURATION_MINUTES', '30'))


class AuthenticationError(Exception):
    """Custom authentication error."""
    pass


class AuthManager:
    """Manages authentication operations."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Create a JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
    
    @staticmethod
    def create_session(db: Session, user_id: int, ip_address: str = None, user_agent: str = None) -> UserSession:
        """Create a new user session."""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Deactivate old sessions
        db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).update({"is_active": False})
        
        # Create new session
        user_session = UserSession(
            user_id=user_id,
            session_token=session_token,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(user_session)
        db.commit()
        
        return user_session
    
    @staticmethod
    def validate_session(db: Session, session_token: str) -> Optional[UserSession]:
        """Validate a session token."""
        session = db.query(UserSession).filter(
            UserSession.session_token == session_token,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow()
        ).first()
        
        if session:
            # Update last activity
            session.last_activity = datetime.utcnow()
            db.commit()
        
        return session
    
    @staticmethod
    def register_user(db: Session, email: str, password: str) -> User:
        """Register a new user."""
        # Validate email format
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        
        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise IntegrityError("User with this email already exists", None, None)
        
        # Create new user
        hashed_password = AuthManager.hash_password(password)
        verification_token = secrets.token_urlsafe(32)
        
        user = User(
            email=email,
            password_hash=hashed_password,
            verification_token=verification_token
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"New user registered: {email}")
        return user
    
    @staticmethod
    def login_user(db: Session, email: str, password: str, ip_address: str = None, user_agent: str = None) -> Dict[str, Any]:
        """Authenticate user and create session."""
        # Find user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise AuthenticationError(f"Account is locked until {user.locked_until}")
        
        # Verify password
        if not AuthManager.verify_password(password, user.password_hash):
            # Increment login attempts
            user.login_attempts += 1
            
            # Lock account if too many attempts
            if user.login_attempts >= MAX_LOGIN_ATTEMPTS:
                user.locked_until = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
                db.commit()
                raise AuthenticationError(f"Account locked due to too many failed attempts")
            
            db.commit()
            raise AuthenticationError("Invalid email or password")
        
        # Check if account is active
        if not user.is_active:
            raise AuthenticationError("Account is deactivated")
        
        # Reset login attempts and update last login
        user.login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        
        # Create session
        session = AuthManager.create_session(db, user.id, ip_address, user_agent)
        
        # Create tokens
        access_token = AuthManager.create_access_token({"sub": str(user.id)})
        refresh_token = AuthManager.create_refresh_token({"sub": str(user.id), "session_id": str(session.id)})
        
        db.commit()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "is_verified": user.is_verified
            }
        }
    
    @staticmethod
    def logout_user(db: Session, user_id: int):
        """Logout user by deactivating all sessions."""
        db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).update({"is_active": False})
        db.commit()
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token."""
        try:
            payload = AuthManager.decode_token(refresh_token)
            
            if payload.get("type") != "refresh":
                raise AuthenticationError("Invalid token type")
            
            user_id = int(payload.get("sub"))
            session_id = payload.get("session_id")
            
            # Validate session
            session = db.query(UserSession).filter(
                UserSession.id == session_id,
                UserSession.user_id == user_id,
                UserSession.is_active == True
            ).first()
            
            if not session:
                raise AuthenticationError("Invalid session")
            
            # Create new access token
            access_token = AuthManager.create_access_token({"sub": str(user_id)})
            
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
            
        except Exception as e:
            raise AuthenticationError(f"Failed to refresh token: {str(e)}")
    
    @staticmethod
    def get_current_user(db: Session, token: str) -> Optional[User]:
        """Get current user from JWT token."""
        try:
            payload = AuthManager.decode_token(token)
            
            if payload.get("type") != "access":
                return None
            
            user_id = payload.get("sub")
            if user_id is None:
                return None
            
            user = db.query(User).filter(
                User.id == int(user_id),
                User.is_active == True
            ).first()
            
            return user
            
        except Exception:
            return None


def login_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401
        
        try:
            # Extract token
            parts = auth_header.split()
            if parts[0].lower() != 'bearer' or len(parts) != 2:
                return jsonify({"error": "Invalid authorization header format"}), 401
            
            token = parts[1]
            
            # Get database session
            with db_config.get_db_session() as db:
                # Get current user
                user = AuthManager.get_current_user(db, token)
                if not user:
                    return jsonify({"error": "Invalid or expired token"}), 401
                
                # Store user in Flask's g object
                g.current_user = user
                g.db = db
                
                # Call the protected function
                return f(*args, **kwargs)
                
        except AuthenticationError as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return jsonify({"error": "Authentication failed"}), 500
    
    return decorated_function


def admin_required(f):
    """Decorator to protect routes that require admin privileges."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # Check if user has admin privileges
        # This is a placeholder - you should add an is_admin field to User model
        if not getattr(g.current_user, 'is_admin', False):
            return jsonify({"error": "Admin privileges required"}), 403
        return f(*args, **kwargs)
    
    return decorated_function