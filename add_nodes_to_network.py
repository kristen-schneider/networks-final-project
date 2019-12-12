import networkx as nx
import matplotlib.pyplot as plt
from louvain_community_detection import louvain_community


def main():
    friendship_edges = 'friendship_adj_list.adjlist'
    friendship_metadata = 'friendship_metadata.txt'
    power_edges = 'power_adj_list.adjlist'
    power_metadata = 'power_metadata.txt'

    friendship_metadata_dictionary = read_adj_file(friendship_edges)
    friendship_metadata_dictionary = add_meta_data(friendship_metadata, friendship_metadata_dictionary)
    G = add_network_nodes(friendship_edges, friendship_metadata_dictionary)
    groups = louvain_community(G)
    G = add_groups(G, groups)

    plot_network(G)

     # #G.remove_nodes_from(list(nx.isolates(G)))
    # nx.draw(G)
    # plt.show()


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

def add_groups(G, groups):
    for n in groups:
        G.nodes[n]['group'] = groups[n]
    return G

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

# def count_group_info(G):
#     for n in G:



def plot_network(G):
    G.remove_nodes_from(list(nx.isolates(G)))
    print(G.number_of_edges())
    print(G.number_of_nodes())

    d = dict(G.degree)

    pos = nx.spring_layout(G)

    group1_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').iteritems() if block == 0]
    group2_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').iteritems() if block == 1]
    group3_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').iteritems() if block == 2]
    group4_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').iteritems() if block == 3]
    group5_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').iteritems() if block == 4]
    group6_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').iteritems() if block == 5]
    group7_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').iteritems() if block == 6]
    group8_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').iteritems() if block == 7]

    # nx.draw(G, pos)
    nx.draw_networkx_nodes(G, pos, nodelist=group1_nodes, node_size=[v * 10 for v in d.values()], node_color='green')
    nx.draw_networkx_nodes(G, pos, nodelist=group2_nodes, node_size=[v * 10 for v in d.values()], node_color='blue')
    nx.draw_networkx_nodes(G, pos, nodelist=group3_nodes, node_size=[v * 10 for v in d.values()], node_color='pink')
    nx.draw_networkx_nodes(G, pos, nodelist=group4_nodes, node_size=[v * 10 for v in d.values()], node_color='purple')
    nx.draw_networkx_nodes(G, pos, nodelist=group5_nodes, node_size=[v * 10 for v in d.values()], node_color='yellow')
    nx.draw_networkx_nodes(G, pos, nodelist=group6_nodes, node_size=[v * 10 for v in d.values()], node_color='red')
    nx.draw_networkx_nodes(G, pos, nodelist=group7_nodes, node_size=[v * 10 for v in d.values()], node_color='orange')
    nx.draw_networkx_nodes(G, pos, nodelist=group8_nodes, node_size=[v * 10 for v in d.values()], node_color='black')

    nx.draw_networkx_edges(G, pos, edge_color='grey')
    plt.title('groups')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('groups.png')
    plt.show()

main()