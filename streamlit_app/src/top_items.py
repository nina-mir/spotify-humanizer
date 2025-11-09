import streamlit as st
import time

def user_top_items_worker(time_range='medium_term'):
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
        print('🎵 Top Songs & 🎤🎷🎶Artists Worker: let\'s get to work!')
        print('✅ Authentication complete! Starting retreiving top artists ...\n')
        print(f'The time_range this worker is retreiving is {time_range}')
             

        try:
            offset = 0
            limit = 50
            
            while True:

                # Fetch the first 50 recently played songs
                results = sp_client.current_user_top_artists(
                    limit=limit, 
                    offset=offset, 
                    time_range=time_range
                )
                print(len(results))
                if not results or 'items' not in results:
                    print(f'⚠️{curr_user["display_name"]} has no top artists!')
                    break 

                if total_items is None:
                    total_items = results['total']  # Set once
                    print(f"Total items available: {total_items}")   

                items = results['items']
                top_artists.extend(items)
                offset += len(items)
                
                if len(top_artists) >= total_items:
                    break

                time.sleep(3)

            print(f'Successfully fetched the top tracks listened by {curr_user["display_name"]}!')
            print(f'Info of {len(top_artists)} artists out of {total_items} total top artists is available!')
            print("let's write it to file!")

            results_data = {
                'metadata': {
                    'time_range': time_range,
                    'total_items': total_items,
                    'fetched_count': len(top_artists),
                    'timestamp': datetime.now().isoformat()
                },
                'artists': top_artists
            }

            with open('results/top_artists.json', 'w', encoding='utf-8') as writer:
                json.dump(results_data, writer, indent=2, ensure_ascii=False)

            print(f"💾 Results saved to results/top_artists.json")
            
            return


        except Exception as e:
            print(f'error {e} occurred.')