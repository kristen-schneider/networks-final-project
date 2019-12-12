# import community
# import networkx as nx
# import matplotlib.pyplot as plt
#
# #better with karate_graph() as defined in networkx example.
# #erdos renyi don't have true community structure
# G = nx.erdos_renyi_graph(30, 0.05)
#
# #first compute the best partition
# partition = community.best_partition(G)
#
# #drawing
# size = float(len(set(partition.values())))
# pos = nx.spring_layout(G)
# count = 0.
# for com in set(partition.values()) :
#     count = count + 1.
#     list_nodes = [nodes for nodes in partition.keys()
#                                 if partition[nodes] == com]
#     nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
#                                 node_color = str(count / size))
#
#
# nx.draw_networkx_edges(G, pos, alpha=0.5)
# plt.show()
#

# from add_nodes_to_network import *
import community
import networkx as nx

def louvain_community(G):
    G = G.to_undirected()
    G.remove_nodes_from(list(nx.isolates(G)))
    partition = community.best_partition(G)

    return partition

    # friendship_edges = 'friendship_adj_list.adjlist'
    # friendship_metadata = 'friendship_metadata.txt'
    # power_edges = 'power_adj_list.adjlist'
    # power_metadata = 'power_metadata.txt'
    #
    # friendship_metadata_dictionary = read_adj_file(friendship_edges)
    # friendship_metadata_dictionary = add_meta_data(friendship_metadata, friendship_metadata_dictionary)
    # G = add_network_nodes(friendship_edges, friendship_metadata_dictionary)
    #
    # G = G.to_undirected()
    # G.remove_nodes_from(list(nx.isolates(G)))
    # partition = community.best_partition(G)
    #
    # size = float(len(set(partition.values())))
    # pos = nx.spring_layout(G)
    # count = 0.
    # for com in set(partition.values()):
    #     count = count + 1.
    #     list_nodes = [nodes for nodes in partition.keys()
    #                   if partition[nodes] == com]
    #     nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
    #                            node_color=str(count / size))
    #
    # number_groups = []
    # print type(partition.values())
    # for v in partition.keys():
    #     if partition[v] not in number_groups: number_groups.append(partition[v])
    # # number_groups.append(partition[v] for v in partition.keys() if partition[v] not in number_groups)
    # print number_groups
    #
    # nx.draw_networkx_edges(G, pos, alpha=0.5)
    # plt.show()
    #
    # # nx.draw(G)
    # # plt.show()