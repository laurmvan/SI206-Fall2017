import requests
import facebook

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAB5YnMuZBQ1jf33cGgViG4XAGNjvOFRXcFXoyggvc0MFzZBMjmvo2KtDBQB0scQiHJyiIVHN7KBeVxrKjjhyYAf8VZAhzButWOLLPomUPdnYFKchKPobpmMm3dPmfzhmZCGHfBPUrypPAPlZBzVOvBzyLm91miZBVI8cejVaEE59eHu6YUGNIZD", version="2.10")

my_feed = graph.get_connections("me", "feed") #variable for my personal feed
my_feed = my_feed['data']
print (my_feed)

user = graph.get_object("me") #this represents my own name and id number for my account

post = graph.search(type='user')

friends = graph.get_connections(user["id"], "friends") #lists my friends and count of my friends. It is a dictionary with keys 'data' ('data' is a list'), 'paging' ('paging' is a dict), and 'summary' ('summary' is a dict)

print (type(friends))

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