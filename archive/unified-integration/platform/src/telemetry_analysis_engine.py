"""
Telemetry Analysis Engine
Advanced system for studying app logs, patterns, and insights
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import statistics
from collections import defaultdict, Counter
import pickle
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Optional ML dependencies
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    ML_AVAILABLE = True
except ImportError:
    # Create mock objects for when ML libraries aren't available
    np = None
    pd = None
    plt = None
    sns = None
    KMeans = None
    StandardScaler = None
    PCA = None
    ML_AVAILABLE = False

logger = logging.getLogger(__name__)


class AnalysisType(Enum):
    """Types of telemetry analysis"""
    USAGE_PATTERNS = "usage_patterns"
    PERFORMANCE_METRICS = "performance_metrics"
    ERROR_ANALYSIS = "error_analysis"
    COST_OPTIMIZATION = "cost_optimization"
    USER_BEHAVIOR = "user_behavior"
    API_EFFICIENCY = "api_efficiency"
    ANOMALY_DETECTION = "anomaly_detection"
    TREND_ANALYSIS = "trend_analysis"


@dataclass
class TelemetryInsight:
    """Represents an insight derived from telemetry data"""
    insight_type: str
    title: str
    description: str
    severity: str  # info, warning, critical
    metrics: Dict[str, Any]
    recommendations: List[str]
    confidence: float
    discovered_at: datetime = field(default_factory=datetime.now)
    impact_score: float = 0.0


@dataclass
class PerformanceProfile:
    """Performance profile derived from telemetry"""
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    error_rate: float
    success_rate: float
    throughput: float  # requests per minute
    latency_distribution: Dict[str, float]
    bottlenecks: List[str]


@dataclass
class UsagePattern:
    """Identified usage pattern"""
    pattern_id: str
    pattern_type: str
    frequency: int
    time_distribution: Dict[str, int]  # hour -> count
    user_segments: List[str]
    common_features: List[str]
    effectiveness_score: float


@dataclass
class AnomalyReport:
    """Anomaly detection report"""
    anomaly_type: str
    timestamp: datetime
    severity: float  # 0-1
    affected_metrics: List[str]
    deviation_score: float
    context: Dict[str, Any]
    recommended_actions: List[str]


class TelemetryAnalysisEngine:
    """Advanced telemetry analysis engine"""
    
    def __init__(self, storage_path: str = "/var/projects/ai-integration-platform/telemetry_analysis"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True, parents=True)
        
        # Analysis components
        self.insights: List[TelemetryInsight] = []
        self.patterns: Dict[str, UsagePattern] = {}
        self.anomalies: List[AnomalyReport] = []
        self.performance_profiles: Dict[str, PerformanceProfile] = {}
        
        # Machine learning models
        self.pattern_classifier = None
        self.anomaly_detector = None
        self.trend_predictor = None
        
        # Load historical data
        self._load_analysis_data()
    
    def analyze_telemetry_data(self, telemetry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive telemetry analysis"""
        logger.info("Starting comprehensive telemetry analysis")
        
        # If ML libraries not available, use simple analysis
        if not ML_AVAILABLE:
            from .simple_telemetry_analyzer import SimpleTelemetryAnalyzer
            simple_analyzer = SimpleTelemetryAnalyzer()
            return simple_analyzer.analyze_telemetry_data(telemetry_data)
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'insights': [],
            'patterns': [],
            'anomalies': [],
            'performance': {},
            'recommendations': []
        }
        
        # Convert to DataFrame for easier analysis
        df = self._telemetry_to_dataframe(telemetry_data)
        
        if df is not None and not df.empty:
            # Run different analysis types
            usage_insights = self._analyze_usage_patterns(df)
            performance_insights = self._analyze_performance(df)
            error_insights = self._analyze_errors(df)
            cost_insights = self._analyze_costs(df)
            behavior_insights = self._analyze_user_behavior(df)
            anomalies = self._detect_anomalies(df)
            trends = self._analyze_trends(df)
            
            # Combine insights
            all_insights = usage_insights + performance_insights + error_insights + cost_insights + behavior_insights
            
            # Rank insights by impact
            ranked_insights = sorted(all_insights, key=lambda x: x.impact_score, reverse=True)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(ranked_insights, anomalies)
            
            # Update results
            analysis_results['insights'] = [self._insight_to_dict(i) for i in ranked_insights[:10]]
            analysis_results['patterns'] = self._get_top_patterns()
            analysis_results['anomalies'] = [self._anomaly_to_dict(a) for a in anomalies[:5]]
            analysis_results['performance'] = self._get_performance_summary(df)
            analysis_results['recommendations'] = recommendations
            
            # Store insights
            self.insights.extend(ranked_insights)
            self.anomalies.extend(anomalies)
            
            # Save analysis
            self._save_analysis_data()
        
        return analysis_results
    
    def _telemetry_to_dataframe(self, telemetry_data: Dict[str, Any]) -> Optional[Any]:
        """Convert telemetry data to pandas DataFrame"""
        if not ML_AVAILABLE or pd is None:
            return None
            
        try:
            events = telemetry_data.get('events', [])
            if not events:
                return None
            
            # Extract relevant fields
            data_rows = []
            for event in events:
                row = {
                    'timestamp': pd.to_datetime(event.get('timestamp')),
                    'type': event.get('type'),
                    'integration': event.get('data', {}).get('integration', 'unknown'),
                    'response_time': event.get('data', {}).get('response_time'),
                    'success': event.get('data', {}).get('success', True),
                    'error': event.get('data', {}).get('error'),
                    'cost': event.get('data', {}).get('cost', 0),
                    'user_tier': event.get('data', {}).get('user_tier', 'basic'),
                    'model': event.get('data', {}).get('model', 'unknown')
                }
                data_rows.append(row)
            
            df = pd.DataFrame(data_rows)
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to convert telemetry to dataframe: {e}")
            return None
    
    def _analyze_usage_patterns(self, df: Any) -> List[TelemetryInsight]:
        """Analyze usage patterns"""
        insights = []
        
        # Time-based patterns
        hourly_usage = df.groupby('hour').size()
        peak_hours = hourly_usage.nlargest(3).index.tolist()
        
        if peak_hours:
            insights.append(TelemetryInsight(
                insight_type=AnalysisType.USAGE_PATTERNS.value,
                title="Peak Usage Hours Identified",
                description=f"System experiences peak usage during hours: {peak_hours}",
                severity="info",
                metrics={
                    'peak_hours': peak_hours,
                    'peak_requests': int(hourly_usage.max()),
                    'avg_requests_per_hour': float(hourly_usage.mean())
                },
                recommendations=[
                    "Consider scaling resources during peak hours",
                    "Implement request queuing for high-traffic periods"
                ],
                confidence=0.85,
                impact_score=0.7
            ))
        
        # Feature usage patterns
        if 'type' in df.columns:
            feature_usage = df['type'].value_counts()
            top_features = feature_usage.head(5).to_dict()
            
            insights.append(TelemetryInsight(
                insight_type=AnalysisType.USAGE_PATTERNS.value,
                title="Feature Usage Distribution",
                description="Analysis of most used features",
                severity="info",
                metrics={'top_features': top_features},
                recommendations=[
                    f"Optimize '{list(top_features.keys())[0]}' as it's the most used feature",
                    "Consider caching for frequently used operations"
                ],
                confidence=0.9,
                impact_score=0.6
            ))
        
        # User segment patterns
        if 'user_tier' in df.columns:
            tier_distribution = df['user_tier'].value_counts(normalize=True).to_dict()
            
            if tier_distribution.get('premium', 0) < 0.1:
                insights.append(TelemetryInsight(
                    insight_type=AnalysisType.USAGE_PATTERNS.value,
                    title="Low Premium User Adoption",
                    description="Less than 10% of users are on premium tier",
                    severity="warning",
                    metrics={'tier_distribution': tier_distribution},
                    recommendations=[
                        "Review premium tier pricing strategy",
                        "Enhance premium features visibility",
                        "Consider limited-time premium trials"
                    ],
                    confidence=0.95,
                    impact_score=0.8
                ))
        
        return insights
    
    def _analyze_performance(self, df: Any) -> List[TelemetryInsight]:
        """Analyze performance metrics"""
        insights = []
        
        if 'response_time' not in df.columns or df['response_time'].isna().all():
            return insights
        
        # Response time analysis
        response_times = df['response_time'].dropna()
        
        if len(response_times) > 0:
            avg_response = response_times.mean()
            p95_response = response_times.quantile(0.95)
            p99_response = response_times.quantile(0.99)
            
            # Check for performance issues
            if p95_response > 5.0:  # 5 seconds
                insights.append(TelemetryInsight(
                    insight_type=AnalysisType.PERFORMANCE_METRICS.value,
                    title="High Response Time Detected",
                    description=f"95th percentile response time is {p95_response:.2f}s",
                    severity="critical",
                    metrics={
                        'avg_response_time': float(avg_response),
                        'p95_response_time': float(p95_response),
                        'p99_response_time': float(p99_response)
                    },
                    recommendations=[
                        "Investigate slow API endpoints",
                        "Consider implementing response caching",
                        "Review model selection for efficiency",
                        "Add request timeout handling"
                    ],
                    confidence=0.95,
                    impact_score=0.9
                ))
            
            # Analyze by integration
            if 'integration' in df.columns:
                integration_perf = df.groupby('integration')['response_time'].agg(['mean', 'count'])
                slowest = integration_perf.nlargest(3, 'mean')
                
                if not slowest.empty:
                    insights.append(TelemetryInsight(
                        insight_type=AnalysisType.PERFORMANCE_METRICS.value,
                        title="Integration Performance Comparison",
                        description="Performance analysis by integration",
                        severity="info",
                        metrics={
                            'slowest_integrations': slowest.to_dict('index'),
                            'fastest_integration': integration_perf.nsmallest(1, 'mean').index[0]
                        },
                        recommendations=[
                            f"Consider alternatives to {slowest.index[0]} for better performance",
                            "Implement fallback to faster integrations when possible"
                        ],
                        confidence=0.85,
                        impact_score=0.7
                    ))
        
        return insights
    
    def _analyze_errors(self, df: Any) -> List[TelemetryInsight]:
        """Analyze error patterns"""
        insights = []
        
        if 'success' not in df.columns:
            return insights
        
        # Error rate analysis
        error_rate = (~df['success']).mean()
        
        if error_rate > 0.05:  # 5% error rate
            insights.append(TelemetryInsight(
                insight_type=AnalysisType.ERROR_ANALYSIS.value,
                title="High Error Rate Detected",
                description=f"System error rate is {error_rate*100:.1f}%",
                severity="critical",
                metrics={
                    'error_rate': float(error_rate),
                    'total_errors': int((~df['success']).sum()),
                    'total_requests': len(df)
                },
                recommendations=[
                    "Implement comprehensive error recovery",
                    "Add retry logic with exponential backoff",
                    "Review error logs for common patterns"
                ],
                confidence=0.95,
                impact_score=0.95
            ))
        
        # Error patterns by time
        if 'hour' in df.columns:
            hourly_errors = df[~df['success']].groupby('hour').size()
            if len(hourly_errors) > 0:
                peak_error_hours = hourly_errors.nlargest(3).index.tolist()
                
                insights.append(TelemetryInsight(
                    insight_type=AnalysisType.ERROR_ANALYSIS.value,
                    title="Time-based Error Pattern",
                    description=f"Errors peak during hours: {peak_error_hours}",
                    severity="warning",
                    metrics={
                        'peak_error_hours': peak_error_hours,
                        'error_distribution': hourly_errors.to_dict()
                    },
                    recommendations=[
                        "Investigate infrastructure issues during peak error hours",
                        "Consider rate limiting during high-error periods"
                    ],
                    confidence=0.8,
                    impact_score=0.7
                ))
        
        return insights
    
    def _analyze_costs(self, df: Any) -> List[TelemetryInsight]:
        """Analyze cost patterns"""
        insights = []
        
        if 'cost' not in df.columns or df['cost'].isna().all():
            return insights
        
        # Total cost analysis
        total_cost = df['cost'].sum()
        daily_avg = total_cost / max(1, (df['timestamp'].max() - df['timestamp'].min()).days)
        
        # Cost by integration
        if 'integration' in df.columns:
            cost_by_integration = df.groupby('integration')['cost'].sum().sort_values(ascending=False)
            
            if len(cost_by_integration) > 0:
                top_cost_integration = cost_by_integration.index[0]
                top_cost_percentage = (cost_by_integration.iloc[0] / total_cost) * 100
                
                if top_cost_percentage > 50:
                    insights.append(TelemetryInsight(
                        insight_type=AnalysisType.COST_OPTIMIZATION.value,
                        title="Cost Concentration Risk",
                        description=f"{top_cost_integration} accounts for {top_cost_percentage:.1f}% of costs",
                        severity="warning",
                        metrics={
                            'cost_distribution': cost_by_integration.to_dict(),
                            'total_cost': float(total_cost),
                            'daily_average': float(daily_avg)
                        },
                        recommendations=[
                            f"Explore alternatives to {top_cost_integration}",
                            "Implement usage caps for expensive integrations",
                            "Consider tiered pricing negotiations"
                        ],
                        confidence=0.9,
                        impact_score=0.85
                    ))
        
        # Cost efficiency
        if 'success' in df.columns:
            successful_cost = df[df['success']]['cost'].sum()
            failed_cost = df[~df['success']]['cost'].sum()
            
            if failed_cost > successful_cost * 0.1:  # 10% of cost on failures
                insights.append(TelemetryInsight(
                    insight_type=AnalysisType.COST_OPTIMIZATION.value,
                    title="High Cost on Failed Requests",
                    description=f"${failed_cost:.2f} spent on failed requests",
                    severity="critical",
                    metrics={
                        'failed_request_cost': float(failed_cost),
                        'success_request_cost': float(successful_cost),
                        'waste_percentage': float(failed_cost / total_cost * 100)
                    },
                    recommendations=[
                        "Implement pre-validation to reduce failed requests",
                        "Add circuit breakers to prevent cascading failures",
                        "Review and fix common failure causes"
                    ],
                    confidence=0.95,
                    impact_score=0.9
                ))
        
        return insights
    
    def _analyze_user_behavior(self, df: Any) -> List[TelemetryInsight]:
        """Analyze user behavior patterns"""
        insights = []
        
        # Request patterns
        if 'timestamp' in df.columns:
            # Calculate request intervals
            df_sorted = df.sort_values('timestamp')
            time_diffs = df_sorted['timestamp'].diff().dt.total_seconds()
            
            if len(time_diffs) > 10:
                avg_interval = time_diffs.mean()
                
                if avg_interval < 5:  # Less than 5 seconds between requests
                    insights.append(TelemetryInsight(
                        insight_type=AnalysisType.USER_BEHAVIOR.value,
                        title="High-Frequency Usage Pattern",
                        description="Users making rapid consecutive requests",
                        severity="info",
                        metrics={
                            'avg_request_interval': float(avg_interval),
                            'min_interval': float(time_diffs.min()),
                            'requests_under_5s': int((time_diffs < 5).sum())
                        },
                        recommendations=[
                            "Implement request batching for better efficiency",
                            "Add client-side caching to reduce redundant requests",
                            "Consider WebSocket for real-time use cases"
                        ],
                        confidence=0.85,
                        impact_score=0.7
                    ))
        
        # Model preference analysis
        if 'model' in df.columns:
            model_preferences = df['model'].value_counts(normalize=True)
            
            if len(model_preferences) > 1:
                insights.append(TelemetryInsight(
                    insight_type=AnalysisType.USER_BEHAVIOR.value,
                    title="Model Usage Preferences",
                    description="Analysis of model selection patterns",
                    severity="info",
                    metrics={
                        'model_distribution': model_preferences.to_dict(),
                        'most_used_model': model_preferences.index[0],
                        'diversity_score': float(1 - model_preferences.iloc[0])  # How diverse the usage is
                    },
                    recommendations=[
                        f"Optimize performance for {model_preferences.index[0]} model",
                        "Create model recommendation system based on task type"
                    ],
                    confidence=0.8,
                    impact_score=0.6
                ))
        
        return insights
    
    def _detect_anomalies(self, df: Any) -> List[AnomalyReport]:
        """Detect anomalies in telemetry data"""
        anomalies = []
        
        # Response time anomalies
        if 'response_time' in df.columns and len(df) > 10:
            response_times = df['response_time'].dropna()
            
            if len(response_times) > 0:
                mean_rt = response_times.mean()
                std_rt = response_times.std()
                
                # Detect outliers (3 sigma)
                outliers = response_times[response_times > mean_rt + 3 * std_rt]
                
                if len(outliers) > 0:
                    for idx, outlier_value in outliers.items():
                        anomalies.append(AnomalyReport(
                            anomaly_type="response_time_spike",
                            timestamp=df.loc[idx, 'timestamp'],
                            severity=min(1.0, (outlier_value - mean_rt) / (5 * std_rt)),
                            affected_metrics=['response_time'],
                            deviation_score=float((outlier_value - mean_rt) / std_rt),
                            context={
                                'value': float(outlier_value),
                                'mean': float(mean_rt),
                                'integration': df.loc[idx, 'integration'] if 'integration' in df.columns else 'unknown'
                            },
                            recommended_actions=[
                                "Check API endpoint health",
                                "Review request complexity",
                                "Verify network conditions"
                            ]
                        ))
        
        # Cost anomalies
        if 'cost' in df.columns and len(df) > 10:
            # Group by hour and detect unusual cost spikes
            hourly_costs = df.groupby(df['timestamp'].dt.floor('H'))['cost'].sum()
            
            if len(hourly_costs) > 3:
                cost_mean = hourly_costs.mean()
                cost_std = hourly_costs.std()
                
                cost_outliers = hourly_costs[hourly_costs > cost_mean + 2 * cost_std]
                
                for timestamp, cost in cost_outliers.items():
                    anomalies.append(AnomalyReport(
                        anomaly_type="cost_spike",
                        timestamp=timestamp,
                        severity=min(1.0, (cost - cost_mean) / (3 * cost_std)),
                        affected_metrics=['cost'],
                        deviation_score=float((cost - cost_mean) / cost_std),
                        context={
                            'hourly_cost': float(cost),
                            'expected_cost': float(cost_mean),
                            'period': timestamp.strftime('%Y-%m-%d %H:00')
                        },
                        recommended_actions=[
                            "Review requests during this period",
                            "Check for unusual usage patterns",
                            "Verify cost calculations"
                        ]
                    ))
        
        return anomalies
    
    def _analyze_trends(self, df: Any) -> Dict[str, Any]:
        """Analyze trends in the data"""
        trends = {}
        
        if len(df) < 10:
            return trends
        
        # Time series analysis
        if 'timestamp' in df.columns:
            # Aggregate by hour
            hourly_counts = df.set_index('timestamp').resample('H').size()
            
            if len(hourly_counts) > 24:  # At least 24 hours of data
                # Simple trend detection
                x = np.arange(len(hourly_counts))
                y = hourly_counts.values
                
                # Linear regression for trend
                z = np.polyfit(x, y, 1)
                slope = z[0]
                
                trends['usage_trend'] = {
                    'direction': 'increasing' if slope > 0 else 'decreasing',
                    'strength': abs(slope),
                    'forecast_next_hour': max(0, z[0] * len(hourly_counts) + z[1])
                }
        
        return trends
    
    def _generate_recommendations(self, insights: List[TelemetryInsight], 
                                 anomalies: List[AnomalyReport]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        priority_actions = []
        
        # Analyze critical insights
        critical_insights = [i for i in insights if i.severity == "critical"]
        
        for insight in critical_insights:
            priority_actions.extend(insight.recommendations[:2])
        
        # Analyze anomalies
        if len(anomalies) > 5:
            recommendations.append("Multiple anomalies detected - consider system health check")
        
        # Cost optimization
        cost_insights = [i for i in insights if i.insight_type == AnalysisType.COST_OPTIMIZATION.value]
        if cost_insights:
            recommendations.append("Implement cost monitoring dashboard with alerts")
        
        # Performance optimization
        perf_insights = [i for i in insights if i.insight_type == AnalysisType.PERFORMANCE_METRICS.value]
        if perf_insights:
            recommendations.append("Set up performance monitoring with SLA tracking")
        
        # Combine and prioritize
        all_recommendations = list(set(priority_actions + recommendations))
        
        return all_recommendations[:10]  # Top 10 recommendations
    
    def _get_performance_summary(self, df: Any) -> Dict[str, Any]:
        """Get performance summary statistics"""
        summary = {
            'total_requests': len(df),
            'time_range': {
                'start': df['timestamp'].min().isoformat() if 'timestamp' in df.columns else None,
                'end': df['timestamp'].max().isoformat() if 'timestamp' in df.columns else None
            }
        }
        
        if 'response_time' in df.columns:
            rt = df['response_time'].dropna()
            if len(rt) > 0:
                summary['response_times'] = {
                    'mean': float(rt.mean()),
                    'median': float(rt.median()),
                    'p95': float(rt.quantile(0.95)),
                    'p99': float(rt.quantile(0.99))
                }
        
        if 'success' in df.columns:
            summary['success_rate'] = float(df['success'].mean() * 100)
        
        if 'cost' in df.columns:
            summary['total_cost'] = float(df['cost'].sum())
        
        return summary
    
    def _get_top_patterns(self) -> List[Dict[str, Any]]:
        """Get top usage patterns"""
        # This would return actual detected patterns
        # For now, returning placeholder
        return []
    
    def _insight_to_dict(self, insight: TelemetryInsight) -> Dict[str, Any]:
        """Convert insight to dictionary"""
        return {
            'type': insight.insight_type,
            'title': insight.title,
            'description': insight.description,
            'severity': insight.severity,
            'metrics': insight.metrics,
            'recommendations': insight.recommendations,
            'confidence': insight.confidence,
            'impact_score': insight.impact_score,
            'discovered_at': insight.discovered_at.isoformat()
        }
    
    def _anomaly_to_dict(self, anomaly: AnomalyReport) -> Dict[str, Any]:
        """Convert anomaly to dictionary"""
        return {
            'type': anomaly.anomaly_type,
            'timestamp': anomaly.timestamp.isoformat(),
            'severity': anomaly.severity,
            'affected_metrics': anomaly.affected_metrics,
            'deviation_score': anomaly.deviation_score,
            'context': anomaly.context,
            'recommended_actions': anomaly.recommended_actions
        }
    
    def visualize_insights(self, analysis_results: Dict[str, Any], 
                          output_dir: str = "/var/projects/ai-integration-platform/telemetry_visuals"):
        """Generate visualizations for insights"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Performance visualization
        if 'performance' in analysis_results and 'response_times' in analysis_results['performance']:
            fig, ax = plt.subplots(figsize=(10, 6))
            rt_data = analysis_results['performance']['response_times']
            
            metrics = ['mean', 'median', 'p95', 'p99']
            values = [rt_data[m] for m in metrics]
            
            ax.bar(metrics, values, color=['blue', 'green', 'orange', 'red'])
            ax.set_ylabel('Response Time (seconds)')
            ax.set_title('Response Time Metrics')
            
            plt.tight_layout()
            plt.savefig(output_path / 'response_time_metrics.png')
            plt.close()
        
        # Insights by severity
        if 'insights' in analysis_results:
            severity_counts = Counter(i['severity'] for i in analysis_results['insights'])
            
            if severity_counts:
                fig, ax = plt.subplots(figsize=(8, 8))
                colors = {'critical': 'red', 'warning': 'orange', 'info': 'blue'}
                
                ax.pie(severity_counts.values(), labels=severity_counts.keys(), 
                      colors=[colors.get(s, 'gray') for s in severity_counts.keys()],
                      autopct='%1.1f%%')
                ax.set_title('Insights by Severity')
                
                plt.tight_layout()
                plt.savefig(output_path / 'insights_severity.png')
                plt.close()
        
        return output_path
    
    def export_report(self, analysis_results: Dict[str, Any], 
                     format: str = 'json') -> str:
        """Export analysis report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"telemetry_analysis_{timestamp}.{format}"
        filepath = self.storage_path / filename
        
        if format == 'json':
            with open(filepath, 'w') as f:
                json.dump(analysis_results, f, indent=2)
        elif format == 'html':
            # Generate HTML report
            html_content = self._generate_html_report(analysis_results)
            with open(filepath, 'w') as f:
                f.write(html_content)
        
        logger.info(f"Analysis report exported to {filepath}")
        return str(filepath)
    
    def _generate_html_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Telemetry Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #333; }}
                .insight {{ background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .critical {{ border-left: 5px solid red; }}
                .warning {{ border-left: 5px solid orange; }}
                .info {{ border-left: 5px solid blue; }}
                .metric {{ display: inline-block; margin: 5px 10px; }}
                .recommendation {{ background: #e0f0e0; padding: 10px; margin: 5px 0; }}
            </style>
        </head>
        <body>
            <h1>Telemetry Analysis Report</h1>
            <p>Generated: {analysis_results['timestamp']}</p>
            
            <h2>Key Insights</h2>
        """
        
        for insight in analysis_results.get('insights', []):
            html += f"""
            <div class="insight {insight['severity']}">
                <h3>{insight['title']}</h3>
                <p>{insight['description']}</p>
                <div class="metrics">
                    <strong>Metrics:</strong>
                    {self._format_metrics_html(insight['metrics'])}
                </div>
                <div class="recommendations">
                    <strong>Recommendations:</strong>
                    <ul>
                        {''.join(f'<li>{r}</li>' for r in insight['recommendations'])}
                    </ul>
                </div>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def _format_metrics_html(self, metrics: Dict[str, Any]) -> str:
        """Format metrics for HTML display"""
        html = ""
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                html += f'<span class="metric"><strong>{key}:</strong> {value:.2f}</span>'
            else:
                html += f'<span class="metric"><strong>{key}:</strong> {value}</span>'
        return html
    
    def _load_analysis_data(self):
        """Load historical analysis data"""
        try:
            insights_file = self.storage_path / 'insights_history.pkl'
            if insights_file.exists():
                with open(insights_file, 'rb') as f:
                    self.insights = pickle.load(f)
            
            patterns_file = self.storage_path / 'patterns.pkl'
            if patterns_file.exists():
                with open(patterns_file, 'rb') as f:
                    self.patterns = pickle.load(f)
                    
        except Exception as e:
            logger.error(f"Failed to load analysis data: {e}")
    
    def _save_analysis_data(self):
        """Save analysis data"""
        try:
            # Keep only recent insights
            recent_insights = [i for i in self.insights 
                             if i.discovered_at > datetime.now() - timedelta(days=30)]
            
            with open(self.storage_path / 'insights_history.pkl', 'wb') as f:
                pickle.dump(recent_insights, f)
            
            with open(self.storage_path / 'patterns.pkl', 'wb') as f:
                pickle.dump(self.patterns, f)
                
        except Exception as e:
            logger.error(f"Failed to save analysis data: {e}")


# Global instance
_telemetry_analyzer: Optional[TelemetryAnalysisEngine] = None


def get_telemetry_analyzer() -> TelemetryAnalysisEngine:
    """Get global telemetry analyzer instance"""
    global _telemetry_analyzer
    if _telemetry_analyzer is None:
        _telemetry_analyzer = TelemetryAnalysisEngine()
    return _telemetry_analyzer