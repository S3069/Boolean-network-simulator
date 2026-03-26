from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv


# ------
# Helper Functions: Draw and name diagrams
# ------

def replaceExtension(filename, new_extension):
    # Source - https://stackoverflow.com/a/56807917
    # Posted by Michael Hall, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-03-24, License - CC BY-SA 4.0

    path = Path(filename)
    current_extensions = "".join(path.suffixes)             # Compile all extensions as a single string to replace
    new_filename = str(path).replace(current_extensions, new_extension)

    return new_filename

def drawDiagram(graph, filename, new_extension):
    # Draw the graph using pygraphviz
    A = nx.nx_agraph.to_agraph(graph)
    A.layout(prog='dot')

    png_name = replaceExtension(filename, new_extension)    # Renames file to match input file
    A.draw(png_name)

# ------
# Helper functions: Calculate next states
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

def globalNextState(G, current_g_state):
    # Alphabetical node order used
    node_order = sorted(G.nodes)
    
    # Find next state of each node and compile
    next_g_states = []
    for node in node_order:
        next_g_states.append(nodeNextState(node, current_g_state, G, node_order))
    next_g_state = "".join(next_g_states)

    # return next global state
    return next_g_state

# ------
# Helper function: Canonical reorder
# ------

def canonicalReorder(cycle):
    # Remove duplicated starting/ending state
    if len(cycle) > 1 and cycle[0] == cycle[-1]:
        cycle = cycle[:-1]

    # Reorder the cycle to start with the smallest state
    smallest_state = min(cycle)
    smallest_index = cycle.index(smallest_state)
    canonical_cycle = cycle[smallest_index:] + cycle[:smallest_index]

    return canonical_cycle

# ------
# File Input
# ------

def loadNetworkFromFile(filename):
    # Create a directed graph to represent the Boolean network
    G = nx.DiGraph()            

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            # Skip rest of loop for empty line(s) in file
            if len(line) == 0:
                continue
            
            # Parse the line into node properties
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
            for neighbour in node_neighbourhood:
                G.add_edge(neighbour, node_letter)          # Add directed edge from neighbour to node

    return G

# ------
# State Transition Graph
# ------

def compileStateTransitions(G):
    # Calculate the number of possible global states
    num_nodes = len(G.nodes)
    num_states = 2 ** num_nodes

    # For each possible global state, calculate the next global state and store in a dictionary
    state_trans = {}
    for i in range(num_states):
        bin_state = bin(i)[2:].zfill(num_nodes)     # Convert to binary state with leading zeros to match length of global states

        next_state = globalNextState(G, bin_state)
        state_trans[bin_state] = next_state
            
    return state_trans

# ------
# Traces
# ------

def runAllTraces(G, cyclicOnly=False, canonicalOrder=False, maxDepth=10000):
    # Calculate the number of possible global states
    num_nodes = len(G.nodes)        
    num_states = 2 ** num_nodes     

    all_traces = {}                 

    # For each possible global state, calculate the trace until a cycle is detected and store in a dictionary
    for i in range(num_states):
        # Initialize the trace with the starting state and an empty set to track seen states
        start_state = bin(i)[2:].zfill(num_nodes)   # Convert to binary state with leading zeros to match length of global states
        
        trace = [start_state]       
        seen_states = set()
        seen_states.add(start_state) 
        
        current_state = start_state

        # Flags to control trace output
        truncated_flag = False
        attractor = None
        depth = 0

        # Loop until a cycle is detected
        while True:
            # Stop if max depth reached
            if depth >= maxDepth:
                truncated_flag = True
                break
            
            # Calculate the next state and add to trace
            next_state = globalNextState(G, current_state)
            trace.append(next_state)
            depth += 1

            # Check for cycle and handle based on flags
            if next_state in seen_states:
                # Extract the cycle from the trace
                cycle_start_index = trace.index(next_state)
                cycle = trace[cycle_start_index:-1]         # "-1" excludes the repeated state at the end of the cycle

                # Canonical reorder the cycle if flag is set
                if canonicalOrder and len(cycle) > 1:
                    cycle = canonicalReorder(cycle)

                # If only cyclic attractors are desired, break if cycle is a fixed point
                if cyclicOnly and len(cycle) == 1:
                    break
                else:
                    attractor = cycle

                break

            seen_states.add(next_state)
            current_state = next_state

        all_traces[start_state] = {
            "trace": trace,
            "truncated": truncated_flag,
            "attractor": attractor
        }

    return all_traces

# ------
# Attractors
# ------

'''
def detectAttractors(G):

    all_traces = runAllTraces(G)

    attractors = {}

    pass
'''


# ------
# Draw Diagrams
# ------

def drawWiringDiagram(G, filename):
    drawDiagram(G, filename, "_WiringDiagram.png")

def drawStateGraph(state_trans, filename):
    SG = nx.DiGraph()               # Create a directed graph to represent the state transition graph

    for state, next_state in state_trans.items():
        SG.add_edge(state, next_state)

    drawDiagram(SG, filename, "_StateGraph.png")

'''
# ------
# Save to File
# ------

def saveTracesToFile(all_traces):
    filename = "traces.txt"
    with open(filename, "w") as file:
        file.write(f"Traces for each initial state:\n\n")
            
        for start_state, trace in all_traces.items():
            file.write(f"{start_state}: " + " -> ".join(trace) + "\n")

    print(f"Traces saved to {filename}")

    
def saveAttractorsToFile(attractors):
    pass
'''


# ------
# Main
# ------

def main():
    filename = 'ExampleBoolNet1.txt'

    G = loadNetworkFromFile(filename)
    print("Network: ", G)

    drawWiringDiagram(G, filename)
 
    state_trans = compileStateTransitions(G)
    drawStateGraph(state_trans, filename)

    '''
    # Run all traces and print them
    all_traces = runAllTraces(G)
    saveTracesToFile(all_traces)
    '''
main()