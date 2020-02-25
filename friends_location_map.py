import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
from geopy.geocoders import Nominatim
import folium


def get_json_file(acct):
    """
    str -> dict
    Takes person Twitter account and returns
    the dictionary friends information 
    """
    # https://apps.twitter.com/
    # Create App and get the four strings, put them in hidden.py

    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE 
    
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '100'})

    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    return js


def find_friends_location(account):
    """
    str -> list
    Takes the person Twitter account and 
    returns list of tuples (name, [latitude, longtitude])
    """
    json_info = get_json_file(account)
    list_friends = []
    for i in json_info['users']:
        try:    
            geolocator = Nominatim(user_agent="my-application")
            location = geolocator.geocode(i['location'])
            list_friends.append((i['name'], [location.latitude, location.longitude]))
        except:
            continue   
    return list_friends


def map_bulding(list_friends):
    """
    list -> file
    Takes the list of tuples (name, [latitude, longtitude]) and 
    saves the map with markers made by the coordinates and the name.
    """
    map = folium.Map(location= [49.83826, 24.02324], zoom_start = 8)
    
    fg_friends = folium.FeatureGroup(name="Friends")
    for tpl in list_friends:
        fg_friends.add_child(folium.Marker(location= tpl[1], icon=folium.Icon(color = 'green'), popup= tpl[0]))
    map.add_child(fg_friends)
    map.add_child(folium.LayerControl())
    return map._repr_html_()


