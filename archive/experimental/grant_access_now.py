#!/usr/bin/env python3
"""
Grant access to the hybrid processor notebook
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.universal_bridge import UniversalColabBridge

def grant_access(user_email="sundeepg8@gmail.com"):
    """Grant access to the user"""
    
    # IDs for sharing
    notebook_file_id = "1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA"
    folder_id = "1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z"
    
    try:
        bridge = UniversalColabBridge("grant_access")
        bridge.initialize()
        
        print(f"🔗 Granting access to: {user_email}")
        
        # Share notebook
        print("📓 Sharing notebook...")
        notebook_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': user_email
        }
        
        bridge.drive_service.permissions().create(
            fileId=notebook_file_id,
            body=notebook_permission,
            sendNotificationEmail=True
        ).execute()
        
        print("✅ Notebook access granted!")
        
        # Share folder
        print("📁 Sharing folder...")
        folder_permission = {
            'type': 'user', 
            'role': 'writer',
            'emailAddress': user_email
        }
        
        bridge.drive_service.permissions().create(
            fileId=folder_id,
            body=folder_permission,
            sendNotificationEmail=True
        ).execute()
        
        print("✅ Folder access granted!")
        
        print(f"\n🎉 SUCCESS! Access granted to {user_email}")
        print(f"📧 You should receive email notifications")
        print(f"\n🔗 Direct links:")
        print(f"   Notebook: https://colab.research.google.com/drive/{notebook_file_id}")
        print(f"   Folder: https://drive.google.com/drive/folders/{folder_id}")
        
        print(f"\n⏭️  Next steps:")
        print(f"   1. Open the notebook link above")
        print(f"   2. It will auto-start when opened")
        print(f"   3. Come back and run: python3 test_now.py")
        print(f"   4. Experience your 'basically local google colab notebook'!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error granting access: {e}")
        print(f"\n💡 Alternative: Use the copy-paste method")
        print(f"   Copy code from simple_colab_processor.py into new Colab notebook")
        return False

if __name__ == "__main__":
    # Grant access using your email from git config
    success = grant_access("sundeepg8@gmail.com")
    
    if success:
        print("\n🚀 You can now access the hybrid processor!")
    else:
        print("\n🔧 Use copy-paste method as backup")