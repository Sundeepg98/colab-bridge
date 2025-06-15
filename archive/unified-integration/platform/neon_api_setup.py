#!/usr/bin/env python3
"""
Set up Neon PostgreSQL using API key.
"""

import os
import requests
import json
import time
from dotenv import load_dotenv, set_key
from sqlalchemy import text

NEON_API_KEY = "napi_s8buji2qmt4ht1zg1a7rw9je2er18bkale1w0glskg7918l6cmynnjvu1cb8iyh5"
NEON_API_URL = "https://console.neon.tech/api/v2"

def create_neon_project():
    """Create a new Neon project using API."""
    
    print("🚀 Creating Neon PostgreSQL Database")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Create project
    project_data = {
        "project": {
            "name": "ai-integration-platform",
            "region_id": "aws-us-east-2"  # US East region
        }
    }
    
    print("\n🔄 Creating Neon project...")
    
    try:
        response = requests.post(
            f"{NEON_API_URL}/projects",
            headers=headers,
            json=project_data
        )
        
        if response.status_code == 201:
            project = response.json()
            project_id = project['project']['id']
            
            print(f"✅ Project created: {project['project']['name']}")
            print(f"📊 Project ID: {project_id}")
            
            # Get connection details
            print("\n🔄 Getting connection details...")
            
            # Wait a moment for project to be fully created
            time.sleep(2)
            
            # Get project details again to ensure it's ready
            project_response = requests.get(
                f"{NEON_API_URL}/projects/{project_id}",
                headers=headers
            )
            
            if project_response.status_code == 200:
                project_details = project_response.json()
                
                # Get connection URI directly from the response
                if 'connection_uris' in project_details['project']:
                    connection_uri = project_details['project']['connection_uris'][0]['connection_uri']
                    return connection_uri, project_id
                
                # Alternative: construct from project details
                databases = project_details['project'].get('databases', [])
                endpoints = project_details['project'].get('endpoints', [])
                roles = project_details['project'].get('roles', [])
                
                if databases and endpoints and roles:
                    db_name = databases[0]['name']
                    host = endpoints[0]['host']
                    role_name = roles[0]['name']
                    password = roles[0].get('password', '')
                    
                    if not password:
                        # Get role details
                        roles_response = requests.get(
                            f"{NEON_API_URL}/projects/{project_id}/roles",
                            headers=headers
                        )
                        if roles_response.status_code == 200:
                            roles_data = roles_response.json()
                            if roles_data['roles']:
                                password = roles_data['roles'][0].get('password', '')
                
                # Get database
                db_response = requests.get(
                    f"{NEON_API_URL}/projects/{project_id}/databases",
                    headers=headers
                )
                
                if db_response.status_code == 200:
                    databases = db_response.json()
                    db_name = databases['databases'][0]['name']
                    
                    # Get endpoint
                    endpoints_response = requests.get(
                        f"{NEON_API_URL}/projects/{project_id}/endpoints",
                        headers=headers
                    )
                    
                    if endpoints_response.status_code == 200:
                        endpoints = endpoints_response.json()
                        host = endpoints['endpoints'][0]['host']
                        
                        # Construct connection string
                        connection_string = f"postgresql://{default_role}:{password}@{host}/{db_name}?sslmode=require"
                        
                        print(f"\n✅ Database ready!")
                        print(f"🏷️  Name: {db_name}")
                        print(f"👤 User: {default_role}")
                        print(f"🌐 Host: {host}")
                        
                        return connection_string, project_id
                    
        else:
            print(f"❌ Failed to create project: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ API Error: {e}")
    
    return None, None

def configure_database(connection_string):
    """Configure the database connection."""
    
    print("\n🔄 Configuring database connection...")
    
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
        
        # Force reload with new connection
        db_config.database_url = connection_string
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Connected to Neon PostgreSQL!")
            print(f"🐘 Version: {version.split()[1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def create_tables():
    """Create database tables."""
    
    print("\n🔄 Creating database tables...")
    
    try:
        from src.database import init_db, db_config
        
        # Initialize database
        init_db()
        
        # List tables
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    """Main setup process."""
    
    print("🎯 Setting up Neon PostgreSQL with your API key\n")
    
    # Create project
    connection_string, project_id = create_neon_project()
    
    if connection_string:
        # Configure database
        if configure_database(connection_string):
            # Create tables
            if create_tables():
                print("\n" + "="*50)
                print("🎉 SUCCESS! Your Neon PostgreSQL is ready!")
                print("\n📊 Database Details:")
                print(f"   Project ID: {project_id}")
                print("   Storage: 3GB (Free tier)")
                print("   Region: US East (AWS)")
                print("   Features: Auto-backups, SSL, Branching")
                
                print("\n🔗 Neon Dashboard:")
                print("   https://console.neon.tech/app/projects")
                print("   (Sign in to see your project)")
                
                print("\n🚀 Next Steps:")
                print("1. Restart your application:")
                print("   python3 app.py")
                print("\n2. Your app now uses Neon PostgreSQL!")
                
                # Save project info
                project_info = {
                    "project_id": project_id,
                    "connection_string": connection_string,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                with open('neon_project.json', 'w') as f:
                    json.dump(project_info, f, indent=2)
                
                print("\n📄 Project details saved to: neon_project.json")
                
                return True
    
    print("\n❌ Setup failed")
    return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)