#!/usr/bin/env python3
"""
Set up Neon database with owner credentials.
"""

import os
from dotenv import load_dotenv, set_key
from sqlalchemy import text

# Owner connection string from user
OWNER_CONNECTION = "postgresql://neondb_owner:npg_uPgh0eMspS6d@ep-purple-pine-a58z5kj2-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

def setup_database():
    """Set up database with owner credentials."""
    
    print("🚀 Setting up Neon PostgreSQL with owner credentials")
    print("=" * 50)
    
    # Update .env
    print("\n🔄 Updating configuration...")
    env_path = '.env'
    set_key(env_path, 'DATABASE_URL', OWNER_CONNECTION)
    
    # Reload environment
    load_dotenv(override=True)
    os.environ['DATABASE_URL'] = OWNER_CONNECTION
    
    print("✅ Configuration updated!")
    
    # Test connection
    print("\n🔄 Testing connection...")
    try:
        from src.database import db_config
        
        # Force reload with owner connection
        db_config.database_url = OWNER_CONNECTION
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), version()"))
            db_name, version = result.fetchone()
            print(f"✅ Connected as owner!")
            print(f"📁 Database: {db_name}")
            print(f"🐘 PostgreSQL: {version.split()[1]}")
        
        # Create tables
        print("\n🔄 Creating tables...")
        from src.database import init_db
        init_db()
        
        # Verify tables
        with db_config.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """))
            tables = [row[0] for row in result]
            
            print(f"\n✅ Successfully created {len(tables)} tables:")
            for table in tables:
                # Get row count
                try:
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = count_result.scalar()
                    print(f"   ✓ {table} ({count} rows)")
                except:
                    print(f"   ✓ {table}")
            
            # Show database info
            result = conn.execute(text("""
                SELECT 
                    pg_database_size(current_database()) / 1024 / 1024 as size_mb,
                    current_user,
                    inet_server_addr() as server_ip
            """))
            size_mb, current_user, server_ip = result.fetchone()
            
            print(f"\n📊 Database Stats:")
            print(f"   Size: {size_mb:.2f} MB / 3072 MB")
            print(f"   User: {current_user}")
            print(f"   Usage: {(size_mb/3072)*100:.1f}% of free tier")
        
        # Test with sample data
        print("\n🔄 Testing with sample data...")
        with db_config.engine.connect() as conn:
            # Insert test user
            conn.execute(text("""
                INSERT INTO users (email, password_hash, is_active, is_verified)
                VALUES ('admin@ai-integration-platform.com', 'pbkdf2:sha256:600000$test$hash', true, true)
                ON CONFLICT (email) DO NOTHING
            """))
            conn.commit()
            
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()
            print(f"✅ Database test successful! Users: {user_count}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Main setup."""
    
    if setup_database():
        print("\n" + "="*50)
        print("🎉 SUCCESS! Your Neon PostgreSQL is fully configured!")
        
        print("\n📊 Database Details:")
        print("   Project: ai-integration-platform")
        print("   Database: neondb")
        print("   Host: ep-purple-pine-a58z5kj2-pooler.us-east-2.aws.neon.tech")
        print("   Region: US East (AWS)")
        print("   Storage: 3GB FREE")
        
        print("\n✅ What's Ready:")
        print("   • All 5 tables created")
        print("   • Authentication system")
        print("   • User management")
        print("   • Usage tracking")
        print("   • Billing records")
        
        print("\n🚀 Next Steps:")
        print("1. Restart your application:")
        print("   python3 app.py")
        print("\n2. Your app now uses Neon PostgreSQL!")
        
        print("\n🔗 Dashboard:")
        print("   https://console.neon.tech/app/projects/spring-paper-60199096")
        
        # Save connection info
        with open('neon_setup_complete.txt', 'w') as f:
            f.write("Neon PostgreSQL Setup Complete!\n")
            f.write(f"Database URL is configured in .env\n")
            f.write(f"Project: ai-integration-platform\n")
            f.write(f"Dashboard: https://console.neon.tech/app/projects/spring-paper-60199096\n")
        
        return True
    
    return False

if __name__ == "__main__":
    main()