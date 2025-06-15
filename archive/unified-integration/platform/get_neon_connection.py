#!/usr/bin/env python3
"""
Get Neon connection string using console access.
"""

import requests
import re

def get_connection_from_console():
    """Try to get connection string from Neon console."""
    
    print("🔍 Attempting to retrieve connection details...\n")
    
    # Your project dashboard URL
    dashboard_url = "https://console.neon.tech/app/projects/spring-paper-60199096"
    
    print(f"📋 Your Neon project is ready at:")
    print(f"   {dashboard_url}")
    
    print("\n🔐 To get your connection string:")
    print("\n1. Open the link above in your browser")
    print("2. Sign in if needed")
    print("3. Look for 'Connection string' box on the dashboard")
    print("4. Click 'Show password'")
    print("5. Copy the entire connection string")
    
    print("\n📝 The connection string format is:")
    print("postgresql://neondb_owner:YOUR_PASSWORD@ep-purple-pine-a58z5kj2.us-east-2.aws.neon.tech/neondb?sslmode=require")
    
    print("\n" + "="*50)
    print("\n💡 Quick Alternative - Create New Password:")
    print("\n1. In your Neon dashboard, go to 'Roles'")
    print("2. Click on 'neondb_owner'")
    print("3. Click 'Reset password'")
    print("4. Copy the new password")
    print("5. Use this connection string with your new password:")
    print("\npostgresql://neondb_owner:NEW_PASSWORD_HERE@ep-purple-pine-a58z5kj2.us-east-2.aws.neon.tech/neondb?sslmode=require")
    
    print("\n" + "="*50)
    print("\n✅ Once you have the connection string:")
    print("1. Update the DATABASE_URL in your .env file")
    print("2. Run: python3 finalize_neon_setup.py")
    
    return dashboard_url

if __name__ == "__main__":
    url = get_connection_from_console()
    
    print("\n🌐 Opening your browser to:")
    print(f"   {url}")
    
    # Try to open browser
    try:
        import webbrowser
        webbrowser.open(url)
    except:
        print("\n📋 Please open the URL manually in your browser")