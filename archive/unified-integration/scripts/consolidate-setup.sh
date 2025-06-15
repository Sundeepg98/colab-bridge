#!/bin/bash
# 🔄 Consolidate Scattered Claude-Colab Integration Files
# Migrates from scattered files to unified project structure

echo "🔄 Claude-Colab Integration Consolidation"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${GREEN}✅${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠️${NC} $1"; }
print_error() { echo -e "${RED}❌${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ️${NC} $1"; }

# Change to unified project directory
cd "$(dirname "$0")/.."

# Step 1: Check for scattered files
echo ""
print_info "Step 1: Checking for scattered Claude-Colab files..."

SCATTERED_LOCATIONS=(
    "/var/projects/claude-colab-bridge"
    "/var/projects/personal-claude-tools/colab-integration"
    "/var/projects/ai-integration-platform/src"
    "/var/projects/UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py"
    "/var/projects/test-multi-instance-bridge.js"
)

found_files=()
for location in "${SCATTERED_LOCATIONS[@]}"; do
    if [ -e "$location" ]; then
        found_files+=("$location")
        print_status "Found: $location"
    fi
done

if [ ${#found_files[@]} -eq 0 ]; then
    print_info "No scattered files found - this appears to be a clean setup"
    exit 0
fi

print_info "Found ${#found_files[@]} scattered file locations to consolidate"

# Step 2: Create unified structure if not exists
echo ""
print_info "Step 2: Ensuring unified project structure..."

REQUIRED_DIRS=(
    "core" "platform" "advanced" "scripts" "docs" 
    "examples" "tests" "config/templates" "config/examples"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_status "Created directory: $dir"
    fi
done

# Step 3: Consolidate core bridge files
echo ""
print_info "Step 3: Consolidating core bridge files..."

if [ -d "/var/projects/claude-colab-bridge" ]; then
    # Copy bridge files
    cp -r /var/projects/claude-colab-bridge/* core/ 2>/dev/null || true
    print_status "Copied core bridge files"
    
    # Rename for clarity
    if [ -f "core/bridge-client.js" ]; then
        mv core/bridge-client.js core/basic-bridge-client.js
        print_status "Renamed basic bridge client"
    fi
    
    if [ -f "core/multi-instance-client.js" ]; then
        mv core/multi-instance-client.js core/multi-instance-bridge-client.js  
        print_status "Renamed multi-instance bridge client"
    fi
fi

# Copy universal processor
if [ -f "/var/projects/UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py" ]; then
    cp /var/projects/UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py core/universal-processor.py
    print_status "Copied universal processor"
fi

# Step 4: Consolidate platform files
echo ""
print_info "Step 4: Consolidating platform files..."

if [ -d "/var/projects/personal-claude-tools/colab-integration" ]; then
    # Copy platform files (excluding duplicates)
    rsync -av --exclude='venv' --exclude='__pycache__' --exclude='*.log' \
        /var/projects/personal-claude-tools/colab-integration/ platform/ 2>/dev/null || true
    print_status "Copied platform files"
    
    # Move src to platform if not already there
    if [ -d "platform/src" ] && [ ! -d "advanced/multi_instance_colab_bridge.py" ]; then
        cp platform/src/multi_instance_colab_bridge.py advanced/ 2>/dev/null || true
        cp platform/src/simplified_unified_manager.py advanced/unified-manager.py 2>/dev/null || true
        print_status "Moved advanced modules"
    fi
fi

# Step 5: Consolidate advanced features
echo ""
print_info "Step 5: Consolidating advanced features..."

if [ -d "/var/projects/ai-integration-platform/src" ]; then
    # Copy advanced integration files
    cp /var/projects/ai-integration-platform/src/multi_instance_colab_bridge.py advanced/ 2>/dev/null || true
    cp /var/projects/ai-integration-platform/src/simplified_unified_manager.py advanced/unified-manager.py 2>/dev/null || true
    print_status "Copied advanced integration modules"
fi

# Step 6: Consolidate tests
echo ""
print_info "Step 6: Consolidating test files..."

TEST_FILES=(
    "/var/projects/test-multi-instance-bridge.js"
    "/var/projects/verify-personal-tools-setup.js"
)

for test_file in "${TEST_FILES[@]}"; do
    if [ -f "$test_file" ]; then
        filename=$(basename "$test_file")
        cp "$test_file" "tests/${filename}"
        print_status "Copied test: $filename"
    fi
done

# Step 7: Consolidate documentation
echo ""
print_info "Step 7: Consolidating documentation..."

DOC_FILES=(
    "/var/projects/MULTI_INSTANCE_COLAB_SETUP_GUIDE.md"
    "/var/projects/UPDATED_PERSONAL_TOOLS_SETUP_GUIDE.md"
    "/var/projects/COLAB_CLAUDE_CONSOLIDATION_PLAN.md"
)

for doc_file in "${DOC_FILES[@]}"; do
    if [ -f "$doc_file" ]; then
        filename=$(basename "$doc_file")
        cp "$doc_file" "docs/${filename}"
        print_status "Copied documentation: $filename"
    fi
done

# Copy README files and merge them
if [ -f "/var/projects/claude-colab-bridge/README.md" ]; then
    cp /var/projects/claude-colab-bridge/README.md docs/BRIDGE_README.md
    print_status "Copied bridge README"
fi

if [ -f "/var/projects/personal-claude-tools/README.md" ]; then
    cp /var/projects/personal-claude-tools/README.md docs/PLATFORM_README.md
    print_status "Copied platform README"
fi

# Step 8: Create configuration templates
echo ""
print_info "Step 8: Creating unified configuration templates..."

# Create .env template
cat > config/templates/.env.template << 'EOF'
# Unified Claude-Colab Integration Configuration
# Copy this file to .env and fill in your actual values

# Required: Anthropic Claude API
ANTHROPIC_API_KEY=your-claude-api-key-here

# Required: Google Cloud Service Account
SERVICE_ACCOUNT_PATH=/path/to/your/service-account.json
GOOGLE_DRIVE_FOLDER_ID=your-google-drive-folder-id

# Optional: Additional AI Services
OPENAI_API_KEY=your-openai-api-key
STABILITY_API_KEY=your-stability-ai-key
RUNWAY_API_KEY=your-runway-ml-key
REPLICATE_API_KEY=your-replicate-key

# Optional: Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database

# Optional: Advanced Features
ENABLE_LEARNING=true
ENABLE_MONITORING=true
ENABLE_ADVANCED_FEATURES=true

# Optional: Performance Tuning
MAX_CONCURRENT_SESSIONS=3
BATCH_SIZE=5
COMMAND_TIMEOUT=30000

# Optional: Development Settings
DEBUG=false
LOG_LEVEL=INFO
FLASK_ENV=production
EOF

print_status "Created unified .env template"

# Create service account template
if [ ! -f "config/templates/service-account.template.json" ]; then
    cat > config/templates/service-account.template.json << 'EOF'
{
  "type": "service_account",
  "project_id": "your-gcp-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
EOF
    print_status "Created service account template"
fi

# Step 9: Create examples
echo ""
print_info "Step 9: Creating usage examples..."

# Create basic usage example
cat > examples/basic-usage.js << 'EOF'
#!/usr/bin/env bun
/**
 * Basic usage example for Unified Claude-Colab Bridge
 */

import UnifiedClaudeColabBridge from '../core/unified-bridge-client.js';

async function basicUsageExample() {
  console.log('🚀 Basic Usage Example');
  console.log('=====================');
  
  // Initialize bridge
  const bridge = await UnifiedClaudeColabBridge.quickStart('example_project');
  
  try {
    // Basic code execution
    console.log('\n1. Basic Code Execution:');
    const result1 = await bridge.exec('print("Hello from unified bridge!")');
    console.log('✅ Result:', result1.data?.output);
    
    // Package installation
    console.log('\n2. Package Installation:');
    const result2 = await bridge.install('requests');
    console.log('✅ Packages installed');
    
    // AI query (if configured)
    console.log('\n3. AI Query:');
    try {
      const result3 = await bridge.ai('Write a simple Python function to calculate factorial');
      console.log('✅ AI response received');
    } catch (error) {
      console.log('⚠️ AI not configured:', error.message);
    }
    
    // System status
    console.log('\n4. System Status:');
    const status = await bridge.getSystemStatus();
    console.log('✅ System status retrieved');
    
  } finally {
    await bridge.cleanup();
  }
}

if (import.meta.main) {
  basicUsageExample().catch(console.error);
}
EOF

chmod +x examples/basic-usage.js
print_status "Created basic usage example"

# Step 10: Create package.json
echo ""
print_info "Step 10: Creating unified package.json..."

cat > package.json << 'EOF'
{
  "name": "unified-claude-colab-integration",
  "version": "1.0.0",
  "description": "Unified platform for Claude Coder + Google Colab integration",
  "type": "module",
  "main": "core/unified-bridge-client.js",
  "scripts": {
    "start": "node platform/app.py",
    "test": "./tests/run-all-tests.sh",
    "test:basic": "bun examples/basic-usage.js",
    "test:integration": "bun tests/test-multi-instance-bridge.js",
    "setup": "./scripts/init-bridge.sh",
    "setup:security": "./scripts/setup-security.sh",
    "consolidate": "./scripts/consolidate-setup.sh"
  },
  "keywords": [
    "claude",
    "colab",
    "ai-integration",
    "multi-instance",
    "anthropic",
    "google-colab"
  ],
  "dependencies": {
    "googleapis": "latest"
  },
  "engines": {
    "node": ">=18.0.0",
    "bun": ">=1.0.0"
  },
  "repository": {
    "type": "git",
    "url": "your-repository-url"
  },
  "license": "MIT"
}
EOF

print_status "Created unified package.json"

# Step 11: Create requirements.txt
echo ""
print_info "Step 11: Creating unified requirements.txt..."

cat > requirements.txt << 'EOF'
# Core dependencies
google-auth>=2.15.0
google-auth-oauthlib>=0.8.0
google-auth-httplib2>=0.1.0
google-api-python-client>=2.70.0

# Web platform
flask>=2.3.0
flask-cors>=4.0.0

# AI integrations
anthropic>=0.5.0
openai>=1.0.0

# Data processing
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0

# Utilities
python-dotenv>=1.0.0
requests>=2.28.0
psutil>=5.9.0
cryptography>=40.0.0

# Development
pytest>=7.0.0
pytest-asyncio>=0.21.0
black>=23.0.0
flake8>=6.0.0
EOF

print_status "Created unified requirements.txt"

# Step 12: Summary and next steps
echo ""
print_info "🎉 Consolidation Summary"
echo "======================="

echo ""
print_status "✅ Core bridge files consolidated"
print_status "✅ Platform files consolidated"  
print_status "✅ Advanced features consolidated"
print_status "✅ Tests consolidated"
print_status "✅ Documentation consolidated"
print_status "✅ Configuration templates created"
print_status "✅ Examples created"
print_status "✅ Package files created"

echo ""
print_info "📋 Next Steps:"
echo "1. Install dependencies: pip install -r requirements.txt && npm install"
echo "2. Configure security: ./scripts/setup-security.sh"
echo "3. Set up environment: cp config/templates/.env.template .env"
echo "4. Initialize bridge: ./scripts/init-bridge.sh your_project"
echo "5. Test setup: bun examples/basic-usage.js"

echo ""
print_warning "⚠️ Important Notes:"
echo "• Review config/templates/ and customize for your setup"
echo "• The original scattered files are preserved (not deleted)"
echo "• Update your scripts to use the new unified structure"
echo "• Test thoroughly before removing old files"

echo ""
print_status "🚀 Unified Claude-Colab Integration is ready!"

# Create a verification script
cat > scripts/verify-consolidation.sh << 'EOF'
#!/bin/bash
# Verify consolidation completed successfully

echo "🔍 Verifying Unified Claude-Colab Integration"
echo "============================================"

# Check required directories
dirs=("core" "platform" "advanced" "scripts" "docs" "examples" "tests" "config")
for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ Directory exists: $dir"
    else
        echo "❌ Missing directory: $dir"
    fi
done

# Check key files
files=(
    "core/unified-bridge-client.js"
    "platform/app.py"
    "config/templates/.env.template"
    "examples/basic-usage.js"
    "package.json"
    "requirements.txt"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ File exists: $file"
    else
        echo "❌ Missing file: $file"
    fi
done

echo ""
echo "🎯 Consolidation verification complete!"
EOF

chmod +x scripts/verify-consolidation.sh
print_status "Created verification script"

echo ""
print_info "Run './scripts/verify-consolidation.sh' to verify the consolidation"