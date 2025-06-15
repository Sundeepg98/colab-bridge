"""
Connector for Google Colab Learning Engine
Integrates the GPU-accelerated learning system with the Flask application
"""

import requests
import json
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from dataclasses import dataclass
from functools import wraps
import os

logger = logging.getLogger(__name__)

@dataclass
class LearningConfig:
    """Configuration for Colab learning integration"""
    colab_api_url: str = os.getenv('COLAB_LEARNING_URL', '')
    api_timeout: int = 2
    batch_size: int = 10
    enable_async: bool = True
    cache_ttl: int = 300  # 5 minutes

class ColabLearningConnector:
    """Connects Flask app to Google Colab learning engine"""
    
    def __init__(self, config: Optional[LearningConfig] = None):
        self.config = config or LearningConfig()
        self.learning_queue = []
        self.cache = {}
        self._session = None
        
    @property
    def session(self):
        """Lazy-loaded requests session"""
        if self._session is None:
            self._session = requests.Session()
        return self._session
    
    def is_available(self) -> bool:
        """Check if Colab learning engine is available"""
        if not self.config.colab_api_url:
            return False
            
        try:
            response = self.session.get(
                f"{self.config.colab_api_url}/",
                timeout=1
            )
            return response.status_code == 200
        except:
            return False
    
    def record_interaction(self, user_id: str, interaction_data: Dict[str, Any]) -> bool:
        """Record a learning interaction"""
        if not self.config.colab_api_url:
            return False
            
        try:
            # Add to queue for batch processing
            if self.config.enable_async:
                self.learning_queue.append({
                    'user_id': user_id,
                    'data': interaction_data,
                    'timestamp': datetime.now()
                })
                
                # Process batch if queue is full
                if len(self.learning_queue) >= self.config.batch_size:
                    self._process_batch()
                
                return True
            else:
                # Synchronous processing
                return self._send_interaction(user_id, interaction_data)
                
        except Exception as e:
            logger.error(f"Failed to record interaction: {e}")
            return False
    
    def _send_interaction(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Send single interaction to learning engine"""
        try:
            payload = {
                "user_id": user_id,
                "input_prompt": data.get('input', ''),
                "output_prompt": data.get('output', ''),
                "interaction_type": data.get('type', 'general'),
                "success": data.get('success', True),
                "confidence": data.get('confidence', 0.8),
                "metadata": data.get('metadata', {})
            }
            
            response = self.session.post(
                f"{self.config.colab_api_url}/learn",
                json=payload,
                timeout=self.config.api_timeout
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.debug(f"Learning API error: {e}")
            return False
    
    def _process_batch(self):
        """Process queued interactions in batch"""
        if not self.learning_queue:
            return
            
        batch = self.learning_queue[:self.config.batch_size]
        self.learning_queue = self.learning_queue[self.config.batch_size:]
        
        # Send batch asynchronously
        for item in batch:
            try:
                self._send_interaction(item['user_id'], item['data'])
            except:
                pass  # Don't break batch processing
    
    def get_adaptation(self, user_id: str, prompt: str, context: Optional[Dict] = None) -> Optional[Dict]:
        """Get adapted optimization strategy from learning engine"""
        if not self.config.colab_api_url:
            return None
            
        # Check cache
        cache_key = f"{user_id}:{hash(prompt)}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.config.cache_ttl:
                return cached_data
        
        try:
            payload = {
                "user_id": user_id,
                "prompt": prompt,
                "context": context or {}
            }
            
            response = self.session.post(
                f"{self.config.colab_api_url}/adapt",
                json=payload,
                timeout=self.config.api_timeout
            )
            
            if response.status_code == 200:
                adaptation = response.json().get('adaptation')
                # Cache result
                self.cache[cache_key] = (adaptation, datetime.now())
                return adaptation
                
        except Exception as e:
            logger.debug(f"Adaptation API error: {e}")
            
        return None
    
    def get_user_insights(self, user_id: str) -> Optional[Dict]:
        """Get user learning profile insights"""
        if not self.config.colab_api_url:
            return None
            
        try:
            response = self.session.get(
                f"{self.config.colab_api_url}/user-profile/{user_id}",
                timeout=self.config.api_timeout
            )
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            logger.debug(f"User insights API error: {e}")
            
        return None
    
    def get_learning_stats(self) -> Optional[Dict]:
        """Get overall learning statistics"""
        if not self.config.colab_api_url:
            return None
            
        try:
            response = self.session.get(
                f"{self.config.colab_api_url}/learning-stats",
                timeout=self.config.api_timeout
            )
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            logger.debug(f"Learning stats API error: {e}")
            
        return None
    
    def mine_patterns(self, min_support: float = 0.1) -> Optional[Dict]:
        """Trigger pattern mining on learning engine"""
        if not self.config.colab_api_url:
            return None
            
        try:
            response = self.session.post(
                f"{self.config.colab_api_url}/mine-patterns",
                json={"min_support": min_support},
                timeout=self.config.api_timeout * 2  # Pattern mining may take longer
            )
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            logger.debug(f"Pattern mining API error: {e}")
            
        return None

# Singleton instance
_connector_instance = None

def get_learning_connector() -> ColabLearningConnector:
    """Get singleton learning connector instance"""
    global _connector_instance
    if _connector_instance is None:
        _connector_instance = ColabLearningConnector()
    return _connector_instance

def with_learning(f):
    """Decorator to add learning capability to Flask endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, g
        
        # Execute original function
        result = f(*args, **kwargs)
        
        # Extract learning data if successful
        try:
            if hasattr(result, 'get_json'):
                response_data = result.get_json()
                if response_data and response_data.get('success'):
                    connector = get_learning_connector()
                    
                    # Get request data
                    request_data = request.get_json() or {}
                    
                    # Prepare learning data
                    learning_data = {
                        'input': request_data.get('prompt', ''),
                        'output': response_data.get('optimized', response_data.get('prompt', '')),
                        'type': request_data.get('type', 'optimization'),
                        'success': True,
                        'confidence': response_data.get('confidence', 0.8),
                        'metadata': {
                            'endpoint': request.endpoint,
                            'method': request.method,
                            'processing_time': response_data.get('processing_time', 0)
                        }
                    }
                    
                    # Record interaction
                    user_id = g.get('user_id', 'anonymous')
                    connector.record_interaction(user_id, learning_data)
                    
        except Exception as e:
            logger.debug(f"Learning decorator error: {e}")
            
        return result
    return decorated_function

def apply_learned_optimization(user_id: str, prompt: str, context: Optional[Dict] = None) -> Optional[Dict]:
    """Apply learned optimization strategies to a prompt"""
    connector = get_learning_connector()
    
    # Get adaptation from learning engine
    adaptation = connector.get_adaptation(user_id, prompt, context)
    
    if adaptation and adaptation.get('success_probability', 0) > 0.7:
        return {
            'strategy': adaptation.get('adapted_strategy', {}),
            'confidence': adaptation.get('confidence', 0.5),
            'techniques': adaptation.get('adapted_strategy', {}).get('techniques', []),
            'parameters': adaptation.get('adapted_strategy', {}).get('parameters', {})
        }
    
    return None

# Integration helpers for Flask app
def setup_learning_routes(app):
    """Add learning-specific routes to Flask app"""
    
    @app.route('/api/learning/status')
    def learning_status():
        """Check learning engine status"""
        connector = get_learning_connector()
        return {
            'available': connector.is_available(),
            'api_url': bool(connector.config.colab_api_url),
            'queue_size': len(connector.learning_queue),
            'cache_size': len(connector.cache)
        }
    
    @app.route('/api/learning/stats')
    def learning_stats():
        """Get learning statistics"""
        connector = get_learning_connector()
        stats = connector.get_learning_stats()
        return stats or {'error': 'Learning engine not available'}
    
    @app.route('/api/learning/user/<user_id>')
    def user_learning_profile(user_id):
        """Get user learning insights"""
        connector = get_learning_connector()
        insights = connector.get_user_insights(user_id)
        return insights or {'error': 'User profile not found'}
    
    @app.route('/api/learning/mine-patterns', methods=['POST'])
    def mine_patterns():
        """Trigger pattern mining"""
        from flask import request
        data = request.get_json() or {}
        min_support = data.get('min_support', 0.1)
        
        connector = get_learning_connector()
        results = connector.mine_patterns(min_support)
        return results or {'error': 'Pattern mining failed'}
    
    return app