"""
Authentication package for AI platform.
"""

from .authentication import (
    AuthManager,
    AuthenticationError,
    login_required,
    admin_required
)

__all__ = [
    'AuthManager',
    'AuthenticationError',
    'login_required',
    'admin_required'
]