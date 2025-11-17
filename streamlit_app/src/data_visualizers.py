import streamlit as st

def render_artist_grid(artists_data, columns=3):
    """
    Render artists in a grid layout with cards showing image, name, rank, followers, and Spotify link.
    
    Args:
        artists_data (list): List of artist dictionaries from extract_artist_data()
        columns (int): Number of columns in the grid (default: 3)
    """
    if not artists_data:
        st.warning("No artist data to display")
        return


    
    # Create grid layout
    for idx in range(0, len(artists_data), columns):
        cols = st.columns(columns)
        
        # Fill each column with artist cards
        for col_idx, col in enumerate(cols):
            artist_idx = idx + col_idx
            
            # Check if we have an artist for this position
            if artist_idx >= len(artists_data):
                break
            
            artist = artists_data[artist_idx]
            rank = artist_idx + 1  # Rank is 1-indexed
            
            with col:
                # Create a container for the card
                with st.container(border=True):
                    # Artist image (use largest available, fallback to medium or small)
                    if artist['images']:
                        image_url = artist['images'][0]['url']  # Largest image first
                        st.image(image_url, width="stretch")
                    else:
                        st.image("https://via.placeholder.com/300x300?text=No+Image", width="stretch")
                    
                    # Rank badge
                    st.markdown(f"### #{rank}")
                    
                    # Artist name
                    st.markdown(f"**{artist['name']}**")
                    
                    # Followers count (formatted)
                    followers_formatted = f"{artist['followers']:,}"
                    st.caption(f"👥 {followers_formatted} followers")
                    
                    # Popularity score
                    st.caption(f"📊 Popularity: {artist['popularity']}/100")
                    
                    # Genres (if available)
                    if artist['genres']:
                        genres_display = ", ".join(artist['genres'][:3])  # Show max 3 genres
                        st.caption(f"🎵 {genres_display}")
                    
                    # Spotify link button
                    if artist['spotify']:
                        st.link_button(
                            "Open in Spotify",
                            artist['spotify'],
                            width=128
                        )

                    st.markdown("""
                                <style>
                                    [data-testid="stLinkButton"] a {
                                        padding: 0 !important;
                                    }
                                    
                                        
                                .stElementContainer.element-container .stMarkdown div[data-testid="stCaptionContainer"]  {
                                        opacity: 0.85 !important;
                                    }
                                </style>
                                """, unsafe_allow_html=True)
    


def plot_genre_distribution(artists_data):
    """Create genre bar chart"""
    # Logic here
    pass


def render_tracks_grid(artists_data, columns=3):
    """
    Render artists in a grid layout with cards showing image, name, rank, followers, and Spotify link.
    
    Args:
        artists_data (list): List of artist dictionaries from extract_artist_data()
        columns (int): Number of columns in the grid (default: 3)
    """
    if not artists_data:
        st.warning("No artist data to display")
        return


    
    # Create grid layout
    for idx in range(0, len(artists_data), columns):
        cols = st.columns(columns)
        
        # Fill each column with artist cards
        for col_idx, col in enumerate(cols):
            artist_idx = idx + col_idx
            
            # Check if we have an artist for this position
            if artist_idx >= len(artists_data):
                break
            
            artist = artists_data[artist_idx]
            rank = artist_idx + 1  # Rank is 1-indexed
            
            with col:
                # Create a container for the card
                with st.container(border=True):
                    # Artist image (use largest available, fallback to medium or small)
                    if artist['images']:
                        image_url = artist['images'][0]['url']  # Largest image first
                        st.image(image_url, width="stretch")
                    else:
                        st.image("https://via.placeholder.com/300x300?text=No+Image", width="stretch")
                    
                    # Rank badge
                    st.markdown(f"### #{rank}")
                    
                    # Artist name
                    st.markdown(f"**{artist['name']}**")
                    
                    # Followers count (formatted)
                    followers_formatted = f"{artist['followers']:,}"
                    st.caption(f"👥 {followers_formatted} followers")
                    
                    # Popularity score
                    st.caption(f"📊 Popularity: {artist['popularity']}/100")
                    
                    # Genres (if available)
                    if artist['genres']:
                        genres_display = ", ".join(artist['genres'][:3])  # Show max 3 genres
                        st.caption(f"🎵 {genres_display}")
                    
                    # Spotify link button
                    if artist['spotify']:
                        st.link_button(
                            "Open in Spotify",
                            artist['spotify'],
                            width=128
                        )

                    st.markdown("""
                                <style>
                                    [data-testid="stLinkButton"] a {
                                        padding: 0 !important;
                                    }
                                    
                                        
                                .stElementContainer.element-container .stMarkdown div[data-testid="stCaptionContainer"]  {
                                        opacity: 0.85 !important;
                                    }
                                </style>
                                """, unsafe_allow_html=True)
    