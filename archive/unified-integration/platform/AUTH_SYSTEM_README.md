# AI Platform Authentication System

## Overview

This is a production-ready authentication and user management system for the AI platform. It includes:

- **User Authentication**: Registration, login, logout with JWT tokens
- **Session Management**: Secure session tracking with refresh tokens
- **Database Models**: User accounts, API integrations, usage tracking, and billing
- **Security Features**: Password hashing (bcrypt), API key encryption, rate limiting support
- **Database Migrations**: Alembic integration for schema versioning

## Features

### Authentication
- Email/password registration and login
- JWT access tokens (30-minute expiry by default)
- Refresh tokens (7-day expiry by default)
- Password reset functionality
- Email verification
- Account lockout after failed login attempts

### Database Models
1. **User**: Core user account with authentication details
2. **UserIntegration**: Stores encrypted API keys for AI services
3. **UsageTracking**: Tracks API usage for analytics and billing
4. **Billing**: Manages billing records and payment status
5. **UserSession**: Tracks active user sessions

### Security
- Bcrypt password hashing
- JWT token authentication
- Encrypted API key storage
- Session management with IP tracking
- Rate limiting support
- Account lockout protection

## Quick Start

### 1. Environment Setup

Create a `.env` file with the following variables:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_platform

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Encryption
ENCRYPTION_MASTER_KEY=your-encryption-key-change-this

# Security
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=30
```

### 2. Database Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python database_setup.py

# Create admin user
python database_setup.py --create-admin --admin-email admin@example.com --admin-password securepassword

# For database reset (WARNING: deletes all data)
python database_setup.py --reset
```

### 3. Integration with Flask App

Add to your `app.py`:

```python
from src.auth.api_routes import auth_bp
from src.database import init_db

app = Flask(__name__)

# Register authentication routes
app.register_blueprint(auth_bp)

# Initialize database
init_db()
```

## API Endpoints

### Authentication Endpoints

#### Register User
```bash
POST /api/auth/register
{
    "email": "user@example.com",
    "password": "securepassword"
}
```

#### Login
```bash
POST /api/auth/login
{
    "email": "user@example.com",
    "password": "securepassword"
}

Response:
{
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "is_verified": false
    }
}
```

#### Logout
```bash
POST /api/auth/logout
Authorization: Bearer <access_token>
```

#### Refresh Token
```bash
POST /api/auth/refresh
{
    "refresh_token": "eyJ..."
}
```

#### Get Current User
```bash
GET /api/auth/me
Authorization: Bearer <access_token>
```

#### Change Password
```bash
POST /api/auth/change-password
Authorization: Bearer <access_token>
{
    "old_password": "currentpassword",
    "new_password": "newsecurepassword"
}
```

#### Request Password Reset
```bash
POST /api/auth/request-password-reset
{
    "email": "user@example.com"
}
```

#### Reset Password
```bash
POST /api/auth/reset-password
{
    "token": "reset-token-from-email",
    "new_password": "newsecurepassword"
}
```

## Protected Routes

Use the `@login_required` decorator to protect routes:

```python
from flask import g, jsonify
from src.auth import login_required

@app.route('/api/protected')
@login_required
def protected_route():
    user = g.current_user
    return jsonify({
        "message": f"Hello {user.email}!",
        "user_id": user.id
    })
```

## Working with User Integrations

Store encrypted API keys:

```python
from src.database import db_config, UserIntegration, ServiceType
from src.auth.encryption import encrypt_api_key

with db_config.get_db_session() as db:
    integration = UserIntegration(
        user_id=user.id,
        service_name=ServiceType.CLAUDE,
        api_key_encrypted=encrypt_api_key("sk-ant-api-key"),
        status="active"
    )
    db.add(integration)
```

Retrieve and decrypt API keys:

```python
from src.auth.encryption import decrypt_api_key

api_key = decrypt_api_key(integration.api_key_encrypted)
```

## Usage Tracking

Track API usage for billing:

```python
from src.database import UsageTracking, ServiceType

with db_config.get_db_session() as db:
    usage = UsageTracking(
        user_id=user.id,
        service=ServiceType.CLAUDE,
        tokens_used=1500,
        cost=0.015,
        model_name="claude-3-opus",
        request_type="completion"
    )
    db.add(usage)
```

## Database Migrations

Using Alembic for database migrations:

```bash
# Initialize Alembic (first time only)
python database_setup.py --init-alembic

# Create a new migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Security Best Practices

1. **Environment Variables**: Never commit secrets to version control
2. **HTTPS Only**: Always use HTTPS in production
3. **Token Rotation**: Implement token rotation for enhanced security
4. **Rate Limiting**: Add rate limiting to prevent brute force attacks
5. **Audit Logging**: Log all authentication events
6. **Regular Updates**: Keep dependencies updated

## Testing

```python
# Test database connection
python database_setup.py --check-connection

# Run authentication tests
pytest tests/test_auth.py
```

## Production Deployment

1. Use environment-specific configurations
2. Enable SSL for PostgreSQL connections
3. Set up proper logging and monitoring
4. Configure backup strategies
5. Implement rate limiting at the API gateway level
6. Use a reverse proxy (nginx) with proper security headers

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check DATABASE_URL format
   - Ensure PostgreSQL is running
   - Verify network connectivity

2. **Token Validation Errors**
   - Ensure JWT_SECRET_KEY is consistent
   - Check token expiration times
   - Verify Authorization header format

3. **Encryption Errors**
   - Ensure ENCRYPTION_MASTER_KEY is set
   - Check for data corruption
   - Verify key consistency across deployments

## License

This authentication system is part of the AI Platform project.