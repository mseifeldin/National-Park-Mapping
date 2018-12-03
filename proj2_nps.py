## proj_nps.py
## Skeleton for Project 2, Fall 2018
## ~~~ modify this file, but don't rename it ~~~
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

## you can, and should add to and modify this class any way you see fityou can add attributes and modify the __init__ parameters,as long as tests still pass the starter code is here just to make the tests run (and fail)
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

##############################################END PART 1##################################

#####################################
## API
#####################################

class NearbyPlace():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{}".format(self.name)

## Must return the list of NearbyPlaces for the specifite NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list

def get_nearby_places_for_site(national_site):
    state = state_abbr
    topic= state + " " + site_search_name
    cache = Cache(cache_file)
    UID = create_id(site, topic)
    nearby_response = cache.get(UID)
    if nearby_response == None:
        nearby_response = requests.get(base).text
        cache.set(UID, nearby_response)
    NationalSiteList = state_process(state_response)
    return NationalSiteList
    return []



##############################################END PART 2##################################

#####################################
## PLOTLY MAPS
#####################################


# ## Must plot all of the NationalSites listed for the state on nps.gov
# ## Note that some NationalSites might actually be located outside the state.
# ## If any NationalSites are not found by the Google Places API they should
# ##  be ignored.
# ## param: the 2-letter state abbreviation
# ## returns: nothing
# ## side effects: launches a plotly page in the web browser
# def plot_sites_for_state(state_abbr):
#     pass
#
# ## Must plot up to 20 of the NearbyPlaces found using the Google Places API
# ## param: the NationalSite around which to search
# ## returns: nothing
# ## side effects: launches a plotly page in the web browser
# def plot_nearby_for_site(site_object):
#     pass

##############################################END PART 3##################################


#####################################
## INTERFACE
#####################################

def print_options():
    print("***************************")
    print("*********PARKMAPS**********")
    print("***************************")
    print("--- list <stateabbr> ")
    print("--- nearby <result_number>")
    print("--- map")
    print("--- exit")
    print("--- help")

def main():

 while True:
        print_options()
        user_input = input("Enter a command: ").lower()
        operations = ['list <stateabbr>', 'nearby <result_number>', 'map', 'exit', 'help']
        if "list" in  user_input:
            state_abbr = user_input[-2:]
            list_of_sites = get_sites_for_state(state_abbr)
            numberlist = list(range(len(list_of_sites)+1))
            numberlist = numberlist[1:]
            ziplist = zip(numberlist, list_of_sites)
            state_printlist = dict(ziplist)
            for k in state_printlist:
                print ("{}) {}".format(k, state_printlist[k]))
            current_level = "state"
        elif "nearby" in user_input:
            site_number = int(user_input[7:])
            reference_site = state_printlist[site_number]
            sn = reference_site.getname()
            st = reference_site.gettype()
            site_search_name = sn + " " + st
            print(site_search_name)
            current_level = "nearby"
        elif user_input == "map":
            if current_level == "state":
                print("state_level")
            elif current_level == "nearby":
                get_nearby_places_for_site(national_site)
                print("nearby_level")
            else:
                continue
        elif user_input == 'help':
            print("* `list <stateabbr>` — e.g. `list MI`")
            print("(always available as possible input)")
            print("result: lists, for user to see, all National Sites in a state, with numbers beside them")
            print("valid inputs: a two-letter state abbreviation")
            print("")
            print("*  `nearby <result_number>` — e.g. `nearby 2`")
            print("(available as possible input only if there is an active result set — if you have already input `list <stateabbr>`)")
            print("lists all `Places` nearby a given result")
            print("valid inputs: an integer (that is included in the list)")
            print("")
            print("*   `map` - e.g. `map`")
            print("displays the current results (if any) on a map")
            print("if there are no current results, it shows nothing")
            print("so for example, if the last thing you searched in input was `list MI`, you should see a map of all the national sites in Michigan. If the last thing you searched was e.g. `nearby 2` and 2 on the list was the park `Sleeping Bear Dunes`, you should see a map of all the places near Sleeping Bear Dunes)")
            print("")
            print("* `exit`")
            print("exits the program")
            print("")
            print("*   `help`")
            print("lists available commands (these instructions, as shown above)")


        elif user_input == "exit":
            print("Thank you for exploring with us! Goodbye!")
            exit()
        else:
            print("Please enter an appropriate command! Enter HELP to see what the ")

if __name__ == "__main__":
    main()
