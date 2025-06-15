#!/usr/bin/env python3
"""
Database setup and verification script.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_database_url():
    """Check if DATABASE_URL is properly configured."""
    db_url = os.getenv('DATABASE_URL', '')
    
    if not db_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("\nPlease add DATABASE_URL to your .env file:")
        print("DATABASE_URL=postgresql://username:password@host:port/database")
        return False
    
    if db_url == 'postgresql://username:password@host:port/database':
        print("❌ DATABASE_URL is still using the example format")
        print("\nPlease update it with your actual database credentials.")
        print("\nRecommended providers:")
        print("- Neon: https://neon.tech")
        print("- Supabase: https://supabase.com")
        print("- Railway: https://railway.app")
        print("- Render: https://render.com")
        return False
    
    # Mask password in output
    if '@' in db_url:
        parts = db_url.split('@')
        if '://' in parts[0]:
            creds = parts[0].split('://')[-1]
            if ':' in creds:
                user = creds.split(':')[0]
                masked_url = f"{parts[0].split('://')[0]}://{user}:****@{parts[1]}"
                print(f"✅ DATABASE_URL configured: {masked_url}")
    
    return True

def test_connection():
    """Test database connection."""
    try:
        from src.database import db_config
        
        print("\n🔄 Testing database connection...")
        
        # Test basic connection
        from sqlalchemy import text
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
        # Get database info
        if 'postgresql' in db_config.database_url:
            with db_config.engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.scalar()
                print(f"📊 PostgreSQL version: {version.split(',')[0]}")
                
                result = conn.execute(text("SELECT current_database()"))
                db_name = result.scalar()
                print(f"📁 Database name: {db_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your DATABASE_URL format")
        print("2. Ensure the database server is accessible")
        print("3. Verify your credentials are correct")
        print("4. Check if SSL is required (add ?sslmode=require)")
        return False

def create_tables():
    """Create database tables."""
    try:
        from src.database import init_db
        
        print("\n🔄 Creating database tables...")
        init_db()
        print("✅ Database tables created successfully!")
        
        # List created tables
        from src.database import db_config
        
        if 'postgresql' in db_config.database_url:
            with db_config.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY tablename
                """))
                tables = [row[0] for row in result]
                
                print(f"\n📋 Created tables ({len(tables)}):")
                for table in tables:
                    print(f"   - {table}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Sora AI Platform - Database Setup")
    print("=" * 50)
    
    # Check DATABASE_URL
    if not check_database_url():
        sys.exit(1)
    
    # Test connection
    if not test_connection():
        sys.exit(1)
    
    # Ask user if they want to create tables
    print("\n" + "=" * 50)
    response = input("Do you want to create/update database tables? (y/N): ")
    
    if response.lower() == 'y':
        if create_tables():
            print("\n✅ Database setup completed successfully!")
            print("\nYou can now run the application with:")
            print("  python3 app.py")
        else:
            sys.exit(1)
    else:
        print("\nDatabase tables not created. Run this script again when ready.")

if __name__ == "__main__":
    main()