import spotipy
from spotipy.oauth2 import SpotifyOAuth
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Enter your Spotify API credentials
client_id = '16a7bf7f239a42d8823ca51608c98b42'
client_secret = '1c0ec4b5958f41618ccf5343619d2130'
redirect_uri = 'http://localhost:8080/callback'  # Set your redirect URI

# Initialize Spotipy with your credentials
sp_oauth = SpotifyOAuth(client_id=client_id, 
                        client_secret=client_secret, 
                        redirect_uri=redirect_uri,
                        scope="user-library-read")

# Start a local web server to handle the redirect
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global redirect_url
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/callback':
            query_parameters = parse_qs(parsed_url.query)
            redirect_url = query_parameters['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><head><title>Authentication Successful</title></head><body><h1>Authentication Successful</h1><p>You can close this window now.</p></body></html>')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><head><title>Not Found</title></head><body><h1>404 - Not Found</h1></body></html>')

def start_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Get authorization URL
auth_url = sp_oauth.get_authorize_url()

# Open the authorization URL in the default web browser
import webbrowser
webbrowser.open(auth_url)

# Wait until the redirect URL is received
server_thread.join()

# Initialize Spotipy with the received redirect URL
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Get a list of playlists for the authenticated user
playlists = sp.current_user_playlists(limit=50)  # Limit to 50 playlists (can adjust as needed)

# Print the names of the playlists
for playlist in playlists['items']:
    print(playlist['name'])
