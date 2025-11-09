import streamlit as st

def init_global_sidebar_styles():
    """
    Apply custom CSS styling to the Streamlit sidebar and global app elements.

    Insert content/text for the sidebar.
    
    This function injects custom CSS to:
    - Style sidebar components (background, text, headers)
    - Modify global app appearance (fonts, colors, spacing)
    - Ensure consistent theming across all app sections
    
    Note: Uses st.markdown with unsafe_allow_html=True to inject CSS
    """

    st.title('spotify humanizer👱🏽🎧')
    # Minimal margins
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #1a1a1a;
            padding: 0 0.2rem;
            padding-top: 0 !important;
            color: #d1d1d1;
        }
        
        [data-testid="stSidebarContent"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Collapse button when sidebar is CLOSED (hamburger menu) */
        [data-testid="collapsedControl"] {
            background-color: white !important;
            border: 2px solid #4CAF50 !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
        }
        
        [data-testid="collapsedControl"] svg {
            fill: #1a1a1a !important;
        }
        
        /* Target the button that contains the Material icon when sidebar is OPEN */
        [data-testid="stSidebar"] button:has([data-testid="stIconMaterial"]) {
            background-color: #757575 !important;
            border: 1px solid #303030 !important;
            border-radius: 8px !important;
            padding: 0.2rem !important;
        }
        
        /* Style the Material icon itself */
        [data-testid="stSidebar"] [data-testid="stIconMaterial"] {
            color: #1a1a1a !important;
        }
        
        /* Alternative: target by the icon's SVG if it exists */
        [data-testid="stSidebar"] button:has([data-testid="stIconMaterial"]) svg {
            fill: #1a1a1a !important;
        }
        
        /* Hover effects */
        [data-testid="collapsedControl"]:hover,
        [data-testid="stSidebar"] button:has([data-testid="stIconMaterial"]):hover {
            background-color: #f0f0f0 !important;
            border-color: #45a049 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    


    with st.sidebar:
        st.write("")  # Add empty space
        st.markdown('# hi! :material/cruelty_free:')
        st.markdown("""
            <p style="font-size:1.2rem;">
            Very recently I realized I don\'t know the names of the artists I've listened to 10<sup>1000</sup> times!
            I did not know their stories, what city they are making music from, their faces,...!😵
            </p>
        """, unsafe_allow_html=True)
        st.markdown("""
            <p 
                style="font-size:1.2rem; font-family: "new-zen", sans-serif;font-weight:300;
                font-style: italic;"
            >
            I decided to humanize my relationship with Spotify!😸
            </p>
        """, unsafe_allow_html=True)
        
