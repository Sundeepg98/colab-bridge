#!/usr/bin/env bun
/**
 * Multi-Instance Claude-Colab Bridge Client
 * Enhanced client supporting multiple Claude instances working simultaneously
 */

import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';
import { ClaudeColabBridge } from './bridge-client.js';

export class MultiInstanceClaudeColabBridge extends ClaudeColabBridge {
  constructor(config = {}) {
    super(config);
    
    // Multi-instance specific config
    this.instanceId = config.instanceId || `claude_${this.config.projectName}_${Date.now()}`;
    this.multiInstanceMode = true;
    this.registrationFile = null;
    
    // Enhanced routing
    this.priorityQueue = [];
    this.batchCommands = [];
    this.batchSize = config.batchSize || 5;
    this.batchTimeout = config.batchTimeout || 2000;
  }

  /**
   * Initialize multi-instance bridge
   */
  async init() {
    const success = await super.init();
    
    if (success) {
      await this.registerInstance();
      this.startInstanceHeartbeat();
      console.log(`🌐 Multi-instance bridge initialized: ${this.instanceId}`);
    }
    
    return success;
  }

  /**
   * Register this Claude instance with the bridge
   */
  async registerInstance() {
    const registration = {
      instance_id: this.instanceId,
      project_name: this.config.projectName,
      registered_at: new Date().toISOString(),
      capabilities: [
        'execute_code', 'install_package', 'shell_command',
        'ai_query', 'data_analysis', 'visualization',
        'file_operation', 'gpu_check', 'benchmark'
      ],
      preferences: {
        prefer_gpu: false,
        max_cost_per_request: 0.01,
        timeout: this.config.timeout
      }
    };

    // Save registration
    const fileMetadata = {
      name: `instance_${this.instanceId}.json`,
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
      console.log(`✅ Instance registered: ${this.instanceId}`);
    } catch (error) {
      console.error('❌ Failed to register instance:', error.message);
    }
  }

  /**
   * Start heartbeat to keep instance alive
   */
  startInstanceHeartbeat() {
    setInterval(async () => {
      try {
        await this.sendHeartbeat();
      } catch (error) {
        console.error('Heartbeat failed:', error.message);
      }
    }, 30000); // Every 30 seconds
  }

  /**
   * Send heartbeat
   */
  async sendHeartbeat() {
    const heartbeat = {
      instance_id: this.instanceId,
      timestamp: new Date().toISOString(),
      status: 'active',
      commands_sent: this.commandsSent || 0,
      last_command: this.lastCommandTime || null
    };

    const fileMetadata = {
      name: `heartbeat_${this.instanceId}.json`,
      parents: [this.config.colabFolderId]
    };

    const media = {
      mimeType: 'application/json',
      body: JSON.stringify(heartbeat, null, 2)
    };

    // Update or create heartbeat file
    await this.driveService.files.create({
      resource: fileMetadata,
      media: media,
      fields: 'id'
    });
  }

  /**
   * Enhanced command sending with multi-instance routing
   */
  async sendCommand(type, data = {}) {
    const command = {
      id: `${this.instanceId}_${type}_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
      type,
      timestamp: new Date().toISOString(),
      instance_id: this.instanceId,
      project: this.config.projectName,
      priority: data.priority || 'normal',
      requires_gpu: data.requires_gpu || false,
      estimated_runtime: data.estimated_runtime || 'short',
      ...data
    };

    try {
      // Check for optimal routing
      const routingInfo = await this.getOptimalRouting(command);
      command.routing_hint = routingInfo;

      // Upload to priority queue if high priority
      const folderPath = command.priority === 'high' ? 'commands/priority' : 'commands/global';
      
      await this.uploadCommandToFolder(command, folderPath);
      
      // Wait for result
      const result = await this.waitForResult(command.id);
      
      // Track usage
      this.commandsSent = (this.commandsSent || 0) + 1;
      this.lastCommandTime = new Date().toISOString();
      
      return result;
      
    } catch (error) {
      throw new Error(`Multi-instance command failed: ${error.message}`);
    }
  }

  /**
   * Get optimal routing information
   */
  async getOptimalRouting(command) {
    try {
      // Check system status to find best session
      const status = await this.getSystemStatus();
      
      if (status && status.sessions) {
        const sessions = Object.entries(status.sessions);
        
        // Filter sessions that can handle the command
        const availableSessions = sessions.filter(([sessionId, sessionInfo]) => {
          if (command.requires_gpu && !sessionInfo.gpu_available) {
            return false;
          }
          
          // Check if session supports required capabilities
          const requiredCaps = command.required_capabilities || [command.type];
          return requiredCaps.every(cap => sessionInfo.capabilities?.includes(cap));
        });

        if (availableSessions.length > 0) {
          // Sort by load (fewer projects = less busy)
          availableSessions.sort((a, b) => 
            (a[1].projects?.length || 0) - (b[1].projects?.length || 0)
          );
          
          return {
            preferred_session: availableSessions[0][0],
            routing_strategy: 'least_busy',
            available_sessions: availableSessions.length
          };
        }
      }
      
      return {
        routing_strategy: 'round_robin',
        available_sessions: 0
      };
      
    } catch (error) {
      return { routing_strategy: 'default', error: error.message };
    }
  }

  /**
   * Upload command to specific folder
   */
  async uploadCommandToFolder(command, folderPath) {
    // Create folder structure if needed
    const folders = folderPath.split('/');
    let currentFolderId = this.config.colabFolderId;
    
    for (const folder of folders) {
      const subFolder = await this.findOrCreateFolder(folder, currentFolderId);
      currentFolderId = subFolder;
    }

    // Upload command
    const fileMetadata = {
      name: `command_${command.id}.json`,
      parents: [currentFolderId]
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

    console.log(`📤 Sent to ${folderPath}: ${command.type} (${command.id})`);
  }

  /**
   * Find or create folder
   */
  async findOrCreateFolder(folderName, parentId) {
    // Check if folder exists
    const response = await this.driveService.files.list({
      q: `name='${folderName}' and '${parentId}' in parents and mimeType='application/vnd.google-apps.folder'`,
      fields: 'files(id, name)'
    });

    if (response.data.files && response.data.files.length > 0) {
      return response.data.files[0].id;
    }

    // Create folder
    const fileMetadata = {
      name: folderName,
      mimeType: 'application/vnd.google-apps.folder',
      parents: [parentId]
    };

    const folder = await this.driveService.files.create({
      resource: fileMetadata,
      fields: 'id'
    });

    return folder.data.id;
  }

  /**
   * Get system status including all instances and sessions
   */
  async getSystemStatus() {
    try {
      const response = await this.driveService.files.list({
        q: `name='system_status.json' and '${this.config.colabFolderId}' in parents`,
        fields: 'files(id, modifiedTime)'
      });

      if (response.data.files && response.data.files.length > 0) {
        const fileId = response.data.files[0].id;
        const result = await this.driveService.files.get({
          fileId: fileId,
          alt: 'media'
        });

        return JSON.parse(result.data);
      }

      return { error: 'System status not available' };
      
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Batch execute multiple commands efficiently
   */
  async batchExecute(commands) {
    const results = [];
    const batches = [];
    
    // Group commands into batches
    for (let i = 0; i < commands.length; i += this.batchSize) {
      batches.push(commands.slice(i, i + this.batchSize));
    }

    // Execute batches with some parallelism
    for (const batch of batches) {
      const batchPromises = batch.map(async (cmd) => {
        try {
          const result = await this.sendCommand(cmd.type, cmd);
          return { success: true, result, command: cmd };
        } catch (error) {
          return { success: false, error: error.message, command: cmd };
        }
      });

      const batchResults = await Promise.all(batchPromises);
      results.push(...batchResults);
      
      // Small delay between batches to avoid overwhelming
      if (batches.indexOf(batch) < batches.length - 1) {
        await this.sleep(500);
      }
    }

    return results;
  }

  /**
   * Priority execute - bypass queue for urgent commands
   */
  async priorityExec(code, options = {}) {
    return this.sendCommand('execute_code', {
      code,
      priority: 'high',
      ...options
    });
  }

  /**
   * GPU execute - request GPU-enabled session
   */
  async gpuExec(code, options = {}) {
    return this.sendCommand('execute_code', {
      code,
      requires_gpu: true,
      ...options
    });
  }

  /**
   * Long-running execute - for tasks that take time
   */
  async longRunningExec(code, options = {}) {
    return this.sendCommand('execute_code', {
      code,
      estimated_runtime: 'long',
      timeout: 300000, // 5 minutes
      ...options
    });
  }

  /**
   * Cleanup instance registration on shutdown
   */
  async cleanup() {
    try {
      if (this.registrationFile) {
        await this.driveService.files.delete({ fileId: this.registrationFile });
        console.log(`🧹 Cleaned up instance registration: ${this.instanceId}`);
      }
    } catch (error) {
      console.error('Cleanup failed:', error.message);
    }
  }

  /**
   * Static method to create multiple instances for load testing
   */
  static async createTestInstances(count, baseConfig = {}) {
    const instances = [];
    
    for (let i = 0; i < count; i++) {
      const config = {
        ...baseConfig,
        projectName: `test_project_${i}`,
        instanceId: `test_instance_${i}_${Date.now()}`
      };
      
      const instance = new MultiInstanceClaudeColabBridge(config);
      await instance.init();
      instances.push(instance);
    }
    
    console.log(`🧪 Created ${count} test instances`);
    return instances;
  }
}

// Command-line interface for multi-instance bridge
if (import.meta.main) {
  const command = process.argv[2];
  const projectName = process.argv[3] || 'multi_test_project';
  
  async function runMultiInstanceCLI() {
    const bridge = new MultiInstanceClaudeColabBridge({ projectName });
    await bridge.init();
    
    switch (command) {
      case 'test':
        console.log('🧪 Testing multi-instance bridge...');
        try {
          const result = await bridge.exec('print("Hello from multi-instance Colab!")');
          console.log('✅ Multi-instance test successful');
          console.log('Result:', result);
        } catch (error) {
          console.error('❌ Multi-instance test failed:', error.message);
        }
        break;
        
      case 'status':
        console.log('📊 Checking multi-instance system status...');
        const status = await bridge.getSystemStatus();
        console.log(JSON.stringify(status, null, 2));
        break;
        
      case 'batch-test':
        console.log('🔄 Testing batch execution...');
        const commands = [
          { type: 'execute_code', code: 'print("Batch command 1")' },
          { type: 'execute_code', code: 'print("Batch command 2")' },
          { type: 'execute_code', code: 'import numpy as np; print("NumPy available")' }
        ];
        
        const results = await bridge.batchExecute(commands);
        console.log(`✅ Batch completed: ${results.filter(r => r.success).length}/${results.length} successful`);
        break;
        
      case 'load-test':
        const instanceCount = parseInt(process.argv[4]) || 3;
        console.log(`🚀 Creating ${instanceCount} test instances...`);
        
        const instances = await MultiInstanceClaudeColabBridge.createTestInstances(instanceCount);
        
        // Run concurrent tests
        const promises = instances.map(async (instance, i) => {
          try {
            const result = await instance.exec(`print("Instance ${i} is working!")`);
            return { instance: i, success: true, result };
          } catch (error) {
            return { instance: i, success: false, error: error.message };
          }
        });
        
        const loadResults = await Promise.all(promises);
        const successCount = loadResults.filter(r => r.success).length;
        console.log(`📊 Load test results: ${successCount}/${instanceCount} instances successful`);
        
        // Cleanup
        for (const instance of instances) {
          await instance.cleanup();
        }
        break;
        
      default:
        console.log(`
🌐 Multi-Instance Claude-Colab Bridge CLI

Usage:
  bun multi-instance-client.js test [project_name]           # Test bridge
  bun multi-instance-client.js status [project_name]        # Check status
  bun multi-instance-client.js batch-test [project_name]    # Test batch execution
  bun multi-instance-client.js load-test [project_name] [instance_count]  # Load test

Examples:
  bun multi-instance-client.js test my_project
  bun multi-instance-client.js load-test my_project 5
        `);
    }
    
    await bridge.cleanup();
  }
  
  runMultiInstanceCLI().catch(console.error);
}

export default MultiInstanceClaudeColabBridge;