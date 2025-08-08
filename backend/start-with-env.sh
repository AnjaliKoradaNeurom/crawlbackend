#!/bin/bash

# Startup script for the Neurom AI Website Analyzer
# This script ensures proper environment variable loading

echo "🚀 Starting Neurom AI Website Analyzer..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found in current directory"
    echo "Please create a .env file with your API keys"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️ Warning: No virtual environment detected"
    echo "Consider activating your virtual environment first"
fi

# Check if required dependencies are installed
echo "🔍 Checking dependencies..."
python -c "import fastapi, uvicorn, openai, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Missing required dependencies"
    echo "Please install requirements: pip install -r requirements.txt"
    exit 1
fi

# main.py now handles environment variable loading and checking
# The original 'check_env.py' script is not provided and is no longer needed.

# Start the server
echo "🌐 Starting FastAPI server..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
