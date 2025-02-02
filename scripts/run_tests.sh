#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Running test suite..."

# Create test environment
echo -e "${GREEN}Setting up test environment...${NC}"
export PYTHONPATH=.
export API_KEY=test_api_key
export DATABASE_URL=sqlite:///./test.db
export LOG_LEVEL=DEBUG
export ENVIRONMENT=test
export DEBUG=true
export PORT=8001
export WORKERS=1
export CORS_ORIGINS="*"
export ALLOWED_HOSTS="*"
export RATE_LIMIT_WINDOW=60
export MAX_REQUESTS=100
export MAX_CONCURRENT_WORKFLOWS=10
export MAX_WORKFLOW_TIME=300

# Initialize test database
echo -e "${GREEN}Initializing test database...${NC}"
python scripts/init_db.py

# Run tests with coverage
echo -e "${GREEN}Running tests with coverage...${NC}"
pytest tests/ \
    --cov=api \
    --cov=core \
    --cov=agents \
    --cov=integrations \
    --cov-report=term-missing \
    --cov-report=html \
    -v

# Run authentication tests separately
echo -e "${GREEN}Running authentication tests...${NC}"
pytest tests/test_auth.py -v

# Clean up
echo -e "${GREEN}Cleaning up test environment...${NC}"
rm -f test.db

echo -e "${GREEN}Test suite completed!${NC}" 