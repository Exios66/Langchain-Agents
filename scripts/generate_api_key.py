#!/usr/bin/env python3
"""Generate a secure API key."""

import secrets
import string
import argparse
import logging
from pathlib import Path
from config import settings

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def generate_api_key(length: int = 32) -> str:
    """Generate a secure API key."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def update_env_file(api_key: str):
    """Update .env file with new API key."""
    env_path = Path(".env")
    
    # Read existing content
    if env_path.exists():
        content = env_path.read_text().splitlines()
        new_content = []
        key_updated = False
        
        # Update API_KEY line if it exists
        for line in content:
            if line.startswith("API_KEY="):
                new_content.append(f"API_KEY={api_key}")
                key_updated = True
            else:
                new_content.append(line)
        
        # Add API_KEY if it doesn't exist
        if not key_updated:
            new_content.append(f"API_KEY={api_key}")
        
        # Write back to file
        env_path.write_text('\n'.join(new_content) + '\n')
    else:
        # Create new .env file
        env_path.write_text(f"API_KEY={api_key}\n")
    
    logger.info(f"Updated {env_path} with new API key")

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Generate a secure API key")
    parser.add_argument(
        "--length",
        type=int,
        default=32,
        help="Length of the API key (default: 32)"
    )
    parser.add_argument(
        "--update-env",
        action="store_true",
        help="Update .env file with the new API key"
    )
    args = parser.parse_args()
    
    try:
        # Generate API key
        api_key = generate_api_key(args.length)
        print(f"\nGenerated API key: {api_key}")
        
        # Update .env file if requested
        if args.update_env:
            update_env_file(api_key)
        
        return 0
    except Exception as e:
        logger.error(f"Error generating API key: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 