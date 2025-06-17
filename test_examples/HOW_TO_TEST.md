# How to Test test_gpu.py with Colab Bridge

## Quick Test Instructions

### 1. Open VS Code in the test directory
```bash
code /tmp/colab-bridge-automated-test
```

### 2. Test if extension is working
- Open `test_extension_working.py`
- Press `Ctrl+Shift+Alt+C` (or `Cmd+Shift+Alt+C` on Mac)
- If it shows "Running on Google Colab" - the extension works!
- If it shows "Running locally" - the extension has issues

### 3. Run test_gpu.py
- Open `test_gpu.py` in VS Code
- Use one of these methods:
  - **Method A**: Press `Ctrl+Shift+Alt+C` to execute entire file
  - **Method B**: Press `Ctrl+Shift+P` then type "Colab Bridge: Execute File in Colab"
  - **Method C**: Right-click in editor → "Execute File in Colab"

### 4. Expected Output (when working)
```
🚀 GPU Test
CUDA available: True
GPU: Tesla T4
Tensor on GPU: cuda:0
```

## If You Get "Command Not Found" Error

The extension might need to be reloaded:

1. Press `Ctrl+Shift+P`
2. Type: "Developer: Reload Window"
3. Try again

## If Extension Still Not Working

### Option A: Reinstall the fixed extension
```bash
# Uninstall old version
code --uninstall-extension colab-bridge.colab-bridge

# Install fixed version
code --install-extension /var/projects/colab-bridge/extensions/vscode/colab-bridge-1.0.0.vsix

# Reload VS Code
```

### Option B: Check extension is enabled
1. Press `Ctrl+Shift+X` to open Extensions
2. Search for "Colab Bridge"
3. Make sure it's enabled (not disabled)

### Option C: Check configuration
1. Press `Ctrl+Shift+P`
2. Type: "Preferences: Open Settings (JSON)"
3. Add these settings:
```json
{
  "colab-bridge.pythonPath": "python3",
  "colab-bridge.serviceAccountPath": "/var/projects/automation-engine/credentials/automation-engine-463103-ee5a06e18248.json",
  "colab-bridge.driveFolder": "YOUR_DRIVE_FOLDER_ID"
}
```

## Current Status
- Extension commands are fixed (no more claude-tools references)
- Need to ensure Google Drive folder is properly configured
- Colab processor notebook needs to be running