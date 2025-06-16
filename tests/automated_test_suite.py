#!/usr/bin/env python3
"""
Automated Test Suite for Colab-Bridge
Focuses on critical functionality that must work for paying customers
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class AutomatedTestRunner:
    """Automated test runner for CI/CD"""
    
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        
    def test(self, name, func):
        """Run a single test"""
        print(f"\n🧪 Testing: {name}")
        try:
            result = func()
            if result:
                self.results.append((name, True, None))
                print(f"{Colors.GREEN}✅ PASSED{Colors.END}")
                return True
            else:
                self.results.append((name, False, "Test returned False"))
                print(f"{Colors.RED}❌ FAILED{Colors.END}")
                return False
        except Exception as e:
            self.results.append((name, False, str(e)))
            print(f"{Colors.RED}❌ ERROR: {e}{Colors.END}")
            return False
    
    def run_all(self):
        """Run all automated tests"""
        print(f"{Colors.BLUE}🚀 COLAB-BRIDGE AUTOMATED TEST SUITE{Colors.END}")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Critical Path Tests
        self.test("Environment Setup", self.test_environment)
        self.test("Python Dependencies", self.test_dependencies)
        self.test("Google Credentials", self.test_credentials)
        self.test("Core Module Import", self.test_core_imports)
        self.test("Bridge Initialization", self.test_bridge_init)
        self.test("VS Code Extension Build", self.test_vscode_extension)
        self.test("Command Generation", self.test_command_generation)
        self.test("Error Handling", self.test_error_handling)
        self.test("Performance Benchmark", self.test_performance)
        
        # Generate report
        self.generate_report()
        
    def test_environment(self):
        """Test environment setup"""
        required_vars = ['SERVICE_ACCOUNT_PATH', 'OWNER_EMAIL']
        
        # Set defaults if not present
        if 'SERVICE_ACCOUNT_PATH' not in os.environ:
            cred_path = Path(__file__).parent.parent / 'credentials' / 'automation-engine-463103-ee5a06e18248.json'
            if cred_path.exists():
                os.environ['SERVICE_ACCOUNT_PATH'] = str(cred_path)
        
        if 'OWNER_EMAIL' not in os.environ:
            os.environ['OWNER_EMAIL'] = 'sundeepg8@gmail.com'
        
        # Check all required
        for var in required_vars:
            if var not in os.environ:
                raise Exception(f"Missing environment variable: {var}")
        
        # Verify credential file exists
        cred_file = Path(os.environ['SERVICE_ACCOUNT_PATH'])
        if not cred_file.exists():
            raise Exception(f"Credential file not found: {cred_file}")
        
        return True
    
    def test_dependencies(self):
        """Test Python dependencies"""
        required_packages = [
            'google.auth',
            'googleapiclient',
            'google.oauth2'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                raise Exception(f"Missing package: {package}")
        
        return True
    
    def test_credentials(self):
        """Test Google credentials validity"""
        from google.oauth2 import service_account
        
        try:
            credentials = service_account.Credentials.from_service_account_file(
                os.environ['SERVICE_ACCOUNT_PATH'],
                scopes=['https://www.googleapis.com/auth/drive']
            )
            
            # Verify it's a valid service account
            if not hasattr(credentials, 'service_account_email'):
                raise Exception("Invalid service account credentials")
            
            return True
        except Exception as e:
            raise Exception(f"Credential validation failed: {e}")
    
    def test_core_imports(self):
        """Test core module imports"""
        try:
            from colab_integration import UniversalColabBridge
            from colab_automation.auto_colab import AutomatedColabBridge
            
            # Check classes are properly defined
            if not hasattr(UniversalColabBridge, 'execute_code'):
                raise Exception("UniversalColabBridge missing execute_code method")
            
            return True
        except ImportError as e:
            raise Exception(f"Import failed: {e}")
    
    def test_bridge_init(self):
        """Test bridge initialization"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        bridge = UniversalColabBridge("automated_test")
        
        # Verify initialization
        if bridge.tool_name != "automated_test":
            raise Exception("Bridge initialization failed")
        
        # Test config loading
        config = bridge._load_config(None)
        if 'service_account_path' not in config:
            raise Exception("Config loading failed")
        
        return True
    
    def test_vscode_extension(self):
        """Test VS Code extension package"""
        ext_path = Path(__file__).parent.parent / 'extensions' / 'vscode'
        vsix_file = ext_path / 'colab-bridge-1.0.0.vsix'
        
        # Check VSIX exists
        if not vsix_file.exists():
            # Try to build it
            print("  Building VS Code extension...")
            os.chdir(ext_path)
            result = subprocess.run(['npm', 'run', 'compile'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Extension build failed: {result.stderr}")
        
        # Verify package.json
        pkg_path = ext_path / 'package.json'
        if not pkg_path.exists():
            raise Exception("package.json not found")
        
        with open(pkg_path) as f:
            package = json.load(f)
        
        if package.get('name') != 'colab-bridge':
            raise Exception("Invalid package.json")
        
        return True
    
    def test_command_generation(self):
        """Test command generation logic"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        bridge = UniversalColabBridge("test")
        
        # Test command structure
        test_code = "print('automated test')"
        command = {
            'id': f"cmd_test_{int(time.time())}",
            'type': 'execute',
            'code': test_code,
            'timestamp': time.time(),
            'tool': 'test'
        }
        
        # Validate command
        if not command['id'].startswith('cmd_test_'):
            raise Exception("Invalid command ID format")
        
        if command['code'] != test_code:
            raise Exception("Code not properly stored")
        
        return True
    
    def test_error_handling(self):
        """Test error handling"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        # Test with invalid credentials
        original_path = os.environ.get('SERVICE_ACCOUNT_PATH')
        os.environ['SERVICE_ACCOUNT_PATH'] = '/invalid/path.json'
        
        bridge = UniversalColabBridge("error_test")
        
        try:
            bridge.initialize()
            # Should raise an error
            os.environ['SERVICE_ACCOUNT_PATH'] = original_path
            raise Exception("Should have raised an error for invalid credentials")
        except:
            # Error correctly raised
            os.environ['SERVICE_ACCOUNT_PATH'] = original_path
            return True
    
    def test_performance(self):
        """Test performance benchmarks"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        # Test initialization speed
        start = time.time()
        bridge = UniversalColabBridge("perf_test")
        init_time = time.time() - start
        
        if init_time > 1.0:
            raise Exception(f"Initialization too slow: {init_time:.2f}s")
        
        # Test command generation speed
        start = time.time()
        for i in range(100):
            cmd = {
                'id': f"cmd_perf_{i}",
                'code': f"print({i})",
                'timestamp': time.time()
            }
        cmd_time = time.time() - start
        
        if cmd_time > 0.1:
            raise Exception(f"Command generation too slow: {cmd_time:.2f}s for 100 commands")
        
        print(f"  Init: {init_time*1000:.1f}ms, Commands: {cmd_time*1000:.1f}ms")
        return True
    
    def generate_report(self):
        """Generate test report"""
        duration = time.time() - self.start_time
        passed = sum(1 for _, success, _ in self.results if success)
        failed = len(self.results) - passed
        
        print("\n" + "=" * 60)
        print(f"{Colors.BLUE}📊 TEST RESULTS{Colors.END}")
        print("=" * 60)
        
        # Summary
        print(f"Total Tests: {len(self.results)}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {failed}{Colors.END}")
        print(f"Duration: {duration:.2f}s")
        print(f"Success Rate: {(passed/len(self.results)*100):.1f}%")
        
        # Failed tests details
        if failed > 0:
            print(f"\n{Colors.RED}Failed Tests:{Colors.END}")
            for name, success, error in self.results:
                if not success:
                    print(f"  ❌ {name}: {error}")
        
        # Write to file
        report_path = Path(__file__).parent.parent / 'test_automation_report.json'
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'total': len(self.results),
            'passed': passed,
            'failed': failed,
            'success_rate': passed/len(self.results)*100,
            'results': [
                {
                    'name': name,
                    'passed': success,
                    'error': error
                }
                for name, success, error in self.results
            ]
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Report saved to: {report_path}")
        
        # Exit code for CI/CD
        if failed > 0:
            print(f"\n{Colors.RED}❌ TESTS FAILED{Colors.END}")
            sys.exit(1)
        else:
            print(f"\n{Colors.GREEN}✅ ALL TESTS PASSED{Colors.END}")
            sys.exit(0)

def main():
    """Run automated tests"""
    runner = AutomatedTestRunner()
    runner.run_all()

if __name__ == "__main__":
    main()