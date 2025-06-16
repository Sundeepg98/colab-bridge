#!/bin/bash
# Run all tests for Colab-Bridge

echo "🧪 Running Colab-Bridge Test Suite"
echo "=================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Set up environment
export SERVICE_ACCOUNT_PATH="$PWD/credentials/automation-engine-463103-ee5a06e18248.json"
export OWNER_EMAIL="sundeepg8@gmail.com"

# Track failures
FAILED=0

# 1. Python tests
echo -e "\n📦 Running Python tests..."
python3 tests/automated_test_suite.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python tests passed${NC}"
else
    echo -e "${RED}❌ Python tests failed${NC}"
    FAILED=1
fi

# 2. VS Code extension build test
echo -e "\n📦 Testing VS Code extension build..."
cd extensions/vscode
npm run compile > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ VS Code extension builds successfully${NC}"
else
    echo -e "${RED}❌ VS Code extension build failed${NC}"
    FAILED=1
fi
cd ../..

# 3. Quick integration test
echo -e "\n📦 Running integration test..."
python3 -c "
from colab_integration.universal_bridge import UniversalColabBridge
bridge = UniversalColabBridge('test')
print('Integration test passed')
" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Integration test passed${NC}"
else
    echo -e "${RED}❌ Integration test failed${NC}"
    FAILED=1
fi

# 4. Check for security issues
echo -e "\n🔒 Security check..."
# Check for hardcoded credentials
if grep -r "AIza\|ya29\|GOCSPX" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=archive --exclude-dir=.github --exclude="*.json" --exclude="run_tests.sh" > /dev/null 2>&1; then
    echo -e "${RED}❌ WARNING: Possible hardcoded credentials found${NC}"
    FAILED=1
else
    echo -e "${GREEN}✅ No hardcoded credentials found${NC}"
fi

# Summary
echo -e "\n=================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    echo "Ready for deployment 🚀"
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo "Please fix issues before deploying"
    exit 1
fi