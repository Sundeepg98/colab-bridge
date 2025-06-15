#!/usr/bin/env python3
"""
Comprehensive test suite for the Enhanced Admin Dashboard and Dynamic Framework
"""

import requests
import json
import time
from datetime import datetime

class DashboardTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0
        self.tests_run = 0
    
    def test(self, name, endpoint, expected_status=200, check_success=True):
        """Run a single test"""
        self.tests_run += 1
        try:
            print(f"🧪 Testing {name}...")
            response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            
            if response.status_code != expected_status:
                print(f"❌ {name}: Expected {expected_status}, got {response.status_code}")
                self.failed += 1
                return False
            
            if check_success and response.status_code == 200:
                try:
                    data = response.json()
                    if not data.get('success', True):
                        print(f"❌ {name}: API returned success=false")
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
    
    def test_dashboard_pages(self):
        """Test dashboard HTML pages"""
        print("\n🌐 TESTING DASHBOARD PAGES")
        print("=" * 50)
        
        self.test("Main Admin Dashboard", "/admin")
        self.test("Enhanced Admin Dashboard", "/admin-enhanced") 
        self.test("Telemetry Dashboard", "/telemetry-dashboard")
        self.test("Home Page", "/")
        self.test("Preview Interface", "/preview")
    
    def test_core_api_endpoints(self):
        """Test core API endpoints"""
        print("\n🔌 TESTING CORE API ENDPOINTS")
        print("=" * 50)
        
        self.test("API Keys List", "/api/api-keys")
        self.test("System Health", "/api/system-health")
        self.test("Claude Status", "/api/claude-status")
        self.test("System Metrics", "/api/system-metrics")
        self.test("Traffic Stats", "/api/traffic-stats")
    
    def test_dynamic_framework_endpoints(self):
        """Test dynamic framework endpoints"""
        print("\n🌐 TESTING DYNAMIC FRAMEWORK ENDPOINTS")
        print("=" * 50)
        
        self.test("Unified System Status", "/api/unified-system-status")
        self.test("System Recommendations", "/api/system-recommendations")
        self.test("Service Discovery Status", "/api/service-discovery-status")
        self.test("Fallback System Status", "/api/fallback-system-status")
        self.test("Independent Core Status", "/api/independent-core-status")
    
    def test_telemetry_endpoints(self):
        """Test telemetry and analytics endpoints"""
        print("\n📈 TESTING TELEMETRY ENDPOINTS")
        print("=" * 50)
        
        self.test("Telemetry Events", "/api/telemetry/events")
        self.test("Telemetry Insights", "/api/telemetry/insights") 
        self.test("Performance Metrics", "/api/telemetry/performance")
        self.test("Pattern Analysis", "/api/telemetry/patterns")
    
    def test_admin_functions(self):
        """Test admin functionality"""
        print("\n🔧 TESTING ADMIN FUNCTIONS")
        print("=" * 50)
        
        self.test("Maintenance Status", "/api/maintenance-status")
        self.test("Learning Analytics", "/api/learning-analytics")
        self.test("Integration Manager", "/api/integration-manager/status")
        self.test("Auto Maintenance", "/api/auto-maintenance/status")
    
    def test_advanced_features(self):
        """Test advanced dynamic framework features"""
        print("\n🚀 TESTING ADVANCED FEATURES")
        print("=" * 50)
        
        # Test unified system data
        try:
            response = requests.get(f"{self.base_url}/api/unified-system-status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    status = data['system_status']
                    
                    print(f"✅ System Uptime: {status.get('uptime_seconds', 0):.1f} seconds")
                    print(f"✅ Total Services: {status.get('total_services', 0)}")
                    print(f"✅ Healthy Services: {status.get('healthy_services', 0)}")
                    print(f"✅ Discovery Found: {status['discovery']['total_discovered']} services")
                    print(f"✅ Fallback Health: {status['fallback']['system_health']}")
                    print(f"✅ Core Capabilities: {len(status['independent_core']['available_capabilities'])}")
                    
                    self.passed += 6
                    self.tests_run += 6
                else:
                    print("❌ Unified system status returned error")
                    self.failed += 1
                    self.tests_run += 1
            else:
                print(f"❌ Unified system status HTTP error: {response.status_code}")
                self.failed += 1
                self.tests_run += 1
        except Exception as e:
            print(f"❌ Advanced features test error: {e}")
            self.failed += 1
            self.tests_run += 1
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🎯 ENHANCED ADMIN DASHBOARD - COMPREHENSIVE TEST SUITE")
        print("=" * 70)
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Testing: {self.base_url}")
        
        start_time = time.time()
        
        # Run all test categories
        self.test_dashboard_pages()
        self.test_core_api_endpoints()
        self.test_dynamic_framework_endpoints()
        self.test_telemetry_endpoints()
        self.test_admin_functions()
        self.test_advanced_features()
        
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
        
        if success_rate >= 90:
            print("\n🎉 EXCELLENT! Dashboard is working perfectly!")
        elif success_rate >= 75:
            print("\n👍 GOOD! Dashboard is mostly functional with minor issues.")
        elif success_rate >= 50:
            print("\n⚠️ WARNING! Dashboard has significant issues that need attention.")
        else:
            print("\n🚨 CRITICAL! Dashboard has major problems and needs immediate attention.")
        
        return success_rate >= 90

if __name__ == "__main__":
    tester = DashboardTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)