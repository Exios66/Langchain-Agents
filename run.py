# run.py
from core.workflow import WorkflowManager

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