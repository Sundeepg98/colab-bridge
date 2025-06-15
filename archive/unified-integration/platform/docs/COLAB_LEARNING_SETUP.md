# 🧠 Google Colab Learning Engine Setup Guide

This guide helps you set up and integrate the GPU-accelerated learning engine with your AI platform.

## 📋 Overview

The learning engine uses Google Colab's free GPU/TPU resources to:
- Learn from user interactions in real-time
- Mine patterns from usage data
- Adapt optimization strategies per user
- Improve success rates over time

## 🚀 Quick Start

### 1. Open the Colab Notebook

1. Go to [Google Colab](https://colab.research.google.com)
2. File → Upload notebook
3. Upload `/colab_notebooks/engine_learning_improvement.ipynb`
4. Runtime → Change runtime type → GPU

### 2. Run Initial Setup

Run cells 1-4 in order:
- Environment setup (GPU check)
- Dependencies installation
- Learning engine initialization
- Pattern mining setup

### 3. Start the API Server

Run the API deployment cell:
```python
# This will start the server and create an ngrok tunnel
run_api_server()
```

You'll get a public URL like: `https://xxxxx.ngrok.io`

### 4. Configure Your Flask App

Add to your `.env`:
```bash
COLAB_LEARNING_URL=https://xxxxx.ngrok.io
```

Update your `app.py`:
```python
from src.colab_learning_connector import (
    setup_learning_routes, 
    with_learning,
    apply_learned_optimization
)

# Add learning routes
app = setup_learning_routes(app)

# Add learning to existing endpoints
@app.route('/api/optimize', methods=['POST'])
@with_learning  # Add this decorator
def optimize_prompt():
    # Your existing code
    pass
```

## 📊 Features

### 1. Automatic Learning

The system automatically learns from:
- Successful optimizations
- User preferences
- Rejection patterns
- Style choices

### 2. Pattern Mining

Discovers patterns across users:
- Common optimization strategies
- Successful transformations
- User segment behaviors

### 3. Real-time Adaptation

Adapts strategies based on:
- User history
- Similar patterns
- Success predictions
- Context awareness

### 4. GPU Acceleration

Leverages Colab's GPU for:
- Fast embedding generation
- Neural pattern matching
- Real-time predictions
- Batch processing

## 🔧 Integration Examples

### Basic Integration

```python
from src.colab_learning_connector import get_learning_connector

# Check if learning is available
connector = get_learning_connector()
if connector.is_available():
    print("✅ Learning engine connected")
```

### Apply Learned Optimizations

```python
# In your optimization endpoint
def optimize_with_learning(user_id, prompt):
    # Try to get learned optimization
    learned = apply_learned_optimization(user_id, prompt)
    
    if learned:
        # Use learned strategy
        strategy = learned['strategy']
        techniques = learned['techniques']
        # Apply to your optimization logic
    else:
        # Fallback to default
        pass
```

### Record Custom Interactions

```python
# Record any interaction for learning
connector.record_interaction(
    user_id="user123",
    interaction_data={
        'input': original_prompt,
        'output': optimized_prompt,
        'type': 'creative_enhancement',
        'success': True,
        'confidence': 0.92
    }
)
```

## 📈 Monitoring

### Check Learning Stats

Visit: `http://localhost:5000/api/learning/stats`

```json
{
    "total_users": 150,
    "total_patterns": 3420,
    "mined_pattern_groups": 28,
    "gpu_enabled": true,
    "device": "cuda"
}
```

### User Learning Profile

Visit: `http://localhost:5000/api/learning/user/user123`

```json
{
    "pattern_count": 45,
    "skill_progression": {
        "creative": 0.85,
        "technical": 0.72,
        "safety": 0.94
    },
    "has_personalization": true
}
```

## 🎯 Best Practices

### 1. Regular Pattern Mining

Schedule pattern mining daily:
```python
# Add to your scheduler
def mine_patterns_daily():
    connector = get_learning_connector()
    results = connector.mine_patterns(min_support=0.05)
    logger.info(f"Mined {results['patterns_found']} patterns")
```

### 2. Batch Processing

For high traffic, enable batching:
```python
# In your config
COLAB_LEARNING_BATCH_SIZE=20
COLAB_LEARNING_ASYNC=true
```

### 3. Cache Management

The connector includes automatic caching:
- 5-minute TTL for adaptations
- Reduces API calls
- Improves response time

### 4. Fallback Strategy

Always have fallback when learning is offline:
```python
learned = apply_learned_optimization(user_id, prompt)
if learned and learned['confidence'] > 0.7:
    # Use learned strategy
else:
    # Use default optimization
```

## 🔍 Troubleshooting

### Learning Engine Offline

1. Check Colab notebook is running
2. Verify ngrok tunnel is active
3. Check COLAB_LEARNING_URL in .env
4. Test: `curl https://xxxxx.ngrok.io/`

### Slow Response Times

1. Enable async mode
2. Increase batch size
3. Check Colab GPU is enabled
4. Monitor queue size

### No Patterns Found

1. Need minimum interactions (>50)
2. Lower min_support parameter
3. Check data variety
4. Verify successful recordings

## 📊 Analytics Dashboard

The Colab notebook includes visualization:
- Pattern distribution charts
- Success rate trends
- User skill heatmaps
- Confidence distributions

Run the analytics cell to generate reports.

## 🚀 Advanced Features

### Custom Pattern Types

Add your own pattern types:
```python
interaction_data = {
    'type': 'custom_rejection_recovery',
    'input': failed_prompt,
    'output': successful_prompt,
    'metadata': {
        'rejection_reason': 'age_gap',
        'recovery_strategy': 'professional_reframe'
    }
}
```

### Model Fine-tuning

The learning engine can be fine-tuned:
1. Collect domain-specific data
2. Run transfer learning
3. Update model weights
4. Deploy updated models

### Multi-instance Support

Run multiple Colab instances:
1. Load balance with round-robin
2. Sync pattern data via shared storage
3. Aggregate learning across instances

## 🔐 Security

- API endpoints are public (via ngrok)
- Add authentication if needed
- Don't send sensitive user data
- Use user IDs, not personal info

## 📚 Resources

- [Colab Notebook](../colab_notebooks/engine_learning_improvement.ipynb)
- [Connector Code](../src/colab_learning_connector.py)
- [Integration Examples](../examples/learning_integration.py)

## ✅ Checklist

- [ ] Colab notebook uploaded and running
- [ ] GPU runtime enabled
- [ ] API server started with ngrok
- [ ] COLAB_LEARNING_URL configured
- [ ] Learning routes added to Flask
- [ ] Test endpoint working
- [ ] First interactions recorded
- [ ] Pattern mining successful
- [ ] Analytics dashboard viewed

---

The learning engine will continuously improve your platform's optimization quality! 🚀