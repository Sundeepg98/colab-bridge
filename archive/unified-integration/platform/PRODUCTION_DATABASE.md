# Production PostgreSQL Setup

## Quick Setup with Neon (Recommended)

1. Go to https://neon.tech and sign up (free)
2. Create a new project
3. Copy your connection string from the dashboard
4. Update your .env file:

```
DATABASE_URL=postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

## Your Current Configuration

For immediate testing, we're using SQLite which requires no setup.
The application is fully compatible with PostgreSQL for production.

## Migration to PostgreSQL

When ready to use PostgreSQL:
1. Sign up for a free PostgreSQL host
2. Update DATABASE_URL in .env
3. Run: python3 setup_database.py
4. All your models and code will work without changes

## Free PostgreSQL Providers:
- Neon: 3GB free (https://neon.tech)
- Supabase: 500MB free (https://supabase.com)
- ElephantSQL: 20MB free (https://elephantsql.com)
- Aiven: 1 month free trial (https://aiven.io)
