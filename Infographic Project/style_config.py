import streamlit as st

def configure_streamlit():
    st.set_page_config(
        page_title="Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"

    )

# style_config.py

def apply_custom_css():
    st.markdown("""
    <style>
    .stSelectbox, .stDateInput {
        background-color: #212529;
        color: white;
        font-weight: bold;
        border: 1px solid #333333 !important;
        border-radius: 12px;
        padding: 5px !important;
    }
    .stSelectbox label, .stDateInput label {
        color: white;
        font-weight: bold;
    }

    .css-2trqyj {
        color: #333333 !important;
    }

    /* Style for the sidebar buttons */
    div.stButton > button {
        background-color: black;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        border: 2px solid white;
        padding: 8px 16px;
        width: 100%;
        margin-top: 10px;
    }

    /* Button hover effect */
    div.stButton > button:hover {
        background-color: #555555;
        border: 2px solid #888888;
    }
    </style>
    
    """, unsafe_allow_html=True)