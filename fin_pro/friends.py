import os
import json
import facebook
import requests
from datetime import datetime
import io

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAG3Jir3YpEJe9gwkiHARZAzYT4k9PJW6EwEuEmiZBvjR9DHB0GNzKOagXRlARkm7ySl3FZCbAjch2f2NrRPGa7uK35HKX7jdEt3EOvcx9K3wlFZBaiWHs8H7gozM27OpWQ5ovLhiGaTCOOV3vS0PGVN9nBphSmoDMW8sdltHMu43NISvFWAZD", version="2.10")	

user = 'me'
friend_dict = {}
user = graph.get_object(user)
friends = graph.get_all_connections(user['id'], 'friends')
friend_list = []

print (type(friends))
if friends: # in case the generator is null
	for x in friends:
		print (x)
# while True: #this is what allows for the paging, this one is paging through posts
# 	with open('my_friends.json','a') as f:
# 		for friend in friends['data']:
# 			f.write(json.dumps(friend)+'\n') #next page
# 			#print (post) prints out all posts I've ever posted
# 			friend_list.append(friend)
# 		friends = requests.get(friends['paging']['next']).json()

# print (friend_list)

# for friend in friends['data']:
# 	friend_dict[friend['name']] = friend['id']
# for friend in friend_dict.keys():
# 	print (friend) #prints name not id but I can make it print the id

