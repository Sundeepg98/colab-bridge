#!/usr/bin/env python3
"""
Quick check if Colab processor is running
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.universal_bridge import UniversalColabBridge

def check_colab_status():
    """Check if Colab processor is responding"""
    print("🔍 Checking Colab Processor Status")
    print("=" * 40)
    
    try:
        bridge = UniversalColabBridge("status_check")
        bridge.initialize()
        print("✅ Connected to Google Drive")
        
        # Send a simple test command
        print("📤 Sending test command...")
        result = bridge.execute_code("print('Colab processor is running!')", timeout=20)
        
        if result.get('status') == 'success':
            print("✅ COLAB PROCESSOR IS RUNNING!")
            print(f"📤 Response: {result.get('output', '')}")
            print("\n🎯 Ready to test hybrid experience!")
            return True
        
        elif result.get('status') == 'queued':
            print("⏳ Command queued - Colab processor not running")
            print("\n💡 Next steps:")
            print("1. Open: https://colab.research.google.com/drive/1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA")
            print("2. Run all cells (it will auto-start)")
            print("3. Wait for '✅ Auto-processor started!'")
            print("4. Come back and run this check again")
            return False
        
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def quick_hybrid_test():
    """Quick test if processor is running"""
    print("\n🚀 Quick Hybrid Test")
    print("=" * 40)
    
    if not check_colab_status():
        return False
    
    print("\n📝 Testing hybrid notebook creation...")
    
    # Test just the basic workflow without full execution
    try:
        from colab_integration.local_notebook import LocalColabNotebook
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = f"{temp_dir}/quick_test.ipynb"
            notebook = LocalColabNotebook(notebook_path, "quick_test")
            
            if notebook.initialize_colab():
                print("✅ Local notebook connected to Colab")
                
                # Add simple test cell
                notebook.add_cell("code", """
print("🎉 SUCCESS! Hybrid experience working!")
print("✅ Local notebook → Colab execution → Local results")
import datetime
print(f"⏰ Executed at: {datetime.datetime.now()}")
""")
                
                print("📝 Added test cell")
                print("🚀 Executing on Colab...")
                
                result = notebook.run_cell(0, timeout=30)
                
                if result.get('status') == 'success':
                    print("\n🎉 HYBRID EXPERIENCE WORKING!")
                    print("=" * 50)
                    print("✅ Your 'basically local google colab notebook' is ready!")
                    print("✅ Local files + Colab execution + Direct impact")
                    print("\n📤 Output from Colab:")
                    print("-" * 30)
                    print(result.get('output', ''))
                    print("-" * 30)
                    return True
                else:
                    print(f"❌ Execution failed: {result.get('error', 'Unknown')}")
                    return False
            else:
                print("❌ Failed to initialize local notebook")
                return False
                
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = quick_hybrid_test()
    
    if success:
        print("\n🎯 READY FOR FULL TESTING!")
        print("Run: python3 test_now.py")
    else:
        print("\n🔧 Please start Colab processor first")
        print("Link: https://colab.research.google.com/drive/1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA")