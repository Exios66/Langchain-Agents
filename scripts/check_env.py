#!/usr/bin/env python3
"""Check environment setup and configuration."""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any
from config import settings

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def check_required_files() -> List[str]:
    """Check if all required files exist."""
    required_files = [
        ".env",
        "alembic.ini",
        "requirements.txt",
        "config.py",
        "api/endpoints.py",
        "core/database.py",
        "migrations/env.py",
        "migrations/versions/001_initial.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    return missing_files

def check_environment_variables() -> Dict[str, bool]:
    """Check if all required environment variables are set."""
    required_vars = {
        "API_KEY": settings.API_KEY != "default_key",
        "DATABASE_URL": settings.DATABASE_URL != "sqlite:///./multi_agent.db",
        "LOG_LEVEL": settings.LOG_LEVEL != "INFO",
        "DEBUG": True,  # Always True since it has a default value
        "PORT": True,  # Always True since it has a default value
        "WORKERS": True,  # Always True since it has a default value
        "CORS_ORIGINS": True,  # Always True since it has a default value
        "ALLOWED_HOSTS": True,  # Always True since it has a default value
    }
    
    return required_vars

def check_database_connection() -> bool:
    """Check if database connection works."""
    try:
        from core.database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def check_migrations() -> bool:
    """Check if all migrations are up to date."""
    try:
        from alembic.config import Config
        from alembic.script import ScriptDirectory
        from alembic.runtime.environment import EnvironmentContext
        
        # Create Alembic config
        config = Config("alembic.ini")
        script = ScriptDirectory.from_config(config)
        
        # Get current head revision
        heads = script.get_heads()
        if not heads:
            logger.error("No migration head found")
            return False
        
        # Get current revision
        def get_current_rev(rev, _):
            return rev
        
        with EnvironmentContext(
            config,
            script,
            fn=get_current_rev,
            as_sql=False,
            starting_rev=None,
            destination_rev=heads[0]
        ) as env:
            current_rev = env.get_current_revision()
        
        # Check if we're at the latest revision
        return current_rev == heads[0]
    except Exception as e:
        logger.error(f"Migration check failed: {e}")
        return False

def check_api_endpoints() -> bool:
    """Check if API endpoints are properly configured."""
    try:
        from fastapi.testclient import TestClient
        from api.endpoints import app
        
        client = TestClient(app)
        response = client.get("/health")
        
        return response.status_code == 200
    except Exception as e:
        logger.error(f"API endpoint check failed: {e}")
        return False

def main():
    """Main execution function."""
    try:
        print("\nChecking environment setup...\n")
        
        # Check required files
        missing_files = check_required_files()
        if missing_files:
            print("❌ Missing required files:")
            for file in missing_files:
                print(f"  - {file}")
        else:
            print("✅ All required files present")
        
        # Check environment variables
        env_vars = check_environment_variables()
        print("\nEnvironment variables:")
        for var, is_set in env_vars.items():
            status = "✅" if is_set else "❌"
            print(f"{status} {var}")
        
        # Check database connection
        db_status = check_database_connection()
        print(f"\nDatabase connection: {'✅' if db_status else '❌'}")
        
        # Check migrations
        migration_status = check_migrations()
        print(f"Database migrations: {'✅' if migration_status else '❌'}")
        
        # Check API endpoints
        api_status = check_api_endpoints()
        print(f"API endpoints: {'✅' if api_status else '❌'}")
        
        # Overall status
        all_good = (
            not missing_files and
            all(env_vars.values()) and
            db_status and
            migration_status and
            api_status
        )
        
        print(f"\nOverall status: {'✅ Ready' if all_good else '❌ Issues found'}")
        
        return 0 if all_good else 1
    except Exception as e:
        logger.error(f"Environment check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 