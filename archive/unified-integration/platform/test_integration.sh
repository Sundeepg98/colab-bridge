#!/bin/bash

echo "🧪 Testing Sun Colab Integration"
echo "================================"

# Test 1: Connection test
echo "📡 Test 1: Connection Test"
curl -s -X POST http://localhost:5000/api/sun-colab-test -H "Content-Type: application/json" | python3 -m json.tool
echo ""

# Test 2: Text enhancement
echo "🎨 Test 2: Text Enhancement"
curl -s -X POST http://localhost:5000/api/sun-colab-enhance \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A mystical forest at twilight", "style": "cinematic"}' | python3 -m json.tool
echo ""

# Test 3: Dashboard status
echo "📊 Test 3: Dashboard Status"
curl -s http://localhost:5000/api/colab/status | python3 -m json.tool
echo ""

echo "✅ Integration tests complete!"
echo "Visit http://localhost:5000/colab-dashboard to see the full dashboard"