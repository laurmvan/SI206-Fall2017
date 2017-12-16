import os
import json
import googlemaps
import facebook
import requests
import sqlite3
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

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAJxqeXbpzreOjZCrtoYS6zKN5c84AnW4hZCySZAccZAmfn1JRwcFwVMfhD904dZAOy1LsGRbv78Qqs5WPtHqZBvsZB9a6bd3oT1ZAoKiWoryLNwQD7nXCXBAlhC1ztm7UME4dZCmN1a44U0ckIMGXCPDSHs0pBkT75SQB1uGcax24BOTG56NDsJdoMlWGwjZBwEQZDZD", version="2.10")

class Student():
	def __init__(self, name, ID):
		self.name = name
		self.id = str(ID)

	def get_fb_name(self): #returns Student's Facebook name
		return (self.name) 

	def get_fb_location(self):
		user = graph.get_object(self.id)
		profile = graph.get_object(user['id'], fields='name,hometown')
		if 'hometown' not in profile.keys():
			return "Location not indicated on Facebook"
		else:
			return str(profile['hometown']['name'])

	def get_fb_long(self): #returns longitude fo facebook users hometown
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
		places = graph.search(type='place',
                      center=long_lat_str,
                      fields='name,location')
		# Each given id maps to an object the contains the requested fields.
		for place in places['data']:
			return_list.append('%s %s' % (place['name'].encode(),place['location'].get('zip')))
		return return_list

	def get_fb_id(self):
		return (self.id) #returns Student's FB ID

	def get_friend_count(self):
		friends = graph.get_connections(self.id, 'friends')
		print (friends['data'])
		return ""

	def get_user_profile(self):
		profile = graph.get_object(self.id, fields='name, gender, hometown, education, location{location}, work, timezone')
		print ("Name: " + profile['name'])
		print (json.dumps(profile, indent=4))
		return (profile['hometown']['name'])

	def google_maps(self):
		profile = graph.get_object(self.id, fields='hometown')	
		gm = googlemaps.Client(key=google_key)
		geocode_result = gm.geocode(profile['hometown']['name'])[0]
		return (geocode_result['geometry']['location'])

	def get_current_weather(self):	
		base_url = 'https://api.darksky.net/forecast/' #base url
		api_key = '13c846e2deb97661c79a55ca57c287dd'
		lat = self.get_fb_lat() +','
		lng = self.get_fb_long()
		full_url = base_url+api_key+'/'+lat+lng
		response = requests.get(full_url)
		data = json.loads(response.text)
		test_data = open('dark_skys.txt','a',encoding = 'utf-8')
		test_data.write(json.dumps(data))
		test_data.close()
		UVI = str(data['currently']['uvIndex'])
		rain = str(data['currently']['precipProbability'])
		temp = str(data['currently']['temperature'])
		print ('Summary: ' + data['currently']['summary'])
		print ('Temperature: ' + temp)
		print ('UV Index: ' + UVI)
		print ('Probability of rain: ' + rain)

	def get_posts_simple(self): #this returns a list of all posts as dictionaries
		post_list = []
		feed = graph.get_connections(self.id, 'posts') #variable for personal feed
		feed = feed['data']
		return (feed)




	# print (json.dumps(profile, indent=4)) #this prints out the profile
	#___________________________________________________________________________

	def get_friends(self): #prints a dictionary of friends as the keys and their id numbers as the values. Also made it so it would return a list of Friend() objects.
	#still need to figure out how to page through
		friend_dict = {}
		list_friend_objects = []
		friends = graph.get_connections(self.id, 'friends')
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




		#___________________________________________________________________________
		#same as above but using the get_connections to get more fields/information
	def get_post_database(self):
		posts = graph.get_connections(self.name, 'posts') # change later once i can get permissions to 
		new_posts = {}
		post_list = []
		CACHE_FNAME = 'my_posts1.json'

		while True: #this is what allows for the paging, this one is paging through posts
		    try:
		        with open(CACHE_FNAME,'a',encoding = 'utf-8') as f:
		            for post in posts['data']:
		                post_list.append(post)
		                f.write(json.dumps(post) + '\n') #next page
		            posts = requests.get(posts['paging']['next']).json()
		        return_post_list = post_list
		    except KeyError: #there are no more pages to go through
		        break

		new_posts['data'] = (return_post_list)
		cache_file = open(CACHE_FNAME, 'w', encoding = 'utf-8')
		cache_file.write(json.dumps(new_posts))
		cache_file.close()

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
			
#___________________________________________________________________________

#how we can parse data and mine for time information

# def get_parser():
# 	parser = ArgumentParser()
# 	parser.add_argument('--file','-f', required = True, help = 'The json file with all posts')
# 	return parser


#in terminal run python3 "filename" -f "posts.json" to grab from cached data
def make_output_graph():
	posts = graph.get_connections('me', 'posts')
	new_posts = {}
	post_list = []
	CACHE_FNAME = "my_posts1.json"

	while True: #this is what allows for the paging, this one is paging through posts
	    try:
	        with open(CACHE_FNAME,'a',encoding = 'utf-8') as f:
	            for post in posts['data']:
	                post_list.append(post) #next page
	            posts = requests.get(posts['paging']['next']).json()
	        return_post_list = post_list
	    except KeyError: #there are no more pages to go through
	        break	   

	post_times = []
	for i in range(len(return_post_list)):
		time = return_post_list[i]['created_time']
		created_time = dateutil.parser.parse(time)
		post_times.append(created_time.strftime('%H:%M:%S')) #changes str object into datetime
	ones = np.ones(len(posts)) #uses numpy to find ones
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

#___________________________________________________________________________
#User input loop

student_me = Student('me', ID = 1090157221024558)
keep_going = ""
user_input_student = student_me
while (keep_going is not '0'):
	print (user_input_student.get_fb_name())
	print ('\n' +"What would you like to do with your facebook data : " + '\n')
	print ("1. Return user profile")
	print ("2. Search for current user's hometown")
	print ("3. Get weather in user's hometown")
	print ("4. Get 10 most recent user posts")
	print ("5. Get all past posts in a database")
	print ("6. Get graph of posts per hour")
	print ("7. Get current geolocation")
	# print ("6. Get places near user")
	# print ("4. Plot friends on a map")
	# print ("9. Select new user")
	print ("0. Quit" + '\n')
	keep_going = input("Enter number for your choice: ")

	if keep_going is '1':
		print ('\n' + "Name: " + user_input_student.get_fb_name())
		print ("ID: " + user_input_student.get_fb_id())
		print ("Friends: ")
		user_input_student.get_friends()
		print ('\n') #returns 5 friends
		# print ("Friend count: " + user_input_student.get_friends())

	if keep_going is '2':
		print ('\n'+"Hometown: " + user_input_student.get_fb_location() + '\n')

	if keep_going is '3':
		print (user_input_student.get_current_weather())

	if keep_going is '9':
		user_input = input("Please enter a Facebook User's name: ") #returns a search of 25 users
		user_input_student = (search_for_a_user(user_input))
		print ('\n')

	if keep_going is '4':
		print ("Most recent Facebook post: ")
		print (user_input_student.get_posts_simple())

	if keep_going is '5':
		user_input_student.get_post_database()
		print ('\n'+ 'A database named "posts.sqlite" can now be opened in DB Browser')

	if keep_going is '6':
		make_output_graph()

	if keep_going is '7':
		print (user_input_student.google_maps())


 
#___________________________________________________________________________

#This next part takes information from a facebook posts and creates a wordcloud



