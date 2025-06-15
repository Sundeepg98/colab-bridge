"""
Claude API Health Check Module

Checks Claude API availability at startup and periodically.
Automatically enables/disables Claude features based on API health.
"""

import os
import time
import threading
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json

logger = logging.getLogger(__name__)

class ClaudeHealthChecker:
    """Manages Claude API health checks and feature availability"""
    
    def __init__(self):
        self.is_available = False
        self.last_check_time = None
        self.last_check_status = None
        self.check_interval = 300  # 5 minutes
        # Temporarily disable Claude by default
        self._force_disabled = False
        self.consecutive_failures = 0
        self.max_failures = 3
        self._stop_monitoring = False
        self._monitor_thread = None
        
    def test_claude_api(self) -> Dict[str, Any]:
        """Test Claude API with a simple request"""
        try:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key or not api_key.strip():
                return {
                    'success': False,
                    'error': 'No API key configured',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Try to import and use anthropic
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                
                # Make a minimal test request
                start_time = time.time()
                response = client.messages.create(
                    model="claude-3-haiku-20240307",  # Use cheapest model for health check
                    max_tokens=10,
                    messages=[
                        {"role": "user", "content": "Hi"}
                    ],
                    timeout=5.0  # 5 second timeout
                )
                
                response_time = time.time() - start_time
                
                return {
                    'success': True,
                    'response_time': response_time,
                    'timestamp': datetime.now().isoformat(),
                    'model_used': 'claude-3-haiku'
                }
                
            except ImportError:
                return {
                    'success': False,
                    'error': 'Anthropic library not installed',
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'API call failed: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Health check error: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def check_health(self) -> bool:
        """Perform health check and update availability status"""
        # Temporarily disabled
        if self._force_disabled:
            logger.info("Claude API is temporarily disabled by configuration")
            self.is_available = False
            self.last_check_time = datetime.now()
            self.last_check_status = {
                'success': False,
                'error': 'Temporarily disabled - see CLAUDE_SETUP.md',
                'timestamp': datetime.now().isoformat()
            }
            self._save_status()
            return False
            
        logger.info("Performing Claude API health check...")
        
        result = self.test_claude_api()
        self.last_check_time = datetime.now()
        self.last_check_status = result
        
        if result['success']:
            self.consecutive_failures = 0
            if not self.is_available:
                logger.info(f"Claude API is now available! Response time: {result.get('response_time', 0):.2f}s")
                self.is_available = True
        else:
            self.consecutive_failures += 1
            logger.warning(f"Claude API check failed: {result.get('error', 'Unknown error')}")
            
            if self.consecutive_failures >= self.max_failures and self.is_available:
                logger.error(f"Claude API disabled after {self.consecutive_failures} consecutive failures")
                self.is_available = False
        
        # Save status to file for persistence
        self._save_status()
        
        return self.is_available
    
    def _save_status(self):
        """Save current status to file"""
        status = {
            'is_available': self.is_available,
            'last_check_time': self.last_check_time.isoformat() if self.last_check_time else None,
            'last_check_status': self.last_check_status,
            'consecutive_failures': self.consecutive_failures
        }
        
        try:
            with open('/var/projects/ai-integration-platform/claude_status.json', 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save Claude status: {e}")
    
    def _load_status(self):
        """Load saved status from file"""
        try:
            with open('/var/projects/ai-integration-platform/claude_status.json', 'r') as f:
                status = json.load(f)
                self.is_available = status.get('is_available', False)
                self.consecutive_failures = status.get('consecutive_failures', 0)
                if status.get('last_check_time'):
                    self.last_check_time = datetime.fromisoformat(status['last_check_time'])
                self.last_check_status = status.get('last_check_status')
                logger.info(f"Loaded Claude status: Available={self.is_available}")
        except Exception as e:
            logger.info(f"No previous Claude status found, starting fresh: {e}")
    
    def start_monitoring(self):
        """Start background monitoring thread"""
        if self._monitor_thread and self._monitor_thread.is_alive():
            logger.warning("Monitoring already running")
            return
        
        self._stop_monitoring = False
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        logger.info(f"Started Claude API monitoring (interval: {self.check_interval}s)")
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while not self._stop_monitoring:
            time.sleep(self.check_interval)
            if not self._stop_monitoring:
                self.check_health()
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self._stop_monitoring = True
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        logger.info("Stopped Claude API monitoring")
    
    def get_status_message(self) -> str:
        """Get user-friendly status message"""
        if self.is_available:
            return "Claude AI enhancement is available"
        else:
            if self.last_check_status and 'error' in self.last_check_status:
                error = self.last_check_status['error']
                if 'No API key' in error:
                    return "Claude AI features are disabled (no API key configured)"
                elif 'rate limit' in error.lower():
                    return "Claude AI temporarily unavailable due to rate limits"
                else:
                    return "Claude AI features temporarily unavailable due to maintenance"
            return "Claude AI features are currently disabled"
    
    def initialize(self) -> bool:
        """Initialize health checker, load previous status, and perform initial check"""
        # Load previous status
        self._load_status()
        
        # If last check was recent (within interval), use that status
        if self.last_check_time and (datetime.now() - self.last_check_time).seconds < self.check_interval:
            logger.info(f"Using recent health check from {self.last_check_time}")
            return self.is_available
        
        # Otherwise perform new check
        return self.check_health()


# Global instance
_health_checker: Optional[ClaudeHealthChecker] = None

def get_health_checker() -> ClaudeHealthChecker:
    """Get global health checker instance"""
    global _health_checker
    if _health_checker is None:
        _health_checker = ClaudeHealthChecker()
    return _health_checker

def is_claude_available() -> bool:
    """Quick check if Claude is available"""
    return get_health_checker().is_available

def get_claude_status() -> Dict[str, Any]:
    """Get detailed Claude status"""
    checker = get_health_checker()
    return {
        'available': checker.is_available,
        'message': checker.get_status_message(),
        'last_check': checker.last_check_time.isoformat() if checker.last_check_time else None,
        'consecutive_failures': checker.consecutive_failures,
        'details': checker.last_check_status
    }