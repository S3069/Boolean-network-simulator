import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"
import graphviz

def manualInputNodes():
    num_nodes = int(input("How many nodes? "))

    ttables = {}
    print("Enter the Boolean tables in the format: node_letter, neighbour,neighbour (comma-separated), Boolean truthtable (e.g. 1001).")

    for num in range(0,num_nodes):

        print("\nNode {}".format(num))
        node_letter = input("Letter: ").upper().strip()

        # Split neighbourhood into tuple
        node_neighbourhood = tuple(input("Neighbourhood: ").upper().replace(" ", "").strip().split(","))

        ttable_len_pass = False
        while(not ttable_len_pass):
            node_ttable = input("Truthtable: ").replace(" ", "").replace(",", "").strip()

            # Validate the truthtable matches length of neighbourhood
            expected_length = 2**len(node_neighbourhood)
            if len(node_ttable) == expected_length:
                ttable_len_pass = True
            else:
                raise ValueError(f"The truthtable does not match expected length for {len(node_neighbourhood)} neighbours.")

        # Convert truthtable to hex
        # node_ttable_hex = format(int(node_ttable, 2), "x")

        ttables[node_letter] = {
            "neighbours": node_neighbourhood,
            "truthtable": node_ttable
        }

    return ttables

def fileInputNodes(filename):
    ttables = {}

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if len(line) == 0:
                continue
            
            node_letter, node_neighbourhood, node_ttable = line.split(",")

            node_letter = node_letter.upper().strip()
            node_neighbourhood = tuple(node_neighbourhood.upper().strip().split())

            # Validate the truthtable matches length of neighbourhood
            expected_length = 2**len(node_neighbourhood)
            if len(node_ttable) != expected_length:
                raise ValueError(f"The truthtable does not match expected length for node {node_letter}.")

            ttables[node_letter] = {
                "neighbours": node_neighbourhood,
                "truthtable": node_ttable
            }

    return ttables

def nextNodeState(node, current_g_state, ttables, node_order):
    # This function should calculate, based on the node's truthtable of neighbours, what the next state of the node should be
    
    # Numbers the alphabetically sorted letters and maps them to the current global state in a dictionary
    state_map = {}
    for i, letter in enumerate(node_order):
        state_map[letter] = current_g_state[i]

    # Compile the neighbours' states
    neighbours = ttables[node]["neighbours"]
    neighbour_bits = "".join(state_map[nb] for nb in neighbours)
    index = int(neighbour_bits, 2)
    
    # Find this node's state using the truth table
    new_state = ttables[node]["truthtable"][index]

    return new_state

def nextGlobalState(ttables, current_g_state):
    # This function calculates the next global state based on the current global state.
    # It calls nextNodeState for each letter, passing in this current global state each time
    
    # Alphabetical node order used
    node_order = sorted(ttables.keys())
    
    # Find next state of each node and compile
    next_g_states = []
    for node in node_order:
        next_g_states.append(nextNodeState(node, current_g_state, ttables, node_order))
    next_g_state = "".join(next_g_states)

    # return next global state
    return next_g_state

def allStateTransitions(ttables):
    num_nodes = len(ttables)
    num_states = 2 ** num_nodes

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

'''
def runAllTraces(ttables):
    num_nodes = len(ttables)
    num_states = 2 ** num_nodes

    all_traces = {}

    for i in range(num_states):
        # Need to convert to binary state with leading zeros to match length of global states
        bin_state = bin(i)[2:].zfill(num_nodes)


    return all_traces
'''

def main():
    filename = 'ExampleBoolNet1.txt'

    ttables = fileInputNodes(filename)
    print("Truthtable of all nodes: ", ttables)

    state_trans = allStateTransitions(ttables)

    dot = drawStateGraph(state_trans)


main()