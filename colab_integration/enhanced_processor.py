#!/usr/bin/env python3
"""
Enhanced Colab Processor with Plot Support
Captures both text output and matplotlib/other visualizations
"""

import os
import sys
import json
import time
import traceback
import io
import base64
from contextlib import redirect_stdout, redirect_stderr
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Import matplotlib and configure for non-interactive backend
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

class EnhancedColabProcessor:
    def __init__(self):
        self.folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
        self.service = self._init_drive_service()
        self.processed_commands = set()
        
    def _init_drive_service(self):
        """Initialize Google Drive service"""
        creds_path = os.environ.get('SERVICE_ACCOUNT_PATH')
        if not creds_path:
            raise ValueError("SERVICE_ACCOUNT_PATH environment variable not set")
            
        credentials = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        return build('drive', 'v3', credentials=credentials)
    
    def execute_code_with_capture(self, code):
        """Execute code and capture text output + plots"""
        # Capture stdout and stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        # Track matplotlib figures before execution
        initial_figs = set(plt.get_fignums()) if 'matplotlib.pyplot' in sys.modules else set()
        
        # Also track if PIL/Pillow images are displayed
        displayed_images = []
        
        # Monkey-patch IPython display if in Colab
        original_display = None
        try:
            from IPython import display
            original_display = display.display
            
            def capture_display(*args, **kwargs):
                """Capture IPython display calls"""
                for obj in args:
                    # Handle PIL images
                    if hasattr(obj, '_repr_png_'):
                        png_data = obj._repr_png_()
                        if png_data:
                            displayed_images.append({
                                'type': 'image/png',
                                'data': base64.b64encode(png_data).decode('utf-8')
                            })
                    # Handle matplotlib figures
                    elif hasattr(obj, 'figure'):
                        fig = obj.figure
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
                        buf.seek(0)
                        displayed_images.append({
                            'type': 'image/png',
                            'data': base64.b64encode(buf.read()).decode('utf-8')
                        })
                # Still call original display
                return original_display(*args, **kwargs)
            
            display.display = capture_display
        except ImportError:
            pass  # Not in IPython/Colab environment
        
        # Execute the code
        error = None
        exec_globals = {'__name__': '__main__'}
        
        try:
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exec(code, exec_globals)
        except Exception as e:
            error = {
                'type': type(e).__name__,
                'message': str(e),
                'traceback': traceback.format_exc()
            }
        finally:
            # Restore display if we patched it
            if original_display:
                try:
                    from IPython import display
                    display.display = original_display
                except:
                    pass
        
        # Capture any matplotlib plots created
        plots = []
        if 'matplotlib.pyplot' in sys.modules:
            final_figs = set(plt.get_fignums())
            new_figs = final_figs - initial_figs
            
            for fig_num in new_figs:
                try:
                    fig = plt.figure(fig_num)
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
                    buf.seek(0)
                    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                    plots.append({
                        'type': 'image/png',
                        'data': img_base64
                    })
                    plt.close(fig)
                except Exception as e:
                    print(f"Error capturing figure {fig_num}: {e}")
        
        # Combine all visualizations
        all_visuals = displayed_images + plots
        
        # Build result
        if error:
            return {
                'status': 'error',
                'error': f"{error['type']}: {error['message']}",
                'traceback': error['traceback'],
                'output': stdout_buffer.getvalue(),
                'stderr': stderr_buffer.getvalue()
            }
        else:
            result = {
                'status': 'success',
                'output': stdout_buffer.getvalue(),
                'stderr': stderr_buffer.getvalue()
            }
            
            # Add visualizations if any
            if all_visuals:
                result['visualizations'] = all_visuals
                result['output_type'] = 'rich'  # Indicates output has visuals
            else:
                result['output_type'] = 'text'
                
            return result
    
    def process_command(self, command_file):
        """Process a single command file"""
        # Read command
        file_id = command_file['id']
        content = self.service.files().get_media(fileId=file_id).execute()
        command = json.loads(content.decode('utf-8'))
        
        command_id = command['id']
        if command_id in self.processed_commands:
            return  # Already processed
            
        print(f"Processing command: {command_id}")
        
        # Delete command file immediately
        try:
            self.service.files().delete(fileId=file_id).execute()
        except:
            pass
            
        # Execute code with enhanced capture
        start_time = time.time()
        result = self.execute_code_with_capture(command.get('code', ''))
        execution_time = time.time() - start_time
        
        # Add metadata
        result['command_id'] = command_id
        result['execution_time'] = execution_time
        result['timestamp'] = time.time()
        
        # Write result
        result_filename = f"result_{command_id}.json"
        self._write_result(result_filename, result)
        
        self.processed_commands.add(command_id)
        
        # Print summary
        print(f"✅ Completed {command_id} in {execution_time:.2f}s")
        if result.get('visualizations'):
            print(f"   Captured {len(result['visualizations'])} visualizations")
    
    def _write_result(self, filename, data):
        """Write result to Drive"""
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f, indent=2)
            temp_path = f.name
        
        try:
            media = MediaFileUpload(temp_path, mimetype='application/json')
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id]
            }
            
            self.service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
        finally:
            os.unlink(temp_path)
    
    def run(self, poll_interval=1):
        """Main processing loop"""
        print("🚀 Enhanced Colab Processor Started")
        print(f"📁 Monitoring folder: {self.folder_id}")
        print("🎨 Plot capture enabled")
        print("-" * 50)
        
        while True:
            try:
                # Look for command files
                query = f"'{self.folder_id}' in parents and name contains 'command_' and trashed=false"
                results = self.service.files().list(
                    q=query,
                    fields="files(id, name)"
                ).execute()
                
                files = results.get('files', [])
                
                for file in files:
                    try:
                        self.process_command(file)
                    except Exception as e:
                        print(f"Error processing {file['name']}: {e}")
                        traceback.print_exc()
                
                time.sleep(poll_interval)
                
            except KeyboardInterrupt:
                print("\n👋 Processor stopped")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(5)

# For Colab notebook
def start_processor():
    """Start the processor (for Colab notebook)"""
    processor = EnhancedColabProcessor()
    processor.run()

if __name__ == '__main__':
    # Can be run directly
    processor = EnhancedColabProcessor()
    processor.run()