import streamlit as st
import streamlit.components.v1 as components
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
from src.init_setup_styling import init_global_sidebar_styles
from src.greeting_user import display_user_profile, initialize_user_data
from src.top_items import user_top_items_worker


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
            # toast 8message is included in initialize_user_data() along balloons. maybe a bit too much! but, well! 
            initialize_user_data()
            display_user_profile()
            st.write("""
                <hr style='margin:0;'>         
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f'❌ Error getting user info: {e}')
        
        if st.session_state.auth_complete:

            time_range = st.radio(
                "Select a time_range :material/face_down:",
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
                index=None
            )



# 1) One-time: load the Material Icons font + add CSS to style expander summary
            st.markdown("""
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Outlined" rel="stylesheet">
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


            if time_range:
                st.write(f":material/music_history: You selected **{time_range}**!")
                st.session_state.time_range = time_range

            col1, spacer, col2 = st.columns([3, 1, 3])

            with col1:
                if st.button(
                    ':material/person_play: Artists', 
                    use_container_width=True,
                    disabled=not time_range  # Disable if no time_range selected
                ):
                    now = datetime.now()
                    artists_data = user_top_items_worker()
                    # Convert to JSON string
                    json_data = json.dumps(artists_data, indent=2)
                    writeable_date = now.strftime("%Y-%m-%d")
                    st.download_button(
                        label="📥 Download as JSON",
                        data=json_data,
                        file_name=f"artists_{st.session_state.time_range}_spotify_data-{writeable_date}.json",
                        mime="application/json"
                    )
                    st.json(artists_data, expanded=2)

            with col2:
                if st.button(
                    ':material/simulation: Songs', 
                    use_container_width=True,
                    disabled=not time_range  # Disable if no time_range selected
                ):
                    artists_data = user_top_items_worker()
                    st.json(artists_data, expanded=2)



if __name__ == '__main__':
    main()