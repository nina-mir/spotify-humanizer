import streamlit as st

def greet_authenticated_user():

    sp = st.session_state.sp_client
    curr_user = sp.current_user()
    # print(curr_user)

    # Let's show user info to the user
    col1, col2 = st.columns(2)

    with col1:
        st.balloons()
        st.write(f'👋 Yo Yo, {curr_user["display_name"]}!')
        st.write(f'📧 User ID: {curr_user["id"]}\n')
        st.info("Press the buttons below and learn what songs, which artists you\'ve been listening to over the past few weeks, months or year!")

    with col2:
        user_image_url = curr_user['images'][0]['url']
        print(user_image_url)
        st.image(user_image_url)