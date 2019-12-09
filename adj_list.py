import networkx as nx
import matplotlib.pyplot as plt


def main():
    friendship_file = 'GetAlongWith_W1.csv'
    power_file = 'PowerInfluence_W1.csv'

    prisoner_IDs = make_ID_dictionary(friendship_file)
    make_adj_list(prisoner_IDs, friendship_file, 'friendship')
    make_adj_list(prisoner_IDs, power_file, 'power')

    # generate_graph('/Users/kristen/PycharmProjects/FinalProject/friendship_adj_list.adjlist')
    #
    # G = nx.read_adjlist('/Users/kristen/PycharmProjects/FinalProject/friendship_adj_list.adjlist')
    # nx.draw(G)
    # plt.show()


# k = open('family.adjlist')
    # for line in k:
    #     for l in line: print type(l)
    #
    # m = open('friendship_adj_list.adjlist')
    # for line in m:
    #     for l in line: print type(l)



def make_ID_dictionary(input):
    input_file = open(input)

    header = None
    for line in input_file:
        A = line.rstrip().split(',')
        if header == None: header = A

        # dictionary = ID: index
        prisoner_IDs = {}
        i = 0
        for h in header:
            prisoner_IDs[i] = h
            i += 1
    input_file.close()
    return prisoner_IDs

def make_adj_list(prisoner_IDs, input, title):
    input_file = open(input)
    edge_list = open(title+'_adj_list.adjlist', 'w')

    header = None
    for line in input_file:
        A = line.rstrip().split(',')
        if header == None: header = A
        else:
            edge_list.write(A[0] + '\t')
            for i in range(len(A)):
                if int(A[i]) == 1:
                    edge_list.write(str(prisoner_IDs[int(i)] + '\t'))
            edge_list.write('\n')

    input_file.close()
    return edge_list

def generate_graph(adjList):
    G = nx.Graph()

    f = open(adjList)

    # generate graph from adj list
    for line in f:
        A = line.rstrip().split()

        # add new node (ADD ATTRIBUTE HERE)
        if A[0] not in G.nodes: G.add_node(A[0])
        for i in range(len(A)):
            # add new edge
            if i != 0: G.add_edge(A[0], A[i])

    G.remove_nodes_from(list(nx.isolates(G)))

    # G = nx.read_adjlist('family.adjlist')
    nx.draw(G)
    plt.show()



main()