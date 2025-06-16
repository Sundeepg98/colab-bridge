# 🧪 Testing VS Code Extension - Quick Guide

## Option 1: Install Pre-built Extension (Fastest)

```bash
# Install the VSIX file directly
code --install-extension ~/projects/colab-bridge/extensions/vscode/colab-bridge-1.0.0.vsix
```

## Option 2: Run in Development Mode

1. **Open VS Code**
```bash
cd ~/projects/colab-bridge/extensions/vscode
code .
```

2. **Run Extension**
- Press `F5` in VS Code
- This opens a new VS Code window with extension loaded

3. **Test Commands**
- Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
- Type "Colab Bridge" to see all commands:
  - `Colab Bridge: Configure`
  - `Colab Bridge: Execute File in Google Colab`
  - `Colab Bridge: Execute Selection in Google Colab`

## Quick Test Script

Create a test file `test_gpu.py`:

```python
# %%gpu
import sys
print(f"Python version: {sys.version}")

# Test GPU availability
try:
    import torch
    print(f"PyTorch available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
except:
    print("PyTorch not available")

# Test computation
import numpy as np
result = np.random.rand(1000, 1000).sum()
print(f"Computation result: {result}")
```

## Testing Steps:

1. **Configure Extension**
   - `Ctrl+Shift+P` → "Colab Bridge: Configure"
   - Set service account path: `/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json`

2. **Test Execution**
   - Open `test_gpu.py`
   - Select some code
   - Press `Ctrl+Shift+C`
   - Or right-click → "Execute Selection in Google Colab"

3. **Check Results**
   - Results should appear in new tab
   - Check Output panel for logs

## Troubleshooting:

If extension doesn't work:

```bash
# Check if extension is installed
code --list-extensions | grep colab

# Check logs
# View → Output → Select "Colab Bridge" from dropdown

# Reinstall
code --uninstall-extension sundeepg.colab-bridge
code --install-extension ~/projects/colab-bridge/extensions/vscode/colab-bridge-1.0.0.vsix
```