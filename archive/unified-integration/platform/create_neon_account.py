#!/usr/bin/env python3
"""
Guide to create Neon account and set up database.
"""

import os
import time
import json
from dotenv import load_dotenv, set_key

def create_setup_instructions():
    """Create detailed setup instructions."""
    
    print("🚀 Let's Set Up Your FREE Neon PostgreSQL")
    print("=" * 50)
    
    print("\n📝 I'll create a step-by-step guide for you...")
    time.sleep(1)
    
    # Create HTML guide
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Neon PostgreSQL Setup</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .step {
            background: #f4f4f4;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        code {
            background: #333;
            color: #fff;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        .connection-string {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            word-break: break-all;
            font-family: monospace;
            margin: 10px 0;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        .warning {
            background: #fff3cd;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
        }
    </style>
</head>
<body>
    <h1>🚀 Neon PostgreSQL Setup Guide</h1>
    
    <div class="step">
        <h2>Step 1: Create Your FREE Neon Account</h2>
        <p>Click the button below to open Neon's signup page:</p>
        <button onclick="window.open('https://console.neon.tech/signup', '_blank')">
            Open Neon Signup →
        </button>
        <p><small>Or visit: <code>https://console.neon.tech/signup</code></small></p>
    </div>
    
    <div class="step">
        <h2>Step 2: Sign Up (30 seconds)</h2>
        <ul>
            <li>Click <strong>"Sign up with GitHub"</strong> (fastest)</li>
            <li>Or use your email</li>
            <li>It's completely FREE - no credit card needed!</li>
        </ul>
    </div>
    
    <div class="step">
        <h2>Step 3: Get Your Connection String</h2>
        <p>After signup, you'll see your dashboard with a connection box:</p>
        <ol>
            <li>Look for <strong>"Connection string"</strong> section</li>
            <li>Click <strong>"Show password"</strong></li>
            <li>Click the <strong>copy button</strong> to copy the entire string</li>
        </ol>
        <p>It will look like this:</p>
        <div class="connection-string">
            postgresql://username:password@ep-something-123456.us-east-2.aws.neon.tech/neondb
        </div>
    </div>
    
    <div class="step">
        <h2>Step 4: Configure Your App</h2>
        <p>Once you have your connection string:</p>
        <ol>
            <li>Return to your terminal</li>
            <li>Run: <code>python3 complete_neon_setup.py</code></li>
            <li>Paste your connection string when prompted</li>
        </ol>
    </div>
    
    <div class="warning">
        <strong>⚠️ Important:</strong> Make sure to copy the ENTIRE connection string including the password!
    </div>
    
    <div class="step" style="background: #e8f5e9;">
        <h2>✅ What You Get for FREE:</h2>
        <ul>
            <li>3GB storage (enough for ~1 million records)</li>
            <li>Always-on database</li>
            <li>Automatic daily backups</li>
            <li>SSL encryption</li>
            <li>Database branching</li>
            <li>No credit card required</li>
        </ul>
    </div>
</body>
</html>"""
    
    # Save HTML guide
    with open('neon_setup_guide.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Created visual guide: neon_setup_guide.html")
    
    # Create the completion script
    completion_script = '''#!/usr/bin/env python3
"""
Complete Neon setup after getting connection string.
"""

import os
from dotenv import load_dotenv, set_key
from sqlalchemy import text

def complete_neon_setup():
    """Complete setup with user's connection string."""
    
    print("\\n🎯 Neon PostgreSQL Configuration")
    print("=" * 50)
    
    print("\\nPaste your Neon connection string below:")
    print("(It starts with postgresql:// and includes your password)\\n")
    
    connection_string = input("> ").strip().strip('"\'')
    
    if not connection_string or not connection_string.startswith("postgresql://"):
        print("\\n❌ Invalid connection string!")
        return False
    
    # Ensure SSL
    if "sslmode=" not in connection_string:
        connection_string += "?sslmode=require" if "?" not in connection_string else "&sslmode=require"
    
    # Update .env
    print("\\n🔄 Updating configuration...")
    set_key('.env', 'DATABASE_URL', connection_string)
    
    # Reload and test
    load_dotenv(override=True)
    
    print("🔄 Testing connection...")
    try:
        from src.database import db_config
        db_config.database_url = connection_string
        db_config.engine = db_config._create_engine()
        
        with db_config.engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"\\n✅ Connected to Neon PostgreSQL!")
            print(f"🐘 Version: {version.split()[1]}")
        
        # Create tables
        print("\\n🔄 Creating tables...")
        from src.database import init_db
        init_db()
        print("✅ All tables created!")
        
        print("\\n🎉 SUCCESS! Your Neon PostgreSQL is ready!")
        print("\\n🚀 Restart your app: python3 app.py")
        return True
        
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    complete_neon_setup()
'''
    
    with open('complete_neon_setup.py', 'w') as f:
        f.write(completion_script)
    
    os.chmod('complete_neon_setup.py', 0o755)
    print("✅ Created setup completion script: complete_neon_setup.py")
    
    # Show instructions
    print("\n" + "="*50)
    print("📋 NEXT STEPS:")
    print("\n1️⃣ Open the visual guide:")
    print("   • File: neon_setup_guide.html")
    print("   • Or visit: https://console.neon.tech/signup")
    
    print("\n2️⃣ Create your FREE Neon account (1 minute)")
    
    print("\n3️⃣ Copy your connection string from the dashboard")
    
    print("\n4️⃣ Run the completion script:")
    print("   python3 complete_neon_setup.py")
    
    print("\n" + "="*50)
    print("💡 Need the direct link?")
    print("   https://console.neon.tech/signup")
    
    return True

def open_guide():
    """Try to open the HTML guide."""
    import webbrowser
    import os
    
    try:
        file_path = os.path.abspath('neon_setup_guide.html')
        webbrowser.open(f'file://{file_path}')
        print("\n🌐 Opened guide in browser!")
    except:
        print("\n📄 Open neon_setup_guide.html in your browser")

if __name__ == "__main__":
    if create_setup_instructions():
        print("\n🎯 Ready to set up Neon!")
        print("\nWould you like me to open the guide in your browser?")
        # Auto-open after creating
        try:
            time.sleep(1)
            open_guide()
        except:
            pass