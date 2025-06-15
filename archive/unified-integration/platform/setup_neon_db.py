#!/usr/bin/env python3
"""
Set up a free Neon PostgreSQL database.
"""

import os
import time
import webbrowser
from dotenv import load_dotenv, set_key

def setup_neon_database():
    """Guide user through Neon database setup."""
    
    print("🚀 Setting up FREE PostgreSQL Database on Neon")
    print("=" * 50)
    print("\nNeon offers:")
    print("✅ 3GB storage FREE")
    print("✅ Automatic backups")
    print("✅ Built-in connection pooling")
    print("✅ SSL encryption")
    print("\n📝 Let's set it up (takes 2 minutes):")
    
    print("\n1. Opening Neon signup page...")
    time.sleep(1)
    
    # Open Neon signup
    neon_url = "https://console.neon.tech/signup"
    print(f"\n🌐 Opening: {neon_url}")
    print("   (If browser doesn't open, visit the URL manually)")
    
    try:
        webbrowser.open(neon_url)
    except:
        print("   ⚠️  Couldn't open browser automatically")
    
    print("\n2. Sign up with GitHub or email (FREE)")
    print("3. Create a new project (any name)")
    print("4. Copy the connection string from the dashboard")
    print("\n📋 It looks like:")
    print("postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb")
    
    print("\n" + "="*50)
    connection_string = input("\n📥 Paste your Neon connection string here: ").strip()
    
    if not connection_string or connection_string == "postgresql://username:password@ep-xxx.region.aws.neon.tech/neondb":
        print("\n❌ Invalid connection string!")
        print("Please get your actual connection string from Neon dashboard")
        return False
    
    # Ensure SSL mode
    if "sslmode=" not in connection_string:
        if "?" in connection_string:
            connection_string += "&sslmode=require"
        else:
            connection_string += "?sslmode=require"
    
    print("\n✅ Connection string received!")
    print("🔄 Updating .env file...")
    
    # Update .env
    env_path = '.env'
    set_key(env_path, 'DATABASE_URL', connection_string)
    
    # Also update SECRET_KEY if it's still default
    load_dotenv()
    if os.getenv('SECRET_KEY') == 'your-secret-key-here-change-in-production':
        import secrets
        secret_key = secrets.token_urlsafe(32)
        set_key(env_path, 'SECRET_KEY', secret_key)
        print("🔐 Generated secure SECRET_KEY")
    
    print("✅ Environment variables updated!")
    
    # Test connection
    print("\n🔄 Testing database connection...")
    try:
        from src.database import db_config
        from sqlalchemy import text
        
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), version()"))
            db_name, version = result.fetchone()
            print(f"\n✅ Connected to Neon PostgreSQL!")
            print(f"📊 Database: {db_name}")
            print(f"🐘 Version: {version.split(',')[0]}")
            
        return True
            
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your connection string is correct")
        print("2. Make sure you copied the ENTIRE string")
        print("3. Try again with the connection string from Neon dashboard")
        return False

def create_tables():
    """Create all database tables."""
    print("\n🔄 Creating database tables...")
    
    try:
        from src.database import init_db
        init_db()
        print("✅ All tables created successfully!")
        
        # Show created tables
        from src.database import db_config
        from sqlalchemy import text
        
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

if __name__ == "__main__":
    print("🎯 FREE PostgreSQL Setup - Quick & Easy!\n")
    
    if setup_neon_database():
        print("\n" + "="*50)
        if create_tables():
            print("\n🎉 SUCCESS! Your database is ready!")
            print("\n🚀 Next steps:")
            print("1. Stop current server: Ctrl+C")
            print("2. Restart application: python3 app.py")
            print("\nYour app now uses a real PostgreSQL database!")
        else:
            print("\n⚠️  Database connected but table creation failed")
    else:
        print("\n❌ Setup failed. Please try again!")