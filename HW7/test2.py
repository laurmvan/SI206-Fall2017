import unittest
import tweepy
import requests
import json
import twitter_info

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
public_tweets = api.home_timeline() 

user_input = input('Enter tweet term: ')

for tweet in public_tweets:
	if user_input in tweet['text']:
		print ("TEXT: " , tweet['text'])
		print ("CREATED AT: " , tweet['created_at'],'\n')

