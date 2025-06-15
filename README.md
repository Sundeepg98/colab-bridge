# 🌉 Colab Bridge

**Universal Google Colab integration for any IDE, coding assistant, or Python tool**

Execute Python code in Google Colab's free GPU environment from any development tool - VS Code, Cursor, PyCharm, or your custom applications.

## 🚀 Features

- **🌍 Universal compatibility** - Works with any IDE or Python tool
- **🔋 Free GPU access** - Leverage Google Colab's free compute resources
- **📚 Pre-installed libraries** - NumPy, PyTorch, TensorFlow, and more
- **🤖 Automated setup** - Zero-click Colab notebook deployment
- **🔧 Multiple interfaces** - CLI, Python API, and IDE extensions
- **📊 Real-time monitoring** - Debug and analyze execution performance

## 📦 Installation

```bash
pip install colab-bridge
```

## 🎯 Quick Start

### Python API
```python
from colab_integration import UniversalColabBridge

# Initialize for your tool
bridge = UniversalColabBridge(tool_name="my_tool")
bridge.initialize()

# Execute code in Colab
result = bridge.execute_code('''
import torch
print(f"GPU available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
''')

print(result['output'])
```

### Command Line
```bash
# Execute code directly
colab-bridge execute --code "print('Hello from Colab!')"

# Execute a Python file
colab-bridge execute --file my_script.py

# Check status
colab-bridge status
```

### IDE Integration
Works with any IDE that can run Python:

**VS Code**:
```python
bridge = UniversalColabBridge(tool_name="vscode")
```

**Cursor**:
```python
bridge = UniversalColabBridge(tool_name="cursor")
```

**PyCharm**:
```python
bridge = UniversalColabBridge(tool_name="pycharm")
```

**Custom Tools**:
```python
bridge = UniversalColabBridge(tool_name="my_custom_tool")
```

## ⚙️ Setup

### 1. Google Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select existing
3. Enable Google Drive API
4. Create service account and download JSON key
5. Share a Google Drive folder with the service account email

### 2. Configure Colab Bridge
```bash
# Interactive setup
colab-bridge setup --interactive

# Or set directly
colab-bridge setup --service-account path/to/service-account.json --folder-id your-drive-folder-id
```

### 3. Start Colab Processor
```bash
# Opens Colab notebook that processes requests
colab-bridge notebook open
```

## 🎭 How It Works

Colab Bridge uses Google Drive as a message queue:

```
Your Tool → Google Drive → Google Colab → Google Drive → Your Tool
```

1. **Your tool** sends code via Python API or CLI
2. **Request file** created in Google Drive
3. **Colab notebook** monitors Drive and executes code
4. **Response file** written back to Drive
5. **Your tool** receives results

## 🔧 Architecture

### Universal Compatibility
```python
# Same interface works for any tool
bridge = UniversalColabBridge(tool_name="any_tool_name")
result = bridge.execute_code(python_code)
```

### File-Based Protocol
- `command_*.json` - Your code execution requests
- `result_*.json` - Colab execution responses
- Automatic cleanup and error handling

### Multiple Notebook Options
1. **Auto-Processor** - Fully automated execution
2. **Interactive Debug** - Step-by-step debugging
3. **Hybrid** - Auto-run with debug capabilities

## 📊 Use Cases

### 🧠 AI/ML Development
```python
bridge = UniversalColabBridge(tool_name="ml_research")
result = bridge.execute_code('''
import torch
import torch.nn as nn

# Train models with free GPU
model = nn.Linear(784, 10).cuda()
print(f"Model on GPU: {next(model.parameters()).is_cuda}")
''')
```

### 📈 Data Science
```python
bridge = UniversalColabBridge(tool_name="data_analysis")
result = bridge.execute_code('''
import pandas as pd
import matplotlib.pyplot as plt

# Process large datasets
df = pd.read_csv('large_dataset.csv')
plt.figure(figsize=(10, 6))
df.plot()
plt.savefig('analysis.png')
''')
```

### 🔬 Research & Prototyping
```python
bridge = UniversalColabBridge(tool_name="research")
result = bridge.execute_code('''
# Test algorithms with powerful compute
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Large-scale experiments
X = np.random.rand(100000, 50)
y = np.random.randint(0, 2, 100000)
clf = RandomForestClassifier(n_estimators=1000)
clf.fit(X, y)
''')
```

## 🛠️ IDE Extensions

### VS Code Extension
Coming soon! Will provide:
- Right-click "Execute in Colab"
- Keyboard shortcuts
- Output panel integration
- Settings management

### Other IDEs
The Python API works with any IDE:
- **Cursor** - Full support
- **PyCharm** - Full support  
- **Sublime Text** - Via Python integration
- **Vim/Neovim** - Via Python plugins
- **Emacs** - Via Python integration

## 🎯 Configuration

### Environment Variables
```bash
export SERVICE_ACCOUNT_PATH="/path/to/service-account.json"
export GOOGLE_DRIVE_FOLDER_ID="your-folder-id"
```

### Config File
`~/.colab-bridge/config.json`:
```json
{
  "service_account_path": "/path/to/service-account.json",
  "google_drive_folder_id": "your-folder-id"
}
```

## 📋 Commands

```bash
# Execute code
colab-bridge execute --code "print('Hello')"
colab-bridge execute --file script.py --tool vscode

# Setup and configuration  
colab-bridge setup --interactive
colab-bridge status

# Notebook management
colab-bridge notebook open
colab-bridge notebook upload
colab-bridge notebook list
```

## 🔍 Debugging

### Monitor Execution
```python
bridge = UniversalColabBridge(tool_name="debug", debug=True)
result = bridge.execute_code(code)  # Shows detailed logs
```

### Check Status
```bash
colab-bridge status  # Shows connection and pending requests
```

### View Files
Check your Google Drive folder for:
- `command_*.json` - Pending requests
- `result_*.json` - Execution results

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙋 Support

- **Issues**: [GitHub Issues](https://github.com/sundeepg98/colab-bridge/issues)
- **Documentation**: [GitHub Wiki](https://github.com/sundeepg98/colab-bridge/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/sundeepg98/colab-bridge/discussions)

## 🎉 Why Colab Bridge?

**Before**: Limited to your local machine's resources
**After**: Free access to Google's GPUs and ML libraries from any tool

Transform any IDE into a powerful ML development environment! 🚀