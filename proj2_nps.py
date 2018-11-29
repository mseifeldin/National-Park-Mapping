## proj_nps.py
## Skeleton for Project 2, Fall 2018
## ~~~ modify this file, but don't rename it ~~~
from secrets import google_places_key
from bs4 import BeautifulSoup
from alternate_advanced_caching import Cache
import requests
from datetime import datetime


#####################################
## Scrape NPS site
#####################################
def create_id(site, topic):
    return "{}_{}_{}.json".format(site, topic, str(datetime.now()).replace(' ', ''))

state_dictionary = {}
project_dictionary = {}
park_data = []

def process(response):
    ## use the `response` to create a BeautifulSoup object
    soup = BeautifulSoup( response, 'html.parser')
    links = soup.find_all('a')
    linklist = []
    for t in links:
        if "state" in t.attrs['href']:
            project_dictionary[t.text] = ["https://www.nps.gov" + t.attrs["href"]]
            linklist.append(t.attrs['href'])

    for state in project_dictionary:
        url = project_dictionary[state][0]
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        parks = soup.find_all("li", {'class':"clearfix"})
        parks = parks[:-1]

        for park in parks:
            attr_list = []
            type = str(park.h2.string)
            abrev = url[26:28]
            name = str(park.h3.a.string)
            blurb = str(park.p.string)
            info = park.ul
            try:
                infolink = park.h3.a["href"]
                infopage = "https://www.nps.gov" + infolink + "index.htm"
                soup = BeautifulSoup(requests.get(infopage.text, "html.parser")
                x = soup.find("div", {'itemprop': "address"})
                strings = list(x.stripped_strings)
                address = "\n".join(strings)
                print(address)
            except:
                print("Sorry, we could not locate this park's address.")

            # address = "abc"
            # attr_list = [state, type, name, blurb, abrev, address]
            # park_data.append(attr_list)
    #print(park_data)


###################
#     CONFIG      #
###################
cache_file = "NPS.json"
site="NPS"
topic="parks"
cache = Cache(cache_file)
base = "https://www.nps.gov/index.htm"


#######################
#     RUN PROGRAM     #
#######################
UID = create_id(site, topic)
response = cache.get(UID)

if response == None:
    response = requests.get(base).text
    cache.set(UID, response)

process(response)

#####################################
## DONE SCRAPE
#####################################





## you can, and should add to and modify this class any way you see fityou can add attributes and modify the __init__ parameters,as long as tests still pass the starter code is here just to make the tests run (and fail)
class NationalSite():
    def __init__(self, type, name, desc, url=None):
        self.type = type
        self.name = name
        self.description = desc
        self.url = url

        # needs to be changed, obvi.
        self.address_street = '123 Main St.'
        self.address_city = 'Smallville'
        self.address_state = 'KS'
        self.address_zip = '11111'

#####################################
## END PART ONE
#####################################

# ## you can, and should add to and modify this class any way you see fit you can add attributes and modify the __init__ parameters,as long as tests still pass the starter code is here just to make the tests run (and fail)
# class NearbyPlace():
#     def __init__(self, name):
#         self.name = name
#
# ## Must return the list of NationalSites for the specified state
# ## param: the 2-letter state abbreviation, lowercase
# ##        (OK to make it work for uppercase too)
# ## returns: all of the NationalSites
# ##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
# ##        for the state at nps.gov
# def get_sites_for_state(state_abbr):
#     return []
#
#
# ## Must return the list of NearbyPlaces for the specifite NationalSite
# ## param: a NationalSite object
# ## returns: a list of NearbyPlaces within 10km of the given site
# ##          if the site is not found by a Google Places search, this should
# ##          return an empty list
# def get_nearby_places_for_site(national_site):
#     return []
#



#####################################
## END PART TWO
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

#####################################
## START INTERFACE
#####################################

# ##helper functions
# def convert_list_dictionary(lst):
# 	lst_new = zip(headers, lst)
# 	return dict(lst_new)
#
# ##helper functions
# def load_data(pyflix, dictionary):
# 	title = dictionary['title']
# 	pyflix[title] = dictionary
#
# def pre_load(pyflix):
# 	for item in data_source:
# 		new_dict = convert_list_dictionary(item)
# 		load_data(pyflix, new_dict)
#
#
# def add_movie(pyflix):
# 	## Save the results to varibles
# 	pass
#
# def edit_movie(pyflix):
# 	pass
#
# def show_movies(pyflix):
# 	count = 1
# 	for key in pyflix:
# 		print("{}: {}".format(count, key))
# 		count += 1
#
# def delete_movie(pyflix, key):
# 	pass
#
#
# def print_options():
# 	print("***************************")
#     print("**********PARKMAPS**********")
# 	print("***************************")
# 	print("--- list <stateabbr> ")
# 	print("--- nearby <result_number>")
# 	print("--- map")
# 	print("--- exit")
# 	print("--- help")
#
# def main():
# 	pyflix = {}
# 	pre_load(pyflix)
#
# 	while True:
# 		print_options()
# 		user_input = input("Enter a command: ").lower()
# 		operations = ['list <stateabbr>', 'nearby <result_number>', 'map', 'exit', 'help']
# 		if user_input == "add":
# 			print("We will do something here!")
# 		elif user_input == "edit":
# 			print("We will do something here!")
# 		elif user_input == "show":
# 			show_movies(pyflix)
# 			##print("We've displayed a movie")
# 		elif user_input == 'help':
#             print("* `list <stateabbr>` — e.g. `list MI`")
#             print("(always available as possible input)")
#             print("result: lists, for user to see, all National Sites in a state, with numbers beside them")
#             print("valid inputs: a two-letter state abbreviation")
#             print("*  `nearby <result_number>` — e.g. `nearby 2`")
#             print("(available as possible input only if there is an active result set — if you have already input `list <stateabbr>`)")
#             print("lists all `Places` nearby a given result")
#             print("valid inputs: an integer (that is included in the list)")
#             print("* `map` - e.g. `map`")
#             print("displays the current results (if any) on a map. If there are no current results, it shows nothing")
#             print("so for example, if the last thing you searched in input was `list MI`, you should see a map of all the national sites in Michigan. If the last thing you searched was e.g. `nearby 2` and 2 on the list was the park `Sleeping Bear Dunes`, you should see a map of all the places near Sleeping Bear Dunes)")
#             print("* `exit`")
#             print("exits the program")
#             print("* `help`")
#             print("lists available commands (these instructions)")
# 		elif user_input == "exit":
# 			print("Thank you for binging with us! Goodbye!")
# 			exit()
# 		else:
# 			print("Please enter an appropriate command! Enter HELP to see what the ")
#
# if __name__ == "__main__":
# 	main()

#####################################
## DONE INTERFACE
#####################################
