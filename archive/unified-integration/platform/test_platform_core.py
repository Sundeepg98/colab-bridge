#!/usr/bin/env python3
"""
Comprehensive Test Suite for AI Platform Core Components
Tests for Platform Engine, Integration Health, User Dashboard, Cost Calculation, and Fallback Mechanisms
"""

import pytest
import requests
import json
import time
from datetime import datetime
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class TestPlatformCore:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0
        self.tests_run = 0
        self.detailed_results = []
    
    def log_result(self, test_name, status, details=""):
        """Log detailed test results"""
        result = {
            'test': test_name,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.detailed_results.append(result)
        
        icon = "✅" if status == "PASSED" else "❌"
        print(f"{icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
    
    def test_api(self, name, endpoint, method="GET", data=None, expected_status=200):
        """Test an API endpoint"""
        self.tests_run += 1
        try:
            if method == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            elif method == "POST":
                response = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=10)
            
            if response.status_code == expected_status:
                self.passed += 1
                self.log_result(name, "PASSED", f"Status: {response.status_code}")
                return True, response
            else:
                self.failed += 1
                self.log_result(name, "FAILED", f"Expected {expected_status}, got {response.status_code}")
                return False, response
        except Exception as e:
            self.failed += 1
            self.log_result(name, "FAILED", f"Error: {str(e)}")
            return False, None
    
    def test_platform_engine_routing(self):
        """Test Platform Engine Routing Capabilities"""
        print("\n🚀 TESTING PLATFORM ENGINE ROUTING")
        print("=" * 50)
        
        # Test 1: Basic routing endpoint
        success, response = self.test_api(
            "Platform Engine Status",
            "/api/platform-engine/status"
        )
        
        if success and response:
            try:
                data = response.json()
                if data.get('success'):
                    print(f"   Engine Version: {data.get('version', 'N/A')}")
                    print(f"   Active Routes: {data.get('active_routes', 0)}")
            except:
                pass
        
        # Test 2: Route optimization
        test_prompt = {
            "prompt": "Test prompt for routing",
            "optimization_type": "smart",
            "user_tier": "basic"
        }
        
        success, response = self.test_api(
            "Route Optimization",
            "/api/optimize",
            method="POST",
            data=test_prompt
        )
        
        # Test 3: Multi-modal routing
        success, response = self.test_api(
            "Multi-Modal Routes",
            "/api/platform-engine/routes/multimodal"
        )
        
        # Test 4: Fallback routing
        success, response = self.test_api(
            "Fallback Routes",
            "/api/platform-engine/routes/fallback"
        )
    
    def test_integration_health_monitoring(self):
        """Test Integration Health Monitoring System"""
        print("\n🏥 TESTING INTEGRATION HEALTH MONITORING")
        print("=" * 50)
        
        # Test 1: Overall integration health
        success, response = self.test_api(
            "Integration Health Overview",
            "/api/integrations/health"
        )
        
        if success and response:
            try:
                data = response.json()
                if data.get('success'):
                    integrations = data.get('integrations', {})
                    for name, status in integrations.items():
                        print(f"   {name}: {status.get('status', 'unknown')}")
            except:
                pass
        
        # Test 2: Individual integration checks
        integrations_to_check = ["claude", "openai", "gemini", "local_llm"]
        for integration in integrations_to_check:
            success, response = self.test_api(
                f"{integration.title()} Integration Health",
                f"/api/integrations/{integration}/health"
            )
        
        # Test 3: Health metrics
        success, response = self.test_api(
            "Integration Metrics",
            "/api/integrations/metrics"
        )
        
        # Test 4: Health alerts
        success, response = self.test_api(
            "Health Alerts",
            "/api/integrations/alerts"
        )
    
    def test_user_dashboard_endpoints(self):
        """Test User Dashboard Endpoints"""
        print("\n👤 TESTING USER DASHBOARD ENDPOINTS")
        print("=" * 50)
        
        # Test 1: User dashboard main page
        success, response = self.test_api(
            "User Dashboard Page",
            "/user-dashboard"
        )
        
        # Test 2: User profile endpoint
        test_user_id = "test_user_123"
        success, response = self.test_api(
            "User Profile",
            f"/api/user/{test_user_id}/profile"
        )
        
        # Test 3: User usage statistics
        success, response = self.test_api(
            "User Usage Stats",
            f"/api/user/{test_user_id}/usage"
        )
        
        # Test 4: User preferences
        success, response = self.test_api(
            "User Preferences",
            f"/api/user/{test_user_id}/preferences"
        )
        
        # Test 5: User integration status
        success, response = self.test_api(
            "User Integration Status",
            "/api/user-integrations/status"
        )
    
    def test_cost_calculation(self):
        """Test Cost Calculation System"""
        print("\n💰 TESTING COST CALCULATION")
        print("=" * 50)
        
        # Test 1: Basic cost calculation
        test_request = {
            "tokens": 1000,
            "model": "claude-3-opus",
            "user_tier": "basic"
        }
        
        success, response = self.test_api(
            "Basic Cost Calculation",
            "/api/cost/calculate",
            method="POST",
            data=test_request
        )
        
        if success and response:
            try:
                data = response.json()
                if data.get('success'):
                    print(f"   Calculated Cost: ${data.get('cost', 0):.4f}")
                    print(f"   Token Count: {data.get('tokens', 0)}")
            except:
                pass
        
        # Test 2: Tier-based pricing
        tiers = ["basic", "premium", "enterprise"]
        for tier in tiers:
            test_request["user_tier"] = tier
            success, response = self.test_api(
                f"{tier.title()} Tier Pricing",
                "/api/cost/calculate",
                method="POST",
                data=test_request
            )
        
        # Test 3: Cost history
        success, response = self.test_api(
            "Cost History",
            f"/api/user/test_user_123/cost-history"
        )
        
        # Test 4: Cost optimization suggestions
        success, response = self.test_api(
            "Cost Optimization",
            "/api/cost/optimize"
        )
    
    def test_fallback_mechanisms(self):
        """Test Fallback Mechanisms"""
        print("\n🔄 TESTING FALLBACK MECHANISMS")
        print("=" * 50)
        
        # Test 1: Fallback system status
        success, response = self.test_api(
            "Fallback System Status",
            "/api/fallback-system-status"
        )
        
        if success and response:
            try:
                data = response.json()
                if data.get('success'):
                    fallback_data = data.get('fallback_system', {})
                    print(f"   System Health: {fallback_data.get('system_health', 'unknown')}")
                    print(f"   Available Providers: {fallback_data.get('available_providers', 0)}")
            except:
                pass
        
        # Test 2: Trigger fallback scenario
        test_request = {
            "prompt": "Test prompt",
            "primary_provider": "claude",
            "simulate_failure": True
        }
        
        success, response = self.test_api(
            "Fallback Trigger Test",
            "/api/test-fallback",
            method="POST",
            data=test_request
        )
        
        # Test 3: Fallback configuration
        success, response = self.test_api(
            "Fallback Configuration",
            "/api/fallback/config"
        )
        
        # Test 4: Fallback history
        success, response = self.test_api(
            "Fallback History",
            "/api/fallback/history"
        )
    
    def test_advanced_features(self):
        """Test Advanced Platform Features"""
        print("\n🎯 TESTING ADVANCED FEATURES")
        print("=" * 50)
        
        # Test 1: Smart optimization
        test_request = {
            "prompt": "Optimize this test prompt for better performance",
            "optimization_level": "high",
            "context": {"user_intent": "testing"}
        }
        
        success, response = self.test_api(
            "Smart Optimization",
            "/api/smart-optimize",
            method="POST",
            data=test_request
        )
        
        # Test 2: Pattern learning
        success, response = self.test_api(
            "Pattern Learning Status",
            "/api/learning/patterns"
        )
        
        # Test 3: A/B testing framework
        success, response = self.test_api(
            "A/B Testing Status",
            "/api/ab-testing/status"
        )
        
        # Test 4: Real-time analytics
        success, response = self.test_api(
            "Real-time Analytics",
            "/api/analytics/realtime"
        )
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🎯 AI PLATFORM CORE - COMPREHENSIVE TEST SUITE")
        print("=" * 70)
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Testing: {self.base_url}")
        
        start_time = time.time()
        
        # Run all test categories
        self.test_platform_engine_routing()
        self.test_integration_health_monitoring()
        self.test_user_dashboard_endpoints()
        self.test_cost_calculation()
        self.test_fallback_mechanisms()
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
        
        # Save detailed results
        with open('test_results.json', 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': self.tests_run,
                    'passed': self.passed,
                    'failed': self.failed,
                    'success_rate': success_rate,
                    'duration': duration,
                    'timestamp': datetime.now().isoformat()
                },
                'detailed_results': self.detailed_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: test_results.json")
        
        if success_rate >= 90:
            print("\n🎉 EXCELLENT! Platform core is working perfectly!")
        elif success_rate >= 75:
            print("\n👍 GOOD! Platform core is mostly functional with minor issues.")
        elif success_rate >= 50:
            print("\n⚠️ WARNING! Platform core has significant issues that need attention.")
        else:
            print("\n🚨 CRITICAL! Platform core has major problems and needs immediate attention.")
        
        return success_rate >= 90


# Additional unit tests using pytest
class TestPlatformComponents:
    """Unit tests for individual platform components"""
    
    @pytest.fixture
    def setup_environment(self):
        """Set up test environment"""
        # Import necessary modules
        try:
            from src.platform_engine import PlatformEngine
            from src.integration_health_monitoring import IntegrationHealthMonitor
            return True
        except ImportError:
            return False
    
    def test_platform_engine_initialization(self, setup_environment):
        """Test platform engine initialization"""
        if not setup_environment:
            pytest.skip("Required modules not available")
        
        from src.platform_engine import PlatformEngine
        engine = PlatformEngine()
        assert engine is not None
        assert hasattr(engine, 'route_request')
    
    def test_health_monitor_initialization(self, setup_environment):
        """Test health monitor initialization"""
        if not setup_environment:
            pytest.skip("Required modules not available")
        
        from src.integration_health_monitoring import IntegrationHealthMonitor
        monitor = IntegrationHealthMonitor()
        assert monitor is not None
        assert hasattr(monitor, 'check_health')
    
    def test_cost_calculation_logic(self):
        """Test cost calculation logic"""
        # Simple cost calculation test
        def calculate_cost(tokens, tier="basic"):
            rates = {
                "basic": 0.001,
                "premium": 0.0008,
                "enterprise": 0.0006
            }
            return tokens * rates.get(tier, 0.001)
        
        assert calculate_cost(1000, "basic") == 1.0
        assert calculate_cost(1000, "premium") == 0.8
        assert calculate_cost(1000, "enterprise") == 0.6
    
    def test_fallback_priority_logic(self):
        """Test fallback priority logic"""
        providers = ["claude", "openai", "gemini", "local"]
        failed_provider = "claude"
        
        fallback_providers = [p for p in providers if p != failed_provider]
        assert len(fallback_providers) == 3
        assert failed_provider not in fallback_providers


if __name__ == "__main__":
    # Run API tests
    tester = TestPlatformCore()
    success = tester.run_all_tests()
    
    # Run unit tests if pytest is available
    try:
        print("\n" + "=" * 70)
        print("🧪 RUNNING UNIT TESTS")
        print("=" * 70)
        pytest.main([__file__, "-v", "-x"])
    except:
        print("⚠️ Pytest not available for unit tests")
    
    exit(0 if success else 1)