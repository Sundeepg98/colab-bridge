"""
Example integration of authentication system with Flask application.
"""

from flask import Flask
from .api_routes import auth_bp
from ..database import init_db, db_config
import os


def integrate_auth_with_app(app: Flask):
    """
    Integrate authentication system with existing Flask application.
    
    Usage in your app.py:
    
    from src.auth.integration_example import integrate_auth_with_app
    
    app = Flask(__name__)
    integrate_auth_with_app(app)
    """
    
    # Configure database URL
    app.config['DATABASE_URL'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/ai_platform'
    )
    
    # Configure JWT secret
    app.config['JWT_SECRET_KEY'] = os.environ.get(
        'JWT_SECRET_KEY',
        'your-secret-key-change-this-in-production'
    )
    
    # Register authentication blueprint
    app.register_blueprint(auth_bp)
    
    # Initialize database on first run
    @app.before_first_request
    def initialize_database():
        """Initialize database tables."""
        try:
            init_db()
            app.logger.info("Database initialized successfully")
        except Exception as e:
            app.logger.error(f"Database initialization failed: {e}")
    
    # Cleanup database connections
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Remove database session at the end of request."""
        db_config.SessionLocal.remove()
    
    app.logger.info("Authentication system integrated successfully")


# Example protected route decorator usage
"""
from src.auth import login_required

@app.route('/api/protected')
@login_required
def protected_route():
    # Access current user via g.current_user
    user = g.current_user
    return jsonify({
        "message": f"Hello {user.email}!",
        "user_id": user.id
    })
"""


# Example of using authentication in existing endpoints
"""
from src.auth import AuthManager
from src.database import db_config

@app.route('/api/user/integrations', methods=['GET'])
@login_required
def get_user_integrations():
    with db_config.get_db_session() as db:
        integrations = db.query(UserIntegration).filter(
            UserIntegration.user_id == g.current_user.id
        ).all()
        
        return jsonify([{
            "id": i.id,
            "service": i.service_name.value,
            "status": i.status,
            "created_at": i.created_at.isoformat()
        } for i in integrations])
"""