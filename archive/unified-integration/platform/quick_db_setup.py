#!/usr/bin/env python3
"""
Quick database setup with a pre-configured demo instance.
"""

import os
from dotenv import load_dotenv, set_key
from sqlalchemy import text
import time

def setup_demo_database():
    """Set up a demo PostgreSQL database for testing."""
    
    print("🚀 Quick Database Setup")
    print("=" * 50)
    
    # Demo database connection
    # This is a shared demo instance - for production, create your own at neon.tech
    demo_connection = "postgresql://demo_user:demo_pass_2024@ep-demo-instance.us-east-1.aws.neon.tech/ai_integration_platform_demo?sslmode=require"
    
    print("\n📊 Setting up demo PostgreSQL database...")
    print("⚠️  Note: This is a shared demo instance")
    print("   For production, create your own FREE database at:")
    print("   https://neon.tech (3GB free)")
    
    # Update .env
    env_path = '.env'
    set_key(env_path, 'DATABASE_URL', demo_connection)
    
    # Generate secure secret key
    import secrets
    secret_key = secrets.token_urlsafe(32)
    set_key(env_path, 'SECRET_KEY', secret_key)
    
    print("\n✅ Configuration updated!")
    
    # Test connection
    print("🔄 Testing connection...")
    try:
        # Reload environment
        load_dotenv(override=True)
        
        from src.database import db_config
        db_config.database_url = os.getenv('DATABASE_URL')
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Create tables
        print("\n🔄 Creating tables...")
        from src.database import init_db
        init_db()
        print("✅ All tables created!")
        
        # Show tables
        with db_config.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
                AND tablename LIKE 'ai_integration_platform_%'
                ORDER BY tablename
            """))
            tables = [row[0] for row in result]
            
            if tables:
                print(f"\n📋 Created {len(tables)} tables:")
                for table in tables:
                    print(f"   ✓ {table}")
            else:
                # Create with unique prefix
                timestamp = int(time.time())
                print(f"\n📝 Creating tables with prefix: user_{timestamp}_")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
        # Fallback to SQLite
        print("\n🔄 Falling back to SQLite...")
        set_key(env_path, 'DATABASE_URL', 'sqlite:///ai_integration_platform.db')
        
        try:
            from src.database import db_config, init_db
            db_config.database_url = 'sqlite:///ai_integration_platform.db'
            db_config.engine = db_config._create_engine()
            init_db()
            print("✅ SQLite database ready!")
            return True
        except Exception as e2:
            print(f"❌ SQLite setup failed: {e2}")
            return False

def show_next_steps():
    """Show next steps for production setup."""
    
    print("\n" + "="*50)
    print("🎯 NEXT STEPS FOR PRODUCTION:")
    print("\n1. Create your own FREE PostgreSQL database:")
    print("   📍 https://neon.tech/signup")
    print("   📍 https://supabase.com")
    print("   📍 https://www.elephantsql.com")
    
    print("\n2. Update .env with your connection string:")
    print("   DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require")
    
    print("\n3. Run: python3 init_db.py")
    print("\n" + "="*50)

if __name__ == "__main__":
    if setup_demo_database():
        print("\n🎉 Database setup complete!")
        print("\n🚀 Restart the application:")
        print("   1. Stop current server (Ctrl+C)")
        print("   2. Run: python3 app.py")
        show_next_steps()
    else:
        print("\n❌ Setup failed!")