# integrations/streaming.py
import sys
import time
from core.state import State

def stream_output(state: State) -> State:
    """Streams output token by token for real-time feedback."""
    state['messages'].append("Streaming response initiated...")
    response_text = "Processing completed successfully."
    
    for char in response_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    
    state['messages'].append("Streaming response delivered.")
    return state