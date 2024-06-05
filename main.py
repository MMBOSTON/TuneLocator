# main.py

import pandas as pd
import streamlit as st
from modules.test_data import music_genres, load_test_data
from modules.search import handle
from modules.ui import display_data, user_sign_in
from modules.session_management import initialize_session_state
from modules.zipcode_handle import get_data_by_zip
from modules.real_data import scrape_restaurants_with_musicians  # Import the function

st.set_page_config(layout='wide')  # Optional: Sets the page layout

def main():
    st.title("Tune Locator")
    
    # Sidebar for data source selection
    st.sidebar.title("Options")
    data_source = st.sidebar.radio(
        "Select Data Source",
        ('Test Data', 'Real Data'),
        horizontal=True
    )
    
    if not st.session_state.get('logged_in', False):
        user_sign_in(st.session_state)
    else:
        # Initialize data to an empty DataFrame
        data = pd.DataFrame()

        # Load data based on the selected source
        if data_source == 'Test Data':
            data = load_test_data()
        elif data_source == 'Real Data':
            zip_code = st.sidebar.text_input("ZIP Code", value="", key="selected_zip")
            if zip_code:
                data = scrape_restaurants_with_musicians(zip_code)  # Use the new function
                if data is not None:
                    st.session_state.original_data = data
                else:
                    st.error("Failed to load data. Please try again.")
            else:
                st.error("Please enter a ZIP Code.")

        # Check if data is not empty before processing it
        if not data.empty:
            # Extract unique cities and zip codes from the loaded data
            unique_cities = data['City'].unique().tolist()
            unique_zips = data['Zip_Code'].unique().tolist()

            # Sidebar for filters
            st.sidebar.header("Filters")
            selected_genres = st.sidebar.multiselect("Music Genres", options=music_genres, default=None, key="selected_genres")
            selected_cities = st.sidebar.multiselect("Cities", options=unique_cities, default=None, key="selected_cities")
            selected_zips = st.sidebar.multiselect("ZIP Codes", options=unique_zips, default=None, key="selected_zips")

            # Apply filters and get filtered data
            filtered_data = handle(data, selected_genres, selected_cities, selected_zips)

            # Display the filtered data
            display_data(filtered_data)

if __name__ == "__main__":
    main()