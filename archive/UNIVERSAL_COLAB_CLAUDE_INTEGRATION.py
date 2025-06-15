# 🤖 Universal Claude Coder + Google Colab Integration
# This code can be used across ANY project with Claude Coder
# Works with Google Drive service account for secure communication

from google.colab import drive
import os, json, time, threading, subprocess
from datetime import datetime
from typing import Dict, Any, List
import traceback

# Mount Google Drive
drive.mount('/content/drive')

# ===========================================
# CONFIGURATION - Customize for your project
# ===========================================

# Change this to your ColabAPI folder path
API_FOLDER = "/content/drive/MyDrive/ColabAPI"

# Your service account folder ID (from Claude's folder creation)
SERVICE_ACCOUNT_FOLDER_ID = "YOUR_FOLDER_ID"  # Update this

# Project identifier (helps separate multiple projects)
PROJECT_NAME = "claude_integration"

# Optional: Add any API keys your project needs
API_KEYS = {
    "GEMINI_API_KEY": "YOUR_KEY_HERE",  # For AI features
    "OPENAI_API_KEY": "YOUR_KEY_HERE",  # Alternative AI
    # Add more as needed
}

# ===========================================
# UNIVERSAL COMMAND PROCESSOR
# ===========================================

class UniversalClaudeProcessor:
    """
    Universal processor that handles commands from Claude Coder
    Works with any project - just customize the command handlers
    """
    
    def __init__(self):
        self.api_folder = API_FOLDER
        self.project_name = PROJECT_NAME
        self.running = True
        self.commands_processed = 0
        self.start_time = time.time()
        
        # Create folder structure
        self.setup_folders()
        
        # Initialize any APIs if keys are provided
        self.setup_apis()
        
    def setup_folders(self):
        """Create necessary folder structure"""
        folders = ['commands', 'results', 'data', 'logs', 'state']
        for folder in folders:
            os.makedirs(f'{self.api_folder}/{folder}', exist_ok=True)
        print("✅ Folder structure ready")
    
    def setup_apis(self):
        """Initialize any APIs based on provided keys"""
        if API_KEYS.get("GEMINI_API_KEY") and API_KEYS["GEMINI_API_KEY"] != "YOUR_KEY_HERE":
            try:
                import google.generativeai as genai
                genai.configure(api_key=API_KEYS["GEMINI_API_KEY"])
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                print("✅ Gemini AI initialized")
            except:
                print("⚠️  Gemini API not available")
                self.gemini_model = None
        else:
            self.gemini_model = None
    
    def process_command(self, cmd_file: str):
        """Process a single command from Claude"""
        try:
            # Read command
            with open(cmd_file, 'r') as f:
                command = json.load(f)
            
            print(f"\n📋 Processing: {command['type']} (ID: {command['id']})")
            
            # Prepare result
            result = {
                'command_id': command['id'],
                'type': command['type'],
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'project': self.project_name
            }
            
            # Route to appropriate handler
            if command['type'] == 'execute_code':
                result['data'] = self.execute_code(command.get('code', ''))
                
            elif command['type'] == 'run_notebook':
                result['data'] = self.run_notebook(command.get('notebook_path', ''))
                
            elif command['type'] == 'install_package':
                result['data'] = self.install_package(command.get('package', ''))
                
            elif command['type'] == 'shell_command':
                result['data'] = self.run_shell_command(command.get('command', ''))
                
            elif command['type'] == 'ai_query':
                result['data'] = self.process_ai_query(command.get('prompt', ''))
                
            elif command['type'] == 'data_analysis':
                result['data'] = self.analyze_data(command.get('data', {}))
                
            elif command['type'] == 'save_file':
                result['data'] = self.save_file(
                    command.get('filename', ''),
                    command.get('content', '')
                )
                
            elif command['type'] == 'read_file':
                result['data'] = self.read_file(command.get('filename', ''))
                
            elif command['type'] == 'get_status':
                result['data'] = self.get_system_status()
                
            elif command['type'] == 'custom':
                # For project-specific commands
                result['data'] = self.handle_custom_command(command)
                
            else:
                result['status'] = 'error'
                result['error'] = f"Unknown command type: {command['type']}"
            
            # Save result
            result_file = f'{self.api_folder}/results/result_{command["id"]}.json'
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            # Clean up command
            os.remove(cmd_file)
            
            self.commands_processed += 1
            print(f"✅ Completed: {command['type']}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            error_result = {
                'command_id': command.get('id', 'unknown'),
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            
            # Save error result
            error_file = f'{self.api_folder}/results/error_{command.get("id", "unknown")}.json'
            with open(error_file, 'w') as f:
                json.dump(error_result, f, indent=2)
    
    # ===========================================
    # COMMAND HANDLERS
    # ===========================================
    
    def execute_code(self, code: str) -> Dict:
        """Execute Python code and capture output"""
        try:
            # Capture output
            from io import StringIO
            import sys
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Execute code
            exec_globals = {}
            exec(code, exec_globals)
            
            # Get output
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            return {
                'output': output,
                'variables': list(exec_globals.keys()),
                'success': True
            }
        except Exception as e:
            sys.stdout = old_stdout
            return {
                'error': str(e),
                'traceback': traceback.format_exc(),
                'success': False
            }
    
    def run_notebook(self, notebook_path: str) -> Dict:
        """Run a Jupyter notebook"""
        try:
            # Use nbconvert to run notebook
            result = subprocess.run(
                ['jupyter', 'nbconvert', '--to', 'notebook', '--execute', 
                 '--output', 'executed_notebook', notebook_path],
                capture_output=True,
                text=True
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def install_package(self, package: str) -> Dict:
        """Install a Python package"""
        try:
            result = subprocess.run(
                ['pip', 'install', package],
                capture_output=True,
                text=True
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def run_shell_command(self, command: str) -> Dict:
        """Run a shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def process_ai_query(self, prompt: str) -> Dict:
        """Process an AI query using available models"""
        if self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                return {
                    'response': response.text,
                    'model': 'gemini-pro',
                    'success': True
                }
            except Exception as e:
                return {'error': str(e), 'success': False}
        else:
            return {
                'error': 'No AI model configured',
                'help': 'Set GEMINI_API_KEY in configuration',
                'success': False
            }
    
    def analyze_data(self, data: Dict) -> Dict:
        """Basic data analysis"""
        try:
            import pandas as pd
            import numpy as np
            
            # Convert data to DataFrame if possible
            if isinstance(data, dict) and 'values' in data:
                df = pd.DataFrame(data['values'])
                
                analysis = {
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'dtypes': df.dtypes.to_dict(),
                    'summary': df.describe().to_dict(),
                    'null_counts': df.isnull().sum().to_dict()
                }
                
                return {'analysis': analysis, 'success': True}
            else:
                return {'error': 'Invalid data format', 'success': False}
                
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def save_file(self, filename: str, content: str) -> Dict:
        """Save a file to the data folder"""
        try:
            filepath = f'{self.api_folder}/data/{filename}'
            with open(filepath, 'w') as f:
                f.write(content)
            
            return {
                'filepath': filepath,
                'size': len(content),
                'success': True
            }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def read_file(self, filename: str) -> Dict:
        """Read a file from the data folder"""
        try:
            filepath = f'{self.api_folder}/data/{filename}'
            with open(filepath, 'r') as f:
                content = f.read()
            
            return {
                'content': content,
                'size': len(content),
                'success': True
            }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def get_system_status(self) -> Dict:
        """Get current system status"""
        import psutil
        
        return {
            'uptime_seconds': int(time.time() - self.start_time),
            'commands_processed': self.commands_processed,
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'cpu_percent': psutil.cpu_percent(interval=1),
            'project': self.project_name,
            'api_folder': self.api_folder
        }
    
    def handle_custom_command(self, command: Dict) -> Dict:
        """
        Handle project-specific custom commands
        Override this method for your specific project needs
        """
        # Example custom handler
        custom_type = command.get('custom_type', '')
        
        if custom_type == 'example':
            return {'message': 'Custom command handled', 'data': command.get('data')}
        else:
            return {'error': f'Unknown custom type: {custom_type}'}
    
    # ===========================================
    # MAIN LOOP
    # ===========================================
    
    def update_status(self):
        """Update system status file"""
        status = {
            'running': True,
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': int(time.time() - self.start_time),
            'commands_processed': self.commands_processed,
            'project': self.project_name,
            'capabilities': [
                'execute_code',
                'run_notebook',
                'install_package',
                'shell_command',
                'ai_query',
                'data_analysis',
                'file_operations',
                'custom_commands'
            ]
        }
        
        with open(f'{self.api_folder}/status.json', 'w') as f:
            json.dump(status, f, indent=2)
    
    def run(self):
        """Main processing loop"""
        print("🔄 Starting universal processor...")
        
        while self.running:
            try:
                # Update status
                self.update_status()
                
                # Check for commands
                cmd_folder = f'{self.api_folder}/commands'
                if os.path.exists(cmd_folder):
                    cmd_files = [f for f in os.listdir(cmd_folder) if f.endswith('.json')]
                    
                    if cmd_files:
                        print(f"\n📥 Found {len(cmd_files)} command(s)")
                        for cmd_file in sorted(cmd_files):  # Process in order
                            full_path = os.path.join(cmd_folder, cmd_file)
                            self.process_command(full_path)
                
                # Small delay to prevent CPU spinning
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n⏹️  Stopping processor...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Loop error: {e}")
                time.sleep(5)

# ===========================================
# USAGE INSTRUCTIONS
# ===========================================

print("""
🤖 UNIVERSAL CLAUDE CODER + COLAB INTEGRATION
=============================================

This is a reusable integration that works with ANY project!

📋 How to use:
1. Update PROJECT_NAME to identify your project
2. Add any API keys you need in API_KEYS
3. Customize handle_custom_command() for project-specific needs
4. Run this cell to start the processor

🛠️ Available Commands:
- execute_code: Run Python code
- run_notebook: Execute Jupyter notebooks
- install_package: Install Python packages
- shell_command: Run shell commands
- ai_query: Process AI queries (needs API key)
- data_analysis: Analyze data
- save_file/read_file: File operations
- custom: Your custom commands

📁 Folder Structure:
{API_FOLDER}/
├── commands/     # Claude sends commands here
├── results/      # Processor saves results here
├── data/         # Working data files
├── logs/         # Execution logs
└── state/        # Persistent state

🚀 Starting processor...
""".format(API_FOLDER=API_FOLDER))

# Create and start processor
processor = UniversalClaudeProcessor()

# Start in a thread
processor_thread = threading.Thread(target=processor.run)
processor_thread.daemon = True
processor_thread.start()

# Display status
print(f"\n✅ PROCESSOR ACTIVE!")
print(f"📂 Monitoring: {API_FOLDER}/commands")
print(f"🏷️  Project: {PROJECT_NAME}")
print("⏳ Waiting for commands from Claude...\n")

# Keep alive with status updates
try:
    while True:
        time.sleep(30)  # Update every 30 seconds
        status = processor.get_system_status()
        print(f"\r⏱️ Uptime: {status['uptime_seconds']}s | 📋 Processed: {status['commands_processed']} | 💾 Memory: {status['memory_usage']:.1f}%", end="", flush=True)
except KeyboardInterrupt:
    print("\n\n👋 Shutting down...")
    processor.running = False
    print("✅ Processor stopped")