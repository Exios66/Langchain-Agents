from typing import Dict, Any
from core.state import State
from core.commands import Command

class YAAT:
    """Your Average Alan Turing (YAAT) agent - balancing casual insight with technical precision."""
    
    def __init__(self):
        self.name = "YAAT"
        self.traits = {
            "technical_precision": 0.95,
            "casual_insight": 0.9,
            "adaptability": 0.85,
            "innovation": 0.8
        }
    
    def process(self, state: State) -> State:
        """Process input with YAAT's balanced approach."""
        try:
            state['messages'].append(f"{self.name}: Starting analysis with technical precision and casual insight.")
            
            # Get input data and previous analyses
            input_data = state['data_store'].get('input_data', {})
            if not input_data:
                raise ValueError("No input data provided")
            
            query = input_data.get('query', '')
            parameters = input_data.get('parameters', {})
            athena_analysis = state['data_store'].get('athena_analysis', {})
            milgrim_analysis = state['data_store'].get('milgrim_analysis', {})
            
            # Process with YAAT's traits
            analysis = self._balanced_analysis(query, parameters, athena_analysis, milgrim_analysis)
            
            # Store results
            state['data_store']['yaat_analysis'] = analysis
            state['data_store']['technical_score'] = self.traits['technical_precision']
            state['data_store']['status'] = 'completed'
            state['messages'].append(
                f"{self.name}: Analysis complete with {self.traits['technical_precision']*100}% technical precision "
                f"and {self.traits['casual_insight']*100}% casual insight."
            )
            
            return state
        except Exception as e:
            state['messages'].append(f"{self.name}: Error during analysis - {str(e)}")
            state['data_store']['status'] = 'failed'
            state['data_store']['error'] = str(e)
            return state
    
    def _balanced_analysis(
        self,
        query: str,
        parameters: Dict[str, Any],
        athena_analysis: Dict[str, Any],
        milgrim_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform balanced analysis combining technical precision with casual insight."""
        analysis = {
            'query_analysis': query.strip(),
            'parameters_evaluated': parameters,
            'technical_precision': self.traits['technical_precision'],
            'casual_insight_score': self.traits['casual_insight'],
            'adaptability_rating': self.traits['adaptability'],
            'innovation_factor': self.traits['innovation'],
            'previous_analyses_integrated': {
                'athena': bool(athena_analysis),
                'milgrim': bool(milgrim_analysis)
            },
            'recommendations': []
        }
        
        # Add specific recommendations based on query type
        if 'monitor' in query.lower():
            analysis['recommendations'].extend([
                "Implement automated monitoring solutions",
                "Set up real-time alerting",
                "Create user-friendly dashboards"
            ])
        elif 'market' in query.lower():
            analysis['recommendations'].extend([
                "Utilize data visualization tools",
                "Apply predictive analytics",
                "Consider user experience factors"
            ])
        elif 'research' in query.lower():
            analysis['recommendations'].extend([
                "Implement machine learning analysis",
                "Create interactive visualizations",
                "Develop automated research tools"
            ])
        
        return analysis

def create_yaat_agent():
    """Factory function to create YAAT agent."""
    agent = YAAT()
    return lambda state: agent.process(state) 