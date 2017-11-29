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

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAFIqO3OwMRPZBfZBSXTdt7JBnNzwZAT6hzvxhedEsUObvSLUFyuu64abXQZAZClPUtJ0bCKbS5Y6CKN48ZBYrN6ChUdZBZCH9lTLZBZAA1vwjEtZCkQOyJLwVfdoaMjDPxi0DGkDfgEzXO8x2LCfroQrzcTelShegpSwk4wSmtTaRwOeUtDfNj4sUlfpRIFNko7WwZDZD", version="2.10")

profile = graph.get_object('me', fields='name,location{location}') #prints out my current location with the longitude and latitude of the location (good to be used for the weather API darkskies)

print (json.dumps(profile, indent=4))
#___________________________________________________________________________

user = graph.get_object('me')
friends = graph.get_connections(user['id'], 'friends')

while True:
	try:
		with open('my_friends.json','a') as r:
			for friend in friends['data']:
				r.write(json.dumps(friend)+'\n')
			friends = requests.get(friends['paging']['next']) #having trouble with paging, this is just returning my list of friends 6 times (just 10 friends)
	except KeyError:
		break
print (json.dumps(friends, indent=4))

#___________________________________________________________________________
#this is one way to get all posts into another file

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

#___________________________________________________________________________
#same as above but using the get_connections to get more fields/information

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
