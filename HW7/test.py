# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # still need this in the same directory, filled out

## Make sure to comment with:
# Your name: Jonathan Bain
# The names of any people you worked with for this assignment:

# ******** #
### Useful resources for this HW:
## cached_tweepy_example.py
## HW5
## https://books.trinket.io/pfe/14-database.html and database examples from class
## Lecture 17 notes, Lecture 18 notes
# ******** #

## Instructions for this assignment can be found in this file, along with some provided structure and some provided code.

## There are 3 parts to this assignment, each of which is described below.

## There are tests for each part, but the tests are NOT exhaustive, because you may each have different tweets, etc. Make sure you check the data you get -- print it out, check the types, look in the database browser, try out your SQL queries!

## We have provided setup code for you to use Tweepy, like we did for HW5 and Project 2:

# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# And we've provided the setup for your cache. But we haven't written any functions for you, so you have to be sure that any function that gets data from the internet relies on caching, just like in Project 2.
CACHE_FNAME = "HW7_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

## [PART 1]

# Here, define a function called get_user_tweets that accepts a specific Twitter user handle (e.g. "umsi" or "umich" or "Lin_Manuel" or "ColleenAtUMSI") and returns data that represents at least 20 tweets from that user's timeline.

# Your function must cache data it retrieves and rely on a cache file!
# Note that this is a lot like work you have done already in class (but, depending upon what you did previously, may not be EXACTLY the same, so be careful your code does exactly what you want here).

def get_user_tweets(key):
	formatted_key = "twitter_{}".format(key)
	if formatted_key in CACHE_DICTION:
		response_list = CACHE_DICTION[formatted_key]
	else:
		response =  api.user_timeline(key)
		CACHE_DICTION[formatted_key] = response
		cache_file = open(CACHE_FNAME, 'w', encoding = 'utf-8')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
		response_list = []
		for r in response:
			response_list.append(r)
	print (response_list[0]['text'])

	return response_list


# Write code to create/build a connection to a database: tweets.db,
# And then load all of those tweets you got from Twitter into a database table called Tweets, with the following columns in each row:

## tweet_id - containing the unique id that belongs to each tweet
## author - containing the screen name of the user who posted the tweet (note that even for RT'd tweets, it will be the person whose timeline it is)
## time_posted - containing the date/time value that represents when the tweet was posted (note that this should be a TIMESTAMP column data type!)
## tweet_text - containing the text that goes with that tweet
## retweets - containing the number that represents how many times the tweet has been retweeted

# Below we have provided interim outline suggestions for what to do, sequentially, in comments.

# Make a connection to a new database tweets.db, and create a variable to hold the database cursor.

conn = sqlite3.connect('tweets.db')
cur = conn.cursor()
# Write code to drop the Tweets table if it exists, and create the table (so you can run the program over and over), with the correct (4) column names and appropriate types for each.
# HINT: Remember that the time_posted column should be the TIMESTAMP data type!
cur.execute('DROP TABLE IF EXISTS Tweets')

p = 'CREATE TABLE IF NOT EXISTS '
p += 'Tweets (tweet_id INTEGER PRIMARY KEY, author TEXT, time_posted TIMESTAMP, tweet_text TEXT, retweets INTEGER)'
cur.execute(p)

# Invoke the function you defined above to get a list that represents a bunch of tweets from the UMSI timeline. Save those tweets in a variable called umsi_tweets.
umsi_tweets = get_user_tweets('umsi')

# Use a for loop, the cursor you defined above to execute INSERT statements, that insert the data from each of the tweets in umsi_tweets into the correct columns in each row of the Tweets database table.

# (You should do nested data investigation on the umsi_tweets value to figure out how to pull out the data correctly!)
container = []

for i in range(20):
	id_item = umsi_tweets[i]["id"]
	user_item = umsi_tweets[i]["user"]["screen_name"]
	created_at_item = umsi_tweets[i]["created_at"]
	text_item = umsi_tweets[i]["text"]
	retweet_item = umsi_tweets[i]["retweet_count"]
	container.append((id_item, user_item, created_at_item, text_item, retweet_item))

p = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'
for i in container:
	cur.execute(p, i)

# Use the database connection to commit the changes to the database

# You can check out whether it worked in the SQLite browser! (And with the tests.)

conn.commit()



# Finally, done with database stuff for a bit: write a line of code to close the cursor to the database.

conn.close()


def get_twitter_users(t):
	return set(re.findall("@([0-9A-Z_a-z]+)", t))

