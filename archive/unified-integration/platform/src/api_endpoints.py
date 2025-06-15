"""
Flask API endpoints for admin dashboard and integration management
"""

from flask import jsonify, request, g
import logging
from datetime import datetime
from typing import Dict, Any

from .api_key_manager import get_api_key_manager
from .auto_maintenance_engine import get_maintenance_engine, MaintenanceAction
from .integration_manager import get_integration_manager
try:
    from .telemetry_analysis_engine import get_telemetry_analyzer
except ImportError:
    from .simple_telemetry_analyzer import get_telemetry_analyzer

logger = logging.getLogger(__name__)

# Import new dynamic framework components
import sys
import os
sys.path.append('/var/projects/ai-integration-platform/src')

try:
    from unified_integration_manager import get_unified_manager
    from dynamic_integration_framework import get_dynamic_framework
    from integration_health_monitor import get_health_monitor
    from cost_optimization_engine import get_cost_optimization_engine
    from fallback_system import get_fallback_manager
    from service_discovery import get_service_discovery
    from independent_core_capabilities import get_independent_core, CoreCapability
    DYNAMIC_FRAMEWORK_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Dynamic framework components not available: {e}")
    DYNAMIC_FRAMEWORK_AVAILABLE = False


def register_admin_endpoints(app):
    """Register all admin dashboard endpoints"""
    
    # API Key Management Endpoints
    @app.route('/api/api-keys', methods=['GET'])
    def get_api_keys():
        """Get all API keys (without exposing actual keys)"""
        try:
            api_key_manager = get_api_key_manager()
            keys = api_key_manager.get_all_keys_info()
            
            return jsonify({
                'success': True,
                'keys': keys
            })
        except Exception as e:
            logger.error(f"Failed to get API keys: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/api-keys', methods=['POST'])
    def add_api_key():
        """Add or update an API key"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No data provided'
                }), 400
            
            integration_name = data.get('integration_name')
            api_key = data.get('api_key')
            
            if not integration_name or not api_key:
                return jsonify({
                    'success': False,
                    'error': 'integration_name and api_key are required'
                }), 400
            
            # Prepare key data
            key_data = {
                'api_key': api_key,
                'base_url': data.get('base_url'),
                'models': data.get('models', []),
                'enabled': data.get('enabled', True),
                'metadata': data.get('metadata', {})
            }
            
            api_key_manager = get_api_key_manager()
            result = api_key_manager.add_or_update_key(integration_name, key_data)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Failed to add API key: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/api-keys/<integration>/test', methods=['POST'])
    def test_api_key(integration):
        """Test an API key"""
        try:
            api_key_manager = get_api_key_manager()
            validation_result = api_key_manager.validate_key(integration)
            
            return jsonify({
                'success': True,
                'validation': validation_result
            })
            
        except Exception as e:
            logger.error(f"Failed to test API key: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/api-keys/<integration>/toggle', methods=['POST'])
    def toggle_api_key(integration):
        """Enable or disable an API key"""
        try:
            data = request.get_json() or {}
            enabled = data.get('enabled', True)
            
            api_key_manager = get_api_key_manager()
            result = api_key_manager.enable_disable_key(integration, enabled)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Failed to toggle API key: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/api-keys/<integration>', methods=['DELETE'])
    def delete_api_key(integration):
        """Delete an API key"""
        try:
            api_key_manager = get_api_key_manager()
            result = api_key_manager.remove_key(integration)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Failed to delete API key: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Maintenance Engine Endpoints
    @app.route('/api/system-health', methods=['GET'])
    def get_system_health():
        """Get overall system health"""
        try:
            maintenance_engine = get_maintenance_engine()
            health = maintenance_engine.get_system_health()
            
            return jsonify({
                'success': True,
                'health': health
            })
            
        except Exception as e:
            logger.error(f"Failed to get system health: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/maintenance-status', methods=['GET'])
    def get_maintenance_status():
        """Get recent maintenance events"""
        try:
            maintenance_engine = get_maintenance_engine()
            
            # Get recent events from history
            recent_events = []
            for event in maintenance_engine.maintenance_history[-20:]:  # Last 20 events
                recent_events.append({
                    'timestamp': event.timestamp.isoformat(),
                    'action': event.action.value,
                    'target': event.target,
                    'status': event.status,
                    'duration': event.duration,
                    'automated': event.automated
                })
            
            return jsonify({
                'success': True,
                'recent_events': recent_events
            })
            
        except Exception as e:
            logger.error(f"Failed to get maintenance status: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/maintenance/trigger', methods=['POST'])
    def trigger_maintenance():
        """Manually trigger a maintenance action"""
        try:
            data = request.get_json() or {}
            action_str = data.get('action')
            target = data.get('target', 'system')
            
            if not action_str:
                return jsonify({
                    'success': False,
                    'error': 'action is required'
                }), 400
            
            # Convert string to enum
            try:
                action = MaintenanceAction(action_str)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': f'Invalid action: {action_str}'
                }), 400
            
            maintenance_engine = get_maintenance_engine()
            result = maintenance_engine.trigger_maintenance(action, target)
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Failed to trigger maintenance: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/maintenance/toggle', methods=['POST'])
    def toggle_maintenance():
        """Enable or disable auto-maintenance"""
        try:
            data = request.get_json() or {}
            enabled = data.get('enabled', True)
            
            maintenance_engine = get_maintenance_engine()
            
            if enabled and not maintenance_engine.running:
                maintenance_engine.start()
            elif not enabled and maintenance_engine.running:
                maintenance_engine.stop()
            
            return jsonify({
                'success': True,
                'enabled': enabled
            })
            
        except Exception as e:
            logger.error(f"Failed to toggle maintenance: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/maintenance-report', methods=['GET'])
    def get_maintenance_report():
        """Get detailed maintenance report"""
        try:
            hours = int(request.args.get('hours', 24))
            
            maintenance_engine = get_maintenance_engine()
            report = maintenance_engine.get_maintenance_report(hours)
            
            return jsonify({
                'success': True,
                'report': report
            })
            
        except Exception as e:
            logger.error(f"Failed to get maintenance report: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Telemetry Endpoints
    @app.route('/api/telemetry-export', methods=['GET'])
    def export_telemetry():
        """Export telemetry data"""
        try:
            hours = int(request.args.get('hours', 24))
            
            maintenance_engine = get_maintenance_engine()
            export_data = maintenance_engine.telemetry.export_telemetry(hours)
            
            return jsonify({
                'success': True,
                'telemetry': export_data
            })
            
        except Exception as e:
            logger.error(f"Failed to export telemetry: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/telemetry-export', methods=['POST'])
    def download_telemetry():
        """Download telemetry data as file"""
        try:
            from flask import make_response
            import json
            
            hours = int(request.get_json().get('hours', 24))
            
            maintenance_engine = get_maintenance_engine()
            export_data = maintenance_engine.telemetry.export_telemetry(hours)
            
            # Create response with file download
            response = make_response(json.dumps(export_data, indent=2))
            response.headers['Content-Type'] = 'application/json'
            response.headers['Content-Disposition'] = f'attachment; filename=telemetry_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to download telemetry: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Integration Test Endpoints
    @app.route('/api/integration-test-all', methods=['POST'])
    def test_all_integrations():
        """Test all configured integrations"""
        try:
            api_key_manager = get_api_key_manager()
            integration_manager = get_integration_manager()
            
            results = {}
            
            # Get all configured keys
            keys_info = api_key_manager.get_all_keys_info()
            
            for integration_name in keys_info:
                # Test the key
                validation = api_key_manager.validate_key(integration_name)
                
                # Update integration status
                if validation['valid']:
                    integration_manager.update_integration_status(integration_name, 'healthy')
                else:
                    integration_manager.update_integration_status(integration_name, 'error')
                
                results[integration_name] = validation
            
            return jsonify({
                'success': True,
                'results': results
            })
            
        except Exception as e:
            logger.error(f"Failed to test all integrations: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Notification Subscription Endpoint
    @app.route('/api/notifications/subscribe', methods=['POST'])
    def subscribe_notifications():
        """Subscribe to real-time notifications (WebSocket endpoint placeholder)"""
        return jsonify({
            'success': True,
            'message': 'WebSocket endpoint for real-time notifications',
            'websocket_url': '/ws/notifications'
        })
    
    return app


def register_enhanced_admin_endpoints(app):
    """Register the enhanced admin dashboard route"""
    
    @app.route('/admin-enhanced')
    def admin_dashboard_enhanced():
        """Enhanced admin dashboard with API key management"""
        from flask import render_template
        return render_template('admin_dashboard_enhanced.html')
    
    @app.route('/telemetry-dashboard')
    def telemetry_dashboard():
        """Telemetry analytics dashboard"""
        from flask import render_template
        return render_template('telemetry_dashboard.html')
    
    @app.route('/integration-quickstart')
    def integration_quickstart():
        """Serve the quick integration setup page"""
        from flask import render_template
        return render_template('integration_quickstart.html')
    
    return app


def register_telemetry_endpoints(app):
    """Register telemetry analysis endpoints"""
    
    @app.route('/api/telemetry-analyze', methods=['POST'])
    def analyze_telemetry():
        """Analyze telemetry data and generate insights"""
        try:
            data = request.get_json() or {}
            telemetry_data = data.get('telemetry_data', {})
            
            if not telemetry_data:
                # Get from maintenance engine if not provided
                maintenance_engine = get_maintenance_engine()
                telemetry_data = maintenance_engine.telemetry.export_telemetry(24)
            
            analyzer = get_telemetry_analyzer()
            analysis_results = analyzer.analyze_telemetry_data(telemetry_data)
            
            return jsonify({
                'success': True,
                'analysis': analysis_results
            })
            
        except Exception as e:
            logger.error(f"Failed to analyze telemetry: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/telemetry-visualize', methods=['POST'])
    def visualize_telemetry():
        """Generate visualizations from telemetry analysis"""
        try:
            data = request.get_json() or {}
            analysis_results = data.get('analysis_results')
            
            if not analysis_results:
                return jsonify({
                    'success': False,
                    'error': 'No analysis results provided'
                }), 400
            
            analyzer = get_telemetry_analyzer()
            output_dir = analyzer.visualize_insights(analysis_results)
            
            return jsonify({
                'success': True,
                'visualization_path': str(output_dir)
            })
            
        except Exception as e:
            logger.error(f"Failed to visualize telemetry: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/telemetry-export-report', methods=['POST'])
    def export_telemetry_report():
        """Export telemetry analysis report"""
        try:
            data = request.get_json() or {}
            analysis_results = data.get('analysis')
            format_type = data.get('format', 'json')
            
            if not analysis_results:
                return jsonify({
                    'success': False,
                    'error': 'No analysis results provided'
                }), 400
            
            analyzer = get_telemetry_analyzer()
            report_path = analyzer.export_report(analysis_results, format_type)
            
            if format_type == 'json':
                # Return file for download
                from flask import send_file
                return send_file(report_path, as_attachment=True)
            else:
                return jsonify({
                    'success': True,
                    'report_path': report_path
                })
            
        except Exception as e:
            logger.error(f"Failed to export telemetry report: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/telemetry-insights', methods=['GET'])
    def get_telemetry_insights():
        """Get historical telemetry insights"""
        try:
            limit = int(request.args.get('limit', 50))
            severity = request.args.get('severity')
            insight_type = request.args.get('type')
            
            analyzer = get_telemetry_analyzer()
            
            # Filter insights
            insights = analyzer.insights[-limit:]
            
            if severity:
                insights = [i for i in insights if i.severity == severity]
            
            if insight_type:
                insights = [i for i in insights if i.insight_type == insight_type]
            
            # Convert to JSON format
            insights_data = []
            for insight in insights:
                insights_data.append({
                    'type': insight.insight_type,
                    'title': insight.title,
                    'description': insight.description,
                    'severity': insight.severity,
                    'metrics': insight.metrics,
                    'recommendations': insight.recommendations,
                    'confidence': insight.confidence,
                    'impact_score': insight.impact_score,
                    'discovered_at': insight.discovered_at.isoformat()
                })
            
            return jsonify({
                'success': True,
                'insights': insights_data,
                'total_count': len(analyzer.insights)
            })
            
        except Exception as e:
            logger.error(f"Failed to get telemetry insights: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    return app


def register_dynamic_framework_endpoints(app):
    """Register dynamic framework endpoints"""
    
    if not DYNAMIC_FRAMEWORK_AVAILABLE:
        logger.warning("Dynamic framework not available, skipping endpoint registration")
        return app
    
    # Unified System Status
    @app.route('/api/unified-system-status', methods=['GET'])
    def get_unified_system_status():
        """Get comprehensive system status from unified manager"""
        try:
            # Initialize in a thread-safe way
            import threading
            import time
            
            system_status = None
            exception_caught = None
            
            def init_and_get_status():
                nonlocal system_status, exception_caught
                try:
                    unified_manager = get_unified_manager()
                    system_status = unified_manager.get_system_status()
                except Exception as e:
                    exception_caught = e
            
            # Run in separate thread to avoid event loop issues
            thread = threading.Thread(target=init_and_get_status)
            thread.start()
            thread.join(timeout=10)  # 10 second timeout
            
            if exception_caught:
                raise exception_caught
            
            if system_status is None:
                raise Exception("Timeout getting system status")
            
            return jsonify({
                'success': True,
                'system_status': system_status
            })
        except Exception as e:
            logger.error(f"Failed to get unified system status: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # System Recommendations
    @app.route('/api/system-recommendations', methods=['GET'])
    def get_system_recommendations():
        """Get system-wide recommendations"""
        try:
            unified_manager = get_unified_manager()
            recommendations = unified_manager.get_recommendations()
            
            return jsonify({
                'success': True,
                'recommendations': recommendations
            })
        except Exception as e:
            logger.error(f"Failed to get system recommendations: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # System Optimization
    @app.route('/api/optimize-system', methods=['POST'])
    def optimize_system():
        """Run system-wide optimization"""
        try:
            import asyncio
            unified_manager = get_unified_manager()
            
            # Run optimization
            optimization_results = asyncio.run(unified_manager.optimize_system())
            
            return jsonify({
                'success': True,
                'optimization_results': optimization_results
            })
        except Exception as e:
            logger.error(f"Failed to optimize system: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Service Discovery Endpoints
    @app.route('/api/service-discovery-status', methods=['GET'])
    def get_service_discovery_status():
        """Get service discovery status"""
        try:
            service_discovery = get_service_discovery()
            discovery_status = service_discovery.get_discovery_status()
            
            return jsonify({
                'success': True,
                'discovery_status': discovery_status
            })
        except Exception as e:
            logger.error(f"Failed to get service discovery status: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/run-service-discovery', methods=['POST'])
    def run_service_discovery():
        """Run service discovery"""
        try:
            import asyncio
            service_discovery = get_service_discovery()
            
            # Run discovery
            results = asyncio.run(service_discovery.run_discovery_cycle())
            
            return jsonify({
                'success': True,
                'discovered_count': len(results),
                'results': results
            })
        except Exception as e:
            logger.error(f"Failed to run service discovery: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Fallback System Endpoints
    @app.route('/api/fallback-system-status', methods=['GET'])
    def get_fallback_system_status():
        """Get fallback system status"""
        try:
            fallback_manager = get_fallback_manager()
            fallback_status = fallback_manager.get_system_status()
            
            return jsonify({
                'success': True,
                'fallback_status': fallback_status
            })
        except Exception as e:
            logger.error(f"Failed to get fallback system status: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/test-fallback-system', methods=['POST'])
    def test_fallback_system():
        """Test fallback system"""
        try:
            fallback_manager = get_fallback_manager()
            
            # Run fallback tests
            test_results = {
                'total_tests': 0,
                'tests_passed': 0,
                'test_details': []
            }
            
            # Test each route
            for capability, route in fallback_manager.routes.items():
                test_results['total_tests'] += 1
                try:
                    # Simple route validation test
                    if route.primary_service and route.fallback_services:
                        test_results['tests_passed'] += 1
                        test_results['test_details'].append({
                            'capability': capability,
                            'status': 'passed',
                            'message': 'Route configuration valid'
                        })
                    else:
                        test_results['test_details'].append({
                            'capability': capability,
                            'status': 'failed',
                            'message': 'Invalid route configuration'
                        })
                except Exception as e:
                    test_results['test_details'].append({
                        'capability': capability,
                        'status': 'error',
                        'message': str(e)
                    })
            
            return jsonify({
                'success': True,
                **test_results
            })
        except Exception as e:
            logger.error(f"Failed to test fallback system: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Independent Core Endpoints
    @app.route('/api/independent-core-status', methods=['GET'])
    def get_independent_core_status():
        """Get independent core status"""
        try:
            independent_core = get_independent_core()
            core_status = independent_core.get_usage_stats()
            
            return jsonify({
                'success': True,
                'core_status': core_status
            })
        except Exception as e:
            logger.error(f"Failed to get independent core status: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/test-independent-core', methods=['POST'])
    def test_independent_core():
        """Test independent core capabilities"""
        try:
            independent_core = get_independent_core()
            health_check = independent_core.health_check()
            
            return jsonify({
                'success': True,
                **health_check
            })
        except Exception as e:
            logger.error(f"Failed to test independent core: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/test-core-capability', methods=['POST'])
    def test_core_capability():
        """Test specific core capability"""
        try:
            data = request.get_json()
            capability_name = data.get('capability')
            
            if not capability_name:
                return jsonify({
                    'success': False,
                    'error': 'Capability name required'
                }), 400
            
            independent_core = get_independent_core()
            
            # Map capability name to enum
            capability_mapping = {
                'text_processing': CoreCapability.TEXT_PROCESSING,
                'text_generation': CoreCapability.TEXT_GENERATION,
                'prompt_optimization': CoreCapability.PROMPT_OPTIMIZATION,
                'data_analysis': CoreCapability.DATA_ANALYSIS,
                'mock_generation': CoreCapability.MOCK_GENERATION
            }
            
            capability = capability_mapping.get(capability_name)
            if not capability:
                return jsonify({
                    'success': False,
                    'error': f'Unknown capability: {capability_name}'
                }), 400
            
            # Get test data for the capability
            test_data = independent_core._get_test_data(capability)
            
            # Run the test
            result = independent_core.process_request(capability, test_data)
            
            return jsonify({
                'success': result.success,
                'processing_time': result.processing_time,
                'capability_used': result.capability_used.value,
                'error': result.error
            })
            
        except Exception as e:
            logger.error(f"Failed to test core capability: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    return app