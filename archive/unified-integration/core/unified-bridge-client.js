#!/usr/bin/env bun
/**
 * Unified Claude-Colab Bridge Client
 * Combines basic bridge + multi-instance + advanced features into one client
 */

import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';

export class UnifiedClaudeColabBridge {
  constructor(config = {}) {
    // Core configuration
    this.config = {
      serviceAccountPath: config.serviceAccountPath || process.env.SERVICE_ACCOUNT_PATH || '/var/projects/eng-flux-459812-q6-e05c54813553.json',
      colabFolderId: config.colabFolderId || process.env.GOOGLE_DRIVE_FOLDER_ID || '1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z',
      projectName: config.projectName || 'unified_claude_project',
      timeout: config.timeout || 30000,
      retries: config.retries || 3,
      
      // Multi-instance configuration
      multiInstanceMode: config.multiInstanceMode !== false, // Default enabled
      instanceId: config.instanceId || `claude_${config.projectName || 'unified'}_${Date.now()}`,
      
      // Advanced features
      enableAdvancedFeatures: config.enableAdvancedFeatures !== false, // Default enabled
      enableLearning: config.enableLearning !== false,
      enableMonitoring: config.enableMonitoring !== false,
      
      // Performance tuning
      batchSize: config.batchSize || 5,
      batchTimeout: config.batchTimeout || 2000,
      concurrentSessions: config.concurrentSessions || 3
    };
    
    // State management
    this.driveService = null;
    this.isInitialized = false;
    this.commandQueue = [];
    this.commandsSent = 0;
    this.lastCommandTime = null;
    this.registrationFile = null;
    
    // Multi-instance state
    this.activeSessions = new Map();
    this.sessionHealth = new Map();
    this.loadBalancingStrategy = config.loadBalancingStrategy || 'intelligent';
    
    // Advanced features
    this.learningData = {
      commandPatterns: new Map(),
      responseMetrics: [],
      userPreferences: {}
    };
  }

  /**
   * Initialize the unified bridge
   */
  async init() {
    try {
      console.log(`🚀 Initializing Unified Claude-Colab Bridge`);
      console.log(`   Project: ${this.config.projectName}`);
      console.log(`   Instance: ${this.config.instanceId}`);
      console.log(`   Multi-instance: ${this.config.multiInstanceMode ? 'Enabled' : 'Disabled'}`);
      
      // Initialize Google Drive connection
      await this.initGoogleDrive();
      
      // Register instance if multi-instance mode
      if (this.config.multiInstanceMode) {
        await this.registerInstance();
        this.startInstanceHeartbeat();
      }
      
      // Initialize advanced features
      if (this.config.enableAdvancedFeatures) {
        await this.initAdvancedFeatures();
      }
      
      // Discovery existing sessions
      await this.discoverSessions();
      
      this.isInitialized = true;
      console.log(`✅ Unified bridge initialized successfully`);
      
      return true;
      
    } catch (error) {
      console.error('❌ Unified bridge initialization failed:', error.message);
      return false;
    }
  }

  /**
   * Initialize Google Drive connection
   */
  async initGoogleDrive() {
    const credentials = JSON.parse(
      fs.readFileSync(this.config.serviceAccountPath, 'utf8')
    );

    const auth = new google.auth.GoogleAuth({
      credentials,
      scopes: ['https://www.googleapis.com/auth/drive']
    });

    this.driveService = google.drive({ version: 'v3', auth });
  }

  /**
   * Register this instance for multi-instance coordination
   */
  async registerInstance() {
    const registration = {
      instance_id: this.config.instanceId,
      project_name: this.config.projectName,
      registered_at: new Date().toISOString(),
      capabilities: [
        'execute_code', 'install_package', 'shell_command',
        'ai_query', 'data_analysis', 'visualization',
        'file_operation', 'gpu_check', 'benchmark',
        'batch_operations', 'priority_queue', 'learning'
      ],
      preferences: {
        prefer_gpu: false,
        max_cost_per_request: 0.01,
        timeout: this.config.timeout,
        load_balancing: this.loadBalancingStrategy
      },
      advanced_features: {
        learning_enabled: this.config.enableLearning,
        monitoring_enabled: this.config.enableMonitoring,
        auto_optimization: true
      }
    };

    const fileMetadata = {
      name: `instance_${this.config.instanceId}.json`,
      parents: [this.config.colabFolderId]
    };

    const media = {
      mimeType: 'application/json',
      body: JSON.stringify(registration, null, 2)
    };

    try {
      const result = await this.driveService.files.create({
        resource: fileMetadata,
        media: media,
        fields: 'id'
      });
      
      this.registrationFile = result.data.id;
      console.log(`✅ Instance registered: ${this.config.instanceId}`);
    } catch (error) {
      console.error('❌ Failed to register instance:', error.message);
    }
  }

  /**
   * Initialize advanced features
   */
  async initAdvancedFeatures() {
    console.log('🧠 Initializing advanced features...');
    
    // Load learning data if available
    if (this.config.enableLearning) {
      await this.loadLearningData();
    }
    
    // Start monitoring if enabled
    if (this.config.enableMonitoring) {
      this.startMonitoring();
    }
    
    console.log('✅ Advanced features initialized');
  }

  /**
   * Discover existing Colab sessions
   */
  async discoverSessions() {
    try {
      const response = await this.driveService.files.list({
        q: `name contains 'session_' and '${this.config.colabFolderId}' in parents`,
        fields: 'files(id, name, modifiedTime)'
      });

      if (response.data.files) {
        for (const file of response.data.files) {
          try {
            const sessionData = await this.driveService.files.get({
              fileId: file.id,
              alt: 'media'
            });
            
            const session = JSON.parse(sessionData.data);
            this.activeSessions.set(session.session_id, {
              ...session,
              discovered_at: new Date(),
              file_id: file.id
            });
            
          } catch (error) {
            console.warn(`⚠️ Could not parse session file: ${file.name}`);
          }
        }
      }
      
      console.log(`🔍 Discovered ${this.activeSessions.size} active sessions`);
      
    } catch (error) {
      console.warn('⚠️ Session discovery failed:', error.message);
    }
  }

  /**
   * Smart command execution with intelligent routing
   */
  async exec(code, options = {}) {
    return this.sendCommand('execute_code', {
      code,
      use_context: options.useContext !== false,
      priority: options.priority || 'normal',
      requires_gpu: options.requiresGpu || false,
      estimated_runtime: options.estimatedRuntime || 'short',
      enable_learning: this.config.enableLearning,
      ...options
    });
  }

  /**
   * Install packages with intelligent caching
   */
  async install(packages, options = {}) {
    if (typeof packages === 'string') {
      packages = packages.split(' ');
    }
    
    // Check if packages are already installed (learning optimization)
    const cachedPackages = this.getCachedPackages();
    const newPackages = packages.filter(pkg => !cachedPackages.includes(pkg));
    
    if (newPackages.length === 0) {
      console.log('📦 All packages already installed (cached)');
      return { success: true, cached: true, packages };
    }
    
    return this.sendCommand('install_package', { 
      packages: newPackages,
      cache_result: true,
      ...options 
    });
  }

  /**
   * Execute shell commands with safety checks
   */
  async shell(command, options = {}) {
    // Basic safety check for dangerous commands
    const dangerousPatterns = ['rm -rf', 'sudo rm', 'dd if=', 'mkfs', 'fdisk'];
    const isDangerous = dangerousPatterns.some(pattern => command.includes(pattern));
    
    if (isDangerous && !options.allowDangerous) {
      throw new Error('Potentially dangerous command detected. Use allowDangerous: true to override.');
    }
    
    return this.sendCommand('shell_command', {
      command,
      cwd: options.cwd,
      safety_checked: true,
      ...options
    });
  }

  /**
   * AI query with learning and optimization
   */
  async ai(prompt, options = {}) {
    // Learn from prompt patterns
    if (this.config.enableLearning) {
      this.recordPromptPattern(prompt);
    }
    
    return this.sendCommand('ai_query', {
      prompt,
      model: options.model || 'gemini',
      optimize_prompt: this.config.enableLearning,
      ...options
    });
  }

  /**
   * Advanced data analysis with automatic visualization
   */
  async analyze(data, options = {}) {
    const analysisType = options.type || 'comprehensive';
    
    const command = {
      data,
      analysis_type: analysisType,
      auto_visualize: options.autoVisualize !== false,
      export_format: options.exportFormat || 'json',
      ...options
    };
    
    return this.sendCommand('data_analysis', command);
  }

  /**
   * Batch execute with intelligent optimization
   */
  async batchExecute(commands, options = {}) {
    console.log(`🔄 Executing batch of ${commands.length} commands...`);
    
    // Intelligent batching based on command types and requirements
    const optimizedBatches = this.optimizeBatches(commands);
    const results = [];
    
    for (let i = 0; i < optimizedBatches.length; i++) {
      const batch = optimizedBatches[i];
      console.log(`  📦 Processing batch ${i + 1}/${optimizedBatches.length} (${batch.length} commands)`);
      
      // Execute batch with appropriate session selection
      const batchPromises = batch.map(async (cmd) => {
        try {
          const result = await this.sendCommand(cmd.type, cmd, { batch: true });
          return { success: true, result, command: cmd };
        } catch (error) {
          return { success: false, error: error.message, command: cmd };
        }
      });

      const batchResults = await Promise.all(batchPromises);
      results.push(...batchResults);
      
      // Adaptive delay between batches
      if (i < optimizedBatches.length - 1) {
        const delay = this.calculateOptimalDelay(batchResults);
        await this.sleep(delay);
      }
    }
    
    // Learn from batch execution patterns
    if (this.config.enableLearning) {
      this.recordBatchPattern(commands, results);
    }
    
    const successCount = results.filter(r => r.success).length;
    console.log(`✅ Batch completed: ${successCount}/${commands.length} successful`);
    
    return results;
  }

  /**
   * Core command sending with intelligent routing
   */
  async sendCommand(type, data = {}, options = {}) {
    if (!this.isInitialized) {
      await this.init();
    }

    const command = {
      id: `${this.config.instanceId}_${type}_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
      type,
      timestamp: new Date().toISOString(),
      instance_id: this.config.instanceId,
      project: this.config.projectName,
      priority: data.priority || 'normal',
      requires_gpu: data.requires_gpu || false,
      estimated_runtime: data.estimated_runtime || 'short',
      ...data
    };

    try {
      // Intelligent session selection
      const targetSession = await this.selectOptimalSession(command);
      command.routing_hint = {
        preferred_session: targetSession,
        routing_strategy: this.loadBalancingStrategy,
        selected_at: new Date().toISOString()
      };

      // Upload command to appropriate queue
      const folderPath = this.determineCommandFolder(command);
      await this.uploadCommandToFolder(command, folderPath);
      
      // Wait for result with intelligent timeout
      const timeout = this.calculateTimeout(command);
      const result = await this.waitForResult(command.id, timeout);
      
      // Learn from execution
      if (this.config.enableLearning) {
        this.recordCommandExecution(command, result);
      }
      
      // Update metrics
      this.commandsSent++;
      this.lastCommandTime = new Date().toISOString();
      
      return result;
      
    } catch (error) {
      // Learn from failures
      if (this.config.enableLearning) {
        this.recordCommandFailure(command, error);
      }
      
      throw new Error(`Unified bridge command failed: ${error.message}`);
    }
  }

  /**
   * Intelligent session selection
   */
  async selectOptimalSession(command) {
    const availableSessions = Array.from(this.activeSessions.values()).filter(session => {
      // Filter by capabilities
      if (command.requires_gpu && !session.gpu_available) return false;
      
      // Filter by health
      const health = this.sessionHealth.get(session.session_id);
      if (health && health.status !== 'healthy') return false;
      
      return true;
    });

    if (availableSessions.length === 0) {
      throw new Error('No suitable sessions available');
    }

    // Apply intelligent selection strategy
    switch (this.loadBalancingStrategy) {
      case 'intelligent':
        return this.selectIntelligentSession(availableSessions, command);
      case 'least_busy':
        return this.selectLeastBusySession(availableSessions);
      case 'round_robin':
        return this.selectRoundRobinSession(availableSessions);
      case 'affinity':
        return this.selectAffinitySession(availableSessions, command);
      default:
        return availableSessions[0].session_id;
    }
  }

  /**
   * Intelligent session selection using learning data
   */
  selectIntelligentSession(sessions, command) {
    // Score sessions based on multiple factors
    const sessionScores = sessions.map(session => {
      let score = 100; // Base score
      
      // Performance history
      const history = this.learningData.commandPatterns.get(session.session_id);
      if (history) {
        score += history.averageResponseTime > 5000 ? -20 : 10;
        score += history.successRate > 0.9 ? 15 : -10;
      }
      
      // Current load
      const currentLoad = session.active_commands || 0;
      score -= currentLoad * 5;
      
      // Resource match
      if (command.requires_gpu && session.gpu_available) score += 20;
      if (command.estimated_runtime === 'long' && session.memory_gb > 8) score += 10;
      
      // Project affinity
      if (session.project_names && session.project_names.includes(command.project)) {
        score += 15;
      }
      
      return { session, score };
    });
    
    // Select highest scoring session
    sessionScores.sort((a, b) => b.score - a.score);
    return sessionScores[0].session.session_id;
  }

  /**
   * Start instance heartbeat for multi-instance coordination
   */
  startInstanceHeartbeat() {
    setInterval(async () => {
      try {
        await this.sendHeartbeat();
      } catch (error) {
        console.warn('⚠️ Heartbeat failed:', error.message);
      }
    }, 30000); // Every 30 seconds
  }

  /**
   * Send heartbeat with advanced metrics
   */
  async sendHeartbeat() {
    const heartbeat = {
      instance_id: this.config.instanceId,
      timestamp: new Date().toISOString(),
      status: 'active',
      commands_sent: this.commandsSent,
      last_command: this.lastCommandTime,
      active_sessions: Array.from(this.activeSessions.keys()),
      performance_metrics: this.getPerformanceMetrics(),
      learning_stats: this.config.enableLearning ? this.getLearningStats() : null
    };

    const fileMetadata = {
      name: `heartbeat_${this.config.instanceId}.json`,
      parents: [this.config.colabFolderId]
    };

    const media = {
      mimeType: 'application/json',
      body: JSON.stringify(heartbeat, null, 2)
    };

    await this.driveService.files.create({
      resource: fileMetadata,
      media: media,
      fields: 'id'
    });
  }

  /**
   * Advanced monitoring
   */
  startMonitoring() {
    console.log('📊 Starting advanced monitoring...');
    
    setInterval(async () => {
      await this.updateSessionHealth();
      await this.optimizePerformance();
    }, 60000); // Every minute
  }

  /**
   * Get comprehensive system status
   */
  async getSystemStatus() {
    try {
      const status = await this.driveService.files.list({
        q: `name='system_status.json' and '${this.config.colabFolderId}' in parents`,
        fields: 'files(id, modifiedTime)'
      });

      if (status.data.files && status.data.files.length > 0) {
        const fileId = status.data.files[0].id;
        const result = await this.driveService.files.get({
          fileId: fileId,
          alt: 'media'
        });

        const systemStatus = JSON.parse(result.data);
        
        // Enhance with local data
        systemStatus.local_instance = {
          instance_id: this.config.instanceId,
          commands_sent: this.commandsSent,
          active_sessions: this.activeSessions.size,
          uptime: Date.now() - this.initTime,
          advanced_features: {
            learning: this.config.enableLearning,
            monitoring: this.config.enableMonitoring
          }
        };
        
        return systemStatus;
      }

      return { error: 'System status not available' };
      
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Cleanup and shutdown
   */
  async cleanup() {
    console.log('🧹 Cleaning up unified bridge...');
    
    try {
      // Remove instance registration
      if (this.registrationFile) {
        await this.driveService.files.delete({ fileId: this.registrationFile });
      }
      
      // Save learning data
      if (this.config.enableLearning) {
        await this.saveLearningData();
      }
      
      console.log(`✅ Cleanup completed for instance: ${this.config.instanceId}`);
      
    } catch (error) {
      console.error('❌ Cleanup failed:', error.message);
    }
  }

  // Additional utility methods for learning, optimization, etc.
  getCachedPackages() { return []; }
  recordPromptPattern(prompt) { /* Learning implementation */ }
  optimizeBatches(commands) { return [commands]; }
  calculateOptimalDelay(results) { return 500; }
  recordBatchPattern(commands, results) { /* Learning implementation */ }
  recordCommandExecution(command, result) { /* Learning implementation */ }
  recordCommandFailure(command, error) { /* Learning implementation */ }
  sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
  
  // Helper methods for session management
  determineCommandFolder(command) {
    return command.priority === 'high' ? 'commands/priority' : 'commands/global';
  }
  
  calculateTimeout(command) {
    const baseTimeout = this.config.timeout;
    const runtimeMultiplier = command.estimated_runtime === 'long' ? 3 : 1;
    return baseTimeout * runtimeMultiplier;
  }
  
  async uploadCommandToFolder(command, folderPath) {
    // Implementation for uploading commands to specific folders
    const fileMetadata = {
      name: `command_${command.id}.json`,
      parents: [this.config.colabFolderId]
    };

    const media = {
      mimeType: 'application/json',
      body: JSON.stringify(command, null, 2)
    };

    await this.driveService.files.create({
      resource: fileMetadata,
      media: media,
      fields: 'id'
    });
  }
  
  async waitForResult(commandId, timeout = this.config.timeout) {
    // Implementation for waiting for command results
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      try {
        const response = await this.driveService.files.list({
          q: `name='result_${commandId}.json' and '${this.config.colabFolderId}' in parents`,
          fields: 'files(id, name)'
        });

        if (response.data.files && response.data.files.length > 0) {
          const fileId = response.data.files[0].id;
          const result = await this.driveService.files.get({
            fileId: fileId,
            alt: 'media'
          });

          await this.driveService.files.delete({ fileId });
          return JSON.parse(result.data);
        }

        await this.sleep(1000);
        
      } catch (error) {
        // Continue waiting
      }
    }

    throw new Error(`Command timeout after ${timeout}ms`);
  }
  
  // Placeholder methods for advanced features
  async loadLearningData() { /* Implementation */ }
  async saveLearningData() { /* Implementation */ }
  async updateSessionHealth() { /* Implementation */ }
  async optimizePerformance() { /* Implementation */ }
  getPerformanceMetrics() { return {}; }
  getLearningStats() { return {}; }
  selectLeastBusySession(sessions) { return sessions[0].session_id; }
  selectRoundRobinSession(sessions) { return sessions[0].session_id; }
  selectAffinitySession(sessions, command) { return sessions[0].session_id; }
}

// Static convenience methods
UnifiedClaudeColabBridge.quickStart = async function(projectName, options = {}) {
  const bridge = new UnifiedClaudeColabBridge({
    projectName,
    ...options
  });
  
  await bridge.init();
  return bridge;
};

// Export for ES modules and CommonJS
export default UnifiedClaudeColabBridge;
export { UnifiedClaudeColabBridge };

// CLI interface
if (import.meta.main) {
  const command = process.argv[2];
  const projectName = process.argv[3] || 'unified_test_project';
  
  async function runCLI() {
    const bridge = await UnifiedClaudeColabBridge.quickStart(projectName);
    
    switch (command) {
      case 'test':
        console.log('🧪 Testing unified bridge...');
        try {
          const result = await bridge.exec('print("Unified bridge test successful!")');
          console.log('✅ Test successful:', result);
        } catch (error) {
          console.error('❌ Test failed:', error.message);
        }
        break;
        
      case 'status':
        console.log('📊 Getting system status...');
        const status = await bridge.getSystemStatus();
        console.log(JSON.stringify(status, null, 2));
        break;
        
      case 'batch-test':
        console.log('🔄 Testing batch execution...');
        const commands = [
          { type: 'execute_code', code: 'print("Batch 1")' },
          { type: 'execute_code', code: 'print("Batch 2")' },
          { type: 'execute_code', code: 'import datetime; print(f"Time: {datetime.datetime.now()}")' }
        ];
        
        const results = await bridge.batchExecute(commands);
        console.log(`✅ Batch: ${results.filter(r => r.success).length}/${results.length} successful`);
        break;
        
      default:
        console.log(`
🚀 Unified Claude-Colab Bridge CLI

Usage:
  bun unified-bridge-client.js test [project_name]           # Test bridge
  bun unified-bridge-client.js status [project_name]        # Check status
  bun unified-bridge-client.js batch-test [project_name]    # Test batch execution

Examples:
  bun unified-bridge-client.js test my_project
        `);
    }
    
    await bridge.cleanup();
  }
  
  runCLI().catch(console.error);
}