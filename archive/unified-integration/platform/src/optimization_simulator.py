"""
Optimization Simulator

A comprehensive simulation system that tests optimization strategies
before deploying them in production. This helps validate:
1. Performance under different traffic conditions
2. Cost efficiency under various budgets
3. Quality consistency across user segments
4. Legal compliance in edge cases
"""

import json
import time
import random
import statistics
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)


class SimulationScenario(Enum):
    """Different simulation scenarios"""
    LOW_TRAFFIC = "low_traffic"
    MODERATE_TRAFFIC = "moderate_traffic"
    HIGH_TRAFFIC = "high_traffic"
    PEAK_LOAD = "peak_load"
    BUDGET_CONSTRAINED = "budget_constrained"
    MIXED_USER_SEGMENTS = "mixed_user_segments"
    LEGAL_EDGE_CASES = "legal_edge_cases"
    SYSTEM_STRESS = "system_stress"


@dataclass
class SimulationRequest:
    """A simulated user request"""
    user_segment: str
    prompt: str
    complexity: str
    expected_quality: float
    budget_remaining: float
    timestamp: datetime
    user_tier: str = "basic"
    force_quality: bool = False


@dataclass
class SimulationResult:
    """Result of a single simulation request"""
    request: SimulationRequest
    model_selected: str
    actual_cost: float
    quality_score: float
    response_time: float
    legal_compliant: bool
    success: bool
    error_message: Optional[str] = None


@dataclass
class SimulationReport:
    """Comprehensive simulation report"""
    scenario: SimulationScenario
    total_requests: int
    successful_requests: int
    failed_requests: int
    
    # Performance metrics
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    
    # Cost metrics
    total_cost: float
    avg_cost_per_request: float
    budget_efficiency: float
    
    # Quality metrics
    avg_quality_score: float
    quality_consistency: float
    user_satisfaction: float
    
    # Compliance metrics
    legal_compliance_rate: float
    blocked_requests: int
    
    # Model usage distribution
    model_usage: Dict[str, int]
    
    # Recommendations
    optimization_recommendations: List[str]
    performance_insights: List[str]
    cost_optimization_tips: List[str]


class OptimizationSimulator:
    """Simulates optimization scenarios to test system performance"""
    
    def __init__(self):
        self.test_prompts = {
            "simple": [
                "A sunset over mountains",
                "Person walking in park",
                "Cat sleeping on sofa",
                "Rain falling on window"
            ],
            "moderate": [
                "Two friends having emotional conversation in cozy cafe during golden hour",
                "Professional dancer performing contemporary piece in minimalist studio",
                "Family gathering around dinner table with warm candlelight",
                "Artist creating mural on urban wall with passing pedestrians"
            ],
            "complex": [
                "Cinematic sequence of elderly musician teaching young student classical violin technique in ornate conservatory with dramatic lighting and emotional depth",
                "Documentary-style footage of marine biologist conducting research underwater with sophisticated equipment and natural marine life interactions",
                "Multi-generational family reunion with complex emotional dynamics captured through intimate close-ups and wide establishing shots"
            ]
        }
        
        self.user_segments = ["casual_user", "creative_professional", "content_creator", "power_user"]
        self.user_tiers = ["basic", "premium", "professional"]
        
    def run_simulation(self, scenario: SimulationScenario, duration_minutes: int = 10, 
                      requests_per_minute: int = 6) -> SimulationReport:
        """Run a complete simulation scenario"""
        logger.info(f"Starting simulation: {scenario.value} for {duration_minutes} minutes")
        
        # Generate simulation requests
        requests = self._generate_requests(scenario, duration_minutes, requests_per_minute)
        
        # Execute simulation
        results = self._execute_simulation(requests, scenario)
        
        # Generate report
        report = self._generate_report(scenario, requests, results)
        
        logger.info(f"Simulation completed: {len(results)} requests processed")
        return report
    
    def _generate_requests(self, scenario: SimulationScenario, 
                          duration_minutes: int, requests_per_minute: int) -> List[SimulationRequest]:
        """Generate simulation requests based on scenario"""
        requests = []
        total_requests = duration_minutes * requests_per_minute
        
        for i in range(total_requests):
            # Time distribution
            timestamp = datetime.now() + timedelta(seconds=i * (60 / requests_per_minute))
            
            # Scenario-specific parameters
            if scenario == SimulationScenario.LOW_TRAFFIC:
                complexity = random.choice(["simple", "simple", "moderate"])
                user_segment = random.choice(["casual_user", "casual_user", "creative_professional"])
                budget_remaining = random.uniform(8.0, 10.0)
                
            elif scenario == SimulationScenario.HIGH_TRAFFIC:
                complexity = random.choice(["simple", "moderate", "moderate", "complex"])
                user_segment = random.choice(self.user_segments)
                budget_remaining = random.uniform(2.0, 8.0)
                
            elif scenario == SimulationScenario.PEAK_LOAD:
                complexity = random.choice(["moderate", "complex", "complex"])
                user_segment = random.choice(["creative_professional", "power_user", "content_creator"])
                budget_remaining = random.uniform(1.0, 5.0)
                
            elif scenario == SimulationScenario.BUDGET_CONSTRAINED:
                complexity = random.choice(["simple", "moderate", "complex"])
                user_segment = random.choice(self.user_segments)
                budget_remaining = random.uniform(0.5, 2.0)  # Very low budget
                
            elif scenario == SimulationScenario.MIXED_USER_SEGMENTS:
                complexity = random.choice(["simple", "moderate", "complex"])
                user_segment = random.choice(self.user_segments)
                budget_remaining = random.uniform(3.0, 10.0)
                
            elif scenario == SimulationScenario.LEGAL_EDGE_CASES:
                # Include some potentially problematic prompts
                complexity = "moderate"
                user_segment = random.choice(self.user_segments)
                budget_remaining = random.uniform(5.0, 10.0)
                
            else:  # SYSTEM_STRESS
                complexity = random.choice(["complex", "complex", "complex"])
                user_segment = "power_user"
                budget_remaining = random.uniform(0.1, 1.0)
            
            # Select prompt
            prompt = random.choice(self.test_prompts[complexity])
            
            # Add edge case prompts for legal testing
            if scenario == SimulationScenario.LEGAL_EDGE_CASES and random.random() < 0.3:
                edge_prompts = [
                    "19 year old and 85 year old discussing philosophy",
                    "Adult couple in romantic setting",
                    "Professional business meeting",
                    "Family celebration with multiple generations"
                ]
                prompt = random.choice(edge_prompts)
            
            # Create request
            request = SimulationRequest(
                user_segment=user_segment,
                prompt=prompt,
                complexity=complexity,
                expected_quality=random.uniform(0.7, 0.95),
                budget_remaining=budget_remaining,
                timestamp=timestamp,
                user_tier=random.choice(self.user_tiers) if scenario == SimulationScenario.MIXED_USER_SEGMENTS else "basic",
                force_quality=random.random() < 0.1  # 10% force quality
            )
            
            requests.append(request)
        
        return requests
    
    def _execute_simulation(self, requests: List[SimulationRequest], 
                           scenario: SimulationScenario) -> List[SimulationResult]:
        """Execute simulation requests concurrently"""
        results = []
        
        # Import required modules
        try:
            from src.smart_claude_selector import get_model_selector
            from src.enhanced_legal_validator import EnhancedLegalValidator
            
            selector = get_model_selector()
            validator = EnhancedLegalValidator()
        except Exception as e:
            logger.error(f"Failed to initialize simulation components: {e}")
            return []
        
        # Execute requests with threading for realistic load
        max_workers = 5 if scenario == SimulationScenario.PEAK_LOAD else 3
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all requests
            future_to_request = {
                executor.submit(self._simulate_single_request, request, selector, validator): request
                for request in requests
            }
            
            # Collect results
            for future in as_completed(future_to_request):
                request = future_to_request[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    # Create failed result
                    failed_result = SimulationResult(
                        request=request,
                        model_selected="error",
                        actual_cost=0.0,
                        quality_score=0.0,
                        response_time=999.0,
                        legal_compliant=False,
                        success=False,
                        error_message=str(e)
                    )
                    results.append(failed_result)
        
        return results
    
    def _simulate_single_request(self, request: SimulationRequest, 
                                selector, validator) -> SimulationResult:
        """Simulate a single optimization request"""
        start_time = time.time()
        
        try:
            # Legal validation
            validation_result = validator.validate_request(request.prompt, {
                'user_id': 'test_user', 
                'ip': '127.0.0.1', 
                'timestamp': request.timestamp
            })
            legal_compliant = validation_result['allowed']
            
            if not legal_compliant:
                return SimulationResult(
                    request=request,
                    model_selected="blocked",
                    actual_cost=0.0,
                    quality_score=0.0,
                    response_time=time.time() - start_time,
                    legal_compliant=False,
                    success=False,
                    error_message="Content blocked for legal compliance"
                )
            
            # Model selection
            selection = selector.select_model(
                prompt=request.prompt,
                user_segment=request.user_segment,
                user_tier=request.user_tier,
                quality_required=request.expected_quality,
                budget_remaining=request.budget_remaining,
                force_quality=request.force_quality
            )
            
            # Simulate processing time based on model
            if "haiku" in selection['model'].lower():
                processing_time = random.uniform(0.5, 1.5)
            elif "sonnet" in selection['model'].lower():
                processing_time = random.uniform(1.0, 3.0)
            else:  # opus
                processing_time = random.uniform(2.0, 5.0)
            
            time.sleep(processing_time * 0.1)  # Scale down for simulation
            
            # Calculate metrics
            response_time = time.time() - start_time
            actual_cost = selection.get('estimated_cost', 0.001)
            
            # Quality score based on model and complexity
            base_quality = selection.get('quality_expected', 0.8)
            complexity_factor = {
                "simple": 1.0,
                "moderate": 0.95,
                "complex": 0.9
            }.get(request.complexity, 0.8)
            
            quality_score = base_quality * complexity_factor * random.uniform(0.95, 1.05)
            quality_score = min(1.0, max(0.0, quality_score))
            
            return SimulationResult(
                request=request,
                model_selected=selection['model'],
                actual_cost=actual_cost,
                quality_score=quality_score,
                response_time=response_time,
                legal_compliant=True,
                success=True
            )
            
        except Exception as e:
            return SimulationResult(
                request=request,
                model_selected="error",
                actual_cost=0.0,
                quality_score=0.0,
                response_time=time.time() - start_time,
                legal_compliant=True,
                success=False,
                error_message=str(e)
            )
    
    def _generate_report(self, scenario: SimulationScenario, 
                        requests: List[SimulationRequest], 
                        results: List[SimulationResult]) -> SimulationReport:
        """Generate comprehensive simulation report"""
        
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]
        blocked_results = [r for r in results if not r.legal_compliant]
        
        # Performance metrics
        response_times = [r.response_time for r in successful_results]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        # Cost metrics
        costs = [r.actual_cost for r in successful_results]
        total_cost = sum(costs)
        avg_cost_per_request = statistics.mean(costs) if costs else 0
        
        total_budget = sum(r.budget_remaining for r in requests)
        budget_efficiency = (total_cost / total_budget) if total_budget > 0 else 0
        
        # Quality metrics
        quality_scores = [r.quality_score for r in successful_results]
        avg_quality_score = statistics.mean(quality_scores) if quality_scores else 0
        quality_consistency = 1.0 - (statistics.stdev(quality_scores) if len(quality_scores) > 1 else 0)
        
        # User satisfaction (based on quality vs expectations)
        satisfaction_scores = []
        for result in successful_results:
            expected = result.request.expected_quality
            actual = result.quality_score
            satisfaction = min(1.0, actual / expected) if expected > 0 else 0
            satisfaction_scores.append(satisfaction)
        
        user_satisfaction = statistics.mean(satisfaction_scores) if satisfaction_scores else 0
        
        # Compliance metrics
        legal_compliance_rate = len([r for r in results if r.legal_compliant]) / len(results) if results else 0
        
        # Model usage distribution
        model_usage = {}
        for result in successful_results:
            model = result.model_selected
            model_usage[model] = model_usage.get(model, 0) + 1
        
        # Generate recommendations
        recommendations = self._generate_recommendations(scenario, results)
        
        return SimulationReport(
            scenario=scenario,
            total_requests=len(requests),
            successful_requests=len(successful_results),
            failed_requests=len(failed_results),
            avg_response_time=avg_response_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            total_cost=total_cost,
            avg_cost_per_request=avg_cost_per_request,
            budget_efficiency=budget_efficiency,
            avg_quality_score=avg_quality_score,
            quality_consistency=quality_consistency,
            user_satisfaction=user_satisfaction,
            legal_compliance_rate=legal_compliance_rate,
            blocked_requests=len(blocked_results),
            model_usage=model_usage,
            optimization_recommendations=recommendations['optimization'],
            performance_insights=recommendations['performance'],
            cost_optimization_tips=recommendations['cost']
        )
    
    def _generate_recommendations(self, scenario: SimulationScenario, 
                                 results: List[SimulationResult]) -> Dict[str, List[str]]:
        """Generate actionable recommendations based on simulation results"""
        recommendations = {
            "optimization": [],
            "performance": [],
            "cost": []
        }
        
        successful_results = [r for r in results if r.success]
        
        # Response time analysis
        slow_requests = [r for r in successful_results if r.response_time > 3.0]
        if len(slow_requests) > len(successful_results) * 0.2:
            recommendations["performance"].append(
                "Consider implementing response time caching for improved performance"
            )
        
        # Cost analysis
        high_cost_requests = [r for r in successful_results if r.actual_cost > 0.01]
        if len(high_cost_requests) > len(successful_results) * 0.3:
            recommendations["cost"].append(
                "High-cost model usage detected - implement budget-aware model selection"
            )
        
        # Quality analysis
        low_quality_requests = [r for r in successful_results if r.quality_score < 0.7]
        if len(low_quality_requests) > len(successful_results) * 0.1:
            recommendations["optimization"].append(
                "Quality scores below threshold - consider prompt enhancement pipeline"
            )
        
        # Model distribution analysis
        model_usage = {}
        for result in successful_results:
            model = result.model_selected
            model_usage[model] = model_usage.get(model, 0) + 1
        
        if model_usage:
            most_used = max(model_usage, key=model_usage.get)
            usage_percentage = model_usage[most_used] / len(successful_results)
            
            if usage_percentage > 0.8:
                recommendations["optimization"].append(
                    f"Over-reliance on {most_used} - consider more diverse model selection"
                )
        
        # Scenario-specific recommendations
        if scenario == SimulationScenario.BUDGET_CONSTRAINED:
            recommendations["cost"].extend([
                "Implement progressive quality degradation for budget constraints",
                "Consider batch processing for cost efficiency",
                "Add budget warning system for users"
            ])
        
        elif scenario == SimulationScenario.PEAK_LOAD:
            recommendations["performance"].extend([
                "Implement load balancing across model endpoints",
                "Consider request queuing during peak times",
                "Add auto-scaling for high traffic periods"
            ])
        
        elif scenario == SimulationScenario.LEGAL_EDGE_CASES:
            blocked_count = len([r for r in results if not r.legal_compliant])
            if blocked_count > 0:
                recommendations["optimization"].append(
                    f"Legal validator blocked {blocked_count} requests - review edge case handling"
                )
        
        return recommendations
    
    def run_comprehensive_test(self) -> Dict[str, SimulationReport]:
        """Run all simulation scenarios for comprehensive testing"""
        logger.info("Starting comprehensive optimization simulation")
        
        scenarios = [
            (SimulationScenario.LOW_TRAFFIC, 5, 2),
            (SimulationScenario.MODERATE_TRAFFIC, 5, 4),
            (SimulationScenario.HIGH_TRAFFIC, 3, 8),
            (SimulationScenario.PEAK_LOAD, 2, 12),
            (SimulationScenario.BUDGET_CONSTRAINED, 3, 6),
            (SimulationScenario.MIXED_USER_SEGMENTS, 4, 5),
            (SimulationScenario.LEGAL_EDGE_CASES, 3, 4),
            (SimulationScenario.SYSTEM_STRESS, 2, 10)
        ]
        
        reports = {}
        
        for scenario, duration, rpm in scenarios:
            try:
                report = self.run_simulation(scenario, duration, rpm)
                reports[scenario.value] = report
                logger.info(f"Completed simulation: {scenario.value}")
            except Exception as e:
                logger.error(f"Failed simulation {scenario.value}: {e}")
        
        return reports


def get_simulator() -> OptimizationSimulator:
    """Get optimization simulator instance"""
    return OptimizationSimulator()


if __name__ == "__main__":
    # Example usage
    simulator = get_simulator()
    
    # Run single scenario
    report = simulator.run_simulation(SimulationScenario.MODERATE_TRAFFIC, duration_minutes=3)
    
    print(f"Simulation Results: {report.scenario.value}")
    print(f"Success Rate: {report.successful_requests}/{report.total_requests}")
    print(f"Avg Response Time: {report.avg_response_time:.2f}s")
    print(f"Avg Quality Score: {report.avg_quality_score:.2f}")
    print(f"Total Cost: ${report.total_cost:.4f}")
    print(f"Legal Compliance: {report.legal_compliance_rate:.1%}")
    
    print("\\nRecommendations:")
    for rec in report.optimization_recommendations:
        print(f"- {rec}")