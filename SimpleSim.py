
def inputNodes():
    num_nodes = int(input("How many nodes? "))

    truthtables = []
    print("Please enter the Boolean tables in the format: node_letter, neighbour,neighbour, (truthtable). \nOnly enter the truthtable outputs.")

    for num in range(0,num_nodes):

        print("\nNode {}".format(num))
        node_letter = input("Letter: ")
        node_neighbourhood = input("Neighbourhood: ")
        node_truthtable = input("Truthtable: ")

        new_node = node_letter + node_neighbourhood + node_truthtable
        truthtables.append(new_node)

    print(truthtables)


inputNodes()
