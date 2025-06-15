#!/usr/bin/env python3
"""
Finalize Neon setup after getting connection string.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import text

def test_and_setup():
    """Test connection and create tables."""
    
    print("🚀 Finalizing Neon PostgreSQL Setup")
    print("=" * 50)
    
    # Load current config
    load_dotenv()
    connection_string = os.getenv('DATABASE_URL', '')
    
    if not connection_string or 'neon_password' in connection_string:
        print("\n❌ Please update DATABASE_URL in .env with your actual connection string")
        print("\n📋 Instructions:")
        print("1. Get your connection string from:")
        print("   https://console.neon.tech/app/projects/spring-paper-60199096")
        print("\n2. Update .env file with the actual connection string")
        print("\n3. Run this script again")
        return False
    
    print(f"\n🔄 Testing connection...")
    print(f"🌐 Host: {connection_string.split('@')[1].split('/')[0]}")
    
    try:
        from src.database import db_config
        
        # Force reload
        db_config.database_url = connection_string
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT version(), current_database()"))
            version, db_name = result.fetchone()
            print(f"\n✅ Connected successfully!")
            print(f"🐘 PostgreSQL: {version.split()[1]}")
            print(f"📁 Database: {db_name}")
        
        # Create tables
        print("\n🔄 Creating tables...")
        from src.database import init_db
        init_db()
        
        # List tables
        with db_config.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """))
            tables = [row[0] for row in result]
            
            print(f"\n✅ Created {len(tables)} tables:")
            for table in tables:
                print(f"   ✓ {table}")
            
            # Show database size
            result = conn.execute(text("""
                SELECT pg_database_size(current_database()) / 1024 / 1024 as size_mb
            """))
            size_mb = result.scalar()
            print(f"\n💾 Database size: {size_mb:.2f} MB / 3072 MB")
            print(f"📊 Usage: {(size_mb/3072)*100:.1f}% of free tier")
        
        print("\n" + "="*50)
        print("🎉 SUCCESS! Your Neon PostgreSQL is fully configured!")
        print("\n🚀 Next Steps:")
        print("1. Stop current app (if running)")
        print("2. Restart: python3 app.py")
        print("\n✨ Your app now uses Neon PostgreSQL!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you copied the ENTIRE connection string")
        print("2. Check that password is included (click 'Show password')")
        print("3. Try the 'Direct connection' option in Neon dashboard")
        return False

if __name__ == "__main__":
    if not test_and_setup():
        print("\n📄 See NEON_MANUAL_SETUP.md for detailed instructions")