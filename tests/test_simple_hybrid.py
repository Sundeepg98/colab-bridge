#!/usr/bin/env python3
"""
Simple test to verify hybrid local experience components work
"""

import os
import sys
import tempfile
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_environment_setup():
    """Test that environment is properly configured"""
    print("🔧 Testing Environment Setup")
    print("=" * 40)
    
    # Check .env file
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        print(f"✅ .env file found: {env_path}")
        with open(env_path, 'r') as f:
            content = f.read()
        print(f"📄 Content preview: {len(content)} characters")
    else:
        print(f"❌ .env file missing: {env_path}")
        return False
    
    # Check service account file
    from colab_integration.universal_bridge import UniversalColabBridge
    
    try:
        bridge = UniversalColabBridge("test")
        service_account_path = bridge.config.get('service_account_path')
        
        if service_account_path:
            print(f"✅ Service account path configured: {service_account_path}")
            
            if Path(service_account_path).exists():
                print(f"✅ Service account file exists")
                return True
            else:
                print(f"❌ Service account file not found: {service_account_path}")
                return False
        else:
            print(f"❌ SERVICE_ACCOUNT_PATH not set")
            return False
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_local_notebook_creation():
    """Test creating a local notebook without Colab connection"""
    print("\n📓 Testing Local Notebook Creation")
    print("=" * 40)
    
    try:
        from colab_integration.local_notebook import LocalColabNotebook
        
        with tempfile.TemporaryDirectory() as temp_dir:
            notebook_path = Path(temp_dir) / "test.ipynb"
            
            # Create notebook without initializing Colab
            notebook = LocalColabNotebook(str(notebook_path), "test")
            
            print(f"✅ Created notebook: {notebook_path.name}")
            print(f"📊 Initial cells: {len(notebook.cells)}")
            
            # Add a cell
            notebook.add_cell("code", "print('Hello from local notebook!')")
            print(f"✅ Added cell, total: {len(notebook.cells)}")
            
            # Save notebook
            notebook.save_notebook()
            
            if notebook_path.exists():
                print(f"✅ Notebook saved successfully")
                print(f"📁 File size: {notebook_path.stat().st_size} bytes")
                return True
            else:
                print(f"❌ Notebook file not created")
                return False
                
    except Exception as e:
        print(f"❌ Notebook creation error: {e}")
        return False

def test_file_sync_setup():
    """Test file sync manager creation"""
    print("\n📁 Testing File Sync Setup")
    print("=" * 40)
    
    try:
        from colab_integration.file_sync import FileSyncManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            sync_manager = FileSyncManager(temp_dir)
            
            print(f"✅ Created file sync manager")
            print(f"📁 Local dir: {sync_manager.local_dir}")
            print(f"🔗 Colab mount: {sync_manager.colab_mount}")
            
            # Create test file
            test_file = Path(temp_dir) / "test.py"
            with open(test_file, 'w') as f:
                f.write("print('test file')")
            
            # Scan local files
            local_files = sync_manager.scan_local_files()
            print(f"✅ Scanned local files: {len(local_files)}")
            
            if 'test.py' in local_files:
                print(f"✅ Test file detected in scan")
                return True
            else:
                print(f"❌ Test file not detected")
                return False
                
    except Exception as e:
        print(f"❌ File sync error: {e}")
        return False

def test_hybrid_components():
    """Test all hybrid components without Colab connection"""
    print("🧪 Testing Hybrid Components (Offline)")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Local Notebook Creation", test_local_notebook_creation),
        ("File Sync Setup", test_file_sync_setup)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"\n📊 {test_name}: {status}")
        except Exception as e:
            print(f"\n💥 {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n" + "=" * 50)
    print(f"🏁 HYBRID COMPONENTS TEST RESULTS")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({passed/total:.1%})")
    
    if passed == total:
        print("\n🎉 ALL COMPONENTS READY!")
        print("✅ Hybrid local experience components working")
        print("✅ Ready for Colab integration testing")
    else:
        print("\n⚠️ SOME COMPONENTS NEED FIXING")
    
    return passed == total

if __name__ == "__main__":
    success = test_hybrid_components()
    sys.exit(0 if success else 1)