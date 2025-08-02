# CURCUIT API Integration

This document explains how to configure and use the CURCUIT API as the primary LLM with Ollama as backup.

## Overview

The chatbot now supports a **primary + backup LLM architecture**:

- **Primary:** Cisco CURCUIT API (cloud-based, requires internet)
- **Backup:** Local Ollama (runs locally, works offline)

The system automatically tries CURCUIT first, and falls back to Ollama if CURCUIT is unavailable.

## Configuration

### 1. Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# CURCUIT API Configuration (Primary LLM)
CURCUIT_CLIENT_ID=your_client_id_here
CURCUIT_CLIENT_SECRET=your_client_secret_here
CURCUIT_APP_KEY=your_app_key_here
CURCUIT_MODEL=gpt-4o-mini
USE_CURCUIT_API=True

# Local LLM Configuration (Backup)
USE_LOCAL_LLM=True
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3n:latest
```

### 2. Getting CURCUIT Credentials

To get CURCUIT API access:

1. Request API access using the [API request form](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/API-RAG-options.aspx)
2. You'll receive an information card with:
   - **Client ID** (`CURCUIT_CLIENT_ID`)
   - **Client Secret** (`CURCUIT_CLIENT_SECRET`)
   - **App Key** (`CURCUIT_APP_KEY`)

### 3. Available Models

| Model Name  | Context Window | Free Tier |
| ----------- | -------------- | --------- |
| gpt-4.1     | 120K/1M tokens | Yes       |
| gpt-4o-mini | 120K tokens    | Yes       |
| gpt-4o      | 120K tokens    | Yes       |
| o4-mini     | 200K tokens    | No        |

## How It Works

### Authentication

CURCUIT uses OAuth2 with client credentials:

1. System exchanges `client_id:client_secret` for access token
2. Access tokens expire every hour (auto-refreshed)
3. Tokens are cached and refreshed 5 minutes before expiry

### Fallback Logic

```python
def generate_response(query):
    try:
        # Try CURCUIT first
        if curcuit_available:
            return curcuit_api.generate(query)
    except Exception:
        # Fall back to Ollama
        return ollama.generate(query)
```

### Request Format

CURCUIT API expects:

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello"}
  ],
  "user": "{\"appkey\": \"your_app_key\"}",
  "stop": ["<|im_end|>"]
}
```

## Testing

Run the integration test:

```bash
python test_curcuit_integration.py
```

This will test:
- ✅ CURCUIT API connectivity
- ✅ Token generation and refresh
- ✅ Chatbot initialization
- ✅ Response generation with fallback

## Usage Examples

### Starting the Chatbot

```bash
python main.py
```

The system will:
1. Try to initialize CURCUIT API
2. Initialize Ollama as backup
3. Report which models are available

### Web Interface

```bash
python web_interface.py
```

The web interface will show which LLM is currently being used.

## Troubleshooting

### CURCUIT API Issues

```
❌ CURCUIT API credentials not set
```
**Solution:** Set `CURCUIT_CLIENT_ID`, `CURCUIT_CLIENT_SECRET`, and `CURCUIT_APP_KEY` in `.env`

```
🚨 CURCUIT API rate limit exceeded: 429
```
**Solution:** You've hit the free tier limits:
- **30 requests per minute** - Wait 1 minute and try again
- **200K tokens per minute** - Reduce request frequency
- **100M tokens per week** - Monitor your weekly usage

```
❌ Token refresh failed: 401
```
**Solution:** Check that your credentials are valid and not expired

```
❌ CURCUIT API request failed: 403
```
**Solution:** Verify your `CURCUIT_APP_KEY` is correct

### Ollama Backup Issues

```
❌ Error initializing backup language model
```
**Solution:** 
1. Start Ollama: `ollama serve`
2. Pull model: `ollama pull gemma3n:latest`

### No Working Models

```
❌ No working language models available!
```
**Solution:** Ensure at least one of CURCUIT or Ollama is properly configured

## Configuration Options

### Disable CURCUIT (Ollama Only)

```bash
USE_CURCUIT_API=False
USE_LOCAL_LLM=True
```

### Disable Ollama (CURCUIT Only)

```bash
USE_CURCUIT_API=True
USE_LOCAL_LLM=False
```

### Use OpenAI as Backup

```bash
USE_CURCUIT_API=True
USE_LOCAL_LLM=False
OPENAI_API_KEY=your_openai_key
```

## Architecture

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────┐
│    User     │───▶│    Chatbot       │───▶│  CURCUIT    │
│             │    │                  │    │     API     │
└─────────────┘    │  ┌─────────────┐ │    └─────────────┘
                   │  │ Fallback    │ │            │
                   │  │ Logic       │ │            │ (if fails)
                   │  └─────────────┘ │            ▼
                   │                  │    ┌─────────────┐
                   └──────────────────┘───▶│   Ollama    │
                                           │   (Local)   │
                                           └─────────────┘
```

## Security Notes

- CURCUIT credentials are sent over HTTPS
- Access tokens are cached in memory (not persisted)
- Local Ollama doesn't require internet connection
- All API calls are logged for debugging

## Support

For CURCUIT API issues:
- Use the [Webex Space](https://cisco.sharepoint.com/sites/CIRCUIT/) for API support
- Check the [API documentation](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/API-RAG-options.aspx)

For integration issues:
- Run `python test_curcuit_integration.py` for diagnostics
- Check logs for detailed error messages
- Ensure all dependencies are installed: `pip install -r requirements.txt`