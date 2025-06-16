#!/usr/bin/env python3
"""
Interactive VS Code Extension Test
Run this to test the extension functionality interactively
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.api_based_execution import VSCodeAPIBridge

def main():
    print("🎯 INTERACTIVE VS CODE EXTENSION TEST")
    print("=" * 50)
    
    # Initialize the bridge
    vscode = VSCodeAPIBridge()
    
    print("\n✅ Extension loaded! You can now:")
    print("1. Enter Python code")
    print("2. Press Enter twice to execute")
    print("3. Type 'quit' to exit")
    print("4. Type 'config' to see configuration")
    
    while True:
        print("\n" + "─" * 30)
        print("📝 Enter Python code (Ctrl+Shift+C simulation):")
        
        # Collect multi-line input
        lines = []
        while True:
            try:
                line = input(">>> " if not lines else "... ")
                if line.strip() == "quit":
                    print("👋 Goodbye!")
                    return
                elif line.strip() == "config":
                    config = vscode.configure()
                    print(f"\n🔧 Configuration:")
                    print(f"   Providers: {config['available_providers']}")
                    print(f"   Current: {config['current_provider']}")
                    if config['setup_required']:
                        print(f"   GPU Setup: {len(config['setup_required'])} options available")
                    break
                elif line.strip() == "":
                    if lines:
                        break
                    continue
                else:
                    lines.append(line)
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return
            except EOFError:
                print("\n👋 Goodbye!")
                return
        
        if lines:
            code = "\n".join(lines)
            print(f"\n⚡ Executing code...")
            print("📺 VS Code Output:")
            print("┌" + "─" * 48 + "┐")
            
            try:
                output = vscode.execute_selection(code)
                for line in output.split('\n'):
                    if line.strip():
                        print(f"│ {line:<46} │")
                print("└" + "─" * 48 + "┘")
            except Exception as e:
                print(f"│ ❌ Error: {str(e):<37} │")
                print("└" + "─" * 48 + "┘")

if __name__ == "__main__":
    main()