#!/bin/bash

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y wget gnupg unzip curl python3-pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Installation complete!"
echo "To start the API server, ensure your .env file is configured, then run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
