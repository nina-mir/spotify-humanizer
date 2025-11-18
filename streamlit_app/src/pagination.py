import streamlit as st

def array_paginator(table, page_size, page_number):
    first_idx = (page_number -1) * page_size
    end_idx = first_idx + page_size
    return table[first_idx:end_idx]


def top_pagination_controllers(page, total_pages):
    st.markdown("""
        <style>
        /* Target multiple levels up the DOM tree */
        div[data-testid="stLayoutWrapper"]:has(.st-key-top-pagination)
        {
            position: sticky !important;
            top: 4.25rem !important;
            z-index: 999 !important;
        }
                
               
        /* controllers' main parent container */
        .st-key-top-pagination  div[data-testid="stLayoutWrapper"] > div[data-testid="stHorizontalBlock"] {
                background-color: #dbdbdb !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                border-radius: 8px !important;
                display: flex !important;
                flex-direction: row !important;
                gap: 0.2rem !important;
                justify-content: center !important;
                align-items: center !important;
        }
        
        .st-key-top-pagination  div[data-testid="stLayoutWrapper"] > div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]{
            flex: 1 !important;
            min-width: 0 !important;
            justify-content: center !important;
            align-items: center !important;                                
        }
        
        .st-key-top-pagination div[data-testid="stLayoutWrapper"] > div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"]{
            align-items: center !important;
        }
                
        span[aria-label="arrow_back_2 icon"],
        span[aria-label="play_arrow icon"] {
            font-size: 1.8rem !important;
        }
                
        </style>
    """, unsafe_allow_html=True)


    with st.container( key="top-pagination", horizontal=True,horizontal_alignment="center",gap=None):
        # Top controls
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            prev_btn = st.button("# :material/arrow_back_2:", disabled=page==1, type="tertiary")
        with col2:
            st.markdown(f'<center style="font-size:1.2rem;">Page {page} of {total_pages}</center>', unsafe_allow_html=True)
        with col3:
            next_btn = st.button("# :material/play_arrow:", disabled=page==total_pages, type="tertiary")

    return prev_btn, next_btn
