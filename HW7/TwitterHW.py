# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # still need this in the same directory, filled out

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# And we've provided the setup for your cache. But we haven't written any functions for you, so you have to be sure that any function that gets data from the internet relies on caching.
CACHE_FNAME = "twitter_cache.json"
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

## [PART 1]

# Here, define a function called get_tweets that searches for all tweets referring to or by "umsi"
# Your function must cache data it retrieves and rely on a cache file!


def get_tweets(key): #get UMSI related tweets
    formatted_key = "twitter_{}".format(key)
    response_list = []
    if formatted_key in CACHE_DICTION:
        print ('caching') #to indicate when using cache
        response_list = CACHE_DICTION[formatted_key]
        for i in range(5):
            print ("TEXT:" ,CACHE_DICTION[formatted_key]['statuses'][i]['text'])

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
        for tweet in input_tweets:
            response_list.append(tweet)
        CACHE_DICTION[formatted_key]=response_list #creating a response list

    return (response_list)

##YOUR CODE HERE

umsi_related_tweets = get_tweets('umsi')

## [PART 2]
# Create a database: tweets.sqlite,
# And then load all of those tweets you got from Twitter into a database table called Tweets, with the following columns in each row:
## tweet_id - containing the unique id that belongs to each tweet
## author - containing the screen name of the user who posted the tweet (note that even for RT'd tweets, it will be the person whose timeline it is)
## time_posted - containing the date/time value that represents when the tweet was posted (note that this should be a TIMESTAMP column data type!)
## tweet_text - containing the text that goes with that tweet
## retweets - containing the number that represents how many times the tweet has been retweeted

# Below we have provided interim outline suggestions for what to do, sequentially, in comments.

# 1 - Make a connection to a new database tweets.sqlite, and create a variable to hold the database cursor.
conn = sqlite3.connect('tweets.sqlite')
cur = conn.cursor()

# 2 - Write code to drop the Tweets table if it exists, and create the table (so you can run the program over and over), with the correct (4) column names and appropriate types for each.
# HINT: Remember that the time_posted column should be the TIMESTAMP data type!
cur.execute('DROP TABLE IF EXISTS Tweets')

p = 'CREATE TABLE IF NOT EXISTS '
p += 'Tweets (tweet_id INTEGER PRIMARY KEY, author TEXT, time_posted TIMESTAMP, tweet_text TEXT, retweets INTEGER)'
cur.execute(p)

# 3 - Invoke the function you defined above to get a list that represents a bunch of tweets from the UMSI timeline. Save those tweets in a variable called umsi_tweets.
umsi_tweets = get_tweets('umsi')

# 4 - Use a for loop, the cursor you defined above to execute INSERT statements, that insert the data from each of the tweets in umsi_tweets into the correct columns in each row of the Tweets database table.
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

#  5- Use the database connection to commit the changes to the database

conn.commit()

# You can check out whether it worked in the SQLite browser! (And with the tests.)

## [PART 3] - SQL statements
# Select all of the tweets (the full rows/tuples of information) from umsi_tweets and display the date and message of each tweet in the form:
    # Mon Oct 09 16:02:03 +0000 2017 - #MondayMotivation https://t.co/vLbZpH390b
    #
    # Mon Oct 09 15:45:45 +0000 2017 - RT @MikeRothCom: Beautiful morning at @UMich - It’s easy to forget to
    # take in the view while running from place to place @umichDLHS  @umich…
# Include the blank line between each tweet.


# Select the author of all of the tweets (the full rows/tuples of information) that have been retweeted MORE
# than 2 times, and fetch them into the variable more_than_2_rts.
# Print the results
umsi_tweets = get_user_tweets('umsi')


if __name__ == "__main__":
    unittest.main(verbosity=2)
