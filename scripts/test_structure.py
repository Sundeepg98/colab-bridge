#!/usr/bin/env python3
"""
Test Claude Tools structure and organization
"""

import os
import sys
from pathlib import Path

def test_project_structure():
    """Test that all expected directories and files exist"""
    print("🧪 Claude Tools Structure Test")
    print("==============================\n")
    
    root = Path(__file__).parent.parent
    
    # Expected structure
    expected_dirs = [
        "colab_integration",
        "notebooks", 
        "config",
        "scripts",
        "docs",
        "docs/guides",
        "archive"
    ]
    
    expected_files = [
        "README.md",
        "requirements.txt",
        ".gitignore",
        "colab_integration/bridge.py",
        "colab_integration/processor.py",
        "notebooks/basic-integration.ipynb",
        "notebooks/universal-integration.ipynb",
        "config/.env.template",
        "config/service-account.template.json",
        "docs/guides/COLAB_INTEGRATION.md",
        "docs/guides/GITHUB_SETUP_GUIDE.md",
        "docs/guides/SECURITY_PREPARATION_GUIDE.md"
    ]
    
    print("📁 Checking directories...")
    dirs_ok = True
    for dir_path in expected_dirs:
        full_path = root / dir_path
        if full_path.exists() and full_path.is_dir():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/ (missing)")
            dirs_ok = False
    
    print("\n📄 Checking files...")
    files_ok = True
    for file_path in expected_files:
        full_path = root / file_path
        if full_path.exists() and full_path.is_file():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
            files_ok = False
    
    print("\n📊 Summary:")
    if dirs_ok and files_ok:
        print("✅ All structure tests passed!")
        print("🎉 Claude Tools is properly organized")
        return True
    else:
        print("❌ Some structure tests failed")
        return False

def test_imports():
    """Test that Python modules can be imported"""
    print("\n\n🐍 Testing Python imports...")
    print("============================\n")
    
    # Add parent to path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    imports_ok = True
    
    try:
        from colab_integration.bridge import ClaudeColabBridge
        print("✅ colab_integration.bridge imported successfully")
    except Exception as e:
        print(f"❌ Failed to import bridge: {e}")
        imports_ok = False
    
    try:
        from colab_integration.processor import ColabProcessor
        print("✅ colab_integration.processor imported successfully")
    except Exception as e:
        print(f"❌ Failed to import processor: {e}")
        imports_ok = False
    
    return imports_ok

def test_configuration():
    """Test configuration templates"""
    print("\n\n⚙️  Testing configuration...")
    print("==========================\n")
    
    root = Path(__file__).parent.parent
    
    # Check .env.template
    env_template = root / "config" / ".env.template"
    if env_template.exists():
        content = env_template.read_text()
        if "SERVICE_ACCOUNT_PATH" in content and "GOOGLE_DRIVE_FOLDER_ID" in content:
            print("✅ .env.template has required variables")
        else:
            print("❌ .env.template missing required variables")
    else:
        print("❌ .env.template not found")
    
    # Check service account template
    sa_template = root / "config" / "service-account.template.json"
    if sa_template.exists():
        print("✅ service-account.template.json exists")
    else:
        print("❌ service-account.template.json not found")
    
    return True

def main():
    """Run all structure tests"""
    print("🚀 Claude Tools Complete Structure Test")
    print("=" * 40)
    print()
    
    # Run tests
    structure_ok = test_project_structure()
    imports_ok = test_imports()
    config_ok = test_configuration()
    
    # Final result
    print("\n\n" + "=" * 40)
    print("📊 FINAL RESULTS")
    print("=" * 40)
    
    all_passed = structure_ok and imports_ok and config_ok
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED!")
        print("🎉 Claude Tools is ready for use")
        print("\n📝 Next steps:")
        print("1. Add your Google service account JSON")
        print("2. Configure .env with your credentials")
        print("3. Run a Colab notebook to test integration")
        return 0
    else:
        print("\n❌ Some tests failed")
        print("Please check the errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())