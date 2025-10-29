from flask import Flask, request, render_template_string, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import threading
import time

load_dotenv()

app = Flask(__name__)

# Global variables to share between routes
auth_success = False
spotify_client = None

# HTML template for the callback page
SUCCESS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Spotify Auth Success</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            padding: 50px; 
            background: linear-gradient(135deg, #1DB954, #191414);
            color: white;
        }
        .container {
            background: rgba(0,0,0,0.7);
            padding: 30px;
            border-radius: 10px;
            max-width: 500px;
            margin: 0 auto;
        }
        .success { color: #1DB954; font-size: 24px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="success">✓ Authentication Successful!</div>
        <p>You can close this window and return to the terminal.</p>
        <p>Your playlists will be displayed in the command line.</p>
    </div>
</body>
</html>
"""

def get_spotify_client():
    """Create and return authenticated Spotify client"""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri="http://127.0.0.1:8000/callback",
        scope="playlist-read-private user-top-read user-library-read user-read-private",
        cache_path=".cache"
    ))

@app.route('/')
def home():
    """Home page with login button"""
    auth_url = get_auth_url()
    html = f"""
    <!DOCTYPE html>
        <html>
        <head>
        <title>Spotify Playlist Fetcher</title>
        <style>
        body {{ 
        font-family: Arial, sans-serif; 
            text-align: center; 
            padding: 50px; 
            background: linear-gradient(135deg, #1DB954, #191414);
            color: white;
        }}
.container {{
            background: rgba(0,0,0,0.7);
            padding: 40px;
            border-radius: 15px;
            max-width: 500px;
            margin: 0 auto;
        }}
        .btn {{
            background: #1DB954;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 18px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 20px 0;
        }}
        .btn:hover {{
            background: #1ed760;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 Spotify Playlist Fetcher</h1>
        <p>Click the button below to authenticate with Spotify and view your playlists.</p>
        <a href="{auth_url}" class="btn">Connect with Spotify</a>
        <p><small>You'll be redirected to Spotify to authorize this app.</small></p>
    </div>
</body>
</html>
    """
    return render_template_string(html)

@app.route('/callback')
def callback():
    """Handle Spotify OAuth callback"""
    global auth_success, spotify_client
    
    try:
        # Get the authorization code from the URL parameters
        code = request.args.get('code')
        
        if code:
            print(f"✓ Received authorization code")
            
            # Create auth manager and exchange code for token
            auth_manager = SpotifyOAuth(
                client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                redirect_uri="http://127.0.0.1:8000/callback",
                scope="playlist-read-private user-top-read user-library-read user-read-private",
                cache_path=".cache"
            )
            
            # Get access token
            token_info = auth_manager.get_access_token(code)
            print(f"✓ Successfully obtained access token {token_info}")
            
            # Create Spotify client
            spotify_client = spotipy.Spotify(auth_manager=auth_manager)
            auth_success = True
            
            return SUCCESS_HTML
        else:
            return "Error: No authorization code received", 400
            
    except Exception as e:
        return f"Error during authentication: {str(e)}", 400

def get_auth_url():
    """Get the Spotify authorization URL"""
    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri="http://127.0.0.1:8000/callback",
        scope="playlist-read-private user-top-read user-library-read user-read-private",
        cache_path=".cache"
    )
    return auth_manager.get_authorize_url()

def fetch_playlists():
    """Fetch and display playlists once authenticated"""
    global spotify_client
    
    print("Waiting for authentication...")
    while not auth_success:
        time.sleep(1)
    
    print("✓ Authentication confirmed! Fetching your playlists...\n")
    
    try:
        # Get user info
        user = spotify_client.current_user()
        print(f"🎵 Welcome, {user['display_name']}!\n")
        
        # Get playlists
        playlists = spotify_client.current_user_playlists(limit=50)
        
        if playlists['items']:
            print(f"📚 Found {len(playlists['items'])} playlists:\n")
            print("-" * 50)
            
            for idx, playlist in enumerate(playlists['items']):
                print(f"\n{idx+1}. {playlist['name']}")
                print(f"   📊 Tracks: {playlist['tracks']['total']}")
                print(f"   🔗 ID: {playlist['id']}")
                
                # Get a few sample tracks
                try:
                    tracks = spotify_client.playlist_tracks(playlist['id'], limit=3)
                    if tracks['items']:
                        print("   🎵 Sample tracks:")
                        for track_item in tracks['items']:
                            if track_item['track']:
                                track = track_item['track']['name']
                                artist = track_item['track']['artists'][0]['name']
                                print(f"      • {track} - {artist}")
                except Exception as e:
                    print(f"   ❌ Could not fetch tracks: {e}")
                
                print("-" * 50)
                
        else:
            print("❌ No playlists found!")
            
    except Exception as e:
        print(f"❌ Error fetching playlists: {e}")

def run_flask():
    """Run the Flask app"""
    app.run(host='localhost', port=8000, debug=False, use_reloader=False)

if __name__ == '__main__':
    print("=== Spotify Playlist Fetcher ===")
    print("Starting Flask server on http://localhost:8000")
    print("The browser should open automatically...")
    print("If not, please visit: http://localhost:8000")
    print("\n" + "="*50 + "\n")
    
    # Start playlist fetching in a separate thread after a short delay
    playlist_thread = threading.Thread(target=fetch_playlists)
    playlist_thread.daemon = True
    playlist_thread.start()
    
    # Run Flask app
    run_flask()