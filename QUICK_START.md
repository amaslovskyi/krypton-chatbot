# Quick Start Guide - Universal Chatbot

## 🚀 Running the Chatbot

**Simple Usage** (recommended):
```bash
# Start the web interface
./run.sh web

# Interactive chat in terminal
./run.sh chat

# Auto-index your documents
./run.sh auto-index

# Check configuration
./run.sh config
```

## 🔧 Direct Python Usage

If you prefer to use Python directly:
```bash
# Use the krypton virtual environment
./krypton/bin/python main.py web
./krypton/bin/python main.py chat
./krypton/bin/python main.py auto-index
```

## ⚠️ Common Errors Fixed

**❌ Error**: `python main.py` shows "usage: main.py [-h] [--debug] {web,chat,index,config,test,auto-index,status} [path]"

**✅ Solution**: Use the run script or specify a command:
- `./run.sh web` (recommended)
- Or: `./krypton/bin/python main.py web`

**❌ Error**: `ModuleNotFoundError: No module named 'langchain_community'`

**✅ Solution**: Use the virtual environment (already fixed in run.sh):
- The `krypton` virtual environment has all required packages
- Always use `./run.sh` or `./krypton/bin/python`

## 📚 Available Commands

| Command        | Description                     |
| -------------- | ------------------------------- |
| `web`          | Start web interface (port 5000) |
| `chat`         | Interactive command-line chat   |
| `auto-index`   | Automatically index documents   |
| `index <path>` | Index specific directory        |
| `status`       | Check indexing status           |
| `config`       | Show configuration              |
| `test`         | Test system connectivity        |

## 🎯 Quick Setup

1. **Add your documents** to the `documents/` folder
2. **Configure external URLs** in `.env` file (optional)
3. **Start chatbot**: `./run.sh web`
4. **Open browser**: http://localhost:5000

## 🌟 Features Available

- ✅ Universal knowledge base (no Snort dependencies)
- ✅ Multi-format document support (PDF, DOCX, TXT, MD)
- ✅ Web interface with conversation history
- ✅ External URL crawling capabilities
- ✅ Enterprise LLM support (CURCUIT + Ollama + fallbacks)
- ✅ Real-time document monitoring

Your universal chatbot is ready to use! 🎉
