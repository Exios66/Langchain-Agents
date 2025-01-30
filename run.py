# run.py
from core.workflow import WorkflowManager
from core.state import State

def main():
    # Initialize workflow
    workflow = WorkflowManager()
    
    # Create initial state
    initial_state = {
        'messages': [],
        'data_store': {
            'input_data': "Sample text for processing",
            'config': {
                'stream_enabled': True,
                'review_required': True
            }
        }
    }
    
    # Execute workflow
    final_state = workflow.execute(initial_state)
    
    # Print execution log
    print("\nExecution Log:")
    for message in final_state['messages']:
        print(f" - {message}")
    
    # Print final results
    print("\nFinal Results:")
    for key, value in final_state['data_store'].items():
        if key != 'config':
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()