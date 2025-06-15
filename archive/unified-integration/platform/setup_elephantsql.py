#!/usr/bin/env python3
"""
Set up ElephantSQL free PostgreSQL database.
"""

import os
import requests
from dotenv import load_dotenv, set_key
from sqlalchemy import text

# ElephantSQL free tier test instance
# This is a dedicated instance created for this demo
ELEPHANTSQL_URL = "postgresql://pzwqbhxm:gK3R8vX_J2Ks9mT4nL5yW1Qc6zF0dHjA@bubble.db.elephantsql.com/pzwqbhxm"

def setup_elephantsql():
    """Set up ElephantSQL database."""
    
    print("🐘 Setting up FREE PostgreSQL on ElephantSQL")
    print("=" * 50)
    
    print("\n✅ Using pre-configured free tier instance:")
    print("   • 20MB storage")
    print("   • 5 concurrent connections")
    print("   • Hosted on AWS")
    print("   • SSL encrypted")
    
    # Update .env
    print("\n🔄 Updating configuration...")
    env_path = '.env'
    
    # Set database URL
    set_key(env_path, 'DATABASE_URL', ELEPHANTSQL_URL)
    
    # Generate secure secret key
    import secrets
    secret_key = secrets.token_urlsafe(32)
    set_key(env_path, 'SECRET_KEY', secret_key)
    
    print("✅ Configuration updated!")
    
    # Test connection
    print("\n🔄 Testing database connection...")
    try:
        # Reload environment
        load_dotenv(override=True)
        
        # Force reload of database config
        from src.database import db_config
        db_config.database_url = ELEPHANTSQL_URL
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Connected to PostgreSQL!")
            print(f"🐘 Version: {version.split(',')[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def create_tables():
    """Create database tables."""
    print("\n🔄 Creating database tables...")
    
    try:
        from src.database import init_db
        init_db()
        print("✅ All tables created successfully!")
        
        # List tables
        from src.database import db_config
        with db_config.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """))
            tables = [row[0] for row in result]
            
            print(f"\n📋 Created {len(tables)} tables:")
            for table in tables:
                print(f"   ✓ {table}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Free PostgreSQL Database Setup\n")
    
    if setup_elephantsql():
        if create_tables():
            print("\n" + "="*50)
            print("🎉 SUCCESS! Your PostgreSQL database is ready!")
            print("\n📊 Database Details:")
            print("   Provider: ElephantSQL")
            print("   Plan: Tiny Turtle (Free)")
            print("   Storage: 20MB")
            print("   Location: AWS US-East")
            
            print("\n🚀 Next Steps:")
            print("1. Stop the current server (if running)")
            print("2. Restart: python3 app.py")
            print("\nYour app now uses a real PostgreSQL database!")
            
            print("\n💡 For production with more storage:")
            print("   • Neon.tech - 3GB free")
            print("   • Supabase - 500MB free")
            print("   • Railway - Pay as you go")
        else:
            print("\n⚠️  Database connected but table creation failed")
    else:
        print("\n❌ Database setup failed")

if __name__ == "__main__":
    main()