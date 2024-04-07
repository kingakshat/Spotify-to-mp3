import json
from youtube_search import YoutubeSearch

def get_youtube_links(track_artist_pairs):
    youtube_links = {}
    for track_name, artist_name in track_artist_pairs:
        query = f"{track_name} {artist_name}"
        results = YoutubeSearch(query, max_results=1).to_dict()
        if results:
            video_id = results[0]['id']
            youtube_link = f"https://www.youtube.com/watch?v={video_id}"
            youtube_links[track_name] = youtube_link
    return youtube_links

def load_playlist_from_json(filename):
    with open(filename, 'r') as f:
        playlist_data = json.load(f)
    track_artist_pairs = [(track['track']['name'], track['track']['artists'][0]['name']) for track in playlist_data['tracks']['items']]
    return track_artist_pairs

def save_links_to_json(youtube_links, filename):
    with open(filename, 'w') as f:
        json.dump(youtube_links, f, indent=4)

if __name__ == "__main__":
    json_file = 'sp_to_list.json' #input("Enter the JSON file name: ")
    output_json_file = 'list_to_link.json'#input("Enter the output JSON file name: ")

    playlist_tracks_artists = load_playlist_from_json(json_file)
    youtube_links = get_youtube_links(playlist_tracks_artists)

    save_links_to_json(youtube_links, output_json_file)
    print(f"YouTube links saved to {output_json_file}")
