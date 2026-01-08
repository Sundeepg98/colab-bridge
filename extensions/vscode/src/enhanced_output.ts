import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';

export interface Visualization {
    type: string;
    data: string;  // base64 encoded
}

export interface EnhancedResult {
    status: string;
    output?: string;
    error?: string;
    visualizations?: Visualization[];
    output_type?: 'text' | 'rich';
}

export async function showEnhancedOutput(result: EnhancedResult) {
    if (!result.visualizations || result.visualizations.length === 0) {
        // No visualizations, show text output
        if (result.output && result.output.trim()) {
            const doc = await vscode.workspace.openTextDocument({
                content: result.output,
                language: 'text'
            });
            await vscode.window.showTextDocument(doc, {
                viewColumn: vscode.ViewColumn.Beside,
                preview: false
            });
        }
        return;
    }

    // Create HTML output with embedded images
    const html = createHtmlOutput(result);
    
    // Create webview panel
    const panel = vscode.window.createWebviewPanel(
        'colabOutput',
        'Colab Output',
        vscode.ViewColumn.Beside,
        {
            enableScripts: true,
            retainContextWhenHidden: true
        }
    );

    panel.webview.html = html;
}

function createHtmlOutput(result: EnhancedResult): string {
    let html = `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
            padding: 10px;
            line-height: 1.6;
        }
        pre {
            background-color: var(--vscode-textBlockQuote-background);
            border: 1px solid var(--vscode-widget-border);
            border-radius: 4px;
            padding: 10px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px 0;
            border: 1px solid var(--vscode-widget-border);
            border-radius: 4px;
        }
        .section {
            margin: 15px 0;
        }
        .section-title {
            font-weight: bold;
            color: var(--vscode-textLink-foreground);
            margin-bottom: 5px;
        }
        .error {
            color: var(--vscode-errorForeground);
        }
    </style>
</head>
<body>`;

    // Add text output if present
    if (result.output && result.output.trim()) {
        html += `
    <div class="section">
        <div class="section-title">Text Output:</div>
        <pre>${escapeHtml(result.output)}</pre>
    </div>`;
    }

    // Add visualizations
    if (result.visualizations && result.visualizations.length > 0) {
        html += `
    <div class="section">
        <div class="section-title">Visualizations:</div>`;
        
        result.visualizations.forEach((viz, index) => {
            if (viz.type === 'image/png') {
                html += `
        <img src="data:image/png;base64,${viz.data}" alt="Plot ${index + 1}">`;
            }
        });
        
        html += `
    </div>`;
    }

    // Add error if present
    if (result.error) {
        html += `
    <div class="section error">
        <div class="section-title">Error:</div>
        <pre>${escapeHtml(result.error)}</pre>
    </div>`;
    }

    html += `
</body>
</html>`;

    return html;
}

function escapeHtml(text: string): string {
    const map: { [key: string]: string } = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Also export a function to save plots to files
export async function savePlotsToFiles(result: EnhancedResult): Promise<string[]> {
    const savedFiles: string[] = [];
    
    if (!result.visualizations || result.visualizations.length === 0) {
        return savedFiles;
    }

    // Create temp directory for plots
    const tempDir = path.join(os.tmpdir(), `colab_plots_${Date.now()}`);
    if (!fs.existsSync(tempDir)) {
        fs.mkdirSync(tempDir, { recursive: true });
    }

    // Save each visualization
    result.visualizations.forEach((viz, index) => {
        if (viz.type === 'image/png') {
            const filename = path.join(tempDir, `plot_${index + 1}.png`);
            const buffer = Buffer.from(viz.data, 'base64');
            fs.writeFileSync(filename, buffer);
            savedFiles.push(filename);
        }
    });

    if (savedFiles.length > 0) {
        vscode.window.showInformationMessage(
            `Saved ${savedFiles.length} plot(s) to ${tempDir}`,
            'Open Folder'
        ).then(selection => {
            if (selection === 'Open Folder') {
                vscode.env.openExternal(vscode.Uri.file(tempDir));
            }
        });
    }

    return savedFiles;
}