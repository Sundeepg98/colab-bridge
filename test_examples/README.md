# Colab Bridge Test Examples

This directory contains test files for verifying the Colab Bridge VS Code extension works correctly.

## Quick Test

1. Open VS Code in this directory:
   ```bash
   code /var/projects/colab-bridge/test_examples
   ```

2. Open `test_gpu.py`

3. Press `Ctrl+Shift+Alt+C` to execute on Colab GPU

4. Check the Output panel for results

## Known Issues Fixed

### "Colab Bridge not installed" Error
This was caused by the VS Code extension not passing environment variables to Python. 

**Solution:** Create a Python wrapper script that sets the required environment variables:

```bash
# Create wrapper at ~/bin/python3-colab
#!/bin/bash
export SERVICE_ACCOUNT_PATH="/path/to/service-account.json"
export GOOGLE_DRIVE_FOLDER_ID="your-folder-id"
/usr/bin/python3 "$@"
```

Then update VS Code settings:
```json
{
  "colab-bridge.pythonPath": "~/bin/python3-colab"
}
```

## Files

- `test_gpu.py` - Simple GPU test using PyTorch
- `test_plots.py` - Test matplotlib plotting
- `playwright_final_test.py` - Automated test using Playwright

## Testing in Cloud Shell

For headless testing in Google Cloud Shell:

```bash
# Install dependencies
pip install playwright
playwright install chromium

# Run headless test
python3 playwright_final_test.py
```

## Configuration

The `.vscode/settings.json` file contains the necessary configuration:
- `colab-bridge.pythonPath` - Path to Python wrapper
- `colab-bridge.serviceAccountPath` - Google service account JSON
- `colab-bridge.driveFolder` - Google Drive folder ID
- `colab-bridge.timeout` - Execution timeout in seconds