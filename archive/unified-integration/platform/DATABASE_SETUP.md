# Database Setup Guide

## Hosted PostgreSQL Options

### 1. **Neon** (Recommended - Free tier available)
- Sign up at: https://neon.tech
- Create a new project
- Copy the connection string from the dashboard
- Format: `postgresql://[user]:[password]@[neon-hostname]/[database]?sslmode=require`

### 2. **Supabase** (Free tier with 500MB)
- Sign up at: https://supabase.com
- Create a new project
- Go to Settings → Database
- Copy the connection string
- Format: `postgresql://postgres:[password]@[project-id].supabase.co:5432/postgres`

### 3. **Railway** (Simple deployment)
- Sign up at: https://railway.app
- Create new project → Add PostgreSQL
- Copy the DATABASE_URL from variables
- Format: `postgresql://postgres:[password]@[host].railway.app:[port]/railway`

### 4. **Render** (Free tier available)
- Sign up at: https://render.com
- Create new PostgreSQL database
- Copy Internal or External Database URL
- Format: `postgresql://[user]:[password]@[host]/[database]`

### 5. **ElephantSQL** (Free 20MB tier)
- Sign up at: https://www.elephantsql.com
- Create new instance (Tiny Turtle - Free)
- Copy the URL from details page
- Format: `postgresql://[user]:[password]@[server]/[user]`

## Setup Instructions

1. Choose a provider and create an account
2. Create a new PostgreSQL database instance
3. Copy the connection string
4. Update `.env` file:
   ```
   DATABASE_URL=your-connection-string-here
   ```

5. Initialize the database:
   ```bash
   python3 -c "from src.database import init_db; init_db()"
   ```

## Production Considerations

1. **SSL/TLS**: Most hosted providers require SSL. Add `?sslmode=require` to your connection string if not included.

2. **Connection Pooling**: The application is configured with connection pooling:
   - Pool size: 10 (configurable via DB_POOL_SIZE)
   - Max overflow: 20 (configurable via DB_MAX_OVERFLOW)
   - Pool timeout: 30s (configurable via DB_POOL_TIMEOUT)

3. **Backups**: Most providers offer automatic backups. Enable them for production use.

4. **Monitoring**: Use the provider's monitoring tools to track:
   - Connection count
   - Query performance
   - Storage usage
   - CPU/Memory usage

## Environment Variables

```bash
# Required
DATABASE_URL=postgresql://username:password@host:port/database

# Optional (with defaults)
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
DB_SSL_REQUIRE=true  # Set to true for production
```

## Testing Connection

```python
from src.database import db_config

# Test connection
try:
    with db_config.get_db() as db:
        db.execute("SELECT 1")
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```