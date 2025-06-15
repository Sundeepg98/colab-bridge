"""
Sophisticated 3rd Party Integration Management System
Handles expensive APIs with learning, cost optimization, and auto-evolution
"""

import os
import json
import time
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from collections import defaultdict, deque
import pickle

logger = logging.getLogger(__name__)


class IntegrationType(Enum):
    """Types of 3rd party integrations"""
    LLM_API = "llm_api"
    IMAGE_API = "image_api"
    VIDEO_API = "video_api"
    ANALYTICS = "analytics"
    STORAGE = "storage"


class IntegrationStatus(Enum):
    """Integration health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded" 
    WARNING = "warning"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class IntegrationConfig:
    """Configuration for a 3rd party integration"""
    name: str
    type: IntegrationType
    api_key: str
    base_url: str
    models: List[str]
    cost_per_1k_tokens: Dict[str, float]  # input/output costs
    rate_limits: Dict[str, int]  # requests per minute/hour/day
    timeout_seconds: int = 30
    retry_attempts: int = 3
    health_check_interval: int = 300  # 5 minutes
    learning_enabled: bool = True
    auto_optimize: bool = True


@dataclass
class UsageMetrics:
    """Usage tracking for integrations"""
    requests_count: int = 0
    tokens_used: Dict[str, int] = None  # input/output
    cost_incurred: float = 0.0
    avg_response_time: float = 0.0
    error_count: int = 0
    success_rate: float = 100.0
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.tokens_used is None:
            self.tokens_used = {"input": 0, "output": 0}
        if self.last_updated is None:
            self.last_updated = datetime.now()


@dataclass
class LearningPattern:
    """Pattern learned from API interactions"""
    pattern_id: str
    prompt_type: str
    optimal_model: str
    optimal_params: Dict[str, Any]
    success_rate: float
    avg_cost: float
    avg_response_time: float
    usage_count: int
    learned_at: datetime
    confidence_score: float


class IntegrationLearningEngine:
    """Learns from API interactions to optimize usage"""
    
    def __init__(self, storage_path: str = "/var/projects/ai-integration-platform/learning_data"):
        self.storage_path = storage_path
        self.patterns: Dict[str, LearningPattern] = {}
        self.interaction_history = deque(maxlen=10000)  # Store last 10k interactions
        self.optimization_rules: Dict[str, Any] = {}
        self.load_learning_data()
        
    def record_interaction(self, integration_name: str, prompt: str, model: str, 
                          response_time: float, cost: float, success: bool, 
                          response_quality: float = None):
        """Record an API interaction for learning"""
        interaction = {
            'timestamp': datetime.now(),
            'integration': integration_name,
            'prompt': prompt[:100],  # Store first 100 chars for privacy
            'prompt_type': self._classify_prompt(prompt),
            'model': model,
            'response_time': response_time,
            'cost': cost,
            'success': success,
            'quality': response_quality or (0.8 if success else 0.2)
        }
        
        self.interaction_history.append(interaction)
        self._update_patterns(interaction)
        
        # Save learning data periodically
        if len(self.interaction_history) % 100 == 0:
            self.save_learning_data()
    
    def _classify_prompt(self, prompt: str) -> str:
        """Classify prompt type for pattern learning"""
        prompt_lower = prompt.lower()
        
        if len(prompt) < 50:
            return "simple"
        elif len(prompt) > 500:
            return "complex"
        elif any(word in prompt_lower for word in ["cinematic", "artistic", "creative"]):
            return "creative"
        elif any(word in prompt_lower for word in ["technical", "precise", "detailed"]):
            return "technical"
        else:
            return "general"
    
    def _update_patterns(self, interaction: Dict):
        """Update learning patterns based on interaction"""
        pattern_key = f"{interaction['prompt_type']}_{interaction['model']}"
        
        if pattern_key in self.patterns:
            pattern = self.patterns[pattern_key]
            # Update existing pattern
            pattern.usage_count += 1
            pattern.avg_cost = (pattern.avg_cost + interaction['cost']) / 2
            pattern.avg_response_time = (pattern.avg_response_time + interaction['response_time']) / 2
            pattern.success_rate = (pattern.success_rate + (100 if interaction['success'] else 0)) / 2
            pattern.confidence_score = min(1.0, pattern.usage_count / 100)  # Confidence grows with usage
        else:
            # Create new pattern
            pattern = LearningPattern(
                pattern_id=pattern_key,
                prompt_type=interaction['prompt_type'],
                optimal_model=interaction['model'],
                optimal_params={},
                success_rate=100 if interaction['success'] else 0,
                avg_cost=interaction['cost'],
                avg_response_time=interaction['response_time'],
                usage_count=1,
                learned_at=datetime.now(),
                confidence_score=0.01
            )
            self.patterns[pattern_key] = pattern
    
    def get_optimal_model(self, prompt: str, available_models: List[str]) -> Tuple[str, float]:
        """Get optimal model recommendation based on learned patterns"""
        prompt_type = self._classify_prompt(prompt)
        
        best_model = None
        best_score = 0.0
        
        for model in available_models:
            pattern_key = f"{prompt_type}_{model}"
            if pattern_key in self.patterns:
                pattern = self.patterns[pattern_key]
                # Score based on success rate, cost efficiency, and speed
                score = (
                    pattern.success_rate * 0.4 +
                    (1 / max(pattern.avg_cost, 0.001)) * 0.3 +
                    (1 / max(pattern.avg_response_time, 0.1)) * 0.2 +
                    pattern.confidence_score * 0.1
                )
                
                if score > best_score:
                    best_score = score
                    best_model = model
        
        # Fallback to fastest/cheapest if no patterns
        if not best_model and available_models:
            best_model = available_models[0]  # Assume first is default
            best_score = 0.5
            
        return best_model, best_score
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning system statistics"""
        return {
            'patterns_learned': len(self.patterns),
            'interactions_recorded': len(self.interaction_history),
            'avg_confidence': sum(p.confidence_score for p in self.patterns.values()) / max(len(self.patterns), 1),
            'most_used_pattern': max(self.patterns.values(), key=lambda p: p.usage_count).pattern_id if self.patterns else None,
            'learning_efficiency': self._calculate_learning_efficiency()
        }
    
    def _calculate_learning_efficiency(self) -> float:
        """Calculate how well the learning system is performing"""
        if len(self.interaction_history) < 10:
            return 0.0
            
        recent_interactions = list(self.interaction_history)[-100:]  # Last 100 interactions
        success_rate = sum(1 for i in recent_interactions if i['success']) / len(recent_interactions)
        avg_quality = sum(i['quality'] for i in recent_interactions) / len(recent_interactions)
        
        return (success_rate + avg_quality) / 2
    
    def save_learning_data(self):
        """Save learning data to disk"""
        try:
            os.makedirs(self.storage_path, exist_ok=True)
            
            # Save patterns
            patterns_file = os.path.join(self.storage_path, 'patterns.json')
            with open(patterns_file, 'w') as f:
                patterns_data = {k: asdict(v) for k, v in self.patterns.items()}
                # Convert datetime objects to strings
                for pattern_data in patterns_data.values():
                    pattern_data['learned_at'] = pattern_data['learned_at'].isoformat()
                json.dump(patterns_data, f, indent=2)
            
            # Save recent interactions (last 1000 for analysis)
            interactions_file = os.path.join(self.storage_path, 'interactions.pickle')
            recent_interactions = list(self.interaction_history)[-1000:]
            with open(interactions_file, 'wb') as f:
                pickle.dump(recent_interactions, f)
                
        except Exception as e:
            logger.error(f"Failed to save learning data: {e}")
    
    def load_learning_data(self):
        """Load learning data from disk"""
        try:
            # Load patterns
            patterns_file = os.path.join(self.storage_path, 'patterns.json')
            if os.path.exists(patterns_file):
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)
                    for k, v in patterns_data.items():
                        v['learned_at'] = datetime.fromisoformat(v['learned_at'])
                        self.patterns[k] = LearningPattern(**v)
            
            # Load interactions
            interactions_file = os.path.join(self.storage_path, 'interactions.pickle')
            if os.path.exists(interactions_file):
                with open(interactions_file, 'rb') as f:
                    interactions = pickle.load(f)
                    self.interaction_history.extend(interactions)
                    
        except Exception as e:
            logger.error(f"Failed to load learning data: {e}")


class IntegrationManager:
    """Manages all 3rd party integrations with sophisticated policies"""
    
    def __init__(self):
        self.integrations: Dict[str, IntegrationConfig] = {}
        self.usage_metrics: Dict[str, Dict[str, UsageMetrics]] = defaultdict(lambda: defaultdict(UsageMetrics))  # integration -> period -> metrics
        self.learning_engine = IntegrationLearningEngine()
        self.status_cache: Dict[str, Tuple[IntegrationStatus, datetime]] = {}
        self.cost_budgets: Dict[str, float] = {}  # daily budgets per integration
        self.circuit_breakers: Dict[str, bool] = {}  # emergency stops
        self.monitoring_thread = None
        self.running = False
        
        self._load_configurations()
        self._start_monitoring()
    
    def _load_configurations(self):
        """Load integration configurations"""
        # Claude/Anthropic
        if os.getenv('ANTHROPIC_API_KEY'):
            self.integrations['claude'] = IntegrationConfig(
                name='claude',
                type=IntegrationType.LLM_API,
                api_key=os.getenv('ANTHROPIC_API_KEY'),
                base_url='https://api.anthropic.com/v1',
                models=['claude-3-haiku-20240307', 'claude-3-5-sonnet-20241022', 'claude-3-opus-20240229'],
                cost_per_1k_tokens={
                    'claude-3-haiku-20240307': {'input': 0.00025, 'output': 0.00125},
                    'claude-3-5-sonnet-20241022': {'input': 0.003, 'output': 0.015},
                    'claude-3-opus-20240229': {'input': 0.015, 'output': 0.075}
                },
                rate_limits={'per_minute': 60, 'per_hour': 1000, 'per_day': 10000},
                timeout_seconds=30,
                learning_enabled=True,
                auto_optimize=True
            )
            self.cost_budgets['claude'] = 50.0  # $50/day budget
        
        # OpenAI (if configured)
        if os.getenv('OPENAI_API_KEY'):
            self.integrations['openai'] = IntegrationConfig(
                name='openai',
                type=IntegrationType.LLM_API,
                api_key=os.getenv('OPENAI_API_KEY'),
                base_url='https://api.openai.com/v1',
                models=['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo'],
                cost_per_1k_tokens={
                    'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},
                    'gpt-4': {'input': 0.03, 'output': 0.06},
                    'gpt-4-turbo': {'input': 0.01, 'output': 0.03}
                },
                rate_limits={'per_minute': 90, 'per_hour': 3000, 'per_day': 20000},
                timeout_seconds=25,
                learning_enabled=True,
                auto_optimize=True
            )
            self.cost_budgets['openai'] = 30.0  # $30/day budget
        
        # Stable Diffusion (if configured)
        if os.getenv('STABILITY_API_KEY'):
            self.integrations['stable_diffusion'] = IntegrationConfig(
                name='stable_diffusion',
                type=IntegrationType.IMAGE_API,
                api_key=os.getenv('STABILITY_API_KEY'),
                base_url='https://api.stability.ai/v1',
                models=['stable-diffusion-xl-base-1.0', 'stable-diffusion-v1-5', 'stable-diffusion-2-1', 'sdxl-turbo', 'stable-diffusion-3'],
                cost_per_1k_tokens={
                    'stable-diffusion-xl-base-1.0': {'input': 0.008, 'output': 0.008},
                    'stable-diffusion-v1-5': {'input': 0.002, 'output': 0.002},
                    'stable-diffusion-2-1': {'input': 0.003, 'output': 0.003},
                    'sdxl-turbo': {'input': 0.005, 'output': 0.005},
                    'stable-diffusion-3': {'input': 0.015, 'output': 0.015}
                },
                rate_limits={'per_minute': 150, 'per_hour': 5000, 'per_day': 10000},
                timeout_seconds=20,
                learning_enabled=True,
                auto_optimize=True
            )
            self.cost_budgets['stable_diffusion'] = 40.0  # $40/day budget
    
    def get_optimal_integration(self, task_type: str, prompt: str, 
                              quality_requirement: float = 0.7) -> Tuple[str, str, Dict]:
        """Get optimal integration and model for a task using learning"""
        available_integrations = []
        
        for name, config in self.integrations.items():
            if self._is_integration_available(name) and config.type == IntegrationType.LLM_API:
                # Get optimal model from learning engine
                optimal_model, confidence = self.learning_engine.get_optimal_model(
                    prompt, config.models
                )
                
                # Check budget
                daily_cost = self._get_daily_cost(name)
                if daily_cost < self.cost_budgets.get(name, 100.0) * 0.8:  # Stay under 80% of budget
                    available_integrations.append({
                        'name': name,
                        'model': optimal_model,
                        'confidence': confidence,
                        'cost_efficiency': self._calculate_cost_efficiency(name, optimal_model),
                        'quality_score': self._estimate_quality_score(name, optimal_model, task_type)
                    })
        
        if not available_integrations:
            return None, None, {"error": "No available integrations"}
        
        # Score integrations based on quality requirement
        best_integration = None
        best_score = 0
        
        for integration in available_integrations:
            score = (
                integration['quality_score'] * (0.6 if quality_requirement > 0.8 else 0.4) +
                integration['cost_efficiency'] * 0.3 +
                integration['confidence'] * 0.1
            )
            
            if score > best_score:
                best_score = score
                best_integration = integration
        
        return best_integration['name'], best_integration['model'], {
            'reasoning': f"Selected based on quality requirement {quality_requirement}",
            'confidence': best_integration['confidence'],
            'estimated_cost': self._estimate_cost(best_integration['name'], best_integration['model'], prompt)
        }
    
    def record_usage(self, integration_name: str, model: str, input_tokens: int, 
                    output_tokens: int, response_time: float, success: bool,
                    cost: float = None):
        """Record usage for learning and monitoring"""
        today = datetime.now().strftime('%Y-%m-%d')
        metrics = self.usage_metrics[integration_name][today]
        
        metrics.requests_count += 1
        metrics.tokens_used['input'] += input_tokens
        metrics.tokens_used['output'] += output_tokens
        
        # Calculate cost if not provided
        if cost is None and integration_name in self.integrations:
            config = self.integrations[integration_name]
            if model in config.cost_per_1k_tokens:
                costs = config.cost_per_1k_tokens[model]
                cost = (input_tokens * costs['input'] + output_tokens * costs['output']) / 1000
        
        if cost:
            metrics.cost_incurred += cost
        
        # Update response time (moving average)
        if metrics.avg_response_time == 0:
            metrics.avg_response_time = response_time
        else:
            metrics.avg_response_time = (metrics.avg_response_time + response_time) / 2
        
        if not success:
            metrics.error_count += 1
        
        metrics.success_rate = ((metrics.requests_count - metrics.error_count) / metrics.requests_count) * 100
        metrics.last_updated = datetime.now()
        
        # Record for learning
        if self.integrations[integration_name].learning_enabled:
            # We'd need the original prompt here - this is a simplified version
            self.learning_engine.record_interaction(
                integration_name, "", model, response_time, cost or 0, success
            )
    
    def update_integration_status(self, integration_name: str, status: str):
        """Update the status of an integration"""
        try:
            status_enum = IntegrationStatus[status.upper()]
            self.status_cache[integration_name] = (status_enum, datetime.now())
            logger.info(f"Updated {integration_name} status to {status}")
        except Exception as e:
            logger.error(f"Failed to update integration status: {e}")
    
    def get_integration_status(self, integration_name: str) -> IntegrationStatus:
        """Get current status of an integration"""
        if integration_name not in self.integrations:
            return IntegrationStatus.ERROR
            
        # Check circuit breaker
        if self.circuit_breakers.get(integration_name, False):
            return IntegrationStatus.DISABLED
        
        # Check cache first
        if integration_name in self.status_cache:
            status, timestamp = self.status_cache[integration_name]
            if datetime.now() - timestamp < timedelta(minutes=5):  # 5 minute cache
                return status
        
        # Check actual health
        status = self._check_integration_health(integration_name)
        self.status_cache[integration_name] = (status, datetime.now())
        
        return status
    
    def _check_integration_health(self, integration_name: str) -> IntegrationStatus:
        """Check actual health of integration"""
        config = self.integrations[integration_name]
        today = datetime.now().strftime('%Y-%m-%d')
        metrics = self.usage_metrics[integration_name][today]
        
        # Check error rate
        if metrics.requests_count > 10 and metrics.success_rate < 80:
            return IntegrationStatus.ERROR
        elif metrics.requests_count > 10 and metrics.success_rate < 95:
            return IntegrationStatus.WARNING
        
        # Check response time
        if metrics.avg_response_time > config.timeout_seconds * 0.8:
            return IntegrationStatus.DEGRADED
        
        # Check budget
        daily_cost = metrics.cost_incurred
        budget = self.cost_budgets.get(integration_name, 100.0)
        
        if daily_cost > budget:
            return IntegrationStatus.ERROR
        elif daily_cost > budget * 0.9:
            return IntegrationStatus.WARNING
        
        return IntegrationStatus.HEALTHY
    
    def _is_integration_available(self, integration_name: str) -> bool:
        """Check if integration is available for use"""
        status = self.get_integration_status(integration_name)
        return status in [IntegrationStatus.HEALTHY, IntegrationStatus.DEGRADED, IntegrationStatus.WARNING]
    
    def _get_daily_cost(self, integration_name: str) -> float:
        """Get today's cost for an integration"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.usage_metrics[integration_name][today].cost_incurred
    
    def _calculate_cost_efficiency(self, integration_name: str, model: str) -> float:
        """Calculate cost efficiency score (higher is better)"""
        if integration_name not in self.integrations:
            return 0.0
        
        config = self.integrations[integration_name]
        if model not in config.cost_per_1k_tokens:
            return 0.0
        
        costs = config.cost_per_1k_tokens[model]
        avg_cost = (costs['input'] + costs['output']) / 2
        
        # Efficiency is inverse of cost (normalized)
        max_cost = 0.1  # Assume $0.1 per 1k tokens is expensive
        return max(0, (max_cost - avg_cost) / max_cost)
    
    def _estimate_quality_score(self, integration_name: str, model: str, task_type: str) -> float:
        """Estimate quality score for integration/model combination"""
        # This would be based on learned patterns and benchmarks
        # For now, using simple heuristics
        
        quality_map = {
            'claude': {
                'claude-3-opus-20240229': 0.95,
                'claude-3-5-sonnet-20241022': 0.90,
                'claude-3-haiku-20240307': 0.75
            },
            'openai': {
                'gpt-4': 0.92,
                'gpt-4-turbo': 0.90,
                'gpt-3.5-turbo': 0.78
            }
        }
        
        return quality_map.get(integration_name, {}).get(model, 0.7)
    
    def _estimate_cost(self, integration_name: str, model: str, prompt: str) -> float:
        """Estimate cost for a request"""
        if integration_name not in self.integrations:
            return 0.0
        
        config = self.integrations[integration_name]
        if model not in config.cost_per_1k_tokens:
            return 0.0
        
        # Rough token estimation
        input_tokens = len(prompt.split()) * 1.3  # Average 1.3 tokens per word
        output_tokens = input_tokens * 0.5  # Assume response is 50% of input
        
        costs = config.cost_per_1k_tokens[model]
        return (input_tokens * costs['input'] + output_tokens * costs['output']) / 1000
    
    def _start_monitoring(self):
        """Start background monitoring thread"""
        self.running = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
    
    def _monitoring_loop(self):
        """Background monitoring and optimization"""
        while self.running:
            try:
                # Check integration health
                for integration_name in self.integrations:
                    status = self._check_integration_health(integration_name)
                    
                    # Auto-disable if too many errors
                    if status == IntegrationStatus.ERROR:
                        today_metrics = self.usage_metrics[integration_name][datetime.now().strftime('%Y-%m-%d')]
                        if today_metrics.requests_count > 20 and today_metrics.success_rate < 70:
                            self.circuit_breakers[integration_name] = True
                            logger.warning(f"Circuit breaker activated for {integration_name}")
                
                # Save learning data
                self.learning_engine.save_learning_data()
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(60)
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive data for admin dashboard"""
        dashboard_data = {
            'integrations': {},
            'total_cost_today': 0.0,
            'total_requests_today': 0,
            'learning_stats': self.learning_engine.get_learning_stats(),
            'circuit_breakers': self.circuit_breakers.copy()
        }
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        for name, config in self.integrations.items():
            metrics = self.usage_metrics[name][today]
            status = self.get_integration_status(name)
            
            # Convert config to dict with serializable values
            config_dict = asdict(config)
            config_dict['type'] = config.type.value  # Convert enum to string
            
            # Convert metrics to dict with serializable values
            metrics_dict = asdict(metrics)
            if metrics_dict['last_updated']:
                metrics_dict['last_updated'] = metrics_dict['last_updated'].isoformat()
            
            dashboard_data['integrations'][name] = {
                'config': config_dict,
                'status': status.value,
                'metrics': metrics_dict,
                'budget_usage': metrics.cost_incurred / self.cost_budgets.get(name, 100.0),
                'available_models': len(config.models),
                'optimal_model': self.learning_engine.get_optimal_model("test", config.models)[0]
            }
            
            dashboard_data['total_cost_today'] += metrics.cost_incurred
            dashboard_data['total_requests_today'] += metrics.requests_count
        
        return dashboard_data
    
    def stop(self):
        """Stop the integration manager"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)


# Global instance
_integration_manager: Optional[IntegrationManager] = None


def get_integration_manager() -> IntegrationManager:
    """Get global integration manager instance"""
    global _integration_manager
    if _integration_manager is None:
        _integration_manager = IntegrationManager()
    return _integration_manager