#!/usr/bin/env python3
"""
Test only the actually implemented and working components
"""

import sys
import os
import json
from datetime import datetime

# Add project paths
sys.path.append('/var/projects/ai-integration-platform/src')
sys.path.append('/var/projects/ai-integration-platform/src')

print("=" * 60)
print("TESTING WORKING COMPONENTS")
print("=" * 60)

# Test results storage
test_results = {
    "timestamp": datetime.now().isoformat(),
    "passed": 0,
    "failed": 0,
    "tests": []
}

def test_component(name, test_func):
    """Run a single component test"""
    print(f"\n[TEST] {name}")
    try:
        result = test_func()
        if result:
            print(f"✅ PASSED: {name}")
            test_results["passed"] += 1
            test_results["tests"].append({
                "name": name,
                "status": "PASSED",
                "details": "Component working correctly"
            })
            return True
        else:
            print(f"❌ FAILED: {name}")
            test_results["failed"] += 1
            test_results["tests"].append({
                "name": name,
                "status": "FAILED",
                "details": "Component test failed"
            })
            return False
    except Exception as e:
        print(f"❌ ERROR: {name} - {str(e)}")
        test_results["failed"] += 1
        test_results["tests"].append({
            "name": name,
            "status": "ERROR",
            "details": str(e)
        })
        return False

# Test 1: Platform Engine
def test_platform_engine():
    from platform_engine import get_platform_engine, PlatformRequest, RequestType
    
    engine = get_platform_engine()
    
    # Test route_request method (newly added)
    request_data = {
        'user_id': 'test_user',
        'type': 'text_generation',
        'prompt': 'Test prompt',
        'parameters': {}
    }
    
    result = engine.route_request(request_data)
    return result.get('success', False)

# Test 2: Dynamic Integration Framework
def test_dynamic_framework():
    from dynamic_integration_framework import get_dynamic_framework
    
    framework = get_dynamic_framework()
    
    # Check if framework has basic methods
    return hasattr(framework, 'register_integration') and hasattr(framework, 'get_available_integrations')

# Test 3: Cost Optimization Engine
def test_cost_optimization():
    from cost_optimization_engine import get_cost_optimization_engine
    
    engine = get_cost_optimization_engine()
    
    # Test cost calculation
    recommendations = engine.get_cost_recommendations('test_user')
    return isinstance(recommendations, list)

# Test 4: Fallback System
def test_fallback_system():
    from fallback_system import get_fallback_manager
    
    manager = get_fallback_manager()
    
    # Test fallback status
    status = manager.get_fallback_status()
    return isinstance(status, dict) and 'active_fallbacks' in status

# Test 5: User Profile System
def test_user_profile():
    from user_profile_system import get_profile_system, UserProfileManager
    
    # Test both interfaces
    system = get_profile_system()
    
    # Test profile creation
    profile = system.get_or_create_profile('test_user')
    
    return profile is not None and hasattr(profile, 'user_id')

# Test 6: API Key Manager
def test_api_key_manager():
    from api_key_manager import get_api_key_manager
    
    manager = get_api_key_manager()
    
    # Test key storage
    key_info = manager.add_api_key('test_service', 'test_key_123', {
        'name': 'Test Key',
        'created_by': 'test_user'
    })
    
    # Verify storage
    all_keys = manager.get_all_keys_info()
    return 'test_service' in all_keys

# Test 7: Integration Manager
def test_integration_manager():
    from integration_manager import get_integration_manager
    
    manager = get_integration_manager()
    
    # Test integration status
    status = manager.get_all_integration_status()
    return isinstance(status, dict)

# Test 8: Health Monitor
def test_health_monitor():
    from integration_health_monitor import get_health_monitor
    
    monitor = get_health_monitor()
    
    # Test health status
    health = monitor.get_system_health()
    return isinstance(health, dict) and 'status' in health

# Run all tests
print("\nRunning component tests...\n")

tests = [
    ("Platform Engine", test_platform_engine),
    ("Dynamic Integration Framework", test_dynamic_framework),
    ("Cost Optimization Engine", test_cost_optimization),
    ("Fallback System", test_fallback_system),
    ("User Profile System", test_user_profile),
    ("API Key Manager", test_api_key_manager),
    ("Integration Manager", test_integration_manager),
    ("Health Monitor", test_health_monitor),
]

for test_name, test_func in tests:
    test_component(test_name, test_func)

# Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"Total Tests: {test_results['passed'] + test_results['failed']}")
print(f"Passed: {test_results['passed']} ✅")
print(f"Failed: {test_results['failed']} ❌")
success_rate = (test_results['passed'] / max(1, test_results['passed'] + test_results['failed'])) * 100
print(f"Success Rate: {success_rate:.1f}%")

# Save results
with open('component_test_results.json', 'w') as f:
    json.dump(test_results, f, indent=2)

print("\nResults saved to component_test_results.json")

# Exit with appropriate code
exit(0 if test_results['failed'] == 0 else 1)