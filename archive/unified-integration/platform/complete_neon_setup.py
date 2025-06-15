#!/usr/bin/env python3
"""
Complete Neon setup after getting connection string.
"""

import os
from dotenv import load_dotenv, set_key
from sqlalchemy import text

def complete_neon_setup():
    """Complete setup with user's connection string."""
    
    print("\n🎯 Neon PostgreSQL Configuration")
    print("=" * 50)
    
    print("\nPaste your Neon connection string below:")
    print("(It starts with postgresql:// and includes your password)\n")
    
    connection_string = input("> ").strip().strip('"'')
    
    if not connection_string or not connection_string.startswith("postgresql://"):
        print("\n❌ Invalid connection string!")
        return False
    
    # Ensure SSL
    if "sslmode=" not in connection_string:
        connection_string += "?sslmode=require" if "?" not in connection_string else "&sslmode=require"
    
    # Update .env
    print("\n🔄 Updating configuration...")
    set_key('.env', 'DATABASE_URL', connection_string)
    
    # Reload and test
    load_dotenv(override=True)
    
    print("🔄 Testing connection...")
    try:
        from src.database import db_config
        db_config.database_url = connection_string
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"\n✅ Connected to Neon PostgreSQL!")
            print(f"🐘 Version: {version.split()[1]}")
        
        # Create tables
        print("\n🔄 Creating tables...")
        from src.database import init_db
        init_db()
        print("✅ All tables created!")
        
        print("\n🎉 SUCCESS! Your Neon PostgreSQL is ready!")
        print("\n🚀 Restart your app: python3 app.py")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    complete_neon_setup()
