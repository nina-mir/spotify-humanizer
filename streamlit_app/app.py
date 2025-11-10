import streamlit as st
import streamlit.components.v1 as components
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
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

    # st.markdown('<p style="color: blue; font-size: 20px;">Blue text</p>', unsafe_allow_html=True)

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
        <a href="{auth_url}" target="_self">
            <button style="background-color: #1DB954; color: white; padding: 10px 20px; border: none; border-radius: 20px; cursor: pointer;">
                Login with Spotify
            </button>
        </a>
        """, unsafe_allow_html=True)

    else:

        try:
            # toast message is included in initialize_user_data() along balloons. maybe a bit too much! but, well! 
            initialize_user_data()
            display_user_profile()
            st.write("""
                <hr style='margin:0;'>         
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f'❌ Error getting user info: {e}')
        
        if st.session_state.auth_complete:
            st.markdown(
                """
                <style>
                .stRadio [role=radiogroup]{
                    margin-top:0.25rem;
                    display: flex;
                    justify-content: center;
                }

                div[data-testid="stRadio"] > label > div {
                    font-size: 1.2rem;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            time_range = st.radio(
                "# Select a time_range 👇",
                ["short_term", "medium_term", "long_term"],
                captions=[
                    "approx. last 4 weeks",
                    "approx. last 6 months",
                    "approx. ~1 year of data",
                ],
                # key="visibility",
                # label_visibility=st.session_state.visibility,
                # disabled=st.session_state.disabled,
                horizontal=True,
                index=None
            )

            if time_range:
                st.write(f":material/music_history: You selected **{time_range}**!")
                st.session_state.time_range = time_range

            col1, spacer, col2 = st.columns([3, 1, 3])

            with col1:
                if st.button(':material/person_play: Artists', use_container_width=True):
                    artists_data = user_top_items_worker()
                    st.json(artists_data, expanded=2)

            with col2:
                if st.button('🎶 Songs', use_container_width=True):
                    artists_data = user_top_items_worker()
                    st.json(artists_data, expanded=2)



if __name__ == '__main__':
    main()