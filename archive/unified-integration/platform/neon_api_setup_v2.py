#!/usr/bin/env python3
"""
Set up Neon PostgreSQL using API key - Version 2.
"""

import os
import requests
import json
import time
from dotenv import load_dotenv, set_key
from sqlalchemy import text

NEON_API_KEY = "napi_s8buji2qmt4ht1zg1a7rw9je2er18bkale1w0glskg7918l6cmynnjvu1cb8iyh5"
NEON_API_URL = "https://console.neon.tech/api/v2"

def get_existing_projects():
    """Check for existing projects."""
    
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Checking existing projects...")
    
    try:
        response = requests.get(f"{NEON_API_URL}/projects", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            for project in projects.get('projects', []):
                if project['name'] == 'ai-integration-platform':
                    print(f"✅ Found existing project: {project['name']}")
                    return project['id']
    except Exception as e:
        print(f"⚠️ Error checking projects: {e}")
    
    return None

def get_connection_string(project_id):
    """Get connection string for a project."""
    
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print(f"\n🔄 Getting connection details for project: {project_id}")
    
    try:
        # Get project details
        response = requests.get(f"{NEON_API_URL}/projects/{project_id}", headers=headers)
        
        if response.status_code == 200:
            project = response.json()['project']
            
            # Get endpoints
            endpoints_response = requests.get(
                f"{NEON_API_URL}/projects/{project_id}/endpoints",
                headers=headers
            )
            
            if endpoints_response.status_code == 200:
                endpoints = endpoints_response.json()['endpoints']
                if endpoints:
                    endpoint = endpoints[0]
                    host = endpoint['host']
                    
                    # Get databases
                    db_response = requests.get(
                        f"{NEON_API_URL}/projects/{project_id}/databases",
                        headers=headers
                    )
                    
                    if db_response.status_code == 200:
                        databases = db_response.json()['databases']
                        if databases:
                            db_name = databases[0]['name']
                            
                            # Get roles
                            roles_response = requests.get(
                                f"{NEON_API_URL}/projects/{project_id}/roles",
                                headers=headers
                            )
                            
                            if roles_response.status_code == 200:
                                roles = roles_response.json()['roles']
                                if roles:
                                    role = roles[0]
                                    role_name = role['name']
                                    
                                    # Get password
                                    password_response = requests.get(
                                        f"{NEON_API_URL}/projects/{project_id}/roles/{role_name}/reveal-password",
                                        headers=headers
                                    )
                                    
                                    if password_response.status_code == 200:
                                        password = password_response.json()['password']
                                    else:
                                        # Try to reset password
                                        print("🔄 Resetting role password...")
                                        reset_response = requests.post(
                                            f"{NEON_API_URL}/projects/{project_id}/roles/{role_name}/reset-password",
                                            headers=headers
                                        )
                                        if reset_response.status_code == 200:
                                            password = reset_response.json()['role']['password']
                                        else:
                                            password = "password"
                                    
                                    connection_string = f"postgresql://{role_name}:{password}@{host}/{db_name}?sslmode=require"
                                    
                                    print(f"✅ Got connection details!")
                                    print(f"🏷️  Database: {db_name}")
                                    print(f"👤 User: {role_name}")
                                    print(f"🌐 Host: {host}")
                                    
                                    return connection_string
        
    except Exception as e:
        print(f"❌ Error getting connection string: {e}")
    
    return None

def create_new_project():
    """Create a new Neon project."""
    
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    
    project_data = {
        "project": {
            "name": "ai-integration-platform",
            "region_id": "aws-us-east-2"
        }
    }
    
    print("\n🔄 Creating new Neon project...")
    
    try:
        response = requests.post(
            f"{NEON_API_URL}/projects",
            headers=headers,
            json=project_data
        )
        
        if response.status_code == 201:
            project = response.json()['project']
            project_id = project['id']
            print(f"✅ Project created: {project['name']}")
            print(f"📊 Project ID: {project_id}")
            
            # Wait for project to be ready
            print("⏳ Waiting for project to be ready...")
            time.sleep(5)
            
            return project_id
        else:
            print(f"❌ Failed to create project: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error creating project: {e}")
    
    return None

def configure_and_test(connection_string):
    """Configure database and test connection."""
    
    print("\n🔄 Configuring database...")
    
    # Update .env
    env_path = '.env'
    set_key(env_path, 'DATABASE_URL', connection_string)
    set_key(env_path, 'NEON_API_KEY', NEON_API_KEY)
    
    # Reload environment
    load_dotenv(override=True)
    
    print("✅ Configuration updated!")
    
    # Test connection
    print("\n🔄 Testing connection...")
    try:
        from src.database import db_config
        
        # Force reload
        db_config.database_url = connection_string
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Connected to Neon PostgreSQL!")
            print(f"🐘 Version: {version.split()[1]}")
        
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
    """Main setup process."""
    
    print("🎯 Setting up Neon PostgreSQL with your API key\n")
    
    # Check for existing project
    project_id = get_existing_projects()
    
    # Create new project if needed
    if not project_id:
        project_id = create_new_project()
    
    if project_id:
        # Get connection string
        connection_string = get_connection_string(project_id)
        
        if connection_string:
            # Configure and test
            if configure_and_test(connection_string):
                print("\n" + "="*50)
                print("🎉 SUCCESS! Your Neon PostgreSQL is ready!")
                print("\n📊 Database Details:")
                print(f"   Project ID: {project_id}")
                print("   Storage: 3GB (Free tier)")
                print("   Region: US East (AWS)")
                
                print("\n🚀 Next Steps:")
                print("1. Restart your application:")
                print("   python3 app.py")
                
                # Save details
                with open('neon_project.json', 'w') as f:
                    json.dump({
                        "project_id": project_id,
                        "connection_string": connection_string,
                        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    }, f, indent=2)
                
                return True
    
    print("\n❌ Setup failed")
    return False

if __name__ == "__main__":
    main()