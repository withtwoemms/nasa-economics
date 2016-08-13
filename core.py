import os
import requests

from first import first
from sodapy import Socrata


#-- CONFIG ------------------------->>>
nasa_app_token = os.environ.get('NASA_APP_TOKEN', None)
client = Socrata('data.nasa.gov', nasa_app_token)
#----------------------------------->>>

questions = {
    1: 'Q: In 2008, what are the top 5 countries with documented meteor strikes and published scientific technical journals?',
    2: 'Q: In 2010, what are the top 5 countries with documented meteor strikes and published scientific technical journals?',
    3: 'Q: What countries are unique to both years?',
    4: 'Q: What countries are the same from both years?',
    5: 'Q: Can you infer anything from this data? Why or why not?',
}

def get_meteorite_landing_coordinates_in(year):
    '''
    uses the Socrata client to get an array of arrays (e.g. [[32.41275, 20.74575], ...])
    where each is the coordinates of a meteorite landing in a given year
    '''
    result = client.get('y77d-th95', where="year='{}'".format(year))
    coords = [item.get('geolocation', {}).get('coordinates', None) for item in result]
    return [pair for pair in coords if pair not in [[0,0], None]]

def format_coordinate_pair(pair):
    '''
    should turn an array of floats to a string (e.g. [32.41275, 20.74575] --> '32.41275,20.74575')
    '''
    return ','.join(map(str, pair))

def format_coordinate_pairs(pairs):
    '''
    batch version of format_coordinate_pair
    '''
    return [format_coordinate_pair(pair) for pair in pairs]

def get_country_data_for(formatted_coordinate_pairs):
    '''
    make call to googlemaps api using formatted coordinates and return array of array of dicts
    '''
    maps_api_url = 'http://maps.googleapis.com/maps/api/geocode/json'
    location_urls = [maps_api_url + "?latlng=" + pair for pair in formatted_coordinate_pairs]
    responses = []
    for url in location_urls:
        resp = requests.get(url)
        if resp.status_code == 200:
            responses.append(resp.json())
    return [r.get('results') for r in responses if r.get('status') == 'OK']

def get_country_names_from(country_data):
    return [next((first(item.get('address_components', {})).get('long_name') for item in r if 'country' in item.get('types'))) for r in country_data]

def get_countries_with_meteorite_landings_in(year):
    coords = format_coordinate_pairs(get_meteorite_landing_coordinates_in(year))
    location_data = get_country_data_for(coords)
    return get_country_names_from(location_data)

def get_country_id(country_name):
    resp = requests.get('http://api.worldbank.org/countries/all/?per_page=1000&format=json')
    country_ids = [[item.get('name', None), item.get('id', None)] for item in resp.json()[-1]]
    return next((item[-1].encode('utf-8') for item in country_ids if item[0] == country_name), None)

def get_journal_article_indicator_data_for(country_name, year):
    cid = get_country_id(country_name)
    base_url = 'http://api.worldbank.org/countries/{}'.format(cid)
    query = '?per_page=1000&format=json&date={}'.format(year)
    path = '/indicators/IP.JRN.ARTC.SC{}'.format(query)
    return requests.get(base_url + path).json()

def get_journal_article_indicator_data_for_multiple(country_names, year):
    result = []
    for country in set(country_names):
        resp = get_journal_article_indicator_data_for(country, year)
        if not first(resp).get('message'):
            num_articles = resp[-1][0].get('value')
            num_articles = num_articles if num_articles else u'0'
            result.append({
                'country': country,
                'num_articles': float(num_articles)
            })
    return result
