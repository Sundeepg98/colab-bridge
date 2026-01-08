# VS Code Extension Debug Guide

## The Issue
- Plots ARE being captured by the enhanced processor ✅
- Results ARE being returned with visualizations ✅
- But VS Code is NOT displaying them ❌

## Debug Steps

### 1. Check if JSON is being parsed
In VS Code, after running matplotlib code:
1. Open Developer Console: `Ctrl+Shift+I` (or `Cmd+Shift+I` on Mac)
2. Go to Console tab
3. Type and run:
```javascript
// This will show what the extension received
console.log(require('./out/extension').lastResult)
```

### 2. Force reload the extension
1. Press `Ctrl+Shift+P`
2. Type: "Developer: Reload Window"
3. Try matplotlib code again

### 3. Check extension version
Make sure you're using the extension from:
`/home/sundeep/projects/colab-bridge-test/extensions/vscode`

Not from: `/var/projects/colab-bridge/extensions/vscode`

### 4. Manual test in VS Code
Open a new file and run exactly this:
```python
import matplotlib.pyplot as plt
plt.plot([1,2,3], [4,5,6])
plt.title("Debug Test")
print("If no plot appears below, check console")
```

### 5. Check Output Panel
View → Output → Select "Colab Bridge"
Look for this line:
`[Colab Bridge] Showing enhanced output with X visualization(s)`

If you see this line, the extension detected plots but failed to display them.

## Possible Issues

### A. Old extension cached
Solution: Delete and reinstall
```bash
cd /home/sundeep/projects/colab-bridge-test/extensions/vscode
rm -rf out/
npx tsc -p .
```

### B. Webview blocked
Some VS Code settings block webviews. Check:
- File → Preferences → Settings
- Search for "webview"
- Make sure nothing is disabled

### C. Extension not activated
Check if extension is active:
- View → Extensions
- Search for "Colab Bridge"
- Make sure it's enabled

## What You Should See
When working correctly:
1. Your code runs
2. A new panel opens on the right
3. The panel shows:
   - Text output at the top
   - Plot images below

## Last Resort
If nothing works, the plots ARE captured. You can manually extract them:
1. Look in Google Drive folder for result files
2. Download the JSON
3. Use online base64 to image converter
4. Paste the "data" field from visualizations