#!/usr/bin/env python3
"""Database initialization and migration script."""

import os
import sys
import logging
from pathlib import Path
import shutil
import sqlite3
from alembic.config import Config
from alembic import command
from config import settings

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def get_database_path() -> Path:
    """Get database path from URL."""
    url = settings.DATABASE_URL
    if url.startswith("sqlite:///"):
        return Path(url.replace("sqlite:///", ""))
    raise ValueError(f"Unsupported database URL: {url}")

def backup_database():
    """Backup existing database if it exists."""
    db_path = get_database_path()
    if db_path.exists():
        backup_path = db_path.with_suffix(".db.backup")
        logger.info(f"Backing up existing database to {backup_path}")
        shutil.copy2(db_path, backup_path)

def drop_database():
    """Drop existing database if it exists."""
    db_path = get_database_path()
    if db_path.exists():
        logger.info("Dropping existing database")
        db_path.unlink()

def init_database():
    """Initialize a new database."""
    logger.info("Initializing new database")
    db_path = get_database_path()
    conn = sqlite3.connect(str(db_path))
    conn.close()

def run_migrations():
    """Run all pending migrations."""
    logger.info("Running database migrations")
    try:
        # Create Alembic config
        alembic_cfg = Config("alembic.ini")
        
        # Run migrations
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrations completed successfully")
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        raise

def verify_database():
    """Verify database schema and connectivity."""
    logger.info("Verifying database")
    try:
        db_path = get_database_path()
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check workflow_states table
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='workflow_states';
        """)
        if not cursor.fetchone():
            raise Exception("workflow_states table not found")
        
        # Check table schema
        cursor.execute("PRAGMA table_info(workflow_states);")
        columns = {row[1] for row in cursor.fetchall()}
        required_columns = {
            "id", "input_data", "state_data", "messages",
            "workflow_type", "status"
        }
        missing_columns = required_columns - columns
        if missing_columns:
            raise Exception(f"Missing columns: {missing_columns}")
        
        logger.info("Database verification successful")
    except Exception as e:
        logger.error(f"Database verification failed: {e}")
        raise
    finally:
        conn.close()

def main():
    """Main execution function."""
    try:
        # Backup existing database
        backup_database()
        
        # Drop existing database
        drop_database()
        
        # Initialize new database
        init_database()
        
        # Run migrations
        run_migrations()
        
        # Verify database
        verify_database()
        
        logger.info("Database initialization completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 