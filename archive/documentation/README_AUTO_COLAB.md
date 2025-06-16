# Claude Tools - Automated Colab Integration

## 🚀 One-Click Setup

```bash
python3 start_colab.py
```

This automatically:
1. Creates a self-running Colab notebook
2. Uploads it to your Google Drive
3. Opens it in your browser (if available)
4. The notebook auto-processes Claude Tools requests

## 📝 What You Need to Do

After running `start_colab.py`:
1. The Colab URL is displayed (and opened if browser available)
2. In Colab, click **"Run all"** (or press Ctrl+F9)
3. Allow Google Drive access when prompted
4. That's it! The notebook runs for 1 hour automatically

## 🧪 Testing

Once Colab is running:
```bash
python3 test_colab_integration.py
```

Or in Python:
```python
from colab_integration.bridge import ClaudeColabBridge

bridge = ClaudeColabBridge()
bridge.initialize()

result = bridge.execute_code('''
    import torch
    print(f"GPU: {torch.cuda.get_device_name(0)}")
''')

print(result['output'])
```

## 🤖 How It Works

1. **Auto-Processor Notebook**: Created with all processing logic embedded
2. **Form Cells**: Uses Colab's form view for cleaner interface
3. **Auto-Run Loop**: Processes requests for 1 hour (configurable)
4. **Drive Integration**: Uses your Google Drive for communication

## 📋 Created Files

- `notebooks/auto-processor.ipynb` - The automated Colab notebook
- `colab_integration/auto_colab.py` - Automation manager
- `start_colab.py` - One-click starter script

## 🔄 Features

- **No manual upload needed** - Notebook uploaded automatically
- **Self-contained** - All code embedded in notebook
- **Auto-processing** - Starts processing immediately
- **1-hour runtime** - Runs continuously (Colab free tier limit)
- **GPU support** - Automatically uses GPU if available

## 🛠️ Advanced Usage

For custom automation:
```python
from colab_integration.auto_colab import AutoColabManager

manager = AutoColabManager(
    service_account_path="path/to/service-account.json",
    drive_folder_id="your-folder-id"
)

manager.initialize()
result = manager.start_colab_session(open_browser=True)
print(f"Colab URL: {result['colab_url']}")
```

## 📊 Your Colab Notebook

The auto-generated notebook is now at:
**https://colab.research.google.com/drive/1X9EaHlau2jZPoQVhCyjk7x8FOvNINeNh**

This notebook will automatically process Claude Tools requests once you run it!