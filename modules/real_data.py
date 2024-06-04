import requests
from bs4 import BeautifulSoup

def scrape_restaurants_with_musicians(zip_code):
    """
    Scrapes Yellow Pages for restaurants with musicians playing in the specified ZIP code area.
    
    :param zip_code: The ZIP code to search within.
    :return: A list of dictionaries containing restaurant names, addresses, and musician status.
    """
    base_url = "https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=Framingham%2C+MA"
    search_url = f"{base_url}?zip={zip_code}&musician=true"  # Adjust this URL based on the actual API or search parameters
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    restaurants = []
    for listing in soup.find_all('div', class_='restaurant-listing'):  # Update these selectors based on the website's HTML
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
