#!/usr/bin/env bun
/**
 * Check what commands are waiting in Google Drive
 */

import { google } from 'googleapis';
import fs from 'fs';

const SERVICE_ACCOUNT_FILE = '/var/projects/eng-flux-459812-q6-e05c54813553.json';
const COLAB_FOLDER_ID = '1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z';

async function checkCommands() {
  console.log('📂 Checking commands in Google Drive');
  console.log('===================================\n');
  
  try {
    const credentials = JSON.parse(fs.readFileSync(SERVICE_ACCOUNT_FILE, 'utf8'));
    
    const auth = new google.auth.GoogleAuth({
      credentials,
      scopes: ['https://www.googleapis.com/auth/drive']
    });
    
    const drive = google.drive({ version: 'v3', auth });
    
    // List all command files
    const response = await drive.files.list({
      q: `name contains 'command_' and '${COLAB_FOLDER_ID}' in parents`,
      fields: 'files(id, name, createdTime)',
      orderBy: 'createdTime desc',
      pageSize: 20
    });
    
    const files = response.data.files || [];
    
    console.log(`📋 Found ${files.length} command(s) waiting:\n`);
    
    // Group by project
    const projects = {};
    
    for (const file of files) {
      // Extract project name from command ID
      const match = file.name.match(/command_([^_]+)_/);
      const project = match ? match[1] : 'unknown';
      
      if (!projects[project]) {
        projects[project] = [];
      }
      projects[project].push(file);
    }
    
    // Display by project
    for (const [project, commands] of Object.entries(projects)) {
      console.log(`📁 Project: ${project}`);
      commands.forEach(cmd => {
        const time = new Date(cmd.createdTime).toLocaleTimeString();
        console.log(`   • ${cmd.name} (created at ${time})`);
      });
      console.log('');
    }
    
    console.log('💡 These commands are waiting to be processed by Colab!');
    console.log('\n🎯 To process them:');
    console.log('1. Run UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py in Colab');
    console.log('2. Set the appropriate PROJECT_NAME');
    console.log('3. Commands will be processed automatically');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

checkCommands();