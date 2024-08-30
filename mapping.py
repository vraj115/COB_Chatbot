import requests
import re

# Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyBOnPQ-bMrIGOvDyBDZEwfwWDm4OhlksmU'

def handle_location_query(location):
    """
    Generates a Google Maps URL for a given location.
    """
    # Ensure the entire location string is passed to the Google Maps API
    location = location.strip()
    
    # Replace spaces with '+' for URL encoding
    location = location.replace(" ", "+")

    # Construct the Google Maps search URL
    location = re.sub(r'[^\w\s]', '', location)  # Remove any special characters
    return location




def get_map_url(location):
    """
    Generates a Google Maps URL for a given location.
    """
    # Properly URL-encode the location
    location = requests.utils.quote(location).replace("%20", "+")
    
    base_url = "https://www.google.com/maps/search/"
    params = {
        "api": "1",
        "query": location
    }
    # Construct the URL with encoded parameters
    url = f"{base_url}?{requests.compat.urlencode(params)}"
    return url

def get_directions_url(origin, destination):
    """
    Generates a Google Maps URL for directions from origin to destination.
    """
    # Properly URL-encode the origin and destination
    origin = requests.utils.quote(origin).replace("%20", "+")
    destination = requests.utils.quote(destination).replace("%20", "+")
    
    base_url = "https://www.google.com/maps/dir/"
    params = {
        "api": "1",
        "origin": origin,
        "destination": destination
    }
    # Construct the URL with encoded parameters
    url = f"{base_url}?{requests.compat.urlencode(params)}"
    return url

def get_geocoding(location):
    """
    Fetches the latitude and longitude of a location using the Geocoding API.
    """
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(geocode_url, params=params)
    if response.status_code == 200:
        geocode_data = response.json()
        if geocode_data['results']:
            return geocode_data['results'][0]['geometry']['location']
    return None

def get_directions(origin, destination):
    """
    Fetches directions between two locations using the Directions API.
    """
    directions_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(directions_url, params=params)
    if response.status_code == 200:
        directions_data = response.json()
        if directions_data['routes']:
            return directions_data['routes'][0]['legs'][0]['steps']
    return None
