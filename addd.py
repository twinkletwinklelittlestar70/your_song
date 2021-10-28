import warnings
import json
import spotipy
import spotipy.util as util
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import csv

from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

username='tlfzphv6cc0volzv1qdzci27f'
scope = 'user-library-read'
token=util.prompt_for_user_token(username,scope,
                           client_id='ee40b06ffa5b4805b660249f36c7ba86',
                           client_secret='69a5ac016de34073b06c775f10cfe48c',
                           redirect_uri='http://localhost:8080/callback/')
#print(token)
#BQAzVGaXSahc0wCXXItq5Kjf5R_Iw0LLOlUC_huL0NpKbBAQMTARjqvB18-FZeFevv--KOb9KQBA7rnYejnZ98Nl9q9O5_pMrnjaFSv9hJ1QysSLz5Y6KBu-UozFeNPMo5xMpVT1C7ClgQsCeAfWjuKsYAn1ZKJirjuxR9h1508sCJU
headers = {"Authorization": "Bearer {}".format(token)}

'''curl --request GET \
    'https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V' \
     --header "Authorization: Bearer BQAzVGaXSahc0wCXXItq5Kjf5R_Iw0LLOlUC_huL0NpKbBAQMTARjqvB18-FZeFevv--KOb9KQBA7rnYejnZ98Nl9q9O5_pMrnjaFSv9hJ1QysSLz5Y6KBu-UozFeNPMo5xMpVT1C7ClgQsCeAfWjuKsYAn1ZKJirjuxR9h1508sCJU"
'''
responses = requests.get("https://api.spotify.com/v1/playlists/0naegdQ8iUGp2Hp3V31jCH", headers=headers)
myjson_data = json.loads(responses.text)

#print(myjson_data)

my_songs_attributes = []
my_songs_names = []
artists = []
song_genres = []
def get_song_attributes(response_text):
    return json.loads(response_text)

for item in myjson_data.get('tracks')['items']:
    song_ids = item['track']['uri'].split(':')[2]
    song_name = item['track']['name']
    artis = item['track']['artists']
    #genress = item['track']['genres']

    song_attributes = requests.get(f"https://api.spotify.com/v1/audio-features/{song_ids}", headers=headers)
    #song_genres = requests.get(f"https://api.spotify.com/v1/tracks/{song_ids}", headers=headers)
    #song_genres = json.loads(song_genres.text)
    my_songs_attributes.append(get_song_attributes(song_attributes.text))
    my_songs_names.append(song_name)
    artists.append(artis)
    #song_genres.append(genress)
#print(song_genres)
#print(artists[1])
ar_name = []
for artist in artists:
    artist_a = artist[0]
    artist_b = artist_a['name']
    ar_name.append(artist_b)
#print(ar_name)




#print(song_artist)
my_songs = pd.DataFrame(my_songs_attributes)
my_songs['song_name'] = my_songs_names
my_songs['artist'] = ar_name
#my_songs['genres'] = song_genres
total_songs = pd.concat([my_songs]).reset_index(drop=True)
#print(total_songs)
total_songs.to_csv("rnb16.csv")

#head=['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','type','id','uri','track_href','analysis_url','duration_ms','time_signature']

