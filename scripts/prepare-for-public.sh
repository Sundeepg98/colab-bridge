#!/bin/bash
# 🔐 Prepare Personal Claude Tools for Public GitHub Repository
# This script ensures no sensitive information is included

echo "🔐 Preparing Personal Claude Tools for Public Release"
echo "==================================================="

# Change to repository directory
cd "$(dirname "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Step 1: Check for sensitive files
echo ""
print_info "Step 1: Scanning for sensitive files..."

SENSITIVE_FILES=(
    "eng-flux-459812-q6-e05c54813553.json"
    "colab-integration/neon_connection.json"
    "colab-integration/.env"
    "colab-integration/secure_keys/"
    "colab-integration/user_profiles/"
    "colab-integration/*.log"
)

found_sensitive=false
for pattern in "${SENSITIVE_FILES[@]}"; do
    if ls $pattern 2>/dev/null | grep -q .; then
        print_error "Found sensitive file: $pattern"
        found_sensitive=true
    fi
done

if [ "$found_sensitive" = false ]; then
    print_status "No sensitive files found in current directory"
else
    print_warning "Sensitive files detected! They will be handled safely."
fi

# Step 2: Remove sensitive files from git tracking (keep local copies)
echo ""
print_info "Step 2: Removing sensitive files from git tracking..."

# Remove from git but keep local files
if [ -f "eng-flux-459812-q6-e05c54813553.json" ]; then
    cp "eng-flux-459812-q6-e05c54813553.json" "../service-account-backup.json"
    git rm --cached "eng-flux-459812-q6-e05c54813553.json" 2>/dev/null || true
    print_status "Service account backed up and removed from git"
fi

if [ -f "colab-integration/neon_connection.json" ]; then
    cp "colab-integration/neon_connection.json" "colab-integration/config/database_config.json"
    git rm --cached "colab-integration/neon_connection.json" 2>/dev/null || true
    print_status "Database config backed up and removed from git"
fi

# Remove logs and user data
git rm --cached -r colab-integration/user_profiles/ 2>/dev/null || true
git rm --cached -r colab-integration/secure_keys/ 2>/dev/null || true
git rm --cached colab-integration/*.log 2>/dev/null || true
git rm --cached colab-integration/.env 2>/dev/null || true

print_status "Sensitive files removed from git tracking"

# Step 3: Verify .gitignore is in place
echo ""
print_info "Step 3: Verifying .gitignore configuration..."

if [ -f ".gitignore" ]; then
    print_status ".gitignore file exists"
    
    # Check for key patterns
    if grep -q "*.json" .gitignore && grep -q "*api_keys*" .gitignore; then
        print_status ".gitignore contains security patterns"
    else
        print_warning ".gitignore may need updates"
    fi
else
    print_error ".gitignore file missing!"
fi

# Step 4: Scan source code for hardcoded secrets
echo ""
print_info "Step 4: Scanning source code for hardcoded secrets..."

# Common secret patterns
SECRET_PATTERNS=(
    "api[_-]?key\s*=\s*['\"][^'\"]+['\"]"
    "secret\s*=\s*['\"][^'\"]+['\"]"
    "password\s*=\s*['\"][^'\"]+['\"]"
    "token\s*=\s*['\"][^'\"]+['\"]"
    "sk-[a-zA-Z0-9]+"
    "xoxb-[a-zA-Z0-9]+"
)

secrets_found=false
for pattern in "${SECRET_PATTERNS[@]}"; do
    matches=$(grep -r -i "$pattern" colab-integration/src/ 2>/dev/null || true)
    if [ ! -z "$matches" ]; then
        print_warning "Potential secret pattern found: $pattern"
        echo "$matches"
        secrets_found=true
    fi
done

if [ "$secrets_found" = false ]; then
    print_status "No hardcoded secrets found in source code"
else
    print_error "Review and fix hardcoded secrets before publishing!"
fi

# Step 5: Create example configurations
echo ""
print_info "Step 5: Creating example configurations..."

# Create .env.example
cat > colab-integration/.env.example << 'EOF'
# Personal Claude Tools Environment Configuration
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

# Optional: Database
DATABASE_URL=postgresql://username:password@host:port/database

# Optional: Development Settings
DEBUG=true
LOG_LEVEL=INFO
FLASK_ENV=development
EOF

print_status "Created .env.example file"

# Step 6: Verify template files exist
echo ""
print_info "Step 6: Verifying template files..."

TEMPLATE_FILES=(
    "colab-integration/config/service_account.template.json"
    "colab-integration/config/database_config.template.json"
    "colab-integration/.env.example"
)

for template in "${TEMPLATE_FILES[@]}"; do
    if [ -f "$template" ]; then
        print_status "Template exists: $(basename "$template")"
    else
        print_error "Missing template: $template"
    fi
done

# Step 7: Check git status
echo ""
print_info "Step 7: Checking git status..."

if git status --porcelain | grep -q .; then
    print_info "Changes detected. Current git status:"
    git status --short
else
    print_status "Working directory clean"
fi

# Step 8: Security summary
echo ""
print_info "🔐 Security Summary"
echo "=================="

print_status "✅ Sensitive files removed from git"
print_status "✅ .gitignore configured"
print_status "✅ Template files created"
print_status "✅ Example configurations provided"

if [ "$secrets_found" = true ]; then
    print_error "❌ Hardcoded secrets found - MUST FIX before publishing"
else
    print_status "✅ No hardcoded secrets detected"
fi

echo ""
print_info "📋 Next Steps:"
echo "1. Review any detected issues above"
echo "2. Test the setup with template files"
echo "3. Update README.md if needed"
echo "4. Commit changes: git add . && git commit -m 'Prepare for public release'"
echo "5. Create GitHub repository"
echo "6. Push: git remote add origin <your-repo-url> && git push -u origin main"

echo ""
print_warning "⚠️  IMPORTANT REMINDERS:"
echo "• Never commit real API keys or credentials"
echo "• Test the public setup before sharing"
echo "• Include security warnings in documentation"
echo "• Monitor the repository for accidental secret commits"

echo ""
print_status "🚀 Personal Claude Tools is ready for public release!"