import sqlite3
import requests
import json

# 1 - Make a connection to a new database fb_posts
conn = sqlite3.connect('fb_posts.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Posts')

p = 'CREATE TABLE IF NOT EXISTS Posts'
p += 'Posts (message PRIMARY KEY TEXT, created_time TIMESTAMP, post_id INTEGER PRIMARY KEY TEXT)'

cur.execute(p)

container = []

all_fields = [
'message',
'created_time',
'id'
]
all_fields = ','.join(all_fields)
posts = graph.get_connections('me','posts',fields=all_fields)

while True: #this is what allows for the paging, this one is paging through posts
	try:
		with open('my_posts1.json','a') as i:
			for post in posts['data']:
				container.append(post)
				i.write(json.dumps(post)+'\n') #next page
				#print (post) prints out all posts I've ever posted
			posts = requests.get(posts['paging']['next']).json()
	except KeyError: #there are no more pages to go through
		break

#print (container)

p = 'INSERT INTO Posts VALUES (?, ?, ?)'
for i in container:
    cur.execute(p, i)

conn.commit()
