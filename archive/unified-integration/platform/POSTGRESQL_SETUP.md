# Setting Up Free PostgreSQL with Neon

## Quick Setup (2 minutes)

1. **Visit**: https://neon.tech/signup
2. **Sign up** with GitHub or email (FREE)
3. **Create Project**:
   - Name: "ai-integration-platform" (or any name)
   - Region: Choose nearest to you
4. **Copy Connection String** from dashboard

## Update Your App

1. Replace DATABASE_URL in .env:
```
DATABASE_URL=postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

2. Run database setup:
```bash
python3 init_db.py
```

3. Restart app:
```bash
python3 app.py
```

## Why Neon?

- ✅ 3GB storage FREE (plenty for thousands of users)
- ✅ Automatic backups
- ✅ Built-in connection pooling
- ✅ Instant provisioning
- ✅ Branching for development

## Alternative: Quick SQLite

Your app is currently using SQLite which works perfectly for:
- Development and testing
- Small to medium applications
- Up to ~100 concurrent users

When you need PostgreSQL features (better concurrency, full-text search, etc.), follow the Neon setup above.
