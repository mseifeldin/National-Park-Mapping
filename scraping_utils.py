from secrets import google_places_key
from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
from datetime import datetime
import json

#####################################
## Scrape NPS site
#####################################
def create_id(site, topic):
    return "{}_{}_{}.json".format(site, topic, str(datetime.now()).replace(' ', ''))


project_dictionary = {}
states_sites_dictionary = {}
park_data = []

def process(response):
    ## use the `response` to create a BeautifulSoup object
    soup = BeautifulSoup( response, 'html.parser')
    links = soup.find_all('a')
    for t in links:
        if "state" in t.attrs['href']:
            project_dictionary[t.attrs['href'][7:9]] = "https://www.nps.gov" + t.attrs["href"]
    return project_dictionary

#################################
#     CONFIG & RUN LIST SCRAPE     #
#################################

cache_file = "NPS.json"
site="NPS"
topic="states"
cache = Cache(cache_file)
base = "https://www.nps.gov/index.htm"
UID = create_id(site, topic)
response = cache.get(UID)

if response == None:
    response = requests.get(base).text
    cache.set(UID, response)

process(response)


#####################################
## NATIONAL SITE CLASS
#####################################

class NationalSite():
    def __init__(self, type, name, desc, address, url=None):
        self.type = type
        self.name = name
        self.description = desc
        self.url = url
        self.address = address

    def gettype(self):
        return self.type

    def getname(self):
        return self.name

    def getdesc(self):
        return self.description

    def getaddress(self):
        return self.address

    def __str__(self):
        return "{} ({}): {}".format(self.name, self.type, self.address)


#####################################
## STATE INFO SCRAPE
#####################################
def state_process(state_response):
    soup = BeautifulSoup(state_response, "html.parser")
    parks = soup.find_all("li", {'class':"clearfix"})
    parks = parks[:-1]
    park_instances = []
    for park in parks:
        type = str(park.h2.string)
        name = str(park.h3.a.string)
        desc = str(park.p.string)
        try:
            infolink = park.h3.a["href"]
            infopage = "https://www.nps.gov" + infolink + "index.htm"
            soup = BeautifulSoup(requests.get(infopage).text, "html.parser")
            x = soup.find("div", {'itemprop': "address"})
            addresstext = x.get_text()
            address = addresstext.strip()
            address = address.replace('\n', ' ')
            address = address.replace("  " , ",")
        except:
            address = "Sorry, we could not locate this park's address."
        park_instance= NationalSite(type, name, desc, address)
        park_instances.append(park_instance)
    return park_instances

def get_sites_for_state(state_abbr):
    state = state_abbr
    topic= state
    cache = Cache(cache_file)
    base = project_dictionary[state]
    UID = create_id(site, topic)
    state_response = cache.get(UID)
    if state_response == None:
        state_response = requests.get(base).text
        cache.set(UID, state_response)
    NationalSiteList = state_process(state_response)
    return NationalSiteList
