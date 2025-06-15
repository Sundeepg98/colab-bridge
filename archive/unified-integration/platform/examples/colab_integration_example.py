"""
Example: Using Google Colab for Advanced Processing
Shows how to leverage Colab's GPU resources for various AI tasks
"""

from flask import Flask, request, jsonify
import asyncio
import base64
from src.colab_seamless_integration import (
    get_colab_orchestrator, 
    get_colab_processor,
    ProcessingType,
    ColabTask
)
import uuid

app = Flask(__name__)

# Example 1: Enhanced text generation with Colab GPU
@app.route('/api/colab-text-enhance', methods=['POST'])
async def colab_text_enhance():
    """Generate enhanced text using Colab GPU models"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    style = data.get('style', 'creative')
    
    processor = get_colab_processor()
    
    try:
        # Process text with advanced model on GPU
        result = await processor.process_text(
            text=prompt,
            model='gpt2-large',  # Can use larger models with GPU
            parameters={
                'max_length': 200,
                'temperature': 0.8,
                'top_p': 0.95,
                'style': style
            }
        )
        
        return jsonify({
            'success': True,
            'original': prompt,
            'enhanced': result.get('generated_text', ''),
            'processing_device': 'Colab GPU',
            'model_used': result.get('model', 'default')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Example 2: Generate images with Stable Diffusion
@app.route('/api/colab-generate-image', methods=['POST'])
async def colab_generate_image():
    """Generate high-quality images using Colab GPU"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    style = data.get('style', 'realistic')
    size = data.get('size', '512x512')
    
    processor = get_colab_processor()
    
    try:
        # Generate image with Stable Diffusion
        result = await processor.generate_image(
            prompt=prompt,
            style=style,
            size=size,
            steps=50,  # More steps for better quality
            guidance_scale=7.5
        )
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'image_base64': result.get('image', ''),
            'style': style,
            'size': size,
            'processing_device': 'Colab GPU'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Example 3: Neural search across documents
@app.route('/api/colab-neural-search', methods=['POST'])
async def colab_neural_search():
    """Perform semantic search using GPU-accelerated embeddings"""
    data = request.get_json()
    query = data.get('query', '')
    documents = data.get('documents', [])
    top_k = data.get('top_k', 5)
    
    processor = get_colab_processor()
    
    try:
        # Perform neural search
        results = await processor.neural_search(
            query=query,
            corpus=documents,
            top_k=top_k
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'total_documents': len(documents),
            'processing_device': 'Colab GPU'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Example 4: Batch embedding generation
@app.route('/api/colab-batch-embeddings', methods=['POST'])
async def colab_batch_embeddings():
    """Generate embeddings for multiple texts efficiently"""
    data = request.get_json()
    texts = data.get('texts', [])
    model = data.get('model', 'sentence-transformers')
    
    processor = get_colab_processor()
    
    try:
        # Generate embeddings in batch
        embeddings = await processor.generate_embeddings(
            texts=texts,
            model=model
        )
        
        return jsonify({
            'success': True,
            'num_texts': len(texts),
            'embedding_dim': embeddings.shape[1] if len(embeddings) > 0 else 0,
            'embeddings': embeddings.tolist(),
            'model': model,
            'processing_device': 'Colab GPU'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Example 5: Style transfer for images
@app.route('/api/colab-style-transfer', methods=['POST'])
async def colab_style_transfer():
    """Apply artistic style transfer using GPU"""
    data = request.get_json()
    content_image = data.get('content_image', '')  # base64
    style_image = data.get('style_image', '')      # base64
    strength = data.get('strength', 0.7)
    
    processor = get_colab_processor()
    
    try:
        # Apply style transfer
        result = await processor.style_transfer(
            content_image=content_image,
            style_image=style_image,
            strength=strength
        )
        
        return jsonify({
            'success': True,
            'stylized_image': result.get('output_image', ''),
            'strength': strength,
            'processing_time': result.get('processing_time', 0),
            'processing_device': 'Colab GPU'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Example 6: Custom task with callback
@app.route('/api/colab-custom-task', methods=['POST'])
async def colab_custom_task():
    """Submit a custom processing task to Colab"""
    data = request.get_json()
    task_type = data.get('task_type', 'text_generation')
    payload = data.get('payload', {})
    priority = data.get('priority', 5)
    
    orchestrator = get_colab_orchestrator()
    
    # Create custom task
    task = ColabTask(
        task_id=str(uuid.uuid4()),
        task_type=ProcessingType(task_type),
        payload=payload,
        priority=priority
    )
    
    try:
        # Submit task
        task_id = await orchestrator.submit_task(task)
        
        # Wait for result (with timeout)
        timeout = 60  # seconds
        start_time = asyncio.get_event_loop().time()
        
        while asyncio.get_event_loop().time() - start_time < timeout:
            task_status = await orchestrator.get_task_status(task_id)
            
            if task_status and task_status.status == 'completed':
                return jsonify({
                    'success': True,
                    'task_id': task_id,
                    'status': 'completed',
                    'result': task_status.result
                })
            elif task_status and task_status.status == 'failed':
                return jsonify({
                    'success': False,
                    'task_id': task_id,
                    'status': 'failed',
                    'error': task_status.error
                }), 500
                
            await asyncio.sleep(0.5)
        
        return jsonify({
            'success': False,
            'task_id': task_id,
            'status': 'timeout',
            'error': 'Task timed out'
        }), 408
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Example 7: Multi-modal processing pipeline
@app.route('/api/colab-multimodal', methods=['POST'])
async def colab_multimodal():
    """Process text and generate related image"""
    data = request.get_json()
    text = data.get('text', '')
    
    processor = get_colab_processor()
    
    try:
        # Step 1: Enhance text
        enhanced_text = await processor.process_text(
            text=text,
            model='gpt2-medium',
            parameters={'max_length': 100}
        )
        
        # Step 2: Extract key concepts for image
        image_prompt = enhanced_text.get('generated_text', text)[:100]
        
        # Step 3: Generate image
        image_result = await processor.generate_image(
            prompt=image_prompt,
            style='artistic',
            size='512x512'
        )
        
        # Step 4: Generate embeddings for similarity
        embeddings = await processor.generate_embeddings(
            texts=[text, image_prompt]
        )
        
        # Calculate similarity
        import numpy as np
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        
        return jsonify({
            'success': True,
            'original_text': text,
            'enhanced_text': enhanced_text.get('generated_text', ''),
            'image_prompt': image_prompt,
            'image_base64': image_result.get('image', ''),
            'text_image_similarity': float(similarity),
            'processing_device': 'Colab GPU'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Example 8: Resource status endpoint
@app.route('/api/colab-resources')
async def colab_resources():
    """Get status of all Colab processing resources"""
    orchestrator = get_colab_orchestrator()
    
    resources = []
    for resource_id, resource in orchestrator.resources.items():
        resources.append({
            'id': resource_id,
            'url': resource.url,
            'active': resource.is_active,
            'gpu_type': resource.gpu_type,
            'current_load': resource.current_load,
            'tasks_processed': resource.tasks_processed,
            'capabilities': [c.value for c in resource.capabilities]
        })
    
    return jsonify({
        'total_resources': len(resources),
        'active_resources': len([r for r in resources if r['active']]),
        'pending_tasks': len(orchestrator.pending_tasks),
        'completed_tasks': len(orchestrator.completed_tasks),
        'resources': resources
    })

# Example 9: Batch processing with progress
@app.route('/api/colab-batch-process', methods=['POST'])
async def colab_batch_process():
    """Process multiple items with progress tracking"""
    data = request.get_json()
    items = data.get('items', [])
    processor_type = data.get('processor', 'embeddings')
    batch_size = data.get('batch_size', 32)
    
    processor = get_colab_processor()
    
    try:
        # Process in batches
        results = await processor.batch_process(
            items=items,
            processor=processor_type,
            batch_size=batch_size
        )
        
        return jsonify({
            'success': True,
            'total_items': len(items),
            'processed_items': len(results),
            'results': results,
            'batch_size': batch_size,
            'processing_device': 'Colab GPU'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Setup Colab instances
    orchestrator = get_colab_orchestrator()
    
    # Example: Register a Colab instance
    # orchestrator.register_colab_instance(
    #     instance_id='colab_gpu_1',
    #     url='https://your-ngrok-url.ngrok.io',
    #     capabilities=[
    #         ProcessingType.TEXT_GENERATION,
    #         ProcessingType.IMAGE_GENERATION,
    #         ProcessingType.EMBEDDINGS,
    #         ProcessingType.NEURAL_SEARCH
    #     ],
    #     gpu_type='Tesla T4'
    # )
    
    print("🚀 Colab Integration Examples")
    print("Configure COLAB_PROCESSING_URLS in .env with your Colab ngrok URLs")
    
    # Run with asyncio support
    import asyncio
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    
    config = Config()
    config.bind = ["localhost:5002"]
    asyncio.run(serve(app, config))