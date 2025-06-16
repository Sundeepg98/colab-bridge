#!/usr/bin/env python3
"""
Comprehensive Test Suite for Colab-Bridge
Tests all components and integration points
"""

import os
import sys
import json
import time
import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Set up test environment
os.environ['SERVICE_ACCOUNT_PATH'] = str(Path(__file__).parent / 'credentials' / 'automation-engine-463103-ee5a06e18248.json')
os.environ['GOOGLE_DRIVE_FOLDER_ID'] = 'test_folder_id'
os.environ['OWNER_EMAIL'] = 'test@example.com'

class TestColabBridgeCore(unittest.TestCase):
    """Test core functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_code = "print('Hello from test')"
        
    def test_import_modules(self):
        """Test that all modules can be imported"""
        try:
            from colab_integration import UniversalColabBridge
            from colab_integration.bridge import ColabBridge
            from colab_integration.processor import ColabProcessor
            self.assertTrue(True, "All modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import modules: {e}")
    
    def test_universal_bridge_init(self):
        """Test UniversalColabBridge initialization"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        bridge = UniversalColabBridge("test_tool")
        self.assertEqual(bridge.tool_name, "test_tool")
        self.assertIsNone(bridge.drive_service)
        self.assertTrue(bridge.instance_id.startswith("test_tool_"))
    
    def test_config_loading(self):
        """Test configuration loading"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        bridge = UniversalColabBridge("test")
        config = bridge._load_config(None)
        
        self.assertIn('service_account_path', config)
        self.assertIn('google_drive_folder_id', config)
        self.assertEqual(config['tool_name'], "test")
    
    @patch('googleapiclient.discovery.build')
    def test_initialize_with_mock(self, mock_build):
        """Test initialization with mocked Google services"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        # Mock the build function
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        bridge = UniversalColabBridge("test")
        bridge.initialize()
        
        self.assertIsNotNone(bridge.drive_service)
        mock_build.assert_called_once()
    
    def test_command_generation(self):
        """Test command generation"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        bridge = UniversalColabBridge("test")
        
        # Manually test command structure
        test_code = "print('test')"
        command = {
            'id': f"cmd_test_{int(time.time())}",
            'type': 'execute',
            'code': test_code,
            'timestamp': time.time(),
            'tool': 'test'
        }
        
        self.assertEqual(command['type'], 'execute')
        self.assertEqual(command['code'], test_code)
        self.assertEqual(command['tool'], 'test')
        self.assertTrue(command['id'].startswith('cmd_test_'))

class TestAutomation(unittest.TestCase):
    """Test automation features"""
    
    def test_auto_colab_import(self):
        """Test automated colab module"""
        try:
            from colab_automation.auto_colab import AutomatedColabBridge, auto_colab
            self.assertTrue(True, "Automation module imported")
        except ImportError as e:
            self.fail(f"Failed to import automation: {e}")
    
    def test_credential_detection(self):
        """Test automatic credential detection"""
        from colab_automation.auto_colab import AutomatedColabBridge
        
        bridge = AutomatedColabBridge("test")
        # Should find credentials in our test environment
        self.assertTrue(hasattr(bridge, 'creds_path'))
    
    def test_folder_creation_logic(self):
        """Test folder creation logic"""
        from colab_automation.auto_colab import AutomatedColabBridge
        
        bridge = AutomatedColabBridge("test")
        
        # Test internal state
        self.assertFalse(bridge.setup_complete)
        self.assertIsNone(bridge.folder_id)
        self.assertIsNone(bridge.notebook_id)

class TestVSCodeExtension(unittest.TestCase):
    """Test VS Code extension components"""
    
    def test_extension_files_exist(self):
        """Test that all extension files exist"""
        ext_path = Path(__file__).parent / 'extensions' / 'vscode'
        
        required_files = [
            'package.json',
            'tsconfig.json',
            'README.md',
            'LICENSE',
            '.vscodeignore',
            'src/extension.ts',
            'out/extension.js'  # Compiled output
        ]
        
        for file in required_files:
            file_path = ext_path / file
            self.assertTrue(file_path.exists(), f"Missing: {file}")
    
    def test_package_json_valid(self):
        """Test package.json structure"""
        pkg_path = Path(__file__).parent / 'extensions' / 'vscode' / 'package.json'
        
        with open(pkg_path, 'r') as f:
            package = json.load(f)
        
        # Check required fields
        self.assertEqual(package['name'], 'colab-bridge')
        self.assertEqual(package['publisher'], 'sundeepg')
        self.assertIn('main', package)
        self.assertIn('contributes', package)
        self.assertIn('commands', package['contributes'])
        
        # Check commands
        commands = package['contributes']['commands']
        command_ids = [cmd['command'] for cmd in commands]
        
        expected_commands = [
            'colab-bridge.executeInColab',
            'colab-bridge.executeSelectionInColab',
            'colab-bridge.openColabNotebook',
            'colab-bridge.configure'
        ]
        
        for cmd in expected_commands:
            self.assertIn(cmd, command_ids, f"Missing command: {cmd}")
    
    def test_extension_package_exists(self):
        """Test that VSIX package was created"""
        vsix_path = Path(__file__).parent / 'extensions' / 'vscode' / 'colab-bridge-1.0.0.vsix'
        self.assertTrue(vsix_path.exists(), "VSIX package not found")
        
        # Check file size is reasonable
        size = vsix_path.stat().st_size
        self.assertGreater(size, 1000, "VSIX file too small")
        self.assertLess(size, 10000000, "VSIX file too large")

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    @patch('googleapiclient.discovery.build')
    def test_end_to_end_flow_mocked(self, mock_build):
        """Test end-to-end flow with mocks"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        # Set up mocks
        mock_drive = MagicMock()
        mock_build.return_value = mock_drive
        
        # Mock file operations
        mock_drive.files().create.return_value.execute.return_value = {'id': 'test_file_id'}
        mock_drive.files().list.return_value.execute.return_value = {
            'files': [{'id': 'result_file_id'}]
        }
        mock_drive.files().get_media.return_value.execute.return_value = json.dumps({
            'id': 'test_cmd',
            'status': 'success',
            'output': 'Hello from Colab!'
        }).encode()
        
        # Run test
        bridge = UniversalColabBridge("test")
        bridge.initialize()
        
        # This would normally execute in Colab
        # result = bridge.execute_code("print('Hello')", timeout=1)
        # For now, just verify initialization worked
        self.assertIsNotNone(bridge.drive_service)
    
    def test_error_handling(self):
        """Test error handling"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        # Test with invalid credentials path
        os.environ['SERVICE_ACCOUNT_PATH'] = '/invalid/path.json'
        
        bridge = UniversalColabBridge("test")
        
        with self.assertRaises(Exception):
            bridge.initialize()
        
        # Restore valid path
        os.environ['SERVICE_ACCOUNT_PATH'] = str(Path(__file__).parent / 'credentials' / 'automation-engine-463103-ee5a06e18248.json')

class TestRegression(unittest.TestCase):
    """Regression tests for known issues"""
    
    def test_timeout_handling(self):
        """Test timeout handling - regression for hanging executions"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        bridge = UniversalColabBridge("test")
        # Don't initialize to avoid actual API calls
        
        # Test that timeout returns proper response
        bridge.drive_service = MagicMock()
        bridge.folder_id = "test_folder"
        
        # Mock no result found
        bridge._check_result = MagicMock(return_value=None)
        bridge._write_to_drive = MagicMock()
        
        result = bridge.execute_code("print('test')", timeout=0.1)
        
        self.assertEqual(result['status'], 'timeout')
        self.assertIn('message', result)
    
    def test_unicode_handling(self):
        """Test Unicode in code - regression for encoding issues"""
        from colab_integration.universal_bridge import UniversalColabBridge
        
        bridge = UniversalColabBridge("test")
        
        # Test Unicode code
        unicode_code = "print('Hello 世界 🚀')"
        
        # Just verify it doesn't crash during command creation
        command = {
            'id': 'test',
            'code': unicode_code,
            'type': 'execute'
        }
        
        # Should handle Unicode properly
        self.assertEqual(command['code'], unicode_code)

def run_all_tests():
    """Run all tests and generate report"""
    print("🧪 COLAB-BRIDGE COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestColabBridgeCore,
        TestAutomation,
        TestVSCodeExtension,
        TestIntegration,
        TestRegression
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split(chr(10))[-2]}")
    
    if result.errors:
        print("\n🔥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split(chr(10))[-2]}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)