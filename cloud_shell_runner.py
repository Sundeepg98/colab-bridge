#!/usr/bin/env python3
"""
Cloud Shell Editor Integration
Provides "Run in Colab" functionality for Cloud Shell Editor
"""

import sys
import os
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.api_based_execution import VSCodeAPIBridge

def main():
    if len(sys.argv) < 2:
        show_usage()
        return
    
    command = sys.argv[1]
    
    if command == "run":
        if len(sys.argv) < 3:
            print("❌ Usage: python3 cloud_shell_runner.py run <file.py>")
            return
        run_file(sys.argv[2])
    
    elif command == "selection":
        run_selection()
    
    elif command == "interactive":
        interactive_mode()
    
    elif command == "setup":
        setup_shortcuts()
    
    else:
        show_usage()

def run_file(file_path):
    """Run entire Python file in Colab"""
    print(f"🚀 Running {file_path} in Colab...")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        vscode = VSCodeAPIBridge()
        result = vscode.execute_selection(code)
        
        print("📺 Colab Output:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        print("✅ Execution completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def run_selection():
    """Run code from stdin (for selected text)"""
    print("📝 Paste your Python code (Ctrl+D to execute):")
    
    try:
        code = sys.stdin.read()
        if not code.strip():
            print("❌ No code provided")
            return
        
        print("🚀 Executing in Colab...")
        vscode = VSCodeAPIBridge()
        result = vscode.execute_selection(code)
        
        print("📺 Colab Output:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        print("✅ Execution completed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")

def interactive_mode():
    """Interactive mode for testing code"""
    print("🎯 Interactive Colab Mode")
    print("Type Python code, press Enter twice to execute, 'quit' to exit")
    
    vscode = VSCodeAPIBridge()
    
    while True:
        print("\n" + "─" * 30)
        print("📝 Enter Python code:")
        
        lines = []
        while True:
            try:
                line = input(">>> " if not lines else "... ")
                if line.strip() == "quit":
                    print("👋 Goodbye!")
                    return
                elif line.strip() == "":
                    if lines:
                        break
                    continue
                else:
                    lines.append(line)
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Goodbye!")
                return
        
        if lines:
            code = "\n".join(lines)
            print("\n🚀 Executing...")
            
            try:
                result = vscode.execute_selection(code)
                print("📺 Output:")
                print("┌" + "─" * 48 + "┐")
                for line in result.split('\n'):
                    if line.strip():
                        print(f"│ {line:<46} │")
                print("└" + "─" * 48 + "┘")
            except Exception as e:
                print(f"❌ Error: {e}")

def setup_shortcuts():
    """Setup convenient shell aliases"""
    print("🔧 Setting up Cloud Shell shortcuts...")
    
    aliases = """
# Colab Bridge shortcuts for Cloud Shell
alias runcolab='python3 /home/sundeepg8/projects/colab-bridge/cloud_shell_runner.py'
alias colab-run='python3 /home/sundeepg8/projects/colab-bridge/cloud_shell_runner.py run'
alias colab-interactive='python3 /home/sundeepg8/projects/colab-bridge/cloud_shell_runner.py interactive'
alias colab-selection='python3 /home/sundeepg8/projects/colab-bridge/cloud_shell_runner.py selection'

# Quick execution aliases
alias pycolab='colab-run'
alias pyrun='colab-run'
"""
    
    bashrc_path = os.path.expanduser("~/.bashrc")
    
    # Check if aliases already exist
    if os.path.exists(bashrc_path):
        with open(bashrc_path, 'r') as f:
            content = f.read()
        
        if "Colab Bridge shortcuts" in content:
            print("✅ Shortcuts already installed!")
            print_usage_examples()
            return
    
    # Add aliases
    with open(bashrc_path, 'a') as f:
        f.write("\n" + aliases)
    
    print("✅ Shortcuts installed! Run: source ~/.bashrc")
    print("\n🎯 New commands available:")
    print_usage_examples()

def print_usage_examples():
    """Print usage examples"""
    examples = [
        ("colab-run myfile.py", "Run entire Python file"),
        ("colab-interactive", "Start interactive mode"),
        ("colab-selection", "Run selected code (paste mode)"),
        ("echo 'print(42)' | colab-selection", "Pipe code directly")
    ]
    
    for cmd, desc in examples:
        print(f"   {cmd:<30} # {desc}")

def show_usage():
    """Show usage information"""
    print("🚀 Cloud Shell Editor Colab Integration")
    print("=" * 50)
    print("Usage:")
    print("  python3 cloud_shell_runner.py <command> [args]")
    print()
    print("Commands:")
    print("  run <file.py>     Run entire Python file")
    print("  selection         Run code from input (paste mode)")
    print("  interactive       Interactive code execution")
    print("  setup            Install shell shortcuts")
    print()
    print("Examples:")
    print("  python3 cloud_shell_runner.py run test.py")
    print("  python3 cloud_shell_runner.py interactive")
    print("  echo 'print(42)' | python3 cloud_shell_runner.py selection")
    print()
    print("After setup:")
    print("  colab-run test.py")
    print("  colab-interactive")

if __name__ == "__main__":
    main()