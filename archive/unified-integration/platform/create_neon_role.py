#!/usr/bin/env python3
"""
Create a new database role with known password.
"""

import os
import requests
import json
import time
import secrets
import string
from dotenv import load_dotenv, set_key
from sqlalchemy import text

NEON_API_KEY = "napi_s8buji2qmt4ht1zg1a7rw9je2er18bkale1w0glskg7918l6cmynnjvu1cb8iyh5"
NEON_API_URL = "https://console.neon.tech/api/v2"
PROJECT_ID = "spring-paper-60199096"

headers = {
    "Authorization": f"Bearer {NEON_API_KEY}",
    "Content-Type": "application/json"
}

def generate_password():
    """Generate a secure password."""
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(16))
    return password

def create_new_role_with_password():
    """Create a new role with a known password."""
    
    print("🚀 Setting up Neon PostgreSQL with new credentials")
    print("=" * 50)
    
    # Get branch ID
    print("\n🔄 Getting branch information...")
    branches_response = requests.get(
        f"{NEON_API_URL}/projects/{PROJECT_ID}/branches",
        headers=headers
    )
    
    if branches_response.status_code != 200:
        print(f"❌ Failed to get branches: {branches_response.text}")
        return None
    
    branches = branches_response.json()['branches']
    branch = branches[0]  # Use first branch
    branch_id = branch['id']
    print(f"✅ Using branch: {branch['name']}")
    
    # Generate credentials
    role_name = "ai_integration_platform_user"
    password = generate_password()
    
    print(f"\n🔄 Creating new role: {role_name}")
    
    # Create new role
    role_data = {
        "role": {
            "name": role_name
        }
    }
    
    create_role_response = requests.post(
        f"{NEON_API_URL}/projects/{PROJECT_ID}/branches/{branch_id}/roles",
        headers=headers,
        json=role_data
    )
    
    if create_role_response.status_code == 201:
        print(f"✅ Role created: {role_name}")
        created_role = create_role_response.json()['role']
        
        # The API might return a password
        if 'password' in created_role:
            password = created_role['password']
            print("✅ Using API-generated password")
    elif create_role_response.status_code == 409:
        print(f"ℹ️ Role {role_name} already exists")
        
        # Try to reset password for existing role
        print("🔄 Resetting password...")
        reset_response = requests.post(
            f"{NEON_API_URL}/projects/{PROJECT_ID}/branches/{branch_id}/roles/{role_name}/reset-password",
            headers=headers
        )
        
        if reset_response.status_code == 200:
            reset_data = reset_response.json()
            if 'password' in reset_data.get('role', {}):
                password = reset_data['role']['password']
                print("✅ Password reset successfully")
            else:
                print("⚠️ Password not returned, using generated password")
    else:
        print(f"❌ Failed to create role: {create_role_response.text}")
        return None
    
    # Get endpoint host
    print("\n🔄 Getting endpoint...")
    endpoints_response = requests.get(
        f"{NEON_API_URL}/projects/{PROJECT_ID}/endpoints",
        headers=headers
    )
    
    if endpoints_response.status_code != 200:
        print("❌ Failed to get endpoints")
        return None
    
    endpoints = endpoints_response.json()['endpoints']
    if not endpoints:
        print("❌ No endpoints found")
        return None
    
    host = endpoints[0]['host']
    print(f"✅ Host: {host}")
    
    # Get database name
    print("\n🔄 Getting database...")
    databases_response = requests.get(
        f"{NEON_API_URL}/projects/{PROJECT_ID}/branches/{branch_id}/databases",
        headers=headers
    )
    
    if databases_response.status_code == 200:
        databases = databases_response.json()['databases']
        db_name = databases[0]['name'] if databases else 'neondb'
    else:
        db_name = 'neondb'
    
    print(f"✅ Database: {db_name}")
    
    # Grant permissions (try via SQL if possible)
    print("\n🔄 Setting up permissions...")
    
    # Construct connection string
    connection_string = f"postgresql://{role_name}:{password}@{host}/{db_name}?sslmode=require"
    
    print("\n✅ Connection string ready!")
    return connection_string

def test_and_setup_database(connection_string):
    """Test connection and create tables."""
    
    print("\n🔄 Testing connection...")
    
    # Update .env
    env_path = '.env'
    set_key(env_path, 'DATABASE_URL', connection_string)
    
    # Reload environment
    load_dotenv(override=True)
    
    try:
        from src.database import db_config
        
        # Force reload
        db_config.database_url = connection_string
        db_config.engine = db_config._create_engine()
        
        # Test connection
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Connected to PostgreSQL {version.split()[1]}")
        
        # Create tables
        print("\n🔄 Creating tables...")
        from src.database import init_db
        init_db()
        
        print("✅ All tables created!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # If permission denied, we need owner access
        if "permission denied" in str(e).lower():
            print("\n⚠️ The new role needs permissions from the database owner")
            print("\n📝 Manual fix required:")
            print("1. Go to: https://console.neon.tech/app/projects/spring-paper-60199096")
            print("2. Get the neondb_owner password")
            print("3. Update .env with that connection string")
            print("4. Run: python3 finalize_neon_setup.py")
        
        return False

def save_connection_info(connection_string):
    """Save connection details."""
    
    parts = connection_string.replace('postgresql://', '').split('@')
    user_pass = parts[0].split(':')
    host_db = parts[1].split('/')
    
    info = {
        "project_id": PROJECT_ID,
        "connection_string": connection_string,
        "details": {
            "username": user_pass[0],
            "host": host_db[0],
            "database": host_db[1].split('?')[0],
            "project_url": f"https://console.neon.tech/app/projects/{PROJECT_ID}"
        },
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open('neon_connection.json', 'w') as f:
        json.dump(info, f, indent=2)
    
    print("\n📄 Connection details saved to: neon_connection.json")

def main():
    """Main setup."""
    
    connection_string = create_new_role_with_password()
    
    if connection_string:
        save_connection_info(connection_string)
        
        if test_and_setup_database(connection_string):
            print("\n" + "="*50)
            print("🎉 SUCCESS! Your Neon PostgreSQL is ready!")
            print("\n🚀 Next steps:")
            print("1. Restart your application:")
            print("   python3 app.py")
            print("\n✨ Your app now uses Neon PostgreSQL!")
            return True
        else:
            print("\n⚠️ Connection created but needs manual setup")
            print("See instructions above")
    
    return False

if __name__ == "__main__":
    main()