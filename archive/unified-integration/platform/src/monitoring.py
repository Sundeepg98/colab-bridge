"""
Enterprise Monitoring and Analytics

Implements comprehensive monitoring, metrics collection, and analytics
for the Ai Integration Platform.
"""

import time
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
from enum import Enum
import threading
import logging
from functools import wraps
from src.config import get_config


logger = logging.getLogger(__name__)


class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class Metric:
    name: str
    value: float
    metric_type: MetricType
    tags: Dict[str, str]
    timestamp: datetime


@dataclass
class PerformanceStats:
    endpoint: str
    response_time_ms: float
    status_code: int
    request_size_bytes: int
    response_size_bytes: int
    timestamp: datetime
    api_key_tier: Optional[str] = None
    optimization_strategy: Optional[str] = None


@dataclass
class UsageStats:
    endpoint: str
    user_tier: str
    tokens_processed: int
    optimization_type: str
    success: bool
    timestamp: datetime


@dataclass
class ErrorEvent:
    endpoint: str
    error_type: str
    error_message: str
    stack_trace: Optional[str]
    request_data: Dict[str, Any]
    timestamp: datetime


class MonitoringManager:
    """Manages monitoring, metrics, and analytics"""
    
    def __init__(self):
        self.config = get_config()
        self.metrics: Dict[str, Metric] = {}
        self.performance_stats: deque = deque(maxlen=10000)
        self.usage_stats: deque = deque(maxlen=10000)
        self.error_events: deque = deque(maxlen=1000)
        
        # Real-time counters
        self.request_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
        self.optimization_success_rates = defaultdict(lambda: {"success": 0, "total": 0})
        
        # Performance tracking
        self.response_times = defaultdict(list)
        self.active_requests = {}
        
        # Lock for thread safety
        self._lock = threading.Lock()
        
        # Health check status
        self.health_status = {
            "status": "healthy",
            "checks": {},
            "last_check": datetime.now()
        }
    
    def record_metric(self, name: str, value: float, metric_type: MetricType,
                     tags: Optional[Dict[str, str]] = None):
        """Record a metric"""
        if not self.config.monitoring.enable_metrics:
            return
        
        with self._lock:
            metric = Metric(
                name=name,
                value=value,
                metric_type=metric_type,
                tags=tags or {},
                timestamp=datetime.now()
            )
            self.metrics[f"{name}_{int(time.time())}"] = metric
    
    def start_request_timer(self, request_id: str, endpoint: str):
        """Start timing a request"""
        if not self.config.monitoring.enable_metrics:
            return
        
        self.active_requests[request_id] = {
            "endpoint": endpoint,
            "start_time": time.time(),
            "timestamp": datetime.now()
        }
    
    def end_request_timer(self, request_id: str, status_code: int = 200,
                         request_size: int = 0, response_size: int = 0,
                         api_key_tier: Optional[str] = None,
                         optimization_strategy: Optional[str] = None):
        """End timing a request and record performance stats"""
        if not self.config.monitoring.enable_metrics or request_id not in self.active_requests:
            return
        
        request_info = self.active_requests.pop(request_id)
        response_time = (time.time() - request_info["start_time"]) * 1000  # Convert to ms
        
        with self._lock:
            # Record performance stats
            stats = PerformanceStats(
                endpoint=request_info["endpoint"],
                response_time_ms=response_time,
                status_code=status_code,
                request_size_bytes=request_size,
                response_size_bytes=response_size,
                timestamp=request_info["timestamp"],
                api_key_tier=api_key_tier,
                optimization_strategy=optimization_strategy
            )
            self.performance_stats.append(stats)
            
            # Update real-time counters
            self.request_counts[request_info["endpoint"]] += 1
            self.response_times[request_info["endpoint"]].append(response_time)
            
            # Keep only recent response times
            if len(self.response_times[request_info["endpoint"]]) > 100:
                self.response_times[request_info["endpoint"]] = \
                    self.response_times[request_info["endpoint"]][-100:]
            
            # Record metrics
            self.record_metric(
                "request_duration_ms",
                response_time,
                MetricType.HISTOGRAM,
                {"endpoint": request_info["endpoint"], "status": str(status_code)}
            )
            
            self.record_metric(
                "requests_total",
                1,
                MetricType.COUNTER,
                {"endpoint": request_info["endpoint"], "status": str(status_code)}
            )
    
    def record_usage(self, endpoint: str, user_tier: str, tokens_processed: int,
                    optimization_type: str, success: bool):
        """Record usage statistics"""
        if not self.config.monitoring.enable_metrics:
            return
        
        with self._lock:
            usage = UsageStats(
                endpoint=endpoint,
                user_tier=user_tier,
                tokens_processed=tokens_processed,
                optimization_type=optimization_type,
                success=success,
                timestamp=datetime.now()
            )
            self.usage_stats.append(usage)
            
            # Update success rates
            self.optimization_success_rates[optimization_type]["total"] += 1
            if success:
                self.optimization_success_rates[optimization_type]["success"] += 1
    
    def record_error(self, endpoint: str, error_type: str, error_message: str,
                    stack_trace: Optional[str] = None,
                    request_data: Optional[Dict[str, Any]] = None):
        """Record error event"""
        if not self.config.monitoring.enable_error_tracking:
            return
        
        with self._lock:
            error = ErrorEvent(
                endpoint=endpoint,
                error_type=error_type,
                error_message=error_message,
                stack_trace=stack_trace,
                request_data=request_data or {},
                timestamp=datetime.now()
            )
            self.error_events.append(error)
            self.error_counts[endpoint] += 1
            
            # Log error
            logger.error(f"Error in {endpoint}: {error_message}", extra={
                "endpoint": endpoint,
                "error_type": error_type,
                "request_data": request_data
            })
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        with self._lock:
            now = datetime.now()
            hour_ago = now - timedelta(hours=1)
            
            # Filter recent stats
            recent_performance = [s for s in self.performance_stats 
                                if s.timestamp > hour_ago]
            recent_usage = [s for s in self.usage_stats 
                          if s.timestamp > hour_ago]
            recent_errors = [e for e in self.error_events 
                           if e.timestamp > hour_ago]
            
            # Calculate averages
            avg_response_times = {}
            for endpoint, times in self.response_times.items():
                if times:
                    avg_response_times[endpoint] = {
                        "avg_ms": sum(times) / len(times),
                        "min_ms": min(times),
                        "max_ms": max(times),
                        "count": len(times)
                    }
            
            # Success rates
            success_rates = {}
            for opt_type, stats in self.optimization_success_rates.items():
                if stats["total"] > 0:
                    success_rates[opt_type] = stats["success"] / stats["total"]
            
            return {
                "timestamp": now.isoformat(),
                "summary": {
                    "total_requests_hour": len(recent_performance),
                    "total_errors_hour": len(recent_errors),
                    "unique_endpoints": len(set(s.endpoint for s in recent_performance)),
                    "optimization_types": len(set(s.optimization_type for s in recent_usage))
                },
                "performance": {
                    "avg_response_times": avg_response_times,
                    "request_counts": dict(self.request_counts),
                    "error_counts": dict(self.error_counts)
                },
                "optimization": {
                    "success_rates": success_rates,
                    "usage_by_tier": self._group_usage_by_tier(recent_usage)
                },
                "health": self.health_status
            }
    
    def _group_usage_by_tier(self, usage_stats: List[UsageStats]) -> Dict[str, Any]:
        """Group usage statistics by user tier"""
        by_tier = defaultdict(lambda: {"requests": 0, "tokens": 0})
        
        for usage in usage_stats:
            by_tier[usage.user_tier]["requests"] += 1
            by_tier[usage.user_tier]["tokens"] += usage.tokens_processed
        
        return dict(by_tier)
    
    def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        checks = {}
        overall_status = "healthy"
        
        # Check API responsiveness
        try:
            response_time_check = self._check_average_response_time()
            checks["response_time"] = response_time_check
            if not response_time_check["healthy"]:
                overall_status = "degraded"
        except Exception as e:
            checks["response_time"] = {"healthy": False, "error": str(e)}
            overall_status = "unhealthy"
        
        # Check error rate
        try:
            error_rate_check = self._check_error_rate()
            checks["error_rate"] = error_rate_check
            if not error_rate_check["healthy"]:
                overall_status = "degraded"
        except Exception as e:
            checks["error_rate"] = {"healthy": False, "error": str(e)}
            overall_status = "unhealthy"
        
        # Check memory usage (simplified)
        try:
            memory_check = self._check_memory_usage()
            checks["memory"] = memory_check
            if not memory_check["healthy"]:
                overall_status = "degraded"
        except Exception as e:
            checks["memory"] = {"healthy": False, "error": str(e)}
            overall_status = "unhealthy"
        
        self.health_status = {
            "status": overall_status,
            "checks": checks,
            "last_check": datetime.now()
        }
        
        return self.health_status
    
    def _check_average_response_time(self) -> Dict[str, Any]:
        """Check if average response time is acceptable"""
        threshold_ms = 5000  # 5 seconds
        
        all_times = []
        for times in self.response_times.values():
            all_times.extend(times)
        
        if not all_times:
            return {"healthy": True, "message": "No requests to check"}
        
        avg_time = sum(all_times) / len(all_times)
        healthy = avg_time < threshold_ms
        
        return {
            "healthy": healthy,
            "avg_response_time_ms": avg_time,
            "threshold_ms": threshold_ms,
            "message": f"Average response time: {avg_time:.2f}ms"
        }
    
    def _check_error_rate(self) -> Dict[str, Any]:
        """Check if error rate is acceptable"""
        threshold_percent = 5.0  # 5%
        
        hour_ago = datetime.now() - timedelta(hours=1)
        recent_requests = len([s for s in self.performance_stats if s.timestamp > hour_ago])
        recent_errors = len([e for e in self.error_events if e.timestamp > hour_ago])
        
        if recent_requests == 0:
            return {"healthy": True, "message": "No requests to check"}
        
        error_rate = (recent_errors / recent_requests) * 100
        healthy = error_rate < threshold_percent
        
        return {
            "healthy": healthy,
            "error_rate_percent": error_rate,
            "threshold_percent": threshold_percent,
            "recent_requests": recent_requests,
            "recent_errors": recent_errors,
            "message": f"Error rate: {error_rate:.2f}%"
        }
    
    def _check_memory_usage(self) -> Dict[str, Any]:
        """Check memory usage (simplified check)"""
        # In a real implementation, this would check actual memory usage
        # For now, we'll check the size of our data structures
        
        total_items = (len(self.performance_stats) + 
                      len(self.usage_stats) + 
                      len(self.error_events) + 
                      len(self.metrics))
        
        threshold = 20000  # items
        healthy = total_items < threshold
        
        return {
            "healthy": healthy,
            "total_items": total_items,
            "threshold": threshold,
            "message": f"Monitoring data items: {total_items}"
        }
    
    def export_metrics_prometheus(self) -> str:
        """Export metrics in Prometheus format"""
        lines = []
        
        # Add help and type comments
        lines.append("# HELP sora_requests_total Total number of requests")
        lines.append("# TYPE sora_requests_total counter")
        
        # Export request counts
        for endpoint, count in self.request_counts.items():
            lines.append(f'sora_requests_total{{endpoint="{endpoint}"}} {count}')
        
        # Add response times
        lines.append("# HELP sora_response_time_ms Response time in milliseconds")
        lines.append("# TYPE sora_response_time_ms histogram")
        
        for endpoint, times in self.response_times.items():
            if times:
                avg_time = sum(times) / len(times)
                lines.append(f'sora_response_time_ms{{endpoint="{endpoint}"}} {avg_time}')
        
        return "\n".join(lines)


# Global monitoring manager instance
_monitoring_manager: Optional[MonitoringManager] = None


def get_monitoring_manager() -> MonitoringManager:
    """Get global monitoring manager instance"""
    global _monitoring_manager
    if _monitoring_manager is None:
        _monitoring_manager = MonitoringManager()
    return _monitoring_manager


# Decorators for monitoring
def monitor_performance(f):
    """Decorator to monitor endpoint performance"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        config = get_config()
        if not config.monitoring.enable_metrics:
            return f(*args, **kwargs)
        
        monitoring = get_monitoring_manager()
        request_id = f"{f.__name__}_{int(time.time() * 1000000)}"
        
        # Start monitoring
        monitoring.start_request_timer(request_id, f.__name__)
        
        try:
            result = f(*args, **kwargs)
            
            # Get response info
            status_code = 200
            if hasattr(result, 'status_code'):
                status_code = result.status_code
            elif isinstance(result, tuple) and len(result) > 1:
                status_code = result[1]
            
            # End monitoring
            monitoring.end_request_timer(request_id, status_code)
            
            return result
            
        except Exception as e:
            monitoring.end_request_timer(request_id, 500)
            monitoring.record_error(
                f.__name__,
                type(e).__name__,
                str(e),
                None,  # Stack trace would be added in production
                {"function": f.__name__}
            )
            raise
    
    return decorated_function


def monitor_usage(optimization_type: str = "unknown"):
    """Decorator to monitor usage statistics"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            config = get_config()
            if not config.monitoring.enable_metrics:
                return f(*args, **kwargs)
            
            monitoring = get_monitoring_manager()
            
            try:
                result = f(*args, **kwargs)
                
                # Determine success
                success = True
                if isinstance(result, dict) and "success" in result:
                    success = result["success"]
                elif hasattr(result, 'status_code'):
                    success = 200 <= result.status_code < 400
                
                # Record usage
                user_tier = "unknown"
                from flask import g
                if hasattr(g, 'api_key_info') and g.api_key_info:
                    user_tier = g.api_key_info.get('tier', 'unknown')
                
                # Estimate tokens processed (simplified)
                tokens = 100  # Default estimate
                if isinstance(result, dict) and "optimized" in result:
                    tokens = len(result["optimized"].split())
                
                monitoring.record_usage(
                    f.__name__,
                    user_tier,
                    tokens,
                    optimization_type,
                    success
                )
                
                return result
                
            except Exception as e:
                monitoring.record_usage(f.__name__, "unknown", 0, optimization_type, False)
                raise
        
        return decorated_function
    return decorator