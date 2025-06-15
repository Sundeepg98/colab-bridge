# Google Colab Integration Setup

## Your Colab Notebook Integration

This guide will help you connect your Flask app with your specific Colab notebook: 
https://colab.research.google.com/drive/1EwfBj0nC9St-2hB1bv2zGWWDTcS4slsx

## Step 1: Set up your Colab Secret

1. **Open your Colab notebook**
2. **Click the key icon (🔑) in the left sidebar** to access Colab Secrets
3. **Add a new secret:**
   - Name: `sun_colab`
   - Value: `your-secure-api-key-here` (choose a strong random string)
4. **Grant notebook access** to the secret

## Step 2: Add the Integration Code to Your Colab Notebook

Copy this code to a cell in your Colab notebook:

```python
# Install required packages
!pip install fastapi uvicorn pyngrok torch transformers diffusers accelerate

# Import libraries
import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.colab import userdata
import uvicorn
from pyngrok import ngrok
import threading
import torch
from transformers import pipeline
import json
from datetime import datetime

# Get your secret key
API_KEY = userdata.get('sun_colab')
print(f"✅ Retrieved API key: {API_KEY[:8]}...")

# Create FastAPI app
app = FastAPI(title="Sun Colab Processing Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class TextRequest(BaseModel):
    prompt: str
    style: str = "creative"
    max_length: int = 512

class ImageRequest(BaseModel):
    prompt: str
    style: str = "photorealistic"
    steps: int = 20

# Initialize models (lazy loading)
text_generator = None
image_generator = None

def get_text_generator():
    global text_generator
    if text_generator is None:
        print("🔄 Loading text generation model...")
        text_generator = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-medium",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device=0 if torch.cuda.is_available() else -1
        )
        print("✅ Text model loaded!")
    return text_generator

def get_image_generator():
    global image_generator
    if image_generator is None:
        print("🔄 Loading image generation model...")
        from diffusers import StableDiffusionPipeline
        image_generator = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        if torch.cuda.is_available():
            image_generator = image_generator.to("cuda")
        print("✅ Image model loaded!")
    return image_generator

# Authentication middleware
def verify_api_key(request_api_key: str):
    if request_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "gpu_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    }

# Text generation endpoint
@app.post("/generate-text")
async def generate_text(request: TextRequest, api_key: str = ""):
    verify_api_key(api_key)
    
    try:
        generator = get_text_generator()
        
        # Enhanced prompt based on style
        enhanced_prompt = f"Create a {request.style} description: {request.prompt}"
        
        result = generator(
            enhanced_prompt,
            max_length=request.max_length,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            pad_token_id=generator.tokenizer.eos_token_id
        )
        
        generated_text = result[0]['generated_text']
        # Clean up the output
        generated_text = generated_text.replace(enhanced_prompt, "").strip()
        
        return {
            "success": True,
            "generated_text": generated_text,
            "original_prompt": request.prompt,
            "style": request.style,
            "processing_time": 0.8,  # Approximate
            "gpu_used": torch.cuda.is_available()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image generation endpoint
@app.post("/generate-image")
async def generate_image(request: ImageRequest, api_key: str = ""):
    verify_api_key(api_key)
    
    try:
        generator = get_image_generator()
        
        # Enhanced prompt based on style
        style_prompts = {
            "photorealistic": f"{request.prompt}, photorealistic, high detail, 8k resolution",
            "artistic": f"{request.prompt}, digital art, artistic style, vibrant colors",
            "cinematic": f"{request.prompt}, cinematic lighting, dramatic composition"
        }
        
        enhanced_prompt = style_prompts.get(request.style, request.prompt)
        
        # Generate image
        image = generator(
            enhanced_prompt,
            num_inference_steps=request.steps,
            guidance_scale=7.5
        ).images[0]
        
        # Save image temporarily
        import base64
        import io
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "success": True,
            "image_base64": img_str,
            "prompt": enhanced_prompt,
            "style": request.style,
            "steps": request.steps,
            "processing_time": 2.5,  # Approximate
            "gpu_used": torch.cuda.is_available()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Status endpoint
@app.get("/status")
async def get_status():
    return {
        "total_resources": 1,
        "active_resources": 1,
        "pending_tasks": 0,
        "completed_tasks": 0,
        "resources": [{
            "instance_id": "sun_colab_main",
            "is_active": True,
            "gpu_type": "T4" if torch.cuda.is_available() else "CPU",
            "current_load": 0.3,
            "tasks_processed": 0,
            "capabilities": ["TEXT_GENERATION", "IMAGE_GENERATION", "EMBEDDINGS"]
        }]
    }

# Start the server
def start_server():
    # Set up ngrok tunnel
    ngrok.set_auth_token("your_ngrok_token_here")  # Optional: add your ngrok token
    public_url = ngrok.connect(8000)
    print(f"🌐 Public URL: {public_url}")
    print(f"🔑 API Key: {API_KEY}")
    print("📋 Copy this URL to your Flask app's SUN_COLAB_URL environment variable")
    
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

# Start in a thread to avoid blocking
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

print("🚀 Server starting...")
print("⏳ Wait for the public URL to appear above")
```

## Step 3: Configure Your Flask App

1. **Set the environment variable** with your Colab's ngrok URL:
   ```bash
   export SUN_COLAB_URL="https://your-ngrok-url.ngrok.io"
   ```

2. **Set your Colab API key** in your Flask environment:
   ```bash
   export SUN_COLAB_API_KEY="your-secure-api-key-here"
   ```

## Step 4: Test the Integration

1. **Run the Flask app:**
   ```bash
   python app.py
   ```

2. **Visit the Colab dashboard:**
   ```
   http://localhost:5000/colab-dashboard
   ```

3. **Test the connection** using the dashboard's test button

## Step 5: Usage Examples

### Text Enhancement
```python
import requests

response = requests.post('http://localhost:5000/api/colab-text-enhance', 
    json={
        'prompt': 'A beautiful sunset over the ocean',
        'style': 'cinematic'
    }
)
result = response.json()
print(result['enhanced_text'])
```

### Image Generation
```python
response = requests.post('http://localhost:5000/api/colab-image-generate', 
    json={
        'prompt': 'A mystical forest with glowing trees',
        'style': 'artistic',
        'steps': 20
    }
)
result = response.json()
# Image will be returned as base64 string
```

## Troubleshooting

### Common Issues:

1. **"Invalid API key" error:**
   - Make sure your `sun_colab` secret in Colab matches your Flask environment variable

2. **"Connection refused" error:**
   - Ensure ngrok tunnel is active in your Colab notebook
   - Check that the SUN_COLAB_URL environment variable is correctly set

3. **GPU out of memory:**
   - Reduce batch sizes or use lighter models
   - Restart Colab runtime to clear GPU memory

4. **Ngrok session expired:**
   - Re-run the Colab cell to create a new tunnel
   - Update the SUN_COLAB_URL with the new ngrok URL

### Getting Help:

- Check the Colab dashboard at `/colab-dashboard` for status
- Monitor Flask logs for connection errors
- Use the test buttons in the dashboard to verify functionality

## Security Notes

- Keep your `sun_colab` secret secure and never share it
- The ngrok URL changes each time you restart - update your Flask app accordingly
- Consider using ngrok auth tokens for more stable tunnels
- In production, use HTTPS and proper authentication

## Next Steps

Once the integration is working:

1. **Explore advanced features** in the Colab dashboard
2. **Scale up** by adding more Colab instances
3. **Optimize models** for your specific use cases
4. **Monitor usage** and costs through the dashboard

---

🎉 **You're now ready to use GPU-accelerated AI processing with your Colab notebook!**