#!/usr/bin/env python3
"""
File Synchronization Manager
Handles bidirectional sync between local files and Colab workspace
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Set, Optional
from pathlib import Path
from datetime import datetime

from .universal_bridge import UniversalColabBridge


class FileSyncManager:
    """
    Manages file synchronization between local directory and Colab workspace
    Provides seamless file access for hybrid local/cloud development
    """
    
    def __init__(self, local_dir: str, colab_mount_point: str = "/content/workspace"):
        self.local_dir = Path(local_dir).resolve()
        self.colab_mount = colab_mount_point
        self.bridge = UniversalColabBridge(tool_name="file_sync")
        
        # Sync state
        self.local_state = {}
        self.colab_state = {}
        self.last_sync = None
        
        # Sync configuration
        self.sync_patterns = {
            "include": ["*.py", "*.ipynb", "*.txt", "*.csv", "*.json", "*.md"],
            "exclude": ["__pycache__", ".git", ".env", "*.pyc", "node_modules"]
        }
        
        # Create local directory if it doesn't exist
        self.local_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 FileSyncManager: {self.local_dir} ↔ {self.colab_mount}")
    
    def should_sync_file(self, file_path: Path) -> bool:
        """Check if file should be synced based on patterns"""
        file_name = file_path.name
        file_str = str(file_path)
        
        # Check exclude patterns
        for pattern in self.sync_patterns["exclude"]:
            if pattern in file_str or file_name.startswith('.'):
                return False
        
        # Check include patterns
        for pattern in self.sync_patterns["include"]:
            if pattern == "*" or file_name.endswith(pattern.replace("*", "")):
                return True
        
        return False
    
    def get_file_hash(self, file_path: Path) -> str:
        """Get file hash for change detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def scan_local_files(self) -> Dict[str, Dict]:
        """Scan local directory for files"""
        files = {}
        
        for file_path in self.local_dir.rglob("*"):
            if file_path.is_file() and self.should_sync_file(file_path):
                rel_path = file_path.relative_to(self.local_dir)
                
                files[str(rel_path)] = {
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime,
                    "hash": self.get_file_hash(file_path)
                }
        
        return files
    
    def get_modified_files(self) -> List[str]:
        """Get list of locally modified files"""
        current_state = self.scan_local_files()
        modified = []
        
        for rel_path, file_info in current_state.items():
            if rel_path not in self.local_state:
                modified.append(rel_path)  # New file
            elif file_info["hash"] != self.local_state[rel_path].get("hash"):
                modified.append(rel_path)  # Modified file
        
        # Update local state
        self.local_state = current_state
        
        return modified
    
    def sync_to_colab(self) -> bool:
        """Upload local changes to Colab workspace"""
        try:
            print("📤 Syncing local files to Colab...")
            
            # Get modified files
            modified_files = self.get_modified_files()
            
            if not modified_files:
                print("✅ No local changes to sync")
                return True
            
            print(f"📋 Uploading {len(modified_files)} files to Colab...")
            
            # Create workspace setup code
            setup_code = f"""
import os
import base64
import json

# Create workspace directory
workspace_dir = '{self.colab_mount}'
os.makedirs(workspace_dir, exist_ok=True)
os.chdir(workspace_dir)

print(f"📁 Workspace ready: {{workspace_dir}}")
"""
            
            # Execute workspace setup
            result = self.bridge.execute_code(setup_code, timeout=30)
            
            if result.get('status') != 'success':
                print(f"❌ Failed to setup workspace: {result.get('error')}")
                return False
            
            # Upload each modified file
            for rel_path in modified_files:
                local_path = self.local_dir / rel_path
                
                try:
                    # Read file content
                    with open(local_path, 'rb') as f:
                        content = f.read()
                    
                    # Encode for transfer
                    encoded_content = base64.b64encode(content).decode('utf-8')
                    
                    # Create upload code
                    upload_code = f"""
import os
import base64

# Decode and write file
file_path = '{self.colab_mount}/{rel_path}'
file_dir = os.path.dirname(file_path)

# Create directory if needed
if file_dir:
    os.makedirs(file_dir, exist_ok=True)

# Write file
content = base64.b64decode('{encoded_content}')
with open(file_path, 'wb') as f:
    f.write(content)

print(f"📤 Uploaded: {rel_path} ({{len(content)}} bytes)")
"""
                    
                    # Execute upload
                    result = self.bridge.execute_code(upload_code, timeout=30)
                    
                    if result.get('status') == 'success':
                        print(f"✅ {rel_path}")
                    else:
                        print(f"❌ Failed to upload {rel_path}: {result.get('error')}")
                
                except Exception as e:
                    print(f"❌ Error uploading {rel_path}: {e}")
            
            self.last_sync = datetime.now()
            print(f"✅ Sync to Colab completed")
            return True
            
        except Exception as e:
            print(f"❌ Sync to Colab failed: {e}")
            return False
    
    def sync_from_colab(self) -> bool:
        """Download Colab changes to local directory"""
        try:
            print("📥 Syncing files from Colab...")
            
            # Get list of files in Colab workspace
            list_code = f"""
import os
import json

workspace_dir = '{self.colab_mount}'
files_info = []

if os.path.exists(workspace_dir):
    for root, dirs, files in os.walk(workspace_dir):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, workspace_dir)
            
            try:
                stat = os.stat(file_path)
                files_info.append({{
                    'rel_path': rel_path,
                    'size': stat.st_size,
                    'modified': stat.st_mtime
                }})
            except:
                pass

print(json.dumps(files_info))
"""
            
            result = self.bridge.execute_code(list_code, timeout=30)
            
            if result.get('status') != 'success':
                print(f"⚠️ Could not list Colab files: {result.get('error')}")
                return False
            
            # Parse file list
            try:
                colab_files = json.loads(result.get('output', '[]'))
            except:
                print("⚠️ No Colab file list received")
                return True
            
            if not colab_files:
                print("✅ No Colab files to sync")
                return True
            
            print(f"📋 Found {len(colab_files)} files in Colab workspace")
            
            # Download new/modified files
            downloaded = 0
            for file_info in colab_files:
                rel_path = file_info['rel_path']
                local_path = self.local_dir / rel_path
                
                # Check if we need to download
                should_download = False
                
                if not local_path.exists():
                    should_download = True  # New file
                elif local_path.stat().st_mtime < file_info['modified']:
                    should_download = True  # Modified in Colab
                
                if should_download:
                    # Download file
                    download_code = f"""
import base64
import os

file_path = '{self.colab_mount}/{rel_path}'
if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    
    encoded = base64.b64encode(content).decode('utf-8')
    print(encoded)
else:
    print("FILE_NOT_FOUND")
"""
                    
                    result = self.bridge.execute_code(download_code, timeout=30)
                    
                    if result.get('status') == 'success':
                        encoded_content = result.get('output', '').strip()
                        
                        if encoded_content and encoded_content != "FILE_NOT_FOUND":
                            try:
                                # Decode and save
                                content = base64.b64decode(encoded_content)
                                
                                # Create directory if needed
                                local_path.parent.mkdir(parents=True, exist_ok=True)
                                
                                with open(local_path, 'wb') as f:
                                    f.write(content)
                                
                                print(f"📥 Downloaded: {rel_path} ({len(content)} bytes)")
                                downloaded += 1
                                
                            except Exception as e:
                                print(f"❌ Error saving {rel_path}: {e}")
            
            if downloaded > 0:
                print(f"✅ Downloaded {downloaded} files from Colab")
            else:
                print("✅ No new files to download")
            
            return True
            
        except Exception as e:
            print(f"❌ Sync from Colab failed: {e}")
            return False
    
    def full_sync(self) -> bool:
        """Perform full bidirectional sync"""
        print("🔄 Performing full sync...")
        
        success = True
        success &= self.sync_to_colab()
        success &= self.sync_from_colab()
        
        if success:
            print("✅ Full sync completed")
        else:
            print("⚠️ Sync completed with errors")
        
        return success
    
    def watch_changes(self, callback=None):
        """Watch for local file changes (basic implementation)"""
        print(f"👀 Watching {self.local_dir} for changes...")
        
        last_scan = {}
        
        try:
            while True:
                current_scan = self.scan_local_files()
                
                # Check for changes
                changes = []
                for rel_path, file_info in current_scan.items():
                    if rel_path not in last_scan:
                        changes.append(f"Added: {rel_path}")
                    elif file_info["hash"] != last_scan[rel_path].get("hash"):
                        changes.append(f"Modified: {rel_path}")
                
                for rel_path in last_scan:
                    if rel_path not in current_scan:
                        changes.append(f"Deleted: {rel_path}")
                
                if changes:
                    print(f"📝 Detected changes:")
                    for change in changes:
                        print(f"  {change}")
                    
                    if callback:
                        callback(changes)
                    else:
                        # Auto-sync on changes
                        self.sync_to_colab()
                
                last_scan = current_scan
                time.sleep(2)  # Check every 2 seconds
                
        except KeyboardInterrupt:
            print("\n👋 Stopped watching for changes")
    
    def get_sync_status(self) -> Dict:
        """Get current sync status"""
        local_files = self.scan_local_files()
        
        return {
            "local_dir": str(self.local_dir),
            "colab_mount": self.colab_mount,
            "local_files": len(local_files),
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "sync_patterns": self.sync_patterns
        }


if __name__ == "__main__":
    # Demo usage
    print("📁 File Sync Manager Demo")
    print("=" * 40)
    
    # Create demo sync manager
    demo_dir = "/tmp/colab_sync_demo"
    sync_manager = FileSyncManager(demo_dir)
    
    # Create some demo files
    demo_file = Path(demo_dir) / "demo.py"
    demo_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(demo_file, 'w') as f:
        f.write("""
# Demo Python file
print("Hello from synced file!")

import datetime
print(f"Created: {datetime.datetime.now()}")
""")
    
    # Test sync
    print(f"\n📊 Sync status: {sync_manager.get_sync_status()}")
    
    if sync_manager.sync_to_colab():
        print("✅ Demo sync successful")
    else:
        print("❌ Demo sync failed")