#!/bin/bash

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -e .

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p chroma_db
mkdir -p logs

# Check if .env exists, if not create it from template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.template .env
    echo "Please update the .env file with your API keys and configuration"
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo "Installation complete!"
echo "Please update the .env file with your API keys and configuration before running the application."
echo "To activate the virtual environment, run: source venv/bin/activate" 