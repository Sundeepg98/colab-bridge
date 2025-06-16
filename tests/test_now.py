#!/usr/bin/env python3
"""
Test the hybrid experience right now
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.local_notebook import LocalColabNotebook

def test_hybrid_now():
    """Test the hybrid notebook experience"""
    print("🎯 Testing Hybrid Experience NOW")
    print("=" * 50)
    
    # Create a test notebook
    notebook_path = "/tmp/test_hybrid_now.ipynb"
    print(f"📓 Creating notebook: {notebook_path}")
    
    notebook = LocalColabNotebook(notebook_path, "test_now")
    
    # Initialize Colab connection
    print("🔗 Connecting to Colab...")
    if notebook.initialize_colab():
        print("✅ Connected to Colab!")
    else:
        print("❌ Colab connection failed")
        return False
    
    # Clear default cells and add test
    notebook.cells = []
    
    # Add a simple test cell
    notebook.add_cell("code", """
print("🎉 Hello from Hybrid Local Notebook!")
print("🌍 This is running on Google Colab...")
print("💻 But feels completely local!")

import datetime
print(f"⏰ Executed at: {datetime.datetime.now()}")

# Test computation
numbers = list(range(1, 6))
result = sum(x**2 for x in numbers)
print(f"🔢 Sum of squares 1-5: {result}")

# Check environment
import sys
print(f"🐍 Python: {sys.version[:20]}...")

# Check for GPU
try:
    import torch
    if torch.cuda.is_available():
        print(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("💻 CPU only")
except ImportError:
    print("💻 PyTorch not available")

print("✅ Hybrid test completed!")
""")
    
    print("📝 Added test cell")
    
    # Execute the cell
    print("\n🚀 Executing on Colab (this may take 30-60 seconds)...")
    print("   Uploading code → Colab execution → Results back to local")
    
    result = notebook.run_cell(0, timeout=90)
    
    print("\n📊 Results:")
    if result.get('status') == 'success':
        print("✅ SUCCESS! Hybrid notebook working!")
        print("📤 Output from Colab:")
        print("-" * 40)
        output = result.get('output', '')
        print(output if output else "No output received")
        print("-" * 40)
        print("🎯 This proves the hybrid experience works:")
        print("  • Code written locally")
        print("  • Executed on Google's cloud")
        print("  • Results displayed locally")
        return True
    
    elif result.get('status') == 'queued':
        print("⏳ Request queued - need to start Colab processor")
        print("\n💡 To complete the test:")
        print("1. Go to Google Colab: https://colab.research.google.com")
        print("2. Upload notebooks/hybrid-processor.ipynb")
        print("3. Run the notebook")
        print("4. Come back and run this test again")
        return False
    
    else:
        print(f"❌ Execution failed: {result.get('error', 'Unknown error')}")
        return False

if __name__ == "__main__":
    success = test_hybrid_now()
    
    if success:
        print("\n🎉 HYBRID EXPERIENCE WORKING!")
        print("Your 'basically local google colab notebook' is ready!")
    else:
        print("\n🔧 Need to setup Colab processor first")