'''
PART 1: ETL the dataset and save in `data/`

Here is the imbd_movie data:
https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true

It is in JSON format, so you'll need to handle accordingly and also figure out what's the best format for the two analysis parts. 
'''

import os
import pandas as pd
import requests

# Create '/data' directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(data_dir, exist_ok=True)

# Load datasets and save to '/data'

def extract_data():
    """Extracts the json data from the provided URL"""
    url = 'https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true'
    response = requests.get(url)

    if response.status_code == 200:
        data = pd.read_json(url, lines=True)
        data.to_json('data/imbd_movies.ndjson', orient='records', lines=True)
    else:
        print("Broken URL")




# if __name__ == "__main__":
#     extract_data()
