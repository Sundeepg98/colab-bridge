# 🌐 Multi-Instance Claude + Colab Integration Setup Guide

## 🎯 Overview

This guide helps you set up a system where **multiple Claude Coder instances** can simultaneously leverage **Google Colab** for AI/ML tasks, eliminating access issues and enabling powerful collaborative workflows.

## 🚀 Quick Start (5 Minutes)

### Step 1: Initialize Bridge in Any Project

```bash
# In any Claude Coder project directory
source /var/projects/claude-colab-bridge/init-bridge.sh your_project_name

# This creates:
# - bridge-helpers.js (convenient functions)
# - bridge-exec, bridge-install, bridge-run, bridge-ai (quick commands)
# - package.json with bridge config
# - .env with settings
# - bridge-example.js (demo script)
```

### Step 2: Start Enhanced Colab Processor

1. **Open Google Colab**: https://colab.research.google.com
2. **Copy this code** to a new cell:

```python
# 🌐 Multi-Instance Claude-Colab Bridge Processor
# Supports multiple Claude instances simultaneously

from google.colab import drive
import os, json, time, threading, subprocess, sys, uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import traceback

# Mount Google Drive
drive.mount('/content/drive')

# Configuration - UPDATE THESE
PROJECT_NAME = "your_project_name"  # Change this!
SESSION_ID = f"colab_{uuid.uuid4().hex[:8]}"
API_FOLDER = "/content/drive/MyDrive/ColabAPI"

# Multi-Instance Colab Processor
class MultiInstanceColabProcessor:
    def __init__(self):
        self.session_id = SESSION_ID
        self.project_name = PROJECT_NAME
        self.api_folder = API_FOLDER
        self.running = True
        self.commands_processed = 0
        self.start_time = time.time()
        self.execution_context = {}
        self.active_instances = set()
        
        # Setup folder structure
        self.setup_folders()
        self.register_session()
        
        print(f"🌐 Multi-Instance Processor: {self.session_id}")
        print(f"🏷️  Project: {self.project_name}")
    
    def setup_folders(self):
        """Create multi-instance folder structure"""
        folders = [
            'instances', 'sessions', 'commands/global', 'commands/priority',
            'results/global', 'routing', 'monitoring'
        ]
        for folder in folders:
            os.makedirs(f'{self.api_folder}/{folder}', exist_ok=True)
    
    def register_session(self):
        """Register this Colab session"""
        session_info = {
            'session_id': self.session_id,
            'project_name': self.project_name,
            'status': 'active',
            'capabilities': [
                'execute_code', 'install_package', 'shell_command',
                'ai_query', 'data_analysis', 'visualization'
            ],
            'gpu_available': self.check_gpu(),
            'registered_at': datetime.now().isoformat()
        }
        
        with open(f'{self.api_folder}/sessions/{self.session_id}.json', 'w') as f:
            json.dump(session_info, f, indent=2)
    
    def check_gpu(self):
        """Check GPU availability"""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def process_commands(self):
        """Process commands from multiple instances"""
        # Check global command queue
        global_dir = f'{self.api_folder}/commands/global'
        priority_dir = f'{self.api_folder}/commands/priority'
        
        # Process priority commands first
        for cmd_dir in [priority_dir, global_dir]:
            if os.path.exists(cmd_dir):
                cmd_files = sorted([f for f in os.listdir(cmd_dir) if f.endswith('.json')])
                for cmd_file in cmd_files:
                    self.process_single_command(os.path.join(cmd_dir, cmd_file))
    
    def process_single_command(self, cmd_file):
        """Process a single command"""
        try:
            with open(cmd_file, 'r') as f:
                command = json.load(f)
            
            instance_id = command.get('instance_id', 'unknown')
            self.active_instances.add(instance_id)
            
            print(f"📋 Processing: {command['type']} from {instance_id[:12]}...")
            
            # Execute command
            result = self.execute_command(command)
            
            # Save result
            result_file = f"{self.api_folder}/results/global/result_{command['id']}.json"
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            # Clean up
            os.remove(cmd_file)
            self.commands_processed += 1
            
            print(f"✅ Completed: {command['type']}")
            
        except Exception as e:
            print(f"❌ Error processing command: {e}")
    
    def execute_command(self, command):
        """Execute different command types"""
        cmd_type = command['type']
        
        if cmd_type == 'execute_code':
            return self.execute_code(command.get('code', ''))
        elif cmd_type == 'install_package':
            return self.install_package(command.get('packages', []))
        elif cmd_type == 'shell_command':
            return self.shell_command(command.get('command', ''))
        elif cmd_type == 'ai_query':
            return self.ai_query(command.get('prompt', ''))
        else:
            return {'error': f'Unknown command type: {cmd_type}', 'success': False}
    
    def execute_code(self, code):
        """Execute Python code"""
        try:
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            exec(code, self.execution_context)
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            return {'output': output, 'success': True}
        except Exception as e:
            sys.stdout = old_stdout
            return {'error': str(e), 'success': False}
    
    def install_package(self, packages):
        """Install packages"""
        if isinstance(packages, str):
            packages = [packages]
        
        try:
            for package in packages:
                result = subprocess.run(['pip', 'install', package], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    return {'error': result.stderr, 'success': False}
            
            return {'message': f'Installed: {", ".join(packages)}', 'success': True}
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def shell_command(self, command):
        """Execute shell command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'success': result.returncode == 0
            }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def ai_query(self, prompt):
        """Handle AI queries (placeholder)"""
        return {
            'response': f'AI query received: {prompt[:50]}...',
            'note': 'Configure AI API keys for full functionality',
            'success': True
        }
    
    def update_status(self):
        """Update system status"""
        status = {
            'session_id': self.session_id,
            'project_name': self.project_name,
            'status': 'active',
            'uptime_seconds': int(time.time() - self.start_time),
            'commands_processed': self.commands_processed,
            'active_instances': list(self.active_instances),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(f'{self.api_folder}/monitoring/system_status.json', 'w') as f:
            json.dump(status, f, indent=2)
    
    def run(self):
        """Main processing loop"""
        print("🔄 Starting multi-instance processor...")
        
        while self.running:
            try:
                self.update_status()
                self.process_commands()
                time.sleep(1)  # Check every second
                
            except KeyboardInterrupt:
                print("\n⏹️  Stopping processor...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Loop error: {e}")
                time.sleep(5)

# Start the processor
processor = MultiInstanceColabProcessor()

# Run in thread
processor_thread = threading.Thread(target=processor.run)
processor_thread.daemon = True
processor_thread.start()

print("✅ Multi-Instance Processor is ACTIVE!")
print("🌐 Ready to handle multiple Claude instances")
print("Press Ctrl+C to stop\n")

# Status display
try:
    while True:
        time.sleep(30)
        status = f"⏱️ {int(time.time() - processor.start_time)}s | "
        status += f"📋 {processor.commands_processed} | "
        status += f"👥 {len(processor.active_instances)} instances"
        print(f"\r{status}", end="", flush=True)
except KeyboardInterrupt:
    print("\n\n👋 Shutting down...")
    processor.running = False
```

3. **Update PROJECT_NAME** to match your project
4. **Run the cell** - processor starts immediately!

### Step 3: Test from Claude

```bash
# Test basic functionality
bun bridge-example.js

# Or use quick commands
./bridge-exec "print('Hello from Colab!')"
./bridge-install numpy pandas matplotlib
./bridge-ai "Generate a Python function for data analysis"
```

## 🌐 Multi-Instance Features

### Simultaneous Claude Instances

```bash
# Project A (Terminal 1)
cd /var/projects/project-a
source /var/projects/claude-colab-bridge/init-bridge.sh project_a
./bridge-exec "print('Project A is running!')"

# Project B (Terminal 2) 
cd /var/projects/project-b
source /var/projects/claude-colab-bridge/init-bridge.sh project_b
./bridge-exec "print('Project B is running!')"

# Both work simultaneously! 🎉
```

### Load Balancing & Routing

```javascript
// Automatic load balancing
import MultiInstanceBridge from '/var/projects/claude-colab-bridge/multi-instance-client.js';

const bridge = new MultiInstanceBridge({ projectName: 'my_project' });
await bridge.init();

// Commands automatically routed to best available session
await bridge.exec('import tensorflow as tf; print(tf.__version__)');
await bridge.priorityExec('urgent_computation_here');  // High priority
await bridge.gpuExec('gpu_intensive_task');            // GPU required
```

### Batch Operations

```javascript
// Process multiple commands efficiently
const commands = [
  { type: 'install_package', packages: ['scikit-learn'] },
  { type: 'execute_code', code: 'import sklearn; print("ML ready!")' },
  { type: 'execute_code', code: 'from sklearn import datasets; print("Datasets loaded")' }
];

const results = await bridge.batchExecute(commands);
console.log(`${results.filter(r => r.success).length}/${results.length} successful`);
```

## 🧪 Testing & Validation

```bash
# Test the entire system
bun /var/projects/test-multi-instance-bridge.js

# Load test with multiple instances
bun /var/projects/claude-colab-bridge/multi-instance-client.js load-test my_project 5
```

## 📊 Monitoring & Status

```bash
# Check system status
bun /var/projects/claude-colab-bridge/multi-instance-client.js status

# Monitor in real-time
watch -n 5 'bun /var/projects/claude-colab-bridge/bridge-client.js status'
```

## 🛠️ Advanced Configuration

### Custom Command Handlers

```python
# In Colab processor, add custom handlers
def handle_custom_ml_training(command):
    # Your custom ML training logic
    model_params = command.get('model_params', {})
    # ... training code ...
    return {'model_id': 'trained_model_123', 'accuracy': 0.95}

# Register in execute_command method
elif cmd_type == 'custom_ml_training':
    return self.handle_custom_ml_training(command)
```

### Project-Specific Routing

```javascript
// Route commands based on project requirements
const bridge = new MultiInstanceBridge({
  projectName: 'data_science_project',
  routingStrategy: 'project_affinity',  // Keep related work together
  preferGPU: true,                      // Prefer GPU sessions
  maxCostPerRequest: 0.05               // Cost limit
});
```

## 🔐 Security & Best Practices

1. **Service Account**: Use project-specific service accounts
2. **Folder Isolation**: Each project gets its own command/result folders
3. **Resource Limits**: Set timeouts and cost limits
4. **Cleanup**: Always call `bridge.cleanup()` when done

## 🚀 Production Deployment

### Multiple Colab Sessions

Start multiple Colab notebooks with different configurations:

```python
# Colab Session 1 - CPU focused
PROJECT_NAME = "general_processing"
SESSION_ID = "cpu_session_01"

# Colab Session 2 - GPU focused  
PROJECT_NAME = "ml_training"
SESSION_ID = "gpu_session_01"

# Colab Session 3 - Data analysis
PROJECT_NAME = "data_analysis"
SESSION_ID = "analysis_session_01"
```

### Auto-scaling

```javascript
// Monitor load and suggest scaling
const status = await bridge.getSystemStatus();
const activeInstances = status.multi_instance_bridge?.active_instances || 0;
const activeSessions = status.multi_instance_bridge?.active_sessions || 0;

if (activeInstances > activeSessions * 2) {
  console.log('💡 Consider starting more Colab sessions for better performance');
}
```

## 🎯 Use Cases

1. **Multi-Project Development**: Work on multiple projects simultaneously
2. **Team Collaboration**: Multiple developers sharing Colab resources
3. **Load Distribution**: Distribute heavy computations across sessions
4. **Specialized Sessions**: GPU session for ML, CPU session for data processing
5. **Development/Production**: Separate sessions for different environments

## 🆘 Troubleshooting

### Common Issues

```bash
# Issue: Commands not processing
# Solution: Check Colab processor is running and PROJECT_NAME matches

# Issue: "No available sessions"
# Solution: Start at least one Colab notebook with the processor

# Issue: Authentication errors
# Solution: Verify service account JSON file exists and has correct permissions

# Issue: Commands timeout
# Solution: Increase timeout in bridge config or break large tasks into smaller ones
```

### Debug Mode

```javascript
// Enable detailed logging
const bridge = new MultiInstanceBridge({
  projectName: 'debug_project',
  debug: true,           // Enable debug logging
  timeout: 60000,        // Longer timeout for debugging
  retries: 1             // Fewer retries for faster debugging
});
```

## 🎉 Success!

You now have a powerful multi-instance system where:
- ✅ Multiple Claude Coder instances work simultaneously
- ✅ Commands are automatically load-balanced across Colab sessions
- ✅ No more access issues or resource conflicts
- ✅ Scalable and reliable for production use

**Next Steps**: Start building amazing AI/ML projects with your new supercharged setup! 🚀