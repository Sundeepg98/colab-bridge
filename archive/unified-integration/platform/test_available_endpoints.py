#!/usr/bin/env python3
"""
Test Suite for Available AI Platform Endpoints
Tests the endpoints that are actually implemented in the application
"""

import requests
import json
import time
from datetime import datetime

class AvailableEndpointsTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0
        self.tests_run = 0
        self.detailed_results = []
    
    def test(self, name, endpoint, method="GET", data=None, expected_status=200, check_success=True):
        """Run a single test"""
        self.tests_run += 1
        try:
            print(f"🧪 Testing {name}...")
            
            if method == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            elif method == "POST":
                headers = {'Content-Type': 'application/json'}
                response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(f"{self.base_url}{endpoint}", timeout=10)
            
            if response.status_code != expected_status:
                print(f"❌ {name}: Expected {expected_status}, got {response.status_code}")
                self.failed += 1
                return False
            
            if check_success and response.status_code == 200:
                try:
                    data = response.json()
                    if not data.get('success', True):
                        print(f"❌ {name}: API returned success=false")
                        print(f"   Error: {data.get('error', 'Unknown error')}")
                        self.failed += 1
                        return False
                except:
                    pass  # Not all endpoints return JSON
            
            print(f"✅ {name}: PASSED")
            self.passed += 1
            return True
            
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")
            self.failed += 1
            return False
    
    def test_health_endpoints(self):
        """Test basic health check endpoints"""
        print("\n🏥 TESTING HEALTH ENDPOINTS")
        print("=" * 50)
        
        self.test("Basic Health Check", "/api/health")
        self.test("System Health", "/api/system-health")
        self.test("Claude Status", "/api/claude-status")
    
    def test_api_key_management(self):
        """Test API key management endpoints"""
        print("\n🔑 TESTING API KEY MANAGEMENT")
        print("=" * 50)
        
        self.test("List API Keys", "/api/api-keys")
        
        # Test adding an API key
        test_key_data = {
            "integration_name": "test_integration",
            "api_key": "test-key-12345",
            "base_url": "https://api.test.com",
            "models": ["test-model"],
            "enabled": True
        }
        self.test("Add API Key", "/api/api-keys", method="POST", data=test_key_data)
        
        # Test toggling API key
        toggle_data = {"enabled": False}
        self.test("Toggle API Key", "/api/api-keys/test_integration/toggle", method="POST", data=toggle_data)
        
        # Test API key validation
        self.test("Test API Key", "/api/api-keys/test_integration/test", method="POST")
        
        # Clean up - delete test key
        self.test("Delete API Key", "/api/api-keys/test_integration", method="DELETE")
    
    def test_maintenance_endpoints(self):
        """Test maintenance and monitoring endpoints"""
        print("\n🔧 TESTING MAINTENANCE ENDPOINTS")
        print("=" * 50)
        
        self.test("Maintenance Status", "/api/maintenance-status")
        self.test("Maintenance Report", "/api/maintenance-report?hours=24")
        
        # Test maintenance toggle
        toggle_data = {"enabled": True}
        self.test("Toggle Auto-Maintenance", "/api/maintenance/toggle", method="POST", data=toggle_data)
    
    def test_telemetry_endpoints(self):
        """Test telemetry endpoints"""
        print("\n📊 TESTING TELEMETRY ENDPOINTS")
        print("=" * 50)
        
        self.test("Export Telemetry", "/api/telemetry-export?hours=24")
        self.test("Telemetry Insights", "/api/telemetry-insights?limit=10")
        
        # Test telemetry analysis
        self.test("Analyze Telemetry", "/api/telemetry-analyze", method="POST", data={})
    
    def test_dashboard_pages(self):
        """Test dashboard HTML pages"""
        print("\n🌐 TESTING DASHBOARD PAGES")
        print("=" * 50)
        
        self.test("Home Page", "/", check_success=False)
        self.test("Admin Dashboard", "/admin", check_success=False)
        self.test("Enhanced Admin Dashboard", "/admin-enhanced", check_success=False)
        self.test("Telemetry Dashboard", "/telemetry-dashboard", check_success=False)
        self.test("Integration Quickstart", "/integration-quickstart", check_success=False)
        self.test("Preview Interface", "/preview", check_success=False)
    
    def test_dynamic_framework_endpoints(self):
        """Test dynamic framework endpoints if available"""
        print("\n🚀 TESTING DYNAMIC FRAMEWORK ENDPOINTS")
        print("=" * 50)
        
        self.test("Unified System Status", "/api/unified-system-status")
        self.test("System Recommendations", "/api/system-recommendations")
        self.test("Service Discovery Status", "/api/service-discovery-status")
        self.test("Fallback System Status", "/api/fallback-system-status")
        self.test("Independent Core Status", "/api/independent-core-status")
    
    def test_integration_endpoints(self):
        """Test integration-related endpoints"""
        print("\n🔌 TESTING INTEGRATION ENDPOINTS")
        print("=" * 50)
        
        self.test("Test All Integrations", "/api/integration-test-all", method="POST")
        self.test("Notification Subscribe", "/api/notifications/subscribe", method="POST")
    
    def test_optimization_endpoints(self):
        """Test optimization endpoints"""
        print("\n⚡ TESTING OPTIMIZATION ENDPOINTS")
        print("=" * 50)
        
        # Test basic optimization
        test_data = {
            "prompt": "This is a test prompt for optimization",
            "optimization_type": "smart"
        }
        self.test("Optimize Prompt", "/api/optimize", method="POST", data=test_data)
        
        # Test smart optimization
        self.test("Smart Optimize", "/api/smart-optimize", method="POST", data=test_data)
    
    def test_claude_endpoints(self):
        """Test Claude-specific endpoints"""
        print("\n🤖 TESTING CLAUDE ENDPOINTS")
        print("=" * 50)
        
        # Test Claude enhancement
        test_data = {
            "prompt": "Test prompt for Claude enhancement",
            "context": {"intent": "testing"}
        }
        self.test("Enhance Prompt", "/api/enhance", method="POST", data=test_data)
    
    def run_all_tests(self):
        """Run all available tests"""
        print("🎯 AI PLATFORM - AVAILABLE ENDPOINTS TEST SUITE")
        print("=" * 70)
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Testing: {self.base_url}")
        
        start_time = time.time()
        
        # Run all test categories
        self.test_health_endpoints()
        self.test_api_key_management()
        self.test_maintenance_endpoints()
        self.test_telemetry_endpoints()
        self.test_dashboard_pages()
        self.test_dynamic_framework_endpoints()
        self.test_integration_endpoints()
        self.test_optimization_endpoints()
        self.test_claude_endpoints()
        
        # Calculate results
        end_time = time.time()
        duration = end_time - start_time
        success_rate = (self.passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        # Print final results
        print("\n" + "=" * 70)
        print("🎊 TEST RESULTS SUMMARY")
        print("=" * 70)
        print(f"📊 Tests Run: {self.tests_run}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"⏱️ Duration: {duration:.2f} seconds")
        
        # Save results
        results = {
            'summary': {
                'total_tests': self.tests_run,
                'passed': self.passed,
                'failed': self.failed,
                'success_rate': success_rate,
                'duration': duration,
                'timestamp': datetime.now().isoformat()
            },
            'base_url': self.base_url
        }
        
        with open('available_endpoints_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results saved to: available_endpoints_test_results.json")
        
        if success_rate >= 90:
            print("\n🎉 EXCELLENT! Available endpoints are working perfectly!")
        elif success_rate >= 75:
            print("\n👍 GOOD! Most endpoints are functional with minor issues.")
        elif success_rate >= 50:
            print("\n⚠️ WARNING! Several endpoints have issues that need attention.")
        else:
            print("\n🚨 CRITICAL! Many endpoints are failing and need immediate attention.")
        
        return success_rate >= 75


if __name__ == "__main__":
    tester = AvailableEndpointsTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)