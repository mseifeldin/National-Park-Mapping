from secrets import google_places_key
from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
from datetime import datetime
import json
from scraping_utils import create_id


#####################################
## GOOGLE PLACES API
#####################################

class NearbyPlace():
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long

    def getname(self):
        return self.name

    def getlat(self):
        return self.lat

    def getlong(self):
        return self.long

    def getcoordinates(self):
        return self.lat , self.long

    def __str__(self):
        return "{}".format(self.name)

## Must return the list of NearbyPlaces for the specifite NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list

def get_site_coordinates(national_site):
    site = "GOOGLE"
    topic = national_site
    cache = Cache(cache_file)
    base1 = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
    params_d = {}
    params_d["key"] = google_places_key
    params_d["input"] = national_site
    params_d["inputtype"] = "textquery"
    params_d['fields'] = 'geometry,formatted_address'
    # params_d["locationbias"] = "point:lat,lng"
    UID = create_id(site, topic)
    get_data = cache.get(UID)
    if get_data == None:
        get_data = requests.get(base1, params_d).text
        #testurl = requests.get(base1, params_d).url
        #print(testurl)
        cache.set(UID, get_data)
    lat = 0
    long = 0
    site_data = json.loads(get_data)
    place = site_data['candidates'][0]
    try:
        latitude = place['geometry']['location']['lat']
        longitude = place['geometry']['location']['lng']
        site_coordinates = latitude, longitude
    except:
            site_coordinates = lat,long
    return site_coordinates

def get_nearby_places_for_site(national_site):
    coordinates = get_site_coordinates(national_site)
    latitude = str(coordinates[0])
    longitude = str(coordinates[1])
    location = latitude + "," +longitude
    site = "GOOGLE"
    national_site = national_site
    topic= "nearby " + national_site
    cache = Cache(cache_file)
    base2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    params_d2 = {}
    params_d2["key"] = google_places_key
    params_d2["location"] = location
    params_d2["radius"] = 10000
    UID = create_id(site, topic)
    nearby_response = cache.get(UID)
    if nearby_response == None:
        nearby_response = requests.get(base2, params_d2).text
        testurl = requests.get(base2, params_d2).url
        #print(testurl)
        #response = nearby_response.json()
        cache.set(UID, nearby_response)
    responses = json.loads(nearby_response)
    responses = responses["results"]
    NearbyList = []
    for i in responses:
        name = i["name"]
        latitude = i["geometry"]["location"]["lat"]
        longitude = i["geometry"]["location"]["lng"]
        place = NearbyPlace(name, latitude, longitude)
        NearbyList.append(place)
    return NearbyList
