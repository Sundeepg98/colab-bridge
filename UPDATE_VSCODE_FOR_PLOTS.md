# VS Code Extension Update for Plot Display

## The Issue
The VS Code extension currently only displays text output, even when the enhanced processor captures matplotlib plots. The extension needs to be updated to use the `showEnhancedOutput` function when visualizations are present.

## Required Changes

### 1. Update the Python command in extension.ts (around line 119)
Change from:
```python
result = bridge.execute_code(code, timeout=${timeout})
```

To:
```python
result = bridge.execute_code(code, timeout=${timeout}, return_format='dict')
```

### 2. Update result handling (around line 121)
Change from:
```typescript
if (result.get('status') == 'success'):
    print('SUCCESS')
    print('---OUTPUT---')
    print(result.get('output', ''))
    print('---END---')
```

To:
```typescript
if result.get('status') == 'success':
    print('SUCCESS')
    print('---OUTPUT---')
    import json
    print(json.dumps(result))
    print('---END---')
```

### 3. Update the result parsing in VS Code (around line 214)
Change from:
```typescript
if (status === 'SUCCESS') {
    statusBar.text = "$(check) Colab GPU";
    statusBar.tooltip = "Last execution: Success";
    vscode.window.showInformationMessage('✅ Execution completed!');
    if (showOutput && content.trim()) {
        showOutputDocument('Colab Output', content);
    }
}
```

To:
```typescript
if (status === 'SUCCESS') {
    statusBar.text = "$(check) Colab GPU";
    statusBar.tooltip = "Last execution: Success";
    vscode.window.showInformationMessage('✅ Execution completed!');
    if (showOutput && content.trim()) {
        try {
            const result = JSON.parse(content) as EnhancedResult;
            if (result.visualizations && result.visualizations.length > 0) {
                // Use enhanced output for plots
                showEnhancedOutput(result);
            } else {
                // Use regular text output
                showOutputDocument('Colab Output', result.output || content);
            }
        } catch (e) {
            // Fallback to text output if not JSON
            showOutputDocument('Colab Output', content);
        }
    }
}
```

### 4. Do the same for the polling result handler (around line 442)

## Testing
After making these changes:
1. Rebuild the extension
2. Run matplotlib code from VS Code
3. You should see plots displayed in a webview panel!