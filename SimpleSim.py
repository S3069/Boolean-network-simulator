
def inputNodes():
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
                print(f"The truthtable does not match expected length for {len(node_neighbourhood)} neighbours.")

        # Convert truthtable to hex
        # node_ttable_hex = format(int(node_ttable, 2), "x")

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

    # test print
    print(f"{node} is now {new_state}")

    return new_state

def nextGlobalState(ttables):
    # This function should calculate the next global state, based on the current global state.
    # It calls nextNodeState for each letter, passing in this current global state each time
    
    # Alphabetical node order used
    node_order = sorted(ttables.keys())

    current_g_state = input(f"\nWhat is the initial global state for {"".join(node_order)}? ").replace(" ", "").replace(",", "").strip()
    
    # Find next state of each node
    next_g_state = []
    for node in node_order:
        next_g_state.append(nextNodeState(node, current_g_state, ttables, node_order))

    # Compile and return next global state
    print(f"{"".join(node_order)}: ({current_g_state}) -> ({next_g_state})")
    return next_g_state

def main():
    ttables = inputNodes()
    nextGlobalState(ttables)

main()