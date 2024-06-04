# modules/search.py

import streamlit as st
import pandas as pd
from .session_management import initialize_session_state

def handle(all_events, selected_genres, selected_cities, selected_zips):
    filtered_data = all_events.copy()

    # Filter by genres if any genres are selected
    if selected_genres:
        filtered_data = filtered_data[filtered_data['Music_Genre'].isin(selected_genres)]
        print(f"After filtering by genres, remaining rows: {len(filtered_data)}")  # Debugging line

    # Filter by cities if any cities are selected
    if selected_cities:
        filtered_data = filtered_data[filtered_data['City'].isin(selected_cities)]
        print(f"After filtering by cities, remaining rows: {len(filtered_data)}")  # Debugging line

    # Filter by zip codes if any zip codes are selected
    if selected_zips:
        filtered_data = filtered_data[filtered_data['Zip_Code'].isin(selected_zips)]
        print(f"After filtering by zip codes, remaining rows: {len(filtered_data)}")  # Debugging line

    return filtered_data