import pandas as pd
import numpy as np
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from time import sleep
import pytz
from iteration_utilities import unique_everseen
from pymongo import MongoClient

key_dict = {
    0 : 'C',
    1 : 'C#/Db',
    2 : 'D',
    3 : 'D#/Eb',
    4 : 'E',
    5 : 'F',
    6 : 'F#/Gb',
    7 : 'G',
    8 : 'G#/Ab',
    9 : 'A',
    10 : 'A#/Bb',
    11 : 'B'
}

mode_dict = {
    0: 'Minor',
    1: 'Major'
}

dow_dict = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

def convert_date(date):
    try:
        converted_date = datetime.strptime(date, '%Y-%m-%d')
    except:
        converted_date = datetime.strptime(date, '%Y')
    return converted_date

with open('$YOUR_PATH_TO_CREDENTIALS_JSON_FILE') as f:
    credentials = json.load(f)

scope = ['user-read-currently-playing', 'user-read-recently-played', 'user-top-read']

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials['client_id'], client_secret=credentials['client_secret'], \
                                               scope=scope, redirect_uri='http://localhost:8080'))

# Spotify API calls
recently_played = sp.current_user_recently_played(limit=50, after=None, before=None)

api_dict = dict()
history_list = list()
tracks_list = list()
albums_list = list()

for track in recently_played['items']:
    played_dict = dict()
    played_dict['track_id'] = track['track']['id']
    played_at_datetime = pytz.utc.localize(datetime.strptime(track['played_at'].split('Z')[0].split('.')[0], '%Y-%m-%dT%H:%M:%S')).astimezone(pytz.timezone('America/Sao_Paulo'))
    played_at_datetime = datetime.combine(played_at_datetime.date(), played_at_datetime.time())
    played_dict['played_at'] = {
        'full': played_at_datetime,
        'hour': played_at_datetime.hour,
        'day': played_at_datetime.day,
        'dow_number': played_at_datetime.weekday(),
        'dow_text': dow_dict[played_at_datetime.weekday()],
        'week': played_at_datetime.isocalendar()[1],
        'month': played_at_datetime.month,
        'year': played_at_datetime.year
    }
    played_dict['popularity'] = track['track']['popularity']
    history_list.append(played_dict)

    track_dict = dict()
    track_dict['track_id'] = track['track']['id']
    track_dict['name'] = track['track']['name']
    track_dict['duration_ms'] = track['track']['duration_ms']
    track_dict['duration_min'] = round(track['track']['duration_ms']/(1000*60),1)
    track_dict['track_number'] = track['track']['track_number']
    track_dict['explicit_flag'] = track['track']['explicit']
    features_result = sp.audio_features(tracks=track['track']['id'])
    track_dict['key'] = key_dict[features_result[0]['key']]
    track_dict['mode'] = mode_dict[features_result[0]['mode']]
    track_dict['danceability'] = features_result[0]['danceability']
    track_dict['energy'] = features_result[0]['energy']
    track_dict['loudness'] = features_result[0]['loudness']
    track_dict['speechiness'] = features_result[0]['speechiness']
    track_dict['acousticness'] = features_result[0]['acousticness']
    track_dict['instrumentalness'] = features_result[0]['instrumentalness']
    track_dict['liveness'] = features_result[0]['liveness']
    track_dict['valence'] = features_result[0]['valence']
    track_dict['tempo'] = features_result[0]['tempo']
    track_dict['time_signature'] = features_result[0]['time_signature']
    track_dict['url'] = track['track']['external_urls']['spotify']
    artists_list = list()
    for artist in track['track']['artists']:
        artist_result = sp.artist(artist['id'])
        artist_dict = {
            'artist_id': artist['id'],
            'name': artist['name'],
            'genres': artist_result['genres'],
            #'followers': artist_result['followers']['total'], > muda com o tempo
            #'popularity': artist_result['popularity'], > muda com o tempo
            'url': artist['external_urls']['spotify'],
            #'images': artist_result['images'] > podem mudar com o tempo também! Como salvar? Collection com imagem, followers, popularity e data em que tudo foi salvo?
        }
        artists_list.append(artist_dict)
        sleep(0.1)
    track_dict['artists'] = artists_list
    track_dict['album_id'] = track['track']['album']['id']
    tracks_list.append(track_dict)

    album_dict = dict()
    album_dict['album_id'] = track['track']['album']['id']
    album_dict['name'] = track['track']['album']['name']
    album_dict['number_tracks'] = track['track']['album']['total_tracks']
    album_dict['release_date'] = convert_date(track['track']['album']['release_date'])
    album_dict['url'] = track['track']['album']['external_urls']['spotify']
    album_dict['images'] = track['track']['album']['images']
    artists_list = list()
    for artist in track['track']['album']['artists']:
        artist_result = sp.artist(artist['id'])
        artist_dict = {
            'artist_id': artist['id'],
            'name': artist['name'],
            'genres': artist_result['genres'],
            #'followers': artist_result['followers']['total'],
            #'popularity': artist_result['popularity'],
            'url': artist['external_urls']['spotify'],
            #'images': artist_result['images']
        }
        artists_list.append(artist_dict)
        sleep(0.1)
    album_dict['artists'] = artists_list
    albums_list.append(album_dict)
    sleep(0.1)

api_dict = {
    'history': {'tracks': history_list},
    'tracks': {'tracks': list(unique_everseen(tracks_list))},
    'albums': {'albums': list(unique_everseen(albums_list))},
}

mongo_client = MongoClient("mongodb+srv://$USERNAME:$PASSWORD@cluster1.chrui.mongodb.net/?retryWrites=true&w=majority")
spotify_db = mongo_client['spotify']
collection_list = spotify_db.list_collection_names()
if collection_list == []:
    collection_list = list(api_dict.keys())

# Save data in MongoDB collections
for col_name in collection_list:
    collection = spotify_db[col_name]
    if col_name == 'history':
        results_list = list(collection.find({},{'_id':0}).sort("played_at.full",-1).limit(50)) # descending

    else:
        results_list = list(collection.find({},{'_id':0}))
    new_docs = []
    new_docs = [x for x in api_dict[col_name][list(api_dict[col_name].keys())[0]] if x not in results_list]
    if new_docs != []:
        collection.insert_many(new_docs)
