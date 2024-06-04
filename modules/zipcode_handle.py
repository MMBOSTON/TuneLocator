# modules/zipcode_handle.py

import requests
from bs4 import BeautifulSoup

def get_data_by_zip(zip_code):
    """
    Scrapes data for restaurants with musicians in the specified ZIP code area.
    
    :param zip_code: The ZIP code to search within.
    :return: A list of dictionaries containing restaurant names, addresses, and musician status.
    """
    base_url = "https://example.com/search?zip={}"
    search_url = base_url.format(zip_code)
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    restaurants = []
    for listing in soup.find_all('div', class_='restaurant-listing'):  # Update these selectors based on the actual HTML structure
        name = listing.find('span', class_='name').text.strip()
        address = listing.find('span', class_='address').text.strip()
        musicians_playing = listing.find('span', class_='has-musician').text.strip()  # Update based on actual HTML
        if musicians_playing.lower() == 'yes':
            restaurants.append({
                'name': name,
                'address': address,
                'musicians_playing': musicians_playing
            })
    
    return restaurants