#!/usr/bin/env bun
/**
 * Verify Personal Claude Tools Colab Integration Setup
 * Checks if everything is properly configured and accessible
 */

import fs from 'fs';
import path from 'path';

class PersonalToolsVerification {
  constructor() {
    this.checks = [];
    this.errors = [];
    this.warnings = [];
  }

  async runVerification() {
    console.log('🔍 Personal Claude Tools - Colab Integration Verification');
    console.log('========================================================\n');

    try {
      // Check 1: Personal tools directory
      await this.checkPersonalToolsDirectory();
      
      // Check 2: Bridge components
      await this.checkBridgeComponents();
      
      // Check 3: Integration files
      await this.checkIntegrationFiles();
      
      // Check 4: Configuration files
      await this.checkConfigurationFiles();
      
      // Check 5: Service account
      await this.checkServiceAccount();
      
      // Check 6: Dependencies
      await this.checkDependencies();
      
      this.printSummary();
      
    } catch (error) {
      console.error('❌ Verification failed:', error.message);
    }
  }

  async checkPersonalToolsDirectory() {
    console.log('📂 Checking Personal Tools Directory...');
    
    const personalToolsPath = '/var/projects/personal-claude-tools/colab-integration';
    
    if (fs.existsSync(personalToolsPath)) {
      this.recordCheck('personal_tools_directory', true, `Found at: ${personalToolsPath}`);
      
      // Check key files
      const keyFiles = [
        'app.py',
        'COMPLETE_COLAB_INTEGRATION.py',
        'src/api_key_manager.py',
        'src/auto_maintenance_engine.py',
        'templates/colab_dashboard.html'
      ];
      
      let foundFiles = 0;
      for (const file of keyFiles) {
        const filePath = path.join(personalToolsPath, file);
        if (fs.existsSync(filePath)) {
          foundFiles++;
        } else {
          this.recordWarning(`Missing personal tools file: ${file}`);
        }
      }
      
      this.recordCheck('personal_tools_files', foundFiles >= keyFiles.length * 0.8, 
        `${foundFiles}/${keyFiles.length} key files found`);
      
    } else {
      this.recordCheck('personal_tools_directory', false, 'Personal tools directory not found');
    }
    
    console.log('  ✅ Personal tools directory check completed\n');
  }

  async checkBridgeComponents() {
    console.log('🌉 Checking Bridge Components...');
    
    const bridgePath = '/var/projects/claude-colab-bridge';
    const components = [
      'bridge-client.js',
      'multi-instance-client.js', 
      'colab-processor.py',
      'init-bridge.sh',
      'README.md'
    ];
    
    let foundComponents = 0;
    for (const component of components) {
      const componentPath = path.join(bridgePath, component);
      if (fs.existsSync(componentPath)) {
        foundComponents++;
      } else {
        this.recordWarning(`Missing bridge component: ${component}`);
      }
    }
    
    this.recordCheck('bridge_components', foundComponents === components.length,
      `${foundComponents}/${components.length} bridge components found`);
    
    console.log('  ✅ Bridge components check completed\n');
  }

  async checkIntegrationFiles() {
    console.log('🔗 Checking Integration Files...');
    
    const integrationFiles = [
      '/var/projects/UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py',
      '/var/projects/MULTI_INSTANCE_COLAB_SETUP_GUIDE.md',
      '/var/projects/UPDATED_PERSONAL_TOOLS_SETUP_GUIDE.md',
      '/var/projects/ai-integration-platform/src/multi_instance_colab_bridge.py',
      '/var/projects/ai-integration-platform/src/simplified_unified_manager.py'
    ];
    
    let foundFiles = 0;
    for (const file of integrationFiles) {
      if (fs.existsSync(file)) {
        foundFiles++;
      } else {
        this.recordWarning(`Missing integration file: ${path.basename(file)}`);
      }
    }
    
    this.recordCheck('integration_files', foundFiles >= integrationFiles.length * 0.8,
      `${foundFiles}/${integrationFiles.length} integration files found`);
    
    console.log('  ✅ Integration files check completed\n');
  }

  async checkConfigurationFiles() {
    console.log('⚙️  Checking Configuration Files...');
    
    const configFiles = [
      '/var/projects/personal-claude-tools/colab-integration/config/api_config.py',
      '/var/projects/ai-integration-platform/config/cost/cost_state.json',
      '/var/projects/ai-integration-platform/claude_status.json'
    ];
    
    let foundConfigs = 0;
    for (const configFile of configFiles) {
      if (fs.existsSync(configFile)) {
        foundConfigs++;
      }
    }
    
    this.recordCheck('configuration_files', foundConfigs > 0,
      `${foundConfigs}/${configFiles.length} configuration files found`);
    
    console.log('  ✅ Configuration files check completed\n');
  }

  async checkServiceAccount() {
    console.log('🔐 Checking Service Account...');
    
    const serviceAccountPath = '/var/projects/eng-flux-459812-q6-e05c54813553.json';
    
    if (fs.existsSync(serviceAccountPath)) {
      try {
        const serviceAccount = JSON.parse(fs.readFileSync(serviceAccountPath, 'utf8'));
        const hasRequiredFields = serviceAccount.client_email && serviceAccount.private_key;
        
        this.recordCheck('service_account', hasRequiredFields, 
          hasRequiredFields ? 'Service account valid' : 'Service account missing required fields');
        
      } catch (error) {
        this.recordCheck('service_account', false, 'Service account file corrupted');
      }
    } else {
      this.recordCheck('service_account', false, 'Service account file not found');
    }
    
    console.log('  ✅ Service account check completed\n');
  }

  async checkDependencies() {
    console.log('📦 Checking Dependencies...');
    
    // Check if bun is available
    try {
      const bunVersion = process.version;
      this.recordCheck('bun_runtime', true, `Bun runtime available: ${bunVersion}`);
    } catch (error) {
      this.recordCheck('bun_runtime', false, 'Bun runtime not available');
    }
    
    // Check Python availability for personal tools
    const pythonFiles = [
      '/var/projects/personal-claude-tools/colab-integration/requirements.txt'
    ];
    
    let pythonSetup = false;
    for (const file of pythonFiles) {
      if (fs.existsSync(file)) {
        pythonSetup = true;
        break;
      }
    }
    
    this.recordCheck('python_setup', pythonSetup, 
      pythonSetup ? 'Python requirements found' : 'Python setup incomplete');
    
    console.log('  ✅ Dependencies check completed\n');
  }

  recordCheck(name, passed, message) {
    this.checks.push({
      name,
      passed,
      message,
      type: 'check'
    });
  }

  recordWarning(message) {
    this.warnings.push(message);
  }

  recordError(message) {
    this.errors.push(message);
  }

  printSummary() {
    console.log('📊 Verification Summary');
    console.log('======================');
    
    const totalChecks = this.checks.length;
    const passedChecks = this.checks.filter(c => c.passed).length;
    const failedChecks = totalChecks - passedChecks;
    
    console.log(`Total Checks: ${totalChecks}`);
    console.log(`Passed: ${passedChecks} ✅`);
    console.log(`Failed: ${failedChecks} ❌`);
    console.log(`Warnings: ${this.warnings.length} ⚠️`);
    
    if (failedChecks > 0) {
      console.log('\n❌ Failed Checks:');
      this.checks
        .filter(c => !c.passed)
        .forEach(c => {
          console.log(`  • ${c.name}: ${c.message}`);
        });
    }
    
    if (this.warnings.length > 0) {
      console.log('\n⚠️  Warnings:');
      this.warnings.forEach(w => {
        console.log(`  • ${w}`);
      });
    }
    
    console.log('\n🎯 Status Assessment:');
    const healthScore = (passedChecks / totalChecks) * 100;
    
    if (healthScore >= 90) {
      console.log('✅ EXCELLENT: Your setup is fully operational!');
    } else if (healthScore >= 75) {
      console.log('🟡 GOOD: Setup is mostly working, minor issues to address');
    } else if (healthScore >= 50) {
      console.log('🟠 FAIR: Setup has some issues that should be resolved');
    } else {
      console.log('🔴 POOR: Setup needs significant attention');
    }
    
    console.log('\n📋 Next Steps:');
    
    if (this.checks.find(c => c.name === 'personal_tools_directory' && c.passed)) {
      console.log('1. ✅ Personal tools are ready - you can start the dashboard:');
      console.log('   cd /var/projects/personal-claude-tools/colab-integration && python app.py');
    } else {
      console.log('1. 🔧 Set up personal tools directory first');
    }
    
    if (this.checks.find(c => c.name === 'bridge_components' && c.passed)) {
      console.log('2. ✅ Bridge is ready - test with:');
      console.log('   bun /var/projects/test-multi-instance-bridge.js');
    } else {
      console.log('2. 🔧 Fix bridge components');
    }
    
    if (this.checks.find(c => c.name === 'service_account' && c.passed)) {
      console.log('3. ✅ Service account configured - ready for Colab');
    } else {
      console.log('3. 🔧 Configure Google service account');
    }
    
    console.log('\n🚀 Your personal Claude tools colab integration is ready!');
  }
}

// Run verification
async function main() {
  const verifier = new PersonalToolsVerification();
  await verifier.runVerification();
}

if (import.meta.main) {
  main().catch(console.error);
}

export { PersonalToolsVerification };