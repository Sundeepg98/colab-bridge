import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

let statusBar: vscode.StatusBarItem;

export function activate(context: vscode.ExtensionContext) {
    console.log('Colab Bridge extension is now active!');

    // Create status bar item
    statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = "$(cloud) Colab GPU";
    statusBar.tooltip = "Click to execute current file in Colab";
    statusBar.command = 'colab-bridge.executeInColab';
    statusBar.backgroundColor = undefined;
    statusBar.show();
    context.subscriptions.push(statusBar);

    // Register commands
    const executeFile = vscode.commands.registerCommand('colab-bridge.executeInColab', async () => {
        await executeInColab(false);
    });

    const executeSelection = vscode.commands.registerCommand('colab-bridge.executeSelectionInColab', async () => {
        await executeInColab(true);
    });

    const openNotebook = vscode.commands.registerCommand('colab-bridge.openColabNotebook', async () => {
        await openColabNotebook();
    });

    const configure = vscode.commands.registerCommand('colab-bridge.configure', async () => {
        await configureIntegration();
    });

    context.subscriptions.push(executeFile, executeSelection, openNotebook, configure);

    // Show welcome message on first activation
    const hasShownWelcome = context.globalState.get('hasShownWelcome', false);
    if (!hasShownWelcome) {
        showWelcomeMessage();
        context.globalState.update('hasShownWelcome', true);
    }
}

async function executeInColab(selectionOnly: boolean) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found');
        return;
    }

    // Get code to execute
    let code: string;
    if (selectionOnly) {
        const selection = editor.selection;
        if (selection.isEmpty) {
            vscode.window.showWarningMessage('No text selected');
            return;
        }
        code = editor.document.getText(selection);
    } else {
        code = editor.document.getText();
    }

    if (!code.trim()) {
        vscode.window.showWarningMessage('No code to execute');
        return;
    }

    // Check configuration
    const config = vscode.workspace.getConfiguration('colab-bridge');
    const pythonPath = config.get<string>('pythonPath', 'python3');
    const timeout = config.get<number>('timeout', 60);
    const showOutput = config.get<boolean>('showOutput', true);

    // Update status bar to show executing
    statusBar.text = "$(sync~spin) Colab...";
    statusBar.tooltip = "Executing in Google Colab...";
    
    // Show progress
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Executing in Google Colab...",
        cancellable: true
    }, async (progress, token) => {
        return new Promise<void>((resolve, reject) => {
            progress.report({ message: "Sending code to Colab..." });

            // Escape code for shell
            const escapedCode = code.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/`/g, '\\`');
            
            // Create Python command
            const pythonCommand = `
from colab_integration.universal_bridge import UniversalColabBridge
import sys

try:
    bridge = UniversalColabBridge(tool_name='vscode')
    bridge.initialize()
    
    code = """${escapedCode}"""
    result = bridge.execute_code(code, timeout=${timeout})
    
    if result.get('status') == 'success':
        print('SUCCESS')
        print('---OUTPUT---')
        print(result.get('output', ''))
        print('---END---')
    elif result.get('status') == 'error':
        print('ERROR')
        print('---ERROR---')
        print(result.get('error', 'Unknown error'))
        print('---END---')
    else:
        print('PENDING')
        print('---INFO---')
        print(f"Request queued: {result.get('request_id', 'unknown')}")
        print('Make sure Colab notebook is running!')
        print('---END---')
        
except Exception as e:
    print('EXCEPTION')
    print('---ERROR---')
    print(f"Failed to execute: {str(e)}")
    print('---END---')
`;

            // Execute command
            const child = exec(`${pythonPath} -c "${pythonCommand}"`, {
                timeout: (timeout + 10) * 1000 // Add buffer to timeout
            }, (error, stdout, stderr) => {
                if (token.isCancellationRequested) {
                    resolve();
                    return;
                }

                if (error) {
                    if (error.message.includes('colab_integration')) {
                        vscode.window.showErrorMessage(
                            'Colab Bridge not installed. Run: pip install -e /var/projects/colab-bridge',
                            'Install Guide'
                        ).then(selection => {
                            if (selection === 'Install Guide') {
                                vscode.env.openExternal(vscode.Uri.parse('https://github.com/colab-bridge/colab-integration#installation'));
                            }
                        });
                    } else {
                        vscode.window.showErrorMessage(`Execution failed: ${error.message}`);
                    }
                    resolve();
                    return;
                }

                // Parse output
                const output = stdout.toString();
                const lines = output.split('\n');
                const status = lines[0];

                let content = '';
                let startCapture = false;
                
                for (const line of lines) {
                    if (line === '---OUTPUT---' || line === '---ERROR---' || line === '---INFO---') {
                        startCapture = true;
                        continue;
                    }
                    if (line === '---END---') {
                        break;
                    }
                    if (startCapture) {
                        content += line + '\n';
                    }
                }

                // Show results
                if (status === 'SUCCESS') {
                    statusBar.text = "$(check) Colab GPU";
                    statusBar.tooltip = "Last execution: Success";
                    vscode.window.showInformationMessage('✅ Code executed successfully in Colab!');
                    if (showOutput && content.trim()) {
                        showOutputDocument('Colab Output', content);
                    }
                } else if (status === 'ERROR') {
                    statusBar.text = "$(error) Colab GPU";
                    statusBar.tooltip = "Last execution: Failed";
                    vscode.window.showErrorMessage('❌ Execution failed in Colab');
                    if (content.trim()) {
                        showOutputDocument('Colab Error', content);
                    }
                } else if (status === 'PENDING') {
                    statusBar.text = "$(warning) Colab GPU";
                    statusBar.tooltip = "Colab notebook not running";
                    vscode.window.showWarningMessage(
                        'Request queued for Colab processing',
                        'Open Colab'
                    ).then(selection => {
                        if (selection === 'Open Colab') {
                            vscode.commands.executeCommand('colab-bridge.openColabNotebook');
                        }
                    });
                } else {
                    statusBar.text = "$(cloud) Colab GPU";
                    statusBar.tooltip = "Click to execute current file in Colab";
                    vscode.window.showErrorMessage('Unexpected response from Colab integration');
                }

                // Reset status bar after a delay
                setTimeout(() => {
                    statusBar.text = "$(cloud) Colab GPU";
                    statusBar.tooltip = "Click to execute current file in Colab";
                }, 5000);

                resolve();
            });

            // Handle cancellation
            token.onCancellationRequested(() => {
                child.kill();
                vscode.window.showInformationMessage('Colab execution cancelled');
                resolve();
            });
        });
    });
}

async function showOutputDocument(title: string, content: string) {
    const doc = await vscode.workspace.openTextDocument({
        content: content,
        language: 'text'
    });
    
    await vscode.window.showTextDocument(doc, {
        viewColumn: vscode.ViewColumn.Beside,
        preview: false
    });
}

async function openColabNotebook() {
    const notebookUrl = 'https://colab.research.google.com/drive/1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA';
    
    const action = await vscode.window.showInformationMessage(
        'Open Colab Bridge processor?',
        'Open in Browser',
        'Copy URL'
    );

    if (action === 'Open in Browser') {
        vscode.env.openExternal(vscode.Uri.parse(notebookUrl));
    } else if (action === 'Copy URL') {
        vscode.env.clipboard.writeText(notebookUrl);
        vscode.window.showInformationMessage('Colab URL copied to clipboard');
    }
}

async function configureIntegration() {
    const items = [
        {
            label: '$(gear) Open Settings',
            description: 'Configure Colab Bridge extension settings',
            action: 'settings'
        },
        {
            label: '$(file) Set Service Account',
            description: 'Select Google service account JSON file',
            action: 'serviceAccount'
        },
        {
            label: '$(folder) Set Drive Folder',
            description: 'Configure Google Drive folder ID',
            action: 'driveFolder'
        },
        {
            label: '$(link-external) Setup Guide',
            description: 'Open installation and setup guide',
            action: 'guide'
        }
    ];

    const selection = await vscode.window.showQuickPick(items, {
        placeHolder: 'Configure Colab Bridge Integration'
    });

    if (!selection) return;

    switch (selection.action) {
        case 'settings':
            vscode.commands.executeCommand('workbench.action.openSettings', 'colab-bridge');
            break;
            
        case 'serviceAccount':
            const fileUri = await vscode.window.showOpenDialog({
                canSelectFiles: true,
                canSelectFolders: false,
                canSelectMany: false,
                filters: {
                    'JSON Files': ['json']
                },
                openLabel: 'Select Service Account File'
            });
            
            if (fileUri && fileUri[0]) {
                const config = vscode.workspace.getConfiguration('colab-bridge');
                await config.update('serviceAccountPath', fileUri[0].fsPath, vscode.ConfigurationTarget.Global);
                vscode.window.showInformationMessage('Service account path updated');
            }
            break;
            
        case 'driveFolder':
            const folderId = await vscode.window.showInputBox({
                prompt: 'Enter Google Drive folder ID',
                placeHolder: '1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z',
                validateInput: (value) => {
                    if (!value || value.length < 10) {
                        return 'Please enter a valid Google Drive folder ID';
                    }
                    return null;
                }
            });
            
            if (folderId) {
                const config = vscode.workspace.getConfiguration('colab-bridge');
                await config.update('driveFolder', folderId, vscode.ConfigurationTarget.Global);
                vscode.window.showInformationMessage('Drive folder ID updated');
            }
            break;
            
        case 'guide':
            vscode.env.openExternal(vscode.Uri.parse('https://github.com/colab-bridge/colab-integration#setup'));
            break;
    }
}

function showWelcomeMessage() {
    vscode.window.showInformationMessage(
        'Welcome to Colab Bridge! Execute Python code in Google Colab.',
        'Setup Guide',
        'Try Example'
    ).then(selection => {
        if (selection === 'Setup Guide') {
            vscode.commands.executeCommand('colab-bridge.configure');
        } else if (selection === 'Try Example') {
            // Create example file
            vscode.workspace.openTextDocument({
                content: `# Colab Bridge Example
print("Hello from Google Colab!")

import datetime
print(f"Executed at: {datetime.datetime.now()}")

# Try some computation
import math
result = math.sqrt(16) + math.pi
print(f"sqrt(16) + π = {result:.4f}")

# Test data science libraries (if available in Colab)
try:
    import numpy as np
    arr = np.random.rand(5)
    print(f"Random array: {arr}")
except ImportError:
    print("NumPy not available")

print("✅ Example completed!")`,
                language: 'python'
            }).then(doc => {
                vscode.window.showTextDocument(doc);
                vscode.window.showInformationMessage(
                    'Select code and press Ctrl+Shift+C to execute in Colab!'
                );
            });
        }
    });
}

export function deactivate() {
    console.log('Colab Bridge extension deactivated');
}