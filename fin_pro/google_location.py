import os
import googlemaps
import requests
from bs4 import BeautifulSoup as BS
api_key = 'AIzaSyDrl6IwtMnO9kl8DeTvTmlon_BcqzwPmeY'



def get_lat_long(city):	
	gm = googlemaps.Client(key=api_key)
	print (type(city))
	geocode_result = gm.geocode(city)[0]
	return (geocode_result['geometry']['location'])


city_input = input("Enter city: ")
print (get_lat_long(city_input))