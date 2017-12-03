import os
import json
import googlemaps
import facebook
import requests
from bs4 import BeautifulSoup as BS #don't use yet but might so i imported it for now
from datetime import datetime
import io
from datetime import datetime
from argparse import ArgumentParser #for time frequency analysis ****** need to do a sudo pip install argparse in terminal to import this
import dateutil.parser #for time frequency analysis ****** type sudo pip3 install  python-dateutil in terminal to import this
import numpy as np #for time frequency analysis ****** type sudo pip3 install  numpy in terminal to import this
import pandas as pd #refer to slides from class ****** sudo pip3 install pandas in terminal to import this
import matplotlib.pyplot as plt #for time frequency analysis  ****** sudo pip3 install matplotlib in terminal to import this

google_key = "AIzaSyDrl6IwtMnO9kl8DeTvTmlon_BcqzwPmeY"
#Name: Lauren Van Vlierbergen
#Final Project Version1 ALL TOGETHER

#this is the information for the facebook API
#___________________________________________________________________________

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAOOTWWQgPp8VVTIeTGY7ULQ5tagpM9lTZBxhSZBPnGIeDydy5uVgck3desZAQYKLi0icqVygkZBAVVM4p999g3ORxbGKIok9O1aBRcaVXFNuckqcwOEApqTUbL3ixDnirtlNSZAn3c4IDWCitZA4PpZBRzoFaQNdj5PrNONZAXZBiN9C7VeIxgxwCPhxRJA47mqGFg1TZAMC3XyuBDKtY79cly9VTlq5vaDAZDZD", version="2.10")

class Student():
	def __init__(self, name, ID):
		self.name = name
		self.id = str(ID)

	def get_fb_name(self):
		profile = graph.get_object(self.name, fields='name,location{location}')
		return profile['name']

	def get_fb_location(self):
		profile = graph.get_object(self.id, fields='name,location{location}') #prints out my current location with the longitude and latitude of the location (good to be used for the weather API darkskies)
		# print ((profile['location']['latitude']))
		profile = graph.get_object(self.id, fields='name,location{location}')
		if 'location' not in profile.keys():
			return "Location not indicated on Facebook"
		else:
			return str(profile['location']['location'])

	def get_fb_long(self):
		profile = graph.get_object(self.id, fields='hometown')	
		gm = googlemaps.Client(key=google_key)
		geocode_result = gm.geocode(profile['hometown']['name'])[0]
		return (str(geocode_result['geometry']['location']['lng']))

	def get_fb_lat(self):
		profile = graph.get_object(self.id, fields='hometown')	
		gm = googlemaps.Client(key=google_key)
		geocode_result = gm.geocode(profile['hometown']['name'])[0]
		return (str(geocode_result['geometry']['location']['lat']))

	def find_places_near(self):
		return_list = []
		lat = self.get_fb_lat() + '00'
		longg = self.get_fb_long() + '00'
		long_lat_str = longg + ',' + lat
		print (long_lat_str)
		places = graph.search(type='place',
                      center=long_lat_str,
                      fields='name,location')
		# Each given id maps to an object the contains the requested fields.
		for place in places['data']:
			return_list.append('%s %s' % (place['name'].encode(),place['location'].get('zip')))
		return return_list

	def get_fb_id(self):
		profile = graph.get_object(self.name, fields='name,location{location}')
		return profile['location']['id']

	def get_friend_count(self):
		user = graph.get_object(self.name)
		friends = graph.get_connections(user['id'], 'friends')
		return (friends['summary']['total_count'])

	def get_user_profile(self):
		profile = graph.get_object(self.id, fields='name, gender, hometown, education, location{location}, work, timezone')
		print ("Name: " + profile['name'])
		return (profile['hometown']['name'])

	def google_maps(self):
		profile = graph.get_object(self.id, fields='hometown')	
		gm = googlemaps.Client(key=google_key)
		geocode_result = gm.geocode(profile['hometown']['name'])[0]
		return (geocode_result['geometry']['location'])

	def get_current_weather(self):	
		base_url = 'https://api.darksky.net/forecast/'
		api_key = '13c846e2deb97661c79a55ca57c287dd'
		lat = self.get_fb_lat() +','
		lng = self.get_fb_long()
		full_url = base_url+api_key+'/'+lat+lng
		response = requests.get(full_url)
		data = json.loads(response.text)
		UVI = str(data['currently']['uvIndex'])
		rain = str(data['currently']['precipProbability'])
		print ('Summary: ' + data['currently']['summary'])
		print ('UV Index: ' + UVI)
		print ('Probability of rain: ' + rain)



	# print (json.dumps(profile, indent=4)) #this prints out the profile
	#___________________________________________________________________________

	def get_friends(self): #prints a dictionary of friends as the keys and their id numbers as the values. Also made it so it would return a list of Friend() objects.
	#still need to figure out how to page through
		friend_dict = {}
		list_friend_objects = []
		user = graph.get_object(self.name)
		friends = graph.get_connections(user['id'], 'friends')
		for friend in friends['data']:
			friend_to_append = Student(friend['name'], friend['id'])
			list_friend_objects.append(friend_to_append)
			friend_dict[friend['name']] = friend['id']
		for friend in friend_dict.keys():
			print (friend) #prints name not id but I can make it print the id
		return (list_friend_objects)

	#___________________________________________________________________________
	def get_friends_friends(self):
		friends = graph.get_connections(self.id,'friends')
		for friend in friends['data']:
			print ("Name: " + friend['name'] + '   ' + "ID: " + friend['id'])
		return (friends)

		#need to make it so it can go through different pages of people

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
			series = pd.Series(ones, index = idx)

			#make into 1 hour buckets
			per_hour = series.resample('1H').sum().fillna(0)
			#plot
			fig, ax = plt.subplots()
			ax.grid(True)
			ax.set_title('Post Frequencies')
			wid = 0.0
			ind = np.arange(len(per_hour))
			plt.bar(ind, per_hour)
			tick_pos = ind + (wid / 2)
			labels = []
			for i in range(24):
				d = datetime.now().replace(hour=i,minute=0)
				labels.append(d.strftime('%H:%M'))
			plt.xticks(tick_pos, labels, rotation=90)
			plt.savefig('FB_posts_per_hr.png') #creates a distribution bar chart and makes a nice figure to refer to about the frequency of when posts are posted. The y axis is number of posts and time of day is on the x-axis

#___________________________________________________________________________

def search_for_a_user(user_input):
	users = graph.search(type='user',q=user_input)
	count = 1
	student_output_list = []
	for user in users['data']:
		student_output_list.append(Student(user['name'],user['id']))
		print(str(count),')  ','ID: %s      NAME: %s' % (user['id'],user['name'].encode()))
		count += 1
	user_input2 = input("Enter number for " + user_input + " you are looking for: ")
	user_input2 = int(user_input2)
	return student_output_list[user_input2-1]


# print (search_for_a_user('Rebecca Deitch'))
student_me = Student('me', ID = 1090157221024558)
student_becca = Student('Rebecca Deitch', ID = 1503585802990219)
# print (student_me.get_friends())
user = '105479049486624'
# posts = graph.get_connections(user, 'feed', limit=20)
# print(posts)

#1503585802990219

print(student_me.get_user_profile())
print(student_me.get_current_weather())

# for friend in my_friends:
# 	print (friend.get_fb_long())


#___________________________________________________________________________

#This next part takes information from a facebook posts and creates a wordcloud



