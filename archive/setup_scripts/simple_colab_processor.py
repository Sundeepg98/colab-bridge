# Simple Colab Processor for Hybrid Experience
# Copy this entire code into a single Colab cell and run it

from google.colab import drive, auth
import os, json, time, traceback
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import threading

# Setup
drive.mount('/content/drive')
auth.authenticate_user()
drive_service = build('drive', 'v3')
FOLDER_ID = "1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z"

print("✅ Setup complete")

class SimpleProcessor:
    def __init__(self, folder_id, drive_service):
        self.folder_id = folder_id
        self.drive_service = drive_service
        self.processed = set()
        
    def get_commands(self):
        try:
            query = f"'{self.folder_id}' in parents and name contains 'command_' and trashed=false"
            results = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
            return [f for f in results.get('files', []) if f['id'] not in self.processed]
        except: return []
    
    def execute_code(self, code):
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        try:
            exec(code, {'__name__': '__main__'})
            output = sys.stdout.getvalue()
            return {'status': 'success', 'output': output, 'timestamp': time.time()}
        except Exception as e:
            return {'status': 'error', 'error': str(e), 'timestamp': time.time()}
        finally:
            sys.stdout = old_stdout
    
    def process_command(self, cmd_file):
        try:
            content = self.drive_service.files().get_media(fileId=cmd_file['id']).execute()
            request = json.loads(content.decode('utf-8'))
            result = self.execute_code(request.get('code', ''))
            
            cmd_id = cmd_file['name'].replace('command_', '').replace('.json', '')
            file_metadata = {'name': f'result_{cmd_id}.json', 'parents': [self.folder_id]}
            media = MediaIoBaseUpload(
                io.BytesIO(json.dumps(result, indent=2).encode('utf-8')),
                mimetype='application/json'
            )
            self.drive_service.files().create(body=file_metadata, media_body=media).execute()
            
            self.processed.add(cmd_file['id'])
            print(f"✅ Processed: {cmd_id}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run(self):
        print("🚀 Hybrid processor started!")
        while True:
            try:
                commands = self.get_commands()
                for cmd in commands:
                    self.process_command(cmd)
                time.sleep(3)
            except KeyboardInterrupt:
                break

# Start processor
processor = SimpleProcessor(FOLDER_ID, drive_service)
processor.run()  # This will run until you stop it