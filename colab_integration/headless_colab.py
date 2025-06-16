#!/usr/bin/env python3
"""
True Headless Colab Automation
User never touches Colab - everything is automated!
"""

import os
import json
import time
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import threading
from datetime import datetime

class HeadlessColabManager:
    """Fully automated Colab management - no user interaction needed"""
    
    def __init__(self, service_account_path=None):
        self.service_account_path = service_account_path
        self.config_dir = Path.home() / '.colab-bridge'
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / 'headless_config.json'
        
        self.browser = None
        self.page = None
        self.notebook_url = None
        self.is_ready = False
        
        # Start headless automation in background
        self.automation_thread = None
        
    async def initialize(self):
        """Initialize headless Colab automation"""
        print("🚀 Starting headless Colab automation...")
        
        try:
            # Check if we have existing session
            if self._has_existing_session():
                print("✅ Found existing session, attempting to reconnect...")
                config = self._load_config()
                self.notebook_url = config.get('notebook_url')
                
                if await self._test_existing_session():
                    self.is_ready = True
                    print("✅ Existing session is working!")
                    return
                else:
                    print("⚠️  Existing session expired, creating new one...")
            
            # Create new automated session
            await self._create_new_session()
            
        except Exception as e:
            print(f"❌ Headless automation failed: {e}")
            raise
    
    async def _create_new_session(self):
        """Create new headless Colab session"""
        print("🎭 Starting headless browser...")
        
        playwright = await async_playwright().start()
        
        # Launch browser (headless=False for debugging, True for production)
        self.browser = await playwright.chromium.launch(
            headless=False,  # Set to True in production
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        # Create new page
        context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await context.new_page()
        
        print("📱 Navigating to Google Colab...")
        await self.page.goto('https://colab.research.google.com/')
        
        # Wait for page to load
        await self.page.wait_for_load_state('networkidle')
        
        print("📓 Creating new notebook...")
        # Click "New notebook"
        try:
            await self.page.click('text=New notebook', timeout=10000)
        except:
            # Alternative selector
            await self.page.click('[data-testid="new-notebook"]', timeout=10000)
        
        # Wait for notebook to open
        await self.page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)
        
        print("⚡ Setting up processor code...")
        await self._setup_processor_code()
        
        print("🔥 Starting notebook execution...")
        await self._start_execution()
        
        # Save session info
        self.notebook_url = self.page.url
        self._save_config({
            'notebook_url': self.notebook_url,
            'created_at': datetime.now().isoformat(),
            'status': 'running'
        })
        
        self.is_ready = True
        print(f"✅ Headless Colab ready! URL: {self.notebook_url}")
    
    async def _setup_processor_code(self):
        """Set up the processor code in Colab"""
        
        # Cell 1: Mount Drive
        mount_code = '''
from google.colab import drive
import os
import sys

if not os.path.exists('/content/drive'):
    drive.mount('/content/drive')
    print('✅ Drive mounted')
else:
    print('✅ Drive already mounted')

print(f'Python {sys.version}')
print('Headless processor ready!')
'''
        
        # Cell 2: Main processor loop
        processor_code = '''
import json
import time
import traceback
from datetime import datetime
from io import StringIO

# Find colab-bridge folder
base_paths = [
    '/content/drive/MyDrive/colab-bridge-auto',
    '/content/drive/My Drive/colab-bridge-auto'
]

base_path = None
for path in base_paths:
    if os.path.exists(path):
        base_path = path
        break

if not base_path:
    print('❌ Could not find colab-bridge-auto folder!')
    # Create it
    base_path = '/content/drive/MyDrive/colab-bridge-auto'
    os.makedirs(base_path, exist_ok=True)
    print(f'✅ Created folder: {base_path}')

print(f'📁 Monitoring: {base_path}')

# Create heartbeat
def update_heartbeat():
    heartbeat_path = os.path.join(base_path, 'heartbeat.json')
    with open(heartbeat_path, 'w') as f:
        json.dump({
            'timestamp': time.time(),
            'status': 'running',
            'processor': 'headless'
        }, f)

print('⏳ Starting command processor...')

while True:
    try:
        # Update heartbeat
        update_heartbeat()
        
        # Look for commands
        for file in os.listdir(base_path):
            if file.startswith('cmd_') and file.endswith('.json'):
                cmd_path = os.path.join(base_path, file)
                
                # Read command
                with open(cmd_path, 'r') as f:
                    cmd = json.load(f)
                
                print(f'\\n⚡ Executing: {cmd["id"]} at {datetime.now().strftime("%H:%M:%S")}')
                
                # Prepare result
                result = {
                    'id': cmd['id'],
                    'status': 'success',
                    'timestamp': time.time(),
                    'processor': 'headless'
                }
                
                # Capture output
                old_stdout = sys.stdout
                sys.stdout = output_buffer = StringIO()
                
                try:
                    # Execute code
                    exec(cmd['code'], {'__name__': '__main__'})
                    result['output'] = output_buffer.getvalue()
                    print(f'✅ Success: {cmd["id"]}')
                except Exception as e:
                    result['status'] = 'error'
                    result['error'] = str(e)
                    result['traceback'] = traceback.format_exc()
                    print(f'❌ Error in {cmd["id"]}: {e}')
                finally:
                    sys.stdout = old_stdout
                
                # Write result
                result_path = cmd_path.replace('cmd_', 'result_')
                with open(result_path, 'w') as f:
                    json.dump(result, f)
                
                # Clean up command
                os.remove(cmd_path)
        
        # Brief pause
        time.sleep(1)
        
    except KeyboardInterrupt:
        print('\\n👋 Processor stopped')
        break
    except Exception as e:
        print(f'❌ Processor error: {e}')
        time.sleep(5)
'''
        
        # Add first cell
        await self._add_code_cell(mount_code)
        await asyncio.sleep(2)
        
        # Add second cell
        await self._add_code_cell(processor_code)
        await asyncio.sleep(2)
    
    async def _add_code_cell(self, code):
        """Add a code cell with given content"""
        
        # Click in the code cell area
        try:
            # Try to find the code cell
            await self.page.click('.inputarea', timeout=5000)
        except:
            # Alternative approach
            await self.page.click('[data-testid="code-cell"]', timeout=5000)
        
        # Clear existing content
        await self.page.keyboard.press('Control+a')
        
        # Type the code
        await self.page.keyboard.type(code)
        
        # Add new cell below
        await self.page.keyboard.press('Escape')  # Exit edit mode
        await self.page.keyboard.press('b')  # Add cell below
        await asyncio.sleep(1)
    
    async def _start_execution(self):
        """Start executing all cells"""
        print("🔥 Executing all cells...")
        
        # Run all cells
        await self.page.keyboard.press('Control+F9')
        
        # Wait for execution to start
        await asyncio.sleep(5)
        
        # Check for runtime connection
        try:
            # Look for "Connect" button and click if present
            connect_button = await self.page.query_selector('text=Connect')
            if connect_button:
                print("🔌 Connecting to runtime...")
                await connect_button.click()
                await asyncio.sleep(10)
        except:
            pass
        
        # Wait for execution to complete
        print("⏳ Waiting for processor to start...")
        await asyncio.sleep(15)
        
        print("✅ Processor should be running!")
    
    async def _test_existing_session(self):
        """Test if existing session is still working"""
        if not self.notebook_url:
            return False
        
        try:
            # Try to navigate to existing notebook
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(self.notebook_url, timeout=10000)
            await page.wait_for_load_state('networkidle')
            
            # Check if it's still a valid Colab notebook
            title = await page.title()
            is_valid = 'Colaboratory' in title or 'Colab' in title
            
            await browser.close()
            return is_valid
        except:
            return False
    
    def _has_existing_session(self):
        """Check if we have existing session config"""
        return self.config_file.exists()
    
    def _load_config(self):
        """Load existing configuration"""
        with open(self.config_file) as f:
            return json.load(f)
    
    def _save_config(self, config):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def start_background_automation(self):
        """Start automation in background thread"""
        def run_automation():
            asyncio.run(self.initialize())
        
        self.automation_thread = threading.Thread(target=run_automation, daemon=True)
        self.automation_thread.start()
        
        # Wait for initialization
        timeout = 60  # 1 minute timeout
        start_time = time.time()
        
        while not self.is_ready and (time.time() - start_time) < timeout:
            time.sleep(1)
        
        if not self.is_ready:
            raise Exception("Headless automation timed out")
    
    async def cleanup(self):
        """Clean up browser resources"""
        if self.browser:
            await self.browser.close()

class TrulyZeroConfigBridge:
    """The ultimate zero-config experience"""
    
    def __init__(self, service_account_path=None):
        self.headless_manager = HeadlessColabManager(service_account_path)
        self.setup_complete = False
        
        # Auto-setup with real zero config
        self._ensure_setup()
    
    def _ensure_setup(self):
        """Ensure everything is set up automatically"""
        if self.setup_complete:
            return
        
        print("🚀 Initializing truly zero-config Colab Bridge...")
        print("   This may take 30-60 seconds on first run...")
        
        # Start headless automation
        self.headless_manager.start_background_automation()
        
        self.setup_complete = True
        print("✅ Zero-config setup complete! Ready to execute code.")
    
    def execute(self, code, timeout=30):
        """Execute code with true zero configuration"""
        self._ensure_setup()
        
        # Use the universal bridge with headless setup
        from .auto_setup import auto_setup
        from .universal_bridge import UniversalColabBridge
        
        # The headless automation handles the notebook
        # We just use the file-based communication
        config = auto_setup()
        
        bridge = UniversalColabBridge("headless")
        bridge.folder_id = config['folder_id']
        bridge.initialize()
        
        return bridge.execute_code(code, timeout)

# For VS Code extension
def truly_zero_config_execute(code, service_account_path=None):
    """
    The ultimate one-liner for VS Code extension.
    Everything happens automatically in the background.
    """
    bridge = TrulyZeroConfigBridge(service_account_path)
    return bridge.execute(code)

if __name__ == "__main__":
    # Demo
    print("🧪 Testing Truly Zero-Config Bridge...")
    
    # This should work with ZERO manual steps
    bridge = TrulyZeroConfigBridge()
    
    print("\n📤 Executing test code...")
    result = bridge.execute('''
import sys
print(f"Python: {sys.version}")
print("🎉 Truly zero-config execution successful!")
print("User never touched Colab!")
''')
    
    print(f"\n📥 Result: {result}")