#!/usr/bin/env python3
"""
Demo: IDE Control Features with Colab Bridge
Shows how IDEs can run/stop/debug code in Google Colab
"""

import time
import threading
from colab_integration import UniversalColabBridge

class IDEControlDemo:
    """Simulate IDE controls for Colab execution"""
    
    def __init__(self, ide_name="demo_ide"):
        self.bridge = UniversalColabBridge(tool_name=ide_name)
        self.running_requests = {}
        
    def initialize(self):
        """Initialize Colab connection"""
        self.bridge.initialize()
        print(f"✅ {self.bridge.tool_name} connected to Colab")
    
    def run_code(self, code, timeout=60):
        """Run code with IDE-like controls"""
        print(f"\n🚀 Running code in Colab...")
        print("─" * 50)
        print(code[:100] + "..." if len(code) > 100 else code)
        print("─" * 50)
        
        start_time = time.time()
        
        try:
            result = self.bridge.execute_code(code, timeout=timeout)
            
            execution_time = time.time() - start_time
            
            if result.get('status') == 'success':
                print(f"✅ Execution completed ({execution_time:.2f}s)")
                print(f"📤 Output:")
                print(result.get('output', 'No output'))
                return result
            elif result.get('status') == 'error':
                print(f"❌ Execution failed ({execution_time:.2f}s)")
                print(f"Error: {result.get('error')}")
                return result
            else:
                print(f"⏳ Request queued ({execution_time:.2f}s)")
                print("Start Colab notebook to process")
                return result
                
        except TimeoutError:
            print(f"⏱️ Execution timed out after {timeout}s")
            return {"status": "timeout", "execution_time": timeout}
        except KeyboardInterrupt:
            print(f"\n🛑 Execution cancelled by user")
            return {"status": "cancelled", "execution_time": time.time() - start_time}
    
    def run_with_progress(self, code, timeout=60):
        """Run code with progress indication"""
        print(f"\n⚡ Running with progress tracking...")
        
        # Start execution in background
        result = {"status": "running"}
        
        def execute():
            nonlocal result
            result = self.bridge.execute_code(code, timeout=timeout)
        
        thread = threading.Thread(target=execute)
        thread.start()
        
        # Show progress
        start_time = time.time()
        while thread.is_alive():
            elapsed = int(time.time() - start_time)
            print(f"⏳ Executing... {elapsed}s elapsed", end='\r')
            time.sleep(1)
        
        thread.join()
        print()  # New line after progress
        
        return result
    
    def debug_execution(self, code):
        """Run code with debug information"""
        print(f"\n🔍 Debug mode execution...")
        
        # Add debug information to code
        debug_code = f'''
import sys
import time
import traceback
from datetime import datetime

print("🐛 DEBUG: Starting execution")
print(f"🐛 DEBUG: Python version: {{sys.version}}")
print(f"🐛 DEBUG: Execution time: {{datetime.now()}}")

try:
    # User code starts here
{code}
    print("🐛 DEBUG: User code completed successfully")
    
except Exception as e:
    print(f"🐛 DEBUG: Error occurred: {{e}}")
    print(f"🐛 DEBUG: Traceback:")
    traceback.print_exc()
    raise

print("🐛 DEBUG: Execution finished")
'''
        
        return self.run_code(debug_code)

def demo_ide_features():
    """Demonstrate IDE-like features"""
    print("🎮 IDE Control Demo for Colab Bridge")
    print("=" * 60)
    
    # Initialize IDE
    ide = IDEControlDemo("VSCode_Demo")
    ide.initialize()
    
    # Demo 1: Basic execution
    print("\n📋 Demo 1: Basic Code Execution")
    basic_code = '''
print("Hello from IDE → Colab!")
import datetime
print(f"Executed at: {datetime.datetime.now()}")

# Simple computation
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(f"Sum: {total}")
'''
    
    result1 = ide.run_code(basic_code, timeout=30)
    
    # Demo 2: ML Code with GPU
    print("\n📋 Demo 2: ML Code with GPU Check")
    ml_code = '''
print("🧠 ML Demo: Checking GPU availability")

try:
    import torch
    print(f"PyTorch available: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        
        # Create tensor on GPU
        x = torch.randn(1000, 1000).cuda()
        y = torch.mm(x, x.t())
        print(f"GPU computation result shape: {y.shape}")
    else:
        print("No GPU available")
        
except ImportError:
    print("PyTorch not available")

print("✅ ML demo completed")
'''
    
    result2 = ide.run_code(ml_code, timeout=30)
    
    # Demo 3: Debug execution
    print("\n📋 Demo 3: Debug Mode Execution")
    debug_code = '''
# This code has a deliberate issue for debugging
numbers = [1, 2, 3, 4, 5]
result = sum(numbers) / len(numbers)
print(f"Average: {result}")
'''
    
    result3 = ide.debug_execution(debug_code)
    
    # Demo 4: Error handling
    print("\n📋 Demo 4: Error Handling")
    error_code = '''
# This will cause an error
undefined_variable = some_undefined_variable
print(undefined_variable)
'''
    
    result4 = ide.run_code(error_code, timeout=10)
    
    # Summary
    print("\n📊 Demo Summary:")
    print("=" * 60)
    print("✅ Basic execution - IDE can run Python code in Colab")
    print("✅ ML/GPU code - Access to Google's GPUs from IDE")  
    print("✅ Debug mode - Enhanced error information")
    print("✅ Error handling - Proper error reporting")
    print("✅ Progress tracking - Real-time execution status")
    print("✅ Timeout control - Prevent hanging operations")

def compare_with_jupyter():
    """Compare with traditional Jupyter"""
    print("\n🆚 Comparison: Jupyter vs Colab Bridge")
    print("=" * 60)
    
    comparison = """
┌─────────────────┬─────────────────┬─────────────────┐
│ Feature         │ Local Jupyter   │ Colab Bridge    │
├─────────────────┼─────────────────┼─────────────────┤
│ Execution       │ Local machine   │ Google's cloud  │
│ GPU Access      │ Only if local   │ Free Tesla T4   │
│ RAM             │ Your RAM        │ 12-25 GB        │
│ Setup           │ Install needed  │ Zero setup      │
│ Libraries       │ pip install     │ Pre-installed   │
│ Persistence     │ Local files     │ Google Drive    │
│ Collaboration   │ Hard to share   │ Easy sharing    │
│ Cost            │ Hardware cost   │ Free            │
│ Internet        │ Not required    │ Required        │
│ Control         │ Full control    │ Some limits     │
└─────────────────┴─────────────────┴─────────────────┘
"""
    
    print(comparison)
    
    print("\n🎯 Best Use Cases:")
    print("📋 Traditional Jupyter:")
    print("  - Quick prototyping and debugging")
    print("  - Interactive data exploration")
    print("  - Offline development")
    print("  - Real-time variable inspection")
    
    print("\n🚀 Colab Bridge:")
    print("  - ML model training")
    print("  - Large dataset processing")
    print("  - GPU-intensive computations")
    print("  - Heavy numerical analysis")
    print("  - No local GPU available")

if __name__ == "__main__":
    demo_ide_features()
    compare_with_jupyter()