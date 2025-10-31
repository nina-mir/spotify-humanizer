from flask import Flask, render_template, request
import spotipy
# import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values

import threading, time

config = dotenv_values(".env")
scope= "playlist-read-private user-top-read user-library-read user-read-private"

# Shared state between routes and worker
auth_is_complete = False
sp_client = None

sp_oauth = SpotifyOAuth( 
    client_id= config["SPOTIPY_CLIENT_ID"],
    client_secret=config["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=config["SPOTIPY_REDIRECT_URI"],
    scope= scope,
    cache_path=".cached",
    # show_dialog=True 
)                                                                               

app = Flask(__name__)

def playlist_worker():
    print('waiting for permission to operate .... ⏳⏰🫸🏽')
    global auth_is_complete, sp_client

    while not auth_is_complete:
        time.sleep(2)

    if auth_is_complete:
        print('permission is guaranteed! ✔️\nOperation begins')
        if sp_client:
            curr_user = sp_client.current_user()
            print( f'hallo {curr_user["display_name"]}!')
            print('CURRENT_USER full info', curr_user)
            
            playlists = sp_client.user_playlists(curr_user["id"])
            while playlists:
                for i, playlist in enumerate(playlists['items']):
                    print(f"{i + 1 + playlists['offset']:4d} {playlist['uri']} {playlist['name']}")
                if playlists['next']:
                    playlists = sp_client.next(playlists)
                else:
                    playlists = None




def get_authorization_URL():
    return sp_oauth.get_authorize_url()

@app.route("/")     
def home():
    authorization_URL = get_authorization_URL()
    return render_template('welcome.html', authorization_URL=authorization_URL)

@app.route("/callback")
def get_code():
    try:

        code = request.args.get("code")

        if code:

            token = sp_oauth.get_access_token(code=code)

            if 'access_token' in token:
                if 'expires_in' in token:
                    global auth_is_complete , sp_client
                    sp_client = spotipy.Spotify(auth_manager=sp_oauth)
                    auth_is_complete = True
            else: 
                return "<h1>Failure in authentication!!</h1>"

            print(sp_client.current_user())

            return render_template('success.html')

        else:

            return "Error: No authorization code received", 400
    
    except Exception as e:

        return f"Error during authentication: {str(e)}", 400

def run_flask():
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)


if __name__ == "__main__":

    playlist_daemon = threading.Thread(target=playlist_worker, name='playlist-worker',daemon=True)
    playlist_daemon.start()

    run_flask()
    # while auth_is_complete:
