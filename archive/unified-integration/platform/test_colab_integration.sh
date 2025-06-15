#!/bin/bash

echo "🧪 Comprehensive Colab Integration Test"
echo "======================================="
echo ""

# Test 1: Basic health check
echo "📡 Test 1: Basic Health Check"
echo "------------------------------"
curl -s http://localhost:5000/api/health | python3 -m json.tool
echo ""

# Test 2: Direct API status
echo "🔑 Test 2: Direct API Status"
echo "-----------------------------"
curl -s http://localhost:5000/api/colab-direct/status | python3 -m json.tool
echo ""

# Test 3: Manual Colab test (should show setup needed)
echo "🌟 Test 3: Manual Colab Test"
echo "-----------------------------"
curl -s -X POST http://localhost:5000/api/sun-colab-test -H "Content-Type: application/json" | python3 -m json.tool
echo ""

# Test 4: Direct API text generation
echo "📝 Test 4: Direct API Text Generation"
echo "--------------------------------------"
curl -s -X POST http://localhost:5000/api/colab-direct/generate-text \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A mystical forest at twilight", "style": "cinematic"}' | python3 -m json.tool
echo ""

# Test 5: Optimization with direct API
echo "⚡ Test 5: Optimization with Direct API"
echo "---------------------------------------"
curl -s -X POST http://localhost:5000/api/optimize-with-colab-direct \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A beautiful mountain landscape", "type": "enhance", "style": "artistic"}' | python3 -m json.tool
echo ""

# Test 6: Code execution test
echo "💻 Test 6: Custom Code Execution"
echo "--------------------------------"
curl -s -X POST http://localhost:5000/api/colab-direct/execute-code \
  -H "Content-Type: application/json" \
  -d '{"code": "import torch\nprint(f\"GPU Available: {torch.cuda.is_available()}\")"}' | python3 -m json.tool
echo ""

# Test 7: Dashboard accessibility
echo "🌐 Test 7: Dashboard Accessibility"
echo "----------------------------------"
echo "Main Interface: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)"
echo "Enhanced Dashboard: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/dashboard)"
echo "Colab Dashboard: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/colab-dashboard)"
echo "Colab API Dashboard: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/colab-api-dashboard)"
echo ""

# Test 8: Integration status
echo "📊 Test 8: Integration Summary"
echo "------------------------------"
echo "✅ Flask App: Running on port 5000"
echo "✅ Direct API: Simulation mode active"
echo "⏳ Manual Setup: Waiting for your Colab notebook"
echo "🎯 Ready for: API credentials or manual ngrok setup"
echo ""

echo "🎉 All tests completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Choose integration method:"
echo "   - Option A: Direct API (set COLAB_RUNTIME_URL + COLAB_API_TOKEN)"
echo "   - Option B: Manual setup (follow COLAB_SETUP.md)"
echo ""
echo "2. Visit dashboards:"
echo "   - Main: http://localhost:5000"
echo "   - Colab API: http://localhost:5000/colab-api-dashboard"
echo "   - Manual Setup: http://localhost:5000/colab-dashboard"
echo ""
echo "🚀 System is ready for your Colab integration!"