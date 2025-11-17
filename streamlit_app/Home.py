import streamlit as st
import streamlit.components.v1 as components
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
from src.init_setup_styling import init_global_sidebar_styles
from src.greeting_user import display_user_profile, initialize_user_data
from src.top_artists import user_top_artists_worker
from src.top_tracks import user_top_tracks_worker
from src.data_transformers import extract_artist_data, extract_track_data


scope = "user-read-recently-played user-top-read"


def initialize_spotipy_oauth():
    return SpotifyOAuth( 
        client_id = st.secrets['SPOTIPY_CLIENT_ID'],
        client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"],
        redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"],
        scope=scope,
        cache_path=".cache"
    )

def main():
    
    # set up global styling and sidebar styling + sidebar's text
    init_global_sidebar_styles()

    #initialize the session state
    if 'auth_complete' not in st.session_state:
        st.session_state.auth_complete = False

    if 'sp_client' not in st.session_state:
        st.session_state.sp_client = None

    # Let's figure out if we are in the callback phase or no by extracting code value if any
    query_prams = st.query_params
    auth_code = query_prams.get('code', None)


    if auth_code and not st.session_state.auth_complete:
    
        #  Handle the callback! 
        try:

            sp_oauth = initialize_spotipy_oauth()
            token_info = sp_oauth.get_access_token(auth_code)
            
            if token_info:
                st.session_state.sp_client = spotipy.Spotify(auth=token_info['access_token'])
                st.session_state.auth_complete = True
                st.session_state.token_info = token_info
                # Clear the code from URL
                st.query_params.clear()
                st.rerun()
            else:
                st.error("Authentication failed!")
                
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
    
    elif not st.session_state.auth_complete:
        # let's authenticate the user by showing the login button
        sp_oauth = initialize_spotipy_oauth()
        auth_url = sp_oauth.get_authorize_url()

        st.markdown(f"""
        <style>
            .spotify-btn {{
                background-color: #0A0A0A;
                color: white;
                padding: 10px 20px;
                border: 2px solid #333;
                border-radius: 3rem;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                transition: all 0.3s ease;
                outline: none;
            }}
            .spotify-btn:hover {{
                background-color: #1a1a1a;
                color: #e5e5e5;
                outline: 2px solid #555;
                outline-offset: 2px;
            }}
        </style>
        <a href="{auth_url}" target="_self">
            <button class="spotify-btn">
                Login with Spotify
            </button>
        </a>
        """, unsafe_allow_html=True)
        
    else:
        try:
            initialize_user_data()
            display_user_profile()
            st.write("""
                <hr style='margin:0;'>         
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f'❌ Error getting user info: {e}')
        
        if st.session_state.auth_complete:

            st.subheader("Select a time_range:")

            # 1) One-time: load the Material Icons font + add CSS to style expander summary
            st.markdown("""
            <style>
            /* Scope to all expanders. If you only have one, this is fine.
            If you have many, see the notes below to scope it tighter. */
            [data-testid="stExpander"] > details > summary {
            font-size: 1.5rem;      
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: .5rem;
            }

            [data-testid="stExpander"] > details > summary:hover {
                opacity: 0.95;
            }
            </style>
            """, unsafe_allow_html=True)

            # 2) Your expander, unchanged
            with st.expander("_What is a time_range?!_ 🧓🏽"):
                st.write("""
                    Per [Spotify Web API documentation](https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks):
                    
                    time_range controlls over what time frame the affinities (i.e. your top artists or tracks at any time) are computed. 
                    Valid values: 
                    - **long_term** (calculated from ~1 year of data and including all new data as it becomes available)
                    - **medium_term** (approximately last 6 months) 
                    - **short_term** (approximately last 4 weeks)
                """)

            time_range = st.radio(
                "Select a time_range:",
                ["short_term", "medium_term", "long_term"],
                captions=[
                    "approx. last 4 weeks",
                    "approx. last 6 months",
                    "~1 year of data",
                ],
                # key="visibility", #b9b9b9;
                # label_visibility=st.session_state.visibility,
                # disabled=st.session_state.disabled,
                key="visibility",
                horizontal=True,
                index=None,
                label_visibility="collapsed"
            )
            
            if time_range:
                st.write(f":material/music_history: You selected **{time_range}**!")
                st.session_state.time_range = time_range

            st.write("""
                <hr style='margin:0;'>         
            """, unsafe_allow_html=True)

            col1, spacer, col2 = st.columns([3, 1, 3])


        # Initialize session state with a dict to hold data for each time range
        if 'time_range' not in st.session_state:
            st.session_state.time_range = None  # initialize time_range to None

        if 'artists_data' not in st.session_state:
            st.session_state.artists_data = {}  # Dict with time_range as keys

        if 'artists_fetched_times' not in st.session_state:
            st.session_state.artists_fetched_times = {}

        if 'tracks_data' not in st.session_state:
            st.session_state.tracks_data = {}
        
        if 'tracks_fetched_times' not in st.session_state:
            st.session_state.tracks_fetched_times = {}


        with col1:
            current_range = st.session_state.time_range

            if st.button(
                ':material/person_play: Artists', 
                use_container_width=True,
                disabled=not time_range
            ):
                # Fetch and store with time_range as key
                now = datetime.now()
                st.session_state.artists_data[current_range] = user_top_artists_worker(current_range)
                st.session_state.artists_fetched_times[current_range] = now
            
            # Show download buttons if data exists for current time_range
            if current_range in st.session_state.artists_data:
                transformed_artists_data = extract_artist_data(st.session_state.artists_data[current_range])
                transformed_json = json.dumps(transformed_artists_data, indent=2, ensure_ascii=False)
                raw_json = json.dumps(st.session_state.artists_data[current_range], indent=2, ensure_ascii=False)
                
                writeable_date = st.session_state.artists_fetched_times[current_range].strftime("%Y-%m-%d")
                
                st.download_button(
                    label=":material/download: Processed Data",
                    data=transformed_json,
                    file_name=f"artists_{current_range}_processed_spotify_data-{writeable_date}.json",
                    mime="application/json",
                    key=f"download_processed_artists_{current_range}"
                )

                st.download_button(
                    label=":material/download: Raw JSON Data",
                    data=raw_json,
                    file_name=f"artists_{current_range}_spotify_data-{writeable_date}.json",
                    mime="application/json",
                    key=f"download_raw_artists_{current_range}"
                )

        with col2:
            current_range = st.session_state.time_range

            if st.button(
                ':material/simulation: Tracks', 
                use_container_width=True,
                disabled=not time_range  # Disable if no time_range selected
            ):
                now = datetime.now()
                st.session_state.tracks_data[current_range] = user_top_tracks_worker(st.session_state.time_range)
                st.session_state.tracks_fetched_times[current_range] = now
            
            # Show download buttons if data exists for current time_range
            if current_range in st.session_state.tracks_data:

                transformed_tracks_data = extract_track_data(st.session_state.tracks_data[current_range], current_range)
                transformed_json = json.dumps(transformed_tracks_data, indent=2, ensure_ascii=False)
                raw_json = json.dumps( st.session_state.tracks_data[current_range], indent=2, ensure_ascii=False)
                
                writeable_date = st.session_state.tracks_fetched_times[current_range].strftime("%Y-%m-%d")

                st.download_button(
                    label=":material/download: Processed Data",
                    data=transformed_json,
                    file_name=f"tracks_{current_range}_processed_spotify_data-{writeable_date}.json",
                    mime="application/json",
                    key=f"download_processed_tracks_{current_range}"
                )
                st.download_button(
                    label=":material/download: Raw JSON Data",
                    data=raw_json,
                    file_name=f"tracks_{st.session_state.time_range}_spotify_data-{writeable_date}.json",
                    mime="application/json"
                )
                # st.json(tracks_data, expanded=2)



if __name__ == '__main__':
    main()