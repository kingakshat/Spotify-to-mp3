import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Enter your Spotify API credentials
client_id = '16a7bf7f239a42d8823ca51608c98b42'
client_secret = '1c0ec4b5958f41618ccf5343619d2130'

# Initialize Spotipy with your credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist(playlist_id):
    # Retrieve playlist information
    playlist = sp.playlist(playlist_id)
    return playlist

def save_playlist_as_json(playlist, filename):
    # Save playlist information as JSON
    with open(filename, 'w') as f:
        json.dump(playlist, f, indent=4)

if __name__ == "__main__":
    playlist_id = '3ZSvxJbe5Lp9XBpogGHINW' #input("Enter Spotify playlist ID: ")

    playlist_info = get_playlist(playlist_id)
    # filename = f"{playlist_info['name']}.json"
    filename = f"{'sp_to_list'}.json"

    save_playlist_as_json(playlist_info, filename)
    print(f"Playlist '{playlist_info['name']}' saved as {filename}")
