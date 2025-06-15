"""
Flask routes for direct Colab API integration
"""

import asyncio
from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

from .colab_api_connector import get_colab_connector, initialize_colab_api

logger = logging.getLogger(__name__)

# Create blueprint for Colab API routes
colab_api_bp = Blueprint('colab_api', __name__)

def run_async(coro):
    """Helper to run async functions in Flask"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

@colab_api_bp.route('/api/colab-direct/status', methods=['GET'])
def get_direct_colab_status():
    """Get direct Colab API connection status"""
    try:
        connector = get_colab_connector()
        status = run_async(connector.get_system_status())
        
        return jsonify({
            'success': True,
            'status': status,
            'connection_type': 'direct_api',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'connection_type': 'direct_api'
        })

@colab_api_bp.route('/api/colab-direct/health', methods=['GET'])
def check_direct_colab_health():
    """Health check for direct Colab connection"""
    try:
        connector = get_colab_connector()
        health = run_async(connector.health_check())
        
        return jsonify({
            'success': True,
            'health': health,
            'connection_method': 'api_credentials'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@colab_api_bp.route('/api/colab-direct/generate-text', methods=['POST'])
def generate_text_direct():
    """Generate text using direct Colab API"""
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt', '')
        style = data.get('style', 'creative')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt is required'
            })
        
        connector = get_colab_connector()
        result = run_async(connector.generate_text(prompt, style))
        
        return jsonify({
            'success': True,
            'result': result,
            'method': 'direct_api',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'method': 'direct_api'
        })

@colab_api_bp.route('/api/colab-direct/generate-image', methods=['POST'])
def generate_image_direct():
    """Generate image using direct Colab API"""
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt', '')
        style = data.get('style', 'photorealistic')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt is required'
            })
        
        connector = get_colab_connector()
        result = run_async(connector.generate_image(prompt, style))
        
        return jsonify({
            'success': True,
            'result': result,
            'method': 'direct_api',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'method': 'direct_api'
        })

@colab_api_bp.route('/api/colab-direct/execute-code', methods=['POST'])
def execute_code_direct():
    """Execute custom code on Colab runtime"""
    try:
        data = request.get_json() or {}
        code = data.get('code', '')
        timeout = data.get('timeout', 30)
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Code is required'
            })
        
        connector = get_colab_connector()
        result = run_async(connector.execute_code(code, timeout))
        
        return jsonify({
            'success': True,
            'execution_result': result,
            'method': 'direct_api',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'method': 'direct_api'
        })

@colab_api_bp.route('/api/colab-direct/initialize', methods=['POST'])
def initialize_direct_connection():
    """Initialize direct Colab API connection"""
    try:
        success = run_async(initialize_colab_api())
        
        if success:
            connector = get_colab_connector()
            status = run_async(connector.get_system_status())
            
            return jsonify({
                'success': True,
                'message': 'Colab API connection initialized successfully',
                'status': status,
                'connection_type': 'direct_api'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to initialize Colab API connection',
                'running_in': 'simulation_mode'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Enhanced optimization endpoint using direct Colab
@colab_api_bp.route('/api/optimize-with-colab-direct', methods=['POST'])
def optimize_with_colab_direct():
    """Optimize prompts using direct Colab API connection"""
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt', '')
        optimization_type = data.get('type', 'enhance')
        style = data.get('style', 'creative')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt is required'
            })
        
        connector = get_colab_connector()
        
        # Use Colab for text enhancement
        if optimization_type in ['enhance', 'creative', 'artistic']:
            result = run_async(connector.generate_text(prompt, style))
            
            return jsonify({
                'success': True,
                'original': prompt,
                'optimized': result.get('enhanced_text', prompt),
                'processing_time': result.get('processing_time', 0),
                'gpu_used': result.get('gpu_used', False),
                'method': 'colab_direct_api',
                'style': style,
                'confidence': 0.9 if result.get('gpu_used') else 0.7
            })
        
        # For other types, use standard optimization with Colab analysis
        else:
            # Get Colab analysis first
            analysis_code = f"""
# Analyze prompt for optimization strategy
prompt = "{prompt}"
analysis = {{
    'complexity': len(prompt.split()) / 10,
    'theme': 'artistic' if any(word in prompt.lower() for word in ['art', 'paint', 'draw']) else 'general',
    'recommended_strategy': 'creative' if 'creative' in prompt.lower() else 'standard'
}}
print(f"ANALYSIS|{{analysis}}")
"""
            
            analysis_result = run_async(connector.execute_code(analysis_code))
            
            # Apply basic optimization with Colab insights
            optimized = f"A beautifully crafted {style} scene: {prompt}"
            
            return jsonify({
                'success': True,
                'original': prompt,
                'optimized': optimized,
                'method': 'colab_assisted_optimization',
                'analysis': analysis_result.get('output', ''),
                'confidence': 0.85
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'method': 'colab_direct_api'
        })

def register_colab_api_routes(app):
    """Register Colab API routes with Flask app"""
    app.register_blueprint(colab_api_bp)
    
    # Initialize connection on startup
    with app.app_context():
        try:
            run_async(initialize_colab_api())
            app.logger.info("✅ Colab Direct API initialized")
        except Exception as e:
            app.logger.warning(f"⚠️ Colab Direct API initialization failed: {e}")
    
    return app