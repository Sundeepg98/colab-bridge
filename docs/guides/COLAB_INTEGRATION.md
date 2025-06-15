# 🔗 Colab Integration Guide

## Overview

The Colab Integration tool enables Claude Coder instances to execute Python code in Google Colab notebooks seamlessly. This is perfect for:
- Running ML/AI experiments
- Processing large datasets
- Using GPU/TPU resources
- Collaborative development

## Prerequisites

1. **Google Account** with Google Drive access
2. **Service Account** for Drive API access
3. **Python 3.8+** installed locally
4. **Google Colab** access

## Setup Steps

### 1. Create Google Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable Google Drive API
4. Create Service Account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Download JSON key file

### 2. Configure Google Drive

1. Create a folder in Google Drive for commands/results
2. Share this folder with your service account email
3. Note the folder ID from the URL

### 3. Local Setup

```bash
# From claude-tools root directory
cd claude-tools

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp config/.env.template .env

# Edit .env with your values:
# SERVICE_ACCOUNT_PATH=/path/to/service-account.json
# GOOGLE_DRIVE_FOLDER_ID=your-folder-id
```

### 4. Test Connection

```bash
# Test basic setup
python scripts/test_basic.py

# Should output:
# ✅ Environment variables configured
# ✅ Bridge created successfully
# ✅ Google Drive connection successful
```

## Usage

### Basic Example

```python
from colab_integration.bridge import ClaudeColabBridge

# Initialize bridge
bridge = ClaudeColabBridge()
bridge.initialize()

# Execute code in Colab
result = bridge.execute_code("""
import numpy as np
print("Hello from Colab!")
print(f"NumPy version: {np.__version__}")
""")

print(result['output'])
```

### Using Notebooks

1. **Basic Integration**: Open `notebooks/basic-integration.ipynb` in Google Colab
2. **Multi-Instance**: Use `notebooks/universal-integration.ipynb` for advanced features

## Advanced Features

### Multi-Instance Support

Multiple Claude instances can share Colab resources:

```python
bridge = ClaudeColabBridge({
    'projectName': 'project_alpha',
    'multiInstanceMode': True
})
```

### Command Types

- `execute_code` - Run Python code
- `install_package` - Install pip packages
- `shell_command` - Execute shell commands
- `file_operation` - Read/write files
- `system_status` - Get system info

## Troubleshooting

### Common Issues

1. **"Missing environment variables"**
   - Ensure `.env` file exists and is properly configured
   - Check variable names match exactly

2. **"Google Drive connection failed"**
   - Verify service account has access to the folder
   - Check service account JSON file path

3. **"Command timeout"**
   - Increase timeout in configuration
   - Check if Colab notebook is running

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Best Practices

1. **Security**
   - Never commit service account files
   - Use environment variables for all credentials
   - Regularly rotate service account keys

2. **Performance**
   - Batch commands when possible
   - Use appropriate timeouts
   - Monitor resource usage

3. **Organization**
   - Use project names for multi-instance setups
   - Clean up old command/result files
   - Document your Colab notebooks

## Examples

See the `notebooks/` directory for complete examples:
- `basic-integration.ipynb` - Simple single-instance setup
- `universal-integration.ipynb` - Advanced multi-project support

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review example notebooks
3. Create an issue on GitHub