import os
from typing import Dict, Any
from dotenv import load_dotenv

class ConfigManager:
    """Manages configuration and environment variables for the application."""
    
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Initialize configuration
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load all configuration values."""
        return {
            'api_keys': {
                'openai': os.getenv('OPENAI_API_KEY'),
                'serpapi': os.getenv('SERPAPI_API_KEY'),
            },
            'agent': {
                'max_iterations': int(os.getenv('MAX_ITERATIONS', 10)),
                'temperature': float(os.getenv('TEMPERATURE', 0.7)),
                'model_name': os.getenv('MODEL_NAME', 'gpt-4'),
            },
            'vector_store': {
                'persist_directory': os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db'),
                'embedding_model': os.getenv('EMBEDDING_MODEL', 'text-embedding-ada-002'),
            },
            'logging': {
                'level': os.getenv('LOG_LEVEL', 'INFO'),
                'file': os.getenv('LOG_FILE', 'agent_execution.log'),
            },
            'debug': os.getenv('DEBUG', 'False').lower() == 'true'
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

# Create a singleton instance
config = ConfigManager() 