# Import statements
import unittest
import sqlite3
import requests
import json
import re
import facebook


# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format
graph = facebook.GraphAPI(access_token="EAACEdEose0cBAKgCqOLL3OoH7M43mI4XLRBWZAG3P4ZC3gU4tJkQMw2XCmQSuI1Jm7MxCMhOFtk1r2xXxo0d369QPMUwXZC4zLPiKnWzm3gPec2arQnZABVPzhdKkmdSRdZBl1HYbz6jy7TuOA4zswKTyGkkgOGOmd56UNa1QI22JZAVP3nu7rZCsZBx3OJRm3akja31QxEsswZDZD", version="2.10")

posts = graph.get_connections('me', 'posts')

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

