# AI Platform - Production Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Domain name (optional, for HTTPS)
- SMTP server for emails (optional)

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/yourorg/ai-platform.git
cd ai-platform

# Copy environment template
cp .env.example .env

# Generate secure keys
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
python3 -c "import secrets; print('MASTER_KEY=' + secrets.token_urlsafe(32))"

# Update .env with generated keys
nano .env
```

### 2. Deploy with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# Initialize database
docker-compose exec app python database_setup.py init

# Create admin user
docker-compose exec app python database_setup.py create-admin
```

### 3. Access the Platform

- Main App: http://localhost
- Admin Dashboard: http://localhost/admin-enhanced
- API Docs: http://localhost/api/docs

Default admin credentials:
- Email: admin@example.com
- Password: (set during create-admin)

## 📦 What's Included

### Services
1. **PostgreSQL Database** - User data, integrations, usage tracking
2. **Redis** - Sessions, caching, rate limiting
3. **Flask App** - Main application (Gunicorn)
4. **Nginx** - Reverse proxy, static files, SSL termination
5. **Worker** - Background tasks (optional)

### Security Features
- JWT authentication with refresh tokens
- Encrypted API key storage
- Rate limiting on all endpoints
- Session management with IP tracking
- Password hashing with bcrypt
- HTTPS support (configure in nginx.conf)

### Database Schema
- **Users** - Authentication, profile, settings
- **UserIntegrations** - Encrypted API keys for AI services
- **UsageTracking** - API calls, costs, performance
- **Billing** - Invoices, payments, subscriptions
- **UserSessions** - Active sessions, security

## 🔧 Configuration

### Environment Variables

Key variables to configure in `.env`:

```bash
# Database
DB_PASSWORD=strong-unique-password

# Security (use generated values)
SECRET_KEY=your-generated-secret
JWT_SECRET_KEY=your-generated-jwt-secret
MASTER_KEY=your-generated-master-key

# Email (for password resets)
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Platform
PLATFORM_NAME=Your AI Platform
PLATFORM_URL=https://yourdomain.com
```

### SSL/HTTPS Setup

1. Obtain SSL certificates (Let's Encrypt recommended)
2. Update `nginx.conf`:
   - Uncomment SSL sections
   - Add certificate paths
   - Update server_name

3. Update `docker-compose.yml`:
   - Mount certificate directory
   - Map port 443

### Scaling Options

```yaml
# docker-compose.yml
app:
  deploy:
    replicas: 3  # Run multiple app instances
```

## 🛠️ Management Commands

### Database
```bash
# Run migrations
docker-compose exec app alembic upgrade head

# Create database backup
docker-compose exec postgres pg_dump -U ai_platform_user ai_platform > backup.sql

# Restore database
docker-compose exec -T postgres psql -U ai_platform_user ai_platform < backup.sql
```

### Monitoring
```bash
# View logs
docker-compose logs -f app

# Check health
curl http://localhost/health

# View metrics
docker-compose exec app python cli/platform_cli.py health check
```

### User Management
```bash
# Create user via CLI
docker-compose exec app python -c "
from src.auth.authentication import create_user
create_user('user@example.com', 'password123')
"

# Reset user password
docker-compose exec app python database_setup.py reset-password user@example.com
```

## 🚨 Production Checklist

- [ ] Change all default passwords in `.env`
- [ ] Generate new security keys
- [ ] Configure SMTP for emails
- [ ] Set up SSL certificates
- [ ] Configure firewall (allow 80, 443)
- [ ] Set up database backups
- [ ] Configure monitoring (optional)
- [ ] Update ALLOWED_ORIGINS for CORS
- [ ] Set FLASK_ENV=production
- [ ] Configure log rotation

## 📊 Monitoring & Logs

### Application Logs
```bash
# Flask app logs
docker-compose logs app

# Nginx access logs
docker-compose exec nginx tail -f /var/log/nginx/access.log

# Database logs
docker-compose logs postgres
```

### Health Endpoints
- `/health` - Basic health check
- `/api/system-health` - Detailed system status
- `/api/metrics` - Platform metrics

## 🆘 Troubleshooting

### Database Connection Issues
```bash
# Test database connection
docker-compose exec app python -c "
from src.database.db_config import test_connection
test_connection()
"
```

### Redis Connection Issues
```bash
# Test Redis
docker-compose exec redis redis-cli ping
```

### Permission Issues
```bash
# Fix file permissions
docker-compose exec app chown -R appuser:appuser /app/logs /app/uploads
```

## 🔄 Updates & Maintenance

### Update Platform
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec app alembic upgrade head
```

### Backup Before Updates
```bash
# Full backup script
./scripts/backup.sh

# Or manually:
docker-compose exec postgres pg_dump -U ai_platform_user ai_platform > backup_$(date +%Y%m%d).sql
tar -czf uploads_$(date +%Y%m%d).tar.gz uploads/
```

## 📈 Performance Tuning

### PostgreSQL
Edit `docker-compose.yml` to add:
```yaml
postgres:
  command: postgres -c shared_buffers=256MB -c max_connections=200
```

### Gunicorn Workers
Adjust in `Dockerfile`:
```dockerfile
CMD ["gunicorn", "--workers", "8", ...]  # 2-4 x CPU cores
```

### Redis Memory
```yaml
redis:
  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

## 🌐 Domain & DNS

1. Point your domain to server IP
2. Update `nginx.conf` with your domain
3. Update `.env` PLATFORM_URL
4. Restart nginx: `docker-compose restart nginx`

## 🔐 Security Notes

- All API keys are encrypted in database
- User passwords are bcrypt hashed
- JWT tokens expire after 15 minutes
- Sessions tracked by IP and user agent
- Rate limiting prevents abuse
- CORS configured for security

---

For issues or questions, check the [documentation](docs/) or open an issue on GitHub.