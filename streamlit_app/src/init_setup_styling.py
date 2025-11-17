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
                
        [data-testid="stSidebarUserContent"] {
                padding-top: unset;
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
        /* Targeting the navbar in the Sidebar */    
        # [data-testid="stSidebarNavLinkContainer"]{
        #     background-color:  #242424;
        # }
                
        [data-testid="stSidebarNavLink"] > span {
            color: white !important;
        }
    
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(
                """
            <style>

            div[class*="stElementContainer"]:has(> [data-testid="stRadio"]) {
                width: 100% !important;
                max-width: 100% !important;
            }

            /* Target label element of the radio group */

            .stRadio > label > div[data-testid="stMarkdownContainer"]{
                font-size: 1.6rem;
            }

            .stRadio [role=radiogroup] {
                width: 100% !important;
                display: flex !important;
                flex-wrap: wrap;
                justify-content: center !important;
                align-items: center !important;  
                gap: 2rem;  /* Space between items */
            }            

            /* targeting the caption text of each radio group item */
            .stRadio div[data-testid="stCaptionContainer"] > p {
                color: #1a1a1a;
                font-family: new-science-mono, sans-serif;
                text-align: center;
                text-shadow: 0 1px 2px rgba(255,255,255,0.8); /* White shadow */

            }
               
            .stRadio div[data-testid="stMarkdownContainer"] > p {
                font-weight: bold;
            }

            /* Mobile breakpoint - stack vertically */
            @media (max-width: 768px) {
                .stRadio [role=radiogroup] {
                    flex-direction: column;
                    align-items: center;
                    justify-content:center;
                }
                
                .stRadio label[data-baseweb="radio"] {
                    flex: none;  /* Reset flex behavior */
                    min-width: 200px;  /* Minimum width before wrapping */

                }
            }
            </style>

                """,
                unsafe_allow_html=True
            )



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
        
