import requests
import json
import tweepy 			# need to pip install tweepy
import twitter_info		# you need to initialize this file with your Tweet app info

# Fill these in in the twitter_info.py file
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

public_tweets = api.home_timeline() # One possible method! Check out: http://tweepy.readthedocs.io/en/v3.5.0/api.html#timeline-methods 
print(type(public_tweets)," is the type of publictweets")

for tweet in public_tweets:
    print("\n*** type of the tweet object that is included ***\n")
    print(type(tweet),"type of one tweet") 
    print(tweet) ## Huh. That's not easy to read.

# Let's pull apart one tweet to take a look at it.
single_tweet = public_tweets[0]

## What are the tags?
print("\n*** tags of the tweet dictionary ***")
print(single_tweet.keys())

## Well, some of these look interesting.
## For example,
print("\nHere's the text of the tweet:")
print(single_tweet["text"])
print("\n")
print("Here are the # of favorites of that tweet:")
print(single_tweet["favorite_count"])

## Taking a look at the keys, try printing some other attributes of the tweet!

## But what if I don't want just my own public timeline's tweets -- I want to search for a certain phrase on Twitter!
print("********\n\n\n*******")
results = api.search(q="university of michigan")
print(type(results), "is the type of the results variable") 

## OK, it's a dictionary. What are its keys?
print(results.keys())

## That 'statuses' key looks interesting.
print(type(results["statuses"]), "is the type of results['statuses']")
## OK, that's a list! Hmm. What's the type of the first element in it?
print(type(results["statuses"][0]), "is the type of the first element in the results")
## OK, that's a dictionary. What are its keys? I have a suspicion they'll be the same as the Tweet dictionary I saw before...
## I'm gonna assign that one tweet to a variable to make it easier.
umich_tweet = results["statuses"][0]
## Now, what are its keys?
print("\nThe keys of the tweet dictionary:")
print(umich_tweet.keys())

## And the list of tweets is in results["statuses"]..
list_of_umich_tweets = results["statuses"]

## Iterate over the tweets you get back...
## And print the text of each one!
for tweet in list_of_umich_tweets:
    print(tweet["text"])
    print("\n")

## Note that there are a bunch of options in the search you can try -- to get more tweets, etc. But for now, look at how much you can access with the basics.

## Here's code to update a status -- uncomment below lines if you fill them in to post something to Twitter
# stat_text = "" # A string for what you want to be posted on your twitter account
# ## Uncomment the following line to post a new status
# api.update_status(stat_text)