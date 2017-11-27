import os
import json
import facebook
import requests


graph = facebook.GraphAPI(access_token="EAACEdEose0cBAMeqFelcHVWC8B4ITfvZCrFkw3sS501IFrxFfgzOJKkqHFvMy4NvosxkX9DKcIsS69NJF0XXwqByAu54TvKhaoEtrW5QP5IBxlJlga74xZAUmHkmilOEpbUvQglhVkbTkjFlcQWaZAmrYoXyf8gFWx5rWjPDCfx7O0mg7MBKNAIKpgRTW0zmSbCZCzKMPwZDZD", version="2.10")

profile = graph.get_object('me', fields='name,location{location}') #prints out my current location with the longitude and latitude of the location (good to be used for the weather API darkskies)

print (json.dumps(profile, indent=4))

user = graph.get_object('me')
friends = graph.get_connections(user['id'], 'friends')
print (json.dumps(friends, indent=4))

posts = graph.get_connections('me', 'posts')

while True: #this is what allows for the paging, this one is paging through posts
	try:
		with open('my_posts.json','a') as f:
			for post in posts['data']:
				f.write(json.dumps(post)+'\n') #next page
				#print (post) prints out all posts I've ever posted
			posts = requests.get(posts['paging']['next']).json()
	except KeyError: #there are no more pages to go through
		break