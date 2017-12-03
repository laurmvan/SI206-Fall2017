import os
import json
import facebook
import requests
from datetime import datetime
import io

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAOOTWWQgPp8VVTIeTGY7ULQ5tagpM9lTZBxhSZBPnGIeDydy5uVgck3desZAQYKLi0icqVygkZBAVVM4p999g3ORxbGKIok9O1aBRcaVXFNuckqcwOEApqTUbL3ixDnirtlNSZAn3c4IDWCitZA4PpZBRzoFaQNdj5PrNONZAXZBiN9C7VeIxgxwCPhxRJA47mqGFg1TZAMC3XyuBDKtY79cly9VTlq5vaDAZDZD", version="2.10")

user = graph.get_object('1503585802990219')
# print(type(user['id']))
# friends = graph.get_connections('1503585802990219', 'friends')
# profile = graph.get_connections('1503585802990219', 'posts')
# print(profile)
# print (friends)

profile = graph.get_object(user['id'], fields='name, profile_pic, gender, hometown, education, location{location}')
print (profile['hometown'])


#'name, profile_pic, gender, hometown, education, location{location}, work, timezone'