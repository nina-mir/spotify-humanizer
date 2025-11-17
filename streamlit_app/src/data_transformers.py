from datetime import datetime

def extract_track_data(raw_data, time_range):
    """
    Extract and transform Spotify track data into a simplified format.
    
    Args:
        raw_data (dict): Raw Spotify API response containing track data
        time_range (str): Time range for the data (e.g., 'short_term', 'medium_term', 'long_term')
        
    Returns:
        dict: Simplified track data with metadata and cleaned track list
    """
    tracks = []
    
    # Handle the nested structure - tracks are in raw_data['items']
    for item in raw_data.get('tracks', []):
        # Extract track info (handle both direct track items and nested track items)
        track = item.get('track', item)
        
        # Simplify artists data
        simplified_artists = []
        for artist in track.get('artists', []):
            simplified_artists.append({
                'name': artist.get('name'),
                'id': artist.get('id'),
                'spotify': artist.get('external_urls', {}).get('spotify')
            })
        
        track_info = {
            'name': track.get('name'),      
            'artists': simplified_artists,
            'duration_ms': track.get('duration_ms'),
            'spotify': track.get('external_urls', {}).get('spotify'),
            'popularity': track.get('popularity'),
            'type': track.get('type'),
        }
        tracks.append(track_info)
    
    # Create the final data structure
    result = {
        'time_range': time_range,
        'time_now': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'total_items': raw_data.get('total', len(tracks)),
        'tracks': tracks
    }
    
    return result


def extract_artist_data(raw_data):
    """
    Extract and transform Spotify artist data into a simplified format.
    
    Args:
        raw_data (dict): Raw Spotify API response containing artist data
        
    Returns:
        list: Array of simplified artist dictionaries
    """
    artists = []
    
    # Handle the nested structure - artists are in raw_data['artists']
    for artist in raw_data.get('artists', []):
        artist_info = {
            'name': artist.get('name'),
            'popularity': artist.get('popularity'),
            'images': artist.get('images', []),
            'genres': artist.get('genres', []),
            'followers': artist.get('followers', {}).get('total', 0),
            'spotify': artist.get('external_urls', {}).get('spotify')
        }
        artists.append(artist_info)
    
    return artists