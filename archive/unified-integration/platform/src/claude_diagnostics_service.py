"""
Claude Diagnostics Service - Integrated with Flask App
Real-time troubleshooting and auto-fixing for Claude integration
"""

import os
from typing import Dict, Any
from src.claude_troubleshooter import ClaudeTroubleshooter


class ClaudeDiagnosticsService:
    """Service for real-time Claude diagnostics within the app"""
    
    def __init__(self):
        self.troubleshooter = None
        self._last_diagnosis = None
        self._cache_timeout = 300  # 5 minutes
        
    def get_troubleshooter(self) -> ClaudeTroubleshooter:
        """Get troubleshooter instance with proper API key"""
        if not self.troubleshooter:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            self.troubleshooter = ClaudeTroubleshooter(api_key)
        return self.troubleshooter
    
    def run_diagnostics(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Run comprehensive diagnostics"""
        troubleshooter = self.get_troubleshooter()
        
        # Use cached results if recent
        if not force_refresh and self._last_diagnosis:
            import time
            if time.time() - self._last_diagnosis.get('_timestamp', 0) < self._cache_timeout:
                return self._last_diagnosis
        
        diagnosis = troubleshooter.generate_health_report()
        diagnosis['_timestamp'] = __import__('time').time()
        self._last_diagnosis = diagnosis
        
        return diagnosis
    
    def auto_fix_models(self, target_files: list = None) -> Dict[str, Any]:
        """Auto-fix model configurations in specified files"""
        if target_files is None:
            target_files = [
                'src/ai_enhancer.py',
                'src/smart_claude_selector.py',
                'src/simple_claude_enhancer.py',
                'src/claude_enhancer.py',
                'src/config.py'
            ]
        
        troubleshooter = self.get_troubleshooter()
        results = []
        
        for file_path in target_files:
            full_path = f"/var/projects/ai-integration-platform/{file_path}"
            if os.path.exists(full_path):
                result = troubleshooter.auto_fix_configuration(full_path)
                result['file'] = file_path
                results.append(result)
        
        return {
            "fixed_files": [r for r in results if r.get("success")],
            "failed_files": [r for r in results if not r.get("success")],
            "total_files": len(results)
        }
    
    def validate_current_models(self) -> Dict[str, Any]:
        """Validate models currently being used in the app"""
        troubleshooter = self.get_troubleshooter()
        
        # Get current models from various sources
        current_models = set()
        
        # From smart selector
        try:
            from src.smart_claude_selector import ModelTier
            for tier in ModelTier:
                current_models.add(tier.value)
        except:
            pass
            
        # From config
        try:
            from src.config import get_config
            config = get_config()
            current_models.add(config.ai.claude_model)
        except:
            pass
        
        # Test each current model
        validation_results = {}
        for model in current_models:
            result = troubleshooter.test_model(model)
            validation_results[model] = result
            
        working_models = [m for m, r in validation_results.items() if r.get("success")]
        broken_models = [m for m, r in validation_results.items() if not r.get("success")]
        
        return {
            "current_models": list(current_models),
            "working_models": working_models,
            "broken_models": broken_models,
            "validation_results": validation_results,
            "all_models_working": len(broken_models) == 0
        }
    
    def get_recommendations(self) -> Dict[str, Any]:
        """Get specific recommendations for improvement"""
        troubleshooter = self.get_troubleshooter()
        diagnosis = self.run_diagnostics()
        
        recommendations = []
        
        # Check critical issues
        if diagnosis['diagnosis']['critical_issues']:
            recommendations.append({
                "priority": "critical",
                "action": "Fix API Configuration",
                "details": diagnosis['diagnosis']['critical_issues']
            })
        
        # Check model availability
        working_models = diagnosis['diagnosis']['model_availability'].get('working', [])
        if len(working_models) < 2:
            recommendations.append({
                "priority": "high",
                "action": "Expand Model Availability",
                "details": "Only one working model found. Consider updating API or checking model names."
            })
            
        # Check current model validation
        current_validation = self.validate_current_models()
        if current_validation['broken_models']:
            recommendations.append({
                "priority": "high",
                "action": "Fix Broken Models",
                "details": f"These models are failing: {', '.join(current_validation['broken_models'])}"
            })
        
        return {
            "recommendations": recommendations,
            "auto_fix_available": len([r for r in recommendations if r["priority"] in ["high", "critical"]]) > 0
        }


# Global service instance
_diagnostics_service = None


def get_diagnostics_service() -> ClaudeDiagnosticsService:
    """Get global diagnostics service instance"""
    global _diagnostics_service
    if _diagnostics_service is None:
        _diagnostics_service = ClaudeDiagnosticsService()
    return _diagnostics_service