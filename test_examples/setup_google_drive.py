#!/usr/bin/env python3
"""Helper script to set up Google Drive for Colab Bridge"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Service account path
SERVICE_ACCOUNT_PATH = "/var/projects/automation-engine/credentials/automation-engine-463103-ee5a06e18248.json"

print("🔧 Setting up Google Drive for Colab Bridge")
print("=" * 50)

# Load service account
print("\n1️⃣ Loading service account...")
with open(SERVICE_ACCOUNT_PATH, 'r') as f:
    service_account_info = json.load(f)
    
service_account_email = service_account_info.get('client_email')
print(f"Service Account Email: {service_account_email}")

# Initialize Drive service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_PATH,
    scopes=['https://www.googleapis.com/auth/drive']
)
drive_service = build('drive', 'v3', credentials=credentials)

# Try to create a folder
print("\n2️⃣ Creating Colab Bridge folder...")
folder_metadata = {
    'name': 'colab-bridge-workspace',
    'mimeType': 'application/vnd.google-apps.folder'
}

try:
    folder = drive_service.files().create(
        body=folder_metadata,
        fields='id,name'
    ).execute()
    
    folder_id = folder.get('id')
    print(f"✅ Created folder: {folder.get('name')}")
    print(f"📋 Folder ID: {folder_id}")
    
    print("\n3️⃣ Configuration values for VS Code:")
    print("-" * 50)
    print(f"Service Account Path: {SERVICE_ACCOUNT_PATH}")
    print(f"Google Drive Folder ID: {folder_id}")
    print("-" * 50)
    
    print("\n4️⃣ To use in VS Code:")
    print("1. Press Ctrl+Shift+P")
    print("2. Type: 'Colab Bridge: Configure'")
    print("3. Enter the values above")
    
except Exception as e:
    print(f"❌ Error creating folder: {e}")
    print("\n📝 Manual setup required:")
    print("1. Go to https://drive.google.com")
    print("2. Create a new folder called 'colab-bridge-workspace'")
    print(f"3. Share it with: {service_account_email}")
    print("4. Copy the folder ID from the URL")
    print("   (It's the part after /folders/ in the URL)")
    print("5. Use that folder ID in VS Code configuration")