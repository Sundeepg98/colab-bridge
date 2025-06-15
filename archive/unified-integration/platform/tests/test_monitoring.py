"""
Test Suite for Monitoring Features

Comprehensive tests for monitoring, metrics collection, and analytics.
"""

import pytest
import time
from datetime import datetime, timedelta
from src.monitoring import MonitoringManager, MetricType, PerformanceStats, UsageStats
from src.config import Config


class TestMonitoringManager:
    
    def setup_method(self):
        """Set up test environment"""
        self.config = Config("testing")
        self.monitoring = MonitoringManager()
    
    def test_metric_recording(self):
        """Test basic metric recording"""
        self.monitoring.record_metric(
            "test_counter", 
            1.0, 
            MetricType.COUNTER, 
            {"endpoint": "test"}
        )
        
        # Check that metric was recorded
        assert len(self.monitoring.metrics) > 0
        
        # Find our metric
        test_metric = None
        for metric in self.monitoring.metrics.values():
            if metric.name == "test_counter":
                test_metric = metric
                break
        
        assert test_metric is not None
        assert test_metric.value == 1.0
        assert test_metric.metric_type == MetricType.COUNTER
        assert test_metric.tags["endpoint"] == "test"
    
    def test_request_timing(self):
        """Test request timing functionality"""
        request_id = "test_request_123"
        endpoint = "test_endpoint"
        
        # Start timing
        self.monitoring.start_request_timer(request_id, endpoint)
        
        # Simulate some work
        time.sleep(0.1)
        
        # End timing
        self.monitoring.end_request_timer(request_id, 200, 1000, 2000)
        
        # Check that performance stats were recorded
        assert len(self.monitoring.performance_stats) > 0
        
        latest_stat = self.monitoring.performance_stats[-1]
        assert latest_stat.endpoint == endpoint
        assert latest_stat.status_code == 200
        assert latest_stat.response_time_ms >= 100  # At least 100ms
        assert latest_stat.request_size_bytes == 1000
        assert latest_stat.response_size_bytes == 2000
    
    def test_usage_recording(self):
        """Test usage statistics recording"""
        self.monitoring.record_usage(
            endpoint="test_endpoint",
            user_tier="premium",
            tokens_processed=150,
            optimization_type="claude_enhancement",
            success=True
        )
        
        # Check that usage was recorded
        assert len(self.monitoring.usage_stats) > 0
        
        latest_usage = self.monitoring.usage_stats[-1]
        assert latest_usage.endpoint == "test_endpoint"
        assert latest_usage.user_tier == "premium"
        assert latest_usage.tokens_processed == 150
        assert latest_usage.optimization_type == "claude_enhancement"
        assert latest_usage.success is True
        
        # Check success rate tracking
        success_rates = self.monitoring.optimization_success_rates
        assert "claude_enhancement" in success_rates
        assert success_rates["claude_enhancement"]["success"] == 1
        assert success_rates["claude_enhancement"]["total"] == 1
    
    def test_error_recording(self):
        """Test error event recording"""
        self.monitoring.record_error(
            endpoint="test_endpoint",
            error_type="ValueError",
            error_message="Test error message",
            stack_trace="Test stack trace",
            request_data={"prompt": "test"}
        )
        
        # Check that error was recorded
        assert len(self.monitoring.error_events) > 0
        
        latest_error = self.monitoring.error_events[-1]
        assert latest_error.endpoint == "test_endpoint"
        assert latest_error.error_type == "ValueError"
        assert latest_error.error_message == "Test error message"
        assert latest_error.request_data["prompt"] == "test"
        
        # Check error count tracking
        assert self.monitoring.error_counts["test_endpoint"] == 1
    
    def test_metrics_summary(self):
        """Test metrics summary generation"""
        # Add some test data
        self.monitoring.record_usage("test", "basic", 100, "optimization", True)
        self.monitoring.record_usage("test", "premium", 200, "optimization", False)
        
        # Add performance data
        request_id = "test"
        self.monitoring.start_request_timer(request_id, "test")
        time.sleep(0.05)
        self.monitoring.end_request_timer(request_id, 200)
        
        # Add error
        self.monitoring.record_error("test", "TestError", "Test message")
        
        # Get summary
        summary = self.monitoring.get_metrics_summary()
        
        assert "timestamp" in summary
        assert "summary" in summary
        assert "performance" in summary
        assert "optimization" in summary
        assert "health" in summary
        
        # Check summary content
        assert summary["summary"]["total_requests_hour"] >= 1
        assert summary["summary"]["total_errors_hour"] >= 1
        assert "test" in summary["performance"]["request_counts"]
        assert "test" in summary["performance"]["error_counts"]
    
    def test_health_check(self):
        """Test health check functionality"""
        # Add some data to make checks meaningful
        for i in range(10):
            request_id = f"test_{i}"
            self.monitoring.start_request_timer(request_id, "test")
            time.sleep(0.01)
            self.monitoring.end_request_timer(request_id, 200)
        
        # Perform health check
        health = self.monitoring.perform_health_check()
        
        assert "status" in health
        assert "checks" in health
        assert "last_check" in health
        
        # Check individual health checks
        assert "response_time" in health["checks"]
        assert "error_rate" in health["checks"]
        assert "memory" in health["checks"]
        
        # All checks should be healthy with this small dataset
        for check in health["checks"].values():
            assert check["healthy"] is True
    
    def test_prometheus_export(self):
        """Test Prometheus metrics export"""
        # Add some test data
        self.monitoring.request_counts["test_endpoint"] = 100
        self.monitoring.response_times["test_endpoint"] = [100, 200, 150]
        
        # Export metrics
        prometheus_text = self.monitoring.export_metrics_prometheus()
        
        assert "sora_requests_total" in prometheus_text
        assert "sora_response_time_ms" in prometheus_text
        assert "test_endpoint" in prometheus_text
        assert "100" in prometheus_text  # Request count
    
    def test_performance_tracking_edge_cases(self):
        """Test edge cases in performance tracking"""
        # Test ending timer for non-existent request
        self.monitoring.end_request_timer("non_existent", 404)
        # Should not crash
        
        # Test multiple timers for same endpoint
        for i in range(5):
            request_id = f"batch_{i}"
            self.monitoring.start_request_timer(request_id, "batch_endpoint")
            time.sleep(0.01)
            self.monitoring.end_request_timer(request_id, 200)
        
        # Check that all requests were recorded
        batch_stats = [s for s in self.monitoring.performance_stats 
                      if s.endpoint == "batch_endpoint"]
        assert len(batch_stats) == 5
    
    def test_data_retention(self):
        """Test data retention limits"""
        # Fill up performance stats beyond limit
        for i in range(10005):  # More than maxlen
            stats = PerformanceStats(
                endpoint="test",
                response_time_ms=100.0,
                status_code=200,
                request_size_bytes=1000,
                response_size_bytes=2000,
                timestamp=datetime.now()
            )
            self.monitoring.performance_stats.append(stats)
        
        # Should not exceed maxlen
        assert len(self.monitoring.performance_stats) == 10000
    
    def test_thread_safety(self):
        """Test thread safety of monitoring operations"""
        import threading
        
        def worker():
            for i in range(100):
                self.monitoring.record_metric(f"test_{i}", float(i), MetricType.COUNTER)
                self.monitoring.record_usage("test", "basic", 10, "test", True)
        
        # Start multiple threads
        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Check that all operations completed
        assert len(self.monitoring.usage_stats) == 500  # 5 threads * 100 operations


class TestMonitoringIntegration:
    """Integration tests for monitoring features"""
    
    def test_configuration_integration(self):
        """Test monitoring configuration integration"""
        config = Config("testing")
        monitoring = MonitoringManager()
        
        # Test that monitoring respects configuration
        if not config.monitoring.enable_metrics:
            monitoring.record_metric("test", 1.0, MetricType.COUNTER)
            assert len(monitoring.metrics) == 0
    
    def test_real_time_metrics(self):
        """Test real-time metrics tracking"""
        monitoring = MonitoringManager()
        
        # Simulate real usage patterns
        endpoints = ["optimize", "enhance", "validate"]
        
        for endpoint in endpoints:
            for i in range(10):
                request_id = f"{endpoint}_{i}"
                monitoring.start_request_timer(request_id, endpoint)
                time.sleep(0.01)
                monitoring.end_request_timer(request_id, 200 if i < 8 else 500)
                
                monitoring.record_usage(
                    endpoint, 
                    "basic", 
                    100, 
                    endpoint, 
                    i < 8  # 80% success rate
                )
        
        # Get summary
        summary = monitoring.get_metrics_summary()
        
        # Verify real-time tracking
        assert len(summary["performance"]["request_counts"]) == 3
        for endpoint in endpoints:
            assert summary["performance"]["request_counts"][endpoint] == 10


if __name__ == "__main__":
    pytest.main([__file__])