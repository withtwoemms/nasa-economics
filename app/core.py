import json
import os
import redis
import requests

from first import first


#-- CONFIG ------------------------->>>
nasa_app_token = os.environ.get('NASA_APP_TOKEN', '')
db = redis.StrictRedis(
    host='localhost',
    port='6379',
    encoding='utf-8'
)
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
    redis_key = 'meteorite_landings_in' + str(year)
    if db.get(redis_key):
        result = json.loads(db.get(redis_key).decode('utf-8'))
    else:
        url = 'https://data.nasa.gov/resource/y77d-th95.json'
        query = '?$$app_token={}&year={}-01-01T00:00:00.000'.format(nasa_app_token, str(year))
        result = requests.get(url + query).json()
        db.set(redis_key, result)
        db.expire(redis_key, 600000)
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
        if db.get(url):
            data = json.loads(db.get(url).decode('utf-8'))
            status = db.get(url + 'status').decode('utf-8')
        else:
            resp = requests.get(url)
            data = resp.json()
            status = str(resp.status_code)
            db.set(url, json.dumps(data))
            db.set(url + 'status', status)
            db.expire(url, 600000)
            db.expire(url + 'status', 600000)
        if status == '200':
            responses.append(data)
    return [r.get('results') for r in responses if r.get('status') == 'OK']

def get_country_names_from(country_data):
    '''
    TODO: refactor -- currently too complex
    parses the array of results from the googlemaps api to return a list of countries (e.g. ['Libya', 'Ukraine', ...])
    '''
    return [next((first(item.get('address_components', {})).get('long_name') for item in r if 'country' in item.get('types')), None) for r in country_data]

def get_countries_with_meteorite_landings_in(year):
    '''
    main interface for dealing with nasa meteorite api; returns array of cities that had landings in a given year
    '''
    coords = format_coordinate_pairs(get_meteorite_landing_coordinates_in(year))
    location_data = get_country_data_for(coords)
    return get_country_names_from(location_data)

def get_country_id(country_name):
    '''
    calls out to the worldbank api to get a list of dictionaries and returns the cid if the country dict is in the list
    '''
    if db.get('all_countries'):
        resp = json.loads(db.get('all_countries').decode('utf-8'))
    else:
        resp = requests.get('http://api.worldbank.org/countries/all/?per_page=1000&format=json').json()
        db.set('all_countries', json.dumps(resp))
    country_ids = [[item.get('name', None), item.get('id', None)] for item in resp[-1]]
    cid = next((item[-1].encode('utf-8') for item in country_ids if item[0] == country_name), None)
    if isinstance(cid, str):
        return cid
    elif not isinstance(cid, str) and cid != None:
        return cid.decode('utf-8')
    else:
        return None

def get_journal_article_indicator_data_for(country_name, year):
    '''
    TODO: cache
    calls out to the worldbank api to get a list whose last item is a dict with relevant info for country passed
    '''
    cid = get_country_id(country_name)
    base_url = 'http://api.worldbank.org/countries/{}'.format(cid)
    query = '?per_page=1000&format=json&date={}'.format(year)
    path = '/indicators/IP.JRN.ARTC.SC{}'.format(query)
    redis_key = country_name + str(year)
    if db.get(redis_key):
        resp = json.loads(db.get(redis_key).decode('utf-8'))
    else:
        resp = requests.get(base_url + path).json()
        db.set(redis_key, json.dumps(resp))
    return resp

def get_journal_article_indicator_data_for_multiple(country_names, year):
    '''
    returns a list of dictionaries with the country name and the number of articles for said country as entries
    '''
    country_names = [c for c in country_names if c != None]
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
