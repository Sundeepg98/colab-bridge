# 🚀 VS Code Extension Testing Guide

## Current Status
✅ Extension built: `colab-bridge-1.0.0.vsix` (8KB)
✅ Located at: `/home/sundeepg8/projects/colab-bridge/extensions/vscode/`

## Testing Options:

### Option 1: Use Cloud Shell Editor (Recommended)
```bash
# In Cloud Shell, click "Open Editor" button
# This opens a web-based VS Code
cloudshell edit .
```

### Option 2: Download and Test Locally

1. **Download the extension**
```bash
# In Cloud Shell
cd ~/projects/colab-bridge/extensions/vscode

# Download using Cloud Shell download
cloudshell download colab-bridge-1.0.0.vsix
```

2. **Install in your local VS Code**
- Open VS Code on your computer
- Press `Ctrl+Shift+P` → "Extensions: Install from VSIX"
- Select the downloaded file

### Option 3: Test Without Extension

Test the core functionality directly:

```bash
cd ~/projects/colab-bridge

# Test the bridge directly
python3 -c "
from colab_integration.universal_bridge import UniversalColabBridge
bridge = UniversalColabBridge('test')
bridge.initialize()
print('✅ Bridge initialized successfully!')
"

# Test with sample code
python3 test_simple_hybrid.py
```

## Quick Functionality Test:

```python
# Save this as quick_test.py
from colab_integration.universal_bridge import UniversalColabBridge

# Initialize
bridge = UniversalColabBridge("vscode_test")
bridge.initialize()

# Test code execution
test_code = '''
import sys
print(f"Python: {sys.version}")
print("Hello from Colab Bridge!")
'''

print("🚀 Sending code to Colab...")
result = bridge.execute_code(test_code, timeout=30)
print(f"📥 Result: {result}")
```

## Manual Testing Steps:

1. **Ensure Colab notebook is running**
   - Open: https://colab.research.google.com/drive/11fwFzrRuxcLIWH9MYjNDWfHWArmgCXSY
   - Run all cells

2. **Test execution**
```bash
cd ~/projects/colab-bridge
python3 test_gpu.py
```

3. **Check results**
   - Look for output in terminal
   - Check Drive folder for result files

## What Success Looks Like:

✅ Bridge initializes without errors
✅ Code is sent to Colab
✅ Results return within 30 seconds
✅ GPU is detected (if using Colab with GPU)

## Troubleshooting:

1. **"SERVICE_ACCOUNT_PATH not found"**
```bash
export SERVICE_ACCOUNT_PATH=~/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json
```

2. **"Timeout waiting for results"**
- Make sure Colab notebook is running
- Check internet connection
- Try increasing timeout

3. **"Module not found"**
```bash
cd ~/projects/colab-bridge
pip3 install -e .
```

Ready to test? Start with Option 3 to verify core functionality!