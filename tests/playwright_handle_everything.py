#!/usr/bin/env python3
"""
Playwright script to handle EVERYTHING - add secret, run notebook, verify success
"""

import asyncio
import json
import base64
import time
import os
from pathlib import Path

def install_playwright():
    """Ensure Playwright is installed"""
    try:
        import playwright
    except ImportError:
        print("📦 Installing Playwright...")
        import subprocess
        subprocess.run(['pip', 'install', 'playwright'], check=True)
        subprocess.run(['python', '-m', 'playwright', 'install', 'chromium'], check=True)

async def handle_sun_colab_until_success():
    """Handle everything until sun_colab secret works"""
    
    print("🎯 HANDLING SUN_COLAB UNTIL SUCCESS")
    print("=" * 60)
    print("I will:")
    print("1. Open Colab")
    print("2. Add/update sun_colab secret")
    print("3. Run the notebook")
    print("4. Test until it works")
    print("5. Not stop until successful!")
    print("=" * 60)
    
    from playwright.async_api import async_playwright
    
    # Get base64 service account
    sa_path = '/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
    with open(sa_path, 'rb') as f:
        sa_base64 = base64.b64encode(f.read()).decode()
    
    print(f"\n✅ Service account ready: {len(sa_base64)} chars")
    
    async with async_playwright() as p:
        print("\n🌐 Launching browser (headless mode)...")
        browser = await p.chromium.launch(
            headless=True,  # Headless for Cloud Shell
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        success = False
        attempt = 0
        
        while not success and attempt < 5:
            attempt += 1
            print(f"\n🔄 Attempt {attempt}/5")
            
            try:
                # Step 1: Load the notebook
                notebook_url = "https://colab.research.google.com/drive/1D5ah8CcpiFZ7LhaA1aEWmyczZRf0DQIq"
                print(f"📄 Loading notebook...")
                
                await page.goto(notebook_url, wait_until='networkidle', timeout=60000)
                await page.wait_for_timeout(5000)
                
                # Handle any popups
                await handle_popups(page)
                
                # Step 2: Open secrets panel
                print("🔐 Opening secrets panel...")
                secrets_opened = await open_secrets_panel(page)
                
                if not secrets_opened:
                    print("❌ Could not open secrets panel")
                    continue
                
                # Step 3: Add or update sun_colab secret
                print("🔑 Handling sun_colab secret...")
                secret_added = await handle_sun_colab_secret(page, sa_base64)
                
                if not secret_added:
                    print("❌ Could not add secret")
                    continue
                
                # Step 4: Close secrets panel
                try:
                    # Click somewhere else to close panel
                    await page.click('body', position={'x': 100, 'y': 100})
                    await page.wait_for_timeout(1000)
                except:
                    pass
                
                # Step 5: Run all cells
                print("▶️ Running all cells...")
                run_success = await run_all_cells(page)
                
                if not run_success:
                    print("❌ Could not run cells")
                    continue
                
                # Step 6: Wait for execution
                print("⏳ Waiting for notebook to initialize...")
                await page.wait_for_timeout(15000)  # 15 seconds
                
                # Step 7: Check if it's working
                print("🔍 Checking if notebook is working...")
                working = await check_notebook_working(page)
                
                if working:
                    print("✅ Notebook is working with secrets!")
                    
                    # Step 8: Test from Cloud Shell
                    print("\n🧪 Testing from Cloud Shell...")
                    test_success = await test_automation()
                    
                    if test_success:
                        success = True
                        print("\n🎉 SUCCESS! SUN_COLAB SECRET IS WORKING!")
                        print("✅ Automation is fully functional!")
                    else:
                        print("⚠️ Notebook running but automation not responding yet")
                        print("⏳ Waiting 30 seconds for processor to fully start...")
                        await page.wait_for_timeout(30000)
                        
                        # Try test again
                        test_success = await test_automation()
                        if test_success:
                            success = True
                            print("\n🎉 SUCCESS AFTER WAIT!")
                else:
                    print("❌ Notebook not working yet")
                    
                if not success:
                    print(f"⏳ Attempt {attempt} failed, trying again...")
                    await page.wait_for_timeout(5000)
                    
            except Exception as e:
                print(f"❌ Error in attempt {attempt}: {e}")
                import traceback
                traceback.print_exc()
        
        # Keep browser open to show success
        if success:
            print("\n" + "=" * 60)
            print("🎉 COMPLETE SUCCESS!")
            print("=" * 60)
            print("✅ sun_colab secret is configured correctly")
            print("✅ Notebook is running with secrets")
            print("✅ Automation is working")
            print("✅ You can now use the system!")
            print("\n🌐 Browser will stay open for 30 seconds...")
            await page.wait_for_timeout(30000)
        else:
            print("\n❌ Could not get it working after 5 attempts")
            print("Please check manually")
        
        await browser.close()

async def handle_popups(page):
    """Handle any Colab popups"""
    try:
        # Dismiss button
        dismiss = await page.query_selector('button:has-text("Dismiss")')
        if dismiss:
            await dismiss.click()
            print("   ✅ Dismissed popup")
    except:
        pass
    
    try:
        # Close button
        close = await page.query_selector('[aria-label="Close"]')
        if close:
            await close.click()
            print("   ✅ Closed popup")
    except:
        pass

async def open_secrets_panel(page):
    """Open the secrets panel"""
    try:
        # Method 1: Look for key icon
        key_icon = await page.query_selector('[aria-label*="Secret" i]')
        if not key_icon:
            key_icon = await page.query_selector('[data-tooltip*="Secret" i]')
        if not key_icon:
            # Try text
            key_icon = await page.query_selector('text=🔑')
        
        if key_icon:
            await key_icon.click()
            await page.wait_for_timeout(2000)
            print("   ✅ Clicked secrets icon")
            return True
            
        # Method 2: Use keyboard shortcut
        await page.keyboard.press('Control+Alt+S')
        await page.wait_for_timeout(2000)
        
        # Check if panel opened
        panel = await page.query_selector('text=Secrets')
        if panel:
            print("   ✅ Opened secrets with shortcut")
            return True
            
    except Exception as e:
        print(f"   ❌ Error opening secrets: {e}")
    
    return False

async def handle_sun_colab_secret(page, sa_base64):
    """Add or update the sun_colab secret"""
    try:
        # Check if secret exists
        existing = await page.query_selector('text=sun_colab')
        
        if existing:
            print("   🔍 Secret sun_colab exists, updating...")
            
            # Click on it to edit
            await existing.click()
            await page.wait_for_timeout(1000)
            
            # Look for edit button
            edit_btn = await page.query_selector('button[aria-label*="Edit" i]')
            if edit_btn:
                await edit_btn.click()
                await page.wait_for_timeout(1000)
        else:
            print("   ➕ Adding new secret sun_colab...")
            
            # Click add button
            add_btn = await page.query_selector('button:has-text("Add a secret")')
            if not add_btn:
                add_btn = await page.query_selector('button:has-text("Add")')
            if not add_btn:
                add_btn = await page.query_selector('button[aria-label*="Add" i]')
            
            if add_btn:
                await add_btn.click()
                await page.wait_for_timeout(1000)
            else:
                print("   ❌ Could not find add button")
                return False
        
        # Fill in the secret
        # Name field
        name_input = await page.query_selector('input[placeholder*="name" i]')
        if name_input:
            await name_input.fill('')  # Clear first
            await name_input.fill('sun_colab')
            print("   ✅ Entered secret name")
        
        # Value field - try different selectors
        value_input = await page.query_selector('textarea[placeholder*="value" i]')
        if not value_input:
            value_input = await page.query_selector('textarea[aria-label*="value" i]')
        if not value_input:
            value_input = await page.query_selector('textarea')
        
        if value_input:
            await value_input.fill('')  # Clear first
            await value_input.fill(sa_base64)
            print("   ✅ Entered secret value (base64)")
        else:
            print("   ❌ Could not find value input")
            return False
        
        # Enable notebook access
        try:
            checkbox = await page.query_selector('input[type="checkbox"]')
            if checkbox:
                is_checked = await checkbox.is_checked()
                if not is_checked:
                    await checkbox.click()
                    print("   ✅ Enabled notebook access")
        except:
            pass
        
        # Save the secret
        save_btn = await page.query_selector('button:has-text("Save")')
        if not save_btn:
            save_btn = await page.query_selector('button[aria-label*="Save" i]')
        
        if save_btn:
            await save_btn.click()
            await page.wait_for_timeout(2000)
            print("   ✅ Saved secret!")
            return True
        else:
            print("   ❌ Could not find save button")
            return False
            
    except Exception as e:
        print(f"   ❌ Error handling secret: {e}")
        return False

async def run_all_cells(page):
    """Run all cells in the notebook"""
    try:
        # Method 1: Keyboard shortcut
        await page.keyboard.press('Control+F9')
        await page.wait_for_timeout(2000)
        print("   ✅ Triggered run all with Ctrl+F9")
        return True
    except:
        try:
            # Method 2: Menu
            await page.click('text=Runtime')
            await page.wait_for_timeout(500)
            await page.click('text=Run all')
            print("   ✅ Triggered run all via menu")
            return True
        except:
            return False

async def check_notebook_working(page):
    """Check if notebook is working with secrets"""
    try:
        # Look for success indicators in page
        content = await page.content()
        
        indicators = [
            "Service account loaded",
            "Using embedded service account",
            "Drive authentication successful",
            "PROCESSOR ACTIVE",
            ""[SERVICE_ACCOUNT_EMAIL]""
        ]
        
        found = []
        for indicator in indicators:
            if indicator in content:
                found.append(indicator)
                print(f"   ✅ Found: {indicator}")
        
        return len(found) > 0
        
    except Exception as e:
        print(f"   ❌ Error checking notebook: {e}")
        return False

async def test_automation():
    """Test if automation is working"""
    try:
        import subprocess
        
        test_script = '''
import os
os.environ["SERVICE_ACCOUNT_PATH"] = "/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json"
os.environ["GOOGLE_DRIVE_FOLDER_ID"] = "1ruRdOXUJi16sHgDtpgxqtR7A7g7J8PpA"

from colab_integration.bridge import ClaudeColabBridge
bridge = ClaudeColabBridge()
bridge.initialize()

test_code = """
print("🎉 PLAYWRIGHT AUTOMATION SUCCESS!")
print("✅ sun_colab secret is working!")
print("✅ Colab processor is running!")
print("🔐 Using secure secrets!")
"""

result = bridge.execute_code(test_code, timeout=30)

if result and result.get("status") == "success":
    print("SUCCESS")
    print(result.get("output", ""))
else:
    print("FAILED")
'''
        
        result = subprocess.run(
            ['python', '-c', test_script],
            capture_output=True,
            text=True,
            timeout=40
        )
        
        if "SUCCESS" in result.stdout:
            print("   ✅ Automation test passed!")
            print(f"   Output: {result.stdout}")
            return True
        else:
            print("   ❌ Automation test failed")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False

async def main():
    """Main function"""
    install_playwright()
    await handle_sun_colab_until_success()

if __name__ == "__main__":
    print("🚀 STARTING COMPLETE AUTOMATION")
    print("I will handle sun_colab until it's successful!")
    asyncio.run(main())