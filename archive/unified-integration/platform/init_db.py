#!/usr/bin/env python3
"""
Initialize database tables.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables
load_dotenv()

def init_database():
    """Initialize database with all tables."""
    from src.database import init_db, db_config
    
    print("🚀 Initializing Sora AI Platform Database")
    print("=" * 50)
    
    # Test connection
    print("\n🔄 Testing database connection...")
    try:
        with db_config.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Create tables
    print("\n🔄 Creating database tables...")
    try:
        init_db()
        print("✅ Database tables created successfully!")
        
        # List tables
        with db_config.engine.connect() as conn:
            if 'sqlite' in db_config.database_url:
                result = conn.execute(text("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    ORDER BY name
                """))
            else:
                result = conn.execute(text("""
                    SELECT tablename FROM pg_tables 
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
    if init_database():
        print("\n✅ Database initialization complete!")
        print("\nYou can now run the application with:")
        print("  python3 app.py")
    else:
        print("\n❌ Database initialization failed!")
        exit(1)