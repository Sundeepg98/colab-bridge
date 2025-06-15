#!/usr/bin/env bun
/**
 * Test Multi-Instance Claude-Colab Bridge
 * Validates that multiple Claude instances can work simultaneously with Colab
 */

import MultiInstanceClaudeColabBridge from './claude-colab-bridge/multi-instance-client.js';

class MultiInstanceBridgeTest {
  constructor() {
    this.testResults = [];
    this.instances = [];
  }

  async runTestSuite() {
    console.log('🚀 Starting Multi-Instance Bridge Test Suite');
    console.log('=============================================\n');

    try {
      // Test 1: Single instance basic functionality
      await this.testSingleInstance();
      
      // Test 2: Multiple instances simultaneously
      await this.testMultipleInstances();
      
      // Test 3: Load balancing and routing
      await this.testLoadBalancing();
      
      // Test 4: Priority and GPU commands
      await this.testAdvancedFeatures();
      
      // Test 5: Cleanup and resource management
      await this.testResourceManagement();
      
      this.printTestSummary();
      
    } catch (error) {
      console.error('❌ Test suite failed:', error.message);
    }
  }

  async testSingleInstance() {
    console.log('🧪 Test 1: Single Instance Basic Functionality');
    console.log('-----------------------------------------------');
    
    try {
      const bridge = new MultiInstanceClaudeColabBridge({
        projectName: 'test_single_instance',
        timeout: 15000
      });
      
      await bridge.init();
      this.instances.push(bridge);
      
      // Test basic execution
      console.log('  Testing basic code execution...');
      const result1 = await bridge.exec('print("Single instance test successful!")');
      
      this.recordTest('single_instance_exec', result1.success, result1.error);
      
      // Test system status
      console.log('  Testing system status...');
      const status = await bridge.getSystemStatus();
      
      this.recordTest('single_instance_status', status && !status.error, status?.error);
      
      console.log('  ✅ Single instance tests completed\n');
      
    } catch (error) {
      this.recordTest('single_instance', false, error.message);
      console.log(`  ❌ Single instance test failed: ${error.message}\n`);
    }
  }

  async testMultipleInstances() {
    console.log('🌐 Test 2: Multiple Instances Simultaneously');
    console.log('--------------------------------------------');
    
    try {
      const instanceCount = 3;
      const instances = [];
      
      // Create multiple instances
      console.log(`  Creating ${instanceCount} Claude instances...`);
      for (let i = 0; i < instanceCount; i++) {
        const bridge = new MultiInstanceClaudeColabBridge({
          projectName: `test_project_${i}`,
          instanceId: `test_instance_${i}_${Date.now()}`,
          timeout: 20000
        });
        
        await bridge.init();
        instances.push(bridge);
        this.instances.push(bridge);
      }
      
      // Run concurrent commands
      console.log('  Running concurrent commands...');
      const promises = instances.map(async (bridge, i) => {
        try {
          const result = await bridge.exec(`
import time
print(f"Instance {i} started at {time.time()}")
time.sleep(1)  # Simulate some work
print(f"Instance {i} completed at {time.time()}")
result = ${i} * 2
print(f"Instance {i} result: {result}")
          `);
          return { instance: i, success: true, result };
        } catch (error) {
          return { instance: i, success: false, error: error.message };
        }
      });
      
      const results = await Promise.all(promises);
      const successCount = results.filter(r => r.success).length;
      
      this.recordTest('multiple_instances_concurrent', 
        successCount === instanceCount, 
        `${successCount}/${instanceCount} instances succeeded`
      );
      
      console.log(`  ✅ Concurrent test: ${successCount}/${instanceCount} instances successful\n`);
      
    } catch (error) {
      this.recordTest('multiple_instances', false, error.message);
      console.log(`  ❌ Multiple instances test failed: ${error.message}\n`);
    }
  }

  async testLoadBalancing() {
    console.log('⚖️  Test 3: Load Balancing and Routing');
    console.log('-------------------------------------');
    
    try {
      if (this.instances.length < 2) {
        console.log('  ⚠️  Skipping load balancing test - insufficient instances\n');
        return;
      }
      
      // Test batch operations
      console.log('  Testing batch operations...');
      const batchCommands = [
        { type: 'execute_code', code: 'print("Batch command 1")' },
        { type: 'execute_code', code: 'print("Batch command 2")' },
        { type: 'execute_code', code: 'print("Batch command 3")' },
        { type: 'execute_code', code: 'print("Batch command 4")' },
        { type: 'execute_code', code: 'print("Batch command 5")' }
      ];
      
      const bridge = this.instances[0];
      const batchResults = await bridge.batchExecute(batchCommands);
      const batchSuccessCount = batchResults.filter(r => r.success).length;
      
      this.recordTest('load_balancing_batch', 
        batchSuccessCount >= batchCommands.length * 0.8, // 80% success rate
        `${batchSuccessCount}/${batchCommands.length} batch commands succeeded`
      );
      
      console.log(`  ✅ Batch operations: ${batchSuccessCount}/${batchCommands.length} successful\n`);
      
    } catch (error) {
      this.recordTest('load_balancing', false, error.message);
      console.log(`  ❌ Load balancing test failed: ${error.message}\n`);
    }
  }

  async testAdvancedFeatures() {
    console.log('🎯 Test 4: Priority and Advanced Features');
    console.log('-----------------------------------------');
    
    try {
      if (this.instances.length === 0) {
        console.log('  ⚠️  Skipping advanced features test - no instances available\n');
        return;
      }
      
      const bridge = this.instances[0];
      
      // Test priority execution
      console.log('  Testing priority execution...');
      const priorityResult = await bridge.priorityExec(`
print("Priority command executed!")
import datetime
print(f"Executed at: {datetime.datetime.now()}")
      `);
      
      this.recordTest('priority_execution', priorityResult.success, priorityResult.error);
      
      // Test package installation
      console.log('  Testing package installation...');
      const installResult = await bridge.install(['requests']);
      
      this.recordTest('package_installation', installResult.success, installResult.error);
      
      // Test AI query (if available)
      console.log('  Testing AI query...');
      try {
        const aiResult = await bridge.ai('Write a simple Python function that adds two numbers');
        this.recordTest('ai_query', aiResult.success, aiResult.error);
      } catch (error) {
        this.recordTest('ai_query', false, 'AI not configured - this is expected');
      }
      
      console.log('  ✅ Advanced features tests completed\n');
      
    } catch (error) {
      this.recordTest('advanced_features', false, error.message);
      console.log(`  ❌ Advanced features test failed: ${error.message}\n`);
    }
  }

  async testResourceManagement() {
    console.log('🧹 Test 5: Cleanup and Resource Management');
    console.log('------------------------------------------');
    
    try {
      console.log('  Testing instance cleanup...');
      
      let cleanupSuccessCount = 0;
      for (const bridge of this.instances) {
        try {
          await bridge.cleanup();
          cleanupSuccessCount++;
        } catch (error) {
          console.log(`    ⚠️  Cleanup warning for instance: ${error.message}`);
        }
      }
      
      this.recordTest('resource_cleanup', 
        cleanupSuccessCount >= this.instances.length * 0.8, // 80% cleanup success
        `${cleanupSuccessCount}/${this.instances.length} instances cleaned up`
      );
      
      console.log(`  ✅ Resource management: ${cleanupSuccessCount}/${this.instances.length} cleaned up\n`);
      
    } catch (error) {
      this.recordTest('resource_management', false, error.message);
      console.log(`  ❌ Resource management test failed: ${error.message}\n`);
    }
  }

  recordTest(testName, success, message) {
    this.testResults.push({
      test: testName,
      success,
      message: message || (success ? 'OK' : 'Failed'),
      timestamp: new Date().toISOString()
    });
  }

  printTestSummary() {
    console.log('📊 Test Suite Summary');
    console.log('====================');
    
    const totalTests = this.testResults.length;
    const passedTests = this.testResults.filter(t => t.success).length;
    const failedTests = totalTests - passedTests;
    
    console.log(`Total Tests: ${totalTests}`);
    console.log(`Passed: ${passedTests} ✅`);
    console.log(`Failed: ${failedTests} ❌`);
    console.log(`Success Rate: ${((passedTests / totalTests) * 100).toFixed(1)}%\n`);
    
    if (failedTests > 0) {
      console.log('Failed Tests:');
      this.testResults
        .filter(t => !t.success)
        .forEach(t => {
          console.log(`  ❌ ${t.test}: ${t.message}`);
        });
    }
    
    console.log('\n🎉 Multi-Instance Bridge Test Suite Completed!');
    console.log('\n💡 Next Steps:');
    console.log('1. Start a Google Colab notebook with the multi-instance processor');
    console.log('2. Update PROJECT_NAME in the processor to match your test projects');
    console.log('3. Run this test again to validate full end-to-end functionality');
    console.log('4. Use ./claude-colab-bridge/multi-instance-client.js for production');
  }
}

// Run the test suite
async function main() {
  const tester = new MultiInstanceBridgeTest();
  await tester.runTestSuite();
}

// Execute if run directly
if (import.meta.main) {
  main().catch(console.error);
}

export { MultiInstanceBridgeTest };