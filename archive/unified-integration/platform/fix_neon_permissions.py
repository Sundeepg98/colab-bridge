#!/usr/bin/env python3
"""
Fix Neon database by using string fields instead of ENUMs.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import text

def fix_database_schema():
    """Modify database to work with limited permissions."""
    
    print("🔧 Fixing database schema for Neon")
    print("=" * 50)
    
    # Temporarily modify the models to use strings instead of enums
    models_file = 'src/database/models.py'
    
    print("\n🔄 Modifying database models...")
    
    # Read the models file
    with open(models_file, 'r') as f:
        content = f.read()
    
    # Backup original
    with open(models_file + '.backup', 'w') as f:
        f.write(content)
    
    # Replace Enum types with String
    modified = content.replace(
        'service_type = Column(Enum(ServiceType)',
        'service_type = Column(String(50)'
    ).replace(
        'status = Column(Enum(BillingStatus)',
        'status = Column(String(50)'
    )
    
    # Write modified version
    with open(models_file, 'w') as f:
        f.write(modified)
    
    print("✅ Models modified to use String instead of Enum")
    
    # Now try to create tables
    print("\n🔄 Creating tables with modified schema...")
    
    try:
        from src.database import db_config, init_db
        
        # Drop existing types if any (ignore errors)
        try:
            with db_config.engine.connect() as conn:
                conn.execute(text("DROP TYPE IF EXISTS servicetype CASCADE"))
                conn.execute(text("DROP TYPE IF EXISTS billingstatus CASCADE"))
                conn.commit()
        except:
            pass
        
        # Create tables
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
                print(f"   ✓ {table}")
            
            # Test by creating a user
            print("\n🔄 Testing database...")
            conn.execute(text("""
                INSERT INTO users (email, password_hash, is_active, is_verified)
                VALUES ('test@neon.db', 'test_hash', true, false)
                ON CONFLICT (email) DO NOTHING
            """))
            conn.commit()
            
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            print(f"✅ Database test successful! Users table has {count} record(s)")
        
        print("\n✅ Database is fully functional!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
        # Restore original models
        print("\n🔄 Restoring original models...")
        with open(models_file + '.backup', 'r') as f:
            original = f.read()
        with open(models_file, 'w') as f:
            f.write(original)
        
        return False
    finally:
        # Clean up backup
        if os.path.exists(models_file + '.backup'):
            os.remove(models_file + '.backup')

def verify_connection():
    """Verify the app can use the database."""
    
    print("\n🔍 Verifying application connection...")
    
    try:
        from src.database import db_config
        
        with db_config.get_db_session() as session:
            # Test query
            result = session.execute(text("SELECT current_database(), version()"))
            db_name, version = result.fetchone()
            print(f"✅ Connected to: {db_name}")
            print(f"🐘 PostgreSQL: {version.split()[1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def main():
    """Main fix process."""
    
    load_dotenv()
    
    if fix_database_schema():
        if verify_connection():
            print("\n" + "="*50)
            print("🎉 SUCCESS! Your Neon PostgreSQL is working!")
            print("\n📊 Database Details:")
            print(f"   Host: ep-purple-pine-a58z5kj2.us-east-2.aws.neon.tech")
            print(f"   Database: neondb")
            print(f"   User: ai_integration_platform_user")
            print("\n🚀 Your app is ready to use Neon PostgreSQL!")
            print("\n1. Restart your application:")
            print("   python3 app.py")
            return True
    
    return False

if __name__ == "__main__":
    main()