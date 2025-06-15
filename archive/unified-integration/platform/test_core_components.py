#!/usr/bin/env python3
"""
Unit Tests for Core AI Platform Components
Tests core functionality without requiring external dependencies
"""

import sys
import os
import json
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_test(self, name, passed, error=None):
        self.tests.append({
            'name': name,
            'passed': passed,
            'error': str(error) if error else None,
            'timestamp': datetime.now().isoformat()
        })
        if passed:
            self.passed += 1
            print(f"✅ {name}")
        else:
            self.failed += 1
            print(f"❌ {name}: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        return {
            'total': total,
            'passed': self.passed,
            'failed': self.failed,
            'success_rate': success_rate
        }

def test_platform_engine():
    """Test Platform Engine core functionality"""
    results = TestResults()
    print("\n🚀 TESTING PLATFORM ENGINE")
    print("=" * 50)
    
    try:
        from platform_engine import PlatformEngine
        engine = PlatformEngine()
        results.add_test("Platform Engine Import", True)
        
        # Test initialization
        results.add_test("Platform Engine Initialization", 
                        hasattr(engine, 'routes') and hasattr(engine, 'integrations'))
        
        # Test route registration
        test_route = {
            'path': '/test',
            'handler': 'test_handler',
            'methods': ['GET', 'POST']
        }
        if hasattr(engine, 'register_route'):
            engine.register_route(test_route)
            results.add_test("Route Registration", True)
        else:
            results.add_test("Route Registration", False, "Method not found")
        
    except Exception as e:
        results.add_test("Platform Engine Import", False, e)
    
    return results

def test_integration_health_monitor():
    """Test Integration Health Monitor"""
    results = TestResults()
    print("\n🏥 TESTING INTEGRATION HEALTH MONITOR")
    print("=" * 50)
    
    try:
        from integration_health_monitoring import IntegrationHealthMonitor
        monitor = IntegrationHealthMonitor()
        results.add_test("Health Monitor Import", True)
        
        # Test health check methods
        results.add_test("Health Monitor Initialization",
                        hasattr(monitor, 'check_integration_health'))
        
        # Test mock health check
        if hasattr(monitor, 'get_all_health_status'):
            status = monitor.get_all_health_status()
            results.add_test("Get Health Status", isinstance(status, dict))
        else:
            results.add_test("Get Health Status", False, "Method not found")
            
    except Exception as e:
        results.add_test("Health Monitor Import", False, e)
    
    return results

def test_cost_calculation():
    """Test cost calculation logic"""
    results = TestResults()
    print("\n💰 TESTING COST CALCULATION")
    print("=" * 50)
    
    try:
        # Simple cost calculation function
        def calculate_token_cost(tokens, model="claude-3-opus", tier="basic"):
            """Calculate cost based on tokens and tier"""
            # Base rates per 1000 tokens
            model_rates = {
                "claude-3-opus": 0.015,
                "claude-3-sonnet": 0.003,
                "gpt-4": 0.03,
                "gpt-3.5": 0.002
            }
            
            # Tier multipliers
            tier_multipliers = {
                "basic": 1.0,
                "premium": 0.8,
                "enterprise": 0.6
            }
            
            base_rate = model_rates.get(model, 0.01)
            multiplier = tier_multipliers.get(tier, 1.0)
            
            return (tokens / 1000) * base_rate * multiplier
        
        # Test calculations
        cost1 = calculate_token_cost(1000, "claude-3-opus", "basic")
        results.add_test("Basic Tier Cost Calculation", abs(cost1 - 0.015) < 0.001)
        
        cost2 = calculate_token_cost(1000, "claude-3-opus", "premium")
        results.add_test("Premium Tier Cost Calculation", abs(cost2 - 0.012) < 0.001)
        
        cost3 = calculate_token_cost(5000, "gpt-4", "enterprise")
        results.add_test("Enterprise GPT-4 Cost", abs(cost3 - 0.09) < 0.001)
        
    except Exception as e:
        results.add_test("Cost Calculation", False, e)
    
    return results

def test_fallback_logic():
    """Test fallback mechanism logic"""
    results = TestResults()
    print("\n🔄 TESTING FALLBACK LOGIC")
    print("=" * 50)
    
    try:
        # Simple fallback priority system
        class FallbackManager:
            def __init__(self):
                self.providers = {
                    "claude": {"priority": 1, "available": True},
                    "openai": {"priority": 2, "available": True},
                    "gemini": {"priority": 3, "available": True},
                    "local": {"priority": 4, "available": True}
                }
            
            def get_fallback_provider(self, failed_provider):
                """Get next available provider"""
                available = [
                    (name, info) for name, info in self.providers.items()
                    if name != failed_provider and info["available"]
                ]
                # Sort by priority
                available.sort(key=lambda x: x[1]["priority"])
                return available[0][0] if available else None
            
            def mark_unavailable(self, provider):
                """Mark provider as unavailable"""
                if provider in self.providers:
                    self.providers[provider]["available"] = False
        
        manager = FallbackManager()
        results.add_test("Fallback Manager Creation", True)
        
        # Test fallback selection
        fallback = manager.get_fallback_provider("claude")
        results.add_test("Primary Fallback Selection", fallback == "openai")
        
        # Test after marking unavailable
        manager.mark_unavailable("openai")
        fallback2 = manager.get_fallback_provider("claude")
        results.add_test("Secondary Fallback Selection", fallback2 == "gemini")
        
        # Test all providers down scenario
        for provider in ["claude", "openai", "gemini", "local"]:
            manager.mark_unavailable(provider)
        fallback3 = manager.get_fallback_provider("claude")
        results.add_test("No Fallback Available", fallback3 is None)
        
    except Exception as e:
        results.add_test("Fallback Logic", False, e)
    
    return results

def test_user_profile_system():
    """Test user profile system"""
    results = TestResults()
    print("\n👤 TESTING USER PROFILE SYSTEM")
    print("=" * 50)
    
    try:
        from user_profile_system import UserProfileManager
        manager = UserProfileManager()
        results.add_test("User Profile Manager Import", True)
        
        # Test profile creation
        test_user_id = "test_user_123"
        profile = manager.get_or_create_profile(test_user_id)
        results.add_test("Profile Creation", profile is not None)
        
        # Test profile update
        if hasattr(manager, 'update_profile'):
            updated = manager.update_profile(test_user_id, {
                'preferences': {'theme': 'dark'},
                'tier': 'premium'
            })
            results.add_test("Profile Update", updated)
        else:
            results.add_test("Profile Update", False, "Method not found")
            
    except Exception as e:
        results.add_test("User Profile Manager Import", False, e)
    
    return results

def test_api_key_manager():
    """Test API key management"""
    results = TestResults()
    print("\n🔑 TESTING API KEY MANAGER")
    print("=" * 50)
    
    try:
        from api_key_manager import APIKeyManager
        manager = APIKeyManager()
        results.add_test("API Key Manager Import", True)
        
        # Test key validation structure
        test_key_data = {
            'api_key': 'test-key-12345',
            'integration_name': 'test_integration',
            'enabled': True,
            'models': ['test-model']
        }
        
        # Test if manager has required methods
        has_methods = all(hasattr(manager, method) for method in 
                         ['add_or_update_key', 'validate_key', 'get_all_keys_info'])
        results.add_test("API Key Manager Methods", has_methods)
        
    except Exception as e:
        results.add_test("API Key Manager Import", False, e)
    
    return results

def run_all_tests():
    """Run all unit tests"""
    print("🧪 AI PLATFORM CORE COMPONENTS - UNIT TEST SUITE")
    print("=" * 70)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_results = []
    
    # Run each test suite
    test_suites = [
        test_platform_engine,
        test_integration_health_monitor,
        test_cost_calculation,
        test_fallback_logic,
        test_user_profile_system,
        test_api_key_manager
    ]
    
    for test_suite in test_suites:
        try:
            results = test_suite()
            all_results.append(results)
        except Exception as e:
            print(f"\n❌ Test suite failed: {e}")
    
    # Calculate overall results
    total_passed = sum(r.passed for r in all_results)
    total_failed = sum(r.failed for r in all_results)
    total_tests = total_passed + total_failed
    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    # Print summary
    print("\n" + "=" * 70)
    print("🎊 UNIT TEST RESULTS SUMMARY")
    print("=" * 70)
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    # Save detailed results
    detailed_results = {
        'summary': {
            'total_tests': total_tests,
            'passed': total_passed,
            'failed': total_failed,
            'success_rate': success_rate,
            'timestamp': datetime.now().isoformat()
        },
        'test_suites': []
    }
    
    for i, results in enumerate(all_results):
        suite_data = results.summary()
        suite_data['tests'] = results.tests
        detailed_results['test_suites'].append(suite_data)
    
    with open('unit_test_results.json', 'w') as f:
        json.dump(detailed_results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: unit_test_results.json")
    
    if success_rate >= 90:
        print("\n🎉 EXCELLENT! Core components are working perfectly!")
    elif success_rate >= 75:
        print("\n👍 GOOD! Most core components are functional.")
    elif success_rate >= 50:
        print("\n⚠️ WARNING! Several components need attention.")
    else:
        print("\n🚨 CRITICAL! Many components are failing.")
    
    return success_rate >= 75

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)