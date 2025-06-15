# 🤖 Claude-Colab Bridge Processor
# Universal processor that runs in Google Colab
# Works with ANY Claude Coder project seamlessly

from google.colab import drive
import os, json, time, threading, subprocess, sys
from datetime import datetime
from typing import Dict, Any, List, Optional
import traceback
import importlib
import tempfile

# Mount Google Drive
drive.mount('/content/drive')

# ==========================================
# CONFIGURATION
# ==========================================

# Core settings - Update these for your setup
PROJECT_NAME = "your_project_name"  # Change this for each project
API_FOLDER = "/content/drive/MyDrive/ColabAPI"
SERVICE_ACCOUNT_FOLDER_ID = "1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z"  # Update with your folder ID

# Optional API keys
API_KEYS = {
    "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
}

# ==========================================
# BRIDGE PROCESSOR
# ==========================================

class ClaudeColabBridge:
    """Universal bridge between Claude Coder and Google Colab"""
    
    def __init__(self):
        self.api_folder = API_FOLDER
        self.project_name = PROJECT_NAME
        self.running = True
        self.commands_processed = 0
        self.start_time = time.time()
        self.execution_context = {}  # Persistent context between commands
        
        # Setup
        self.setup_folders()
        self.setup_apis()
        self.load_helpers()
        
        print(f"🌉 Claude-Colab Bridge initialized for project: {PROJECT_NAME}")
    
    def setup_folders(self):
        """Create necessary folder structure"""
        folders = ['commands', 'results', 'data', 'logs', 'state', 'outputs']
        for folder in folders:
            os.makedirs(f'{self.api_folder}/{folder}', exist_ok=True)
    
    def setup_apis(self):
        """Initialize AI APIs if available"""
        self.ai_models = {}
        
        # Gemini
        if API_KEYS.get("GEMINI_API_KEY"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=API_KEYS["GEMINI_API_KEY"])
                self.ai_models['gemini'] = genai.GenerativeModel('gemini-pro')
                print("✅ Gemini AI available")
            except Exception as e:
                print(f"⚠️  Gemini not available: {e}")
        
        # Add other AI models as needed
    
    def load_helpers(self):
        """Load helper functions for enhanced capabilities"""
        self.helpers = {
            'visualize': self.create_visualization,
            'analyze_data': self.analyze_dataframe,
            'benchmark': self.run_benchmark,
            'profile': self.profile_code
        }
    
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
            handlers = {
                'execute_code': self.execute_code,
                'execute_notebook': self.execute_notebook,
                'install_package': self.install_package,
                'shell_command': self.run_shell_command,
                'ai_query': self.process_ai_query,
                'data_analysis': self.analyze_data,
                'visualization': self.create_visualization,
                'file_operation': self.handle_file_operation,
                'gpu_check': self.check_gpu_status,
                'benchmark': self.run_benchmark,
                'custom': self.handle_custom_command
            }
            
            handler = handlers.get(command['type'], self.handle_unknown_command)
            result['data'] = handler(command)
            
            # Save result
            self.save_result(result)
            
            # Clean up
            os.remove(cmd_file)
            self.commands_processed += 1
            
            print(f"✅ Completed: {command['type']}")
            
        except Exception as e:
            self.handle_error(command, e)
    
    # ==========================================
    # COMMAND HANDLERS
    # ==========================================
    
    def execute_code(self, command: Dict) -> Dict:
        """Execute Python code with persistent context"""
        code = command.get('code', '')
        use_context = command.get('use_context', True)
        
        try:
            # Capture output
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Execute code
            exec_globals = self.execution_context if use_context else {}
            exec(code, exec_globals)
            
            # Update context
            if use_context:
                self.execution_context.update(exec_globals)
            
            # Get output
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Check for generated files
            output_files = self.check_output_files()
            
            return {
                'output': output,
                'variables': list(exec_globals.keys()),
                'output_files': output_files,
                'success': True
            }
            
        except Exception as e:
            sys.stdout = old_stdout
            return {
                'error': str(e),
                'traceback': traceback.format_exc(),
                'success': False
            }
    
    def execute_notebook(self, command: Dict) -> Dict:
        """Execute a Jupyter notebook"""
        notebook_path = command.get('notebook_path', '')
        
        try:
            result = subprocess.run(
                ['jupyter', 'nbconvert', '--to', 'notebook', '--execute',
                 '--output', f'executed_{os.path.basename(notebook_path)}',
                 notebook_path],
                capture_output=True,
                text=True
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'output_path': f'executed_{os.path.basename(notebook_path)}'
            }
            
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def install_package(self, command: Dict) -> Dict:
        """Install Python packages"""
        packages = command.get('packages', command.get('package', ''))
        
        if isinstance(packages, list):
            packages = ' '.join(packages)
        
        try:
            result = subprocess.run(
                f'pip install {packages}',
                shell=True,
                capture_output=True,
                text=True
            )
            
            # Import newly installed packages
            for pkg in packages.split():
                try:
                    pkg_name = pkg.split('==')[0].split('>=')[0].split('<=')[0]
                    importlib.import_module(pkg_name.replace('-', '_'))
                except:
                    pass
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'packages_installed': packages.split()
            }
            
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def run_shell_command(self, command: Dict) -> Dict:
        """Run shell commands"""
        cmd = command.get('command', '')
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=command.get('cwd', None)
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
            
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def process_ai_query(self, command: Dict) -> Dict:
        """Process AI queries using available models"""
        prompt = command.get('prompt', '')
        model = command.get('model', 'gemini')
        
        if model in self.ai_models:
            try:
                if model == 'gemini':
                    response = self.ai_models['gemini'].generate_content(prompt)
                    return {
                        'response': response.text,
                        'model': 'gemini-pro',
                        'success': True
                    }
                # Add other models here
                
            except Exception as e:
                return {'error': str(e), 'success': False}
        else:
            return {
                'error': f'Model {model} not available',
                'available_models': list(self.ai_models.keys()),
                'success': False
            }
    
    def analyze_data(self, command: Dict) -> Dict:
        """Perform data analysis"""
        try:
            import pandas as pd
            import numpy as np
            
            data = command.get('data', {})
            analysis_type = command.get('analysis_type', 'basic')
            
            # Create DataFrame
            if 'dataframe' in data:
                df = pd.DataFrame(data['dataframe'])
            elif 'csv_path' in data:
                df = pd.read_csv(data['csv_path'])
            elif 'values' in data:
                df = pd.DataFrame(data['values'])
            else:
                return {'error': 'No data provided', 'success': False}
            
            results = {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'summary': df.describe().to_dict(),
                'null_counts': df.isnull().sum().to_dict()
            }
            
            # Additional analysis based on type
            if analysis_type == 'correlation':
                numeric_df = df.select_dtypes(include=[np.number])
                results['correlation'] = numeric_df.corr().to_dict()
            
            elif analysis_type == 'distribution':
                results['distribution'] = {}
                for col in df.select_dtypes(include=[np.number]).columns:
                    results['distribution'][col] = {
                        'mean': df[col].mean(),
                        'std': df[col].std(),
                        'min': df[col].min(),
                        'max': df[col].max(),
                        'quartiles': df[col].quantile([0.25, 0.5, 0.75]).to_dict()
                    }
            
            return {'analysis': results, 'success': True}
            
        except Exception as e:
            return {'error': str(e), 'traceback': traceback.format_exc(), 'success': False}
    
    def create_visualization(self, command: Dict) -> Dict:
        """Create data visualizations"""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            import pandas as pd
            
            viz_type = command.get('type', 'plot')
            data = command.get('data', {})
            options = command.get('options', {})
            
            # Create figure
            plt.figure(figsize=options.get('figsize', (10, 6)))
            
            if viz_type == 'plot':
                plt.plot(data.get('x', []), data.get('y', []))
            elif viz_type == 'scatter':
                plt.scatter(data.get('x', []), data.get('y', []))
            elif viz_type == 'bar':
                plt.bar(data.get('x', []), data.get('y', []))
            elif viz_type == 'histogram':
                plt.hist(data.get('values', []), bins=options.get('bins', 20))
            elif viz_type == 'heatmap' and 'dataframe' in data:
                df = pd.DataFrame(data['dataframe'])
                sns.heatmap(df.corr(), annot=True)
            
            # Customize
            plt.title(options.get('title', 'Visualization'))
            plt.xlabel(options.get('xlabel', ''))
            plt.ylabel(options.get('ylabel', ''))
            
            # Save
            output_path = f"{self.api_folder}/outputs/viz_{command['id']}.png"
            plt.savefig(output_path)
            plt.close()
            
            return {
                'output_path': output_path,
                'success': True
            }
            
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def handle_file_operation(self, command: Dict) -> Dict:
        """Handle file operations"""
        operation = command.get('operation', 'read')
        
        try:
            if operation == 'read':
                filepath = command.get('filepath', '')
                with open(filepath, 'r') as f:
                    content = f.read()
                return {'content': content, 'size': len(content), 'success': True}
                
            elif operation == 'write':
                filepath = command.get('filepath', '')
                content = command.get('content', '')
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'w') as f:
                    f.write(content)
                return {'filepath': filepath, 'size': len(content), 'success': True}
                
            elif operation == 'list':
                directory = command.get('directory', '.')
                files = os.listdir(directory)
                return {'files': files, 'count': len(files), 'success': True}
                
            else:
                return {'error': f'Unknown operation: {operation}', 'success': False}
                
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def check_gpu_status(self, command: Dict) -> Dict:
        """Check GPU availability and status"""
        try:
            gpu_info = !nvidia-smi
            gpu_available = 'NVIDIA' in ''.join(gpu_info)
            
            if gpu_available:
                import torch
                cuda_available = torch.cuda.is_available()
                device_count = torch.cuda.device_count() if cuda_available else 0
                
                return {
                    'gpu_available': True,
                    'cuda_available': cuda_available,
                    'device_count': device_count,
                    'gpu_info': gpu_info,
                    'success': True
                }
            else:
                return {
                    'gpu_available': False,
                    'message': 'No GPU detected. Using CPU.',
                    'success': True
                }
                
        except Exception as e:
            return {'error': str(e), 'gpu_available': False, 'success': False}
    
    def run_benchmark(self, command: Dict) -> Dict:
        """Run performance benchmarks"""
        benchmark_type = command.get('benchmark_type', 'basic')
        
        try:
            import time
            import numpy as np
            
            results = {}
            
            if benchmark_type in ['basic', 'all']:
                # CPU benchmark
                start = time.time()
                _ = np.random.rand(1000, 1000) @ np.random.rand(1000, 1000)
                results['matrix_multiply_time'] = time.time() - start
                
                # Memory benchmark
                import psutil
                results['memory_usage'] = psutil.virtual_memory().percent
                results['cpu_count'] = psutil.cpu_count()
            
            if benchmark_type in ['gpu', 'all']:
                try:
                    import torch
                    if torch.cuda.is_available():
                        # GPU benchmark
                        device = torch.device('cuda')
                        a = torch.randn(1000, 1000).to(device)
                        b = torch.randn(1000, 1000).to(device)
                        
                        start = time.time()
                        c = torch.matmul(a, b)
                        torch.cuda.synchronize()
                        results['gpu_matrix_multiply_time'] = time.time() - start
                except:
                    results['gpu_benchmark'] = 'GPU not available'
            
            return {'benchmarks': results, 'success': True}
            
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def profile_code(self, code: str) -> Dict:
        """Profile code execution"""
        try:
            import cProfile
            import pstats
            from io import StringIO
            
            pr = cProfile.Profile()
            pr.enable()
            
            # Execute code
            exec(code, self.execution_context)
            
            pr.disable()
            
            # Get stats
            s = StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats(20)  # Top 20 functions
            
            return {
                'profile_stats': s.getvalue(),
                'success': True
            }
            
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def handle_custom_command(self, command: Dict) -> Dict:
        """Handle project-specific custom commands"""
        custom_type = command.get('custom_type', '')
        
        # Add your custom handlers here
        custom_handlers = {
            'example': lambda cmd: {'message': 'Custom command executed', 'data': cmd.get('data')}
        }
        
        handler = custom_handlers.get(custom_type)
        if handler:
            return handler(command)
        else:
            return {'error': f'Unknown custom type: {custom_type}', 'success': False}
    
    def handle_unknown_command(self, command: Dict) -> Dict:
        """Handle unknown command types"""
        return {
            'error': f"Unknown command type: {command['type']}",
            'available_commands': [
                'execute_code', 'execute_notebook', 'install_package',
                'shell_command', 'ai_query', 'data_analysis',
                'visualization', 'file_operation', 'gpu_check',
                'benchmark', 'custom'
            ],
            'success': False
        }
    
    # ==========================================
    # HELPER METHODS
    # ==========================================
    
    def check_output_files(self) -> List[str]:
        """Check for any files generated during execution"""
        output_dir = f'{self.api_folder}/outputs'
        before = set(os.listdir(output_dir))
        time.sleep(0.1)  # Brief pause
        after = set(os.listdir(output_dir))
        return list(after - before)
    
    def save_result(self, result: Dict):
        """Save command result"""
        result_file = f'{self.api_folder}/results/result_{result["command_id"]}.json'
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
    
    def handle_error(self, command: Dict, error: Exception):
        """Handle command execution errors"""
        error_result = {
            'command_id': command.get('id', 'unknown'),
            'type': command.get('type', 'unknown'),
            'status': 'error',
            'error': str(error),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().isoformat()
        }
        
        error_file = f'{self.api_folder}/results/error_{command.get("id", "unknown")}.json'
        with open(error_file, 'w') as f:
            json.dump(error_result, f, indent=2)
        
        print(f"❌ Error: {error}")
    
    def update_status(self):
        """Update bridge status"""
        status = {
            'running': True,
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': int(time.time() - self.start_time),
            'commands_processed': self.commands_processed,
            'project': self.project_name,
            'capabilities': list(self.get_capabilities()),
            'ai_models': list(self.ai_models.keys()),
            'context_variables': list(self.execution_context.keys())[:20]  # First 20
        }
        
        with open(f'{self.api_folder}/status.json', 'w') as f:
            json.dump(status, f, indent=2)
    
    def get_capabilities(self) -> List[str]:
        """Get list of bridge capabilities"""
        return [
            'execute_code', 'execute_notebook', 'install_package',
            'shell_command', 'ai_query', 'data_analysis',
            'visualization', 'file_operation', 'gpu_check',
            'benchmark', 'profile', 'custom_commands'
        ]
    
    def run(self):
        """Main processing loop"""
        print("🔄 Starting Claude-Colab Bridge processor...")
        print(f"📂 Monitoring: {self.api_folder}/commands")
        print("⏳ Waiting for commands from Claude...\n")
        
        while self.running:
            try:
                # Update status
                self.update_status()
                
                # Check for commands
                cmd_folder = f'{self.api_folder}/commands'
                if os.path.exists(cmd_folder):
                    cmd_files = sorted([
                        f for f in os.listdir(cmd_folder)
                        if f.endswith('.json')
                    ])
                    
                    if cmd_files:
                        print(f"\n📥 Found {len(cmd_files)} command(s)")
                        for cmd_file in cmd_files:
                            full_path = os.path.join(cmd_folder, cmd_file)
                            self.process_command(full_path)
                
                time.sleep(1)  # Check interval
                
            except KeyboardInterrupt:
                print("\n⏹️  Stopping bridge...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Loop error: {e}")
                time.sleep(5)

# ==========================================
# STARTUP
# ==========================================

print("""
🌉 Claude-Colab Bridge v2.0
===========================

A seamless integration between Claude Coder and Google Colab.
This bridge enables Claude to execute code, analyze data, and more!

📋 Configuration:
""")

print(f"Project: {PROJECT_NAME}")
print(f"API Folder: {API_FOLDER}")
print(f"Folder ID: {SERVICE_ACCOUNT_FOLDER_ID}")

# Check for AI models
ai_status = []
if API_KEYS.get("GEMINI_API_KEY"):
    ai_status.append("Gemini")
if API_KEYS.get("OPENAI_API_KEY"):
    ai_status.append("OpenAI")

print(f"AI Models: {', '.join(ai_status) if ai_status else 'None configured'}")

print("\n🚀 Starting bridge processor...\n")

# Create and start bridge
bridge = ClaudeColabBridge()

# Start in thread
bridge_thread = threading.Thread(target=bridge.run)
bridge_thread.daemon = True
bridge_thread.start()

# Display status loop
print("✅ Bridge is active and processing commands!")
print("Press Ctrl+C to stop\n")

try:
    while True:
        time.sleep(30)
        status = f"⏱️ Uptime: {int(time.time() - bridge.start_time)}s | "
        status += f"📋 Processed: {bridge.commands_processed} | "
        status += f"🧠 Context vars: {len(bridge.execution_context)}"
        print(f"\r{status}", end="", flush=True)
except KeyboardInterrupt:
    print("\n\n👋 Shutting down bridge...")
    bridge.running = False
    print("✅ Bridge stopped")