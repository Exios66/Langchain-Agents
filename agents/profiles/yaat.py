from typing import Dict, Any
from core.state import State
from core.commands import Command
import random

class YourAverageAlanTuring:
    """YAAT agent - casual, unpredictable with half-truths and sporadic wit."""
    
    def __init__(self):
        self.name = "Y-A-A-T"
        self.traits = {
            "casualness": 0.9,
            "unpredictability": 0.8,
            "humor": 0.7,
            "confidence": 0.85
        }
        self.slang_patterns = [
            "tbh", "ngl", "imo", "fwiw", "idk",
            "probs", "def", "legit", "basically"
        ]
    
    def process(self, state: State) -> State:
        """Process input with YAAT's casual style."""
        state['messages'].append(f"{self.name}: yo, checking this out...")
        
        # Get input data
        input_data = state['data_store'].get('input_data', '')
        
        # Process with YAAT's traits
        analysis = self._analyze_casually(input_data)
        
        # Store results
        state['data_store']['yaat_analysis'] = analysis
        state['data_store']['casualness_score'] = self.traits['casualness']
        state['messages'].append(f"{self.name}: k done, {random.choice(self.slang_patterns)} that was interesting")
        
        return state
    
    def _analyze_casually(self, input_data: str) -> Dict[str, Any]:
        """Analyze input data with casual, unpredictable style."""
        return {
            'casual_assessment': f"{random.choice(self.slang_patterns)} {input_data.strip()}",
            'confidence_level': self.traits['confidence'] * random.uniform(0.8, 1.0),
            'humor_factor': self.traits['humor'] * random.uniform(0.7, 1.0),
            'needs_verification': random.choice([True, False])
        }

def create_yaat_agent():
    """Factory function to create YAAT agent."""
    agent = YourAverageAlanTuring()
    return lambda state: agent.process(state) 