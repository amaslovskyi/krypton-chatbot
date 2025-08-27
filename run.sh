#!/bin/bash
# Universal Chatbot Runner Script
# This script ensures the correct Python environment is used

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXEC="$SCRIPT_DIR/krypton/bin/python"

# Check if virtual environment exists
if [ ! -f "$PYTHON_EXEC" ]; then
    echo "❌ Virtual environment not found at: $PYTHON_EXEC"
    echo "Please run ./install.sh first to set up the environment"
    exit 1
fi

# Check if arguments provided
if [ $# -eq 0 ]; then
    echo "🚀 Universal Chatbot"
    echo "===================="
    echo ""
    echo "Usage: ./run.sh <command> [options]"
    echo ""
    echo "Available commands:"
    echo "  web        - Start web interface (recommended)"
    echo "  chat       - Interactive chat mode"
    echo "  index      - Index documents manually"
    echo "  auto-index - Auto-detect and index new documents"
    echo "  status     - Check indexing status"
    echo "  config     - Check configuration"
    echo "  test       - Test connectivity"
    echo ""
    echo "Examples:"
    echo "  ./run.sh web           # Start web interface"
    echo "  ./run.sh chat          # Interactive chat"
    echo "  ./run.sh auto-index    # Index your documents"
    echo "  ./run.sh config        # Check settings"
    echo ""
    exit 1
fi

# Run the application with the correct Python environment
echo "🔧 Using Python: $PYTHON_EXEC"
exec "$PYTHON_EXEC" main.py "$@"
