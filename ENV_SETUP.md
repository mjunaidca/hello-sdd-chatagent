# Environment Setup Guide

This project uses environment variables for configuration across multiple services. Each directory has its own `.env.example` file that you should copy and customize for your environment.

## Quick Setup

1. **Backend Setup**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   cp .env.example .env
   # Edit .env if you need to change backend URL or ports
   ```

3. **Chat UI Setup**:
   ```bash
   cd chat-ui
   cp .env.example .env.local
   # Edit .env.local if you need to change API URL or features
   ```

4. **Specs Setup** (for testing):
   ```bash
   cd specs
   cp .env.example .env
   # Edit .env if you need to change test configuration
   ```

## Required Environment Variables

### Backend (Required)
- `GEMINI_API_KEY`: Your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Frontend (Optional)
- `BACKEND_URL`: Backend API URL (default: http://localhost:8000)
- `CHAINLIT_PORT`: Chainlit server port (default: 8001)

### Chat UI (Optional)
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL (default: http://localhost:8000/api/v1)
- `NEXT_PUBLIC_DEBUG`: Enable debug mode (default: false)

### Specs (Optional)
- `TEST_API_BASE_URL`: Test API URL (default: http://localhost:8000)
- `TEST_TIMEOUT_SECONDS`: Test timeout (default: 30)

## Environment File Locations

```
project/
├── backend/
│   ├── .env.example          # Backend configuration template
│   └── .env                  # Your actual backend config (create from .env.example)
├── frontend/
│   ├── .env.example          # Frontend configuration template
│   └── .env                  # Your actual frontend config (create from .env.example)
├── chat-ui/
│   ├── .env.example          # Chat UI configuration template
│   └── .env.local            # Your actual chat UI config (create from .env.example)
└── specs/
    ├── .env.example          # Specs testing configuration template
    └── .env                  # Your actual specs config (create from .env.example)
```

## Security Notes

- **Never commit `.env` files** to version control
- **Always use `.env.example`** as a template
- **Replace placeholder values** with your actual configuration
- **Use different API keys** for development, staging, and production
- **Rotate API keys** regularly for security

## Development vs Production

### Development
- Use `DEBUG=true` and `RELOAD=true` for backend
- Use `CHAINLIT_DEBUG=true` for frontend
- Use `NEXT_PUBLIC_DEBUG=true` for chat UI

### Production
- Use `DEBUG=false` and `RELOAD=false` for backend
- Use `CHAINLIT_DEBUG=false` for frontend
- Use `NEXT_PUBLIC_DEBUG=false` for chat UI
- Use production API keys and URLs
- Enable proper logging and monitoring

## Troubleshooting

### Backend Issues
- Check that `GEMINI_API_KEY` is set correctly
- Verify `BACKEND_URL` matches your backend server
- Check CORS settings if frontend can't connect

### Frontend Issues
- Ensure `BACKEND_URL` points to running backend
- Check that backend is running on the correct port
- Verify CORS configuration allows frontend origin

### Chat UI Issues
- Ensure `NEXT_PUBLIC_API_BASE_URL` is correct
- Check that backend API is accessible
- Verify environment variables are prefixed with `NEXT_PUBLIC_`

### Testing Issues
- Ensure `TEST_API_BASE_URL` points to running backend
- Check that all required services are running
- Verify test timeout settings are appropriate
