"""
Example: Integrating Google Colab Learning Engine with Flask App
Shows practical examples of using the learning system
"""

from flask import Flask, request, jsonify, g
from src.colab_learning_connector import (
    get_learning_connector,
    with_learning,
    apply_learned_optimization,
    setup_learning_routes
)
from src.unified_optimizer import UnifiedOptimizer
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Setup learning routes
app = setup_learning_routes(app)

# Example 1: Basic optimization with learning
@app.route('/api/optimize-with-learning', methods=['POST'])
@with_learning  # Automatically records interactions
def optimize_with_learning():
    """Optimization that learns from each interaction"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    user_id = g.get('user_id', 'anonymous')
    
    # Try to apply learned optimization first
    learned = apply_learned_optimization(
        user_id=user_id,
        prompt=prompt,
        context={'endpoint': 'optimize', 'version': 'v2'}
    )
    
    if learned and learned['confidence'] > 0.75:
        # High confidence - use learned strategy
        logger.info(f"Using learned strategy with confidence {learned['confidence']}")
        
        # Apply learned parameters to optimizer
        optimizer = UnifiedOptimizer()
        result = optimizer.optimize(
            prompt,
            ai_profile={
                'enhancement_level': learned['parameters'].get('enhancement_level', 0.7),
                'creativity_boost': learned['parameters'].get('creativity_boost', 0.0)
            }
        )
        
        return jsonify({
            'success': True,
            'original': prompt,
            'optimized': result.optimized_prompt,
            'confidence': result.unified_confidence,
            'learning_applied': True,
            'learned_confidence': learned['confidence']
        })
    else:
        # Low confidence or no learning - use default
        optimizer = UnifiedOptimizer()
        result = optimizer.optimize(prompt)
        
        return jsonify({
            'success': True,
            'original': prompt,
            'optimized': result.optimized_prompt,
            'confidence': result.unified_confidence,
            'learning_applied': False
        })

# Example 2: Custom interaction recording
@app.route('/api/creative-transform', methods=['POST'])
def creative_transform():
    """Example of recording custom interactions"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    style = data.get('style', 'cinematic')
    user_id = g.get('user_id', 'anonymous')
    
    # Perform transformation
    # ... your transformation logic ...
    transformed = f"A {style} masterpiece: {prompt}"
    
    # Record the interaction for learning
    connector = get_learning_connector()
    success = connector.record_interaction(
        user_id=user_id,
        interaction_data={
            'input': prompt,
            'output': transformed,
            'type': f'style_transform_{style}',
            'success': True,
            'confidence': 0.88,
            'metadata': {
                'style': style,
                'complexity': len(prompt.split()),
                'user_segment': 'creative'
            }
        }
    )
    
    return jsonify({
        'success': True,
        'original': prompt,
        'transformed': transformed,
        'style': style,
        'learning_recorded': success
    })

# Example 3: Batch learning from historical data
@app.route('/api/learning/import-history', methods=['POST'])
def import_history():
    """Import historical interactions for learning"""
    data = request.get_json()
    interactions = data.get('interactions', [])
    
    connector = get_learning_connector()
    success_count = 0
    
    for interaction in interactions:
        success = connector.record_interaction(
            user_id=interaction.get('user_id', 'historical'),
            interaction_data={
                'input': interaction.get('input', ''),
                'output': interaction.get('output', ''),
                'type': interaction.get('type', 'historical'),
                'success': interaction.get('success', True),
                'confidence': interaction.get('confidence', 0.7),
                'metadata': {
                    'timestamp': interaction.get('timestamp'),
                    'source': 'historical_import'
                }
            }
        )
        if success:
            success_count += 1
    
    return jsonify({
        'success': True,
        'imported': success_count,
        'total': len(interactions)
    })

# Example 4: User-specific optimization with learning
@app.route('/api/personalized-optimize', methods=['POST'])
def personalized_optimize():
    """Optimization that adapts to user preferences"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    user_id = g.get('user_id', 'anonymous')
    
    # Get user learning insights
    connector = get_learning_connector()
    user_insights = connector.get_user_insights(user_id)
    
    if user_insights:
        # User has learning history
        skill_level = user_insights.get('skill_progression', {})
        pattern_count = user_insights.get('pattern_count', 0)
        
        # Adapt optimization based on user profile
        if skill_level.get('creative', 0) > 0.8:
            optimization_mode = 'creative_expert'
        elif skill_level.get('technical', 0) > 0.8:
            optimization_mode = 'technical_expert'
        else:
            optimization_mode = 'balanced'
        
        # Apply learned optimization
        learned = apply_learned_optimization(user_id, prompt)
        
        response = {
            'success': True,
            'optimization_mode': optimization_mode,
            'user_pattern_count': pattern_count,
            'personalized': True
        }
        
        if learned:
            response['learning_confidence'] = learned['confidence']
            response['learned_techniques'] = learned['techniques']
        
        return jsonify(response)
    else:
        # New user - use default optimization
        return jsonify({
            'success': True,
            'optimization_mode': 'default',
            'personalized': False,
            'message': 'Building your preference profile...'
        })

# Example 5: A/B testing with learning
@app.route('/api/ab-optimize', methods=['POST'])
def ab_optimize():
    """A/B test different strategies and learn from results"""
    import random
    
    data = request.get_json()
    prompt = data.get('prompt', '')
    user_id = g.get('user_id', 'anonymous')
    
    # Randomly assign strategy
    use_learning = random.random() > 0.5
    
    if use_learning:
        # Group A: Use learned optimization
        learned = apply_learned_optimization(user_id, prompt)
        strategy = 'learned' if learned else 'learned_fallback'
        confidence = learned['confidence'] if learned else 0.5
    else:
        # Group B: Use standard optimization
        strategy = 'standard'
        confidence = 0.7
    
    # ... perform optimization ...
    
    # Record the A/B test result
    connector = get_learning_connector()
    connector.record_interaction(
        user_id=user_id,
        interaction_data={
            'input': prompt,
            'output': f"Optimized: {prompt}",  # Your actual output
            'type': 'ab_test',
            'success': True,
            'confidence': confidence,
            'metadata': {
                'test_group': 'A' if use_learning else 'B',
                'strategy': strategy
            }
        }
    )
    
    return jsonify({
        'success': True,
        'test_group': 'A' if use_learning else 'B',
        'strategy': strategy
    })

# Example 6: Trigger pattern mining
@app.route('/api/learning/mine-patterns-now', methods=['POST'])
def mine_patterns_now():
    """Manually trigger pattern mining"""
    data = request.get_json()
    min_support = data.get('min_support', 0.1)
    
    connector = get_learning_connector()
    
    # Mine patterns
    results = connector.mine_patterns(min_support)
    
    if results:
        return jsonify({
            'success': True,
            'patterns_found': results.get('patterns_found', 0),
            'rules_extracted': results.get('rules_extracted', 0),
            'top_patterns': results.get('patterns', [])[:5],
            'top_rules': results.get('rules', [])[:3]
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Pattern mining failed or learning engine offline'
        })

# Example 7: Real-time learning dashboard
@app.route('/api/learning/dashboard')
def learning_dashboard():
    """Get comprehensive learning metrics"""
    connector = get_learning_connector()
    
    # Check if learning is available
    is_available = connector.is_available()
    
    if not is_available:
        return jsonify({
            'status': 'offline',
            'message': 'Learning engine not connected'
        })
    
    # Get various stats
    learning_stats = connector.get_learning_stats()
    
    # Get queue status
    queue_size = len(connector.learning_queue)
    cache_size = len(connector.cache)
    
    return jsonify({
        'status': 'online',
        'engine_stats': learning_stats,
        'connector_stats': {
            'queue_size': queue_size,
            'cache_size': cache_size,
            'cache_ttl': connector.config.cache_ttl
        },
        'performance': {
            'gpu_enabled': learning_stats.get('gpu_enabled', False),
            'total_patterns': learning_stats.get('total_patterns', 0),
            'active_users': learning_stats.get('total_users', 0)
        }
    })

# Example 8: Export learning data
@app.route('/api/learning/export', methods=['GET'])
def export_learning_data():
    """Export learning insights for analysis"""
    user_id = request.args.get('user_id')
    
    connector = get_learning_connector()
    
    if user_id:
        # Export specific user data
        insights = connector.get_user_insights(user_id)
        if insights:
            return jsonify({
                'export_type': 'user',
                'user_id': user_id,
                'data': insights
            })
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        # Export global stats
        stats = connector.get_learning_stats()
        return jsonify({
            'export_type': 'global',
            'data': stats
        })

if __name__ == '__main__':
    # Check if learning engine is configured
    connector = get_learning_connector()
    if connector.config.colab_api_url:
        print(f"✅ Learning engine configured: {connector.config.colab_api_url}")
        if connector.is_available():
            print("✅ Learning engine is online!")
        else:
            print("❌ Learning engine is offline")
    else:
        print("⚠️  No COLAB_LEARNING_URL configured")
    
    app.run(debug=True, port=5001)