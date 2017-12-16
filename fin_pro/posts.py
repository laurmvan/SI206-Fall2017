import os
import json
import facebook
import requests
from datetime import datetime
import sqlite3

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAFKB9YzmZCY9qyRHTHcsAtVhSHUtmxGiOJDjMVqZCbQbv9h7KNbZA0fLjnFK3BZCQv1UtB09hNVff7ytIPyD5CgKxSYWoHZCd2FxZAHG0GehmVkMnC28klz5Ofgqc1ILNOUyxt1r3ZCAJGK7fkDSAz4q9WKixXpA2duPmZBxw58XwM26wEBOXbx2atLRZBumBmgZDZD", version="2.10")

posts = graph.get_connections('me', 'posts')
posts_list = []

CACHE_FNAME = "my_posts1.json"
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.readlines()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
    print (CACHE_DICTION)
except:
    CACHE_DICTION = {}

while True: #this is what allows for the paging, this one is paging through posts
	try:
		with open('my_posts1.json','a') as f:
			for post in posts['data']:
				f.write(json.dumps(post) + '\n') #next page
				#print (post) prints out all posts I've ever posted
			posts = requests.get(posts['paging']['next']).json()
	except KeyError: #there are no more pages to go through
		break




# container = []
# for post in posts_list:
# 	if 'message' in post.keys():
# 		post_message = post['message']
# 	elif 'story' in post.keys():
# 		post_message = post['story']
# 	else:
# 		post_message = 'No content'
# 	post_id = post['id']
# 	post_created = post['created_time']
# 	container.append((post_message, post_created, post_created))

# conn = sqlite3.connect('fb_posts.sqlite')
# cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS Posts')

# p = 'CREATE TABLE IF NOT EXISTS Posts'
# p += 'Posts (message_text TEXT, created_time TIMESTAMP, post_id INTEGER PRIMARY KEY TEXT)'
# cur.execute(p)

# p = 'INSERT INTO Posts VALUES (?, ?, ?)'
# for i in posts_list:
#     cur.execute(p, i)

# conn.commit()




