# Testing Claude Tools with Your Credentials

## Quick Setup

### 1. Add Your Service Account File

Place your Google service account JSON file somewhere secure, for example:
```bash
# Option 1: In your home directory
~/keys/my-service-account.json

# Option 2: In the project (but don't commit it!)
/var/projects/claude-tools/config/service-account.json
```

### 2. Create .env File

```bash
cd /var/projects/claude-tools
cp config/.env.template .env
```

Edit `.env` with your actual values:
```env
SERVICE_ACCOUNT_PATH=/path/to/your/service-account.json
GOOGLE_DRIVE_FOLDER_ID=your-folder-id-here
ANTHROPIC_API_KEY=your-anthropic-key (optional)
OPENAI_API_KEY=your-openai-key (optional)
```

### 3. Test the Connection

```bash
# Test basic setup
python3 scripts/test_basic.py

# Test full structure
python3 scripts/test_structure.py
```

## Full Integration Test

### Step 1: Start Colab Processor

1. Open Google Colab
2. Upload `notebooks/basic-integration.ipynb`
3. Run all cells - this starts the processor

### Step 2: Test from Claude Tools

Create a test script `test_integration.py`:

```python
from colab_integration.bridge import ClaudeColabBridge

# Initialize
bridge = ClaudeColabBridge()
bridge.initialize()

# Test 1: Simple code execution
result = bridge.execute_code('''
print("Hello from Colab!")
import sys
print(f"Python version: {sys.version}")
''')
print("Test 1 Result:", result)

# Test 2: Install package
result = bridge.execute_code('''
!pip install numpy
import numpy as np
print(f"NumPy version: {np.__version__}")
''')
print("Test 2 Result:", result)

# Test 3: GPU check
result = bridge.execute_code('''
import tensorflow as tf
print("GPU Available:", tf.config.list_physical_devices('GPU'))
''')
print("Test 3 Result:", result)
```

## Expected Results

If everything is working:
- ✅ "Google Drive connection successful"
- ✅ Code executes in Colab
- ✅ Results return to Claude Tools
- ✅ Multi-instance support works

## Troubleshooting

### "No such file or directory: service-account.json"
- Check the path in .env is absolute, not relative
- Ensure the file exists at that location

### "Google Drive connection failed"
- Verify service account has access to the folder
- Check folder ID is correct (from the URL)
- Ensure Drive API is enabled

### "Command timeout"
- Make sure Colab notebook is running
- Check internet connection
- Increase timeout in config

## Security Reminder

⚠️ **Never commit these files:**
- Your service account JSON
- .env with real credentials
- Any file with API keys

Use the security scanner before sharing:
```bash
./scripts/prepare-for-public.sh
```