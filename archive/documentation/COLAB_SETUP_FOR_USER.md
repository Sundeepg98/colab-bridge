# 🚀 Setup Your Own Colab Processor

Since the notebook is in the service account's Drive, here's how to create your own:

## Method 1: Copy the Notebook Content

1. **Go to Google Colab**: https://colab.research.google.com
2. **Create new notebook**: Click "New notebook"  
3. **Copy the content below** into cells:

### Cell 1 (Code):
```python
# Mount Drive and authenticate
from google.colab import drive, auth
import os, json, time, traceback
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import threading
from IPython.display import display, HTML, clear_output

# Mount drive
drive.mount('/content/drive')
print("✅ Drive mounted")

# Authenticate
auth.authenticate_user()
drive_service = build('drive', 'v3')
print("✅ Authenticated")

# Your Google Drive folder ID for colab-bridge
FOLDER_ID = "1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z"
print(f"📁 Using folder: {FOLDER_ID}")
```

### Cell 2 (Code):
```python
class SimpleProcessor:
    def __init__(self, folder_id, drive_service):
        self.folder_id = folder_id
        self.drive_service = drive_service
        self.processed = set()
        self.running = False
        
    def get_commands(self):
        """Get unprocessed commands"""
        try:
            query = f"'{self.folder_id}' in parents and name contains 'command_' and trashed=false"
            results = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
            return [f for f in results.get('files', []) if f['id'] not in self.processed]
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def process_command(self, cmd_file):
        """Process a command"""
        try:
            # Read command
            content = self.drive_service.files().get_media(fileId=cmd_file['id']).execute()
            request = json.loads(content.decode('utf-8'))
            
            # Execute code
            result = self.execute_code(request.get('code', ''))
            
            # Write response
            cmd_id = cmd_file['name'].replace('command_', '').replace('.json', '')
            self.write_response(cmd_id, result)
            
            self.processed.add(cmd_file['id'])
            print(f"✅ Processed: {cmd_id}")
            
        except Exception as e:
            print(f"❌ Error processing: {e}")
    
    def execute_code(self, code):
        """Execute Python code safely"""
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
    
    def write_response(self, cmd_id, response):
        """Write response to Drive"""
        try:
            file_metadata = {'name': f'result_{cmd_id}.json', 'parents': [self.folder_id]}
            media = MediaIoBaseUpload(
                io.BytesIO(json.dumps(response, indent=2).encode('utf-8')),
                mimetype='application/json'
            )
            self.drive_service.files().create(body=file_metadata, media_body=media).execute()
        except Exception as e:
            print(f"❌ Write error: {e}")
    
    def run(self, duration=3600):
        """Run processor"""
        self.running = True
        start_time = time.time()
        
        print(f"🚀 Processor started for {duration}s")
        
        while self.running and (time.time() - start_time < duration):
            try:
                commands = self.get_commands()
                for cmd in commands:
                    self.process_command(cmd)
                time.sleep(3)  # Check every 3 seconds
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Loop error: {e}")
                time.sleep(5)
        
        print("🛑 Processor stopped")

# Create and start processor
processor = SimpleProcessor(FOLDER_ID, drive_service)
```

### Cell 3 (Code):
```python
# Start processor in background
def run_processor():
    processor.run(duration=1800)  # 30 minutes

processor_thread = threading.Thread(target=run_processor)
processor_thread.daemon = True
processor_thread.start()

print("✅ Hybrid processor running!")
print("💡 Your local notebooks can now execute on this Colab!")
print("⏱️  Will run for 30 minutes")

# Show status updates
for i in range(10):
    time.sleep(5)
    commands = processor.get_commands()
    print(f"📊 Status: {len(processor.processed)} processed, {len(commands)} pending")
```

## Method 2: Upload the File

1. **Download the notebook**: Copy `notebooks/hybrid-processor.ipynb` to your computer
2. **Go to Colab**: https://colab.research.google.com  
3. **Upload**: File → Upload notebook → Select the .ipynb file

## 🎯 After Setup

Once your Colab processor is running, come back and test:

```bash
python3 test_now.py
```

You'll see your "basically local google colab notebook" in action! 🚀