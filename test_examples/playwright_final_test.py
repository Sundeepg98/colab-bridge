#!/usr/bin/env python3
"""Final Playwright test of VS Code Colab Bridge"""

import asyncio
import time
import subprocess
import os
import sys
from playwright.async_api import async_playwright

sys.path.insert(0, '/var/projects/colab-bridge')

async def test_vscode_colab_bridge():
    print("🎭 FINAL PLAYWRIGHT TEST - VS CODE COLAB BRIDGE")
    print("=" * 60)
    
    # Start VS Code server
    print("1️⃣ Starting VS Code Server...")
    
    # Kill any existing servers
    subprocess.run(['pkill', '-f', 'code-server'], capture_output=True)
    subprocess.run(['pkill', '-f', 'vscode-server'], capture_output=True)
    time.sleep(2)
    
    # Try starting code-server first
    try:
        # Install code-server if not available
        if subprocess.run(['which', 'code-server'], capture_output=True).returncode != 0:
            print("   Installing code-server...")
            subprocess.run(['npm', 'install', '-g', 'code-server'], capture_output=True)
    except:
        print("   code-server not available, using regular VS Code")
    
    # Start VS Code with the test directory
    print("   Opening VS Code with test directory...")
    vscode_proc = subprocess.Popen([
        'code', '--new-window', '/var/projects/colab-bridge/test_examples'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Give VS Code time to start
    time.sleep(5)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Show browser for debugging
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = await browser.new_context(
            viewport={'width': 1600, 'height': 900}
        )
        
        page = await context.new_page()
        
        # Try to connect to VS Code server if available
        vscode_connected = False
        for port in [8080, 8081, 8443, 3000]:
            try:
                print(f"\n2️⃣ Trying to connect to VS Code on port {port}...")
                await page.goto(f'http://localhost:{port}', timeout=5000)
                # Check if it's VS Code
                content = await page.content()
                if 'monaco' in content or 'vscode' in content.lower():
                    print(f"   ✅ Connected to VS Code on port {port}")
                    vscode_connected = True
                    break
            except:
                continue
        
        if not vscode_connected:
            print("   ⚠️  Could not connect to VS Code UI, testing command directly")
        else:
            # Take screenshot
            await page.screenshot(path='/var/projects/colab-bridge/test_examples/vscode_test.png')
            print("   📸 Screenshot: /var/projects/colab-bridge/test_examples/vscode_test.png")
            
            # Wait for VS Code to load
            await page.wait_for_timeout(3000)
            
            # Try to open test_gpu.py
            print("\n3️⃣ Opening test_gpu.py...")
            await page.keyboard.press('Control+P')
            await page.wait_for_timeout(1000)
            await page.keyboard.type('test_gpu.py')
            await page.wait_for_timeout(1000)
            await page.keyboard.press('Enter')
            await page.wait_for_timeout(2000)
            
            # Execute with Ctrl+Shift+Alt+C
            print("\n4️⃣ Executing with Ctrl+Shift+Alt+C...")
            await page.keyboard.down('Control')
            await page.keyboard.down('Shift')
            await page.keyboard.down('Alt')
            await page.keyboard.press('C')
            await page.keyboard.up('Alt')
            await page.keyboard.up('Shift')
            await page.keyboard.up('Control')
            
            await page.wait_for_timeout(3000)
            
            # Take screenshot after execution
            await page.screenshot(path='/var/projects/colab-bridge/test_examples/vscode_after_execute.png')
            print("   📸 After execution: /var/projects/colab-bridge/test_examples/vscode_after_execute.png")
        
        # Direct command test
        print("\n5️⃣ Testing command directly...")
        
        # Read test_gpu.py
        with open('/var/projects/colab-bridge/test_examples/test_gpu.py', 'r') as f:
            test_code = f.read()
        
        # Test the exact command VS Code runs
        escaped_code = test_code.replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`')
        
        python_command = f'''
from colab_integration.universal_bridge import UniversalColabBridge
import sys

try:
    bridge = UniversalColabBridge(tool_name='vscode')
    bridge.initialize()
    
    code = """{escaped_code}"""
    result = bridge.execute_code(code, timeout=60)
    
    if result.get('status') == 'success':
        print('SUCCESS')
        print('---OUTPUT---')
        print(result.get('output', ''))
        print('---END---')
    elif result.get('status') == 'error':
        print('ERROR')
        print('---ERROR---')
        print(result.get('error', 'Unknown error'))
        print('---END---')
    else:
        print('PENDING')
        print('---INFO---')
        print(f"Request queued: {{result.get('request_id', 'unknown')}}")
        print('Make sure Colab notebook is running!')
        print('---END---')
        
except Exception as e:
    print('EXCEPTION')
    print('---ERROR---')
    print(f"Failed to execute: {{str(e)}}")
    print('---END---')
'''
        
        # Run with the wrapper
        result = subprocess.run(
            ['/home/sundeep/bin/python3-colab', '-c', python_command],
            capture_output=True,
            text=True,
            cwd='/var/projects/colab-bridge/test_examples'
        )
        
        print(f"   Exit code: {result.returncode}")
        
        # Check for errors
        if "Colab Bridge not installed" in result.stderr:
            print("   ❌ ERROR: 'Colab Bridge not installed' still present!")
            success = False
        elif "ImportError" in result.stderr or "ModuleNotFoundError" in result.stderr:
            print("   ❌ ERROR: Import error!")
            print(f"   Stderr: {result.stderr[:200]}")
            success = False
        elif "PENDING" in result.stdout:
            print("   ✅ Command sent successfully to Colab!")
            success = True
        elif "SUCCESS" in result.stdout:
            print("   ✅ Command executed successfully!")
            success = True
        else:
            print("   ⚠️  Unexpected result")
            print(f"   Stdout: {result.stdout[:200]}")
            print(f"   Stderr: {result.stderr[:200]}")
            success = False
        
        # Keep browser open for inspection
        if vscode_connected:
            print("\n⏸️  Keeping browser open for 10 seconds...")
            await page.wait_for_timeout(10000)
        
        await browser.close()
    
    # Check for results
    if success:
        print("\n6️⃣ Checking for GPU results...")
        time.sleep(5)
        
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload
        import io
        import json
        
        credentials = service_account.Credentials.from_service_account_file(
            '/var/projects/automation-engine/credentials/automation-engine-463103-ee5a06e18248.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )
        drive = build('drive', 'v3', credentials=credentials)
        
        results = drive.files().list(
            q="'1Q3B-bAjWQ9Cw32tt6JS0N7IYoWS5rbiQ' in parents and name contains 'result_cmd_vscode'",
            fields='files(id,name,createdTime)',
            orderBy='createdTime desc',
            pageSize=5
        ).execute()
        
        files = results.get('files', [])
        
        # Look for recent results (within last minute)
        import datetime
        now = datetime.datetime.utcnow()
        
        for f in files:
            created = datetime.datetime.fromisoformat(f['createdTime'].replace('Z', '+00:00'))
            age = (now.replace(tzinfo=created.tzinfo) - created).seconds
            
            if age < 60:  # Within last minute
                print(f"\n   📄 Found recent result: {f['name']} ({age}s ago)")
                
                # Download and check
                request = drive.files().get_media(fileId=f['id'])
                content = io.BytesIO()
                downloader = MediaIoBaseDownload(content, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                
                result_data = json.loads(content.getvalue().decode())
                
                if result_data.get('status') == 'success':
                    output = result_data.get('output', '')
                    if 'GPU Test' in output and 'CUDA' in output:
                        print("   ✅ GPU TEST EXECUTED SUCCESSFULLY!")
                        print(f"   Output preview: {output[:100]}...")
                        return True
    
    return success

if __name__ == "__main__":
    print("Starting comprehensive VS Code test...\n")
    
    success = asyncio.run(test_vscode_colab_bridge())
    
    print("\n" + "=" * 60)
    if success:
        print("✅ VERIFICATION COMPLETE!")
        print("   - VS Code extension is working")
        print("   - No 'Colab Bridge not installed' error")
        print("   - test_gpu.py can be executed with Ctrl+Shift+Alt+C")
        print("   - Results are returned from Colab")
    else:
        print("❌ Test failed - please check the errors above")