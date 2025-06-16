#!/usr/bin/env python3
"""
Smart Colab Bridge with Fallback Options
1. Try headless automation first
2. Fallback to manual setup if needed
3. User always has control
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional

class SmartColabBridge:
    """
    Intelligent bridge that tries automation first, falls back to manual
    """
    
    def __init__(self, service_account_path=None, automation_mode="auto"):
        """
        Args:
            service_account_path: Path to service account JSON
            automation_mode: "auto", "headless", "manual", "prompt"
        """
        self.service_account_path = service_account_path
        self.automation_mode = automation_mode
        self.bridge = None
        self.setup_method = None
        
    def initialize(self):
        """Smart initialization with fallbacks"""
        print("🧠 Smart Colab Bridge - Choosing best setup method...")
        
        if self.automation_mode == "auto":
            return self._auto_choose_method()
        elif self.automation_mode == "headless":
            return self._try_headless_only()
        elif self.automation_mode == "manual":
            return self._manual_setup_only()
        elif self.automation_mode == "prompt":
            return self._prompt_user_choice()
    
    def _auto_choose_method(self):
        """Automatically choose the best method"""
        print("🤖 Auto-selecting setup method...")
        
        # 1. Check if headless automation is possible
        if self._can_use_headless():
            print("✅ Headless automation available - trying automated setup...")
            if self._try_headless():
                return True
            else:
                print("⚠️  Headless automation failed - falling back to manual...")
                return self._fallback_to_manual()
        else:
            print("ℹ️  Headless automation not available - using manual setup...")
            return self._fallback_to_manual()
    
    def _can_use_headless(self):
        """Check if headless automation is possible"""
        try:
            # Check if Playwright is installed
            import playwright
            
            # Check if we're in an environment that supports browsers
            if os.environ.get('DISPLAY') or sys.platform == 'win32':
                return True
            
            # Check if we're in a container/cloud environment
            if os.path.exists('/.dockerenv') or os.environ.get('COLAB_GPU'):
                print("   🐳 Container environment detected - headless may not work")
                return False
            
            return True
            
        except ImportError:
            print("   📦 Playwright not installed - install with: pip install playwright")
            return False
    
    def _try_headless(self):
        """Try headless automation"""
        try:
            from .headless_colab import TrulyZeroConfigBridge
            
            print("   🎭 Starting headless automation...")
            self.bridge = TrulyZeroConfigBridge(self.service_account_path)
            self.setup_method = "headless"
            print("   ✅ Headless automation successful!")
            return True
            
        except Exception as e:
            print(f"   ❌ Headless automation failed: {e}")
            return False
    
    def _try_headless_only(self):
        """Try headless automation only (no fallback)"""
        if not self._can_use_headless():
            raise Exception("Headless automation not available in this environment")
        
        if self._try_headless():
            return True
        else:
            raise Exception("Headless automation failed and no fallback requested")
    
    def _fallback_to_manual(self):
        """Fallback to manual setup"""
        print("📋 Using manual setup method...")
        
        try:
            from .zero_config_bridge import ZeroConfigBridge
            
            self.bridge = ZeroConfigBridge(self.service_account_path)
            self.setup_method = "manual"
            
            # Show user what they need to do
            self._show_manual_instructions()
            
            return True
            
        except Exception as e:
            print(f"❌ Manual setup also failed: {e}")
            raise
    
    def _manual_setup_only(self):
        """Manual setup only"""
        print("📋 Manual setup requested...")
        return self._fallback_to_manual()
    
    def _prompt_user_choice(self):
        """Ask user which method they prefer"""
        print("\n🤔 How would you like to set up Colab Bridge?")
        print("1. 🎭 Automatic (headless browser automation)")
        print("2. 📋 Manual (you open the notebook yourself)")
        print("3. 🤖 Auto-choose (try automatic, fallback to manual)")
        
        while True:
            choice = input("\nEnter choice (1/2/3): ").strip()
            
            if choice == "1":
                return self._try_headless_only()
            elif choice == "2":
                return self._manual_setup_only()
            elif choice == "3":
                return self._auto_choose_method()
            else:
                print("Please enter 1, 2, or 3")
    
    def _show_manual_instructions(self):
        """Show manual setup instructions"""
        if hasattr(self.bridge, 'get_notebook_url'):
            notebook_url = self.bridge.get_notebook_url()
            
            print("\n" + "="*60)
            print("📋 MANUAL SETUP REQUIRED")
            print("="*60)
            print("Please complete these steps:")
            print(f"1. Open this URL: {notebook_url}")
            print("2. Click 'Run all' (or press Ctrl+F9)")
            print("3. Wait for all cells to execute")
            print("4. Keep the notebook tab open")
            print("5. Come back here and press Enter to continue")
            print("="*60)
            
            input("Press Enter when you've completed the steps above...")
            print("✅ Manual setup completed!")
    
    def execute(self, code, timeout=30):
        """Execute code using the configured bridge"""
        if not self.bridge:
            self.initialize()
        
        if self.setup_method == "headless":
            print("⚡ Executing via headless automation...")
        else:
            print("📤 Executing via manual setup...")
        
        return self.bridge.execute(code, timeout)
    
    def get_setup_info(self):
        """Get information about the current setup"""
        return {
            'method': self.setup_method,
            'automation_available': self._can_use_headless(),
            'bridge_type': type(self.bridge).__name__ if self.bridge else None
        }

class FlexibleVSCodeBridge:
    """VS Code bridge with flexible setup options"""
    
    def __init__(self, automation_preference="auto"):
        """
        Args:
            automation_preference: "auto", "headless", "manual", "prompt"
        """
        self.bridge = SmartColabBridge(automation_mode=automation_preference)
        self.initialized = False
    
    def execute_selection(self, code):
        """Execute selected code with smart fallbacks"""
        if not self.initialized:
            print("🚀 Initializing Colab Bridge...")
            self.bridge.initialize()
            self.initialized = True
        
        result = self.bridge.execute(code)
        
        if result.get('status') == 'success':
            return result.get('output', '')
        elif result.get('status') == 'error':
            return f"❌ Error: {result.get('error', 'Unknown error')}"
        else:
            return "⏳ Processing... (check if Colab notebook is running)"
    
    def configure(self):
        """Interactive configuration"""
        print("🔧 Colab Bridge Configuration")
        print("="*40)
        
        # Check current setup
        info = self.bridge.get_setup_info()
        print(f"Automation available: {'✅' if info['automation_available'] else '❌'}")
        
        if info['automation_available']:
            print("\n🎭 Headless automation is available!")
            print("This means the extension can set up Colab automatically.")
        else:
            print("\n📋 Manual setup will be used.")
            print("You'll need to open a Colab notebook manually.")
        
        # Ask for preference
        print("\nPreferences:")
        print("1. Auto (try headless, fallback to manual)")
        print("2. Always use headless automation")
        print("3. Always use manual setup")
        print("4. Ask me each time")
        
        choice = input("\nEnter preference (1-4): ").strip()
        
        preferences = {
            "1": "auto",
            "2": "headless", 
            "3": "manual",
            "4": "prompt"
        }
        
        if choice in preferences:
            self.bridge.automation_mode = preferences[choice]
            print(f"✅ Preference set to: {preferences[choice]}")
            
            # Save preference
            config_dir = Path.home() / '.colab-bridge'
            config_dir.mkdir(exist_ok=True)
            
            import json
            with open(config_dir / 'preferences.json', 'w') as f:
                json.dump({'automation_mode': preferences[choice]}, f)
        else:
            print("Invalid choice, keeping current settings")

# Convenience functions for different use cases
def auto_execute(code):
    """Execute with automatic method selection"""
    bridge = SmartColabBridge(automation_mode="auto")
    bridge.initialize()
    return bridge.execute(code)

def headless_execute(code):
    """Execute with headless automation only"""
    bridge = SmartColabBridge(automation_mode="headless")
    bridge.initialize()
    return bridge.execute(code)

def manual_execute(code):
    """Execute with manual setup only"""
    bridge = SmartColabBridge(automation_mode="manual")
    bridge.initialize()
    return bridge.execute(code)

if __name__ == "__main__":
    # Demo all approaches
    print("🧪 Testing Smart Colab Bridge...")
    
    # Let user choose
    bridge = SmartColabBridge(automation_mode="prompt")
    bridge.initialize()
    
    # Test execution
    result = bridge.execute('''
import sys
print(f"Python: {sys.version}")
print("✅ Smart bridge execution successful!")
print(f"Setup method: {bridge.setup_method}")
''')
    
    print(f"\n📥 Result: {result}")
    print(f"\n📊 Setup info: {bridge.get_setup_info()}")