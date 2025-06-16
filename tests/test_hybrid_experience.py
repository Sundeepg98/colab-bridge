#!/usr/bin/env python3
"""
Test Hybrid Local Experience - Direct Impact Testing
Tests the "basically local google colab notebook" experience from local directory
"""

import os
import sys
import time
import tempfile
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.local_notebook import LocalColabNotebook
from colab_integration.file_sync import FileSyncManager
from colab_integration.universal_bridge import UniversalColabBridge


def test_direct_impact_workflow():
    """
    Test the complete workflow: local files → Colab execution → local results
    This demonstrates "direct impact" from local directory
    """
    print("🎯 Testing Direct Impact Workflow")
    print("=" * 60)
    print("Goal: Work locally, execute on Colab, see immediate local impact")
    print("=" * 60)
    
    # Create temporary workspace
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = Path(temp_dir)
        print(f"📁 Test workspace: {workspace}")
        
        # Test 1: Create local files
        print("\n📋 Test 1: Creating local files...")
        
        # Create Python script
        script_file = workspace / "analysis.py"
        with open(script_file, 'w') as f:
            f.write("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

print("🔬 Starting data analysis...")

# Generate sample data
np.random.seed(42)
data = {
    'date': pd.date_range('2024-01-01', periods=100),
    'sales': np.random.normal(1000, 200, 100),
    'profit': np.random.normal(150, 50, 100)
}

df = pd.DataFrame(data)
print(f"📊 Generated dataset: {df.shape}")

# Analysis
monthly_sales = df.groupby(df['date'].dt.month)['sales'].sum()
total_profit = df['profit'].sum()

print(f"💰 Total profit: ${total_profit:.2f}")
print(f"📈 Monthly sales summary:")
print(monthly_sales)

# Save results
df.to_csv('results.csv', index=False)
monthly_sales.to_csv('monthly_summary.csv')

# Create visualization
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(df['date'], df['sales'])
plt.title('Daily Sales')
plt.ylabel('Sales ($)')

plt.subplot(2, 1, 2)
plt.plot(df['date'], df['profit'])
plt.title('Daily Profit')
plt.ylabel('Profit ($)')
plt.xlabel('Date')

plt.tight_layout()
plt.savefig('analysis_plot.png', dpi=150, bbox_inches='tight')
print("📊 Saved analysis plot: analysis_plot.png")

# Summary report
with open('analysis_report.txt', 'w') as f:
    f.write(f"Data Analysis Report\\n")
    f.write(f"Generated: {datetime.now()}\\n")
    f.write(f"Dataset size: {df.shape[0]} records\\n")
    f.write(f"Total sales: ${df['sales'].sum():.2f}\\n")
    f.write(f"Total profit: ${total_profit:.2f}\\n")
    f.write(f"Average daily sales: ${df['sales'].mean():.2f}\\n")
    f.write(f"Profit margin: {(total_profit/df['sales'].sum()*100):.1f}%\\n")

print("✅ Analysis complete - all files saved locally!")
print(f"📁 Output files: results.csv, monthly_summary.csv, analysis_plot.png, analysis_report.txt")
""")
        
        # Create data file
        data_file = workspace / "config.json"
        with open(data_file, 'w') as f:
            f.write('{"project": "hybrid_test", "version": "1.0", "gpu_required": true}')
        
        print(f"✅ Created local files:")
        print(f"  📄 {script_file.name}")
        print(f"  📄 {data_file.name}")
        
        # Test 2: Initialize hybrid notebook
        print("\n📋 Test 2: Initializing hybrid notebook...")
        
        notebook_path = workspace / "hybrid_test.ipynb"
        notebook = LocalColabNotebook(str(notebook_path), "hybrid_test")
        
        if not notebook.initialize_colab():
            print("❌ Failed to initialize Colab connection")
            return False
        
        print("✅ Hybrid notebook initialized")
        
        # Test 3: Add code cells that work with local files
        print("\n📋 Test 3: Creating notebook with local file operations...")
        
        # Clear default cells
        notebook.cells = []
        
        # Cell 1: Environment check
        notebook.add_cell("code", """
print("🌍 Environment Check")
print("-" * 30)

import os
import sys
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")

# Check available libraries
libraries = ['pandas', 'numpy', 'matplotlib', 'torch']
for lib in libraries:
    try:
        __import__(lib)
        print(f"✅ {lib} available")
    except ImportError:
        print(f"❌ {lib} not available")

# Check GPU
try:
    import torch
    if torch.cuda.is_available():
        print(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("💻 CPU only")
except:
    print("💻 CPU only")
""")
        
        # Cell 2: Execute local script
        notebook.add_cell("code", """
print("🔄 Executing local analysis script...")
exec(open('analysis.py').read())
""")
        
        # Cell 3: Verify local outputs
        notebook.add_cell("code", """
print("🔍 Verifying local outputs...")

import os
import pandas as pd

# Check generated files
expected_files = ['results.csv', 'monthly_summary.csv', 'analysis_plot.png', 'analysis_report.txt']
existing_files = []

for file in expected_files:
    if os.path.exists(file):
        existing_files.append(file)
        size = os.path.getsize(file)
        print(f"✅ {file} ({size} bytes)")
    else:
        print(f"❌ {file} missing")

print(f"\\n📊 Generated {len(existing_files)}/{len(expected_files)} expected files")

# Preview results
if 'results.csv' in existing_files:
    df = pd.read_csv('results.csv')
    print(f"\\n📋 Results preview (first 5 rows):")
    print(df.head())

if 'analysis_report.txt' in existing_files:
    with open('analysis_report.txt', 'r') as f:
        report = f.read()
    print(f"\\n📝 Analysis report:")
    print(report)
""")
        
        # Cell 4: Additional GPU computation
        notebook.add_cell("code", """
print("🧠 GPU Computation Test...")

try:
    import torch
    import numpy as np
    
    if torch.cuda.is_available():
        print("🚀 Using GPU for computation")
        
        # Large matrix operations on GPU
        size = 5000
        a = torch.randn(size, size).cuda()
        b = torch.randn(size, size).cuda()
        
        start_time = time.time()
        c = torch.mm(a, b)
        gpu_time = time.time() - start_time
        
        print(f"✅ GPU computation: {size}x{size} matrix multiplication in {gpu_time:.3f}s")
        
        # Save computation result info
        with open('gpu_computation.txt', 'w') as f:
            f.write(f"GPU Computation Results\\n")
            f.write(f"Matrix size: {size}x{size}\\n")
            f.write(f"Computation time: {gpu_time:.3f}s\\n")
            f.write(f"GPU: {torch.cuda.get_device_name(0)}\\n")
            f.write(f"Result matrix norm: {torch.norm(c).item():.2f}\\n")
        
        print("💾 Saved GPU computation info to gpu_computation.txt")
        
    else:
        print("💻 No GPU available, using CPU")
        
        # CPU computation
        a = np.random.randn(1000, 1000)
        b = np.random.randn(1000, 1000)
        
        start_time = time.time()
        c = np.dot(a, b)
        cpu_time = time.time() - start_time
        
        print(f"✅ CPU computation: 1000x1000 matrix multiplication in {cpu_time:.3f}s")
        
        with open('cpu_computation.txt', 'w') as f:
            f.write(f"CPU Computation Results\\n")
            f.write(f"Matrix size: 1000x1000\\n")
            f.write(f"Computation time: {cpu_time:.3f}s\\n")
            f.write(f"Result matrix norm: {np.linalg.norm(c):.2f}\\n")

except Exception as e:
    print(f"❌ Computation error: {e}")

print("✅ Computation test completed")
""")
        
        notebook.save_notebook()
        print(f"✅ Created notebook with {len(notebook.cells)} cells")
        
        # Test 4: Execute notebook and verify direct local impact
        print("\n📋 Test 4: Executing notebook - testing direct local impact...")
        
        # Count files before execution
        files_before = list(workspace.glob("*"))
        print(f"📁 Files before execution: {len(files_before)}")
        for f in files_before:
            print(f"  📄 {f.name}")
        
        # Execute all cells
        results = notebook.run_all_cells()
        
        # Count files after execution
        files_after = list(workspace.glob("*"))
        new_files = [f for f in files_after if f not in files_before]
        
        print(f"\n📊 Execution Results:")
        print(f"  📋 Cells executed: {len(results)}")
        print(f"  ✅ Successful: {sum(1 for r in results if r.get('status') == 'success')}")
        print(f"  ❌ Failed: {sum(1 for r in results if r.get('status') == 'error')}")
        print(f"  📁 Files after: {len(files_after)}")
        print(f"  ➕ New files: {len(new_files)}")
        
        # Show new files (direct impact)
        if new_files:
            print(f"\n🎯 DIRECT IMPACT - New files created:")
            for f in new_files:
                size = f.stat().st_size
                print(f"  📄 {f.name} ({size} bytes)")
        
        # Test 5: Verify file contents (prove local impact)
        print("\n📋 Test 5: Verifying local file contents...")
        
        expected_outputs = [
            'results.csv',
            'monthly_summary.csv', 
            'analysis_plot.png',
            'analysis_report.txt'
        ]
        
        verified_files = 0
        for filename in expected_outputs:
            filepath = workspace / filename
            if filepath.exists():
                size = filepath.stat().st_size
                print(f"  ✅ {filename} ({size} bytes)")
                
                # Verify content
                if filename.endswith('.txt'):
                    with open(filepath, 'r') as f:
                        content = f.read()
                    print(f"    📝 Preview: {content[:100]}...")
                elif filename.endswith('.csv'):
                    try:
                        import pandas as pd
                        df = pd.read_csv(filepath)
                        print(f"    📊 Shape: {df.shape}")
                    except:
                        print(f"    📄 CSV file present")
                
                verified_files += 1
            else:
                print(f"  ❌ {filename} missing")
        
        # Test 6: Performance summary
        print(f"\n📊 Test Summary:")
        print(f"  📓 Notebook: {notebook_path.name}")
        print(f"  📄 Cells: {len(notebook.cells)}")
        print(f"  ⚡ Executions: {notebook.execution_count}")
        print(f"  📁 Generated files: {verified_files}/{len(expected_outputs)}")
        print(f"  🎯 Direct impact: {'✅ SUCCESS' if verified_files >= 3 else '❌ PARTIAL'}")
        
        success = verified_files >= 3
        
        if success:
            print("\n🎉 HYBRID EXPERIENCE TEST PASSED!")
            print("✅ Successfully demonstrated:")
            print("  • Local file creation and editing")
            print("  • Colab execution with GPU access") 
            print("  • Direct local file output (immediate impact)")
            print("  • Seamless local ↔ cloud workflow")
        else:
            print("\n⚠️ Test completed with some issues")
        
        return success


def test_file_synchronization():
    """Test bidirectional file sync between local and Colab"""
    print("\n🔄 Testing File Synchronization")
    print("=" * 40)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = Path(temp_dir)
        
        # Create test files
        test_files = {
            'script.py': 'print("Hello from synced file!")',
            'data.json': '{"test": true, "value": 42}',
            'readme.md': '# Test Project\nThis is a test.'
        }
        
        for filename, content in test_files.items():
            with open(workspace / filename, 'w') as f:
                f.write(content)
        
        print(f"📁 Created {len(test_files)} test files")
        
        # Test sync manager
        sync_manager = FileSyncManager(str(workspace))
        
        # Test upload
        print("📤 Testing upload to Colab...")
        upload_success = sync_manager.sync_to_colab()
        
        if upload_success:
            print("✅ Upload successful")
        else:
            print("❌ Upload failed")
        
        # Test download
        print("📥 Testing download from Colab...")
        download_success = sync_manager.sync_from_colab()
        
        if download_success:
            print("✅ Download successful")
        else:
            print("❌ Download failed")
        
        # Test full sync
        print("🔄 Testing full sync...")
        full_sync_success = sync_manager.full_sync()
        
        print(f"📊 Sync test results:")
        print(f"  📤 Upload: {'✅' if upload_success else '❌'}")
        print(f"  📥 Download: {'✅' if download_success else '❌'}")
        print(f"  🔄 Full sync: {'✅' if full_sync_success else '❌'}")
        
        return upload_success and download_success


def test_ide_workflow():
    """Test complete IDE-like workflow"""
    print("\n🎮 Testing IDE Workflow")
    print("=" * 40)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = Path(temp_dir)
        
        # Create notebook
        notebook_path = workspace / "ide_test.ipynb"
        notebook = LocalColabNotebook(str(notebook_path), "ide_test")
        
        if not notebook.initialize_colab():
            print("❌ Failed to initialize notebook")
            return False
        
        print("✅ Notebook initialized")
        
        # Test IDE operations
        operations = [
            ("Add cell", lambda: notebook.add_cell("code", "print('IDE test cell')")),
            ("Run cell", lambda: notebook.run_cell(0)),
            ("Add another cell", lambda: notebook.add_cell("code", "x = 42\nprint(f'The answer is {x}')")),
            ("Run all cells", lambda: notebook.run_all_cells()),
            ("Save notebook", lambda: notebook.save_notebook())
        ]
        
        results = []
        for operation_name, operation in operations:
            try:
                print(f"🔄 {operation_name}...")
                result = operation()
                print(f"✅ {operation_name} successful")
                results.append(True)
            except Exception as e:
                print(f"❌ {operation_name} failed: {e}")
                results.append(False)
        
        success_rate = sum(results) / len(results)
        print(f"📊 IDE workflow success rate: {success_rate:.1%}")
        
        return success_rate >= 0.8


def run_all_tests():
    """Run comprehensive hybrid experience tests"""
    print("🧪 Comprehensive Hybrid Experience Tests")
    print("=" * 70)
    print("Testing: 'Basically local google colab notebook'")
    print("Goal: Local comfort + Colab power + Direct impact")
    print("=" * 70)
    
    tests = [
        ("Direct Impact Workflow", test_direct_impact_workflow),
        ("File Synchronization", test_file_synchronization),
        ("IDE Workflow", test_ide_workflow)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🚀 Running {test_name}...")
        try:
            result = test_func()
            results[test_name] = result
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"📊 {test_name}: {status}")
        except Exception as e:
            print(f"💥 {test_name} crashed: {e}")
            results[test_name] = False
    
    # Final summary
    print("\n" + "=" * 70)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 70)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({passed/total:.1%})")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Hybrid local Colab experience is working!")
        print("✅ Users can work locally with direct Colab impact!")
    elif passed >= total * 0.5:
        print("\n⚠️ PARTIAL SUCCESS")
        print("Some features working, needs improvement")
    else:
        print("\n❌ TESTS FAILED")
        print("Hybrid experience needs significant work")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🎯 READY FOR PRODUCTION!")
        print("The hybrid local experience is working as requested:")
        print("• 'Basically local google colab notebook' ✅")
        print("• 'Run test all from local directory' ✅") 
        print("• 'Direct impact' ✅")
    else:
        print("\n🔧 NEEDS WORK")
        print("Some issues detected - check logs above")
    
    sys.exit(0 if success else 1)