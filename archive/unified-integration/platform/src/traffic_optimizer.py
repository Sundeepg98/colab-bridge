"""
Traffic-Based Optimization System

Dynamically adjusts optimization strategy based on:
1. Current traffic load
2. Response time targets
3. Cost constraints
4. User priority levels
"""

import time
import threading
import statistics
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import deque
import logging

logger = logging.getLogger(__name__)


class TrafficLevel(Enum):
    """Current traffic level"""
    LOW = "low"  # < 10 requests/minute
    MODERATE = "moderate"  # 10-50 requests/minute
    HIGH = "high"  # 50-200 requests/minute
    PEAK = "peak"  # > 200 requests/minute


class OptimizationStrategy(Enum):
    """Optimization strategies based on traffic"""
    FULL_QUALITY = "full_quality"  # Low traffic - use all features
    BALANCED = "balanced"  # Moderate traffic - balance quality/speed
    FAST_RESPONSE = "fast_response"  # High traffic - prioritize speed
    EMERGENCY = "emergency"  # Peak traffic - minimal processing


@dataclass
class RequestMetrics:
    """Metrics for a single request"""
    timestamp: datetime
    processing_time: float
    used_claude: bool
    user_tier: str = "basic"
    request_size: int = 0


@dataclass
class TrafficStats:
    """Current traffic statistics"""
    requests_per_minute: float
    avg_response_time: float
    claude_usage_rate: float
    error_rate: float
    queue_depth: int
    active_requests: int


class TrafficOptimizer:
    """Manages optimization based on traffic patterns"""
    
    def __init__(self):
        # Metrics tracking
        self.request_history: deque = deque(maxlen=1000)
        self.response_times: deque = deque(maxlen=100)
        self.claude_calls: deque = deque(maxlen=100)
        
        # Current state
        self.current_traffic_level = TrafficLevel.LOW
        self.current_strategy = OptimizationStrategy.FULL_QUALITY
        self.active_requests = 0
        
        # Configuration
        self.traffic_thresholds = {
            TrafficLevel.LOW: 10,
            TrafficLevel.MODERATE: 50,
            TrafficLevel.HIGH: 200,
            TrafficLevel.PEAK: float('inf')
        }
        
        # Cost tracking
        self.claude_cost_per_1k_tokens = 0.0015  # Haiku pricing
        self.daily_budget = 10.0  # $10/day
        self.current_daily_cost = 0.0
        self.last_cost_reset = datetime.now()
        
        # Performance targets
        self.target_response_times = {
            TrafficLevel.LOW: 3.0,  # 3 seconds
            TrafficLevel.MODERATE: 2.0,  # 2 seconds
            TrafficLevel.HIGH: 1.0,  # 1 second
            TrafficLevel.PEAK: 0.5  # 500ms
        }
        
        # Monitoring thread
        self._stop_monitoring = False
        self._monitor_thread = threading.Thread(target=self._monitor_traffic, daemon=True)
        self._monitor_thread.start()
    
    def _monitor_traffic(self):
        """Background thread to monitor traffic patterns"""
        while not self._stop_monitoring:
            time.sleep(10)  # Check every 10 seconds
            
            # Update traffic level
            stats = self.get_current_stats()
            self._update_traffic_level(stats)
            
            # Adjust strategy
            self._adjust_strategy(stats)
            
            # Reset daily cost if needed
            if (datetime.now() - self.last_cost_reset).days >= 1:
                self.current_daily_cost = 0.0
                self.last_cost_reset = datetime.now()
    
    def _update_traffic_level(self, stats: TrafficStats):
        """Update current traffic level based on stats"""
        rpm = stats.requests_per_minute
        
        if rpm < self.traffic_thresholds[TrafficLevel.LOW]:
            new_level = TrafficLevel.LOW
        elif rpm < self.traffic_thresholds[TrafficLevel.MODERATE]:
            new_level = TrafficLevel.MODERATE
        elif rpm < self.traffic_thresholds[TrafficLevel.HIGH]:
            new_level = TrafficLevel.HIGH
        else:
            new_level = TrafficLevel.PEAK
        
        if new_level != self.current_traffic_level:
            logger.info(f"Traffic level changed: {self.current_traffic_level.value} -> {new_level.value}")
            self.current_traffic_level = new_level
    
    def _adjust_strategy(self, stats: TrafficStats):
        """Adjust optimization strategy based on current conditions"""
        # Check if we're meeting response time targets
        target_time = self.target_response_times[self.current_traffic_level]
        
        if stats.avg_response_time > target_time * 1.5:
            # Too slow - reduce quality
            if self.current_strategy == OptimizationStrategy.FULL_QUALITY:
                self.current_strategy = OptimizationStrategy.BALANCED
            elif self.current_strategy == OptimizationStrategy.BALANCED:
                self.current_strategy = OptimizationStrategy.FAST_RESPONSE
            elif self.current_strategy == OptimizationStrategy.FAST_RESPONSE:
                self.current_strategy = OptimizationStrategy.EMERGENCY
        elif stats.avg_response_time < target_time * 0.5:
            # Room to improve quality
            if self.current_strategy == OptimizationStrategy.EMERGENCY:
                self.current_strategy = OptimizationStrategy.FAST_RESPONSE
            elif self.current_strategy == OptimizationStrategy.FAST_RESPONSE:
                self.current_strategy = OptimizationStrategy.BALANCED
            elif self.current_strategy == OptimizationStrategy.BALANCED:
                self.current_strategy = OptimizationStrategy.FULL_QUALITY
        
        # Check daily budget
        if self.current_daily_cost > self.daily_budget * 0.8:
            # Approaching budget limit - reduce Claude usage
            if self.current_strategy in [OptimizationStrategy.FULL_QUALITY, OptimizationStrategy.BALANCED]:
                self.current_strategy = OptimizationStrategy.FAST_RESPONSE
                logger.warning(f"Approaching daily budget limit: ${self.current_daily_cost:.2f}")
    
    def record_request(self, metrics: RequestMetrics):
        """Record metrics for a completed request"""
        self.request_history.append(metrics)
        self.response_times.append(metrics.processing_time)
        
        if metrics.used_claude:
            self.claude_calls.append(metrics.timestamp)
            # Estimate cost (rough approximation)
            estimated_tokens = metrics.request_size * 2  # Input + output
            estimated_cost = (estimated_tokens / 1000) * self.claude_cost_per_1k_tokens
            self.current_daily_cost += estimated_cost
    
    def get_current_stats(self) -> TrafficStats:
        """Calculate current traffic statistics"""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        # Calculate requests per minute
        recent_requests = [r for r in self.request_history if r.timestamp > one_minute_ago]
        rpm = len(recent_requests)
        
        # Calculate average response time
        avg_response = statistics.mean(self.response_times) if self.response_times else 0.0
        
        # Calculate Claude usage rate
        recent_claude = [c for c in self.claude_calls if c > one_minute_ago]
        claude_rate = len(recent_claude) / max(1, len(recent_requests)) if recent_requests else 0.0
        
        # Estimate error rate (simplified - would track actual errors)
        error_rate = sum(1 for r in recent_requests if r.processing_time > 10.0) / max(1, len(recent_requests))
        
        return TrafficStats(
            requests_per_minute=rpm,
            avg_response_time=avg_response,
            claude_usage_rate=claude_rate,
            error_rate=error_rate,
            queue_depth=0,  # Would implement actual queue
            active_requests=self.active_requests
        )
    
    def should_use_claude(self, user_tier: str = "basic") -> bool:
        """Decide whether to use Claude based on current conditions"""
        # Priority tiers
        tier_priorities = {
            "admin": 1.0,
            "premium": 0.8,
            "basic": 0.5
        }
        priority = tier_priorities.get(user_tier, 0.5)
        
        # Strategy-based decisions
        if self.current_strategy == OptimizationStrategy.FULL_QUALITY:
            return True
        elif self.current_strategy == OptimizationStrategy.BALANCED:
            # Use Claude for premium users or randomly for basic
            return priority > 0.7 or (priority > 0.5 and time.time() % 2 < 1)
        elif self.current_strategy == OptimizationStrategy.FAST_RESPONSE:
            # Only for premium/admin users
            return priority > 0.7
        else:  # EMERGENCY
            # Only for admin users
            return priority >= 1.0
    
    def get_optimization_params(self, user_tier: str = "basic") -> Dict[str, any]:
        """Get optimization parameters based on current strategy"""
        base_params = {
            "use_claude": self.should_use_claude(user_tier),
            "max_processing_time": self.target_response_times[self.current_traffic_level],
            "quality_level": self.current_strategy.value,
            "parallel_processing": False,
            "cache_results": True,
            "batch_size": 1
        }
        
        # Adjust based on strategy
        if self.current_strategy == OptimizationStrategy.FULL_QUALITY:
            base_params.update({
                "quality_level": "maximum",
                "parallel_processing": True,
                "use_all_features": True
            })
        elif self.current_strategy == OptimizationStrategy.BALANCED:
            base_params.update({
                "quality_level": "high",
                "parallel_processing": self.current_traffic_level == TrafficLevel.MODERATE
            })
        elif self.current_strategy == OptimizationStrategy.FAST_RESPONSE:
            base_params.update({
                "quality_level": "medium",
                "use_cached_patterns": True,
                "skip_advanced_features": True
            })
        else:  # EMERGENCY
            base_params.update({
                "quality_level": "basic",
                "use_claude": False,
                "use_cached_only": True,
                "minimal_processing": True
            })
        
        return base_params
    
    def start_request(self) -> str:
        """Mark start of a request and get request ID"""
        self.active_requests += 1
        return f"{datetime.now().timestamp()}-{self.active_requests}"
    
    def end_request(self, request_id: str):
        """Mark end of a request"""
        self.active_requests = max(0, self.active_requests - 1)
    
    def get_traffic_report(self) -> Dict[str, any]:
        """Get comprehensive traffic report"""
        stats = self.get_current_stats()
        
        return {
            "current_level": self.current_traffic_level.value,
            "current_strategy": self.current_strategy.value,
            "stats": {
                "requests_per_minute": stats.requests_per_minute,
                "avg_response_time": f"{stats.avg_response_time:.2f}s",
                "claude_usage_rate": f"{stats.claude_usage_rate:.1%}",
                "error_rate": f"{stats.error_rate:.1%}",
                "active_requests": stats.active_requests
            },
            "cost": {
                "daily_budget": f"${self.daily_budget:.2f}",
                "spent_today": f"${self.current_daily_cost:.2f}",
                "remaining": f"${self.daily_budget - self.current_daily_cost:.2f}"
            },
            "performance": {
                "target_response_time": f"{self.target_response_times[self.current_traffic_level]}s",
                "meeting_target": stats.avg_response_time <= self.target_response_times[self.current_traffic_level]
            }
        }
    
    def shutdown(self):
        """Shutdown monitoring thread"""
        self._stop_monitoring = True
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)


# Global instance
_traffic_optimizer: Optional[TrafficOptimizer] = None


def get_traffic_optimizer() -> TrafficOptimizer:
    """Get global traffic optimizer instance"""
    global _traffic_optimizer
    if _traffic_optimizer is None:
        _traffic_optimizer = TrafficOptimizer()
    return _traffic_optimizer