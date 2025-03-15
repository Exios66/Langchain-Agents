#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Initializing environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${GREEN}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -r requirements.txt

# Generate API key if .env doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${GREEN}Generating API key and creating .env file...${NC}"
    python scripts/generate_api_key.py --update-env
fi

# Initialize database
echo -e "${GREEN}Initializing database...${NC}"
python scripts/init_db.py

# Run environment check
echo -e "${GREEN}Checking environment setup...${NC}"
python scripts/check_env.py

# Print completion message
echo -e "\n${GREEN}Environment initialization completed!${NC}"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To start the server, run: python run.py" 