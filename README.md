# networks-final-project

There is a lot of redundant code here. I messed around with a few things before landing on my final idea that I moved forward with.

### adj_list.py
Converts the `GetAlongWith_W1.csv` to an adjacency list. Produces two files: `friendship_adj_list.adjlist` and `power_adj_list.adjlist`

### add_metadata.py
This writes metadata to a file

### add_nodes_to_network.py
This script contains a function that will create the graph with all edges and all metadata. First it builds a dictionary for the metadata, then it adds 


### GetAlongWith_W1.csv
Binary adjacency matrix where 1 indicates frieship between i and j, and 0 indicates no friendship. Provided by PINS authors.

### PINS_Schneider_Data.csv
Metadata for prisoners
