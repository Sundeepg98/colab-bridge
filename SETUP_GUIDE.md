# 🚀 Colab Bridge - Setup Guide

## 📁 Organized Project Structure

```
colab-bridge/
├── 🔐 credentials/          # Service account JSON files (private)
├── ⚙️ config/              # Configuration files
├── 📊 data/                # Runtime data and cache
├── 📓 notebooks/           # Colab processor notebooks
├── 🐍 colab_integration/   # Core Python package
├── 🔌 extensions/          # IDE extensions
├── 🧪 tests/               # Test scripts
└── 📚 docs/                # Documentation
```

## 🔧 Quick Setup

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Setup Credentials**
```bash
# Place your service account JSON in credentials/
cp your-service-account.json credentials/

# Create configuration
cp config/.env.template config/.env
# Edit config/.env with your values
```

### 3. **Configure Environment**
Edit `config/.env`:
```bash
SERVICE_ACCOUNT_PATH=./credentials/your-service-account.json
GOOGLE_DRIVE_FOLDER_ID=your-google-drive-folder-id
```

### 4. **Test Installation**
```bash
python3 -c "from colab_integration import UniversalColabBridge; print('✅ Ready!')"
```

### 5. **Start Colab Processor**
Upload `notebooks/hybrid-processor.ipynb` to Google Colab and run it.

## 🎯 Usage Examples

### Python API
```python
from colab_integration import UniversalColabBridge

bridge = UniversalColabBridge(tool_name="my_tool")
bridge.initialize()

result = bridge.execute_code("print('Hello from Colab!')")
print(result['output'])
```

### Command Line
```bash
python3 -m colab_integration.cli execute --code "print('Hello CLI!')"
```

## 🔒 Security Features

- ✅ **Credentials isolated** in `credentials/` directory
- ✅ **Auto-gitignored** sensitive files
- ✅ **Template configs** for safe sharing
- ✅ **Structured logging** in `logs/`
- ✅ **Temporary data** auto-cleanup

## 📊 Directory Functions

| Directory | Purpose | Gitignored |
|-----------|---------|------------|
| `credentials/` | Service accounts & API keys | ✅ |
| `config/` | Configuration files | Partial |
| `data/` | Runtime data & cache | ✅ |
| `logs/` | Application logs | ✅ |
| `temp/` | Temporary files | ✅ |
| `notebooks/` | Colab processors | ❌ |
| `colab_integration/` | Core package | ❌ |

## 🧪 Testing

```bash
# Test core functionality
python3 -c "from colab_integration import UniversalColabBridge; print('✅ Import works')"

# Test with actual Colab (needs setup)
python3 visual_demo.py
```

## 🎉 Ready to Use!

Your Colab Bridge is now properly organized and secure:
- Credentials safely isolated
- Clean separation of concerns  
- Ready for IDE integration
- Scalable architecture