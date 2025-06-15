"""
Simple Telemetry Analysis Engine
Basic system for studying app logs without heavy ML dependencies
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import statistics
from collections import defaultdict, Counter
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)


class AnalysisType(Enum):
    """Types of analysis"""
    PERFORMANCE = "performance"
    USAGE_PATTERNS = "usage_patterns"
    ERROR_ANALYSIS = "error_analysis"
    COST_ANALYSIS = "cost_analysis"


@dataclass
class TelemetryInsight:
    """Insight discovered from telemetry data"""
    insight_id: str
    insight_type: AnalysisType
    title: str
    description: str
    recommendations: List[str]
    confidence: float
    impact_score: float
    discovered_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class SimpleTelemetryAnalyzer:
    """Simple telemetry analyzer without ML dependencies"""
    
    def __init__(self, storage_path: str = "/var/projects/ai-integration-platform/telemetry_data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True, parents=True)
        self.insights: List[TelemetryInsight] = []
        self.analysis_cache: Dict[str, Any] = {}
        
    def analyze_telemetry_data(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze telemetry data and generate insights"""
        
        if not telemetry_data:
            return {
                'success': False,
                'error': 'No telemetry data provided'
            }
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'total_events': len(telemetry_data.get('events', [])),
            'analysis_types': []
        }
        
        events = telemetry_data.get('events', [])
        if not events:
            return {
                'success': True,
                'analysis': analysis_results,
                'insights': [],
                'recommendations': ['No events to analyze']
            }
        
        # Performance analysis
        performance_analysis = self._analyze_performance(events)
        analysis_results['performance'] = performance_analysis
        analysis_results['analysis_types'].append('performance')
        
        # Usage pattern analysis
        usage_analysis = self._analyze_usage_patterns(events)
        analysis_results['usage_patterns'] = usage_analysis
        analysis_results['analysis_types'].append('usage_patterns')
        
        # Error analysis
        error_analysis = self._analyze_errors(events)
        analysis_results['error_analysis'] = error_analysis
        analysis_results['analysis_types'].append('error_analysis')
        
        # Cost analysis
        cost_analysis = self._analyze_costs(events)
        analysis_results['cost_analysis'] = cost_analysis
        analysis_results['analysis_types'].append('cost_analysis')
        
        # Generate insights
        insights = self._generate_insights(analysis_results)
        
        return {
            'success': True,
            'analysis': analysis_results,
            'insights': [self._insight_to_dict(insight) for insight in insights],
            'recommendations': self._generate_recommendations(analysis_results)
        }
    
    def _analyze_performance(self, events: List[Dict]) -> Dict[str, Any]:
        """Analyze performance metrics"""
        response_times = []
        success_count = 0
        total_requests = 0
        
        for event in events:
            if event.get('event_type') == 'request_completed':
                total_requests += 1
                if event.get('data', {}).get('success'):
                    success_count += 1
                
                processing_time = event.get('data', {}).get('processing_time', 0)
                if processing_time > 0:
                    response_times.append(processing_time)
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
        else:
            avg_response_time = median_response_time = max_response_time = min_response_time = 0
        
        success_rate = (success_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'total_requests': total_requests,
            'success_count': success_count,
            'success_rate': success_rate,
            'avg_response_time': avg_response_time,
            'median_response_time': median_response_time,
            'max_response_time': max_response_time,
            'min_response_time': min_response_time,
            'response_time_count': len(response_times)
        }
    
    def _analyze_usage_patterns(self, events: List[Dict]) -> Dict[str, Any]:
        """Analyze usage patterns"""
        hourly_usage = defaultdict(int)
        service_usage = defaultdict(int)
        capability_usage = defaultdict(int)
        
        for event in events:
            # Extract hour from timestamp
            timestamp = event.get('timestamp')
            if timestamp:
                if isinstance(timestamp, str):
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    except:
                        dt = datetime.now()
                else:
                    dt = timestamp
                hour = dt.hour
                hourly_usage[hour] += 1
            
            # Count service usage
            data = event.get('data', {})
            service = data.get('service')
            if service:
                service_usage[service] += 1
            
            # Count capability usage
            capability = data.get('capability')
            if capability:
                capability_usage[capability] += 1
        
        # Find peak usage hour
        peak_hour = max(hourly_usage, key=hourly_usage.get) if hourly_usage else 0
        
        # Find most used service
        most_used_service = max(service_usage, key=service_usage.get) if service_usage else None
        
        # Find most used capability
        most_used_capability = max(capability_usage, key=capability_usage.get) if capability_usage else None
        
        return {
            'hourly_distribution': dict(hourly_usage),
            'peak_hour': peak_hour,
            'service_usage': dict(service_usage),
            'most_used_service': most_used_service,
            'capability_usage': dict(capability_usage),
            'most_used_capability': most_used_capability,
            'unique_services': len(service_usage),
            'unique_capabilities': len(capability_usage)
        }
    
    def _analyze_errors(self, events: List[Dict]) -> Dict[str, Any]:
        """Analyze error patterns"""
        error_types = defaultdict(int)
        error_services = defaultdict(int)
        total_errors = 0
        
        for event in events:
            data = event.get('data', {})
            if not data.get('success', True):
                total_errors += 1
                
                # Categorize error types
                error_msg = str(data.get('error', 'Unknown error')).lower()
                if 'timeout' in error_msg:
                    error_types['timeout'] += 1
                elif 'rate limit' in error_msg or 'too many requests' in error_msg:
                    error_types['rate_limit'] += 1
                elif 'auth' in error_msg or 'unauthorized' in error_msg:
                    error_types['authentication'] += 1
                elif 'network' in error_msg or 'connection' in error_msg:
                    error_types['network'] += 1
                else:
                    error_types['other'] += 1
                
                # Track which services have errors
                service = data.get('service')
                if service:
                    error_services[service] += 1
        
        most_error_prone_service = max(error_services, key=error_services.get) if error_services else None
        most_common_error_type = max(error_types, key=error_types.get) if error_types else None
        
        return {
            'total_errors': total_errors,
            'error_types': dict(error_types),
            'most_common_error_type': most_common_error_type,
            'error_by_service': dict(error_services),
            'most_error_prone_service': most_error_prone_service,
            'error_rate': total_errors / len(events) * 100 if events else 0
        }
    
    def _analyze_costs(self, events: List[Dict]) -> Dict[str, Any]:
        """Analyze cost patterns"""
        total_cost = 0
        service_costs = defaultdict(float)
        free_tier_usage = 0
        paid_usage = 0
        
        for event in events:
            data = event.get('data', {})
            cost = data.get('cost', 0)
            
            if cost > 0:
                total_cost += cost
                paid_usage += 1
                
                service = data.get('service')
                if service:
                    service_costs[service] += cost
            else:
                free_tier_usage += 1
        
        most_expensive_service = max(service_costs, key=service_costs.get) if service_costs else None
        
        return {
            'total_cost': total_cost,
            'service_costs': dict(service_costs),
            'most_expensive_service': most_expensive_service,
            'free_tier_usage': free_tier_usage,
            'paid_usage': paid_usage,
            'avg_cost_per_request': total_cost / paid_usage if paid_usage > 0 else 0,
            'free_tier_percentage': free_tier_usage / len(events) * 100 if events else 0
        }
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[TelemetryInsight]:
        """Generate insights from analysis"""
        insights = []
        
        # Performance insights
        perf = analysis.get('performance', {})
        if perf.get('success_rate', 0) < 95:
            insights.append(TelemetryInsight(
                insight_id=f"perf_low_success_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                insight_type=AnalysisType.PERFORMANCE,
                title="Low Success Rate Detected",
                description=f"System success rate is {perf.get('success_rate', 0):.1f}%, below recommended 95%",
                recommendations=[
                    "Review error logs for common failure patterns",
                    "Consider implementing additional fallback services",
                    "Check service health and API limits"
                ],
                confidence=0.9,
                impact_score=8.5,
                discovered_at=datetime.now()
            ))
        
        if perf.get('avg_response_time', 0) > 5:
            insights.append(TelemetryInsight(
                insight_id=f"perf_slow_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                insight_type=AnalysisType.PERFORMANCE,
                title="Slow Response Times",
                description=f"Average response time is {perf.get('avg_response_time', 0):.2f}s, above recommended 5s",
                recommendations=[
                    "Optimize API request processing",
                    "Consider caching frequently used responses",
                    "Review service timeouts and connection pooling"
                ],
                confidence=0.8,
                impact_score=7.0,
                discovered_at=datetime.now()
            ))
        
        # Cost insights
        cost = analysis.get('cost_analysis', {})
        if cost.get('free_tier_percentage', 0) < 50:
            insights.append(TelemetryInsight(
                insight_id=f"cost_low_free_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                insight_type=AnalysisType.COST_ANALYSIS,
                title="Low Free Tier Usage",
                description=f"Only {cost.get('free_tier_percentage', 0):.1f}% of requests use free tier",
                recommendations=[
                    "Prioritize free tier services in routing logic",
                    "Review service selection algorithm",
                    "Consider adding more free tier alternatives"
                ],
                confidence=0.7,
                impact_score=6.0,
                discovered_at=datetime.now()
            ))
        
        self.insights.extend(insights)
        return insights
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Performance recommendations
        perf = analysis.get('performance', {})
        if perf.get('success_rate', 0) < 95:
            recommendations.append("Improve system reliability - success rate below 95%")
        
        if perf.get('avg_response_time', 0) > 3:
            recommendations.append("Optimize response times - currently above 3 seconds")
        
        # Usage pattern recommendations
        usage = analysis.get('usage_patterns', {})
        if usage.get('unique_services', 0) < 2:
            recommendations.append("Add more service providers for redundancy")
        
        # Error recommendations
        errors = analysis.get('error_analysis', {})
        if errors.get('error_rate', 0) > 5:
            recommendations.append("Investigate and fix error patterns - error rate above 5%")
        
        # Cost recommendations
        cost = analysis.get('cost_analysis', {})
        if cost.get('total_cost', 0) > 50:
            recommendations.append("Review spending - daily cost exceeds $50")
        
        if cost.get('free_tier_percentage', 0) < 30:
            recommendations.append("Increase free tier usage to reduce costs")
        
        if not recommendations:
            recommendations.append("System is performing well - no immediate actions needed")
        
        return recommendations
    
    def _insight_to_dict(self, insight: TelemetryInsight) -> Dict[str, Any]:
        """Convert insight to dictionary"""
        return {
            'insight_id': insight.insight_id,
            'insight_type': insight.insight_type.value,
            'title': insight.title,
            'description': insight.description,
            'recommendations': insight.recommendations,
            'confidence': insight.confidence,
            'impact_score': insight.impact_score,
            'discovered_at': insight.discovered_at.isoformat(),
            'metadata': insight.metadata
        }
    
    def export_telemetry(self, hours: int = 24) -> Dict[str, Any]:
        """Export telemetry data"""
        return {
            'exported_at': datetime.now().isoformat(),
            'hours_covered': hours,
            'insights_count': len(self.insights),
            'insights': [self._insight_to_dict(insight) for insight in self.insights[-10:]]  # Last 10 insights
        }


# Global instance
_telemetry_analyzer: Optional[SimpleTelemetryAnalyzer] = None


def get_telemetry_analyzer() -> SimpleTelemetryAnalyzer:
    """Get global telemetry analyzer instance"""
    global _telemetry_analyzer
    if _telemetry_analyzer is None:
        _telemetry_analyzer = SimpleTelemetryAnalyzer()
    return _telemetry_analyzer