import os
import json
import facebook
import requests
from datetime import datetime
import io

from argparse import ArgumentParser #for time frequency analysis ****** need to do a sudo pip install argparse in terminal to import this
import dateutil.parser #for time frequency analysis ****** type sudo pip3 install  python-dateutil in terminal to import this
import numpy as np #for time frequency analysis ****** type sudo pip3 install  numpy in terminal to import this
import pandas as pd #refer to slides from class ****** sudo pip3 install pandas in terminal to import this
import matplotlib.pyplot as plt #for time frequency analysis  ****** sudo pip3 install matplotlib in terminal to import this

#Name: Lauren Van Vlierbergen
#Final Project Version1 ALL TOGETHER

#this is the information for the facebook API
#___________________________________________________________________________

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAA1ZCwtqOU2BZCAXFbtYLhWRAZA3qscOcn0f3cCcQWNsAZAmsr8bAVHC7kSFr8PSZBWYZAsP9AaL6wmOs5fifYh9koX2uGg6EJvMTtj0UNWpRemx3VfN8CaZCarVvpfb119hBqpZADqrBkmuzOHceJ0ou1K0jFEn8V0yBy2wCa2OGQQLJtQGnjPFDmZBc8r3oZBgZDZD", version="2.10")

def get_fb_name(friend = 'me'):
	profile = graph.get_object('me', fields='name,location{location}')
	return profile['name']

def get_fb_location(friend = 'me'):
	profile = graph.get_object('me', fields='name,location{location}') #prints out my current location with the longitude and latitude of the location (good to be used for the weather API darkskies)
	# print ((profile['location']['latitude']))
	return profile['location']['location']

def get_fb_long(friend = 'me'):
	profile = graph.get_object('me', fields='name,location{location}')
	return profile['location']['location']['latitude']

def get_fb_lat(friend = 'me'):
	profile = graph.get_object('me', fields='name,location{location}')
	return profile['location']['location']['longitude']

def get_fb_id(friend = 'me'):
	profile = graph.get_object('me', fields='name,location{location}')
	return profile['location']['id']

def get_friend_count(friend = 'me'):
	user = graph.get_object(friend)
	friends = graph.get_connections(user['id'], 'friends')
	return (friends['summary']['total_count'])

# print (json.dumps(profile, indent=4)) #this prints out the profile
#___________________________________________________________________________

def get_friends(friend = 'me'): #returns a dictionary of friends as the keys and their id numbers as the values. 
#still need to figure out how to page through
	friend_dict = {}
	user = graph.get_object(friend)
	friends = graph.get_connections(user['id'], 'friends')
	for friend in friends['data']:
		friend_dict[friend['name']] = friend['id']
	return (friend_dict)

#___________________________________________________________________________
#this is one way to get all posts into another file

def get_posts_simple(friend = 'me'): #this returns a list of all posts as dictionaries
	post_list = []
	posts = graph.get_connections(friend, 'posts')
	while True: #this is what allows for the paging, this one is paging through posts
		try:
			with open('my_posts.json','a') as f:
				for post in posts['data']:
					f.write(json.dumps(post)+'\n') #next page
					#print (post) prints out all posts I've ever posted
					post_list.append(post)
				posts = requests.get(posts['paging']['next']).json()
		except KeyError: #there are no more pages to go through
			return post_list[0] #really long list of all posts so only return most recent post for now (can change this laters)

#___________________________________________________________________________
#same as above but using the get_connections to get more fields/information

def get_posts_advanced():
	all_fields = [
	'message',
	'created_time',
	'description',
	'caption',
	'link',
	'place',
	'status_type'
	]
	all_fields = ','.join(all_fields)
	posts2 = graph.get_connections('me','posts',fields=all_fields)

	while True: #this is what allows for the paging, this one is paging through posts
		try:
			with open('my_posts2.json','a') as i:
				for post in posts['data']:
					i.write(json.dumps(post)+'\n') #next page
					#print (post) prints out all posts I've ever posted
				posts = requests.get(posts['paging']['next']).json()
		except KeyError: #there are no more pages to go through
			break



#___________________________________________________________________________

#how we can parse data and mine for time information

def get_parser():
	parser = ArgumentParser()
	parser.add_argument('--file','-f', required = True, help = 'The json file with all posts')
	return parser


#in terminal run python3 "filename" -f "posts.json" to grab from cached data
def make_output_graph():
	if __name__ == '__main__':
		parser = get_parser()
		args = parser.parse_args()
		with open(args.file) as f:
			posts = []
			for line in f:
				post = json.loads(line)
				created_time = dateutil.parser.parse(post['created_time'])
				posts.append(created_time.strftime('%H:%M:%S'))
			ones = np.ones(len(posts))
			idx = pd.DatetimeIndex(posts) #from panda
			#the series of ones before converting in the following lines
			my_series = pd.Series(ones, index = idx)

			#make into 1 hour buckets
			per_hour = my_series.resample('1H').sum().fillna(0)
			#plot
			fig, ax = plt.subplots()
			ax.grid(True)
			ax.set_title('Post Frequencies')
			width = 0.0
			ind = np.arange(len(per_hour))
			plt.bar(ind, per_hour)
			tick_pos = ind + (width / 2)
			labels = []
			for i in range(24):
				d = datetime.now().replace(hour=i,minute=0)
				labels.append(d.strftime('%H:%M'))
			plt.xticks(tick_pos, labels, rotation=90)
			plt.savefig('FB_posts_per_hr.png') #creates a distribution bar chart and makes a nice figure to refer to about the frequency of when posts are posted. The y axis is number of posts and time of day is on the x-axis
#___________________________________________________________________________
#This next part takes information from a facebook posts and creates a wordcloud

print (get_friends('me'))
# print (get_fb_location('me'))
# print (get_fb_lat('me'))
# print (get_fb_long('me'))
# print (get_fb_id('me'))
#print (get_friend_count('me'))