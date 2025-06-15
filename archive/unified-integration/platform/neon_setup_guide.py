#!/usr/bin/env python3
"""
Interactive Neon.tech PostgreSQL setup guide.
"""

import os
import time
import webbrowser
from dotenv import load_dotenv, set_key
from sqlalchemy import text
import re

def validate_neon_url(url):
    """Validate Neon connection string format."""
    # Check basic PostgreSQL URL format
    pattern = r'^postgresql://[^:]+:[^@]+@[^/]+\.neon\.tech(?::\d+)?/[^?]+(?:\?sslmode=require)?$'
    return bool(re.match(pattern, url))

def setup_neon():
    """Interactive Neon setup."""
    
    print("🚀 Neon.tech PostgreSQL Setup")
    print("=" * 50)
    print("\n✨ Neon offers:")
    print("   • 3GB storage FREE")
    print("   • Automatic backups")
    print("   • Connection pooling")
    print("   • Instant provisioning")
    print("   • Branch databases")
    
    print("\n📝 Let's set it up together...")
    print("\n1️⃣ First, I'll open the Neon signup page")
    time.sleep(2)
    
    # Try to open browser
    neon_url = "https://console.neon.tech/signup"
    print(f"\n🌐 Opening: {neon_url}")
    print("   (If browser doesn't open, visit manually)")
    
    try:
        webbrowser.open(neon_url)
        opened = True
    except:
        opened = False
    
    print("\n2️⃣ Sign up with GitHub or Email (it's FREE)")
    print("\n3️⃣ After signup, Neon will:")
    print("   • Create a project automatically")
    print("   • Show you the dashboard")
    
    print("\n4️⃣ On the dashboard, look for:")
    print("   • 'Connection Details' or 'Connection String'")
    print("   • It's usually in a green/blue box")
    print("   • Click 'Show password' if needed")
    
    print("\n📋 The connection string looks like this:")
    print("postgresql://username:password@ep-xyz-123456.us-east-2.aws.neon.tech/neondb")
    
    if not opened:
        print(f"\n🔗 Manual link: {neon_url}")
    
    print("\n" + "="*50)
    
    # Wait for user to get connection string
    print("\n⏳ Take your time to sign up and get the connection string...")
    print("   (I'll wait here)")
    
    connection_string = input("\n📥 Paste your Neon connection string here:\n> ").strip()
    
    # Validate connection string
    if not connection_string:
        print("\n❌ No connection string provided!")
        return False
    
    # Add quotes if not present
    if not (connection_string.startswith('"') or connection_string.startswith("'")):
        connection_string = connection_string.strip()
    else:
        connection_string = connection_string.strip('"\'')
    
    # Ensure sslmode=require
    if "sslmode=" not in connection_string:
        if "?" in connection_string:
            connection_string += "&sslmode=require"
        else:
            connection_string += "?sslmode=require"
    
    # Basic validation
    if not connection_string.startswith("postgresql://"):
        print("\n❌ Invalid format! Connection string should start with 'postgresql://'")
        return False
    
    if "@" not in connection_string or ".neon.tech" not in connection_string:
        print("\n❌ This doesn't look like a Neon connection string!")
        print("   Make sure it contains '@' and '.neon.tech'")
        return False
    
    print("\n✅ Connection string looks good!")
    
    # Update .env file
    print("🔄 Updating configuration...")
    env_path = '.env'
    
    # Backup current DATABASE_URL
    load_dotenv()
    old_db_url = os.getenv('DATABASE_URL', '')
    
    # Update DATABASE_URL
    set_key(env_path, 'DATABASE_URL', connection_string)
    
    # Reload environment
    load_dotenv(override=True)
    
    # Test connection
    print("\n🔄 Testing Neon connection...")
    try:
        from src.database import db_config
        
        # Force reload with new URL
        db_config.database_url = connection_string
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            # Test basic query
            result = conn.execute(text("SELECT current_database(), version()"))
            db_name, version = result.fetchone()
            
            print(f"\n✅ Successfully connected to Neon!")
            print(f"📊 Database: {db_name}")
            print(f"🐘 PostgreSQL: {version.split(' ')[1]}")
            print(f"☁️  Region: {connection_string.split('@')[1].split('.')[0]}")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you copied the ENTIRE connection string")
        print("2. Check that the password is included")
        print("3. Try the 'pooled connection' option in Neon dashboard")
        
        # Restore old DATABASE_URL
        if old_db_url:
            set_key(env_path, 'DATABASE_URL', old_db_url)
            print(f"\n↩️  Restored previous database configuration")
        
        return False

def create_tables():
    """Create all tables in Neon."""
    print("\n🔄 Creating tables in Neon...")
    
    try:
        from src.database import init_db, db_config
        from sqlalchemy import text
        
        # Create tables
        init_db()
        
        # Verify tables
        with db_config.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """))
            tables = [row[0] for row in result]
            
            print(f"\n✅ Created {len(tables)} tables:")
            for table in tables:
                print(f"   ✓ {table}")
                
            # Show database size
            result = conn.execute(text("""
                SELECT pg_database_size(current_database()) as size
            """))
            size_bytes = result.scalar()
            size_mb = size_bytes / (1024 * 1024)
            print(f"\n💾 Database size: {size_mb:.2f} MB / 3072 MB (Free tier)")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def main():
    """Main setup flow."""
    print("🎯 Let's set up your Neon PostgreSQL database!\n")
    
    if setup_neon():
        print("\n" + "="*50)
        
        if create_tables():
            print("\n🎉 SUCCESS! Your Neon PostgreSQL is ready!")
            print("\n📊 What you've got:")
            print("   ✅ Real PostgreSQL database")
            print("   ✅ 3GB storage (FREE)")
            print("   ✅ Automatic daily backups")
            print("   ✅ SSL encrypted connection")
            print("   ✅ All tables created")
            
            print("\n🚀 Next steps:")
            print("1. Restart your app to use Neon:")
            print("   python3 app.py")
            print("\n2. Your app now uses production PostgreSQL!")
            
            print("\n💡 Neon Dashboard:")
            print("   https://console.neon.tech")
            print("   (Monitor usage, create branches, view metrics)")
            
        else:
            print("\n⚠️  Connected to Neon but table creation failed")
            print("   Try running: python3 init_db.py")
    else:
        print("\n❌ Neon setup incomplete")
        print("\n💡 Need help?")
        print("1. Make sure you're copying from 'Connection string' section")
        print("2. Include the password (click 'show password' if hidden)")
        print("3. Try the 'Direct connection' option instead of 'Pooled'")

if __name__ == "__main__":
    main()