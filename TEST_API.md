# 🧪 Testing ChatWait API

## Quick Start

### 1. Start the API Server
```bash
cd /Users/mjs/Documents/code/spec-dev/hello-sdd-chatagent/backend
uv run python main.py
```

### 2. Test the API
```bash
cd /Users/mjs/Documents/code/spec-dev/hello-sdd-chatagent
python test_api.py
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Chat Wait (Synchronous)
```bash
curl -X POST http://localhost:8000/api/v1/chat/wait \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

### Chat Streaming
```bash
curl -N "http://localhost:8000/api/v1/chat/streaming?message=Hello%20streaming"
```

## Expected Responses

### Health Check Response
```json
{
  "status": "healthy",
  "service": "chatwait-backend",
  "version": "0.1.0",
  "environment": "development"
}
```

### Chat Wait Response
```json
{
  "message": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "context_id": "abc123",
  "token_count": 15,
  "processing_time_ms": 245.6
}
```

### Chat Streaming Response
```
data: {"token": "Hello", "token_index": 0, "context_id": "abc123"}

data: {"token": " ", "token_index": 1, "context_id": "abc123"}

data: {"token": "world", "token_index": 2, "context_id": "abc123"}

data: {"type": "end", "context_id": "abc123", "final_output": "Hello world!"}
```

## Troubleshooting

### Rate Limits
If you see 429 errors, you've hit Gemini API rate limits:
- Free tier: 10 requests per minute
- Wait a few minutes and try again
- Or upgrade to a paid tier

### Validation Errors
422 responses mean invalid input:
- Check message format
- Ensure message is not empty
- Verify JSON syntax

### Connection Issues
If the server won't start:
- Check if port 8000 is available
- Verify API key in .env file
- Check Python dependencies

## Manual Testing with curl

### Test Health
```bash
curl http://localhost:8000/health
```

### Test Chat Wait
```bash
curl -X POST http://localhost:8000/api/v1/chat/wait \
  -H "Content-Type: application/json" \
  -d '{"message": "What is machine learning?"}'
```

### Test Chat Streaming
```bash
curl -N "http://localhost:8000/api/v1/chat/streaming?message=Explain%20quantum%20computing"
```

### Test Error Handling
```bash
# Missing message
curl -X POST http://localhost:8000/api/v1/chat/wait \
  -H "Content-Type: application/json" \
  -d '{}'

# Missing query parameter
curl "http://localhost:8000/api/v1/chat/streaming"
```

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
