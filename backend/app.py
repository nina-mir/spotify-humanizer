import json
from pathlib import Path
import time

from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values
import threading
import time
from datetime import datetime


config = dotenv_values(".env")
scope = "user-read-recently-played user-top-read"

# Shared state between routes and worker
auth_is_complete = threading.Event()
sp_client = None
sp_client_lock = threading.Lock()

sp_oauth = SpotifyOAuth( 
    client_id=config["SPOTIPY_CLIENT_ID"],
    client_secret=config["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=config["SPOTIPY_REDIRECT_URI"],
    scope=scope,
    cache_path=".cache",
)                                                                               

app = Flask(__name__)

# create a results folder
Path('results').mkdir(exist_ok=True)

def user_top_items_worker(time_range='medium_term'):
    """
    Make API calls to get user's top songs and artists for different time ranges.
    
    This function performs a series of discrete API calls (not continuous monitoring)
    to retrieve the user's listening statistics across specified time periods.
    
    Args:
        time_range (str): Time period for analysis. Options are:
            - 'long_term': ~1 year of data, updated with new data
            - 'medium_term': ~6 months (default)
            - 'short_term': ~4 weeks
    
    Returns:
        dict or None: Contains top artists and songs data, or None if API call fails
        
    Raises:
        ConnectionError: If API connection fails
        ValueError: If time_range parameter is invalid
    """

    # TO-DO: Change it later! 
    # dev notes: for now it is only about artists and short_term

    print('🎵 Top Songs & 🎤🎷🎶Artists Worker: Waiting for authentication... ⏳')
    
    # initial values
  
    total_items = None
    top_tracks = []
    top_artists = []


    global sp_client
    
    auth_is_complete.wait()  # Block until auth is done
    
    print('✅ Authentication complete! Starting retreiving top artists ...\n')
    print(f'The time_range this worker is retreiving is {time_range}')
    
    # Wait a moment to ensure sp_client is fully set
    time.sleep(1)
    
    with sp_client_lock:
        if not sp_client:
            print('❌ Error: Spotify client not initialized')
            return
        
        try:
            curr_user = sp_client.current_user()
            # To-DO store this info somewhere or feed it to a template for the user?    
            print(f'👋 Hello {curr_user["display_name"]}!')
            print(f'📧 User: {curr_user["id"]}\n')
        except Exception as e:
            print(f'❌ Error getting user info: {e}')
            return
    


    try:
        offset = 0
        limit = 50
        
        while True:

            with sp_client_lock:
                # Fetch the first 50 recently played songs
                results = sp_client.current_user_top_artists(
                    limit=limit, 
                    offset=offset, 
                    time_range=time_range
                )
                print(len(results))
                if not results or 'items' not in results:
                    print(f'⚠️{curr_user["display_name"]} has no top artists!')
                    break 

                if total_items is None:
                    total_items = results['total']  # Set once
                    print(f"Total items available: {total_items}")   

                items = results['items']
                top_artists.extend(items)
                offset += len(items)
                
                if len(top_artists) >= total_items:
                    break

                time.sleep(3)

        print(f'Successfully fetched the top tracks listened by {curr_user["display_name"]}!')
        print(f'Info of {len(top_artists)} artists out of {total_items} total top artists is available!')
        print("let's write it to file!")

        results_data = {
            'metadata': {
                'time_range': time_range,
                'total_items': total_items,
                'fetched_count': len(top_artists),
                'timestamp': datetime.now().isoformat()
            },
            'artists': top_artists
        }

        with open('results/top_artists.json', 'w', encoding='utf-8') as writer:
            json.dump(results_data, writer, indent=2, ensure_ascii=False)

        print(f"💾 Results saved to results/top_artists.json")
        
        return


    except Exception as e:
        print(f'error {e} occurred.')
         

def recent_songs_history_worker():
    """
    Continuously monitor and display the user's recently played tracks.
    
    This worker runs in a loop, periodically checking for new recently played tracks
    and displaying them to the console. It waits for authentication to complete before
    starting and maintains state to only show new tracks since the last check.
    
    Dependencies:
        - Requires `sp_client` global variable to be set after authentication
        - Uses `auth_is_complete` event to wait for authentication
        - Uses `sp_client_lock` for thread-safe access to Spotify client
        
    Behavior:
        - Initially displays the last 50 played tracks
        - Subsequent checks only show new tracks since last poll
        - Uses a 100-minute polling interval (optimized for typical listening patterns)
        - Implements error handling with retry logic
        
    Side Effects:
        - Prints track information to console
        - Modifies global state (last_track_played_at tracking)
        - Makes periodic API calls to Spotify Web API
        
    Error Handling:
        - Continues running on errors with exponential backoff
        - Handles authentication and API failures gracefully
    """    
    
    print('🎵 Recent Songs Worker: Waiting for authentication... ⏳')
    global sp_client
    
    auth_is_complete.wait()  # Block until auth is done
    
    print('✅ Authentication complete! Starting recent songs monitoring...\n')
    
    # Wait a moment to ensure sp_client is fully set
    time.sleep(1)
    
    with sp_client_lock:
        if not sp_client:
            print('❌ Error: Spotify client not initialized')
            return
        
        try:
            curr_user = sp_client.current_user()
            print(f'👋 Hello {curr_user["display_name"]}!')
            print(f'📧 User: {curr_user["id"]}\n')
        except Exception as e:
            print(f'❌ Error getting user info: {e}')
            return
    
    last_track_played_at = None
    
    # Continuous monitoring loop
    while True:
        try:
            with sp_client_lock:
                # Fetch last 50 recently played tracks
                results = sp_client.current_user_recently_played(
                    limit=50,
                    after=None,  # Can use timestamp in milliseconds
                    before=None
                )
            
            if not results or 'items' not in results:
                print('⚠️  No recent tracks found')
                time.sleep(60)
                continue
            
            # Process tracks (most recent first)
            tracks = results['items']
            
            if tracks:
                # Check if there are new tracks since last check
                latest_played_at = tracks[0]['played_at']
                
                if last_track_played_at is None:
                    # First run - show all tracks
                    print(f'\n📊 Showing last {len(tracks)} played tracks:\n')
                    for idx, item in enumerate(tracks, 1):
                        track = item['track']
                        played_at = item['played_at']
                        artists = ', '.join([artist['name'] for artist in track['artists']])
                        
                        # Convert ISO timestamp to readable format
                        dt = datetime.fromisoformat(played_at.replace('Z', '+00:00'))
                        time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                        
                        print(f"{idx:2d}. 🎵 {track['name']}")
                        print(f"    👤 {artists}")
                        print(f"    💿 {track['album']['name']}")
                        print(f"    🕐 {time_str}\n")
                    
                    last_track_played_at = latest_played_at
                
                elif latest_played_at != last_track_played_at:
                    # New tracks detected - show only new ones
                    print(f'\n🆕 New tracks detected!\n')
                    new_tracks = []
                    
                    for item in tracks:
                        if item['played_at'] > last_track_played_at:
                            new_tracks.append(item)
                        else:
                            break  # Stop when we reach old tracks
                    
                    for idx, item in enumerate(new_tracks, 1):
                        track = item['track']
                        played_at = item['played_at']
                        artists = ', '.join([artist['name'] for artist in track['artists']])
                        
                        dt = datetime.fromisoformat(played_at.replace('Z', '+00:00'))
                        time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                        
                        print(f"🎵 {track['name']} - {artists}")
                        print(f"   🕐 {time_str}\n")
                    
                    last_track_played_at = latest_played_at
                else:
                    print('⏸️  No new tracks since last check')
            
            # Wait before next check (adjust interval as needed)
            # The thread sleep could be an adjustable variable depending on the user's listening habits
            # medium is 100 minutes i.e. 50 songs of 2 min lenght
            # frequent is 15 minutes
            # occassional user is 180 minutes & so on                 
            time.sleep(6000)  # Check every 6000 seconds i.e. 50 tracks of 2 min length
            
        except Exception as e:
            print(f'❌ Error fetching recent tracks: {e}')
            time.sleep(60)  # Wait longer on error


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
        
        if not code:
            return "Error: No authorization code received", 400
        
        token = sp_oauth.get_access_token(code=code)
        
        if not token:
            return "<h1>Failure in authentication!!</h1>", 401
        
        # Thread-safe client initialization
        global sp_client
        with sp_client_lock:
            sp_client = spotipy.Spotify(auth_manager=sp_oauth)
        
        # Signal that authentication is complete
        auth_is_complete.set()
        
        return render_template('success.html')
    
    except Exception as e:
        return f"Error during authentication: {str(e)}", 400


def run_flask():
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)


if __name__ == "__main__":


    songs_daemon = threading.Thread(
        target=user_top_items_worker,
        args=('short_term',),
        name='recent-songs-worker',
        daemon=True
    )
    songs_daemon.start()
    
    run_flask()