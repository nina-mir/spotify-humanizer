import streamlit as st

def initialize_user_data():
    """Initialize user data once"""
    if 'user_initialized' not in st.session_state:
        st.toast("Successfully authenticated with Spotify!", icon=":material/celebration:")
        sp = st.session_state.sp_client
        curr_user = sp.current_user()
        st.session_state.curr_user = curr_user
        st.session_state.user_initialized = True
        
        # Show balloon on initialization
        # st.balloons()

def display_user_profile():
    """Display user profile (safe to call multiple times)"""
    if st.session_state.get('user_initialized'):
        curr_user = st.session_state.curr_user
        
        col1, col2 = st.columns([1, 1])

        with col1:
            st.write(f"Hello, **{curr_user['display_name']}**! :material/waving_hand: ")
            user_image_url = curr_user['images'][0]['url']
            st.image(user_image_url)

        with col2:
            st.markdown(""" 
                    #### How this works :material/info:   
                    :material/counter_1: Select a time_range value for your data.  
                    :material/counter_2: Fetch your corresponding top artists or tracks.  
                    :material/counter_3: Download your data!          
                    :material/counter_4: Check-out Artists / Tracks Analytics pages for more!     
                    :material/counter_5: Go to a local music show! :material/heart_smile:    
                    """)

