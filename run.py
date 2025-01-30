# run.py
from core.workflow import WorkflowManager
# run.py
import uvicorn
import socket
from typing import Optional

def find_available_port(start_port: int = 8000, max_port: int = 8020) -> Optional[int]:
    """Find an available port in the given range."""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    return None

if __name__ == "__main__":
    port = find_available_port()
    if port is None:
        print("Error: No available ports found in range 8000-8020")
        exit(1)
        
    print(f"Starting server on port {port}")
    config = uvicorn.Config(
        "api.endpoints:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
    server = uvicorn.Server(config)
    try:
        server.run()
    except Exception as e:
        print(f"Error starting server: {e}")
        exit(1)

def main():
    """Main execution function."""
    # Initialize workflow
    workflow = WorkflowManager()
    
    # Create initial state with test input
    initial_state = {
        'messages': [],
        'data_store': {
            'input_data': "This is a test statement that needs to be analyzed for truth and deception.",
            'config': {
                'stream_enabled': True,
                'review_required': True,
                'agent_settings': {
                    'athena_threshold': 0.8,
                    'milgrim_authority': 0.7,
                    'yaat_casualness': 0.9
                }
            }
        }
    }
    
    # Execute workflow
    final_state = workflow.execute(initial_state)
    
    # Print execution log
    print("\nExecution Log:")
    for message in final_state['messages']:
        print(f" - {message}")
    
    # Print agent analyses
    print("\nAgent Analyses:")
    analyses = {
        'Professor Athena': final_state['data_store'].get('athena_analysis', {}),
        'Dr. Milgrim': final_state['data_store'].get('milgrim_analysis', {}),
        'YAAT': final_state['data_store'].get('yaat_analysis', {})
    }
    
    for agent, analysis in analyses.items():
        print(f"\n{agent}'s Analysis:")
        for key, value in analysis.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()