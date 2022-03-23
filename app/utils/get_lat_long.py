import requests

API_URL = 'http://api.positionstack.com/v1/forward'
API_KEY = 'eae43cf933f08d739e75c176359d0b6c'


def get_lat_long(address, city, zipcode, country_code):
    query = ', '.join([address, city, country_code])
    response = requests.get(f"{API_URL}?access_key={API_KEY}&query={query}&limit=80").json()['data']
    for result in response:
        if result['postal_code'] == zipcode:
            return result['latitude'], result['longitude']
    return None, None
