# Enterprise Deployment Guide

## AI Integration Platform - Enterprise Ready

This document provides comprehensive guidance for deploying the AI Integration Platform in enterprise environments.

## Overview

The platform has been enhanced with enterprise-grade features including:

- **Security Layer**: Rate limiting, API key authentication, input sanitization
- **Monitoring & Analytics**: Comprehensive metrics, health checks, performance tracking
- **Configuration Management**: Environment-based settings with validation
- **Testing Suite**: Comprehensive test coverage for security and monitoring
- **Production Deployment**: Docker containerization with orchestration

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Nginx Proxy   │    │   Application   │
│      (nginx)    ├────┤    (SSL/TLS)    ├────┤    (Flask)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Monitoring    │    │    Database     │
                       │  (Prometheus)   │    │  (PostgreSQL)   │
                       └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Visualization │    │     Cache       │
                       │   (Grafana)     │    │    (Redis)      │
                       └─────────────────┘    └─────────────────┘
```

## Security Features

### API Key Authentication
- Tier-based access control (basic, premium, enterprise, admin)
- Rate limiting based on tier
- Secure key generation and storage
- Key revocation capabilities

### Rate Limiting
- Per-minute and per-hour limits
- IP-based and key-based tracking
- Automatic blocking for violations
- Configurable limits per environment

### Input Sanitization
- XSS protection
- SQL injection prevention
- Command injection detection
- Content length validation
- Suspicious pattern detection

## Monitoring & Analytics

### Metrics Collection
- Request/response metrics
- Performance statistics
- Error tracking
- Usage analytics
- Success rates by optimization type

### Health Checks
- Response time monitoring
- Error rate tracking
- Memory usage monitoring
- Database connectivity
- External service health

### Prometheus Integration
- Standard metrics format
- Custom metrics export
- Alert integration ready
- Grafana visualization

## Configuration Management

### Environment-Based Settings
- Development: Permissive, debug enabled
- Staging: Production-like with monitoring
- Production: Secure, optimized, monitored
- Testing: Isolated, fast execution

### Configuration Categories
- Security settings
- Performance parameters
- Monitoring configuration
- AI model settings
- Database connections

## Deployment Options

### 1. Docker Compose (Recommended for Development/Testing)

```bash
# Clone repository
git clone <repository-url>
cd ai-integration-platform

# Set environment variables
cp .env.example .env
# Edit .env with your values

# Deploy with Docker Compose
cd docker
docker-compose up -d

# Check health
curl http://localhost/api/health
```

### 2. Kubernetes (Recommended for Production)

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app=ai-integration-platform

# Access application
kubectl port-forward svc/ai-integration-platform 5000:5000
```

### 3. Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export ENVIRONMENT=production
export ANTHROPIC_API_KEY=your_key_here

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

## Environment Variables

### Required
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key
ENVIRONMENT=production
```

### Optional Security
```bash
ENABLE_RATE_LIMITING=true
RATE_LIMIT_PER_MINUTE=60
ENABLE_API_KEY_AUTH=true
ENABLE_HTTPS_ONLY=true
ALLOWED_ORIGINS=https://yourdomain.com
```

### Optional Database
```bash
DATABASE_URL=postgresql://user:pass@host:port/db
ENABLE_DATABASE=true
```

### Optional Monitoring
```bash
LOG_LEVEL=INFO
ENABLE_METRICS=true
ERROR_TRACKING_DSN=your_sentry_dsn
```

## API Endpoints

### Core Functionality
- `POST /api/optimize` - Optimize prompts
- `POST /api/claude-enhance` - Claude AI enhancement
- `POST /api/validate-legality` - Legal validation
- `POST /api/create-narrative-scene` - Narrative generation

### Monitoring
- `GET /api/health` - Basic health check
- `GET /api/health/detailed` - Detailed health status
- `GET /api/metrics` - System metrics
- `GET /api/metrics/prometheus` - Prometheus format metrics

### Administration
- `GET /api/config` - Public configuration
- `POST /api/security/generate-key` - Generate API key (admin)

## Authentication

### API Key Usage
```bash
# Include in request headers
curl -H "X-API-Key: your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "test"}' \
     http://localhost:5000/api/optimize
```

### Demo Keys (Development Only)
- `demo-key-001` - Basic tier
- `demo-key-002` - Premium tier  
- `demo-key-admin` - Admin tier

## Monitoring Setup

### Prometheus Configuration
Add to `prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'ai-integration-platform'
    static_configs:
      - targets: ['ai-integration-platform:5000']
    metrics_path: '/api/metrics/prometheus'
```

### Grafana Dashboards
Import dashboard templates from `docker/grafana/dashboards/`

### Alert Rules
Configure alerts for:
- High error rates (>5%)
- Slow response times (>5s)
- Rate limit violations
- Service unavailability

## Performance Tuning

### Application Settings
```python
# Adjust in config.py
performance.max_workers = 8
performance.enable_caching = True
performance.cache_ttl_seconds = 3600
```

### Database Optimization
```sql
-- Add indexes for performance
CREATE INDEX idx_usage_timestamp ON usage_stats(timestamp);
CREATE INDEX idx_performance_endpoint ON performance_stats(endpoint);
```

### Caching Strategy
- Response caching for similar prompts
- API key validation caching
- Rate limit state caching

## Security Best Practices

### Production Checklist
- [ ] HTTPS enabled with valid certificates
- [ ] API key authentication active
- [ ] Rate limiting configured
- [ ] Input sanitization enabled
- [ ] Error details disabled in responses
- [ ] Audit logging configured
- [ ] Database connections encrypted
- [ ] Secrets management in place

### Network Security
```yaml
# Example security group rules
ingress:
  - port: 443
    protocol: HTTPS
    source: 0.0.0.0/0
  - port: 80
    protocol: HTTP
    source: 0.0.0.0/0
    redirect: 443
egress:
  - port: 443
    protocol: HTTPS
    destination: api.anthropic.com
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure PYTHONPATH is set
   export PYTHONPATH=/app/src:$PYTHONPATH
   ```

2. **Rate Limit Issues**
   ```bash
   # Check rate limit status
   curl -H "X-API-Key: your-key" http://localhost:5000/api/metrics
   ```

3. **Authentication Failures**
   ```bash
   # Verify API key
   curl -H "X-API-Key: demo-key-001" http://localhost:5000/api/config
   ```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
export ENVIRONMENT=development
```

### Health Check Failures
```bash
# Check detailed health
curl http://localhost:5000/api/health/detailed

# Check individual components
curl http://localhost:5000/api/metrics
```

## Backup and Recovery

### Database Backups
```bash
# PostgreSQL backup
pg_dump ai_integration_platform > backup_$(date +%Y%m%d).sql

# Restore
psql ai_integration_platform < backup_20240613.sql
```

### Configuration Backups
- Store `.env` files securely
- Version control configuration changes
- Document API key assignments

## Scaling

### Horizontal Scaling
```yaml
# Kubernetes replica scaling
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 5
```

### Load Balancing
```nginx
upstream ai_integration_platform {
    server ai-integration-platform-1:5000;
    server ai-integration-platform-2:5000;
    server ai-integration-platform-3:5000;
}
```

### Database Scaling
- Read replicas for analytics
- Connection pooling
- Query optimization

## Compliance

### Data Privacy
- Input sanitization for PII
- Request/response logging controls
- Data retention policies
- User consent tracking

### Audit Requirements
- All API calls logged
- Authentication events tracked
- Error events recorded
- Performance metrics retained

## Support

### Log Locations
- Application: `/app/logs/app.log`
- Access: `/var/log/nginx/access.log`
- Error: `/var/log/nginx/error.log`

### Monitoring Dashboards
- Application metrics: `http://localhost:3000`
- System metrics: `http://localhost:9090`
- Health status: `http://localhost:5000/api/health`

### Contact
For enterprise support and customization:
- Technical issues: Check application logs
- Performance issues: Review metrics dashboard
- Security concerns: Audit security logs

## License

This enterprise deployment guide is part of the AI Integration Platform.