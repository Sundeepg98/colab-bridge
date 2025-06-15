"""
Auto-Maintenance Engine for Integration System
Monitors health, performs self-healing, and maintains integration stability
"""

import os
import json
import time
import threading
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
from collections import deque
import statistics
from pathlib import Path

logger = logging.getLogger(__name__)


class MaintenanceAction(Enum):
    """Types of maintenance actions"""
    HEALTH_CHECK = "health_check"
    KEY_ROTATION = "key_rotation"
    CACHE_CLEANUP = "cache_cleanup"
    PERFORMANCE_TUNING = "performance_tuning"
    ERROR_RECOVERY = "error_recovery"
    COST_OPTIMIZATION = "cost_optimization"
    MODEL_VALIDATION = "model_validation"
    TELEMETRY_SYNC = "telemetry_sync"


class SystemHealth(Enum):
    """Overall system health status"""
    EXCELLENT = "excellent"
    GOOD = "good"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"


@dataclass
class MaintenanceEvent:
    """Record of a maintenance event"""
    timestamp: datetime
    action: MaintenanceAction
    target: str
    status: str
    details: Dict[str, Any]
    duration: float
    automated: bool


@dataclass
class HealthMetrics:
    """Health metrics for an integration"""
    integration_name: str
    availability: float  # Percentage uptime
    avg_response_time: float
    error_rate: float
    success_rate: float
    last_check: datetime
    consecutive_failures: int
    health_score: float  # 0-100


class TelemetryCollector:
    """Collects and manages telemetry data"""
    
    def __init__(self, buffer_size: int = 10000):
        self.events = deque(maxlen=buffer_size)
        self.metrics: Dict[str, deque] = {}
        self.aggregated_data: Dict[str, Any] = {}
        self._lock = threading.Lock()
    
    def record_event(self, event_type: str, data: Dict[str, Any]):
        """Record a telemetry event"""
        with self._lock:
            event = {
                'timestamp': datetime.now().isoformat(),
                'type': event_type,
                'data': data
            }
            self.events.append(event)
            
            # Update metrics
            integration = data.get('integration', 'system')
            if integration not in self.metrics:
                self.metrics[integration] = deque(maxlen=1000)
            
            self.metrics[integration].append({
                'timestamp': datetime.now(),
                'response_time': data.get('response_time'),
                'success': data.get('success', True),
                'error': data.get('error')
            })
    
    def get_metrics_summary(self, integration: str = None) -> Dict[str, Any]:
        """Get summarized metrics"""
        with self._lock:
            if integration:
                if integration not in self.metrics:
                    return {}
                
                metrics = list(self.metrics[integration])
                if not metrics:
                    return {}
                
                response_times = [m['response_time'] for m in metrics if m['response_time']]
                successes = [m for m in metrics if m['success']]
                
                return {
                    'total_requests': len(metrics),
                    'success_rate': len(successes) / len(metrics) if metrics else 0,
                    'avg_response_time': statistics.mean(response_times) if response_times else 0,
                    'p95_response_time': statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0,
                    'error_count': len(metrics) - len(successes)
                }
            else:
                # Return summary for all integrations
                summary = {}
                for name, metrics_data in self.metrics.items():
                    summary[name] = self.get_metrics_summary(name)
                return summary
    
    def export_telemetry(self, duration_hours: int = 24) -> Dict[str, Any]:
        """Export telemetry data for analysis"""
        cutoff_time = datetime.now() - timedelta(hours=duration_hours)
        
        with self._lock:
            recent_events = [
                e for e in self.events 
                if datetime.fromisoformat(e['timestamp']) > cutoff_time
            ]
            
            return {
                'export_time': datetime.now().isoformat(),
                'duration_hours': duration_hours,
                'total_events': len(recent_events),
                'events_by_type': self._group_events_by_type(recent_events),
                'metrics_summary': self.get_metrics_summary(),
                'recent_events': recent_events[-100:]  # Last 100 events
            }
    
    def _group_events_by_type(self, events: List[Dict]) -> Dict[str, int]:
        """Group events by type"""
        grouped = {}
        for event in events:
            event_type = event['type']
            grouped[event_type] = grouped.get(event_type, 0) + 1
        return grouped


class AutoMaintenanceEngine:
    """Automatic maintenance engine for integration system"""
    
    def __init__(self):
        self.telemetry = TelemetryCollector()
        self.health_metrics: Dict[str, HealthMetrics] = {}
        self.maintenance_history: List[MaintenanceEvent] = []
        self.maintenance_rules: Dict[str, Callable] = {}
        self.notification_handlers: List[Callable] = []
        self.running = False
        self.maintenance_thread = None
        self.check_interval = 60  # seconds
        self.last_full_maintenance = datetime.now()
        
        # Initialize maintenance rules
        self._setup_maintenance_rules()
    
    def _setup_maintenance_rules(self):
        """Setup automatic maintenance rules"""
        self.maintenance_rules = {
            'health_check': self._health_check_rule,
            'error_recovery': self._error_recovery_rule,
            'performance_optimization': self._performance_optimization_rule,
            'cost_monitoring': self._cost_monitoring_rule,
            'cache_management': self._cache_management_rule,
            'model_validation': self._model_validation_rule
        }
    
    def start(self):
        """Start the maintenance engine"""
        if not self.running:
            self.running = True
            self.maintenance_thread = threading.Thread(
                target=self._maintenance_loop,
                daemon=True
            )
            self.maintenance_thread.start()
            logger.info("Auto-maintenance engine started")
            self._notify("Maintenance engine started", "system", "info")
    
    def stop(self):
        """Stop the maintenance engine"""
        self.running = False
        if self.maintenance_thread:
            self.maintenance_thread.join(timeout=5)
        logger.info("Auto-maintenance engine stopped")
    
    def _maintenance_loop(self):
        """Main maintenance loop"""
        while self.running:
            try:
                # Quick health checks every minute
                self._perform_quick_maintenance()
                
                # Full maintenance every hour
                if datetime.now() - self.last_full_maintenance > timedelta(hours=1):
                    self._perform_full_maintenance()
                    self.last_full_maintenance = datetime.now()
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"Maintenance loop error: {e}")
                self.telemetry.record_event('maintenance_error', {
                    'error': str(e),
                    'action': 'maintenance_loop'
                })
                time.sleep(30)  # Wait before retry
    
    def _perform_quick_maintenance(self):
        """Perform quick maintenance checks"""
        start_time = time.time()
        
        # Run health checks
        for rule_name in ['health_check', 'error_recovery']:
            if rule_name in self.maintenance_rules:
                try:
                    self.maintenance_rules[rule_name]()
                except Exception as e:
                    logger.error(f"Maintenance rule {rule_name} failed: {e}")
        
        duration = time.time() - start_time
        self.telemetry.record_event('quick_maintenance', {
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        })
    
    def _perform_full_maintenance(self):
        """Perform full maintenance"""
        start_time = time.time()
        logger.info("Starting full maintenance cycle")
        
        # Run all maintenance rules
        for rule_name, rule_func in self.maintenance_rules.items():
            try:
                rule_func()
            except Exception as e:
                logger.error(f"Maintenance rule {rule_name} failed: {e}")
                self._record_maintenance_event(
                    MaintenanceAction.ERROR_RECOVERY,
                    rule_name,
                    'failed',
                    {'error': str(e)},
                    0
                )
        
        duration = time.time() - start_time
        self._record_maintenance_event(
            MaintenanceAction.HEALTH_CHECK,
            'system',
            'completed',
            {'type': 'full_maintenance'},
            duration
        )
        
        logger.info(f"Full maintenance completed in {duration:.2f}s")
    
    def _health_check_rule(self):
        """Check health of all integrations"""
        from integration_manager import get_integration_manager
        from api_key_manager import get_api_key_manager
        
        integration_manager = get_integration_manager()
        api_key_manager = get_api_key_manager()
        
        for integration_name in integration_manager.integrations:
            try:
                # Check integration status
                status = integration_manager.get_integration_status(integration_name)
                
                # Get metrics
                today = datetime.now().strftime('%Y-%m-%d')
                metrics = integration_manager.usage_metrics[integration_name][today]
                
                # Calculate health score
                health_score = self._calculate_health_score(status.value, metrics)
                
                # Update health metrics
                self.health_metrics[integration_name] = HealthMetrics(
                    integration_name=integration_name,
                    availability=100.0 if status.value != 'error' else 0.0,
                    avg_response_time=metrics.avg_response_time,
                    error_rate=(metrics.error_count / max(metrics.requests_count, 1)) * 100,
                    success_rate=metrics.success_rate,
                    last_check=datetime.now(),
                    consecutive_failures=0 if metrics.success_rate > 50 else metrics.error_count,
                    health_score=health_score
                )
                
                # Take action based on health
                if health_score < 50:
                    self._handle_unhealthy_integration(integration_name, health_score)
                
                self.telemetry.record_event('health_check', {
                    'integration': integration_name,
                    'health_score': health_score,
                    'status': status.value
                })
                
            except Exception as e:
                logger.error(f"Health check failed for {integration_name}: {e}")
    
    def _calculate_health_score(self, status: str, metrics: Any) -> float:
        """Calculate health score (0-100)"""
        score = 100.0
        
        # Status impact
        status_scores = {
            'healthy': 100,
            'degraded': 70,
            'warning': 50,
            'error': 20,
            'disabled': 0
        }
        score = status_scores.get(status, 50)
        
        # Success rate impact (40% weight)
        if hasattr(metrics, 'success_rate'):
            score = score * 0.6 + metrics.success_rate * 0.4
        
        return max(0, min(100, score))
    
    def _handle_unhealthy_integration(self, integration_name: str, health_score: float):
        """Handle unhealthy integration"""
        logger.warning(f"Integration {integration_name} is unhealthy (score: {health_score})")
        
        # Notify about health issue
        self._notify(
            f"Integration {integration_name} health degraded",
            integration_name,
            'warning',
            {'health_score': health_score}
        )
        
        # Try auto-recovery
        if health_score < 30:
            self._attempt_auto_recovery(integration_name)
    
    def _attempt_auto_recovery(self, integration_name: str):
        """Attempt automatic recovery of integration"""
        logger.info(f"Attempting auto-recovery for {integration_name}")
        
        try:
            from integration_manager import get_integration_manager
            integration_manager = get_integration_manager()
            
            # Clear circuit breaker
            if integration_manager.circuit_breakers.get(integration_name):
                integration_manager.circuit_breakers[integration_name] = False
                logger.info(f"Cleared circuit breaker for {integration_name}")
            
            # Clear status cache to force re-check
            if integration_name in integration_manager.status_cache:
                del integration_manager.status_cache[integration_name]
            
            # Test integration
            new_status = integration_manager.get_integration_status(integration_name)
            
            self._record_maintenance_event(
                MaintenanceAction.ERROR_RECOVERY,
                integration_name,
                'success' if new_status.value != 'error' else 'failed',
                {'new_status': new_status.value},
                0
            )
            
        except Exception as e:
            logger.error(f"Auto-recovery failed for {integration_name}: {e}")
    
    def _error_recovery_rule(self):
        """Monitor and recover from errors"""
        # Check for integrations with high error rates
        for name, health in self.health_metrics.items():
            if health.error_rate > 20:  # More than 20% errors
                logger.warning(f"High error rate detected for {name}: {health.error_rate}%")
                
                # Check if we should disable temporarily
                if health.consecutive_failures > 10:
                    self._temporary_disable_integration(name)
    
    def _temporary_disable_integration(self, integration_name: str, duration_minutes: int = 30):
        """Temporarily disable an integration"""
        from integration_manager import get_integration_manager
        integration_manager = get_integration_manager()
        
        # Set circuit breaker
        integration_manager.circuit_breakers[integration_name] = True
        
        # Schedule re-enable
        def re_enable():
            time.sleep(duration_minutes * 60)
            integration_manager.circuit_breakers[integration_name] = False
            logger.info(f"Re-enabled integration {integration_name}")
            self._notify(
                f"Integration {integration_name} re-enabled",
                integration_name,
                'info'
            )
        
        threading.Thread(target=re_enable, daemon=True).start()
        
        self._notify(
            f"Integration {integration_name} temporarily disabled",
            integration_name,
            'warning',
            {'duration_minutes': duration_minutes}
        )
    
    def _performance_optimization_rule(self):
        """Optimize performance based on metrics"""
        telemetry_summary = self.telemetry.get_metrics_summary()
        
        for integration, metrics in telemetry_summary.items():
            if not metrics:
                continue
            
            # Check response time
            avg_response = metrics.get('avg_response_time', 0)
            if avg_response > 5.0:  # Slow responses
                logger.warning(f"Slow response time for {integration}: {avg_response}s")
                
                # Suggest optimization
                self._notify(
                    f"Performance issue detected for {integration}",
                    integration,
                    'performance',
                    {
                        'avg_response_time': avg_response,
                        'suggestion': 'Consider using lighter models or caching'
                    }
                )
    
    def _cost_monitoring_rule(self):
        """Monitor and optimize costs"""
        from integration_manager import get_integration_manager
        integration_manager = get_integration_manager()
        
        dashboard_data = integration_manager.get_dashboard_data()
        total_cost = dashboard_data['total_cost_today']
        
        # Check if approaching budget limits
        for integration_name, integration_data in dashboard_data['integrations'].items():
            budget_usage = integration_data['budget_usage']
            
            if budget_usage > 0.9:  # Over 90% of budget
                logger.warning(f"Budget alert for {integration_name}: {budget_usage*100:.1f}% used")
                
                self._notify(
                    f"Budget warning for {integration_name}",
                    integration_name,
                    'budget',
                    {
                        'usage_percentage': budget_usage * 100,
                        'recommendation': 'Consider switching to cheaper models'
                    }
                )
    
    def _cache_management_rule(self):
        """Manage caches across the system"""
        # Clear old telemetry data
        old_events = len(self.telemetry.events)
        if old_events > 8000:  # Near buffer limit
            # Export before clearing
            export_data = self.telemetry.export_telemetry(24)
            # Save to file
            self._save_telemetry_export(export_data)
            
            # Clear old events
            with self.telemetry._lock:
                # Keep last 5000 events
                self.telemetry.events = deque(
                    list(self.telemetry.events)[-5000:],
                    maxlen=10000
                )
            
            logger.info(f"Cleared {old_events - 5000} old telemetry events")
    
    def _model_validation_rule(self):
        """Validate available models"""
        from claude_troubleshooter import ClaudeTroubleshooter
        
        try:
            troubleshooter = ClaudeTroubleshooter()
            diagnosis = troubleshooter.run_diagnostics()
            
            if diagnosis['working_models']:
                self.telemetry.record_event('model_validation', {
                    'working_models': len(diagnosis['working_models']),
                    'failed_models': len(diagnosis['failed_models'])
                })
        except Exception as e:
            logger.error(f"Model validation failed: {e}")
    
    def _record_maintenance_event(self, action: MaintenanceAction, target: str, 
                                status: str, details: Dict, duration: float):
        """Record a maintenance event"""
        event = MaintenanceEvent(
            timestamp=datetime.now(),
            action=action,
            target=target,
            status=status,
            details=details,
            duration=duration,
            automated=True
        )
        
        self.maintenance_history.append(event)
        
        # Keep only last 1000 events
        if len(self.maintenance_history) > 1000:
            self.maintenance_history = self.maintenance_history[-1000:]
    
    def _notify(self, message: str, integration: str, level: str, data: Dict = None):
        """Send notification to handlers"""
        notification = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'integration': integration,
            'level': level,
            'data': data or {}
        }
        
        # Log notification
        log_func = getattr(logger, level, logger.info)
        log_func(f"[{integration}] {message}")
        
        # Call notification handlers
        for handler in self.notification_handlers:
            try:
                handler(notification)
            except Exception as e:
                logger.error(f"Notification handler failed: {e}")
    
    def add_notification_handler(self, handler: Callable):
        """Add a notification handler"""
        self.notification_handlers.append(handler)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        if not self.health_metrics:
            return {
                'status': SystemHealth.MAINTENANCE.value,
                'message': 'System initializing'
            }
        
        # Calculate overall health
        health_scores = [h.health_score for h in self.health_metrics.values()]
        avg_health = statistics.mean(health_scores) if health_scores else 0
        
        # Determine status
        if avg_health >= 90:
            status = SystemHealth.EXCELLENT
        elif avg_health >= 70:
            status = SystemHealth.GOOD
        elif avg_health >= 50:
            status = SystemHealth.DEGRADED
        else:
            status = SystemHealth.CRITICAL
        
        return {
            'status': status.value,
            'health_score': avg_health,
            'integrations': {
                name: {
                    'health_score': metrics.health_score,
                    'availability': metrics.availability,
                    'last_check': metrics.last_check.isoformat()
                }
                for name, metrics in self.health_metrics.items()
            },
            'last_maintenance': self.last_full_maintenance.isoformat(),
            'telemetry_summary': self.telemetry.get_metrics_summary()
        }
    
    def get_maintenance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Get maintenance report"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_events = [
            e for e in self.maintenance_history
            if e.timestamp > cutoff_time
        ]
        
        # Group by action
        events_by_action = {}
        for event in recent_events:
            action_name = event.action.value
            if action_name not in events_by_action:
                events_by_action[action_name] = []
            events_by_action[action_name].append({
                'timestamp': event.timestamp.isoformat(),
                'target': event.target,
                'status': event.status,
                'duration': event.duration
            })
        
        return {
            'report_period_hours': hours,
            'total_events': len(recent_events),
            'events_by_action': events_by_action,
            'system_health': self.get_system_health(),
            'recent_notifications': self._get_recent_notifications()
        }
    
    def _get_recent_notifications(self, limit: int = 10) -> List[Dict]:
        """Get recent notifications from telemetry"""
        # This would be implemented with a proper notification store
        return []
    
    def _save_telemetry_export(self, export_data: Dict):
        """Save telemetry export to file"""
        try:
            export_dir = Path("/var/projects/ai-integration-platform/telemetry_exports")
            export_dir.mkdir(exist_ok=True, parents=True)
            
            filename = f"telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = export_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Telemetry exported to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save telemetry export: {e}")
    
    def trigger_maintenance(self, action: MaintenanceAction, target: str = 'system') -> Dict[str, Any]:
        """Manually trigger a maintenance action"""
        logger.info(f"Manual maintenance triggered: {action.value} for {target}")
        
        start_time = time.time()
        
        try:
            if action == MaintenanceAction.HEALTH_CHECK:
                self._health_check_rule()
            elif action == MaintenanceAction.ERROR_RECOVERY:
                self._error_recovery_rule()
            elif action == MaintenanceAction.PERFORMANCE_TUNING:
                self._performance_optimization_rule()
            elif action == MaintenanceAction.COST_OPTIMIZATION:
                self._cost_monitoring_rule()
            elif action == MaintenanceAction.CACHE_CLEANUP:
                self._cache_management_rule()
            elif action == MaintenanceAction.MODEL_VALIDATION:
                self._model_validation_rule()
            
            duration = time.time() - start_time
            
            self._record_maintenance_event(
                action,
                target,
                'completed',
                {'manual': True},
                duration
            )
            
            return {
                'success': True,
                'action': action.value,
                'duration': duration
            }
            
        except Exception as e:
            logger.error(f"Manual maintenance failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }


# Global instance
_maintenance_engine: Optional[AutoMaintenanceEngine] = None


def get_maintenance_engine() -> AutoMaintenanceEngine:
    """Get global maintenance engine instance"""
    global _maintenance_engine
    if _maintenance_engine is None:
        _maintenance_engine = AutoMaintenanceEngine()
        _maintenance_engine.start()
    return _maintenance_engine