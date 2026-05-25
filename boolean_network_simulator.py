from fileinput import filename
from inspect import trace
from pathlib import Path

import networkx as nx
# import matplotlib.pyplot as plt
import pygraphviz as pgv

# ------
# Helper Functions: Draw and name generated files
# ------

def replaceExtension(filename, new_extension):
    """
    Replace the extension of a filename with a new extension, even if there are multiple extensions.

    Inputs:
    - filename: the original filename to be modified
    - new_extension: the new extension to replace the original extension(s)

    Output:
    - new_filename: the modified filename with the new extension

    Source - https://stackoverflow.com/a/56807917
    Posted by Michael Hall, modified by community. See post 'Timeline' for change history
    Retrieved 2026-03-24, License - CC BY-SA 4.0
    """

    path = Path(filename)
    current_extensions = "".join(path.suffixes)             # Compile all extensions as a single string to replace
    new_filename = str(path).replace(current_extensions, new_extension)

    return new_filename

def saveImageBytes(image_bytes, filename, new_extension):
    """
    Save image bytes to a file.

    Inputs:
    - image_bytes: the image data in bytes format
    - filename: the path of the original network file. The output file name will be based on this.
    - new_extension: the new extension that will replace the original extension(s) for the output file

    Output:
    - filelocation: the location of the saved file
    """
    output_path = replaceExtension(filename, new_extension)

    with open(output_path, 'wb') as f:
        f.write(image_bytes)

    return output_path

def getGraphImageBytes(graph):
    """
    Draw the graph using pygraphviz and return the image as bytes.

    Input:
    - graph: a NetworkX graph object to be drawn

    Output:
    - image_bytes: the image of the drawn graph in bytes format
    """
    A = nx.nx_agraph.to_agraph(graph)
    A.layout(prog='dot')
    return A.draw(format='png')

def getGraphSVGBytes(graph):
    """
    Draw the graph using pygraphviz and return the image as SVG bytes.

    Input:
    - graph: a NetworkX graph object to be drawn

    Output:
    - svg_bytes: the image of the drawn graph in SVG bytes format
    """
    A = nx.nx_agraph.to_agraph(graph)
    A.layout(prog='dot')
    return A.draw(format='svg')

def createStateGraph(state_trans):
    """
    Create a NetworkX graph object representing the state transition graph of the Boolean network.

    Input:
    - state_trans: a dictionary representing the state transition graph, mapping each global state (as a binary string) to its next global state

    Output:
    - SG: a NetworkX directed graph object representing the state transition graph
    """
        
    SG = nx.DiGraph()               # Create a directed graph to represent the state transition graph

    for state, next_state in state_trans.items():
        SG.add_edge(state, next_state)

    return SG


# ------
# Helper functions: Calculate next states
# ------

def nodeNextState(node, current_g_state, G, node_order):
    """
    Calculate the next state of a given node based on the current global state and the graph structure.

    Inputs:
    - node: the node for which to calculate the next state
    - current_g_state: a binary string representing the current global state of the network
    - G: the NetworkX graph representing the Boolean network
    - node_order: a list of nodes in a consistent order to map to the global state string
    
    Output:
    - new_state: a binary character representing the next state of the specified node
    """
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

def globalNextState(G, current_g_state, node_order):
    """
    Calculate the next global state based on the current global state and the graph structure.
    
    Inputs:
    - G: the NetworkX graph representing the Boolean network
    - current_g_state: a binary string representing the current global state of the network
    - node_order: a list of nodes in a consistent order to map to the global state string

    Output:
    - next_g_state: a binary string representing the next global state of the network
    """
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
    """
    Reorder a cycle of states to a canonical form (starting with the smallest state in the cycle).
    
    Inputs:
    - cycle: a list of states representing a cyclical attractor

    Output:
    - canonical_cycle: the input cycle reordered to start with the smallest state
    """
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
    """
    Load a Boolean network from a file and create a directed graph representation.
    
    Input:
    - filename: the name of the file containing the Boolean network definition. The file should have lines in the format:
        
        NodeLetter, Neighbour1 Neighbour2 ..., TruthTable.

      For example:
        A, B C, 0001
        B, A, 01
        C, A, 10

    Output:
    - G: a directed graph where each node has attributes 'truthtable', 'neighbours', and edges to represent the influence of neighbours on the node.
    """
    # Create a directed graph to represent the Boolean network
    network_definitions = {}

    with open(filename, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            # Skip empty line(s) in file
            if len(line) == 0:
                continue

            # Validate that there is 3 comma-separated values in the line
            split_up = line.split(",")
            if len(split_up) != 3:
                raise ValueError(f"Invalid format on line {line_number}. \nEach line must use the format: NodeLetter, Neighbour1 Neighbour2 ..., TruthTable)")
            
            # Parse the line into node properties
            node_identifier, node_neighbourhood, node_ttable = split_up
            node_identifier = node_identifier.upper().strip()
            node_neighbourhood = tuple(node_neighbourhood.upper().strip().split())
            node_ttable = node_ttable.strip()


            # Validate the node identifier

            # Missing node identifier
            if node_identifier == "":
                raise ValueError(f"Missing node identifier on line {line_number}.")
            
            # Node identifier contains spaces
            if " " in node_identifier:
                raise ValueError(f"Invalid node identifier on line {line_number}. \nNode identifiers cannot contain spaces.")
            
            # Duplicate node identifier
            if node_identifier in network_definitions:
                raise ValueError(f"Duplicate node identifier '{node_identifier}' on line {line_number}. \nEach node must have a unique identifier.")


            # Validate the truthtable

            # Missing truthtable
            if node_ttable == "":
                raise ValueError(f"Missing truthtable on line {line_number}.")

            # Truthtable contains characters other than 0 and 1
            if any(char not in "01" for char in node_ttable):
                raise ValueError(f"Invalid truthtable on line {line_number}. \nTruthtable must only contain '0' and '1's.")

            # Truthtable matches length of neighbourhood
            expected_length = 2**len(node_neighbourhood)
            if len(node_ttable) != expected_length:
                raise ValueError(f"Invalid truthtable length on line {line_number}. \nTruthtable must have a length of 2^n where n is the number of neighbours. \nExpected length for node '{node_identifier}' with {len(node_neighbourhood)} neighbour(s) is {expected_length}.")

            network_definitions[node_identifier] = {
                "neighbourhood": node_neighbourhood,
                "truthtable": node_ttable
            }

    # Validate that all referenced neighbours are defined as nodes in the file
    for node, node_properties in network_definitions.items():
        for neighbour in node_properties["neighbourhood"]:
            if neighbour not in network_definitions:
                raise ValueError(f"Undefined neighbour '{neighbour}' for node '{node}'. \nAll neighbours must be defined as nodes in the file.")

    # Add node definitions to new graph
    G = nx.DiGraph()  

    for node_identifier, node_properties in network_definitions.items():
        G.add_node(
            node_identifier,
            neighbours = node_properties["neighbourhood"],
            truthtable = node_properties["truthtable"]
        )
    
    # Add edges to graph
    for node_identifier, node_properties in network_definitions.items():
        for neighbour in node_properties["neighbourhood"]:
            G.add_edge(neighbour, node_identifier)          # Add directed edge from neighbour to node

    return G


# ------
# State Transition Graph
# ------

def compileStateTransitions(G):
    """
    Compile the state transition graph for a given Boolean network graph.
    
    Input:
    - G: a directed graph representing the Boolean network
    
    Output:
    - state_trans: a dictionary representing the state transition graph, mapping each global state (as a binary string) to its next global state
    """
    # Calculate the number of possible global states
    num_nodes = len(G.nodes)
    num_states = 2 ** num_nodes

    # Sort nodes and pass into globalNextState
    node_order = sorted(G.nodes)

    # For each possible global state, calculate the next global state and store in a dictionary
    state_trans = {}
    for i in range(num_states):
        bin_state = bin(i)[2:].zfill(num_nodes)     # Convert to binary state with leading zeros to match length of global states

        next_state = globalNextState(G, bin_state, node_order)
        state_trans[bin_state] = next_state
            
    return state_trans


# ------
# Traces
# ------

def runAllTraces(state_trans, cyclicOnly=False, canonicalOrder=False, maxDepth=10000):
    """
    Compile traces for all starting states in the state transition graph. Run each trace until a cycle is detected or max search depth is reached, and extract attractor information based on parameters.

    Inputs:
    - state_trans: a dictionary representing the state transition graph, mapping each global state (as a binary string) to its next global state
    - cyclicOnly: a boolean flag indicating whether to only consider cyclic attractors (default: False)
    - canonicalOrder: a boolean flag indicating whether to reorder cycles to a canonical form for comparison (default: False)
    - maxDepth: an integer specifying the maximum search depth for each trace (default: 10000)

    Output:
    - all_traces: a dictionary mapping each starting state to its trace information, including
        - "trace": the sequential list of states in the trace
        - "truncated": a boolean indicating whether the trace was truncated due to reaching maxDepth
        - "attractor": the attractor found in the trace (if any, otherwise None)
    """
    all_traces = {}                 

    # For each possible starting state, run the trace until a cycle is detected or max search depth is reached
    for start_state in state_trans:
        # Initialize trace and seen states
        trace = [start_state]       
        seen_states = {start_state}
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
            
            # Take the next state and add to trace
            next_state = state_trans[current_state]
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

                # If only cyclic attractors are desired, break if cycle is a fixed point cycle (length = 1)
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

def compileAttractors(state_trans, cyclicOnly=False, canonicalOrder=False, maxDepth=10000):
    """
    Compile attractor information from the state transition graph based on the specified parameters.
    
    Inputs:
    - state_trans: a dictionary representing the state transition graph, mapping each global state (as a binary string) to its next global state
    - cyclicOnly: a boolean flag indicating whether to only consider cyclic attractors (default: False)
    - canonicalOrder: a boolean flag indicating whether to reorder cycles to a canonical form for comparison (default: False)
    - maxDepth: an integer specifying the maximum search depth for each trace (default: 10000)

    Output:
    - attractors: a dictionary mapping each unique attractor (as a tuple of states) to its information, including
        - "id": a unique identifier for the attractor
        - "states": a sorted list of states in the attractor
        - "length": the length of the attractor (number of states in the cycle)
        - "type": a string indicating the type of attractor ("Cyclic" or "Fixed Point")
        - "basin": a list of starting states that lead to this attractor

    """

    '''
    TODO: make it optional to run all_traces if this has already been run to save time when using the UI
    '''

    # Run all traces to extract attractor information
    all_traces = runAllTraces(
        state_trans,
        cyclicOnly=cyclicOnly,
        canonicalOrder=canonicalOrder,
        maxDepth=maxDepth)

    attractors = {}
    seen_canon_attractors = {}
    attractor_id = 1

    for start_state, trace_info in all_traces.items():
        # Skip if trace was truncated or no attractor found
        if trace_info["truncated"] or trace_info["attractor"] is None:
            continue

        trace_attractor = tuple(trace_info["attractor"])
        canon_trace_attractor = tuple(canonicalReorder(list(trace_attractor)))
        
        # Compare canonical order of attractor to ensure uniqueness
        if canon_trace_attractor not in seen_canon_attractors:
            # Store unique attractor for future comparisons
            seen_canon_attractors[canon_trace_attractor] = trace_attractor

            # Add desired attractor information
            attractors[trace_attractor] = {
                "id": attractor_id,
                "states": sorted(list(trace_attractor)),
                "length": len(trace_attractor),
                "type": "Cyclic" if len(trace_attractor) > 1 else "Fixed Point",
                "basin": [start_state],
            }
            attractor_id += 1
        else:
            # If attractor already exists, add the starting state to its basin
            existing_attractor = seen_canon_attractors[canon_trace_attractor]
            attractors[existing_attractor]["basin"].append(start_state)

    return attractors


# ------
# Save Diagrams
# ------

def saveWiringDiagramSVG(svg_bytes, filename):
    """
    Save a wiring diagram in SVG format to a file.

    Inputs:
    - image_bytes: The SVG image data as bytes.
    - filename: the original filename to base the output filename on

    Output:
    - message: a string stating the location of the saved diagram. Used for UI status updates
    """

    output_path = saveImageBytes(
        image_bytes=svg_bytes,
        filename=filename,
        new_extension="_WiringDiagram.svg")

    message = f"Wiring diagram saved to {output_path}."
    return message

def saveStateGraphSVG(svg_bytes, filename):
    """
    Save a state transition graph to a file.

    Inputs:
    - svg_bytes: The SVG image data as bytes.
    - filename: the original filename to base the output filename on

    Output:
    - message: a string stating the location of the saved diagram. Used for UI status updates
    """

    output_path = saveImageBytes(
        image_bytes=svg_bytes,
        filename=filename,
        new_extension="_StateGraph.svg",
    )

    message = f"State transition graph saved to {output_path}."
    return message


# ------
# Save to File
# ------

def saveTracesToFile(all_traces, filename="", maxDepth=10000):
    """
    Save the traces for all starting states to a text file.
    
    Inputs:
    - all_traces: a dictionary mapping each starting state to its trace information, including
        - "trace": the sequential list of states in the trace
        - "truncated": a boolean indicating whether the trace was truncated due to reaching maxDepth
        - "attractor": the attractor found in the trace (if any, otherwise None)
    - filename: the original filename to base the output filename on

    Output:
    - message: a string indicating where the traces were saved used for UI status updates
    """
    filename = replaceExtension(filename, "_Traces.txt")    # Renames file to match input file

    with open(filename, "w") as file:
        file.write(f"Traces output settings:\n")
        file.write(f"Max depth: {maxDepth}\n\n")

        file.write(f"Traces for each initial state:\n\n")

        for start_state, trace_info in all_traces.items():
            file.write(f"{start_state}: " + " -> ".join(trace_info["trace"]) + "\n")

    message = f"Traces saved to {filename}."
    return message
    
def saveAttractorsToFile(attractors, filename="", maxDepth=10000, cyclicOnly=False, canonicalOrder=False):
    """
    Save the attractor information to a text file.
    
    Inputs:
    - attractors: a dictionary mapping each unique attractor (as a tuple of states) to its information, including
        - "id": a unique identifier for the attractor
        - "states": a sorted list of states in the attractor
        - "length": the length of the attractor (number of states in the cycle)
        - "type": a string indicating the type of attractor ("Cyclic" or "Fixed Point")
        - "basin": a list of starting states that lead to this attractor
    - filename: the original filename to base the output filename on

    Output:
    - message: a string indicating where the attractor information was saved used for UI status updates
    """
    filename = replaceExtension(filename, "_Attractors.txt")    # Renames file to match input file

    with open(filename, "w") as file:
        file.write(f"Attractors output settings:\n")
        file.write(f"Max depth: {maxDepth}\n")
        file.write(f"Cyclic attractors only: {cyclicOnly}\n")
        file.write(f"Canonical ordering: {canonicalOrder}\n\n")

        file.write(f"Attractors detected:\n\n")

        '''
        TODO: add settings for attractor detection/trace run to top of the file.
        '''

        if not attractors:
            file.write("No attractors detected.\n")

        else:    
            for attractor, info in attractors.items():
                attractor_seq = " -> ".join(attractor)
                file.write(f"Attractor: {attractor_seq}\n")
                file.write(f"ID: {info['id']}\n")
                file.write(f"Sorted States: {', '.join(info['states'])}\n")
                file.write(f"Length: {info['length']}\n")
                file.write(f"Type: {info['type']}\n")
                file.write(f"Basin states: {', '.join(info['basin'])}\n")
                file.write("\n")

    message = f"Attractors saved to {filename}."
    return message