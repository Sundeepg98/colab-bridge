# Claude AI Integration Setup

## Current Status
Claude AI integration is implemented but currently disabled due to timeout issues with the decorators.

## How it works:

1. **Health Check at Startup**: The app checks Claude API availability when starting
2. **Automatic Monitoring**: Background thread checks Claude API every 5 minutes
3. **Automatic Fallback**: If Claude is unavailable, the system automatically uses local optimization
4. **User Notification**: Web interface shows a banner when Claude is unavailable

## Features:

### 1. Health Check System (`src/claude_health_check.py`)
- Tests Claude API with a simple request at startup
- Monitors API availability every 5 minutes
- Automatically disables Claude features after 3 consecutive failures
- Saves status to `claude_status.json` for persistence

### 2. Simple Claude Enhancer (`src/simple_claude_enhancer.py`)
- Makes a single API call (not 13+ like the original)
- Uses Claude 3 Haiku for fast responses
- 5-second timeout to prevent hanging
- Handles sensitive content appropriately

### 3. API Endpoints:
- `/api/claude-status` - Check current Claude availability
- `/api/claude-enhance` - Use Claude if available, fallback if not

## To Enable Claude:

1. Ensure you have a valid API key in `.env`:
   ```
   ANTHROPIC_API_KEY=your-api-key-here
   ```

2. Fix the decorator issue in `app.py`:
   - The `@secure_endpoint` decorator has a JSON parsing bug with Werkzeug
   - Either fix the decorator or remove it from the claude-enhance endpoint

3. The system will automatically detect and use Claude when available

## Temporary Workaround:

Currently using `/api/claude-enhance-simple` which bypasses the problematic decorators and provides:
- Fast response times (< 100ms)
- Content filtering for inappropriate prompts
- Consistent results

## Testing:

```bash
# Check Claude status
curl http://localhost:5000/api/claude-status

# Test enhancement (will use Claude if available, fallback if not)
curl -X POST http://localhost:5000/api/claude-enhance \
  -H "Content-Type: application/json" \
  -d '{"prompt": "your prompt here"}'
```

## Frontend Integration:

The web interface automatically:
1. Checks Claude status on page load
2. Shows a yellow banner if Claude is unavailable
3. Updates button text from "Claude AI" to "Smart Local" when using fallback
4. Uses the appropriate endpoint based on availability