"""
Integration Health Monitoring & User Notification System
Provides real-time monitoring, proactive notifications, and clear error attribution
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import aiohttp
from collections import defaultdict

logger = logging.getLogger(__name__)


class IssueType(Enum):
    """Types of integration issues"""
    # User Issues
    INVALID_API_KEY = "invalid_api_key"
    EXPIRED_API_KEY = "expired_api_key"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    INSUFFICIENT_CREDITS = "insufficient_credits"
    WRONG_PERMISSIONS = "wrong_permissions"
    
    # Platform Issues
    SERVICE_DOWN = "service_down"
    API_CHANGED = "api_changed"
    NETWORK_ERROR = "network_error"
    PLATFORM_BUG = "platform_bug"
    
    # External Issues
    PROVIDER_OUTAGE = "provider_outage"
    PROVIDER_MAINTENANCE = "provider_maintenance"
    PROVIDER_DEGRADED = "provider_degraded"


class NotificationPriority(Enum):
    """Notification priority levels"""
    CRITICAL = "critical"  # Service completely down
    HIGH = "high"         # Degraded performance
    MEDIUM = "medium"     # Minor issues
    LOW = "low"          # Informational
    

@dataclass
class HealthCheckResult:
    """Result of an integration health check"""
    service: str
    user_id: str
    timestamp: datetime
    is_healthy: bool
    response_time_ms: Optional[float] = None
    error_type: Optional[IssueType] = None
    error_message: Optional[str] = None
    error_details: Dict[str, Any] = field(default_factory=dict)
    suggested_action: Optional[str] = None
    is_user_issue: bool = False
    is_platform_issue: bool = False
    is_external_issue: bool = False


@dataclass
class UserNotification:
    """Notification to send to user"""
    user_id: str
    service: str
    priority: NotificationPriority
    title: str
    message: str
    action_required: bool
    action_url: Optional[str] = None
    auto_resolve_possible: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class IntegrationHealthMonitor:
    """Monitors integration health and notifies users proactively"""
    
    def __init__(self):
        self.health_history: Dict[str, List[HealthCheckResult]] = defaultdict(list)
        self.active_issues: Dict[str, Dict[str, Any]] = {}
        self.notification_queue: List[UserNotification] = []
        self.check_interval = 60  # seconds
        self.running = False
        
        # Known error patterns for each service
        self.error_patterns = {
            'openai': {
                'invalid_api_key': ['Invalid API key', 'Incorrect API key provided'],
                'rate_limit': ['Rate limit exceeded', 'Too many requests'],
                'insufficient_credits': ['Insufficient credits', 'quota exceeded'],
                'service_error': ['Internal server error', '503 Service Unavailable']
            },
            'anthropic': {
                'invalid_api_key': ['Invalid x-api-key', 'Authentication failed'],
                'rate_limit': ['rate_limit_error', 'Too many requests'],
                'service_error': ['Internal server error', 'Service temporarily unavailable']
            },
            'stability': {
                'invalid_api_key': ['Unauthorized', 'Invalid API key'],
                'insufficient_credits': ['Insufficient balance', 'Payment required'],
                'service_error': ['Service unavailable', 'Generation failed']
            }
        }
        
        # Service status endpoints
        self.status_endpoints = {
            'openai': 'https://status.openai.com/api/v2/status.json',
            'anthropic': 'https://status.anthropic.com/api/v2/status.json',
            'stability': 'https://api.stability.ai/v1/health'
        }
    
    async def check_user_integration(self, user_id: str, service: str, 
                                   api_key: str, test_request: Dict[str, Any]) -> HealthCheckResult:
        """Check health of a specific user integration"""
        start_time = datetime.now()
        
        try:
            # Make test request to service
            response = await self._make_test_request(service, api_key, test_request)
            response_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            if response['success']:
                return HealthCheckResult(
                    service=service,
                    user_id=user_id,
                    timestamp=datetime.now(),
                    is_healthy=True,
                    response_time_ms=response_time_ms
                )
            else:
                # Analyze error to determine cause
                issue_type, is_user_issue, suggested_action = self._analyze_error(
                    service, response.get('error', ''), response.get('status_code')
                )
                
                return HealthCheckResult(
                    service=service,
                    user_id=user_id,
                    timestamp=datetime.now(),
                    is_healthy=False,
                    error_type=issue_type,
                    error_message=response.get('error', 'Unknown error'),
                    error_details=response,
                    suggested_action=suggested_action,
                    is_user_issue=is_user_issue,
                    is_platform_issue=not is_user_issue and issue_type == IssueType.PLATFORM_BUG,
                    is_external_issue=not is_user_issue and issue_type in [
                        IssueType.PROVIDER_OUTAGE, 
                        IssueType.PROVIDER_MAINTENANCE,
                        IssueType.SERVICE_DOWN
                    ]
                )
                
        except Exception as e:
            logger.error(f"Health check failed for {service}: {e}")
            return HealthCheckResult(
                service=service,
                user_id=user_id,
                timestamp=datetime.now(),
                is_healthy=False,
                error_type=IssueType.PLATFORM_BUG,
                error_message=str(e),
                is_platform_issue=True,
                suggested_action="Our team has been notified and is investigating."
            )
    
    def _analyze_error(self, service: str, error_msg: str, 
                      status_code: Optional[int] = None) -> Tuple[IssueType, bool, str]:
        """Analyze error to determine type and ownership"""
        error_lower = error_msg.lower()
        patterns = self.error_patterns.get(service, {})
        
        # Check for invalid API key
        if any(pattern.lower() in error_lower for pattern in patterns.get('invalid_api_key', [])):
            return (
                IssueType.INVALID_API_KEY, 
                True,  # User issue
                f"Please check your {service} API key in your integrations settings."
            )
        
        # Check for rate limit
        if any(pattern.lower() in error_lower for pattern in patterns.get('rate_limit', [])):
            return (
                IssueType.RATE_LIMIT_EXCEEDED,
                True,  # User issue (they're making too many requests)
                f"You've exceeded {service}'s rate limits. Please wait or upgrade your plan."
            )
        
        # Check for insufficient credits
        if any(pattern.lower() in error_lower for pattern in patterns.get('insufficient_credits', [])):
            return (
                IssueType.INSUFFICIENT_CREDITS,
                True,  # User issue
                f"Your {service} account has insufficient credits. Please add credits to continue."
            )
        
        # Check for service errors
        if status_code and status_code >= 500:
            return (
                IssueType.SERVICE_DOWN,
                False,  # Not user issue
                f"{service} is experiencing issues. We'll automatically retry when it's back."
            )
        
        # Default to platform issue if we can't identify
        return (
            IssueType.PLATFORM_BUG,
            False,
            "We're investigating this issue. Your integration will resume automatically when resolved."
        )
    
    async def _make_test_request(self, service: str, api_key: str, 
                               test_config: Dict[str, Any]) -> Dict[str, Any]:
        """Make a minimal test request to verify integration"""
        try:
            if service == 'openai':
                return await self._test_openai(api_key)
            elif service == 'anthropic':
                return await self._test_anthropic(api_key)
            elif service == 'stability':
                return await self._test_stability(api_key)
            else:
                return {'success': False, 'error': f'Unknown service: {service}'}
                
        except aiohttp.ClientError as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}',
                'status_code': getattr(e, 'status', None)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _test_openai(self, api_key: str) -> Dict[str, Any]:
        """Test OpenAI integration"""
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bearer {api_key}'}
            
            # Simple models endpoint test
            async with session.get(
                'https://api.openai.com/v1/models',
                headers=headers
            ) as response:
                if response.status == 200:
                    return {'success': True}
                else:
                    error_data = await response.json()
                    return {
                        'success': False,
                        'error': error_data.get('error', {}).get('message', 'Unknown error'),
                        'status_code': response.status
                    }
    
    async def _test_anthropic(self, api_key: str) -> Dict[str, Any]:
        """Test Anthropic integration"""
        async with aiohttp.ClientSession() as session:
            headers = {
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            }
            
            # Minimal completion test
            data = {
                'model': 'claude-3-haiku-20240307',
                'max_tokens': 1,
                'messages': [{'role': 'user', 'content': 'Hi'}]
            }
            
            async with session.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    return {'success': True}
                else:
                    error_data = await response.json()
                    return {
                        'success': False,
                        'error': error_data.get('error', {}).get('message', 'Unknown error'),
                        'status_code': response.status
                    }
    
    async def check_provider_status(self, provider: str) -> Dict[str, Any]:
        """Check if provider is having issues"""
        try:
            status_url = self.status_endpoints.get(provider)
            if not status_url:
                return {'status': 'unknown', 'operational': True}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(status_url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Parse status page format
                        is_operational = data.get('status', {}).get('indicator', 'none') == 'none'
                        return {
                            'status': 'operational' if is_operational else 'issues',
                            'operational': is_operational,
                            'description': data.get('status', {}).get('description', '')
                        }
        except:
            # If we can't check status, assume operational
            return {'status': 'unknown', 'operational': True}
    
    def create_user_notification(self, health_result: HealthCheckResult) -> Optional[UserNotification]:
        """Create appropriate notification based on health check result"""
        if health_result.is_healthy:
            return None
        
        # Determine priority
        priority = NotificationPriority.HIGH
        if health_result.error_type in [IssueType.INVALID_API_KEY, IssueType.EXPIRED_API_KEY]:
            priority = NotificationPriority.CRITICAL
        elif health_result.error_type == IssueType.RATE_LIMIT_EXCEEDED:
            priority = NotificationPriority.MEDIUM
        
        # Create title and message
        if health_result.is_user_issue:
            title = f"Action Required: {health_result.service} Integration"
            message = f"Your {health_result.service} integration needs attention: {health_result.suggested_action}"
            action_required = True
            action_url = f"/dashboard/integrations/{health_result.service}/settings"
        elif health_result.is_external_issue:
            title = f"{health_result.service} Service Issue"
            message = f"{health_result.service} is experiencing issues. We'll automatically resume when it's resolved. No action needed from you."
            action_required = False
            action_url = None
        else:
            title = f"Integration Issue Detected"
            message = "We're experiencing a technical issue with your integration. Our team is investigating."
            action_required = False
            action_url = None
        
        return UserNotification(
            user_id=health_result.user_id,
            service=health_result.service,
            priority=priority,
            title=title,
            message=message,
            action_required=action_required,
            action_url=action_url,
            auto_resolve_possible=not health_result.is_user_issue,
            metadata={
                'error_type': health_result.error_type.value if health_result.error_type else None,
                'error_details': health_result.error_details
            }
        )
    
    async def notify_user(self, notification: UserNotification):
        """Send notification to user through available channels"""
        # In-app notification
        await self._send_in_app_notification(notification)
        
        # Email for critical issues
        if notification.priority == NotificationPriority.CRITICAL:
            await self._send_email_notification(notification)
        
        # SMS for urgent user actions
        if notification.action_required and notification.priority == NotificationPriority.CRITICAL:
            await self._send_sms_notification(notification)
    
    async def _send_in_app_notification(self, notification: UserNotification):
        """Send in-app notification"""
        # Store in database for user dashboard
        # This would integrate with your notification system
        logger.info(f"In-app notification for user {notification.user_id}: {notification.title}")
    
    def get_integration_status_message(self, service: str, health_results: List[HealthCheckResult]) -> Dict[str, Any]:
        """Get user-friendly status message for integration"""
        if not health_results:
            return {
                'status': 'unknown',
                'message': 'No health data available',
                'icon': '❓'
            }
        
        latest = health_results[-1]
        
        if latest.is_healthy:
            avg_response_time = sum(r.response_time_ms for r in health_results[-10:] if r.response_time_ms) / min(10, len(health_results))
            return {
                'status': 'healthy',
                'message': f'Working perfectly ({avg_response_time:.0f}ms avg)',
                'icon': '✅',
                'details': {
                    'uptime': self._calculate_uptime(health_results),
                    'avg_response_time': avg_response_time
                }
            }
        
        if latest.is_user_issue:
            return {
                'status': 'user_action_required',
                'message': latest.suggested_action,
                'icon': '⚠️',
                'action_url': f'/dashboard/integrations/{service}/settings'
            }
        
        if latest.is_external_issue:
            return {
                'status': 'external_issue',
                'message': f'{service} is experiencing issues. No action needed.',
                'icon': '🔧',
                'auto_retry': True
            }
        
        return {
            'status': 'investigating',
            'message': 'We\'re investigating an issue with this integration.',
            'icon': '🔍'
        }
    
    def _calculate_uptime(self, health_results: List[HealthCheckResult]) -> float:
        """Calculate uptime percentage"""
        if not health_results:
            return 0.0
        
        healthy_count = sum(1 for r in health_results if r.is_healthy)
        return (healthy_count / len(health_results)) * 100


# Integration with the main system
class ResponsiveIntegrationSupport:
    """Main class for responsive integration support"""
    
    def __init__(self):
        self.monitor = IntegrationHealthMonitor()
        self.user_integrations = {}  # user_id -> {service -> integration_config}
    
    async def on_integration_added(self, user_id: str, service: str, api_key: str):
        """When user adds new integration, immediately test it"""
        result = await self.monitor.check_user_integration(
            user_id, service, api_key, {}
        )
        
        if not result.is_healthy:
            # Immediate feedback
            notification = self.monitor.create_user_notification(result)
            if notification:
                await self.monitor.notify_user(notification)
            
            return {
                'success': False,
                'error': result.error_message,
                'user_action_required': result.is_user_issue,
                'suggested_action': result.suggested_action
            }
        
        return {
            'success': True,
            'message': f'{service} integration verified and working!',
            'response_time_ms': result.response_time_ms
        }
    
    async def on_request_failed(self, user_id: str, service: str, 
                               error: Exception, request_data: Dict[str, Any]):
        """When a user request fails, determine cause and notify appropriately"""
        # Quick analysis
        api_key = self.user_integrations.get(user_id, {}).get(service, {}).get('api_key')
        if not api_key:
            return
        
        result = await self.monitor.check_user_integration(
            user_id, service, api_key, request_data
        )
        
        # Only notify if this is a new issue
        key = f"{user_id}:{service}"
        if key not in self.monitor.active_issues:
            self.monitor.active_issues[key] = {
                'first_seen': datetime.now(),
                'last_seen': datetime.now(),
                'count': 1,
                'notified': False
            }
            
            notification = self.monitor.create_user_notification(result)
            if notification:
                await self.monitor.notify_user(notification)
                self.monitor.active_issues[key]['notified'] = True
    
    def get_user_integration_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive integration status for user dashboard"""
        user_integrations = self.user_integrations.get(user_id, {})
        dashboard_data = {
            'integrations': {},
            'has_issues': False,
            'action_required': False
        }
        
        for service, config in user_integrations.items():
            # Get recent health checks
            health_results = [
                r for r in self.monitor.health_history[f"{user_id}:{service}"]
                if r.timestamp > datetime.now() - timedelta(hours=24)
            ]
            
            status = self.monitor.get_integration_status_message(service, health_results)
            dashboard_data['integrations'][service] = status
            
            if status['status'] != 'healthy':
                dashboard_data['has_issues'] = True
            if status['status'] == 'user_action_required':
                dashboard_data['action_required'] = True
        
        return dashboard_data


# Global instance
_integration_support: Optional[ResponsiveIntegrationSupport] = None

def get_integration_support() -> ResponsiveIntegrationSupport:
    """Get global integration support instance"""
    global _integration_support
    if _integration_support is None:
        _integration_support = ResponsiveIntegrationSupport()
    return _integration_support