# run.py
from core.graph_builder import compiled_graph
from core.state import State

if __name__ == "__main__":
    initial_state = State(messages=[], data_store={'input_data': "Sample text"})
    final_state = compiled_graph.invoke(initial_state)

    print("\nExecution Log:")
    for message in final_state['messages']:
        print(f" - {message}")