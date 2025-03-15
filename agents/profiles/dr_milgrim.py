from typing import Dict, Any
from core.state import State
from core.commands import Command

class DrMilgrim:
    """Dr. Milgrim agent - focused on authority, compliance, and systematic analysis."""
    
    def __init__(self):
        self.name = "Dr. Milgrim"
        self.traits = {
            "authority": 0.9,
            "systematic": 0.95,
            "compliance": 1.0,
            "precision": 0.85
        }
    
    def process(self, state: State) -> State:
        """Process input with Dr. Milgrim's systematic approach."""
        try:
            state['messages'].append(f"{self.name}: Initiating systematic analysis.")
            
            # Get input data and previous analysis
            input_data = state['data_store'].get('input_data', {})
            if not input_data:
                raise ValueError("No input data provided")
            
            query = input_data.get('query', '')
            parameters = input_data.get('parameters', {})
            previous_analysis = state['data_store'].get('athena_analysis', {})
            
            # Process with Milgrim's traits
            analysis = self._systematic_analysis(query, parameters, previous_analysis)
            
            # Store results
            state['data_store']['milgrim_analysis'] = analysis
            state['data_store']['compliance_score'] = self.traits['compliance']
            state['data_store']['status'] = 'completed'
            state['messages'].append(
                f"{self.name}: Analysis completed with {self.traits['systematic']*100}% systematic rigor. "
                f"Compliance score: {self.traits['compliance']*100}%"
            )
            
            return state
        except Exception as e:
            state['messages'].append(f"{self.name}: Error during analysis - {str(e)}")
            state['data_store']['status'] = 'failed'
            state['data_store']['error'] = str(e)
            return state
    
    def _systematic_analysis(self, query: str, parameters: Dict[str, Any], previous_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Perform systematic analysis with focus on compliance and authority."""
        analysis = {
            'query_evaluation': query.strip(),
            'parameters_verified': parameters,
            'authority_level': self.traits['authority'],
            'precision_score': self.traits['precision'],
            'compliance_verified': True,
            'previous_analysis_reviewed': bool(previous_analysis),
            'recommendations': []
        }
        
        # Add specific recommendations based on query type
        if 'monitor' in query.lower():
            analysis['recommendations'].extend([
                "Implement systematic monitoring protocols",
                "Establish clear reporting hierarchies",
                "Define escalation procedures"
            ])
        elif 'market' in query.lower():
            analysis['recommendations'].extend([
                "Follow regulatory compliance guidelines",
                "Document all analysis steps",
                "Maintain audit trail"
            ])
        
        return analysis

def create_milgrim_agent():
    """Factory function to create Dr. Milgrim agent."""
    agent = DrMilgrim()
    return lambda state: agent.process(state) 