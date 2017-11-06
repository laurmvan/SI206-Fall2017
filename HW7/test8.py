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
CACHE_FNAME = "HW7_cache_9.json"
try:
	cache_file = open(CACHE_FNAME,'r') #check to see if there is an existing file as CACHE_FNAME
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
	response_list = []
	if formatted_key in CACHE_DICTION:
		print ('caching') #to indicate when using cache
		response_list = CACHE_DICTION[formatted_key]
		for i in range(5):
			print ("TEXT:" ,CACHE_DICTION[formatted_key]['statuses'][i]['text'])
			print ("CREATED AT: ",CACHE_DICTION[formatted_key]['statuses'][i]['created_at'],'\n') #formated output
		# for i in range(5): #printing out text and created at date if info is cached
		# 	print ('TEXT: ', CACHE_DICTION[formatted_key][int(i)]['text'])
		# 	print ('CREATED AT: ', CACHE_DICTION[formatted_key][int(i)]['created_at'],'\n')
	else:
		print ('fetching') #to indicate when going to the web to fetch new data
		response_list = []
		formatted_key = "twitter_{}".format(key)
		input_tweets = api.search(q = key, count = 5) #just to get 5 tweets
		CACHE_DICTION[formatted_key] = input_tweets
		cache_file = open(CACHE_FNAME, 'w', encoding = 'utf-8') #to help with any potential encoding errors when writing the file
		cache_file.write(json.dumps(CACHE_DICTION)) #creating the cache file
		cache_file.close()
		save_list = []
		for i in range(5): #printing out text and created at date if needs to fetch
			print ('TEXT: ' ,input_tweets['statuses'][i]['text']) #formatted output
			print ('CREATED AT: ', input_tweets['statuses'][i]['created_at'],'\n')
		for tweet in input_tweets:
			response_list.append(tweet)
		CACHE_DICTION[formatted_key]=response_list #creating a response list


	return (response_list)


user_input = input('Enter a term: ')
formatted_key = "twitter_{}".format(user_input)
input_tweets = api.search(q = user_input, count = 5)

while user_input != "": #continues to take user input until no text is entered
	get_user_tweets(user_input)
	formatted_key = "twitter_{}".format(user_input)
	input_tweets = api.search(q = user_input, count = 5)
	user_input = input('Enter a term: ')









