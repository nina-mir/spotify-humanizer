from src.data_visualizers import render_tracks_grid
import streamlit as st
from src.data_transformers import extract_track_data
from src.pagination import (
    array_paginator, 
    top_pagination_controllers,
    calculate_total_pages,
    initialize_pagination_state,
    handle_pagination_controls
)

# Constants
PAGE_SIZE = 200
PAGINATION_THRESHOLD = 400

# Initialize pagination state
initialize_pagination_state('tracks_current_page', default_page=1)

# After fetching and transforming data
if "time_range" in st.session_state and st.session_state.tracks_data:
    current_range = st.session_state.time_range
    available_data = list(st.session_state.tracks_data.keys())

    # Handle time range selection if multiple ranges available
    if len(available_data) > 1:
        time_range = st.radio(
            "# Select a time_range to see your data! :material/sentiment_excited:",
            available_data,
            key="visibility",
            horizontal=True,
            index=available_data.index(str(current_range)),
        )
        
        if time_range != st.session_state.time_range:
            st.write(f":material/music_history: You selected **{time_range}**!")
            st.session_state.time_range = time_range
            # Reset pagination when time range changes
            st.session_state.tracks_current_page = 1

    # Get transformed data
    transformed_tracks_data = extract_track_data(
        st.session_state.tracks_data[st.session_state.time_range], 
        st.session_state.time_range
    )
    all_tracks = transformed_tracks_data.get("tracks", [])
    total_tracks = len(all_tracks)

    st.subheader(f"Your Top Tracks - {st.session_state.time_range.replace('_', ' ').title()}")

    # Determine if pagination is needed
    if total_tracks >= PAGINATION_THRESHOLD:
        # Calculate pagination
        total_pages = calculate_total_pages(total_tracks, PAGE_SIZE)
        
        # Show pagination controls
        prev_btn, next_btn = top_pagination_controllers(
            st.session_state.tracks_current_page,
            total_pages
        )
        
        # Handle button clicks
        handle_pagination_controls(
            prev_btn, 
            next_btn, 
            'tracks_current_page', 
            total_pages
        )
        
        # Get paginated tracks
        first_idx, paginated_tracks = array_paginator(
            all_tracks, 
            PAGE_SIZE, 
            st.session_state.tracks_current_page
        )
        
        # Render paginated grid
        render_tracks_grid(paginated_tracks, columns=4, idx_offset = first_idx)
        
    else:
        # No pagination needed - show all tracks
        render_tracks_grid(all_tracks, columns=4)

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
    



# from src.data_visualizers import render_tracks_grid
# import streamlit as st
# from src.data_transformers import extract_track_data
# from src.pagination import array_paginator, top_pagination_controllers


# # Layout

# # After fetching and transforming data
# if "time_range" in st.session_state and st.session_state.tracks_data:
#     current_range = st.session_state.time_range

#     available_data = list(st.session_state.tracks_data.keys())

#     if len(available_data) > 1:
#         #TO-DO figure out an option like radio button for the user to change the current_range
#         time_range = st.radio(
#                 "# Select a time_range to see your data! :material/sentiment_excited:",
#                 available_data,

#                 # captions=[
#                 #     "approx. last 4 weeks",
#                 #     "approx. last 6 months",
#                 #     "~1 year of data",
#                 # ],
#                 # key="visibility", #b9b9b9;
#                 # label_visibility=st.session_state.visibility,
#                 # disabled=st.session_state.disabled,
#                 key="visibility",
#                 horizontal=True,
#                 index= available_data.index(str(current_range)),
#             )
            
#         if time_range:
#                 st.write(f":material/music_history: You selected **{time_range}**!")
#                 st.session_state.time_range = time_range
#                 transformed_tracks_data = extract_track_data(st.session_state.tracks_data[time_range], time_range)
#                 st.subheader(f"Your Top Tracks - {time_range.replace('_', ' ').title()}")
#                 render_tracks_grid(transformed_tracks_data.get("tracks", [])[0:100], columns=4)  # 4 columns
#                 # st.rerun()

#     else:
#         top_pagination_controllers(1, 10)
#         transformed_tracks_data = extract_track_data(st.session_state.tracks_data[current_range], current_range)
#         st.subheader(f"Your Top Tracks - {current_range.replace('_', ' ').title()}")
#         render_tracks_grid(transformed_tracks_data.get("tracks", [])[0:100], columns=4)  # 4 columns

    
# else:
#     st.header("Your Tracks Analytics")
#     st.warning('# Nothing to see!   (>_<)', icon="⚠️")
#     st.divider()
#     st.write("""
#                 <div style="font-size: 1.5rem;">
#                     <p>There's no track data available <b>yet</b>!</p>
#                     <p 
#                     style="background-color: #191970; 
#                     color: #E0FFFF; 
#                     font-weight:600;
#                     padding: 0.5rem 1.5rem; 
#                     border-radius:0.2rem;">
#                          Make sure you are logged in then follow these steps:
#                     </p>
#                     <ol> 
#                         <li>Navigate to Home.</li> 
#                         <li>Choose a <em>time_range</em>!</li>
#                         <li>Press the Tracks button to fetch your data! </li>
#                         <li>Come back here to see your tracks analytics! </li>
#                     <ol> 
#                 <div>
#              """, unsafe_allow_html=True)
    




    