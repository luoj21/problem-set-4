'''
You will run this problem set from main.py, so set things up accordingly
'''

import part1_etl as etl
import part2_network_centrality as nc
import part3_similar_actors_genre as sag

# Call functions / instanciate objects from the .py files
def main():
    # PART 1: Instanciate etl, saving the dataset in `./data/`
    etl.extract_data()

    # PART 2: Call functions/instanciate objects for the network centrality analysis
    G = nc.build_graph()
    nc.get_top_10_central_nodes(G)

    # PART 3: Call functions/instanciate objects for similar actors by genre
    FM = sag.create_feature_matrix()
    top10_cos_sim = sag.get_cos_similarity(feature_matrix= FM, query='Chris Hemsworth')
    top10_euc_sim = sag.get_euclidean_dist(feature_matrix= FM, query='Chris Hemsworth')

    print(top10_cos_sim)
    print(top10_euc_sim)
    print("The list changes based of Euclidean distance as the top 2 most similar stay the same, but the other actors differ")

if __name__ == "__main__":
    main()