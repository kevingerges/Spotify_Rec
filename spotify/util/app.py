from flask import Flask, render_template, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

app = Flask(__name__)

# Get client_id and client_secret from .env file
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommendation', methods=['POST'])
def recommendation():

    input_song_name = request.json['song_name']
    input_artist_name = request.json['artist_name']
    num_similar_tracks = int(request.json['num_similar_tracks'])


    results = sp.search(q=f'track:"{input_song_name}" artist:"{input_artist_name}"', type='track', limit=1)
    if len(results['tracks']['items']) > 0:
        input_track = results['tracks']['items'][0]
        input_track_id = input_track['id']
        input_track_artist_id = input_track['artists'][0]['id']


        input_track_features = sp.audio_features(input_track_id)[0]


        similar_tracks = sp.recommendations(seed_artists=[input_track_artist_id], limit=num_similar_tracks)


        similar_songs = []
        for track in similar_tracks['tracks']:
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            similar_songs.append({'name': track_name, 'artist': track_artist})


        response = {'similar_songs': similar_songs}
        return jsonify(response)
    else:
        return jsonify({'error': 'No results found for the input song'})


if __name__ == '__main__':
    app.run(debug=True)
