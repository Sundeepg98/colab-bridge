#!/bin/bash
# Setup script for Google Cloud Shell

echo "🚀 Setting up Colab Bridge in Cloud Shell"
echo "========================================"

# Install dependencies
echo "1️⃣ Installing Python dependencies..."
pip install -e .
pip install playwright

echo "2️⃣ Installing Playwright browsers..."
playwright install chromium
playwright install-deps

echo "3️⃣ Installing code-server..."
curl -fsSL https://code-server.dev/install.sh | sh

echo "4️⃣ Creating Python wrapper..."
mkdir -p ~/bin
cat > ~/bin/python3-colab << 'EOF'
#!/bin/bash
# You'll need to update these with your actual values
export SERVICE_ACCOUNT_PATH="$HOME/service-account.json"
export GOOGLE_DRIVE_FOLDER_ID="your-folder-id-here"
/usr/bin/python3 "$@"
EOF
chmod +x ~/bin/python3-colab

echo "5️⃣ Creating VS Code settings..."
mkdir -p ~/.config/Code/User
cat > ~/.config/Code/User/settings.json << 'EOF'
{
  "colab-bridge.pythonPath": "~/bin/python3-colab",
  "colab-bridge.serviceAccountPath": "~/service-account.json",
  "colab-bridge.driveFolder": "your-folder-id-here",
  "colab-bridge.timeout": 60,
  "colab-bridge.showOutput": true
}
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Upload your service account JSON to ~/service-account.json"
echo "2. Update the folder ID in ~/bin/python3-colab"
echo "3. Update the folder ID in ~/.config/Code/User/settings.json"
echo "4. Start code-server: code-server --bind-addr 0.0.0.0:8080"
echo "5. Click on the Web Preview button in Cloud Shell"
echo ""
echo "🧪 To run tests:"
echo "   cd test_examples"
echo "   python3 playwright_final_test.py"