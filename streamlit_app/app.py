import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from spotipy.oauth2 import SpotifyOAuth


# st.write(st.secrets['SPOTIPY_CLIENT_ID'])

scope = "user-read-recently-played user-top-read"
  

def initialize_spotipy_oauth():
    return SpotifyOAuth( 
        client_id = st.secrets['SPOTIPY_CLIENT_ID'],
        client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"],
        redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"],
        scope=scope,
        cache_path=".cache",
        show_dialog = True
    )

def main():
    st.title('spotify humanizer ....')

    #initialize the session state
    if 'auth_complete' not in st.session_state:
        st.session_state.auth_complete = False

    if 'sp_client' not in st.session_state:
        st.session_state.sp_client = None

    # Let's figure out if we are in the callback phase or no by extracting code value if any
    query_prams = st.query_params

    print('one!', query_prams)

    auth_code = query_prams.get('code', None)

    print('two', auth_code)

    if auth_code and not st.session_state.auth_complete:
    
        #  Handle the callback! 
    
        try:
    
            sp_oauth = initialize_spotipy_oauth()
            token_info = sp_oauth.get_access_token(auth_code)

            print('three', token_info)
            
            if token_info:
                st.session_state.sp_client = spotipy.Spotify(auth=token_info['access_token'])
                st.session_state.auth_complete = True
                st.session_state.token_info = token_info
                print('success line 51!')
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
        # User is authenticated - show your app
        st.success("✅ Successfully authenticated with Spotify!")


if __name__ == '__main__':
    main()