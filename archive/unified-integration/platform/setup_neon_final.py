#!/usr/bin/env python3
"""
Final Neon setup with proper connection details.
"""

import os
import requests
import json
import time
from dotenv import load_dotenv, set_key
from sqlalchemy import text

NEON_API_KEY = "napi_s8buji2qmt4ht1zg1a7rw9je2er18bkale1w0glskg7918l6cmynnjvu1cb8iyh5"
NEON_API_URL = "https://console.neon.tech/api/v2"
PROJECT_ID = "spring-paper-60199096"

headers = {
    "Authorization": f"Bearer {NEON_API_KEY}",
    "Content-Type": "application/json"
}

def get_connection_details():
    """Get all connection details step by step."""
    
    print("🚀 Setting up Neon PostgreSQL")
    print("=" * 50)
    print(f"\n📊 Project: ai-integration-platform")
    print(f"🆔 ID: {PROJECT_ID}")
    
    # Get branches (default branch contains the database)
    print("\n🔄 Getting database branch...")
    branches_response = requests.get(
        f"{NEON_API_URL}/projects/{PROJECT_ID}/branches",
        headers=headers
    )
    
    if branches_response.status_code != 200:
        print(f"❌ Failed to get branches: {branches_response.text}")
        return None
    
    branches = branches_response.json()['branches']
    default_branch = next((b for b in branches if b.get('default', False)), branches[0])
    branch_id = default_branch['id']
    print(f"✅ Branch: {default_branch['name']} ({branch_id})")
    
    # Get endpoints
    print("\n🔄 Getting endpoints...")
    endpoints_response = requests.get(
        f"{NEON_API_URL}/projects/{PROJECT_ID}/endpoints",
        headers=headers
    )
    
    if endpoints_response.status_code != 200:
        # Create endpoint if it doesn't exist
        print("📝 Creating endpoint...")
        endpoint_data = {
            "endpoint": {
                "type": "read_write",
                "branch_id": branch_id
            }
        }
        create_response = requests.post(
            f"{NEON_API_URL}/projects/{PROJECT_ID}/endpoints",
            headers=headers,
            json=endpoint_data
        )
        if create_response.status_code == 201:
            print("✅ Endpoint created")
            time.sleep(5)  # Wait for endpoint to be ready
            endpoints_response = requests.get(
                f"{NEON_API_URL}/projects/{PROJECT_ID}/endpoints",
                headers=headers
            )
    
    endpoints = endpoints_response.json()['endpoints']
    if not endpoints:
        print("❌ No endpoints found")
        return None
    
    endpoint = endpoints[0]
    host = endpoint['host']
    print(f"✅ Host: {host}")
    
    # Get databases
    print("\n🔄 Getting databases...")
    databases_response = requests.get(
        f"{NEON_API_URL}/projects/{PROJECT_ID}/branches/{branch_id}/databases",
        headers=headers
    )
    
    if databases_response.status_code != 200:
        print(f"❌ Failed to get databases: {databases_response.text}")
        return None
    
    databases = databases_response.json()['databases']
    if not databases:
        # Create database
        print("📝 Creating database...")
        db_data = {
            "database": {
                "name": "ai_integration_platform_db",
                "owner_name": "neondb_owner"
            }
        }
        create_db_response = requests.post(
            f"{NEON_API_URL}/projects/{PROJECT_ID}/branches/{branch_id}/databases",
            headers=headers,
            json=db_data
        )
        if create_db_response.status_code == 201:
            print("✅ Database created")
            databases = [create_db_response.json()['database']]
        else:
            databases = [{"name": "neondb", "owner_name": "neondb_owner"}]
    
    database = databases[0]
    db_name = database['name']
    owner_name = database['owner_name']
    print(f"✅ Database: {db_name}")
    print(f"✅ Owner: {owner_name}")
    
    # Get roles
    print("\n🔄 Getting roles...")
    roles_response = requests.get(
        f"{NEON_API_URL}/projects/{PROJECT_ID}/branches/{branch_id}/roles",
        headers=headers
    )
    
    if roles_response.status_code != 200:
        print(f"❌ Failed to get roles: {roles_response.text}")
        return None
    
    roles = roles_response.json()['roles']
    role = next((r for r in roles if r['name'] == owner_name), roles[0] if roles else None)
    
    if not role:
        print("❌ No roles found")
        return None
    
    role_name = role['name']
    print(f"✅ Role: {role_name}")
    
    # Get or reset password
    print("\n🔄 Getting password...")
    password = role.get('password')
    
    if not password:
        # Try to reveal password
        reveal_response = requests.get(
            f"{NEON_API_URL}/projects/{PROJECT_ID}/branches/{branch_id}/roles/{role_name}/reveal-password",
            headers=headers
        )
        
        if reveal_response.status_code == 200:
            password = reveal_response.json()['password']
        else:
            # Reset password
            print("🔄 Resetting password...")
            reset_response = requests.post(
                f"{NEON_API_URL}/projects/{PROJECT_ID}/branches/{branch_id}/roles/{role_name}/reset-password",
                headers=headers
            )
            if reset_response.status_code == 200:
                password = reset_response.json()['role']['password']
                print("✅ Password reset")
    
    if password:
        print("✅ Password obtained")
    else:
        print("⚠️ Using default password")
        password = "neon_password"
    
    # Construct connection string
    connection_string = f"postgresql://{role_name}:{password}@{host}/{db_name}?sslmode=require"
    
    print("\n✅ Connection string ready!")
    return connection_string

def setup_database(connection_string):
    """Configure and test database."""
    
    print("\n🔄 Configuring database...")
    
    # Update .env
    env_path = '.env'
    set_key(env_path, 'DATABASE_URL', connection_string)
    set_key(env_path, 'NEON_API_KEY', NEON_API_KEY)
    set_key(env_path, 'NEON_PROJECT_ID', PROJECT_ID)
    
    # Reload environment
    load_dotenv(override=True)
    
    print("✅ Configuration saved!")
    
    # Test connection
    print("\n🔄 Testing connection...")
    try:
        from src.database import db_config
        
        # Force reload
        db_config.database_url = connection_string
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT version(), current_database()"))
            version, db_name = result.fetchone()
            print(f"✅ Connected to Neon PostgreSQL!")
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main setup."""
    
    connection_string = get_connection_details()
    
    if connection_string:
        if setup_database(connection_string):
            print("\n" + "="*50)
            print("🎉 SUCCESS! Your Neon PostgreSQL is ready!")
            print("\n📊 Database Details:")
            print(f"   Project: ai-integration-platform")
            print(f"   Region: US East (AWS)")
            print(f"   Storage: 3GB (Free tier)")
            print(f"   PostgreSQL: Version 17")
            
            print("\n🚀 Next Steps:")
            print("1. Restart your application:")
            print("   python3 app.py")
            print("\n2. Your app now uses Neon PostgreSQL!")
            
            print("\n🔗 Neon Dashboard:")
            print("   https://console.neon.tech/app/projects/spring-paper-60199096")
            
            # Save details
            with open('neon_connection.json', 'w') as f:
                json.dump({
                    "project_id": PROJECT_ID,
                    "connection_string": connection_string,
                    "api_key": NEON_API_KEY,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }, f, indent=2)
            
            return True
    
    print("\n❌ Setup failed")
    return False

if __name__ == "__main__":
    main()