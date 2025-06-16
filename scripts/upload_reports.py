#!/usr/bin/env python3
"""
Upload the reports to Google Drive
"""

import os
import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_reports_to_drive():
    """Upload both reports to Google Drive"""
    
    print("📤 UPLOADING REPORTS TO GOOGLE DRIVE")
    print("=" * 50)
    
    try:
        # Load service account
        creds_path = '/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
        
        with open(creds_path) as f:
            sa_info = json.load(f)
        
        credentials = service_account.Credentials.from_service_account_info(
            sa_info, scopes=['https://www.googleapis.com/auth/drive']
        )
        
        drive_service = build('drive', 'v3', credentials=credentials)
        folder_id = '1ruRdOXUJi16sHgDtpgxqtR7A7g7J8PpA'
        
        # Reports to upload
        reports = [
            '/home/sundeepg8/projects/colab-bridge/AUTOMATION_REPORT.md',
            '/home/sundeepg8/projects/colab-bridge/SECRETS_ARCHITECTURE.md',
            '/home/sundeepg8/projects/colab-bridge/HONEST_TEST_RESULTS.md'
        ]
        
        uploaded_files = []
        
        for report_path in reports:
            if os.path.exists(report_path):
                filename = os.path.basename(report_path)
                
                print(f"\n📄 Uploading: {filename}")
                
                file_metadata = {
                    'name': filename,
                    'parents': [folder_id],
                    'mimeType': 'text/markdown'
                }
                
                media = MediaFileUpload(
                    report_path,
                    mimetype='text/markdown',
                    resumable=True
                )
                
                result = drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,webViewLink'
                ).execute()
                
                file_id = result['id']
                view_link = result.get('webViewLink', f'https://drive.google.com/file/d/{file_id}/view')
                
                print(f"✅ Uploaded: {filename}")
                print(f"🔗 View: {view_link}")
                
                uploaded_files.append({
                    'name': filename,
                    'id': file_id,
                    'link': view_link
                })
                
        print("\n" + "=" * 50)
        print("✅ ALL REPORTS UPLOADED SUCCESSFULLY!")
        print("=" * 50)
        
        print("\n📋 Quick Links:")
        for file in uploaded_files:
            print(f"\n{file['name']}:")
            print(f"   {file['link']}")
            
        return uploaded_files
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

if __name__ == "__main__":
    upload_reports_to_drive()