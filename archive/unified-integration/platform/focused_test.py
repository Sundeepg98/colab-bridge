#!/usr/bin/env python3
"""
Focused test on the most important dashboard features
"""

import requests
import json

def test_core_features():
    """Test the core admin dashboard functionality"""
    base_url = "http://localhost:5000"
    
    print("🎯 TESTING CORE ADMIN DASHBOARD FEATURES")
    print("=" * 60)
    
    # Test dashboard pages
    print("\n📱 DASHBOARD PAGES:")
    pages = [
        ("/", "Home Page"),
        ("/admin", "Main Admin Dashboard"),
        ("/admin-enhanced", "Enhanced Admin Dashboard"),
    ]
    
    for url, name in pages:
        try:
            response = requests.get(f"{base_url}{url}", timeout=5)
            status = "✅ WORKING" if response.status_code == 200 else f"❌ ERROR ({response.status_code})"
            print(f"  {name}: {status}")
        except Exception as e:
            print(f"  {name}: ❌ ERROR ({e})")
    
    # Test critical API endpoints
    print("\n🔌 CRITICAL API ENDPOINTS:")
    endpoints = [
        ("/api/unified-system-status", "Unified System Status"),
        ("/api/api-keys", "API Key Management"),
        ("/api/service-discovery-status", "Service Discovery"),
        ("/api/fallback-system-status", "Fallback System"),
        ("/api/independent-core-status", "Independent Core"),
        ("/api/system-recommendations", "System Recommendations"),
        ("/api/claude-status", "Claude Integration"),
    ]
    
    working = 0
    total = len(endpoints)
    
    for url, name in endpoints:
        try:
            response = requests.get(f"{base_url}{url}", timeout=5)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success', True):
                        print(f"  {name}: ✅ WORKING")
                        working += 1
                    else:
                        print(f"  {name}: ⚠️ API ERROR - {data.get('error', 'Unknown')}")
                except:
                    print(f"  {name}: ✅ WORKING (HTML)")
                    working += 1
            else:
                print(f"  {name}: ❌ HTTP {response.status_code}")
        except Exception as e:
            print(f"  {name}: ❌ ERROR ({e})")
    
    # Test dynamic framework functionality
    print("\n🌐 DYNAMIC FRAMEWORK STATUS:")
    try:
        response = requests.get(f"{base_url}/api/unified-system-status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                status = data['system_status']
                print(f"  System Status: ✅ OPERATIONAL")
                print(f"  Services: {status['healthy_services']}/{status['total_services']} healthy")
                print(f"  Discovery: {status['discovery']['total_discovered']} services found")
                print(f"  Fallback: {status['fallback']['system_health']} health")
                print(f"  Core: {len(status['independent_core']['available_capabilities'])} capabilities")
                print(f"  Cost: ${status['costs']['total_cost']} (Budget: ${status['costs']['budget_status']['monthly_limit']})")
            else:
                print(f"  System Status: ❌ ERROR - {data['error']}")
        else:
            print(f"  System Status: ❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"  System Status: ❌ ERROR ({e})")
    
    # Calculate success rate
    success_rate = (working / total) * 100
    
    print(f"\n📊 RESULTS:")
    print(f"  Critical endpoints working: {working}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("  🎉 EXCELLENT! All core features are operational!")
    elif success_rate >= 75:
        print("  👍 GOOD! Most core features are working!")
    else:
        print("  ⚠️ Some core features need attention.")
    
    return success_rate >= 75

if __name__ == "__main__":
    success = test_core_features()
    print(f"\n🚀 Core admin dashboard functionality: {'✅ PASSED' if success else '❌ NEEDS WORK'}")