import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get client_id and client_secret from .env file
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


input_song_name = input('Enter the input song name: ')
input_artist_name = input('Enter the input artist name: ')


results = sp.search(q=f'track:"{input_song_name}" artist:"{input_artist_name}"', type='track', limit=1)
if len(results['tracks']['items']) > 0:
    input_track = results['tracks']['items'][0]
    input_track_id = input_track['id']
    input_track_artist_id = input_track['artists'][0]['id']
    input_track_name = input_track['name']
    print(f'Input song: {input_track_name} by {input_artist_name}\n')


    input_track_features = sp.audio_features(input_track_id)[0]


    num_similar_tracks = int(input('Enter the number of similar tracks to generate: '))


    similar_tracks = sp.recommendations(seed_artists=[input_track_artist_id], limit=num_similar_tracks)
    print(f'Similar songs ({num_similar_tracks}):')
    for i, track in enumerate(similar_tracks['tracks']):
        track_name = track['name']
        track_artist = track['artists'][0]['name']
        print(f'{i+1}. {track_name} by {track_artist}')
else:
    print(f'No results found for the song: {input_song_name} by {input_artist_name}')
