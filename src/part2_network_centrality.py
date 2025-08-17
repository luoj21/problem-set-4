'''
PART 2: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is inline with the standards we're using in this class 
'''

import pandas as pd
import networkx as nx
import json
from datetime import datetime

# Build the graph
G = nx.Graph()


def build_graph():
    """Builds the graph for the IMBD data set and exports the network_centrality_{current_datetime}.csv 
    
    Parameters:
    None
    
    Returns:
    - G: the graph built from the imdb ndjson data"""

    edge_rows = []
    with open('data/imbd_movies.ndjson') as in_file:
        for line in in_file:

            # Load the movie from this line
            this_movie = json.loads(line)
                
            # Create a node for every actor
            for actor_id, actor_name in this_movie['actors']:
                # add the actor to the graph  
                G.add_node(actor_name)
  
            # Iterate through the list of actors, generating all pairs
            # Starting with the first actor in the list, generate pairs with all subsequent actors
            # then continue to second actor in the list and repeat
            
            i = 0 #counter
            for left_actor_id,left_actor_name in this_movie['actors']:
                for right_actor_id,right_actor_name in this_movie['actors'][i+1:]:

                    # Get the current weight, if it exists
                    if G.has_edge(left_actor_name, right_actor_name):
                        G[left_actor_name][right_actor_name]["weight"] += 1
                    else:
                    # Add an edge for these actors
                        G.add_edge(left_actor_name, right_actor_name, weight=1)
                    i += 1

                    edge_rows.append({'left_actor_name': left_actor_name,
                                    'arrow': "<->",
                                    'right_actor_name': right_actor_name})
                    
    current_datetime = datetime.now()
    network_centrality = pd.DataFrame(edge_rows)
    network_centrality.to_csv(f'data/network_centrality_{current_datetime}.csv', index = False)

    return G


#Print the 10 the most central nodes
def get_top_10_central_nodes(G):
    """Gets top 10 most central nodes in a graph and prints the number of nodes
    
    Parameters:
    - G: a graph outputted by the build_graph method
    
    Returns:
    None"""

    print("Nodes:", len(G.nodes))
    degree_centrality = nx.degree_centrality(G)

    # Sort by value in descending order
    degree_centrality = dict(sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True))
    
    print('The top 10 most central nodes are \n')
    
    i = 0
    for key, value in degree_centrality.items():
        print(f"{i+1}.) Name: {key}, Degree Centrality: {value}")
        i += 1

        if i == 10:
            break



# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`


# if __name__ == "__main__":
#     G = build_graph()
#     get_top_10_central_nodes(G)