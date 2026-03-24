from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv

# ------
# File input and parsing
# ------

def loadNetworkFromFile(filename):
    G = nx.DiGraph()

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if len(line) == 0:
                continue        # Skip rest of loop for empty lines in file
            
            node_letter, node_neighbourhood, node_ttable = line.split(",")

            node_letter = node_letter.upper().strip()
            node_neighbourhood = tuple(node_neighbourhood.upper().strip().split())
            node_ttable = node_ttable.strip()

            # Validate the truthtable matches length of neighbourhood
            expected_length = 2**len(node_neighbourhood)
            if len(node_ttable) != expected_length:
                raise ValueError(f"The truthtable does not match expected length for node {node_letter}.")

            # Add node and its properties to graph
            G.add_node(node_letter, truthtable=node_ttable, neighbours=node_neighbourhood)  # Neighbourhood is added to preserve order for later state calculations

    return G

# ------
# Helper Function: extension replacement for output files
# ------

def replaceExtension(filename, new_extension):
    path = Path(filename)
    current_extensions = "".join(path.suffixes)             # Compile all extensions as a single string to replace
    new_filename = str(path).replace(current_extensions, new_extension)

    return new_filename

# ------
# Wiring Diagram
# ------

def printWiringDiagram(G, filename):
    # Draw the graph using pygraphviz
    A = nx.nx_agraph.to_agraph(G)
    A.layout(prog='dot')

    # Save the graph as a PNG image with the same name as the input file 
    png_name = replaceExtension(filename, "_WiringDiagram.png")
    A.draw(png_name)

# ------
# Calculate next states
# ------

def nodeNextState(node, current_g_state, G, node_order):
    
    # Map the sorted nodes to the current global state in a dictionary
    state_map = {}
    for i, letter in enumerate(node_order):
        state_map[letter] = current_g_state[i]

    # Get neighbour's nodes
    neighbours = G.nodes[node]["neighbours"]

    # Create a binary string from neighbours
    neighbour_bits = "".join(state_map[nb] for nb in neighbours)
    index = int(neighbour_bits, 2)
    
    # Look up next state from truth table
    new_state = G.nodes[node]["truthtable"][index]

    return new_state


'''

def globalNextState(G, current_g_state):
    # This function calculates the next global state based on the current global state.
    # It calls nodeNextState for each letter, passing in this current global state each time
    
    # Alphabetical node order used
    node_order = sorted(ttables.keys())
    
    # Find next state of each node and compile
    next_g_states = []
    for node in node_order:
        next_g_states.append(nextNodeState(node, current_g_state, ttables, node_order))
    next_g_state = "".join(next_g_states)

    # return next global state
    return next_g_state

# ------
# State Transition Graph
# ------

def allStateTransitions(ttables):
    num_nodes = len(ttables)        # Calculate the number of possible global states
    num_states = 2 ** num_nodes     # Initialize a dictionary to store the traces for each initial state

    state_trans = {}

    for i in range(num_states):
        # Need to convert to binary state with leading zeros to match length of global states
        bin_state = bin(i)[2:].zfill(num_nodes)

        next_state = nextGlobalState(ttables, bin_state)
        
        state_trans[bin_state] = next_state
            
    return state_trans

def drawStateGraph(state_trans):

    dot = graphviz.Digraph(comment='State Transition Graph') 

    for state in state_trans:
        dot.node(state)

    for state, next_state in state_trans.items():
        dot.edge(state, next_state)

    dot.render(format='png', view=True)

    return dot

# ------
# Traces
# ------

def runAllTraces(ttables):
    num_nodes = len(ttables)        # Calculate the number of possible global states
    num_states = 2 ** num_nodes     # Initialize a dictionary to store the traces for each initial state

    all_traces = {}                 # Dictionary to store all traces for each initial state

    for i in range(num_states):
        start_state = bin(i)[2:].zfill(num_nodes)
        trace = [start_state]       # Initialize the trace with the starting state
        seen_states = set()         # Set to track seen states for cycle detection

        seen_states.add(start_state) # added start_state to seen_states to prevent skipping it from the loop detection
        
        current_state = start_state
        while True:
            next_state = nextGlobalState(ttables, current_state)
            trace.append(next_state)

            if next_state in seen_states:  # Cycle detected
                break

            seen_states.add(next_state)
            current_state = next_state

        all_traces[start_state] = trace

    return all_traces

def saveTracesToFile(all_traces):
    filename = "traces.txt"
    with open(filename, "w") as file:
        file.write(f"Traces for each initial state:\n\n")
            
        for start_state, trace in all_traces.items():
            file.write(f"{start_state}: " + " -> ".join(trace) + "\n")

    print(f"Traces saved to {filename}")

# ------
# Attractors
# ------

def detectAttractors():
    pass

def saveAttractorsToFile(attractors):
    pass

# ------
# Main
# ------
'''

def main():
    filename = 'ExampleBoolNet1.txt'

    G = loadNetworkFromFile(filename)
    print("Graph of all nodes: ", G)

    printWiringDiagram(G, filename)

    '''
    state_trans = allStateTransitions(G)

    dot = drawStateGraph(state_trans)

    # Run all traces and print them
    all_traces = runAllTraces(G)
    saveTracesToFile(all_traces)
    '''
main()