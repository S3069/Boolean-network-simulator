
def inputNodes():
    num_nodes = int(input("How many nodes? "))

    ttables = {}
    print("Enter the Boolean tables in the format: node_letter, neighbour,neighbour (comma separated), Boolean truthtable (e.g. 1001).")

    for num in range(0,num_nodes):

        print("\nNode {}".format(num))
        node_letter = input("Letter: ").upper()

        # Split neighbourhood into tuple
        node_neighbourhood = tuple(input("Neighbourhood: ").upper().split(","))

        ttable_len_pass = False
        while(not ttable_len_pass):
            node_ttable = input("Truthtable: ").replace(" ", "").replace(",", "")

            # Validate the truthtable matches length of neighbourhood
            expected_length = 2**len(node_neighbourhood)
            if len(node_ttable) == expected_length:
                ttable_len_pass = True
            else:
                print(f"The truthtable does not match expected length for {len(node_neighbourhood)} neighbours.")

        ttables[node_letter] = {
            "neighbours": node_neighbourhood,
            "truthtable": node_ttable
        }


    print(ttables)


inputNodes()
