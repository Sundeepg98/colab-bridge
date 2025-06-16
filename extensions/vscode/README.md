# Colab Bridge - VS Code Extension

Execute Python code in Google Colab directly from VS Code with GPU access!

## Features

- 🚀 **Execute Python code in Google Colab** - Run your code with free GPU/TPU
- 📝 **Execute selection or entire file** - Flexible execution options
- ⚡ **Keyboard shortcuts** - Quick access with `Ctrl+Shift+C`
- 📊 **Inline results** - See output directly in VS Code
- 🔧 **Easy configuration** - Simple setup process

## Quick Start

1. Install the extension from VS Code Marketplace
2. Configure your Google service account:
   - Press `Ctrl+Shift+P` → "Colab Bridge: Configure"
   - Provide your service account JSON path
3. Execute code:
   - Select code and press `Ctrl+Shift+C`
   - Or right-click → "Execute Selection in Google Colab"

## Requirements

- Python 3.7+
- Google Cloud service account with Drive API access
- `colab-bridge` Python package: `pip install colab-bridge`

## Commands

| Command | Description | Shortcut |
|---------|-------------|----------|
| Execute Selection in Colab | Run selected Python code | `Ctrl+Shift+C` |
| Execute File in Colab | Run entire Python file | - |
| Open Colab Notebook | Open the processor notebook | - |
| Configure Colab Bridge | Set up credentials | - |

## Configuration

Access settings through VS Code preferences:

- `colab-bridge.serviceAccountPath`: Path to your Google service account JSON
- `colab-bridge.googleDriveFolderId`: Google Drive folder for integration
- `colab-bridge.pythonPath`: Python executable path (default: `python3`)
- `colab-bridge.timeout`: Execution timeout in seconds (default: 30)
- `colab-bridge.showOutputInNewTab`: Show results in new tab (default: true)

## Example

```python
# Select this code and press Ctrl+Shift+C
import torch
print(f"GPU Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
```

## Troubleshooting

1. **"Service account not configured"**
   - Run "Colab Bridge: Configure" command
   - Ensure JSON file path is correct

2. **"Timeout waiting for result"**
   - Make sure Colab notebook is running
   - Check internet connection
   - Increase timeout in settings

3. **"Module not found"**
   - Install colab-bridge: `pip install colab-bridge`
   - Check Python path in settings

## Links

- [GitHub Repository](https://github.com/Sundeepg98/colab-bridge)
- [Report Issues](https://github.com/Sundeepg98/colab-bridge/issues)
- [Documentation](https://github.com/Sundeepg98/colab-bridge#readme)