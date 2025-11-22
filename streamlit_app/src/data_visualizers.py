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


def render_tracks_grid(tracks_data, columns=3, idx_offset=0):
    """
    Render tracks in a grid layout with cards showing image, name, rank, followers, and Spotify link.
    
    Args:
        artists_data (list): List of artist dictionaries from extract_artist_data()
        columns (int): Number of columns in the grid (default: 3)

    {
      "name": "Changes",
      "artists": [
        {
          "name": "Antonio Williams",
          "id": "4OdKVXxhqKvBH0rNyv5hn0",
          "spotify": "https://open.spotify.com/artist/4OdKVXxhqKvBH0rNyv5hn0"
        },
        {
          "name": "Kerry McCoy",
          "id": "2gAaA8XU9yOXCgSbAQBdHO",
          "spotify": "https://open.spotify.com/artist/2gAaA8XU9yOXCgSbAQBdHO"
        }
      ],
      "images": [
        {
          "height": 640,
          "url": "https://i.scdn.co/image/ab67616d0000b273e9856af993182cfe6cbb2064",
          "width": 640
        },
        {
          "height": 300,
          "url": "https://i.scdn.co/image/ab67616d00001e02e9856af993182cfe6cbb2064",
          "width": 300
        },
        {
          "height": 64,
          "url": "https://i.scdn.co/image/ab67616d00004851e9856af993182cfe6cbb2064",
          "width": 64
        }
      ],
      "duration_ms": 248035,
      "spotify": "https://open.spotify.com/track/3y5YNaqouWN4A8wfynfel5",
      "popularity": 46,
      "type": "track"
    }


    """
    if not tracks_data:
        st.warning("No tracks data to display 🤪")
        return


    # Create grid layout
    for idx in range(0, len(tracks_data), columns):
        cols = st.columns(columns)
        
        # Fill each column with track cards
        for col_idx, col in enumerate(cols):
            track_idx = idx + col_idx
            
            # Check if we have an artist for this position
            if track_idx >= len(tracks_data):
                break
            
            track = tracks_data[track_idx]
            rank = track_idx + 1 + idx_offset # Rank is 1-indexed
            
            with col:
                # Create a container for the card
                with st.container(border=True):
                    # Track image (use largest available, fallback to medium or small)
                    if track['images']:
                        image_url = track['images'][0]['url']  # Largest image first
                        st.image(image_url, width="stretch")
                    else:
                        st.image("https://via.placeholder.com/300x300?text=No+Image", width="stretch")
                    
                    # Rank badge
                    st.markdown(f"### #{rank}")
                    
                    # Track name
                    st.markdown(f"**{track['name']}**")

                    # Track artists
                    artists =  track.get('artists', [])
                    if artists:
                        for artist in artists:
                            st.markdown(f"[{artist.get('name', {})}]({artist.get('spotify', {})})")

                    # Popularity score
                    st.caption(f"📊 Popularity: {track['popularity']}/100")
                    
                    
                    # Spotify link button
                    if artist['spotify']:
                        st.link_button(
                            "Play on Spotify",
                            track['spotify'],
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
    