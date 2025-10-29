from flask import Flask, render_template, request
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values

config = dotenv_values(".env")
scope= "playlist-read-private"


sp_oauth = SpotifyOAuth( 
    client_id= config["SPOTIPY_CLIENT_ID"],
    client_secret=config["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=config["SPOTIPY_REDIRECT_URI"],
    scope= scope,
    cache_path="./.cache_Nina" 
)

# sp = spotipy.Spotify(auth_manager=sp_oauth)


print(config)

app = Flask(__name__)

def get_authorization_URL():
    return sp_oauth.get_authorize_url()

@app.route("/")     
def home():
    authorization_URL = get_authorization_URL()
    return render_template('welcome.html', authorization_URL=authorization_URL)

@app.route("/callback")
def get_code():
    code = request.args.get("code")
    token = sp_oauth.get_access_token(code=code)

    if 'access_token' in token:
        if 'expires_in' in token:
            print('all is good!')
    else: 
        return 'issue with token!'

    sp = spotipy.Spotify(auth=token.access_token)
    print(sp.current_user())
    # sp = spotipy.Spotify(auth_manager=sp_oauth)
    # print(code)
    # print("sssssssssssssssssssssssssss<<<")
    # print(token)

    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)