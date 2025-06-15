"""
Authentication API routes for Flask integration.
"""

from flask import Blueprint, request, jsonify, g
from sqlalchemy.exc import IntegrityError
import logging

from ..database import db_config
from .authentication import AuthManager, AuthenticationError, login_required

logger = logging.getLogger(__name__)

# Create Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        with db_config.get_db_session() as db:
            user = AuthManager.register_user(db, email, password)
            
            return jsonify({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_verified": user.is_verified
                }
            }), 201
            
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        return jsonify({"error": "User with this email already exists"}), 409
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"error": "Registration failed"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return tokens."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Get client info
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        with db_config.get_db_session() as db:
            result = AuthManager.login_user(db, email, password, ip_address, user_agent)
            return jsonify(result), 200
            
    except AuthenticationError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"error": "Login failed"}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout current user."""
    try:
        with db_config.get_db_session() as db:
            AuthManager.logout_user(db, g.current_user.id)
            return jsonify({"message": "Logged out successfully"}), 200
            
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return jsonify({"error": "Logout failed"}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({"error": "Refresh token is required"}), 400
        
        with db_config.get_db_session() as db:
            result = AuthManager.refresh_access_token(db, refresh_token)
            return jsonify(result), 200
            
    except AuthenticationError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        return jsonify({"error": "Token refresh failed"}), 500


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user information."""
    try:
        user = g.current_user
        
        return jsonify({
            "user": {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "created_at": user.created_at.isoformat(),
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Get user error: {e}")
        return jsonify({"error": "Failed to get user information"}), 500


@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({"error": "Old and new passwords are required"}), 400
        
        if len(new_password) < 8:
            return jsonify({"error": "New password must be at least 8 characters long"}), 400
        
        with db_config.get_db_session() as db:
            user = g.current_user
            
            # Verify old password
            if not AuthManager.verify_password(old_password, user.password_hash):
                return jsonify({"error": "Invalid old password"}), 401
            
            # Update password
            user.password_hash = AuthManager.hash_password(new_password)
            db.add(user)
            db.commit()
            
            return jsonify({"message": "Password changed successfully"}), 200
            
    except Exception as e:
        logger.error(f"Password change error: {e}")
        return jsonify({"error": "Failed to change password"}), 500


@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """Verify user email with token."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        token = data.get('token')
        
        if not token:
            return jsonify({"error": "Verification token is required"}), 400
        
        with db_config.get_db_session() as db:
            from ..database.models import User
            
            user = db.query(User).filter(User.verification_token == token).first()
            
            if not user:
                return jsonify({"error": "Invalid verification token"}), 400
            
            user.is_verified = True
            user.verification_token = None
            db.commit()
            
            return jsonify({"message": "Email verified successfully"}), 200
            
    except Exception as e:
        logger.error(f"Email verification error: {e}")
        return jsonify({"error": "Email verification failed"}), 500


@auth_bp.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    """Request password reset token."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email')
        
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        with db_config.get_db_session() as db:
            from ..database.models import User
            from datetime import datetime, timedelta
            import secrets
            
            user = db.query(User).filter(User.email == email).first()
            
            if user:
                # Generate reset token
                user.reset_token = secrets.token_urlsafe(32)
                user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
                db.commit()
                
                # In a real application, you would send an email here
                logger.info(f"Password reset requested for {email}")
            
            # Always return success to prevent email enumeration
            return jsonify({
                "message": "If the email exists, a password reset link has been sent"
            }), 200
            
    except Exception as e:
        logger.error(f"Password reset request error: {e}")
        return jsonify({"error": "Failed to process password reset request"}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not token or not new_password:
            return jsonify({"error": "Token and new password are required"}), 400
        
        if len(new_password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        
        with db_config.get_db_session() as db:
            from ..database.models import User
            from datetime import datetime
            
            user = db.query(User).filter(
                User.reset_token == token,
                User.reset_token_expires > datetime.utcnow()
            ).first()
            
            if not user:
                return jsonify({"error": "Invalid or expired reset token"}), 400
            
            # Update password
            user.password_hash = AuthManager.hash_password(new_password)
            user.reset_token = None
            user.reset_token_expires = None
            db.commit()
            
            return jsonify({"message": "Password reset successfully"}), 200
            
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        return jsonify({"error": "Failed to reset password"}), 500


# Error handlers
@auth_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@auth_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {error}")
    return jsonify({"error": "Internal server error"}), 500