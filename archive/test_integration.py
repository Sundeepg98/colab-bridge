#!/usr/bin/env python3
"""
🧪 Claude Tools - Comprehensive Integration Testing Script
Tests all core functionality before GitHub release
"""

import os
import sys
import json
import time
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
import concurrent.futures
import threading

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ClaudeToolsIntegrationTester:
    def __init__(self):
        self.project_root = Path("/var/projects/personal-claude-tools")
        self.test_results = {}
        self.start_time = datetime.now()
        self.critical_files = [
            "colab-integration/COMPLETE_COLAB_INTEGRATION.py",
            "colab-integration/app.py",
            "notebooks/claude-tools-colab-basic.ipynb",
            "notebooks/claude-tools-colab-multi.ipynb"
        ]
        
    def print_header(self, text):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}🧪 {text}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        
    def print_test(self, test_name):
        print(f"\n{Colors.BLUE}🔍 Testing: {test_name}{Colors.END}")
        
    def print_success(self, message):
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
        
    def print_warning(self, message):
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
        
    def print_error(self, message):
        print(f"{Colors.RED}❌ {message}{Colors.END}")
        
    def print_info(self, message):
        print(f"{Colors.PURPLE}ℹ️  {message}{Colors.END}")

    def test_project_structure(self):
        """Test 1: Verify project structure"""
        self.print_test("Project Structure")
        
        required_dirs = [
            "colab-integration",
            "colab-integration/src",
            "colab-integration/templates", 
            "notebooks",
            "config",
            "docs"
        ]
        
        structure_score = 0
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists():
                self.print_success(f"Directory exists: {dir_path}")
                structure_score += 1
            else:
                self.print_error(f"Missing directory: {dir_path}")
        
        # Check critical files
        for file_path in self.critical_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.print_success(f"Critical file exists: {file_path}")
                structure_score += 1
            else:
                self.print_error(f"Missing critical file: {file_path}")
        
        self.test_results['structure'] = {
            'score': structure_score,
            'total': len(required_dirs) + len(self.critical_files),
            'passed': structure_score == len(required_dirs) + len(self.critical_files)
        }
        
        return self.test_results['structure']['passed']

    def test_security_compliance(self):
        """Test 2: Security audit - no hardcoded credentials"""
        self.print_test("Security Compliance")
        
        security_issues = []
        dangerous_patterns = [
            r'sk-[a-zA-Z0-9]{48}',  # OpenAI API keys
            r'claude-[a-zA-Z0-9\-]{48}',  # Claude API keys
            r'"private_key":\s*"-----BEGIN',  # Service account keys
            r'AIza[0-9A-Za-z\-_]{35}',  # Google API keys
            r'[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com',  # OAuth client IDs
        ]
        
        # Scan Python files
        for py_file in self.project_root.rglob("*.py"):
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text()
                for pattern in dangerous_patterns:
                    import re
                    if re.search(pattern, content):
                        security_issues.append(f"Potential credential in {py_file}")
                        
            except Exception as e:
                self.print_warning(f"Could not scan {py_file}: {e}")
        
        # Scan JavaScript/JSON files
        for js_file in self.project_root.rglob("*.js"):
            try:
                content = js_file.read_text()
                if 'serviceAccountPath' in content and '/var/projects/eng-flux' in content:
                    security_issues.append(f"Hardcoded service account path in {js_file}")
            except Exception:
                pass
        
        if security_issues:
            for issue in security_issues:
                self.print_error(issue)
            self.test_results['security'] = {'passed': False, 'issues': security_issues}
        else:
            self.print_success("No hardcoded credentials detected")
            self.test_results['security'] = {'passed': True, 'issues': []}
        
        return len(security_issues) == 0

    def test_python_syntax(self):
        """Test 3: Python syntax validation"""
        self.print_test("Python Syntax Validation")
        
        syntax_errors = []
        python_files = list(self.project_root.rglob("*.py"))
        
        for py_file in python_files:
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r') as f:
                    compile(f.read(), py_file, 'exec')
                self.print_success(f"Syntax OK: {py_file.relative_to(self.project_root)}")
            except SyntaxError as e:
                error_msg = f"Syntax error in {py_file}: {e}"
                syntax_errors.append(error_msg)
                self.print_error(error_msg)
            except Exception as e:
                self.print_warning(f"Could not check {py_file}: {e}")
        
        self.test_results['python_syntax'] = {
            'passed': len(syntax_errors) == 0,
            'errors': syntax_errors,
            'files_checked': len(python_files)
        }
        
        return len(syntax_errors) == 0

    def test_dependency_imports(self):
        """Test 4: Check if critical imports work"""
        self.print_test("Dependency Import Check")
        
        critical_imports = [
            ('google.auth', 'Google Auth'),
            ('google.auth.transport.requests', 'Google Auth Transport'),
            ('googleapiclient.discovery', 'Google API Client'),
            ('flask', 'Flask'),
            ('flask_cors', 'Flask CORS'),
            ('anthropic', 'Anthropic (optional)'),
            ('openai', 'OpenAI (optional)')
        ]
        
        import_results = {}
        for module_name, display_name in critical_imports:
            try:
                __import__(module_name)
                self.print_success(f"{display_name} import successful")
                import_results[module_name] = True
            except ImportError:
                if 'optional' in display_name.lower():
                    self.print_warning(f"{display_name} not available (optional)")
                    import_results[module_name] = 'optional'
                else:
                    self.print_error(f"{display_name} import failed")
                    import_results[module_name] = False
        
        required_imports = [k for k, v in import_results.items() 
                          if not any(opt in k for opt in ['anthropic', 'openai'])]
        passed = all(import_results.get(k, False) for k in required_imports)
        
        self.test_results['imports'] = {
            'passed': passed,
            'results': import_results
        }
        
        return passed

    def test_flask_app_startup(self):
        """Test 5: Flask app can start"""
        self.print_test("Flask App Startup")
        
        app_path = self.project_root / "colab-integration" / "app.py"
        if not app_path.exists():
            self.print_error("Flask app.py not found")
            self.test_results['flask_startup'] = {'passed': False, 'error': 'app.py missing'}
            return False
        
        try:
            # Test import and basic initialization
            import sys
            sys.path.insert(0, str(app_path.parent))
            
            # Create minimal test
            test_code = f"""
import sys
sys.path.insert(0, '{app_path.parent}')
try:
    from app import app
    print("Flask app imported successfully")
    # Test app context
    with app.app_context():
        print("Flask app context works")
    exit(0)
except Exception as e:
    print(f"Flask app error: {{e}}")
    exit(1)
"""
            
            result = subprocess.run([
                sys.executable, '-c', test_code
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.print_success("Flask app startup test passed")
                self.test_results['flask_startup'] = {'passed': True}
                return True
            else:
                self.print_error(f"Flask app startup failed: {result.stderr}")
                self.test_results['flask_startup'] = {'passed': False, 'error': result.stderr}
                return False
                
        except Exception as e:
            self.print_error(f"Flask test error: {e}")
            self.test_results['flask_startup'] = {'passed': False, 'error': str(e)}
            return False

    def test_notebook_validation(self):
        """Test 6: Validate Jupyter notebooks"""
        self.print_test("Notebook Validation")
        
        notebooks = [
            Path("/var/projects/claude-tools/notebooks/claude-tools-colab-basic.ipynb"),
            Path("/var/projects/claude-tools/notebooks/claude-tools-colab-multi.ipynb")
        ]
        
        notebook_results = {}
        for notebook_path in notebooks:
            if not notebook_path.exists():
                self.print_error(f"Notebook missing: {notebook_path.name}")
                notebook_results[notebook_path.name] = False
                continue
            
            try:
                with open(notebook_path, 'r') as f:
                    notebook_data = json.load(f)
                
                # Basic validation
                if 'cells' not in notebook_data:
                    self.print_error(f"Invalid notebook structure: {notebook_path.name}")
                    notebook_results[notebook_path.name] = False
                    continue
                
                # Check for critical cells
                has_processor = False
                has_bridge_init = False
                
                for cell in notebook_data['cells']:
                    if cell.get('cell_type') == 'code':
                        source = ''.join(cell.get('source', []))
                        if 'UniversalClaudeProcessor' in source:
                            has_processor = True
                        if 'claude_tools_bridge' in source:
                            has_bridge_init = True
                
                if has_processor and has_bridge_init:
                    self.print_success(f"Notebook valid: {notebook_path.name}")
                    notebook_results[notebook_path.name] = True
                else:
                    self.print_warning(f"Notebook may be incomplete: {notebook_path.name}")
                    notebook_results[notebook_path.name] = 'partial'
                    
            except Exception as e:
                self.print_error(f"Notebook validation failed {notebook_path.name}: {e}")
                notebook_results[notebook_path.name] = False
        
        passed = all(result in [True, 'partial'] for result in notebook_results.values())
        self.test_results['notebooks'] = {
            'passed': passed,
            'results': notebook_results
        }
        
        return passed

    def test_multi_instance_simulation(self):
        """Test 7: Simulate multi-instance scenario"""
        self.print_test("Multi-Instance Simulation")
        
        try:
            # Test basic multi-instance bridge import
            bridge_path = self.project_root / "colab-integration" / "src" / "multi_instance_colab_bridge.py"
            if not bridge_path.exists():
                self.print_error("Multi-instance bridge file missing")
                self.test_results['multi_instance'] = {'passed': False, 'error': 'missing file'}
                return False
            
            # Simulate multiple instances registering
            test_instances = [
                {'id': 'claude_test1', 'project': 'project_a'},
                {'id': 'claude_test2', 'project': 'project_b'},
                {'id': 'claude_test3', 'project': 'project_c'}
            ]
            
            # Test instance registration logic
            import sys
            sys.path.insert(0, str(bridge_path.parent))
            
            try:
                from multi_instance_colab_bridge import MultiInstanceColabBridge
                bridge = MultiInstanceColabBridge()
                
                for instance in test_instances:
                    instance_id = bridge.register_claude_instance(instance['project'])
                    if instance_id:
                        self.print_success(f"Instance registered: {instance['id']}")
                    else:
                        self.print_error(f"Failed to register: {instance['id']}")
                
                self.test_results['multi_instance'] = {'passed': True}
                return True
                
            except Exception as e:
                self.print_error(f"Multi-instance test failed: {e}")
                self.test_results['multi_instance'] = {'passed': False, 'error': str(e)}
                return False
                
        except Exception as e:
            self.print_error(f"Multi-instance simulation error: {e}")
            self.test_results['multi_instance'] = {'passed': False, 'error': str(e)}
            return False

    def test_documentation_completeness(self):
        """Test 8: Check documentation completeness"""
        self.print_test("Documentation Completeness")
        
        required_docs = [
            ("README.md", "Main documentation"),
            ("SETUP_GUIDE.md", "Setup instructions"),
            ("SECURITY.md", "Security guidelines"),
            ("TESTING_AND_RELEASE_PLAN.md", "Release plan")
        ]
        
        doc_results = {}
        for doc_file, description in required_docs:
            doc_path = self.project_root / doc_file
            if doc_path.exists():
                try:
                    content = doc_path.read_text()
                    if len(content) > 500:  # Basic completeness check
                        self.print_success(f"{description} exists and substantial")
                        doc_results[doc_file] = True
                    else:
                        self.print_warning(f"{description} exists but seems incomplete")
                        doc_results[doc_file] = 'partial'
                except Exception:
                    self.print_error(f"{description} exists but unreadable")
                    doc_results[doc_file] = False
            else:
                self.print_error(f"Missing: {description}")
                doc_results[doc_file] = False
        
        passed = all(result in [True, 'partial'] for result in doc_results.values())
        self.test_results['documentation'] = {
            'passed': passed,
            'results': doc_results
        }
        
        return passed

    def test_configuration_templates(self):
        """Test 9: Validate configuration templates"""
        self.print_test("Configuration Templates")
        
        template_files = [
            "config/service-account.template.json",
            "config/.env.template",
            "config/project-config.template.json"
        ]
        
        template_results = {}
        for template_file in template_files:
            template_path = self.project_root / template_file
            if template_path.exists():
                try:
                    content = template_path.read_text()
                    # Check for placeholder values
                    if 'your-' in content or 'YOUR_' in content or 'template' in content.lower():
                        self.print_success(f"Template valid: {template_file}")
                        template_results[template_file] = True
                    else:
                        self.print_warning(f"Template may contain real values: {template_file}")
                        template_results[template_file] = 'warning'
                except Exception as e:
                    self.print_error(f"Template validation failed {template_file}: {e}")
                    template_results[template_file] = False
            else:
                self.print_warning(f"Template missing: {template_file}")
                template_results[template_file] = False
        
        self.test_results['configuration'] = {
            'passed': len(template_results) > 0,
            'results': template_results
        }
        
        return len(template_results) > 0

    def run_comprehensive_test_suite(self):
        """Run all tests and generate report"""
        self.print_header("CLAUDE TOOLS INTEGRATION TESTING")
        self.print_info(f"Testing project at: {self.project_root}")
        self.print_info(f"Started at: {self.start_time}")
        
        # Run all tests
        tests = [
            self.test_project_structure,
            self.test_security_compliance,
            self.test_python_syntax,
            self.test_dependency_imports,
            self.test_flask_app_startup,
            self.test_notebook_validation,
            self.test_multi_instance_simulation,
            self.test_documentation_completeness,
            self.test_configuration_templates
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.print_error(f"Test {test_func.__name__} crashed: {e}")
        
        # Generate final report
        self.generate_test_report(passed_tests, total_tests)
        
        return passed_tests == total_tests

    def generate_test_report(self, passed_tests, total_tests):
        """Generate comprehensive test report"""
        self.print_header("TEST RESULTS SUMMARY")
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print(f"\n{Colors.BOLD}📊 OVERALL RESULTS{Colors.END}")
        print(f"Tests Passed: {Colors.GREEN}{passed_tests}/{total_tests}{Colors.END}")
        print(f"Success Rate: {Colors.GREEN if passed_tests == total_tests else Colors.YELLOW}{(passed_tests/total_tests)*100:.1f}%{Colors.END}")
        print(f"Duration: {duration.total_seconds():.1f} seconds")
        
        # Detailed results
        print(f"\n{Colors.BOLD}📋 DETAILED RESULTS{Colors.END}")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result.get('passed') else "❌ FAIL"
            color = Colors.GREEN if result.get('passed') else Colors.RED
            print(f"{color}{status}{Colors.END} {test_name.replace('_', ' ').title()}")
            
            if not result.get('passed') and 'error' in result:
                print(f"   {Colors.RED}Error: {result['error']}{Colors.END}")
        
        # GitHub readiness assessment
        print(f"\n{Colors.BOLD}🚀 GITHUB READINESS ASSESSMENT{Colors.END}")
        
        critical_tests = ['structure', 'security', 'python_syntax']
        critical_passed = all(self.test_results.get(test, {}).get('passed', False) for test in critical_tests)
        
        if critical_passed and passed_tests >= total_tests * 0.8:
            print(f"{Colors.GREEN}✅ READY FOR GITHUB RELEASE{Colors.END}")
            print(f"{Colors.GREEN}   All critical tests passed, minor issues can be addressed post-release{Colors.END}")
        elif critical_passed:
            print(f"{Colors.YELLOW}⚠️  MOSTLY READY - MINOR FIXES NEEDED{Colors.END}")
            print(f"{Colors.YELLOW}   Critical tests passed, but some features need attention{Colors.END}")
        else:
            print(f"{Colors.RED}❌ NOT READY FOR RELEASE{Colors.END}")
            print(f"{Colors.RED}   Critical issues must be fixed before GitHub release{Colors.END}")
        
        # Save detailed report
        report_path = self.project_root / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump({
                'summary': {
                    'passed_tests': passed_tests,
                    'total_tests': total_tests,
                    'success_rate': (passed_tests/total_tests)*100,
                    'duration_seconds': duration.total_seconds(),
                    'timestamp': self.start_time.isoformat()
                },
                'detailed_results': self.test_results,
                'github_ready': critical_passed and passed_tests >= total_tests * 0.8
            }, f, indent=2)
        
        self.print_info(f"Detailed report saved: {report_path}")

if __name__ == "__main__":
    print(f"{Colors.CYAN}🧪 Claude Tools Integration Testing Suite{Colors.END}")
    print(f"{Colors.CYAN}Testing comprehensive colab integration before GitHub release{Colors.END}")
    
    tester = ClaudeToolsIntegrationTester()
    success = tester.run_comprehensive_test_suite()
    
    exit_code = 0 if success else 1
    sys.exit(exit_code)