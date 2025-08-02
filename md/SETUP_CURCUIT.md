# 🚀 Quick Setup Guide: CURCUIT API Integration

This guide helps you set up the CURCUIT API as your primary LLM with Ollama as backup.

## ⚡ Quick Start

### 1. Install and Setup

```bash
# Clone and setup the project
./install.sh

# This creates a .env file with CURCUIT configuration template
```

### 2. Configure CURCUIT Credentials

Edit the `.env` file created by the install script:

```bash
nano .env
```

**Required CURCUIT Settings:**
```bash
# =========================
# LLM Configuration  
# =========================
# CURCUIT API Configuration (Primary LLM)
USE_CURCUIT_API=true
CURCUIT_CLIENT_ID=your_actual_client_id        # ← Replace this
CURCUIT_CLIENT_SECRET=your_actual_client_secret # ← Replace this  
CURCUIT_APP_KEY=your_actual_app_key            # ← Replace this
CURCUIT_MODEL=gpt-4o-mini                      # ← Choose your model

# Local Ollama Configuration (Backup LLM)
USE_LOCAL_LLM=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3n:latest
```

### 3. Get CURCUIT Credentials

1. **Request Access:** Use the [CURCUIT API request form](https://cisco.sharepoint.com/sites/CIRCUIT/SitePages/API-RAG-options.aspx)
2. **Receive Information Card** with your credentials:
   - `CLIENT_ID` → Put in `CURCUIT_CLIENT_ID`
   - `CLIENT_SECRET` → Put in `CURCUIT_CLIENT_SECRET`  
   - `APP_KEY` → Put in `CURCUIT_APP_KEY`

### 4. Test Your Setup

```bash
# Check environment configuration
python3 check_env_mapping.py

# Test CURCUIT integration
python test_curcuit_integration.py

# Start the chatbot
python main.py config  # Check configuration
python main.py web     # Launch web interface
```

## 🔧 Environment Variables Reference

| Variable                | Purpose                | Example       |
| ----------------------- | ---------------------- | ------------- |
| `USE_CURCUIT_API`       | Enable/disable CURCUIT | `true`        |
| `CURCUIT_CLIENT_ID`     | OAuth2 client ID       | `abc123...`   |
| `CURCUIT_CLIENT_SECRET` | OAuth2 client secret   | `xyz789...`   |
| `CURCUIT_APP_KEY`       | Application identifier | `my-app-key`  |
| `CURCUIT_MODEL`         | Model to use           | `gpt-4o-mini` |

**Available Models:**
- `gpt-4o-mini` (120K tokens, Free Tier) ← **Recommended**
- `gpt-4.1` (120K/1M tokens, Free Tier)
- `gpt-4o` (120K tokens, Free Tier)
- `o4-mini` (200K tokens, Pay-per-use)

## 🛡️ Security Best Practices

### ✅ What's Safe (Already Configured)

- ✅ `.env` file is in `.gitignore` (never committed to git)
- ✅ Environment variables are loaded securely via pydantic
- ✅ Credentials are not logged or exposed in error messages
- ✅ HTTPS is used for all CURCUIT API calls

### 🚨 Important Security Notes

- **Never commit `.env` to git** - it contains sensitive credentials
- **Use different credentials for different environments** (dev/prod)
- **Rotate credentials regularly** - tokens expire hourly anyway
- **Don't share your `.env` file** - each user should have their own

## 🔍 Troubleshooting

### Environment Loading Issues

```bash
# Check if .env file exists and has correct variables
python3 check_env_mapping.py
```

**Common Issues:**
```
❌ Missing CURCUIT variables
```
**Solution:** Run `./install.sh` to create `.env` template

```
⚠️ Variables found but need configuration  
```
**Solution:** Replace `your_*_here` values with actual credentials

### Authentication Issues

```
❌ CURCUIT API credentials not set
```
**Solution:** Set actual values in `.env` file (not the template values)

```
❌ Token refresh failed: 401
```
**Solution:** Check that CLIENT_ID and CLIENT_SECRET are valid

```
❌ CURCUIT API request failed: 403  
```
**Solution:** Verify APP_KEY is correct for your application

### Fallback Issues

```
⚠️ CURCUIT API connection failed, will use backup
```
**This is normal!** The system automatically falls back to Ollama.

**To fix CURCUIT:**
1. Check internet connection
2. Verify credentials in `.env`
3. Run test: `python test_curcuit_integration.py`

## 🏗️ How Fallback Works

```
User Question
    ↓
🎯 Try CURCUIT API (Primary)
    ↓ (if fails)
🔄 Try Ollama (Backup)  
    ↓ (if fails)
🆘 Try OpenAI (Fallback)
```

**Fallback Triggers:**
- Network issues
- Invalid credentials  
- API rate limits
- Service downtime
- Token expiration

## 📝 Configuration Examples

### Production Setup (CURCUIT + Ollama)
```bash
USE_CURCUIT_API=true
CURCUIT_CLIENT_ID=prod_client_id
CURCUIT_CLIENT_SECRET=prod_client_secret
CURCUIT_APP_KEY=prod_app_key
CURCUIT_MODEL=gpt-4o

USE_LOCAL_LLM=true
OLLAMA_MODEL=gemma3n:latest
```

### Development Setup (Ollama Only)
```bash
USE_CURCUIT_API=false
USE_LOCAL_LLM=true
OLLAMA_MODEL=gemma3n:latest
```

### Cloud Setup (CURCUIT + OpenAI)
```bash
USE_CURCUIT_API=true
CURCUIT_CLIENT_ID=client_id
CURCUIT_CLIENT_SECRET=client_secret
CURCUIT_APP_KEY=app_key

USE_LOCAL_LLM=false
OPENAI_API_KEY=your_openai_key
```

## 🎯 Next Steps

1. **✅ Complete Setup:** Follow this guide to configure your `.env`
2. **🧪 Test Integration:** Run `python test_curcuit_integration.py`
3. **📚 Add Documents:** Put PDFs/docs in `./documents/` directory
4. **🌐 Launch Web UI:** Run `python main.py web`
5. **📖 Read Full Guide:** See `CURCUIT_INTEGRATION.md` for details

## 🆘 Need Help?

- **Environment Issues:** Run `python3 check_env_mapping.py`
- **Integration Issues:** Run `python test_curcuit_integration.py`
- **CURCUIT API Support:** Use [Webex Space](https://cisco.sharepoint.com/sites/CIRCUIT/)
- **General Issues:** Check logs and error messages

---

💡 **Tip:** The system is designed to work even if CURCUIT fails - your backup Ollama will take over seamlessly!