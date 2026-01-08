#!/bin/bash
# Script to rebuild the VS Code extension in test folder

echo "🔨 Rebuilding VS Code extension..."

# Navigate to test extension
cd /home/sundeep/projects/colab-bridge-test/extensions/vscode

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Compile the extension
echo "🏗️ Compiling extension..."
npm run compile

echo "✅ Extension rebuilt!"
echo ""
echo "📝 To use the updated extension:"
echo "1. In VS Code: Press Ctrl+Shift+P (or Cmd+Shift+P on Mac)"
echo "2. Run 'Developer: Reload Window'"
echo "3. Try your matplotlib code again"
echo ""
echo "You should now see actual plot images instead of just text! 🎨"