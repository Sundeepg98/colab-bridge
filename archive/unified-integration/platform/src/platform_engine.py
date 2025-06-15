"""
Platform Engine - Core routing and execution engine
Demonstrates smooth, independent operation regardless of external service status
"""

import asyncio
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RequestType(Enum):
    """Types of requests the platform handles"""
    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    VIDEO_GENERATION = "video_generation"
    AUDIO_GENERATION = "audio_generation"
    CODE_GENERATION = "code_generation"


@dataclass
class ServiceHealth:
    """Real-time health status of a service"""
    name: str
    is_healthy: bool
    response_time_ms: Optional[float]
    success_rate: float
    last_checked: datetime
    error_count: int = 0
    circuit_breaker_open: bool = False


@dataclass
class PlatformRequest:
    """User request to the platform"""
    user_id: str
    request_type: RequestType
    prompt: str
    parameters: Dict[str, Any]
    preferred_service: Optional[str] = None
    max_cost: Optional[float] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class PlatformResponse:
    """Response from the platform"""
    request_id: str
    success: bool
    service_used: Optional[str]
    result: Optional[Any]
    cost: float
    processing_time_ms: float
    fallback_used: bool = False
    error_message: Optional[str] = None


class PlatformEngine:
    """
    Core engine that handles all requests independently of external services
    Demonstrates resilience, routing, and fallback capabilities
    """
    
    def __init__(self):
        self.services = self._initialize_services()
        self.service_health: Dict[str, ServiceHealth] = {}
        self.request_queue: asyncio.Queue = asyncio.Queue()
        self.processing = True
        self.fallback_chain = self._build_fallback_chains()
        self.circuit_breaker_threshold = 5  # failures before opening circuit
        self.circuit_breaker_timeout = 60  # seconds before retry
        
        # Initialize health status
        self._initialize_health_monitoring()
        
    def _initialize_services(self) -> Dict[str, Dict[str, Any]]:
        """Initialize available services with their capabilities"""
        return {
            # Chatbots
            'openai': {
                'type': 'chatbot',
                'capabilities': [RequestType.TEXT_GENERATION, RequestType.CODE_GENERATION],
                'cost_per_1k_tokens': 0.03,
                'max_tokens': 4096,
                'priority': 1
            },
            'claude': {
                'type': 'chatbot',
                'capabilities': [RequestType.TEXT_GENERATION, RequestType.CODE_GENERATION],
                'cost_per_1k_tokens': 0.025,
                'max_tokens': 100000,
                'priority': 2
            },
            'cohere': {
                'type': 'chatbot',
                'capabilities': [RequestType.TEXT_GENERATION],
                'cost_per_1k_tokens': 0.015,
                'max_tokens': 2048,
                'priority': 3
            },
            
            # Image Simulators
            'stable_diffusion': {
                'type': 'simulator',
                'capabilities': [RequestType.IMAGE_GENERATION],
                'cost_per_image': 0.08,
                'priority': 1
            },
            'dalle': {
                'type': 'simulator',
                'capabilities': [RequestType.IMAGE_GENERATION],
                'cost_per_image': 0.04,
                'priority': 2
            },
            'midjourney': {
                'type': 'simulator',
                'capabilities': [RequestType.IMAGE_GENERATION],
                'cost_per_image': 0.10,
                'priority': 3
            },
            
            # Video Simulators
            'runway': {
                'type': 'simulator',
                'capabilities': [RequestType.VIDEO_GENERATION],
                'cost_per_second': 0.10,
                'priority': 1
            },
            
            # Local/Mock services (always available)
            'local_text': {
                'type': 'local',
                'capabilities': [RequestType.TEXT_GENERATION, RequestType.CODE_GENERATION],
                'cost_per_1k_tokens': 0,
                'priority': 99  # Last resort
            },
            'local_image': {
                'type': 'local',
                'capabilities': [RequestType.IMAGE_GENERATION],
                'cost_per_image': 0,
                'priority': 99
            }
        }
    
    def _initialize_health_monitoring(self):
        """Initialize health status for all services"""
        for service_name in self.services:
            self.service_health[service_name] = ServiceHealth(
                name=service_name,
                is_healthy=True,
                response_time_ms=random.uniform(50, 200),
                success_rate=0.99,
                last_checked=datetime.now()
            )
    
    def _build_fallback_chains(self) -> Dict[RequestType, List[str]]:
        """Build fallback chains for each request type"""
        chains = {}
        
        for request_type in RequestType:
            # Get all services that support this request type
            capable_services = [
                (name, config['priority']) 
                for name, config in self.services.items()
                if request_type in config['capabilities']
            ]
            
            # Sort by priority (lower number = higher priority)
            capable_services.sort(key=lambda x: x[1])
            
            # Extract just the service names
            chains[request_type] = [name for name, _ in capable_services]
        
        return chains
    
    async def process_request(self, request: PlatformRequest) -> PlatformResponse:
        """
        Process a user request with intelligent routing and fallback
        This is the main demonstration of platform independence
        """
        start_time = time.time()
        request_id = f"{request.user_id}_{int(start_time * 1000)}"
        
        # Get fallback chain for this request type
        service_chain = self.fallback_chain.get(request.request_type, [])
        
        if not service_chain:
            return PlatformResponse(
                request_id=request_id,
                success=False,
                service_used=None,
                result=None,
                cost=0,
                processing_time_ms=0,
                error_message=f"No services available for {request.request_type.value}"
            )
        
        # Try each service in the fallback chain
        last_error = None
        for service_name in service_chain:
            # Skip if user has preference and this isn't it (unless all preferred failed)
            if request.preferred_service and service_name != request.preferred_service:
                if service_chain.index(service_name) < len(service_chain) - 1:
                    continue
            
            # Check service health
            health = self.service_health.get(service_name)
            if not health or not health.is_healthy or health.circuit_breaker_open:
                logger.info(f"Skipping unhealthy service: {service_name}")
                continue
            
            # Check cost constraints
            estimated_cost = self._estimate_cost(service_name, request)
            if request.max_cost and estimated_cost > request.max_cost:
                logger.info(f"Skipping {service_name} due to cost constraint")
                continue
            
            # Try to process with this service
            try:
                result = await self._execute_with_service(service_name, request)
                
                # Update health metrics
                self._update_service_health(service_name, success=True, 
                                          response_time=(time.time() - start_time) * 1000)
                
                return PlatformResponse(
                    request_id=request_id,
                    success=True,
                    service_used=service_name,
                    result=result,
                    cost=estimated_cost,
                    processing_time_ms=(time.time() - start_time) * 1000,
                    fallback_used=(service_name != service_chain[0])
                )
                
            except Exception as e:
                logger.error(f"Service {service_name} failed: {str(e)}")
                last_error = str(e)
                
                # Update health metrics
                self._update_service_health(service_name, success=False)
                
                # Continue to next service in chain
                continue
        
        # All services failed - use local fallback
        logger.warning("All external services failed, using local fallback")
        
        # Find appropriate local service
        local_service = next(
            (name for name in service_chain if self.services[name]['type'] == 'local'),
            None
        )
        
        if local_service:
            try:
                result = await self._execute_with_service(local_service, request)
                return PlatformResponse(
                    request_id=request_id,
                    success=True,
                    service_used=local_service,
                    result=result,
                    cost=0,
                    processing_time_ms=(time.time() - start_time) * 1000,
                    fallback_used=True
                )
            except Exception as e:
                logger.error(f"Even local fallback failed: {str(e)}")
        
        # Complete failure
        return PlatformResponse(
            request_id=request_id,
            success=False,
            service_used=None,
            result=None,
            cost=0,
            processing_time_ms=(time.time() - start_time) * 1000,
            error_message=last_error or "All services unavailable"
        )
    
    async def _execute_with_service(self, service_name: str, 
                                   request: PlatformRequest) -> Any:
        """Execute request with specific service"""
        service_config = self.services[service_name]
        
        # Simulate service execution
        if service_config['type'] == 'local':
            # Local services always work
            return await self._execute_local_service(service_name, request)
        else:
            # External services might fail
            return await self._execute_external_service(service_name, request)
    
    async def _execute_local_service(self, service_name: str, 
                                   request: PlatformRequest) -> Any:
        """Execute with local/mock service - always works"""
        await asyncio.sleep(0.1)  # Simulate processing
        
        if request.request_type == RequestType.TEXT_GENERATION:
            return {
                'text': f"[Local Generated] Response to: {request.prompt[:50]}...",
                'tokens': 100,
                'model': 'local-gpt'
            }
        elif request.request_type == RequestType.IMAGE_GENERATION:
            return {
                'image_url': 'data:image/png;base64,placeholder',
                'size': '512x512',
                'model': 'local-diffusion'
            }
        else:
            return {'result': 'Local processing completed'}
    
    async def _execute_external_service(self, service_name: str, 
                                      request: PlatformRequest) -> Any:
        """Simulate external service execution"""
        # Simulate network delay
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Simulate occasional failures
        if random.random() < 0.1:  # 10% failure rate for demo
            raise Exception(f"{service_name} temporarily unavailable")
        
        # Simulate rate limiting
        if random.random() < 0.05:  # 5% rate limit
            raise Exception(f"{service_name} rate limit exceeded")
        
        # Return simulated success response
        if request.request_type == RequestType.TEXT_GENERATION:
            return {
                'text': f"[{service_name}] Generated response for: {request.prompt[:50]}...",
                'tokens': random.randint(50, 500),
                'model': f'{service_name}-model'
            }
        elif request.request_type == RequestType.IMAGE_GENERATION:
            return {
                'image_url': f'https://example.com/{service_name}/image.png',
                'size': '1024x1024',
                'model': service_name
            }
        else:
            return {'result': f'{service_name} processing completed'}
    
    def _estimate_cost(self, service_name: str, request: PlatformRequest) -> float:
        """Estimate cost for a request"""
        service_config = self.services[service_name]
        
        if request.request_type in [RequestType.TEXT_GENERATION, RequestType.CODE_GENERATION]:
            # Estimate tokens (rough: 1 token ≈ 4 characters)
            estimated_tokens = len(request.prompt) / 4 + 200  # prompt + response
            return (estimated_tokens / 1000) * service_config.get('cost_per_1k_tokens', 0)
        
        elif request.request_type == RequestType.IMAGE_GENERATION:
            return service_config.get('cost_per_image', 0)
        
        elif request.request_type == RequestType.VIDEO_GENERATION:
            duration = request.parameters.get('duration_seconds', 5)
            return duration * service_config.get('cost_per_second', 0)
        
        return 0
    
    def _update_service_health(self, service_name: str, success: bool, 
                             response_time: Optional[float] = None):
        """Update service health metrics"""
        health = self.service_health.get(service_name)
        if not health:
            return
        
        health.last_checked = datetime.now()
        
        if success:
            health.error_count = 0
            health.success_rate = min(0.99, health.success_rate * 1.01)  # Slowly improve
            
            if response_time:
                # Moving average of response time
                health.response_time_ms = (health.response_time_ms * 0.9 + response_time * 0.1)
            
            # Close circuit breaker if it was open
            if health.circuit_breaker_open:
                logger.info(f"Closing circuit breaker for {service_name}")
                health.circuit_breaker_open = False
                
        else:
            health.error_count += 1
            health.success_rate = max(0.5, health.success_rate * 0.95)  # Degrade faster
            
            # Open circuit breaker if too many failures
            if health.error_count >= self.circuit_breaker_threshold:
                logger.warning(f"Opening circuit breaker for {service_name}")
                health.circuit_breaker_open = True
                health.is_healthy = False
                
                # Schedule circuit breaker reset
                asyncio.create_task(self._reset_circuit_breaker(service_name))
    
    async def _reset_circuit_breaker(self, service_name: str):
        """Reset circuit breaker after timeout"""
        await asyncio.sleep(self.circuit_breaker_timeout)
        
        health = self.service_health.get(service_name)
        if health and health.circuit_breaker_open:
            logger.info(f"Resetting circuit breaker for {service_name}")
            health.circuit_breaker_open = False
            health.is_healthy = True
            health.error_count = 0
    
    def route_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route request to appropriate service - compatibility method"""
        request = PlatformRequest(
            user_id=request_data.get('user_id', 'anonymous'),
            request_type=RequestType(request_data.get('type', 'text_generation')),
            prompt=request_data.get('prompt', ''),
            parameters=request_data.get('parameters', {}),
            preferred_service=request_data.get('preferred_service'),
            max_cost=request_data.get('max_cost')
        )
        
        # Run async method in sync context
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(self.process_request(request))
            return {
                'success': response.success,
                'service_used': response.service_used,
                'result': response.result,
                'cost': response.cost,
                'processing_time_ms': response.processing_time_ms,
                'error': response.error_message
            }
        finally:
            loop.close()
    
    def get_platform_status(self) -> Dict[str, Any]:
        """Get current platform status"""
        healthy_services = sum(1 for h in self.service_health.values() if h.is_healthy)
        total_services = len(self.service_health)
        
        return {
            'platform_health': 'operational' if healthy_services > 0 else 'degraded',
            'healthy_services': healthy_services,
            'total_services': total_services,
            'service_status': {
                name: {
                    'healthy': health.is_healthy,
                    'response_time_ms': health.response_time_ms,
                    'success_rate': health.success_rate,
                    'circuit_breaker': 'open' if health.circuit_breaker_open else 'closed'
                }
                for name, health in self.service_health.items()
            },
            'fallback_available': True,  # Always true due to local services
            'timestamp': datetime.now().isoformat()
        }


# Global engine instance
_engine: Optional[PlatformEngine] = None


def get_platform_engine() -> PlatformEngine:
    """Get global platform engine instance"""
    global _engine
    if _engine is None:
        _engine = PlatformEngine()
    return _engine


# Example usage demonstrating platform resilience
async def demonstrate_platform_resilience():
    """Demonstrate how the platform handles various scenarios"""
    engine = get_platform_engine()
    
    # Test scenarios
    scenarios = [
        # Normal request
        PlatformRequest(
            user_id="user1",
            request_type=RequestType.TEXT_GENERATION,
            prompt="Explain quantum computing",
            parameters={}
        ),
        
        # Image generation with cost constraint
        PlatformRequest(
            user_id="user2",
            request_type=RequestType.IMAGE_GENERATION,
            prompt="A futuristic city at sunset",
            parameters={'size': '1024x1024'},
            max_cost=0.05
        ),
        
        # Request with service preference
        PlatformRequest(
            user_id="user3",
            request_type=RequestType.TEXT_GENERATION,
            prompt="Write a Python function",
            parameters={},
            preferred_service='claude'
        )
    ]
    
    print("\n=== Platform Resilience Demonstration ===\n")
    
    for i, request in enumerate(scenarios, 1):
        print(f"Scenario {i}: {request.request_type.value}")
        print(f"Prompt: {request.prompt}")
        
        response = await engine.process_request(request)
        
        print(f"Success: {response.success}")
        print(f"Service Used: {response.service_used}")
        print(f"Cost: ${response.cost:.4f}")
        print(f"Processing Time: {response.processing_time_ms:.0f}ms")
        print(f"Fallback Used: {response.fallback_used}")
        
        if response.error_message:
            print(f"Error: {response.error_message}")
        
        print("-" * 50)
    
    # Show platform status
    status = engine.get_platform_status()
    print("\nPlatform Status:")
    print(f"Health: {status['platform_health']}")
    print(f"Healthy Services: {status['healthy_services']}/{status['total_services']}")
    print(f"Fallback Available: {status['fallback_available']}")


if __name__ == "__main__":
    # Run demonstration
    asyncio.run(demonstrate_platform_resilience())