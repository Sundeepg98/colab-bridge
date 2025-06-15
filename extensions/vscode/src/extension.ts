import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
    console.log('Claude Tools extension is now active!');

    // Register commands
    const executeFile = vscode.commands.registerCommand('claude-tools.executeInColab', async () => {
        await executeInColab(false);
    });

    const executeSelection = vscode.commands.registerCommand('claude-tools.executeSelectionInColab', async () => {
        await executeInColab(true);
    });

    const openNotebook = vscode.commands.registerCommand('claude-tools.openColabNotebook', async () => {
        await openColabNotebook();
    });

    const configure = vscode.commands.registerCommand('claude-tools.configure', async () => {
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
    const config = vscode.workspace.getConfiguration('claude-tools');
    const pythonPath = config.get<string>('pythonPath', 'python3');
    const timeout = config.get<number>('timeout', 60);
    const showOutput = config.get<boolean>('showOutput', true);

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
                    if (error.message.includes('claude-tools')) {
                        vscode.window.showErrorMessage(
                            'Claude Tools not installed. Run: pip install claude-tools',
                            'Install Guide'
                        ).then(selection => {
                            if (selection === 'Install Guide') {
                                vscode.env.openExternal(vscode.Uri.parse('https://github.com/claude-tools/colab-integration#installation'));
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
                    vscode.window.showInformationMessage('✅ Code executed successfully in Colab!');
                    if (showOutput && content.trim()) {
                        showOutputDocument('Colab Output', content);
                    }
                } else if (status === 'ERROR') {
                    vscode.window.showErrorMessage('❌ Execution failed in Colab');
                    if (content.trim()) {
                        showOutputDocument('Colab Error', content);
                    }
                } else if (status === 'PENDING') {
                    vscode.window.showWarningMessage(
                        'Request queued for Colab processing',
                        'Open Colab'
                    ).then(selection => {
                        if (selection === 'Open Colab') {
                            vscode.commands.executeCommand('claude-tools.openColabNotebook');
                        }
                    });
                } else {
                    vscode.window.showErrorMessage('Unexpected response from Colab integration');
                }

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
        'Open Claude Tools Colab processor?',
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
            description: 'Configure Claude Tools extension settings',
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
        placeHolder: 'Configure Claude Tools Colab Integration'
    });

    if (!selection) return;

    switch (selection.action) {
        case 'settings':
            vscode.commands.executeCommand('workbench.action.openSettings', 'claude-tools');
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
                const config = vscode.workspace.getConfiguration('claude-tools');
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
                const config = vscode.workspace.getConfiguration('claude-tools');
                await config.update('driveFolder', folderId, vscode.ConfigurationTarget.Global);
                vscode.window.showInformationMessage('Drive folder ID updated');
            }
            break;
            
        case 'guide':
            vscode.env.openExternal(vscode.Uri.parse('https://github.com/claude-tools/colab-integration#setup'));
            break;
    }
}

function showWelcomeMessage() {
    vscode.window.showInformationMessage(
        'Welcome to Claude Tools! Execute Python code in Google Colab.',
        'Setup Guide',
        'Try Example'
    ).then(selection => {
        if (selection === 'Setup Guide') {
            vscode.commands.executeCommand('claude-tools.configure');
        } else if (selection === 'Try Example') {
            // Create example file
            vscode.workspace.openTextDocument({
                content: `# Claude Tools Colab Example
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
    console.log('Claude Tools extension deactivated');
}