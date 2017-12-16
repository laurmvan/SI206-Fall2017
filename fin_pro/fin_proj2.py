import os
import json
import facebook
import requests
from datetime import datetime

from argparse import ArgumentParser #for time frequency analysis ****** need to do a sudo pip install argparse in terminal to import this
import dateutil.parser #for time frequency analysis ****** type sudo pip3 install  python-dateutil in terminal to import this
import numpy as np #for time frequency analysis ****** type sudo pip3 install  numpy in terminal to import this
import pandas as pd #refer to slides from class ****** sudo pip3 install pandas in terminal to import this
import matplotlib.pyplot as plt #for time frequency analysis  ****** sudo pip3 install matplotlib in terminal to import this

#Name: Lauren Van Vlierbergen
#Final Project Version1 ALL TOGETHER

#this is the information for the facebook API
#___________________________________________________________________________

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAME1mZBN4EzZALB5njvbjZCZAq5ZAf42N0jLgJrsjyecQIp0GFJhhUyB2F5xQZAwVR9vcM2gbZBkeEmjgg6okskiVjbOydlv38MOawJJUtXPrDFy9UvNLPJRrHfZBJbxVUDlDg0is3vgmXuQn4H6fZCT6yIRe1SSLTER4IRX1njWEmBZAOrAaIMUfvpZAyMyVoTwQZDZD", version="2.10")

profile = graph.get_object('me', fields='name,location{location}') #prints out my current location with the longitude and latitude of the location (good to be used for the weather API darkskies)


#___________________________________________________________________________

user = graph.get_object('me')
#___________________________________________________________________________
#this is one way to get all posts into another file

posts = graph.get_connections('me', 'posts')


# while True: #this is what allows for the paging, this one is paging through posts
# 	try:
# 		with open('my_posts.json','a') as f:
# 			for post in posts['data']:
# 				f.write(json.dumps(post)+'\n') #next page
# 				#print (post) prints out all posts I've ever posted
# 			posts = requests.get(posts['paging']['next']).json()
# 	except KeyError: #there are no more pages to go through
# 		break

#___________________________________________________________________________
#same as above but using the get_connections to get more fields/information

# all_fields = [
# 'message',
# 'created_time',
# 'description',
# 'caption',
# 'link',
# 'place',
# 'status_type'
# ]
# all_fields = ','.join(all_fields)

# posts2 = graph.get_connections('me','posts',fields=all_fields)

# while True: #this is what allows for the paging, this one is paging through posts
# 	try:
# 		with open('my_posts2.json','a') as i:
# 			for post in posts['data']:
# 				i.write(json.dumps(post)+'\n') #next page
# 				#print (post) prints out all posts I've ever posted
# 			posts = requests.get(posts['paging']['next']).json()
# 	except KeyError: #there are no more pages to go through
# 		break



#___________________________________________________________________________

#how we can parse data and mine for time information

# def get_parser():
# 	parser = ArgumentParser()
# 	parser.add_argument('--file','-f', required = False, help = 'The json file with all posts')
# 	return parser

posts = graph.get_connections('me', 'posts')

new_posts = {}
post_list = []
CACHE_FNAME = "my_posts1.json"
#in terminal run python3 fin_proj2.py -f "my_posts1.json" to grab from cached data

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

#___________________________________________________________________________
#This next part takes information from a facebook posts and creates a wordcloud
