import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import add_nodes_to_network as antn

def main():

    FG, PG = create_graphs()
    FG = add_power_attribute(FG,PG)
    create_power_plot(FG)
    FG = add_centrality_attribures(FG)
    eigen_diff = compare_power_rankings(FG, 'eigen')
    harmonic_diff = compare_power_rankings(FG, 'harmonic')
    in_diff = compare_power_rankings(FG, 'in')
    out_diff = compare_power_rankings(FG, 'out')


def create_graphs():
    #Create Graph
    friendship_edges = 'friendship_adj_list.adjlist'
    friendship_metadata = 'friendship_metadata.txt'
    power_edges = 'power_adj_list.adjlist'
    power_metadata = 'power_metadata.txt'

    friendship_metadata_dictionary = antn.read_adj_file(friendship_edges)
    friendship_metadata_dictionary = antn.add_meta_data(friendship_metadata, friendship_metadata_dictionary)
    FG = antn.add_network_nodes(friendship_edges, friendship_metadata_dictionary)

    PG = add_power_network_nodes(power_edges)

    return FG, PG

def add_power_network_nodes(edges):
    e = open(edges, 'r')

    G = nx.DiGraph()
    for line in e:
        # get one node from this line
        A = line.rstrip().split('\t')
        ID = A[0]
        neighbors = A[1:]

        # add node to network
        G.add_node(ID)
        for n in neighbors: G.add_edge(ID, n)

    e.close()
    return G

def add_power_attribute(freindship_graph, power_graph):
    #Creates in degree dictionary
    power_in_degree_dictionary = dict(power_graph.in_degree())
    #Adds power attribute to newtork
    nx.set_node_attributes(freindship_graph, power_in_degree_dictionary, 'power')

    return freindship_graph

def create_power_plot(friendship_graph):
    graph = friendship_graph
    
    fig = plt.figure(figsize = (10,10))
    pos = nx.spring_layout(graph, iterations=200)
    nx.draw_networkx_nodes(G = graph, pos = pos, nodelist = [x for x in graph.nodes() if graph.nodes[x]['race'] == '1'],
		                       node_color = 'r', alpha = 0.8,
		                       node_size = [(graph.nodes[x]['power']*20) + 20  for x in graph.nodes() if graph.nodes[x]['race'] == '1'])
    nx.draw_networkx_nodes(G = graph, pos = pos, nodelist = [x for x in graph.nodes() if graph.nodes[x]['race'] == '2'],
		                       node_color = 'g', alpha = 0.8,
		                       node_size = [(graph.nodes[x]['power']*20) + 20  for x in graph.nodes() if graph.nodes[x]['race'] == '2'])
    nx.draw_networkx_nodes(G = graph, pos = pos, nodelist = [x for x in graph.nodes() if graph.nodes[x]['race'] == '3'],
		                       node_color = 'b', alpha = 0.8,
		                       node_size = [(graph.nodes[x]['power']*20) + 20  for x in graph.nodes() if graph.nodes[x]['race'] == '3'])

    nx.draw_networkx_edges(G = graph, pos = pos)

    line1 = mlines.Line2D(range(1), range(1), color="white", marker='o', markerfacecolor="red")
    line2 = mlines.Line2D(range(1), range(1), color="white", marker='o',markerfacecolor="green")
    line3 = mlines.Line2D(range(1), range(1), color="white", marker='o',markerfacecolor="blue")
    plt.legend((line1, line2, line3), ('race 1', 'race 2', 'race 3'))

    plt.show()

def add_centrality_attribures(friendship_graph):
    #Harmonic centrality
    hc = nx.harmonic_centrality(friendship_graph)
    nx.set_node_attributes(friendship_graph, hc, 'harmonic')

    #Eigenvector centrality
    ec = nx.eigenvector_centrality(friendship_graph)
    nx.set_node_attributes(friendship_graph, ec, 'eigen')

    #in-degree centrality
    idc = nx.in_degree_centrality(friendship_graph)
    nx.set_node_attributes(friendship_graph, idc, 'in')

    #out-degree centrality
    odc = nx.out_degree_centrality(friendship_graph)
    nx.set_node_attributes(friendship_graph, odc, 'out')

    return friendship_graph

def compare_power_rankings(graph,attribute):
    power_list = create_metadata_list(graph, 'power')
    test_list = create_metadata_list(graph,attribute)
    difference_list = find_ranking_differences(power_list,test_list)
    return difference_list

def find_ranking_differences(power_list,test_list):
    difference_list = []
    test_list_subset = []
    power_list_subset = []

    for i in range(len(power_list)):
        power_list_subset.append(power_list[i][0])
        test_list_subset.append(test_list[i][0])
    for j in range(len(power_list)):
        test_elem = test_list[j][0]
        difference = test_list_subset.index(test_elem) - power_list_subset.index(test_elem)
        difference_list.append([test_elem,difference])

    return difference_list

def create_metadata_list(graph,attribute):
    data_list = []
    for node in graph.nodes():
        data = graph.nodes[node][attribute]
        data_list.append([node,data])
    data_list.sort(key = index_sort, reverse=True)
        
    return data_list

def index_sort(data_list):
    return data_list[1]

main()