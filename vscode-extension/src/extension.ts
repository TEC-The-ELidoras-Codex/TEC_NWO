import * as vscode from 'vscode';
import axios from 'axios';
import { WebSocket } from 'ws';

interface TECServerConfig {
    serverUrl: string;
    serverMode: 'mcp' | 'flask';
    autoConnect: boolean;
    enableHybridIntelligence: boolean;
    axiomValidationLevel: 'strict' | 'moderate' | 'lenient';
}

interface MCPResponse {
    success: boolean;
    result?: any;
    error?: string;
    processing_time?: number;
}

interface AxiomValidationResult {
    valid: boolean;
    axiom_scores: { [key: string]: number };
    violations: string[];
    confidence_score: number;
}

interface MemoryQueryResult {
    fragments: any[];
    total_matches: number;
    query_time: number;
}

class TECMCPClient {
    private config: TECServerConfig;
    private connected: boolean = false;
    private websocket?: WebSocket;
    private statusBarItem: vscode.StatusBarItem;
    
    constructor(private context: vscode.ExtensionContext) {
        this.config = this.loadConfig();
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right, 
            100
        );
        this.statusBarItem.command = 'tec.serverStatus';
        this.updateStatusBar();
        this.statusBarItem.show();
        
        if (this.config.autoConnect) {
            this.connectToServer();
        }
    }
    
    private loadConfig(): TECServerConfig {
        const config = vscode.workspace.getConfiguration('tec');
        return {
            serverUrl: config.get('serverUrl', 'http://localhost:8000'),
            serverMode: config.get('serverMode', 'mcp'),
            autoConnect: config.get('autoConnect', true),
            enableHybridIntelligence: config.get('enableHybridIntelligence', true),
            axiomValidationLevel: config.get('axiomValidationLevel', 'moderate')
        };
    }
    
    private updateStatusBar() {
        if (this.connected) {
            this.statusBarItem.text = "$(check) TEC Connected";
            this.statusBarItem.backgroundColor = undefined;
        } else {
            this.statusBarItem.text = "$(x) TEC Disconnected";
            this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
        }
    }
    
    async connectToServer(): Promise<boolean> {
        try {
            const response = await axios.get(`${this.config.serverUrl}/health`, {
                timeout: 5000
            });
            
            if (response.data.status === 'operational') {
                this.connected = true;
                this.updateStatusBar();
                vscode.commands.executeCommand('setContext', 'tec.serverConnected', true);
                
                vscode.window.showInformationMessage(
                    `🏛️ Connected to TEC Asimov Engine (${response.data.mode})`
                );
                
                // Setup WebSocket for real-time updates if available
                if (this.config.serverMode === 'mcp') {
                    this.setupWebSocket();
                }
                
                return true;
            }
        } catch (error) {
            this.connected = false;
            this.updateStatusBar();
            vscode.commands.executeCommand('setContext', 'tec.serverConnected', false);
            
            vscode.window.showErrorMessage(
                `Failed to connect to TEC server: ${error}`
            );
        }
        
        return false;
    }
    
    private setupWebSocket() {
        try {
            const wsUrl = this.config.serverUrl.replace('http', 'ws') + '/ws';
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.on('open', () => {
                console.log('TEC WebSocket connected');
            });
            
            this.websocket.on('message', (data) => {
                try {
                    const message = JSON.parse(data.toString());
                    this.handleServerMessage(message);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            });
            
            this.websocket.on('close', () => {
                console.log('TEC WebSocket disconnected');
                this.websocket = undefined;
            });
            
        } catch (error) {
            console.error('WebSocket setup failed:', error);
        }
    }
    
    private handleServerMessage(message: any) {
        if (message.type === 'memory_update') {
            vscode.window.showInformationMessage(
                `📚 Memory Core Updated: ${message.fragments_added} new fragments`
            );
        } else if (message.type === 'axiom_violation') {
            vscode.window.showWarningMessage(
                `⚠️ Axiom Violation Detected: ${message.axiom}`
            );
        }
    }
    
    async validateAxioms(content: string, contentType: string = 'narrative'): Promise<AxiomValidationResult | null> {
        if (!this.connected) {
            vscode.window.showErrorMessage('Not connected to TEC server');
            return null;
        }
        
        try {
            const response = await axios.post(`${this.config.serverUrl}/validate_axioms`, {
                content,
                content_type: contentType,
                validation_level: this.config.axiomValidationLevel
            });
            
            const result = response.data as MCPResponse;
            if (result.success) {
                return result.result as AxiomValidationResult;
            } else {
                vscode.window.showErrorMessage(`Axiom validation failed: ${result.error}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Request failed: ${error}`);
        }
        
        return null;
    }
    
    async queryMemory(query: string, limit: number = 10): Promise<MemoryQueryResult | null> {
        if (!this.connected) {
            vscode.window.showErrorMessage('Not connected to TEC server');
            return null;
        }
        
        try {
            const response = await axios.post(`${this.config.serverUrl}/query_memory`, {
                query,
                limit,
                include_metadata: true
            });
            
            const result = response.data as MCPResponse;
            if (result.success) {
                return result.result as MemoryQueryResult;
            } else {
                vscode.window.showErrorMessage(`Memory query failed: ${result.error}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Request failed: ${error}`);
        }
        
        return null;
    }
    
    async processAsset(filePath: string): Promise<any> {
        if (!this.connected) {
            vscode.window.showErrorMessage('Not connected to TEC server');
            return null;
        }
        
        try {
            const response = await axios.post(`${this.config.serverUrl}/process_asset`, {
                file_path: filePath,
                enable_hybrid_intelligence: this.config.enableHybridIntelligence
            });
            
            const result = response.data as MCPResponse;
            if (result.success) {
                vscode.window.showInformationMessage(
                    `✅ Asset processed: ${result.result.fragments_created} fragments created`
                );
                return result.result;
            } else {
                vscode.window.showErrorMessage(`Asset processing failed: ${result.error}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Request failed: ${error}`);
        }
        
        return null;
    }
    
    async hybridSynthesis(content: string, processingType: string = 'creative'): Promise<any> {
        if (!this.connected) {
            vscode.window.showErrorMessage('Not connected to TEC server');
            return null;
        }
        
        try {
            const response = await axios.post(`${this.config.serverUrl}/hybrid_synthesis`, {
                content,
                processing_type: processingType,
                include_performance_metrics: true
            });
            
            const result = response.data as MCPResponse;
            if (result.success) {
                return result.result;
            } else {
                vscode.window.showErrorMessage(`Hybrid synthesis failed: ${result.error}`);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Request failed: ${error}`);
        }
        
        return null;
    }
    
    dispose() {
        this.statusBarItem.dispose();
        if (this.websocket) {
            this.websocket.close();
        }
    }
}

let tecClient: TECMCPClient;

export function activate(context: vscode.ExtensionContext) {
    console.log('🏛️ TEC MCP Client activated');
    
    // Initialize TEC client
    tecClient = new TECMCPClient(context);
    
    // Register commands
    const commands = [
        vscode.commands.registerCommand('tec.connectToServer', async () => {
            await tecClient.connectToServer();
        }),
        
        vscode.commands.registerCommand('tec.serverStatus', async () => {
            vscode.window.showInformationMessage(
                tecClient['connected'] ? 
                '🏛️ TEC Asimov Engine: Connected' : 
                '❌ TEC Asimov Engine: Disconnected'
            );
        }),
        
        vscode.commands.registerCommand('tec.validateAxioms', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showErrorMessage('No active editor');
                return;
            }
            
            const selection = editor.selection;
            const content = editor.document.getText(selection.isEmpty ? undefined : selection);
            
            if (!content.trim()) {
                vscode.window.showErrorMessage('No content to validate');
                return;
            }
            
            const result = await tecClient.validateAxioms(content);
            if (result) {
                const message = result.valid ? 
                    `✅ Axiom validation passed (${(result.confidence_score * 100).toFixed(1)}%)` :
                    `❌ Axiom violations: ${result.violations.join(', ')}`;
                
                vscode.window.showInformationMessage(message);
                
                // Show detailed results in output channel
                const outputChannel = vscode.window.createOutputChannel('TEC Axiom Validation');
                outputChannel.clear();
                outputChannel.appendLine('TEC AXIOM VALIDATION RESULTS');
                outputChannel.appendLine('=' * 40);
                outputChannel.appendLine(`Valid: ${result.valid}`);
                outputChannel.appendLine(`Confidence: ${(result.confidence_score * 100).toFixed(1)}%`);
                outputChannel.appendLine('');
                outputChannel.appendLine('Axiom Scores:');
                Object.entries(result.axiom_scores).forEach(([axiom, score]) => {
                    outputChannel.appendLine(`  ${axiom}: ${(score * 100).toFixed(1)}%`);
                });
                
                if (result.violations.length > 0) {
                    outputChannel.appendLine('');
                    outputChannel.appendLine('Violations:');
                    result.violations.forEach(violation => {
                        outputChannel.appendLine(`  - ${violation}`);
                    });
                }
                
                outputChannel.show();
            }
        }),
        
        vscode.commands.registerCommand('tec.queryMemory', async () => {
            const query = await vscode.window.showInputBox({
                prompt: 'Enter memory query',
                placeholder: 'e.g. "exploited genius pattern" or "Tesla wireless power"'
            });
            
            if (!query) return;
            
            const result = await tecClient.queryMemory(query);
            if (result) {
                const outputChannel = vscode.window.createOutputChannel('TEC Memory Query');
                outputChannel.clear();
                outputChannel.appendLine('TEC MEMORY CORE QUERY RESULTS');
                outputChannel.appendLine('=' * 40);
                outputChannel.appendLine(`Query: "${query}"`);
                outputChannel.appendLine(`Matches: ${result.total_matches}`);
                outputChannel.appendLine(`Query time: ${result.query_time}ms`);
                outputChannel.appendLine('');
                
                result.fragments.forEach((fragment, index) => {
                    outputChannel.appendLine(`Fragment ${index + 1}: ${fragment.title}`);
                    outputChannel.appendLine(`ID: ${fragment.fragment_id}`);
                    outputChannel.appendLine(`Themes: ${fragment.themes.join(', ')}`);
                    outputChannel.appendLine(`Emotional Intensity: ${fragment.emotional_intensity}`);
                    outputChannel.appendLine('');
                    outputChannel.appendLine(fragment.content.substring(0, 300) + '...');
                    outputChannel.appendLine('=' * 40);
                });
                
                outputChannel.show();
                vscode.window.showInformationMessage(`Found ${result.total_matches} memory fragments`);
            }
        }),
        
        vscode.commands.registerCommand('tec.processAsset', async (uri: vscode.Uri) => {
            if (!uri) {
                const options: vscode.OpenDialogOptions = {
                    canSelectMany: false,
                    openLabel: 'Process Asset',
                    filters: {
                        'TEC Assets': ['m4a', 'mp4', 'txt', 'md', 'json']
                    }
                };
                
                const fileUri = await vscode.window.showOpenDialog(options);
                if (fileUri && fileUri[0]) {
                    uri = fileUri[0];
                } else {
                    return;
                }
            }
            
            vscode.window.showInformationMessage('🎵 Processing asset through TEC pipeline...');
            
            const result = await tecClient.processAsset(uri.fsPath);
            if (result) {
                vscode.window.showInformationMessage(
                    `✅ Asset processed: ${result.fragments_created} fragments, ` +
                    `${result.narrative_threads?.length || 0} threads identified`
                );
            }
        }),
        
        vscode.commands.registerCommand('tec.hybridSynthesis', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showErrorMessage('No active editor');
                return;
            }
            
            const selection = editor.selection;
            const content = editor.document.getText(selection.isEmpty ? undefined : selection);
            
            if (!content.trim()) {
                vscode.window.showErrorMessage('No content to process');
                return;
            }
            
            const processingType = await vscode.window.showQuickPick([
                'creative', 'logical', 'intuitive', 'analytical', 'hybrid'
            ], {
                placeHolder: 'Select processing type'
            });
            
            if (!processingType) return;
            
            vscode.window.showInformationMessage('🧠 Processing through hybrid intelligence...');
            
            const result = await tecClient.hybridSynthesis(content, processingType);
            if (result) {
                const outputChannel = vscode.window.createOutputChannel('TEC Hybrid Synthesis');
                outputChannel.clear();
                outputChannel.appendLine('TEC HYBRID INTELLIGENCE SYNTHESIS');
                outputChannel.appendLine('=' * 40);
                outputChannel.appendLine(`Processing Type: ${processingType}`);
                outputChannel.appendLine(`Pathway: ${result.processing_pathway}`);
                outputChannel.appendLine(`Processing Time: ${result.processing_time}ms`);
                outputChannel.appendLine('');
                
                if (result.performance_metrics) {
                    outputChannel.appendLine('Performance Metrics:');
                    Object.entries(result.performance_metrics).forEach(([metric, value]) => {
                        outputChannel.appendLine(`  ${metric}: ${value}`);
                    });
                    outputChannel.appendLine('');
                }
                
                if (result.synthesis_output) {
                    outputChannel.appendLine('Synthesis Output:');
                    outputChannel.appendLine(result.synthesis_output);
                }
                
                outputChannel.show();
                vscode.window.showInformationMessage(
                    `✅ Hybrid synthesis complete (${result.processing_time}ms)`
                );
            }
        })
    ];
    
    context.subscriptions.push(...commands, tecClient);
}

export function deactivate() {
    if (tecClient) {
        tecClient.dispose();
    }
}
