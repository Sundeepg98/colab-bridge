#!/usr/bin/env python3
"""
Local Notebook Interface with Colab Backend
Provides Jupyter-like local experience powered by Google Colab
"""

import os
import json
import time
import threading
import tempfile
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

from .universal_bridge import UniversalColabBridge
from .file_sync import FileSyncManager


class NotebookCell:
    """Represents a notebook cell"""
    
    def __init__(self, cell_type: str = "code", source: str = "", outputs: List = None):
        self.cell_type = cell_type
        self.source = source
        self.outputs = outputs or []
        self.execution_count = None
        self.metadata = {}
    
    def to_dict(self):
        return {
            "cell_type": self.cell_type,
            "source": self.source.split('\n') if isinstance(self.source, str) else self.source,
            "outputs": self.outputs,
            "execution_count": self.execution_count,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        cell = cls(
            cell_type=data.get("cell_type", "code"),
            source='\n'.join(data.get("source", [])) if isinstance(data.get("source"), list) else data.get("source", ""),
            outputs=data.get("outputs", [])
        )
        cell.execution_count = data.get("execution_count")
        cell.metadata = data.get("metadata", {})
        return cell


class LocalColabNotebook:
    """
    Local Jupyter-like interface powered by Google Colab
    Provides the comfort of local notebooks with cloud compute power
    """
    
    def __init__(self, notebook_path: str, tool_name: str = "local_notebook"):
        self.notebook_path = Path(notebook_path)
        self.tool_name = tool_name
        self.cells = []
        self.metadata = {
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3 (Colab)"
            },
            "colab": {
                "provenance": [],
                "machine_shape": "hm"
            }
        }
        
        # Initialize components
        self.colab_bridge = UniversalColabBridge(tool_name=tool_name)
        self.file_sync = FileSyncManager(
            local_dir=self.notebook_path.parent,
            colab_mount_point="/content/workspace"
        )
        
        # State management
        self.kernel_state = "idle"  # idle, busy, dead
        self.execution_count = 0
        self.running_cell = None
        self.interrupt_requested = False
        
        # Load existing notebook or create new
        if self.notebook_path.exists():
            self.load_notebook()
        else:
            self.create_new_notebook()
    
    def load_notebook(self):
        """Load notebook from file"""
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.cells = [NotebookCell.from_dict(cell_data) for cell_data in data.get("cells", [])]
            self.metadata.update(data.get("metadata", {}))
            
            print(f"📓 Loaded notebook: {self.notebook_path.name} ({len(self.cells)} cells)")
            
        except Exception as e:
            print(f"❌ Error loading notebook: {e}")
            self.create_new_notebook()
    
    def create_new_notebook(self):
        """Create new empty notebook"""
        self.cells = [NotebookCell(source="# Local Colab Notebook\nprint('Hello from local notebook powered by Colab!')")]
        print(f"📝 Created new notebook: {self.notebook_path.name}")
    
    def save_notebook(self):
        """Save notebook to file"""
        try:
            # Ensure directory exists
            self.notebook_path.parent.mkdir(parents=True, exist_ok=True)
            
            notebook_data = {
                "cells": [cell.to_dict() for cell in self.cells],
                "metadata": self.metadata,
                "nbformat": 4,
                "nbformat_minor": 2
            }
            
            with open(self.notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved notebook: {self.notebook_path.name}")
            
        except Exception as e:
            print(f"❌ Error saving notebook: {e}")
    
    def initialize_colab(self):
        """Initialize Colab connection"""
        try:
            self.colab_bridge.initialize()
            
            # Sync local files to Colab workspace
            self.file_sync.sync_to_colab()
            
            self.kernel_state = "idle"
            print(f"✅ Local notebook connected to Colab (tool: {self.tool_name})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize Colab: {e}")
            self.kernel_state = "dead"
            return False
    
    def add_cell(self, cell_type: str = "code", source: str = "", index: Optional[int] = None):
        """Add new cell to notebook"""
        cell = NotebookCell(cell_type=cell_type, source=source)
        
        if index is None:
            self.cells.append(cell)
        else:
            self.cells.insert(index, cell)
        
        print(f"➕ Added {cell_type} cell (total: {len(self.cells)})")
        return len(self.cells) - 1 if index is None else index
    
    def run_cell(self, cell_index: int, timeout: int = 60) -> Dict:
        """
        Run cell like local Jupyter but execute on Colab
        Provides local comfort with cloud power
        """
        if cell_index >= len(self.cells):
            return {"status": "error", "error": f"Cell index {cell_index} out of range"}
        
        cell = self.cells[cell_index]
        
        if cell.cell_type != "code":
            return {"status": "success", "output": ""}
        
        print(f"🚀 Running cell {cell_index + 1}/{len(self.cells)} on Colab...")
        
        # Update state
        self.kernel_state = "busy"
        self.running_cell = cell_index
        self.interrupt_requested = False
        
        start_time = time.time()
        
        try:
            # Sync local files before execution
            print("📤 Syncing local files to Colab...")
            self.file_sync.sync_to_colab()
            
            # Prepare code with workspace setup
            workspace_code = f"""
# Change to workspace directory
import os
os.chdir('/content/workspace')

# User code starts here
{cell.source}
"""
            
            # Execute on Colab
            result = self.colab_bridge.execute_code(workspace_code, timeout=timeout)
            
            execution_time = time.time() - start_time
            
            if result.get('status') == 'success':
                # Update cell with results
                self.execution_count += 1
                cell.execution_count = self.execution_count
                cell.outputs = [{
                    "output_type": "stream",
                    "name": "stdout",
                    "text": result.get('output', '')
                }]
                
                # Sync results back to local
                print("📥 Syncing results back to local...")
                self.file_sync.sync_from_colab()
                
                # Auto-save notebook
                self.save_notebook()
                
                print(f"✅ Cell executed successfully ({execution_time:.2f}s)")
                
                return {
                    "status": "success",
                    "output": result.get('output', ''),
                    "execution_time": execution_time,
                    "execution_count": self.execution_count
                }
            
            elif result.get('status') == 'error':
                # Handle errors
                cell.outputs = [{
                    "output_type": "error",
                    "ename": "ExecutionError",
                    "evalue": result.get('error', 'Unknown error'),
                    "traceback": [result.get('error', 'Unknown error')]
                }]
                
                print(f"❌ Cell execution failed ({execution_time:.2f}s)")
                return {
                    "status": "error",
                    "error": result.get('error'),
                    "execution_time": execution_time
                }
            
            else:
                print(f"⏳ Cell queued for execution ({execution_time:.2f}s)")
                return {
                    "status": "queued",
                    "message": "Execution queued - start Colab notebook",
                    "execution_time": execution_time
                }
        
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"💥 Execution error: {e}")
            
            cell.outputs = [{
                "output_type": "error",
                "ename": "SystemError",
                "evalue": str(e),
                "traceback": [str(e)]
            }]
            
            return {
                "status": "error",
                "error": str(e),
                "execution_time": execution_time
            }
        
        finally:
            self.kernel_state = "idle"
            self.running_cell = None
    
    def run_all_cells(self, timeout_per_cell: int = 60):
        """Run all cells in sequence"""
        print(f"🔄 Running all {len(self.cells)} cells...")
        
        results = []
        for i, cell in enumerate(self.cells):
            if cell.cell_type == "code":
                print(f"\n📋 Cell {i + 1}/{len(self.cells)}:")
                result = self.run_cell(i, timeout=timeout_per_cell)
                results.append(result)
                
                if result['status'] == 'error':
                    print(f"⚠️ Stopping execution due to error in cell {i + 1}")
                    break
        
        print(f"✅ Finished running cells")
        return results
    
    def interrupt_kernel(self):
        """Stop current execution (like Jupyter)"""
        if self.kernel_state == "busy":
            self.interrupt_requested = True
            print("🛑 Interrupting kernel execution...")
            
            # Note: Actual interruption would require Colab API support
            # For now, we set a flag and rely on timeout
            
            return True
        else:
            print("ℹ️ No execution to interrupt")
            return False
    
    def restart_kernel(self):
        """Restart Colab session"""
        print("🔄 Restarting kernel...")
        
        # Reset execution count
        self.execution_count = 0
        for cell in self.cells:
            cell.execution_count = None
            cell.outputs = []
        
        # Reinitialize Colab
        self.kernel_state = "dead"
        success = self.initialize_colab()
        
        if success:
            print("✅ Kernel restarted successfully")
        else:
            print("❌ Failed to restart kernel")
        
        return success
    
    def get_cell_source(self, cell_index: int) -> str:
        """Get cell source code"""
        if 0 <= cell_index < len(self.cells):
            return self.cells[cell_index].source
        return ""
    
    def set_cell_source(self, cell_index: int, source: str):
        """Update cell source code"""
        if 0 <= cell_index < len(self.cells):
            self.cells[cell_index].source = source
            self.save_notebook()
    
    def delete_cell(self, cell_index: int):
        """Delete cell from notebook"""
        if 0 <= cell_index < len(self.cells):
            deleted_cell = self.cells.pop(cell_index)
            print(f"🗑️ Deleted cell {cell_index + 1}")
            self.save_notebook()
            return True
        return False
    
    def get_notebook_info(self) -> Dict:
        """Get notebook information"""
        code_cells = sum(1 for cell in self.cells if cell.cell_type == "code")
        markdown_cells = sum(1 for cell in self.cells if cell.cell_type == "markdown")
        
        return {
            "path": str(self.notebook_path),
            "total_cells": len(self.cells),
            "code_cells": code_cells,
            "markdown_cells": markdown_cells,
            "kernel_state": self.kernel_state,
            "execution_count": self.execution_count,
            "tool_name": self.tool_name
        }
    
    def __str__(self):
        return f"LocalColabNotebook({self.notebook_path.name}, {len(self.cells)} cells, {self.kernel_state})"


def create_local_notebook(notebook_path: str, tool_name: str = "local_notebook") -> LocalColabNotebook:
    """
    Create a new local notebook with Colab backend
    
    Args:
        notebook_path: Path to notebook file (.ipynb)
        tool_name: Name of the tool using this notebook
    
    Returns:
        LocalColabNotebook instance
    """
    notebook = LocalColabNotebook(notebook_path, tool_name)
    
    if notebook.initialize_colab():
        return notebook
    else:
        raise RuntimeError("Failed to initialize Colab connection")


if __name__ == "__main__":
    # Demo usage
    print("🎯 Local Colab Notebook Demo")
    print("=" * 50)
    
    # Create demo notebook
    demo_path = "/tmp/demo_local_colab.ipynb"
    notebook = LocalColabNotebook(demo_path, "demo")
    
    if notebook.initialize_colab():
        print(f"\n📓 Notebook info: {notebook.get_notebook_info()}")
        
        # Add some demo cells
        notebook.add_cell("code", "print('Hello from local notebook!')")
        notebook.add_cell("code", "import datetime\nprint(f'Current time: {datetime.datetime.now()}')")
        notebook.add_cell("code", "import torch\nprint(f'PyTorch available: {torch.__version__ if torch else \"Not installed\"}')")
        
        # Run all cells
        results = notebook.run_all_cells()
        
        print(f"\n📊 Execution summary: {len(results)} cells executed")
        
    else:
        print("❌ Failed to initialize demo notebook")