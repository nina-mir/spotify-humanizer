from src.data_visualizers import render_artist_grid, plot_genre_distribution
import streamlit as st
from src.data_transformers import extract_artist_data



# Layout


# After fetching and transforming data
if "time_range" in st.session_state and st.session_state.tracks_data:
    pass

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

    