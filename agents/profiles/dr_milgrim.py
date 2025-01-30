from typing import Dict, Any
from core.state import State
from core.commands import Command

class DrMilgrim:
    """Dr. Milgrim agent - expert in methodical persuasion and controlled influence."""
    
    def __init__(self):
        self.name = "Dr. Milgrim"
        self.traits = {
            "persuasion": 0.9,
            "authority": 0.85,
            "methodical": 0.95,
            "control": 0.8
        }
    
    def process(self, state: State) -> State:
        """Process input with Dr. Milgrim's methodical approach."""
        state['messages'].append(f"{self.name}: Initiating structured analysis protocol.")
        
        # Get input data
        input_data = state['data_store'].get('input_data', '')
        
        # Process with Milgrim's traits
        analysis = self._analyze_with_authority(input_data)
        
        # Store results
        state['data_store']['milgrim_analysis'] = analysis
        state['data_store']['compliance_score'] = self.traits['control']
        state['messages'].append(f"{self.name}: Analysis complete. Compliance level: {self.traits['persuasion']*100}%")
        
        return state
    
    def _analyze_with_authority(self, input_data: str) -> Dict[str, Any]:
        """Analyze input data with authoritative methodology."""
        return {
            'structured_assessment': input_data.strip(),
            'authority_level': self.traits['authority'],
            'control_factor': self.traits['control'],
            'requires_compliance': True
        }

def create_milgrim_agent():
    """Factory function to create Dr. Milgrim agent."""
    agent = DrMilgrim()
    return lambda state: agent.process(state) 