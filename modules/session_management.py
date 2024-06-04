# modules/session_management.py

import streamlit as st

def initialize_session_state():
    """Initializes the session state for the application."""
    # Ensure the session state is initialized only once per session
    if 'original_data' not in st.session_state:
        st.session_state.original_data = None
    if 'filtered_data' not in st.session_state:
        st.session_state.filtered_data = None
    if 'selected_genres' not in st.session_state:
        st.session_state.selected_genres = []
    if 'selected_zip_codes' not in st.session_state:
        st.session_state.selected_zip_codes = []
    if 'selected_locations' not in st.session_state:
        st.session_state.selected_locations = []
    if 'selected_cities' not in st.session_state:
        st.session_state.selected_cities = []
