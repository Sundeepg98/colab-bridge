"""
Claude Auto-Troubleshooter
Automatically detects, validates, and fixes Claude model configuration issues.
"""

import os
import logging
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import anthropic
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeTroubleshooter:
    """Automatically troubleshoot and fix Claude integration issues"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        self.troubleshoot_log = []
        
        # Known model patterns to test
        self.known_models = [
            # Current generation models
            "claude-3-5-sonnet-20241022",
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229",
            
            # Potential newer models to test
            "claude-3-5-sonnet-20250101",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20241022",
            
            # Legacy models
            "claude-instant-1.2",
            "claude-2.1",
            "claude-2.0"
        ]
        
        self.validated_models = []
        self.failed_models = []
        
    def initialize_client(self) -> bool:
        """Initialize Claude client with error handling"""
        try:
            if not self.api_key:
                self.log_issue("No API key found", "critical")
                return False
                
            self.client = Anthropic(api_key=self.api_key)
            self.log_issue("Client initialized successfully", "info")
            return True
            
        except Exception as e:
            self.log_issue(f"Client initialization failed: {e}", "error")
            return False
    
    def test_model(self, model_name: str, timeout: float = 5.0) -> Dict[str, Any]:
        """Test a specific model with minimal request"""
        if not self.client:
            return {"success": False, "error": "Client not initialized"}
            
        try:
            start_time = datetime.now()
            
            response = self.client.messages.create(
                model=model_name,
                max_tokens=5,
                messages=[{"role": "user", "content": "Hi"}],
                timeout=timeout
            )
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            return {
                "success": True,
                "model": model_name,
                "response_time": response_time,
                "tokens": response.usage.output_tokens if hasattr(response, 'usage') else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = str(e)
            error_type = "unknown"
            
            if "not_found_error" in error_msg or "404" in error_msg:
                error_type = "model_not_found"
            elif "rate_limit" in error_msg.lower():
                error_type = "rate_limit"
            elif "authentication" in error_msg.lower():
                error_type = "auth_error"
            elif "timeout" in error_msg.lower():
                error_type = "timeout"
                
            return {
                "success": False,
                "model": model_name,
                "error": error_msg,
                "error_type": error_type,
                "timestamp": datetime.now().isoformat()
            }
    
    def auto_detect_working_models(self) -> Dict[str, List[str]]:
        """Automatically detect which models are available"""
        if not self.initialize_client():
            return {"working": [], "failed": []}
            
        self.log_issue("Starting model auto-detection", "info")
        
        working_models = []
        failed_models = []
        
        for model in self.known_models:
            self.log_issue(f"Testing model: {model}", "info")
            result = self.test_model(model)
            
            if result["success"]:
                working_models.append({
                    "model": model,
                    "response_time": result["response_time"]
                })
                self.log_issue(f"✅ {model} - Working ({result['response_time']:.2f}s)", "success")
            else:
                failed_models.append({
                    "model": model,
                    "error": result["error"],
                    "error_type": result["error_type"]
                })
                self.log_issue(f"❌ {model} - {result['error_type']}: {result['error']}", "warning")
        
        # Sort by response time (fastest first)
        working_models.sort(key=lambda x: x["response_time"])
        
        self.validated_models = [m["model"] for m in working_models]
        self.failed_models = [m["model"] for m in failed_models]
        
        return {
            "working": working_models,
            "failed": failed_models,
            "total_tested": len(self.known_models),
            "success_rate": len(working_models) / len(self.known_models) if self.known_models else 0
        }
    
    def get_recommended_models(self) -> Dict[str, str]:
        """Get recommended model configuration based on testing"""
        if not self.validated_models:
            self.auto_detect_working_models()
            
        if not self.validated_models:
            return {
                "error": "No working models found",
                "recommendation": "Check API key and network connectivity"
            }
        
        # Categorize models by purpose
        recommendations = {}
        
        # Best overall model (prefer Sonnet for balance)
        sonnet_models = [m for m in self.validated_models if "sonnet" in m.lower()]
        if sonnet_models:
            recommendations["primary"] = sonnet_models[0]
        else:
            recommendations["primary"] = self.validated_models[0]
            
        # Fast model (prefer Haiku)
        haiku_models = [m for m in self.validated_models if "haiku" in m.lower()]
        if haiku_models:
            recommendations["fast"] = haiku_models[0]
        else:
            recommendations["fast"] = self.validated_models[-1]  # Last (likely fastest tested)
            
        # Premium model (prefer Opus)
        opus_models = [m for m in self.validated_models if "opus" in m.lower()]
        if opus_models:
            recommendations["premium"] = opus_models[0]
        else:
            recommendations["premium"] = recommendations["primary"]
            
        return recommendations
    
    def diagnose_integration_issues(self) -> Dict[str, Any]:
        """Comprehensive diagnosis of Claude integration"""
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "api_key_status": "missing",
            "client_status": "not_initialized",
            "model_availability": {},
            "recommendations": [],
            "critical_issues": [],
            "warnings": []
        }
        
        # Check API key
        if self.api_key:
            diagnosis["api_key_status"] = "present"
            if len(self.api_key) > 20:
                diagnosis["api_key_status"] = "valid_format"
        else:
            diagnosis["critical_issues"].append("ANTHROPIC_API_KEY environment variable not set")
            
        # Test client initialization
        if self.initialize_client():
            diagnosis["client_status"] = "initialized"
        else:
            diagnosis["critical_issues"].append("Failed to initialize Claude client")
            
        # Test model availability
        model_results = self.auto_detect_working_models()
        diagnosis["model_availability"] = model_results
        
        if not model_results["working"]:
            diagnosis["critical_issues"].append("No working Claude models found")
        elif len(model_results["working"]) < 2:
            diagnosis["warnings"].append("Limited model availability - only one model working")
            
        # Generate recommendations
        if diagnosis["critical_issues"]:
            diagnosis["recommendations"].append("Fix critical issues before proceeding")
        else:
            recommended_models = self.get_recommended_models()
            diagnosis["recommended_config"] = recommended_models
            diagnosis["recommendations"].append("Use recommended model configuration")
            
        return diagnosis
    
    def auto_fix_configuration(self, config_file_path: str) -> Dict[str, Any]:
        """Automatically fix configuration files with working models"""
        try:
            diagnosis = self.diagnose_integration_issues()
            
            if diagnosis["critical_issues"]:
                return {
                    "success": False,
                    "error": "Cannot auto-fix due to critical issues",
                    "issues": diagnosis["critical_issues"]
                }
                
            recommended = diagnosis.get("recommended_config", {})
            if not recommended:
                return {
                    "success": False,
                    "error": "No working models to configure"
                }
                
            # Read current config
            config_content = ""
            if os.path.exists(config_file_path):
                with open(config_file_path, 'r') as f:
                    config_content = f.read()
                    
            # Apply fixes
            fixes_applied = []
            
            # Update model names in various patterns
            old_models = [m["model"] for m in diagnosis["model_availability"]["failed"]]
            for old_model in old_models:
                if old_model in config_content:
                    config_content = config_content.replace(old_model, recommended["primary"])
                    fixes_applied.append(f"Replaced {old_model} with {recommended['primary']}")
                    
            # Write back fixed config
            with open(config_file_path, 'w') as f:
                f.write(config_content)
                
            return {
                "success": True,
                "fixes_applied": fixes_applied,
                "recommended_config": recommended,
                "config_file": config_file_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Auto-fix failed: {e}"
            }
    
    def log_issue(self, message: str, level: str = "info"):
        """Log troubleshooting issues"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        self.troubleshoot_log.append(log_entry)
        
        # Also log to standard logger
        if level == "critical" or level == "error":
            logger.error(f"Claude Troubleshooter: {message}")
        elif level == "warning":
            logger.warning(f"Claude Troubleshooter: {message}")
        elif level == "success":
            logger.info(f"Claude Troubleshooter: ✅ {message}")
        else:
            logger.info(f"Claude Troubleshooter: {message}")
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        diagnosis = self.diagnose_integration_issues()
        
        # Calculate health score
        health_score = 100
        if diagnosis["critical_issues"]:
            health_score -= len(diagnosis["critical_issues"]) * 30
        if diagnosis["warnings"]:
            health_score -= len(diagnosis["warnings"]) * 10
            
        working_models = diagnosis["model_availability"].get("working", [])
        if working_models:
            health_score += min(len(working_models) * 5, 20)  # Bonus for multiple models
            
        health_score = max(0, min(100, health_score))
        
        return {
            "health_score": health_score,
            "status": "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "critical",
            "diagnosis": diagnosis,
            "troubleshoot_log": self.troubleshoot_log[-10:],  # Last 10 entries
            "timestamp": datetime.now().isoformat()
        }
    
    def save_diagnostics(self, file_path: str = "/var/projects/ai-integration-platform/claude_diagnostics.json"):
        """Save diagnostic results to file"""
        try:
            report = self.generate_health_report()
            with open(file_path, 'w') as f:
                json.dump(report, f, indent=2)
            self.log_issue(f"Diagnostics saved to {file_path}", "info")
            return True
        except Exception as e:
            self.log_issue(f"Failed to save diagnostics: {e}", "error")
            return False


def run_auto_troubleshoot() -> Dict[str, Any]:
    """Run complete auto-troubleshooting process"""
    troubleshooter = ClaudeTroubleshooter()
    
    print("🔍 Starting Claude Auto-Troubleshooter...")
    
    # Run comprehensive diagnosis
    health_report = troubleshooter.generate_health_report()
    
    print(f"\n📊 Health Score: {health_report['health_score']}/100")
    print(f"🔶 Status: {health_report['status'].upper()}")
    
    diagnosis = health_report['diagnosis']
    
    if diagnosis['critical_issues']:
        print(f"\n❌ Critical Issues ({len(diagnosis['critical_issues'])}):")
        for issue in diagnosis['critical_issues']:
            print(f"   • {issue}")
            
    if diagnosis['warnings']:
        print(f"\n⚠️  Warnings ({len(diagnosis['warnings'])}):")
        for warning in diagnosis['warnings']:
            print(f"   • {warning}")
            
    working_models = diagnosis['model_availability'].get('working', [])
    if working_models:
        print(f"\n✅ Working Models ({len(working_models)}):")
        for model_info in working_models:
            print(f"   • {model_info['model']} ({model_info['response_time']:.2f}s)")
            
    if 'recommended_config' in diagnosis:
        print(f"\n🎯 Recommended Configuration:")
        for purpose, model in diagnosis['recommended_config'].items():
            print(f"   • {purpose}: {model}")
    
    # Save diagnostics
    troubleshooter.save_diagnostics()
    
    return health_report


if __name__ == "__main__":
    run_auto_troubleshoot()