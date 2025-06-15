#!/usr/bin/env bun
/**
 * Simple test of Universal Colab Integration
 * Shows how any project can use the universal integration
 */

import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';

console.log('🧪 Testing Universal Colab Integration');
console.log('=====================================\n');

// Configuration - same for all projects
const SERVICE_ACCOUNT_FILE = '/var/projects/eng-flux-459812-q6-e05c54813553.json';
const COLAB_FOLDER_ID = '1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z';
const PROJECT_NAME = 'test_project';  // Different from movie booking!

async function demonstrateUniversalIntegration() {
  try {
    // Load service account
    const credentials = JSON.parse(fs.readFileSync(SERVICE_ACCOUNT_FILE, 'utf8'));
    
    // Authenticate
    const auth = new google.auth.GoogleAuth({
      credentials,
      scopes: ['https://www.googleapis.com/auth/drive']
    });
    
    const drive = google.drive({ version: 'v3', auth });
    
    // Create different types of commands
    const testCommands = [
      {
        id: `${PROJECT_NAME}_hello_${Date.now()}`,
        type: 'execute_code',
        code: `
# This is from a TEST project, not movie booking!
print("🧪 Testing Universal Integration")
print(f"Project: ${PROJECT_NAME}")
print("This proves any project can use the same Colab integration!")

# Do some calculations
result = sum([1, 2, 3, 4, 5])
print(f"Sum of [1,2,3,4,5] = {result}")
`,
        timestamp: new Date().toISOString()
      },
      {
        id: `${PROJECT_NAME}_shell_${Date.now()}`,
        type: 'shell_command',
        command: 'echo "Running shell command from test project" && pwd && ls -la',
        timestamp: new Date().toISOString()
      },
      {
        id: `${PROJECT_NAME}_ai_${Date.now()}`,
        type: 'ai_query',
        prompt: 'Write a haiku about universal integrations',
        timestamp: new Date().toISOString()
      }
    ];
    
    console.log(`📤 Sending ${testCommands.length} test commands...\n`);
    
    // Send each command
    for (const cmd of testCommands) {
      const fileMetadata = {
        name: `command_${cmd.id}.json`,
        parents: [COLAB_FOLDER_ID]
      };
      
      const media = {
        mimeType: 'application/json',
        body: JSON.stringify(cmd, null, 2)
      };
      
      await drive.files.create({
        resource: fileMetadata,
        media: media,
        fields: 'id,name'
      });
      
      console.log(`✅ Sent: ${cmd.type}`);
      console.log(`   ID: ${cmd.id}`);
    }
    
    console.log('\n📊 Test Summary:');
    console.log('================');
    console.log(`Project Name: ${PROJECT_NAME} (NOT movie booking!)`);
    console.log(`Commands Sent: ${testCommands.length}`);
    console.log(`Folder ID: ${COLAB_FOLDER_ID}`);
    
    console.log('\n🎯 To see these commands execute:');
    console.log('1. Open Google Colab');
    console.log('2. Copy contents of /var/projects/UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py');
    console.log(`3. Update: PROJECT_NAME = "${PROJECT_NAME}"`);
    console.log(`4. Update: SERVICE_ACCOUNT_FOLDER_ID = "${COLAB_FOLDER_ID}"`);
    console.log('5. Run the cell');
    
    console.log('\n✨ The same integration works for ANY project!');
    
    // Check if results exist
    console.log('\n🔍 Checking for results...');
    const results = await drive.files.list({
      q: `name contains 'result_${PROJECT_NAME}' and '${COLAB_FOLDER_ID}' in parents`,
      fields: 'files(id, name, createdTime)',
      pageSize: 10
    });
    
    if (results.data.files && results.data.files.length > 0) {
      console.log(`\n📥 Found ${results.data.files.length} result(s):`);
      for (const file of results.data.files) {
        console.log(`   • ${file.name}`);
      }
    } else {
      console.log('\n⏳ No results yet (Colab needs to be running)');
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

// Show universal integration location
console.log('📍 Universal Integration Location:');
console.log('   /var/projects/UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py\n');

// Run the test
demonstrateUniversalIntegration();