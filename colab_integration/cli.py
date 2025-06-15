#!/usr/bin/env python3
"""
Colab Bridge - Command Line Interface
Universal Google Colab integration for any IDE or tool
"""

import argparse
import sys
import json
import os
from pathlib import Path
from .universal_bridge import UniversalColabBridge

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Colab Bridge - Execute code in Google Colab from any tool",
        prog="colab-bridge"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Execute command
    execute_parser = subparsers.add_parser("execute", help="Execute code in Colab")
    execute_parser.add_argument("--code", "-c", help="Python code to execute")
    execute_parser.add_argument("--file", "-f", help="Python file to execute")
    execute_parser.add_argument("--tool", "-t", default="cli", help="Tool name (default: cli)")
    execute_parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds")
    execute_parser.add_argument("--output", "-o", choices=["json", "text"], default="text", help="Output format")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup Colab Bridge")
    setup_parser.add_argument("--service-account", help="Path to service account JSON")
    setup_parser.add_argument("--folder-id", help="Google Drive folder ID")
    setup_parser.add_argument("--interactive", "-i", action="store_true", help="Interactive setup")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check Colab Bridge status")
    
    # Notebook command
    notebook_parser = subparsers.add_parser("notebook", help="Manage Colab notebooks")
    notebook_parser.add_argument("action", choices=["upload", "open", "list"], help="Notebook action")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "execute":
        execute_command(args)
    elif args.command == "setup":
        setup_command(args)
    elif args.command == "status":
        status_command(args)
    elif args.command == "notebook":
        notebook_command(args)

def execute_command(args=None):
    """Execute code in Colab"""
    if args is None:
        # Called directly
        parser = argparse.ArgumentParser(description="Execute code in Google Colab")
        parser.add_argument("--code", "-c", help="Python code to execute")
        parser.add_argument("--file", "-f", help="Python file to execute")
        parser.add_argument("--tool", "-t", default="cli", help="Tool name")
        parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds")
        parser.add_argument("--output", "-o", choices=["json", "text"], default="text", help="Output format")
        args = parser.parse_args()
    
    # Get code to execute
    if args.code:
        code = args.code
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        with open(args.file, 'r') as f:
            code = f.read()
    else:
        print("Error: Must provide either --code or --file", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Initialize bridge
        bridge = UniversalColabBridge(tool_name=args.tool)
        bridge.initialize()
        
        # Execute code
        result = bridge.execute_code(code, timeout=args.timeout)
        
        # Output result
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            if result.get('status') == 'success':
                print("✅ Success!")
                if result.get('output'):
                    print("\nOutput:")
                    print("-" * 40)
                    print(result['output'])
                    print("-" * 40)
            elif result.get('status') == 'error':
                print("❌ Error!")
                print(f"Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)
            else:
                print("⏳ Request queued for processing")
                print(f"Request ID: {result.get('request_id', 'unknown')}")
                print("Start the Colab notebook to process it!")
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def setup_command(args):
    """Setup Colab Bridge configuration"""
    config_file = Path.home() / ".colab-bridge" / "config.json"
    config_file.parent.mkdir(exist_ok=True)
    
    config = {}
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
    
    if args.interactive:
        print("🔧 Colab Bridge Interactive Setup")
        print("=" * 40)
        
        # Service account
        sa_path = input(f"Service account JSON path [{config.get('service_account_path', '')}]: ").strip()
        if sa_path:
            config['service_account_path'] = sa_path
        
        # Folder ID
        folder_id = input(f"Google Drive folder ID [{config.get('google_drive_folder_id', '')}]: ").strip()
        if folder_id:
            config['google_drive_folder_id'] = folder_id
        
    else:
        if args.service_account:
            config['service_account_path'] = args.service_account
        if args.folder_id:
            config['google_drive_folder_id'] = args.folder_id
    
    # Save config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to {config_file}")

def status_command(args):
    """Check Colab Bridge status"""
    try:
        bridge = UniversalColabBridge(tool_name="status")
        bridge.initialize()
        
        print("✅ Colab Bridge Status")
        print("=" * 30)
        print(f"Service Account: {bridge.config.get('service_account_path', 'Not configured')}")
        print(f"Drive Folder: {bridge.folder_id}")
        print(f"Instance ID: {bridge.instance_id}")
        
        # Check pending requests
        query = f"'{bridge.folder_id}' in parents and name contains 'command_' and trashed=false"
        results = bridge.drive_service.files().list(q=query, fields="files(id, name)").execute()
        pending = len(results.get('files', []))
        
        print(f"Pending requests: {pending}")
        print("Status: Ready ✅")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def notebook_command(args):
    """Manage Colab notebooks"""
    if args.action == "open":
        import webbrowser
        notebook_url = "https://colab.research.google.com/drive/1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA"
        print(f"Opening Colab notebook: {notebook_url}")
        webbrowser.open(notebook_url)
    
    elif args.action == "upload":
        print("📤 Uploading notebooks to Google Drive...")
        # Implementation for uploading notebooks
        
    elif args.action == "list":
        print("📋 Available notebooks:")
        print("- Hybrid Processor (auto-run + debug)")
        print("- Interactive Debug (step-by-step)")
        print("- Auto Script (fully automated)")

if __name__ == "__main__":
    main()