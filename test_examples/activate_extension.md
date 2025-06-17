# How to Activate Colab Bridge Extension

The extension `sundeepg.colab-bridge` is installed. To activate it:

## Method 1: Command Palette
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: "Colab"
3. Look for commands like:
   - "Colab Bridge: Connect"
   - "Colab Bridge: Execute in Colab"
   - "Colab Bridge: Configure"

## Method 2: Run Python File
1. Open `test_gpu.py` in VS Code
2. Right-click in the editor
3. Look for "Execute in Colab" option

## Method 3: Keyboard Shortcut
1. Open a Python file
2. Select some code
3. Press `Ctrl+Shift+C` to execute selection in Colab

## Method 4: Terminal Override
If the extension has terminal integration:
1. Open terminal (`Ctrl+``)
2. Run: `python test_gpu.py`
3. The extension should intercept and run on Colab

## Quick Test
In the VS Code terminal, run:
```bash
python -c "import sys; print(sys.executable)"
```

If it shows a Colab path, the extension is working.
If it shows local path, try the activation methods above.