# main.py

import streamlit as st
from modules.test_data import music_genres, load_test_data
from modules.search import handle
#from modules.ui import display_data, user_sign_in, display_filters, handle_data
from modules.ui import display_data, user_sign_in

from modules.session_management import initialize_session_state
from modules.zipcode_handle import get_data_by_zip

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
        # Load data based on the selected source
        if data_source == 'Test Data':
            data = load_test_data()
        elif data_source == 'Real Data':
            zip_code = st.sidebar.text_input("ZIP Code", value="", key="selected_zip")
            if zip_code:
                data = get_data_by_zip(zip_code)  # Use the function from zipcode_handler.py
                if data:
                    st.session_state.original_data = data
                else:
                    st.error("Failed to load data. Please try again.")
            else:
                st.error("Please enter a ZIP Code.")
        
        # Call the display_filters function with the loaded data
        #display_filters(st.session_state, data)

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

        # Apply sorting and display the filtered data
        #handle_data(st.session_state, filtered_data)

        # Display the filtered data
        display_data(filtered_data)

if __name__ == "__main__":
    main()