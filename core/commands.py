from typing import Any, Dict
from core.state import State

class Command:
    """Base class for agent commands."""
    
    def execute(self, state: State) -> Dict[str, Any]:
        """Execute the command and return updated state."""
        raise NotImplementedError("Command execution must be implemented by subclass.") 