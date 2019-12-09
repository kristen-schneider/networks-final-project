import networkx as nx
import matplotlib.pyplot as plt

def main():
    friendship_edges = 'friendship_adj_list.adjlist'
    friendship_metadata = 'friendship_metadata.txt'
    power_edges = 'power_adj_list.adjlist'
    power_metadata = 'power_metadata.txt'

    friendship_metadata_dictionary = read_adj_file(friendship_edges)
    friendship_metadata_dictionary = add_meta_data(friendship_metadata, friendship_metadata_dictionary)
    G = add_network_nodes(friendship_edges, friendship_metadata_dictionary)
    #G.remove_nodes_from(list(nx.isolates(G)))
    nx.draw(G)
    plt.show()


def read_adj_file(file_name):
    adj_file = open(file_name)

    metadata_dictionary = {}
    for line in adj_file:
        A = line.rstrip().split()
        for i in range(len(A)):
            if i == 0: metadata_dictionary[A[0]] = []
            #else: metadata_dictionary[A[0]][0].append(A[i])
    adj_file.close()
    return metadata_dictionary


def add_meta_data(file_name, metadata_dictionary):

    m_file = open(file_name)
    for line in m_file:
        A = line.rstrip().split()
        metadata_dictionary[A[0]].append(A[1])
        metadata_dictionary[A[0]].append(A[2].split()[0])
        metadata_dictionary[A[0]].append(A[3])

    return metadata_dictionary


def add_network_nodes(edges, metadata_dictionary):
    e = open(edges, 'r')

    G = nx.DiGraph()
    for line in e:
        # get one node from this line
        A = line.rstrip().split('\t')
        ID = A[0]
        neighbors = A[1:]
        metadata = metadata_dictionary[ID]

        # add node to network
        G.add_node(ID, age=metadata[0], race=metadata[1], daysonunit=metadata[2])
        for n in neighbors: G.add_edge(ID, n)

    e.close()
    return G

main()