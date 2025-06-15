#!/usr/bin/env python3
"""
Local Notebook Demo - Jupyter-like controls with Colab power
Demonstrates run/stop/debug controls like traditional Jupyter
"""

import os
import sys
import time
import signal
import threading
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from colab_integration.local_notebook import LocalColabNotebook, create_local_notebook


class IDENotebookController:
    """
    Simulates IDE notebook controls like VS Code, PyCharm, etc.
    Provides run/stop/debug functionality for local notebooks with Colab backend
    """
    
    def __init__(self, notebook_path: str, ide_name: str = "demo_ide"):
        self.notebook_path = notebook_path
        self.ide_name = ide_name
        self.notebook = None
        self.current_execution = None
        self.execution_thread = None
        
    def initialize(self):
        """Initialize notebook connection"""
        try:
            print(f"🎮 {self.ide_name} - Initializing notebook controls...")
            self.notebook = LocalColabNotebook(self.notebook_path, self.ide_name)
            
            if self.notebook.initialize_colab():
                print(f"✅ {self.ide_name} connected to local notebook with Colab backend")
                return True
            else:
                print(f"❌ Failed to initialize {self.ide_name} notebook")
                return False
                
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            return False
    
    def run_cell(self, cell_index: int, timeout: int = 60):
        """Run cell with IDE-like controls"""
        if not self.notebook:
            print("❌ Notebook not initialized")
            return None
        
        print(f"\n▶️ {self.ide_name} - Running cell {cell_index + 1}")
        print("─" * 50)
        
        # Show cell content
        cell_source = self.notebook.get_cell_source(cell_index)
        print(f"📄 Cell source:")
        print(cell_source[:200] + "..." if len(cell_source) > 200 else cell_source)
        print("─" * 50)
        
        # Execute with progress tracking
        def execute_with_progress():
            try:
                result = self.notebook.run_cell(cell_index, timeout=timeout)
                self.current_execution = result
                return result
            except Exception as e:
                self.current_execution = {"status": "error", "error": str(e)}
                return self.current_execution
        
        # Run in thread for interrupt capability
        self.execution_thread = threading.Thread(target=execute_with_progress)
        self.execution_thread.start()
        
        # Show progress
        start_time = time.time()
        while self.execution_thread.is_alive():
            elapsed = int(time.time() - start_time)
            print(f"⏳ Executing on Colab... {elapsed}s", end='\r')
            time.sleep(0.5)
        
        self.execution_thread.join()
        print()  # New line after progress
        
        # Show results
        if self.current_execution:
            self.show_execution_result(self.current_execution)
        
        return self.current_execution
    
    def run_all_cells(self):
        """Run all cells like Jupyter 'Run All'"""
        if not self.notebook:
            print("❌ Notebook not initialized")
            return
        
        print(f"\n🔄 {self.ide_name} - Running all cells...")
        
        results = self.notebook.run_all_cells()
        
        # Summary
        successful = sum(1 for r in results if r.get('status') == 'success')
        failed = sum(1 for r in results if r.get('status') == 'error')
        
        print(f"\n📊 Execution Summary:")
        print(f"  ✅ Successful: {successful}")
        print(f"  ❌ Failed: {failed}")
        print(f"  📊 Total: {len(results)}")
        
        return results
    
    def stop_execution(self):
        """Stop current execution (interrupt kernel)"""
        print(f"\n🛑 {self.ide_name} - Stopping execution...")
        
        if self.notebook:
            success = self.notebook.interrupt_kernel()
            if success:
                print("✅ Execution interrupted")
            else:
                print("ℹ️ No execution to stop")
            return success
        
        return False
    
    def restart_kernel(self):
        """Restart kernel like Jupyter"""
        print(f"\n🔄 {self.ide_name} - Restarting kernel...")
        
        if self.notebook:
            success = self.notebook.restart_kernel()
            if success:
                print("✅ Kernel restarted - all variables cleared")
            else:
                print("❌ Failed to restart kernel")
            return success
        
        return False
    
    def debug_cell(self, cell_index: int):
        """Run cell in debug mode with enhanced error information"""
        if not self.notebook:
            print("❌ Notebook not initialized")
            return None
        
        print(f"\n🐛 {self.ide_name} - Debug mode: Cell {cell_index + 1}")
        
        # Get original cell source
        original_source = self.notebook.get_cell_source(cell_index)
        
        # Wrap with debug code
        debug_source = f"""
import sys
import traceback
import time
from datetime import datetime

print("🐛 DEBUG: Starting cell execution")
print(f"🐛 DEBUG: Timestamp: {{datetime.now()}}")
print(f"🐛 DEBUG: Python version: {{sys.version}}")
print("🐛 DEBUG: Current working directory:", end=" ")

import os
print(os.getcwd())

print("🐛 DEBUG: Available memory:", end=" ")
try:
    import psutil
    memory = psutil.virtual_memory()
    print(f"{{memory.available / 1e9:.1f}} GB available")
except ImportError:
    print("psutil not available")

print("🐛 DEBUG: GPU status:", end=" ")
try:
    import torch
    if torch.cuda.is_available():
        print(f"CUDA {{torch.version.cuda}} - {{torch.cuda.get_device_name(0)}}")
    else:
        print("No CUDA available")
except ImportError:
    print("PyTorch not available")

print("─" * 40)
print("🐛 DEBUG: Executing user code...")
print("─" * 40)

try:
    # Original cell code starts here
    start_time = time.time()
    
{original_source}
    
    execution_time = time.time() - start_time
    print("─" * 40)
    print(f"🐛 DEBUG: Cell completed successfully in {{execution_time:.2f}}s")
    
except Exception as e:
    execution_time = time.time() - start_time
    print("─" * 40)
    print(f"🐛 DEBUG: Error occurred after {{execution_time:.2f}}s")
    print(f"🐛 DEBUG: Error type: {{type(e).__name__}}")
    print(f"🐛 DEBUG: Error message: {{str(e)}}")
    print("🐛 DEBUG: Full traceback:")
    traceback.print_exc()
    print("─" * 40)
    raise

print("🐛 DEBUG: Cell execution finished")
"""
        
        # Temporarily replace cell source
        self.notebook.set_cell_source(cell_index, debug_source)
        
        # Execute debug version
        result = self.run_cell(cell_index)
        
        # Restore original source
        self.notebook.set_cell_source(cell_index, original_source)
        
        return result
    
    def show_execution_result(self, result: dict):
        """Display execution results like IDE output"""
        status = result.get('status', 'unknown')
        execution_time = result.get('execution_time', 0)
        
        if status == 'success':
            print(f"✅ Execution completed in {execution_time:.2f}s")
            output = result.get('output', '')
            if output:
                print("📤 Output:")
                print("─" * 30)
                print(output)
                print("─" * 30)
            else:
                print("📝 No output")
        
        elif status == 'error':
            print(f"❌ Execution failed in {execution_time:.2f}s")
            error = result.get('error', 'Unknown error')
            print("🚨 Error:")
            print("─" * 30)
            print(error)
            print("─" * 30)
        
        elif status == 'queued':
            print(f"⏳ Execution queued ({execution_time:.2f}s)")
            print("💡 Start the Colab notebook to process the request")
        
        else:
            print(f"❓ Unknown status: {status}")
    
    def add_cell(self, cell_type: str = "code", source: str = ""):
        """Add new cell (like clicking + in IDE)"""
        if self.notebook:
            index = self.notebook.add_cell(cell_type, source)
            print(f"➕ Added {cell_type} cell at index {index}")
            return index
        return None
    
    def delete_cell(self, cell_index: int):
        """Delete cell (like clicking delete in IDE)"""
        if self.notebook:
            success = self.notebook.delete_cell(cell_index)
            if success:
                print(f"🗑️ Deleted cell {cell_index + 1}")
            return success
        return False
    
    def get_notebook_status(self):
        """Get current notebook status"""
        if self.notebook:
            info = self.notebook.get_notebook_info()
            print(f"\n📊 {self.ide_name} Notebook Status:")
            print(f"  📓 File: {info['path']}")
            print(f"  📄 Cells: {info['total_cells']} ({info['code_cells']} code, {info['markdown_cells']} markdown)")
            print(f"  🔄 Kernel: {info['kernel_state']}")
            print(f"  🔢 Execution count: {info['execution_count']}")
            return info
        return None


def demo_ide_controls():
    """Demonstrate IDE-like notebook controls"""
    print("🎮 IDE Notebook Controls Demo")
    print("=" * 60)
    print("Simulating VS Code/PyCharm/Cursor notebook experience")
    print("with Google Colab backend for compute power")
    print("=" * 60)
    
    # Create demo notebook
    demo_path = "/tmp/ide_demo_notebook.ipynb"
    ide = IDENotebookController(demo_path, "VSCode_Demo")
    
    if not ide.initialize():
        print("❌ Failed to initialize IDE controls")
        return
    
    # Setup demo notebook with various cell types
    print("\n📝 Setting up demo notebook...")
    
    # Clear existing cells and add demo cells
    ide.notebook.cells = []
    
    # Cell 1: Welcome
    ide.add_cell("markdown", "# Local Notebook with Colab Power\nThis notebook runs locally but executes on Google's cloud!")
    
    # Cell 2: Basic Python
    ide.add_cell("code", """
print("Hello from local IDE with Colab backend!")
import datetime
print(f"Executed at: {datetime.datetime.now()}")

# Test basic computation
numbers = list(range(1, 11))
total = sum(numbers)
average = total / len(numbers)
print(f"Numbers: {numbers}")
print(f"Sum: {total}, Average: {average}")
""")
    
    # Cell 3: GPU check
    ide.add_cell("code", """
print("🔍 Checking GPU availability...")

try:
    import torch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        device = torch.cuda.get_device_name(0)
        memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"GPU: {device}")
        print(f"GPU Memory: {memory:.1f} GB")
        
        # Simple GPU computation
        x = torch.randn(1000, 1000).cuda()
        y = torch.mm(x, x.t())
        print(f"GPU computation test: {y.shape}")
    else:
        print("No GPU available")
        
except ImportError:
    print("PyTorch not installed")

print("✅ GPU check completed")
""")
    
    # Cell 4: Error demonstration
    ide.add_cell("code", """
# This cell will cause an error for debugging demo
print("This will cause an error...")
undefined_variable = some_undefined_variable  # This will fail
print("This line won't execute")
""")
    
    # Cell 5: File operations
    ide.add_cell("code", """
print("📁 Testing file operations...")

# Create a test file
with open('test_output.txt', 'w') as f:
    f.write("Hello from Colab!\\n")
    f.write(f"Created at: {datetime.datetime.now()}\\n")

# Read it back
with open('test_output.txt', 'r') as f:
    content = f.read()

print("File content:")
print(content)
print("✅ File operations completed")
""")
    
    # Save notebook
    ide.notebook.save_notebook()
    
    # Show notebook status
    ide.get_notebook_status()
    
    # Demo different IDE features
    print("\n🎯 Demo 1: Run Single Cell")
    ide.run_cell(1)  # Run basic Python cell
    
    print("\n🎯 Demo 2: Run GPU Check")
    ide.run_cell(2)  # Run GPU check
    
    print("\n🎯 Demo 3: Debug Error Cell")
    ide.debug_cell(3)  # Debug the error cell
    
    print("\n🎯 Demo 4: File Operations")
    ide.run_cell(4)  # Run file operations
    
    print("\n🎯 Demo 5: Restart Kernel")
    ide.restart_kernel()
    
    print("\n🎯 Demo 6: Run All Cells")
    # Skip error cell for run-all demo
    ide.notebook.delete_cell(3)
    ide.run_all_cells()
    
    # Final status
    print("\n📊 Final Status:")
    ide.get_notebook_status()
    
    print("\n🎉 IDE Controls Demo Complete!")
    print("=" * 60)
    print("✅ All IDE-like features demonstrated:")
    print("  • Run single cells")
    print("  • Run all cells")
    print("  • Debug mode")
    print("  • Stop/restart kernel")
    print("  • Add/delete cells")
    print("  • File synchronization")
    print("  • Real-time output")
    print("  • Error handling")


def interactive_demo():
    """Interactive demo for testing controls"""
    print("\n🎮 Interactive IDE Controls Demo")
    print("Commands: run <cell>, debug <cell>, restart, status, quit")
    
    demo_path = "/tmp/interactive_notebook.ipynb"
    ide = IDENotebookController(demo_path, "Interactive_IDE")
    
    if not ide.initialize():
        print("❌ Failed to initialize")
        return
    
    # Add some demo cells
    ide.add_cell("code", "print('Hello from interactive notebook!')")
    ide.add_cell("code", "import math\nprint(f'Pi = {math.pi}')")
    ide.add_cell("code", "x = [1, 2, 3, 4, 5]\nprint(f'Numbers: {x}, Sum: {sum(x)}')")
    
    ide.get_notebook_status()
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command.startswith("run "):
                try:
                    cell_index = int(command.split()[1]) - 1
                    ide.run_cell(cell_index)
                except (IndexError, ValueError):
                    print("Usage: run <cell_number>")
            
            elif command.startswith("debug "):
                try:
                    cell_index = int(command.split()[1]) - 1
                    ide.debug_cell(cell_index)
                except (IndexError, ValueError):
                    print("Usage: debug <cell_number>")
            
            elif command == "restart":
                ide.restart_kernel()
            
            elif command == "status":
                ide.get_notebook_status()
            
            elif command == "stop":
                ide.stop_execution()
            
            elif command in ["quit", "exit"]:
                print("👋 Goodbye!")
                break
            
            else:
                print("Commands: run <cell>, debug <cell>, restart, status, stop, quit")
        
        except KeyboardInterrupt:
            print("\n🛑 Interrupted")
            break


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_demo()
    else:
        demo_ide_controls()