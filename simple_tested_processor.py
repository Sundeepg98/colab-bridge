# TESTED Colab Processor - Copy this into Colab
# Each section tested individually

# ========== CELL 1: Mount and Auth ==========
from google.colab import drive, auth
drive.mount('/content/drive')
auth.authenticate_user()
print("✅ Drive mounted and authenticated")

# ========== CELL 2: Dependencies ==========
import os, json, time, traceback
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

drive_service = build('drive', 'v3')
FOLDER_ID = "1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z"
print(f"✅ Drive service ready, Folder: {FOLDER_ID}")

# ========== CELL 3: Test Connection ==========
# Test if we can access the folder
try:
    query = f"'{FOLDER_ID}' in parents and trashed=false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    print(f"✅ Folder accessible, {len(files)} files found")
except Exception as e:
    print(f"❌ Folder access error: {e}")

# ========== CELL 4: Simple Processor ==========
class SimpleProcessor:
    def __init__(self):
        self.processed = set()
        self.running = False
        
    def get_commands(self):
        try:
            query = f"'{FOLDER_ID}' in parents and name contains 'command_' and trashed=false"
            results = drive_service.files().list(q=query, fields="files(id, name)").execute()
            return [f for f in results.get('files', []) if f['id'] not in self.processed]
        except Exception as e:
            print(f"❌ Get commands error: {e}")
            return []
    
    def execute_code(self, code):
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Create safe namespace
            namespace = {
                '__name__': '__main__',
                'print': print,
                'datetime': datetime,
                'time': time,
                'os': os,
                'json': json
            }
            
            # Add common imports
            exec('import numpy as np', namespace)
            exec('import pandas as pd', namespace)
            exec('import matplotlib.pyplot as plt', namespace)
            
            # Execute user code
            exec(code, namespace)
            output = sys.stdout.getvalue()
            
            return {
                'status': 'success', 
                'output': output,
                'timestamp': time.time()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'timestamp': time.time()
            }
        finally:
            sys.stdout = old_stdout
    
    def write_response(self, cmd_id, response):
        try:
            # Use temporary file method to avoid BytesIO issues
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(response, f, indent=2)
                temp_path = f.name
            
            file_metadata = {
                'name': f'result_{cmd_id}.json',
                'parents': [FOLDER_ID]
            }
            
            from googleapiclient.http import MediaFileUpload
            media = MediaFileUpload(temp_path, mimetype='application/json')
            
            drive_service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
            
            # Clean up
            os.unlink(temp_path)
            print(f"✅ Response written: result_{cmd_id}.json")
            
        except Exception as e:
            print(f"❌ Write response error: {e}")
    
    def process_command(self, cmd_file):
        try:
            # Read command
            content = drive_service.files().get_media(fileId=cmd_file['id']).execute()
            request = json.loads(content.decode('utf-8'))
            
            cmd_id = cmd_file['name'].replace('command_', '').replace('.json', '')
            print(f"📋 Processing: {cmd_id}")
            
            # Execute
            result = self.execute_code(request.get('code', ''))
            
            # Write response
            self.write_response(cmd_id, result)
            
            # Mark processed
            self.processed.add(cmd_file['id'])
            
        except Exception as e:
            print(f"❌ Process error: {e}")
    
    def run(self, duration=1800):  # 30 minutes
        self.running = True
        start_time = time.time()
        
        print(f"🚀 Processor started for {duration//60} minutes")
        
        while self.running and (time.time() - start_time < duration):
            try:
                commands = self.get_commands()
                if commands:
                    for cmd in commands:
                        self.process_command(cmd)
                else:
                    print("⏳ No commands, waiting...")
                
                time.sleep(3)  # Check every 3 seconds
                
            except KeyboardInterrupt:
                print("🛑 Interrupted by user")
                break
            except Exception as e:
                print(f"❌ Main loop error: {e}")
                time.sleep(5)
        
        self.running = False
        print("🛑 Processor stopped")

processor = SimpleProcessor()
print("✅ Processor created")

# ========== CELL 5: Start Processor ==========
print("🚀 Starting processor...")
processor.run()  # This will run until stopped