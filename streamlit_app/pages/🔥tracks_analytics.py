from src.data_visualizers import render_tracks_grid
import streamlit as st
from src.data_transformers import extract_track_data

# Layout

# After fetching and transforming data
if "time_range" in st.session_state and st.session_state.tracks_data:
    current_range = st.session_state.time_range

    available_data = list(st.session_state.tracks_data.keys())

    if len(available_data) > 1:
        #TO-DO figure out an option like radio button for the user to change the current_range
        time_range = st.radio(
                "# Select a time_range to see your data! :material/sentiment_excited:",
                available_data,

                # captions=[
                #     "approx. last 4 weeks",
                #     "approx. last 6 months",
                #     "~1 year of data",
                # ],
                # key="visibility", #b9b9b9;
                # label_visibility=st.session_state.visibility,
                # disabled=st.session_state.disabled,
                key="visibility",
                horizontal=True,
                index= available_data.index(str(current_range)),
            )
            
        if time_range:
                st.write(f":material/music_history: You selected **{time_range}**!")
                st.session_state.time_range = time_range
                transformed_tracks_data = extract_track_data(st.session_state.tracks_data[current_range], current_range)
                st.subheader(f"Your Top Tracks - {time_range.replace('_', ' ').title()}")
                render_tracks_grid(transformed_tracks_data.get("tracks", []), columns=4)  # 4 columns
                # st.rerun()

    else:
        transformed_tracks_data = extract_track_data(st.session_state.tracks_data[current_range], current_range)
        st.subheader(f"Your Top Tracks - {current_range.replace('_', ' ').title()}")
        render_tracks_grid(transformed_tracks_data.get("tracks", []), columns=4)  # 4 columns

else:
    st.header("Your Tracks Analytics")
    st.warning('# Nothing to see!   (>_<)', icon="⚠️")
    st.divider()
    st.write("""
                <div style="font-size: 1.5rem;">
                    <p>There's no track data available <b>yet</b>!</p>
                    <p 
                    style="background-color: #191970; 
                    color: #E0FFFF; 
                    font-weight:600;
                    padding: 0.5rem 1.5rem; 
                    border-radius:0.2rem;">
                         Make sure you are logged in then follow these steps:
                    </p>
                    <ol> 
                        <li>Navigate to Home.</li> 
                        <li>Choose a <em>time_range</em>!</li>
                        <li>Press the Tracks button to fetch your data! </li>
                        <li>Come back here to see your tracks analytics! </li>
                    <ol> 
                <div>
             """, unsafe_allow_html=True)

    