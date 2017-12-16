import os
import json
import googlemaps
import facebook
import requests
import sqlite3
from datetime import datetime
import io
#from argparse import ArgumentParser #for time frequency analysis ****** need to do a sudo pip install argparse in terminal to import this
import dateutil.parser #for time frequency analysis ****** type sudo pip3 install  python-dateutil in terminal to import this
import numpy as np #for time frequency analysis ****** type sudo pip3 install  numpy in terminal to import this
import pandas as pd #refer to slides from class ****** sudo pip3 install pandas in terminal to import this
import matplotlib.pyplot as plt #for time frequency analysis  ****** sudo pip3 install matplotlib in terminal to import this
from mpl_toolkits.basemap import Basemap #for map of location
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation) #i was getting a weirdd warning

google_key = "AIzaSyDrl6IwtMnO9kl8DeTvTmlon_BcqzwPmeY" #this is a key that can be used by anyone for testing purposes of this project

post_cache = open('profile_Lauren.json','r') # this is caching all of my profile information. This program works for my user information, but can be scaled to multiple users in the future.s
data = post_cache.read()
profile = json.loads(data) #data from text file in a dictionary
post_cache.close()

#Name: Lauren Van Vlierbergen
#Final Project Final Version

#this is the information for the facebook API
#___________________________________________________________________________

graph = facebook.GraphAPI(access_token="EAACEdEose0cBADaD4MZBumT0DYtU9hZCdPLlIYUH2iXLZBcg1jxPZAsKo9k6Jz1uBTB280urXeXXxl1PN1HDGQEpzZBgbOxoIypqE9pZCaagsOxWC4eKvmd2x71qltbcnJQV7S7PZAdZBuRrYjcOeq7BNYzZABRqKozBN40BjgtCKyHV46Un7wm4OzbHeXZCna6esRxBdQ7ODwhAZDZD", version="2.10")

class Student():
	def __init__(self, name, ID):
		self.name = name
		self.id = str(ID)

	def get_fb_name(self): #returns Student's Facebook name
		return (self.name) 

	def get_fb_location(self):
		# user = graph.get_object(self.id)
		# profile = graph.get_object(user['id'], fields='name,hometown') #only necessary for caching data
		if 'hometown' not in profile.keys():
			return "Location not indicated on Facebook"
		else:
			return str(profile['hometown']['name'])

	def get_fb_long(self): #returns longitude fo facebook users hometown
		# profile = graph.get_object(self.id, fields='hometown')	
		gm = googlemaps.Client(key=google_key)
		geocode_result = gm.geocode(profile['hometown']['name'])[0]
		return (str(geocode_result['geometry']['location']['lng']))

	def get_fb_lat(self):
		# profile = graph.get_object(self.id, fields='hometown')	
		gm = googlemaps.Client(key=google_key)
		geocode_result = gm.geocode(profile['hometown']['name'])[0]
		return (str(geocode_result['geometry']['location']['lat']))

	def find_places_near(self):
		return_list = []
		lat = self.get_fb_lat() + '00'
		longg = self.get_fb_long() + '00'
		long_lat_str = longg + ',' + lat
		places = graph.search(type='place',
                      center=long_lat_str,
                      fields='name,location')
		# Each given id maps to an object the contains the requested fields.
		for place in places['data']:
			return_list.append('%s %s' % (place['name'].encode(),place['location'].get('zip')))
		return return_list

	def make_location_graph(self):
		# profile = graph.get_object(self.id, fields='hometown') #this is for when not using cached data
		gm = googlemaps.Client(key=google_key)
		geocode_result = gm.geocode(profile['hometown']['name'])[0]
		lat1 = geocode_result['geometry']['location']['lat']
		lon1 = geocode_result['geometry']['location']['lng']
		m = Basemap(projection = 'mill', llcrnrlat = 20, urcrnrlat=50,\
		llcrnrlon=-130,urcrnrlon=-60,resolution = 'c') #miller cyndrical map look of whole US, these are corner parameters listed here
		m.drawcoastlines() #draw lines on the coast
		m.drawcountries() #draw country lines
		m.drawstates() #draw state lines
		m.fillcontinents() #fill continents
		lat,lon = lat1, lon1 # need to change this into a format basemap understands
		#change this to an array
		x,y = m(lon,lat)
		m.plot(x,y,'ro') #plot the point
		m.drawmapboundary()
		plt.title('Current Location')
		plt.show()

	def get_fb_id(self):
		return (self.id) #returns Student's FB ID

	def get_user_profile(self):
		# profile = graph.get_object(self.id, fields='name, gender, hometown, education, location{location}, work, timezone') #this is for when not using cached data
		print ("Name: " + profile['name'])
		print (json.dumps(profile, indent=4))
		return (profile['hometown']['name'])

	def google_maps(self):
		# profile = graph.get_object(self.id, fields='hometown')	#this is for when not using cached data
		gm = googlemaps.Client(key=google_key)
		geocode_result = gm.geocode(profile['hometown']['name'])[0]
		return (geocode_result['geometry']['location'])

	def get_current_weather(self):	
		base_url = 'https://api.darksky.net/forecast/'
		api_key = '13c846e2deb97661c79a55ca57c287dd' #my personal dark skies API key but cn be used by others as well
		lat = self.get_fb_lat() +','
		lng = self.get_fb_long()
		full_url = base_url+api_key+'/'+lat+lng

		try:
			post_cache = open('dark_skys.json','r') #first check for cached posts in dark skies
			resp = post_cache.read()
			data = json.loads(data) #data from text file in a dictionary
			post_cache.close()
		except:
			response = requests.get(full_url)
			data = json.loads(response.text)
			test_data = open('dark_skys.json','a',encoding = 'utf-8')
			test_data.write(json.dumps(data))
			test_data.close() #makes a cached file of weather
		UVI = str(data['currently']['uvIndex'])
		rain = str(data['currently']['precipProbability'])
		temp = str(data['currently']['temperature'])
		print ('Summary: ' + data['currently']['summary'])
		print ('Temperature: ' + temp)
		print ('UV Index: ' + UVI)
		print ('Probability of rain: ' + rain)

	#this returns a list of all posts as dictionaries. useful to find a few posts from a friends feed, but difficult to page for friends posts -- something I could look into further if I continue to follow up with this process
	def get_posts_simple(self): 
		post_list = []
		feed = graph.get_connections(self.id, 'posts') #variable for personal feed
		feed = feed['data']
		return (feed)

	#This function checks to see if there is a cached file with my posts, and if there's not, it then makes an API request to get my posts and then create a cached file from them.
	def get_my_posts(self):
		new_posts = {}
		post_list = []
		#posts = graph.get_connections(self.id, 'posts') #only necessary to make a request if there is not a current my_posts.json in the directory

		try:
			post_cache = open('my_posts1.json','r') #first check for cached posts
			data = post_cache.read()
			response_post_list = json.loads(data) #data from text file in a dictionary
			post_cache.close()
			return response_post_list
		except:
			while True: #this is what allows for the paging, this one is paging through posts
				try:
					for post in posts['data']:
						post_list.append(post)
						# f.write(json.dumps(post) + '\n') #next page
					posts = requests.get(posts['paging']['next']).json()
					return_post_list = post_list
				except KeyError: #there are no more pages to go through
					new_posts['data'] = return_post_list
					cache_file = open('my_posts1.json','w')
					data = json.dumps(new_posts)
					cache_file.write(data)
					cache_file.close()
					break
		return new_posts #return so it can be used by other functions

	#___________________________________________________________________________
	def get_friends(self): #prints a dictionary of friends as the keys and their id numbers as the values. Also made it so it would return a list of Friend() objects.
	#still need to figure out how to page through
		friend_dict = {}
		list_friend_objects = []
		friends = graph.get_connections(self.id, 'friends') #cannot be run without API key so this function is not called on in the user output loop
		for friend in friends['data']:
			friend_to_append = Student(friend['name'], friend['id'])
			list_friend_objects.append(friend_to_append)
			friend_dict[friend['name']] = friend['id']
		for friend in friend_dict.keys():
			print (friend) #prints name not id but I can make it print the id
		return (list_friend_objects)

	#___________________________________________________________________________

	def get_post_database(self): #creates a database that can be manipulated in sq.lite with every Facebook post I have ever made
		new_posts = self.get_my_posts()

		conn = sqlite3.connect('posts.sqlite')
		cur = conn.cursor()

		cur.execute('DROP TABLE IF EXISTS Posts')

		p = 'CREATE TABLE IF NOT EXISTS '
		p += 'Posts (post_id TEXT, post_text TEXT, time_posted TEXT, post_story TEXT)'
		cur.execute(p)

		container = []

		for i in range(len(new_posts['data'])):
		    if 'message' not in (new_posts['data'][i]).keys():
		        post_text = "No content"
		    else:
		        post_text = new_posts['data'][i]["message"]
		    post_id = new_posts['data'][i]["id"]
		    created_at_item = new_posts['data'][i]["created_time"]
		    if 'story' not in (new_posts['data'][i]).keys():
		        post_story = "No story"
		    else:
		        post_story = new_posts['data'][i]["story"]
		    container.append((post_id, post_text, created_at_item, post_story))
		#print (container)

		p = 'INSERT INTO Posts VALUES (?, ?, ?, ?)'
		for post in container:
		    cur.execute(p, post)

		conn.commit()

	def make_output_graph(self = None): #makes graph of all posts ever (bar graph)
		my_post_list = self.get_my_posts()
		return_post_list = my_post_list['data']

		post_times = []
		for i in range(len(return_post_list)):
			time = return_post_list[i]['created_time']
			created_time = dateutil.parser.parse(time)
			post_times.append(created_time.strftime('%H:%M:%S')) #changes str object into datetime
		ones = np.ones(len(return_post_list)) #uses numpy to find ones
		idx = pd.DatetimeIndex(post_times) #from panda
		#the series of ones before converting in the following lines
		my_series = pd.Series(ones, index = idx)

		#make into 1 hour buckets
		per_hour = my_series.resample('1H').sum().fillna(0)
		#plot the data
		fig, ax = plt.subplots()
		ax.grid(True)
		ax.set_title('Number of Posts at Different Times') #title of png file
		width = 0.0
		ind = np.arange(len(per_hour))
		plt.bar(ind, per_hour)
		tick_pos = ind + (width / 2)
		labels = []
		for i in range(24):# range 0-24 represents lilnk in military time
			d = datetime.now().replace(hour=i,minute=0)
			labels.append(d.strftime('%H:%M'))
		plt.xticks(tick_pos, labels, rotation=90) #just makes the labels look better
		plt.savefig('FB_posts_per_hour_cached.png') #creates a distribution bar chart and makes a nice figure to refer to about the frequency of when posts are posted. The y axis is number of posts and time of day is on the x-axis
		return ("Check directory for a graph of your post frequencies called FB_posts_per_hr")

#___________________________________________________________________________

def search_for_a_user(user_input): #this can only be used online. Not applicable to this particular phase, but in the future I look to be able to run this program on more than just me but also on searched users on facebook. This function is called on by option 9 in the user input loop below.
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
#___________________________________________________________________________
#This is the part of the program that accepts user input

student_me = Student('me', ID = 1090157221024558) #information for my profiles
keep_going = ""
user_input_student = student_me #using myself as the input student
while (keep_going is not '0'):
	print ('\n' +"What would you like to do with your facebook data : " + '\n')
	print ("1. Return user profile")
	print ("2. Search for current user's hometown and graph on map")
	print ("3. Get weather in user's hometown")
	print ("4. Get all user posts")
	print ("5. Get all past posts in a database")
	print ("6. Get graph of posts per hour")
	print ("7. Get friends posts")
	print ("0. Quit" + '\n') #enter 0 to exit the loop
	keep_going = input("Enter number for your choice: ")

	if keep_going is '1':
		print ('\n' + "Name: " + user_input_student.get_fb_name())
		print ("ID: " + user_input_student.get_fb_id())
		print ('\n') #returns 5 friends
		# print ("Friend count: " + user_input_student.get_friends())

	if keep_going is '2':
		print ('\n'+"Hometown: " + user_input_student.get_fb_location() + '\n')
		user_input_student.make_location_graph()

	if keep_going is '3':
		print (user_input_student.get_current_weather())


	if keep_going is '4':
		print ("Most recent Facebook post: ")
		print (user_input_student.get_my_posts())
		
	if keep_going is '5':
		print (user_input_student.get_post_database())
		print ('\n'+ 'A database named "posts.sqlite" can now be opened in DB Browser')

	if keep_going is '6':
		user_input_student.make_output_graph()

	if keep_going is '7':
		#friends_list=user_input_student.get_friends() #only when have API key, not cached data
		post_list = []
		return_dict = {}
		f = open('friends_posts.json','r',encoding = 'utf-8')
		friends_posts = json.loads(f.read())
		#insert a graph of words per post
		print (friends_posts)

	if keep_going is '9': #not used in this example - but envoes the search for a user function I made and returns 25 friend results based off of the user's input
		user_input = input("Please enter a Facebook User's name: ") #returns a search of 25 users
		user_input_student = (search_for_a_user(user_input))
		print ('\n')




