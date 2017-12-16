import os
import json
import facebook
import requests
from datetime import datetime
import io

graph = facebook.GraphAPI(access_token="EAACEdEose0cBALtoZBQbZBFz6tJ8KYDrxr8ZBHUOzyqEG6JVQX2N7TOfyZCsCBt0TH0G7pj85FeQNEp6SSMWV7gzfPSdpG5ZBWsUjgRqBzCIuTinXmrNcSEc5ZCBB5uk6CG0GOUIC1eT6qL0jZCuEpfh8R0B8XvuJfOJg1ZAj2peUDo2gaEnibVQCDX1jPwsPEVxqSz9FbJthQZDZD", version="2.10")

user = graph.get_object('100001584408888')

# print(type(user['id']))
# friends = graph.get_connections('1503585802990219', 'friends')
# profile = graph.get_connections('1503585802990219', 'posts')
# print(profile)
# print (friends)

friend_dict = {}
list_friend_objects = []
friends = graph.get_connections(user['id'], 'friends')
print (friends)
for friend in friends['data']:
	friend_dict[friend['name']] = friend['id']
for friend in friend_dict.keys():
	print (friend) #prints name not id but I can make it print the id

# profile = graph.get_object(user['id'], fields='name, gender, hometown, education, location{location}')
# print (profile['hometown']['name'])


#'name, profile_pic, gender, hometown, education, location{location}, work, timezone'