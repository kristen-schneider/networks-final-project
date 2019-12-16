import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import add_nodes_to_network as antn
from louvain_community_detection import louvain_community

def main():

    #Infering Power from Friendship
    FG, PG = create_graphs()
    FG = add_power_attribute(FG,PG)
    create_power_plot(FG)
    FG = add_centrality_attributes(FG)
    power_rank = create_metadata_list(FG,'power')
    plot_power_ranking_heatmap(FG)

    #Power in Prison Communities
    FG_groups = louvain_community(FG)
    FG = antn.add_groups(FG, FG_groups)
    top_nodes = find_top_nodes(power_rank)
    plot_prison_network_power_comm(FG,top_nodes)

    #Power in School Communities
    fh=open("school_weighted_edgelist.txt", 'rb')
    SFG=nx.read_edgelist(fh,create_using=nx.DiGraph(),delimiter = ' ',data=(('weight',float),))
    fh.close()
    school_top_nodes = analyze_school_network(SFG)
    plot_school_network_power_comm(SFG,school_top_nodes)
    

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
    graph.remove_nodes_from(list(nx.isolates(graph)))

    fig = plt.figure(figsize = (15,15))
    pos = nx.spring_layout(graph, iterations=200, k = 2)
    nx.draw_networkx_nodes(G = graph, pos = pos, nodelist = [x for x in graph.nodes() if graph.nodes[x]['race'] == '1'],
		                       node_color = 'r', alpha = 0.9,
		                       node_size = [(graph.nodes[x]['power']*20) + 40  for x in graph.nodes() if graph.nodes[x]['race'] == '1'])
    nx.draw_networkx_nodes(G = graph, pos = pos, nodelist = [x for x in graph.nodes() if graph.nodes[x]['race'] == '2'],
		                       node_color = 'g', alpha = 0.9,
		                       node_size = [(graph.nodes[x]['power']*20) + 40  for x in graph.nodes() if graph.nodes[x]['race'] == '2'])
    nx.draw_networkx_nodes(G = graph, pos = pos, nodelist = [x for x in graph.nodes() if graph.nodes[x]['race'] == '3'],
		                       node_color = 'b', alpha = 0.9,
		                       node_size = [(graph.nodes[x]['power']*20) + 40  for x in graph.nodes() if graph.nodes[x]['race'] == '3'])

    nx.draw_networkx_edges(G = graph, pos = pos, alpha = .3)

    line1 = mlines.Line2D(range(1), range(1), color="white", marker='o', markerfacecolor="red")
    line2 = mlines.Line2D(range(1), range(1), color="white", marker='o',markerfacecolor="green")
    line3 = mlines.Line2D(range(1), range(1), color="white", marker='o',markerfacecolor="blue")
    plt.legend((line1, line2, line3), ('White', 'Black', 'Hispanic'))

    plt.show()

def add_centrality_attributes(friendship_graph):
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

    #betweenness centrality
    bet = nx.betweenness_centrality(friendship_graph)
    nx.set_node_attributes(friendship_graph, bet, 'bet')

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

def plot_power_ranking_heatmap(FG):
    eigen_diff = compare_power_rankings(FG, 'eigen')
    harmonic_diff = compare_power_rankings(FG, 'harmonic')
    in_diff = compare_power_rankings(FG, 'in')
    out_diff = compare_power_rankings(FG, 'out')
    bet_diff = compare_power_rankings(FG, 'bet')
    power_rank = create_metadata_list(FG,'power') #use first 18

    heatmap_data = format_heat_map_data(power_rank,eigen_diff,harmonic_diff,in_diff,out_diff,bet_diff)
    y_labels = ['eigen','harmonic','in','out', 'betweenness']
    x_labels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
    create_power_heat_map(np.transpose(heatmap_data), x_labels, y_labels)


def format_heat_map_data(power_list, cent1, cent2, cent3, cent4, cent5):
    top_nodes = find_top_nodes(power_list)

    cent1_subset = get_id_subset(cent1)
    cent2_subset = get_id_subset(cent2)
    cent3_subset = get_id_subset(cent3)
    cent4_subset = get_id_subset(cent4)
    cent5_subset = get_id_subset(cent5)

    heatmap_data = np.zeros((18,5))
    for j in range(len(top_nodes)):
        heatmap_data[j,0] = cent1[cent1_subset.index(top_nodes[j])][1]
        heatmap_data[j,1] = cent2[cent2_subset.index(top_nodes[j])][1]
        heatmap_data[j,2] = cent3[cent3_subset.index(top_nodes[j])][1]
        heatmap_data[j,3] = cent4[cent4_subset.index(top_nodes[j])][1]
        heatmap_data[j,4] = cent5[cent5_subset.index(top_nodes[j])][1]
    
    return heatmap_data 

def find_top_nodes(power_list):
    top_nodes = []
    for i in range(18):
        top_nodes.append(power_list[i][0])

    return top_nodes

def get_id_subset(attrib_list):
    subset = []
    for i in range(len(attrib_list)):
        subset.append(attrib_list[i][0])

    return subset

def create_power_heat_map(data, y_labels, x_labels):
    fig, ax = plt.subplots(figsize=(15, 3))

    im, cbar = heatmap(data, x_labels, y_labels, ax=ax, cmap= "coolwarm", cbarlabel= "Diffenece in Rank", vmax = 170)
    texts = annotate_heatmap(im, valfmt="{x:0.0f}",size=12)

    plt.show()

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    # FROM THE MATPLOTLIB 
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)
    plt.rcParams.update({'font.size': 15})

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    plt.rc('xtick', labelsize=15) 
    plt.rc('ytick', labelsize=15) 

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "black"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

def plot_prison_network_power_comm(G, top_nodes):
    G.remove_nodes_from(list(nx.isolates(G)))
    print(G.number_of_edges())
    print(G.number_of_nodes())

    d = dict(G.degree)
    fig = plt.figure(figsize=(10,10))

    pos = nx.spring_layout(G,iterations=200, k = 2)

    group1_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 0]
    group2_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 1]
    group3_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 2]
    group4_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 3]
    group5_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 4]
    group6_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 5]
    group7_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 6]
    group8_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 7]

    nx.draw_networkx_nodes(G, pos, nodelist=group1_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group1_nodes], 
                            node_color='green')
    nx.draw_networkx_nodes(G, pos, nodelist=group2_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group2_nodes], 
                            node_color='blue')
    nx.draw_networkx_nodes(G, pos, nodelist=group3_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group3_nodes], 
                            node_color='pink')
    nx.draw_networkx_nodes(G, pos, nodelist=group4_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group4_nodes], 
                            node_color='purple')
    nx.draw_networkx_nodes(G, pos, nodelist=group5_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group5_nodes], 
                            node_color='yellow')
    nx.draw_networkx_nodes(G, pos, nodelist=group6_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group6_nodes], 
                            node_color='red')
    nx.draw_networkx_nodes(G, pos, nodelist=group7_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group7_nodes], 
                            node_color='orange')
    nx.draw_networkx_nodes(G, pos, nodelist=group8_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group8_nodes], 
                            node_color='black')

    nx.draw_networkx_edges(G, pos, edge_color='grey', alpha = .3)
    plt.title('Prison Groups')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('P_groups.png')
    plt.show()

def analyze_school_network(SFG):
    SFG = add_centrality_attributes(SFG)
    groups = louvain_community(SFG)
    SFG = antn.add_groups(SFG, groups)
    in_list_school = create_metadata_list(SFG,'in')
    school_top_nodes = []
    for i in range(len(in_list_school)):
        if in_list_school[i][1]>.1:
            school_top_nodes.append(in_list_school[i][0])
    return school_top_nodes

def plot_school_network_power_comm(G, top_nodes):
    G.remove_nodes_from(list(nx.isolates(G)))
    print(G.number_of_edges())
    print(G.number_of_nodes())

    d = dict(G.degree)
    fig = plt.figure(figsize=(10,10))

    pos = nx.spring_layout(G,iterations=200, k = 2)

    group1_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 0]
    group2_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 1]
    group3_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 2]
    group4_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 3]
    group5_nodes = [n for (n, block) in nx.get_node_attributes(G, 'group').items() if block == 4]

    nx.draw_networkx_nodes(G, pos, nodelist=group1_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group1_nodes], 
                            node_color='green')
    nx.draw_networkx_nodes(G, pos, nodelist=group2_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group2_nodes], 
                            node_color='blue')
    nx.draw_networkx_nodes(G, pos, nodelist=group3_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group3_nodes], 
                            node_color='pink')
    nx.draw_networkx_nodes(G, pos, nodelist=group4_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group4_nodes], 
                            node_color='purple')
    nx.draw_networkx_nodes(G, pos, nodelist=group5_nodes, 
                            node_size=[200 if x in top_nodes else 40 for x in group5_nodes], 
                            node_color='yellow')

    nx.draw_networkx_edges(G, pos, edge_color='grey', alpha = .3)
    plt.title('Schoolboy Groups')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('S_groups.png')
    plt.show()

main()