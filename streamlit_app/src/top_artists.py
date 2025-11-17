from datetime import datetime
import streamlit as st
import time

@st.cache_data
def user_top_artists_worker(time_range='short_term'):
    """
    Make API calls to get user's top songs and artists for different time ranges.
    
    This function performs a series of discrete API calls (not continuous monitoring)
    to retrieve the user's listening statistics across specified time periods.
    
    Args:
        time_range (str): Time period for analysis. Options are:
            - 'long_term': ~1 year of data, updated with new data
            - 'medium_term': ~6 months (default)
            - 'short_term': ~4 weeks
    
    Returns:
        dict or None: Contains top artists and songs data, or None if API call fails
        
    Raises:
        ConnectionError: If API connection fails
        ValueError: If time_range parameter is invalid
    """

    # initial values
    total_items = None
    top_tracks = []
    top_artists = []


    if st.session_state.auth_complete:

         # Create empty placeholders for dynamic updates
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        count_placeholder = st.empty()

        print('🎵 Top Songs & 🎤🎷🎶Artists Worker: let\'s get to work!')
        print(f'The time_range this worker is retreiving is {time_range}')
        
        # Initial status
        status_placeholder.info("Starting to fetch your top artists... :material/cycle:")
        status_placeholder.info(f'The time_range this worker is retreiving is {time_range}')
        

        try:
            offset = 0
            limit = 50

            # set the spotipy client and curr_user info from session cache
            sp = st.session_state.sp_client
            curr_user = st.session_state.curr_user
            
            while True:

                # Update progress
                progress_placeholder.write(f":material/contact_phone: Fetching batch {offset//limit + 1}...")

                # Fetch the first 50 recently played songs
                results = sp.current_user_top_artists(
                    limit=limit, 
                    offset=offset, 
                    time_range=time_range
                )
                print(len(results))

                if not results or 'items' not in results:
                    status_placeholder.warning(f'⚠️ {curr_user["display_name"]} has no top artists!')                    
                    break 

                if total_items is None:
                    total_items = results['total']  # Set once
                    count_placeholder.write(f":material/architecture: Total artists available: **{total_items}**")


                items = results['items']
                top_artists.extend(items)
                offset += len(items)

                 # Update count in real-time
                count_placeholder.write(f":material/moving: Progress: **{len(top_artists)}** / {total_items} artists fetched")
                
                if len(top_artists) >= total_items:
                    break

                time.sleep(3)

            # st.success(f'Successfully fetched the top tracks listened by {curr_user["display_name"]}!')
            # st.success(f'Info of {len(top_artists)} artists out of {total_items} total top artists is available!')
            # Final updates
            status_placeholder.success(f'✅ Successfully fetched top artists for {curr_user["display_name"]}!')
            
            results_data = {
                'metadata': {
                    'time_range': time_range,
                    'total_items': total_items,
                    'fetched_count': len(top_artists),
                    'timestamp': datetime.now().isoformat()
                },
                'artists': top_artists
            }
            

            return results_data


        except Exception as e:
            print(f'error {e} occurred.')