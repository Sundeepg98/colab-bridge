# 🔍 VS Code Extension Debugging Guide

## 1. Check Extension Installation

### In VS Code:
1. **Open Extensions panel** (Ctrl+Shift+X)
2. Search for "Colab Bridge"
3. Is it installed and enabled?

### Check version:
```bash
code --list-extensions | grep colab
```

## 2. Check Extension Commands

### Command Palette Test:
1. Open Command Palette (Ctrl+Shift+P)
2. Type "Colab Bridge"
3. You should see:
   - `Colab Bridge: Execute File in Colab`
   - `Colab Bridge: Execute Selection in Colab`
   - `Colab Bridge: Open Colab Processor`
   - `Colab Bridge: Configure`
   - `Colab Bridge: Show Status`

## 3. Check Extension Configuration

### Open VS Code Settings:
1. Ctrl+, (Settings)
2. Search for "colab-bridge"
3. Check these settings:
   - `colab-bridge.pythonPath`
   - `colab-bridge.interceptTerminal`
   - `colab-bridge.showStatusBar`

## 4. Check Extension Logs

### View Output:
1. View → Output (or Ctrl+Shift+U)
2. From dropdown, select "Colab Bridge"
3. Look for errors like:
   - "Failed to activate"
   - "Configuration missing"
   - "Drive API error"

## 5. Manual Test

### Create test file:
```python
# test_colab.py
print("Testing from VS Code!")
import torch
print(f"GPU: {torch.cuda.is_available()}")
```

### Execute manually:
1. Open test_colab.py
2. Ctrl+Shift+P → "Colab Bridge: Execute File in Colab"
3. Check Output panel for results

## 6. Check Terminal Integration

### The extension should:
- Show "Colab Bridge Active" in status bar
- Intercept `python` commands in terminal
- Replace local execution with Colab execution

### Test terminal:
```bash
python test_colab.py
```

Should show Colab output, not local output.

## 7. Common Issues

### Extension not activating:
- Check if Python extension is installed
- Reload VS Code window (Ctrl+Shift+P → "Reload Window")

### Commands not showing:
- Extension might not be built properly
- Try reinstalling from VSIX file

### Terminal not intercepted:
- Check setting: `colab-bridge.interceptTerminal` is true
- Make sure you're in a Python workspace

## 8. Reinstall Extension

If nothing works:
```bash
# Uninstall
code --uninstall-extension colab-bridge.colab-bridge

# Reinstall from VSIX
code --install-extension /var/projects/colab-bridge/extensions/vscode/colab-bridge-1.0.0.vsix
```

## 9. Check Development Console

### For deeper debugging:
1. Help → Toggle Developer Tools
2. Go to Console tab
3. Look for errors related to "colab-bridge"

## 10. Verify Bridge Connection

### The extension needs:
- ✅ Service account credentials at: `/var/projects/colab-bridge/credentials/`
- ✅ Config file at: `~/.colab-bridge/config.json`
- ✅ Running processor in Colab
- ✅ Correct folder ID in config

All these are already set up correctly!