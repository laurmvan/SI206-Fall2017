import os
import googlemaps
import requests
from bs4 import BeautifulSoup as BS
api_key = os.environ['google_key']



def get_lat_long(city):	
	gm = googlemaps.Client(key=api_key)
	geocode_result = gm.geocode(city)[0]
	return (geocode_result['geometry']['location'])


city_input = input("Enter city: ")
print (get_lat_long(city_input))