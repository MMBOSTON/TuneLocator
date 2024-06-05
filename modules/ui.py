# modules/ui.py
import pandas as pd
import streamlit as st
import time  # Import the time module at the top of your ui.py file
import os  # Import the os module to get the process ID

# Define state as an empty dictionary
state = {}

# Define data as a DataFrame
data = pd.DataFrame()

# def display_filters(state, data):
#     state['text_filter'] = st.text_input('Enter text to filter by')
#     # Add a selectbox to choose the column to sort by
#     state['sort_by'] = st.selectbox('Sort by', options=data.columns.tolist())
#     # Add a selectbox to choose the sorting order
#     state['sort_order'] = st.selectbox('Sort order', options=['Ascending', 'Descending'])

def display(events):
    st.title("Tune Locator")
    # Sort the data before displaying it
    events = events.sort_values(by=state['sort_by'])
    st.table(events)


def display_data(data):
    """Displays the filtered data to the user."""
    # Initialize the session state if it hasn't been done already
    if 'page' not in st.session_state:
        st.session_state.page = 1

    # Define the number of rows per page
    rows_per_page = 10

    # Calculate the number of pages
    num_pages = len(data) // rows_per_page
    if len(data) % rows_per_page > 0:
        num_pages += 1

    # Check if there is more than one page
    if num_pages > 1:
        # Add a slider to select the page
        st.session_state.page = st.slider('Select a page', 1, num_pages, st.session_state.page, key='page_slider')
    else:
        # If there's only one page, set page to 1
        st.session_state.page = 1

    # Calculate the start and end indices for the rows to display on this page
    start = (st.session_state.page - 1) * rows_per_page
    end = start + rows_per_page

    # Replace underscores in column names with spaces for specific columns
    data.rename(columns={'Venue_Name': 'Venue Name', 'Music_Genre': 'Music Genre', 'Zip_Code': 'Zip Code'}, inplace=True)

    # Display the DataFrame for the selected page
    st.dataframe(data.iloc[start:end])
    
def user_sign_in(state):
    st.subheader("User Sign In")
    state['username'] = st.text_input("User Name")
    state['password'] = st.text_input("Password", type="password")
    
    if st.button("Sign In"):
        # Here you would typically check the username and password
        # against your user database. As this is just an example,
        # we're not actually doing that.
        if state['username'] == "admin" and state['password'] == "admin":
            state['logged_in'] = True
            st.success("Logged in successfully")
        else:
            st.error("Incorrect username or password")

# def handle_data(state, data):
#     """Applies the text filter and sorting to the data, then displays the data."""
#     # Apply text filter if it exists
#     if state['text_filter']:
#         data = data[data.apply(lambda row: state['text_filter'].lower() in row.to_string().lower(), axis=1)]

#     # Sort data based on user selection
#     if state['sort_by']:
#         ascending = state['sort_order'] == 'Ascending'
#         data = data.sort_values(by=state['sort_by'], ascending=ascending)

#     # Display the data
#     display_data(data)