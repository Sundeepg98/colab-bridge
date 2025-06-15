# 🚀 COMPLETE COLAB INTEGRATION WITH SECRETS
# Uses your sun_colab secret for enhanced features

from google.colab import userdata, drive
import os
import json
import time
import requests
from datetime import datetime
from IPython.display import clear_output, display
import threading

# Mount Drive
print("🔄 Mounting Google Drive...")
drive.mount('/content/drive')

# Get API key from your secret
print("\n🔐 Retrieving credentials...")
try:
    API_KEY = userdata.get('sun_colab')
    print(f"✅ Retrieved API key from 'sun_colab' secret")
    print(f"🔑 Key format: {API_KEY[:8]}...{API_KEY[-4:]}")
    HAS_API_KEY = True
except Exception as e:
    print(f"⚠️ No API key found in secrets: {e}")
    print("📝 Add 'sun_colab' to your Colab secrets for enhanced features")
    API_KEY = None
    HAS_API_KEY = False

# Set up folder structure
BASE_PATH = '/content/drive/MyDrive/ColabAPI'
FOLDERS = {
    'commands': f'{BASE_PATH}/commands',
    'results': f'{BASE_PATH}/results', 
    'status': f'{BASE_PATH}/status',
    'logs': f'{BASE_PATH}/logs',
    'checkpoints': f'{BASE_PATH}/checkpoints'
}

print("\n📁 Setting up folder structure...")
for name, path in FOLDERS.items():
    os.makedirs(path, exist_ok=True)
    print(f"✅ {name}/")

# Status tracking
class ColabStatus:
    def __init__(self):
        self.start_time = datetime.now()
        self.commands_processed = 0
        self.last_command = None
        self.api_key_status = "Available" if HAS_API_KEY else "Not configured"
        
    def update(self):
        """Update status file"""
        status = {
            'status': 'RUNNING',
            'start_time': self.start_time.isoformat(),
            'uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
            'commands_processed': self.commands_processed,
            'last_command': self.last_command,
            'last_update': datetime.now().isoformat(),
            'api_key_status': self.api_key_status,
            'capabilities': {
                'drive_access': True,
                'api_key': HAS_API_KEY,
                'gpu': torch.cuda.is_available() if 'torch' in globals() else False
            }
        }
        
        with open(f"{FOLDERS['status']}/current.json", 'w') as f:
            json.dump(status, f, indent=2)

# Initialize status
status = ColabStatus()
status.update()

# Command processor
def process_commands():
    """Main command processing loop"""
    print("\n🚀 Command processor started!")
    print("📥 Waiting for commands in:", FOLDERS['commands'])
    
    while True:
        try:
            # Check for command files
            cmd_files = [f for f in os.listdir(FOLDERS['commands']) if f.endswith('.json')]
            
            for cmd_file in cmd_files:
                cmd_path = f"{FOLDERS['commands']}/{cmd_file}"
                
                try:
                    # Read command
                    with open(cmd_path, 'r') as f:
                        command = json.load(f)
                    
                    print(f"\n📥 Processing: {command.get('action', 'unknown')}")
                    status.last_command = command.get('action')
                    
                    # Execute based on action
                    result = execute_command(command)
                    
                    # Save result
                    result_data = {
                        'command': command,
                        'result': result,
                        'success': True,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    result_path = f"{FOLDERS['results']}/{cmd_file}"
                    with open(result_path, 'w') as f:
                        json.dump(result_data, f, indent=2)
                    
                    # Clean up
                    os.remove(cmd_path)
                    status.commands_processed += 1
                    status.update()
                    
                    print(f"✅ Completed: {cmd_file}")
                    
                except Exception as e:
                    print(f"❌ Error processing {cmd_file}: {e}")
                    # Save error
                    error_path = f"{FOLDERS['results']}/error_{cmd_file}"
                    with open(error_path, 'w') as f:
                        json.dump({
                            'error': str(e),
                            'command_file': cmd_file,
                            'timestamp': datetime.now().isoformat()
                        }, f)
                    
                    # Remove problematic command
                    if os.path.exists(cmd_path):
                        os.remove(cmd_path)
            
            # Update display
            if cmd_files:
                clear_output(wait=True)
                display_status()
            
        except Exception as e:
            print(f"❌ Loop error: {e}")
        
        time.sleep(2)  # Check every 2 seconds

def execute_command(command):
    """Execute different command types"""
    action = command.get('action', 'unknown')
    
    if action == 'execute_code':
        code = command.get('code', '')
        exec_globals = {'API_KEY': API_KEY} if API_KEY else {}
        exec_locals = {}
        exec(code, exec_globals, exec_locals)
        return exec_locals.get('result', 'Code executed successfully')
    
    elif action == 'install_package':
        package = command.get('package', '')
        import subprocess
        result = subprocess.run(['pip', 'install', package], capture_output=True, text=True)
        return f"Installed {package}: {result.stdout}"
    
    elif action == 'test_gpu':
        try:
            import torch
            if torch.cuda.is_available():
                return f"GPU Available: {torch.cuda.get_device_name(0)}"
            else:
                return "No GPU available"
        except:
            return "PyTorch not installed"
    
    elif action == 'api_test' and API_KEY:
        # Test API key capabilities
        tests = []
        
        # Drive API
        r = requests.get(f"https://www.googleapis.com/drive/v3/files?key={API_KEY}")
        tests.append(f"Drive API: {r.status_code}")
        
        # Maps API
        r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address=test&key={API_KEY}")
        tests.append(f"Maps API: {r.status_code}")
        
        return " | ".join(tests)
    
    else:
        return f"Unknown action: {action}"

def display_status():
    """Display current status"""
    print("="*60)
    print("🚀 COLAB AUTOMATION ACTIVE")
    print("="*60)
    print(f"⏱️ Uptime: {datetime.now() - status.start_time}")
    print(f"📊 Commands processed: {status.commands_processed}")
    print(f"🔑 API Key: {status.api_key_status}")
    print(f"📁 Base path: {BASE_PATH}")
    print(f"💾 Last command: {status.last_command or 'None'}")
    print("="*60)

# Background status updater
def status_updater():
    """Update status file periodically"""
    while True:
        status.update()
        time.sleep(30)  # Update every 30 seconds

# Start background thread
threading.Thread(target=status_updater, daemon=True).start()

# Display initial status
display_status()
print("\n✅ Integration ready!")
print("📥 Send commands to:", FOLDERS['commands'])
print("📤 Results will appear in:", FOLDERS['results'])

# Start processing
process_commands()