#!/usr/bin/env python3
"""
Claude Tools - Colab Processor
Runs in Google Colab to process commands from Claude instances
"""

import os
import json
import time
import subprocess
import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

class ColabProcessor:
    """Processes commands from Claude instances in Google Colab"""
    
    def __init__(self):
        self.session_id = f"colab_{int(time.time())}"
        print(f"🚀 Claude Tools Colab Processor: {self.session_id}")
        
    def process_command(self, command):
        """Process a single command"""
        try:
            cmd_type = command.get('type')
            
            if cmd_type == 'execute_code':
                return self._execute_python_code(command['code'])
            elif cmd_type == 'install_package':
                return self._install_packages(command['packages'])
            elif cmd_type == 'shell_command':
                return self._execute_shell(command['command'])
            else:
                return {'error': f'Unknown command type: {cmd_type}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _execute_python_code(self, code):
        """Execute Python code and capture output"""
        stdout_capture = StringIO()
        stderr_capture = StringIO()
        
        try:
            # Capture stdout and stderr
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # Execute the code
                exec(code, globals())
            
            output = stdout_capture.getvalue()
            error = stderr_capture.getvalue()
            
            return {
                'success': True,
                'output': output,
                'error': error if error else None
            }
            
        except Exception as e:
            return {
                'success': False,
                'output': stdout_capture.getvalue(),
                'error': str(e)
            }
    
    def _install_packages(self, packages):
        """Install Python packages"""
        if isinstance(packages, str):
            packages = [packages]
        
        try:
            for package in packages:
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    return {
                        'success': False,
                        'error': f'Failed to install {package}: {result.stderr}'
                    }
            
            return {
                'success': True,
                'output': f'Successfully installed: {", ".join(packages)}'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _execute_shell(self, command):
        """Execute shell command"""
        try:
            result = subprocess.run(
                command, shell=True, 
                capture_output=True, text=True, timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Command timed out'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Google Drive integration for Colab
def setup_drive_integration():
    """Setup Google Drive integration in Colab"""
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        print("✅ Google Drive mounted")
        return True
    except ImportError:
        print("⚠️ Not running in Google Colab")
        return False

def start_processor():
    """Start the command processor loop"""
    processor = ColabProcessor()
    drive_mounted = setup_drive_integration()
    
    if not drive_mounted:
        print("❌ Drive mounting failed - using local mode")
        return
    
    # Set up monitoring folder
    monitor_folder = "/content/drive/MyDrive/claude-tools-commands"
    os.makedirs(monitor_folder, exist_ok=True)
    
    print(f"👁️ Monitoring folder: {monitor_folder}")
    
    processed_files = set()
    
    while True:
        try:
            # Look for command files
            for filename in os.listdir(monitor_folder):
                if filename.startswith('command_') and filename.endswith('.json'):
                    filepath = os.path.join(monitor_folder, filename)
                    
                    if filepath in processed_files:
                        continue
                    
                    # Process command
                    with open(filepath, 'r') as f:
                        command = json.load(f)
                    
                    print(f"📝 Processing: {command.get('type', 'unknown')}")
                    result = processor.process_command(command)
                    
                    # Save result
                    result_filename = filename.replace('command_', 'result_')
                    result_path = os.path.join(monitor_folder, result_filename)
                    
                    with open(result_path, 'w') as f:
                        json.dump(result, f)
                    
                    # Clean up command file
                    os.remove(filepath)
                    processed_files.add(filepath)
                    
                    print(f"✅ Completed: {result.get('success', False)}")
            
            time.sleep(2)  # Check every 2 seconds
            
        except KeyboardInterrupt:
            print("\n🛑 Processor stopped")
            break
        except Exception as e:
            print(f"❌ Processor error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("🧪 Claude Tools Colab Processor")
    print("================================")
    start_processor()