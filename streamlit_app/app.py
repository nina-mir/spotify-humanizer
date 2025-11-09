import streamlit as st
import streamlit.components.v1 as components
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from spotipy.oauth2 import SpotifyOAuth
from src.init_setup_styling import init_global_sidebar_styles
from src.greeting_user import greet_authenticated_user


# st.write(st.secrets['SPOTIPY_CLIENT_ID'])

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
        # User is authenticated - show your app
        # st.success(, icon="✅")
        st.toast("Successfully authenticated with Spotify!", icon=":material/celebration:")
        
        try:
            # sp = st.session_state.sp_client
            # curr_user = sp.current_user()
            # # print(curr_user)
            
            # # Let's show user info to the user
            # col1, col2 = st.columns(2)

            # with col1:
            #     st.write(f'👋 Hello {curr_user["display_name"]}!')
            #     st.write(f'📧 User: {curr_user["id"]}\n')

            # with col2:
            #     user_image_url = curr_user['images'][0]['url']
            #     print(user_image_url)
            #     st.image(user_image_url)
            greet_authenticated_user()

        except Exception as e:
            st.error(f'❌ Error getting user info: {e}')
            return
        
        if st.session_state.auth_complete:
            st.button('get artists')





if __name__ == '__main__':
    main()