import json
import requests
import facebook


post_cache = open('profile_Lauren.json','r')
data = post_cache.read()
response_post_list = json.loads(data) #data from text file in a dictionary
post_cache.close()
print (response_post_list)