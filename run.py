# run.py
import uvicorn
import socket
from typing import Optional
import logging
from config import settings

# Initialize logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def find_available_port(start_port: int = 8000, max_port: int = 8020) -> Optional[int]:
    """Find an available port in the given range."""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((settings.HOST, port))
                return port
            except OSError:
                continue
    return None

def main():
    """Main execution function."""
    port = settings.PORT
    
    # If port is not available, find another one
    if port < 8000 or port > 8020:
        logger.warning(f"Port {port} is outside recommended range (8000-8020)")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((settings.HOST, port))
    except OSError:
        logger.warning(f"Port {port} is not available, searching for an alternative")
        port = find_available_port()
        if port is None:
            logger.error("No available ports found in range 8000-8020")
            return 1
    
    logger.info(f"Starting server on {settings.HOST}:{port}")
    config = uvicorn.Config(
        "api.endpoints:app",
        host=settings.HOST,
        port=port,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )
    
    server = uvicorn.Server(config)
    try:
        server.run()
        return 0
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        return 1

if __name__ == "__main__":
    exit(main())