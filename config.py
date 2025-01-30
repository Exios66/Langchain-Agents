# config.py

import os
from typing import Dict, Any, List
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_KEY: str = Field(default=os.getenv("API_KEY", "default_key"), description="API key for authentication")
    API_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=bool(os.getenv("DEBUG", False)), description="Debug mode")
    
    # Database Settings
    DATABASE_URL: str = Field(
        default=os.getenv("DATABASE_URL", "sqlite:///./multi_agent.db"),
        description="Database connection string"
    )
    DB_POOL_SIZE: int = Field(default=5, description="Database connection pool size")
    DB_POOL_TIMEOUT: int = Field(default=30, description="Database connection timeout in seconds")
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=int(os.getenv("PORT", 8000)), description="Server port")
    WORKERS: int = Field(default=4, description="Number of worker processes")
    
    # Security Settings
    CORS_ORIGINS: List[str] = Field(
        default=os.getenv("CORS_ORIGINS", "*").split(","),
        description="Allowed CORS origins"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=os.getenv("ALLOWED_HOSTS", "*").split(","),
        description="Allowed hosts"
    )
    
    # Rate Limiting
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")
    MAX_REQUESTS: int = Field(default=100, description="Maximum requests per window")
    
    # Workflow Settings
    MAX_CONCURRENT_WORKFLOWS: int = Field(default=10, description="Maximum concurrent workflows")
    MAX_WORKFLOW_TIME: int = Field(default=300, description="Maximum workflow execution time in seconds")
    WORKFLOW_TYPES: List[str] = Field(
        default=["sequential", "parallel", "hybrid"],
        description="Available workflow types"
    )
    
    # Agent Settings
    AVAILABLE_AGENTS: List[str] = Field(
        default=["professor_athena", "dr_milgrim", "yaat"],
        description="Available agents"
    )
    AGENT_CONFIGS: Dict[str, Dict[str, Any]] = Field(
        default={
            "professor_athena": {
                "max_concurrent_tasks": 3,
                "specialties": ["research", "analysis", "planning"],
                "response_timeout": 30
            },
            "dr_milgrim": {
                "max_concurrent_tasks": 2,
                "specialties": ["data_processing", "pattern_recognition"],
                "response_timeout": 20
            },
            "yaat": {
                "max_concurrent_tasks": 5,
                "specialties": ["task_execution", "coordination"],
                "response_timeout": 15
            }
        },
        description="Agent-specific configurations"
    )
    
    # Logging Settings
    LOG_LEVEL: str = Field(
        default=os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level"
    )
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Webhook URLs for various services
WEBHOOK_URLS = {
    "notion": "https://api.notion.com/v1/pages",
    "github": "https://api.github.com/repos/{owner}/{repo}/issues",
    "zapier": "https://hooks.zapier.com/hooks/catch/123456/",
    "slack": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
}

# API Credentials
NOTION_API_KEY = "your_notion_secret"
NOTION_DATABASE_ID = "your_database_id"

GITHUB_ACCESS_TOKEN = "your_github_token"
GITHUB_REPO_OWNER = "your_github_username"
GITHUB_REPO_NAME = "your_repository_name"

SLACK_CHANNEL = "#workflow-updates"

# API Configuration
API_CONFIG = {
    "title": "Multi-Agent Workflow API",
    "description": "API for managing and executing multi-agent workflows",
    "version": "1.0.0",
    "docs_url": "/docs",
    "redoc_url": "/redoc"
}

# Security Configuration
SECURITY_CONFIG = {
    "api_key": os.getenv("API_KEY", "default_key_do_not_use_in_production"),
    "rate_limit_window": 60,  # seconds
    "max_requests": 100,  # requests per window
    "cors_origins": os.getenv("CORS_ORIGINS", "*").split(","),
    "allowed_hosts": os.getenv("ALLOWED_HOSTS", "*").split(",")
}

# Agent Configuration
AGENT_CONFIG = {
    "available_agents": ["professor_athena", "dr_milgrim", "yaat"],
    "workflow_types": ["sequential", "parallel", "hybrid"],
    "max_workflow_time": 300,  # seconds
    "max_concurrent_workflows": 10
}

# Database Configuration
DATABASE_CONFIG = {
    "url": os.getenv("DATABASE_URL", "sqlite:///./workflow.db"),
    "min_connections": 1,
    "max_connections": 10,
    "connection_timeout": 30
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": os.getenv("LOG_FILE", "workflow.log")
}

def get_config() -> Dict[str, Any]:
    """Get the complete configuration dictionary."""
    return {
        "api": API_CONFIG,
        "security": SECURITY_CONFIG,
        "agents": AGENT_CONFIG,
        "database": DATABASE_CONFIG,
        "logging": LOGGING_CONFIG
    }

def validate_config() -> bool:
    """Validate the configuration settings."""
    try:
        # Check required environment variables
        required_vars = [
            "API_KEY",
            "DATABASE_URL",
            "LOG_LEVEL"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False
        
        # Validate agent configuration
        if not AGENT_CONFIG["available_agents"]:
            print("No available agents configured")
            return False
        
        if not AGENT_CONFIG["workflow_types"]:
            print("No workflow types configured")
            return False
        
        # Validate security configuration
        if SECURITY_CONFIG["api_key"] == "default_key_do_not_use_in_production":
            print("Warning: Using default API key. This is not secure for production.")
        
        return True
    except Exception as e:
        print(f"Configuration validation failed: {str(e)}")
        return False