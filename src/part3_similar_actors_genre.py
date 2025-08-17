'''
PART 2: SIMILAR ACTROS BY GENRE

Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

import pandas as pd
import numpy as np

from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances
from collections import defaultdict
from datetime import datetime

def get_actors(movie_actors):
        """Extracts only the actors name for each actor in a movie and stores the names in a list"""
        actor_names = []
        for actor_info in movie_actors:
            actor = actor_info[1]
            actor_names.append(actor)

        return actor_names


def create_feature_matrix():
        """Creates the feature matrix from the movie json dataset"""
    
        data = pd.read_json('data/imbd_movies.ndjson', lines=True)
        actors = data['actors']
        genres = data['genres']

        # Gets all the unique genres
        all_genres = set(genre for sublist in genres for genre in sublist)
        all_genres.pop() # removes '' genre
        all_actors = set(actor_info[1] for sublist in actors for actor_info in sublist)
        # Nested dictionary where the key value pairs are actor name and the initialized genre_dict (with default counts of 0)
        actors_dict = defaultdict(lambda: defaultdict(int))
   
        for __, movie in tqdm(data.iterrows(), total=len(data), desc="processing data"):
              movie_actors_names = get_actors(movie['actors']) # gets all names of actors in the movie
              movie_genres = movie['genres'] # gets all genres associated with that movie
              movie_genres = [m for m in movie['genres'] if m != ''] # removes the '' genre

              for actor_name in all_actors:
                        if actor_name in movie_actors_names:
                               for genre in movie_genres:
                                      actors_dict[actor_name][genre] += 1

        # Export dict to data frame to csv
        feature_matrix = pd.DataFrame.from_dict(actors_dict, orient='index')
        feature_matrix.fillna(0, inplace=True)
        feature_matrix.reset_index(names = "actor_name", inplace=True)



        return feature_matrix
                                

def get_cos_similarity(feature_matrix, query):
       """Gets cosine similarity for a query vector and exports to a csv
       
       Parameters:
       -feature matrix: the feature matrix developed in create_feature_matrix
       -query: a string represetning an actors name
       
       Returns:
       - similarity_actors_genre: data frame with the top 10 most similar actors to the query"""
       
       query_vector = feature_matrix[feature_matrix['actor_name'] == query]
       query_vector = np.array(query_vector.drop(columns = 'actor_name'))

       actor_names = list(feature_matrix['actor_name'])
       feature_matrix = np.array(feature_matrix.drop(columns = 'actor_name'))


       distances = cosine_distances(feature_matrix, query_vector)
       
       similarity_actors_genre = pd.DataFrame(distances, columns = ['distance'])
       similarity_actors_genre['actor_name'] = actor_names
       similarity_actors_genre['similarity'] = 1 - similarity_actors_genre['distance']
       similarity_actors_genre.sort_values(by = 'distance', ascending=True, inplace=True)
       similarity_actors_genre = similarity_actors_genre.head(10)
       current_datetime = datetime.now()
       similarity_actors_genre.to_csv(f'data/similar_actors_genre_{current_datetime}.csv', index = False)

       return similarity_actors_genre

              
def get_euclidean_dist(feature_matrix, query):
       """Gets euclidean for a query vector and exports to a csv
       
       Parameters:
       -feature matrix: the feature matrix developed in create_feature_matrix
       -query: a string represetning an actors name
       
       Returns:
       - similarity_actors_genre: data frame with the top 10 most similar actors to the query"""
       
       query_vector = feature_matrix[feature_matrix['actor_name'] == query]
       query_vector = np.array(query_vector.drop(columns = 'actor_name'))

       actor_names = list(feature_matrix['actor_name'])
       feature_matrix = np.array(feature_matrix.drop(columns = 'actor_name'))


       distances = euclidean_distances(feature_matrix, query_vector)
       
       similarity_actors_genre = pd.DataFrame(distances, columns = ['distance'])
       similarity_actors_genre['actor_name'] = actor_names
       similarity_actors_genre.sort_values(by = 'distance', ascending=True, inplace=True)
       similarity_actors_genre = similarity_actors_genre.head(10)
       current_datetime = datetime.now()
       similarity_actors_genre.to_csv(f'data/similar_actors_genre_euclidean_{current_datetime}.csv', index = False)

       return similarity_actors_genre
        


# if __name__ == "__main__":
#     FM = create_feature_matrix()
#     print(FM.head(10))
#     get_cos_similarity(FM, 'Chris Hemsworth')
#     get_euclidean_dist(FM, 'Chris Hemsworth')

