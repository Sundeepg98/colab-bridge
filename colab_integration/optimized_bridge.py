#!/usr/bin/env python3
"""
Optimized Colab Bridge with realistic Drive API timings
Based on actual measurements:
- Poll: ~400ms per check
- Upload: ~2 seconds
- Read: ~1.6 seconds
"""

from .universal_bridge import UniversalColabBridge
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import queue

class OptimizedColabBridge(UniversalColabBridge):
    """Bridge optimized for actual Drive API performance"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result_cache = {}
        self.pending_results = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=3)
        
    def _wait_for_result(self, command_id, timeout):
        """Optimized polling based on real Drive API timings"""
        start_time = time.time()
        poll_count = 0
        
        # Since each poll takes ~400ms, adjust our strategy
        while time.time() - start_time < timeout:
            poll_count += 1
            elapsed = time.time() - start_time
            
            # Check both patterns
            files = []
            for pattern in [f"result_{command_id}.json", f"result_result_{command_id}.json"]:
                query = f"name='{pattern}' and '{self.folder_id}' in parents and trashed=false"
                results = self.drive_service.files().list(q=query, fields="files(id)").execute()
                
                files = results.get('files', [])
                if files:
                    break
                    
            if files:
                # Read result
                content = self.drive_service.files().get_media(fileId=files[0]['id']).execute()
                result = json.loads(content.decode('utf-8'))
                
                # Clean up result file
                self.drive_service.files().delete(fileId=files[0]['id']).execute()
                
                # Log timing
                print(f"✅ Got result in {elapsed:.1f}s after {poll_count} polls")
                return result
            
            # Smart polling intervals based on Drive API reality
            # Each poll takes ~400ms, so adjust sleep accordingly
            if elapsed < 3:
                # First 3 seconds: poll every 400ms (API limit)
                # No sleep needed - API call itself takes 400ms
                pass
            elif elapsed < 10:
                # 3-10 seconds: poll every 600ms
                time.sleep(0.2)  # 400ms API + 200ms sleep = 600ms
            elif elapsed < 30:
                # 10-30 seconds: poll every 1 second  
                time.sleep(0.6)  # 400ms API + 600ms sleep = 1s
            else:
                # After 30 seconds: poll every 2 seconds
                time.sleep(1.6)  # 400ms API + 1.6s sleep = 2s
        
        raise TimeoutError(f"Command {command_id} timed out after {timeout}s")


class SmartBatchBridge(UniversalColabBridge):
    """Bridge that batches operations for efficiency"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_queue = queue.Queue()
        self.result_futures = {}
        self.batch_thread = None
        self.stop_batching = False
        
    def initialize(self):
        """Initialize and start batch processor"""
        super().initialize()
        self.start_batch_processor()
        
    def start_batch_processor(self):
        """Process commands in batches to reduce API calls"""
        def batch_worker():
            while not self.stop_batching:
                # Collect commands for batch processing
                commands_batch = []
                
                # Wait up to 100ms to collect multiple commands
                try:
                    while len(commands_batch) < 5:  # Max 5 per batch
                        cmd = self.command_queue.get(timeout=0.1)
                        commands_batch.append(cmd)
                except queue.Empty:
                    pass
                
                if commands_batch:
                    # Process batch
                    for cmd in commands_batch:
                        try:
                            self._write_command(cmd['command'])
                            cmd['future'].set_result({'status': 'sent'})
                        except Exception as e:
                            cmd['future'].set_exception(e)
                
                # Check for results in batch
                try:
                    # Get ALL result files in one API call
                    results = self.drive_service.files().list(
                        q=f"name contains 'result_' and '{self.folder_id}' in parents",
                        fields='files(id, name)',
                        pageSize=20
                    ).execute()
                    
                    for file in results.get('files', []):
                        self._process_result_file(file)
                        
                except Exception:
                    pass
                    
                # Wait before next batch
                time.sleep(0.5)  # Balance API rate limits
                
        self.batch_thread = threading.Thread(target=batch_worker)
        self.batch_thread.daemon = True
        self.batch_thread.start()
        
    def _process_result_file(self, file):
        """Process a result file"""
        file_name = file['name']
        
        # Extract command ID
        for prefix in ['result_result_', 'result_']:
            if file_name.startswith(prefix):
                cmd_id = file_name.replace(prefix, '').replace('.json', '')
                break
        else:
            return
            
        # Check if we're waiting for this
        if cmd_id in self.result_futures:
            try:
                # Get result
                content = self.drive_service.files().get_media(fileId=file['id']).execute()
                result = json.loads(content.decode('utf-8'))
                
                # Deliver result
                self.result_futures[cmd_id].set_result(result)
                del self.result_futures[cmd_id]
                
                # Clean up
                self.drive_service.files().delete(fileId=file['id']).execute()
            except:
                pass


def create_optimized_bridge(tool_name='vscode'):
    """Factory to create the best bridge for current needs"""
    
    # For now, use the optimized polling bridge
    # Can switch to SmartBatchBridge for multiple commands
    return OptimizedColabBridge(tool_name=tool_name)


# Monkey patch the universal bridge with optimized polling
UniversalColabBridge._wait_for_result = OptimizedColabBridge._wait_for_result