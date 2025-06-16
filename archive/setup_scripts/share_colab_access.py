#!/usr/bin/env python3
"""
Share Colab notebook access with user
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.universal_bridge import UniversalColabBridge

def share_notebook_access(user_email):
    """Share the hybrid processor notebook with user"""
    
    # The notebook file ID from previous uploads
    notebook_file_id = "1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA"
    
    try:
        bridge = UniversalColabBridge("share_access")
        bridge.initialize()
        
        print(f"🔗 Sharing notebook access with: {user_email}")
        
        # Share the file
        permission = {
            'type': 'user',
            'role': 'writer',  # Give edit access
            'emailAddress': user_email
        }
        
        bridge.drive_service.permissions().create(
            fileId=notebook_file_id,
            body=permission,
            sendNotificationEmail=True
        ).execute()
        
        print(f"✅ Access granted!")
        print(f"📧 Notification sent to: {user_email}")
        print(f"🔗 Direct link: https://colab.research.google.com/drive/{notebook_file_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sharing access: {e}")
        return False

def share_folder_access(user_email):
    """Share the entire Google Drive folder"""
    
    # The folder ID 
    folder_id = "1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z"
    
    try:
        bridge = UniversalColabBridge("share_folder")
        bridge.initialize()
        
        print(f"📁 Sharing folder access with: {user_email}")
        
        # Share the folder
        permission = {
            'type': 'user',
            'role': 'writer',  # Give edit access
            'emailAddress': user_email
        }
        
        bridge.drive_service.permissions().create(
            fileId=folder_id,
            body=permission,
            sendNotificationEmail=True
        ).execute()
        
        print(f"✅ Folder access granted!")
        print(f"📧 Notification sent to: {user_email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sharing folder: {e}")
        return False

if __name__ == "__main__":
    # You can provide your email here or we can ask
    user_email = input("Enter your Google email address: ").strip()
    
    if user_email and '@' in user_email:
        print(f"\n🚀 Granting access to: {user_email}")
        
        # Share both notebook and folder
        notebook_shared = share_notebook_access(user_email)
        folder_shared = share_folder_access(user_email)
        
        if notebook_shared and folder_shared:
            print(f"\n🎉 SUCCESS!")
            print(f"✅ You now have access to the hybrid processor")
            print(f"✅ You can access the notebook and test the hybrid experience")
            print(f"\n🔗 Direct access:")
            print(f"   Notebook: https://colab.research.google.com/drive/1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA")
            print(f"\n⏭️  Next steps:")
            print(f"   1. Open the notebook link above")
            print(f"   2. Run all cells (it will auto-start)")
            print(f"   3. Come back and run: python3 test_now.py")
        else:
            print(f"\n⚠️  Some access sharing failed, but you can still use copy-paste method")
    else:
        print("❌ Please provide a valid email address")