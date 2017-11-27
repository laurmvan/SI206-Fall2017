import requests
import facebook

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAJbrrMKR1UoOEVYiDFAWaileZCVJaswjddbn68UzUdeZBqcEpZCTO2XMCpEHc9a46epZCu5UXCXNeRui9riWFjqV7ZCmBrmzwoRHDyKwaaZCLdsE2l95WcSoUgcDkl84WGUuQA7JAgXZCFKHbqOqGfTsPZApkAMwxnqaMbx6d5YRoc74PchajBj15o1khJ6y8gZDZD", version="2.10")

my_feed = graph.get_connections("me", "feed") #variable for my personal feed
my_feed = my_feed['data']
print (my_feed)

user = graph.get_object("me") #this represents my own name and id number for my account


friends = graph.get_connections(user["id"], "friends") #lists my friends and count of my friends. It is a dictionary with keys 'data' ('data' is a list'), 'paging' ('paging' is a dict), and 'summary' ('summary' is a dict)

friends2 = graph.get_object("me/friends")
for friend in friends2['data']:
    print ("{0} has id {1}".format(friend['name'].encode('utf-8'), friend['id']))


print (type(friends))

#this part below allows you to insert any user's name and get their facebook posts
user = 'BillGates'
profile = graph.get_object('me') #this can get a user
posts2 = graph.get_connections(profile['id'], 'posts')

allfriends = []

# Wrap this block in a while loop so we can keep paginating requests until
# finished.
while(True):
    try:
        for friend in friends['data']:
            allfriends.append(friend['name'].encode('utf-8'))
            # Attempt to make a request to the next page of data, if it exists.
        friends2=requests.get(friends['paging']['next']).json()
        print (friends2)
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break
print (allfriends)

# for item in friends['data']:
# 	print (item)

# print (friends['summary'])
# print

# places = graph.search(type='place',
#                       center='42.2808,83.7430', #lat and longetude
#                       fields='name,location')

# # Each given id maps to an object the contains the requested fields.
# for place in places['data']:
#     print('%s %s' % (place['name'].encode(),place['location'].get('zip')))

# friends2 = graph.get_connections(id='me', connection_name='friends')

# print (friends2)