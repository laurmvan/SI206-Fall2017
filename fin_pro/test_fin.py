
import facebook
import requests

graph = facebook.GraphAPI(access_token="EAACEdEose0cBAB5YnMuZBQ1jf33cGgViG4XAGNjvOFRXcFXoyggvc0MFzZBMjmvo2KtDBQB0scQiHJyiIVHN7KBeVxrKjjhyYAf8VZAhzButWOLLPomUPdnYFKchKPobpmMm3dPmfzhmZCGHfBPUrypPAPlZBzVOvBzyLm91miZBVI8cejVaEE59eHu6YUGNIZD", version="2.10")

totalFriends = []
friends = graph.get_connections("me", "friends&summary=1")

while 'paging' in friends:
    for i in friends['data']:
        totalFriends.append(i['id'])
    friends = graph.get_connections("me", "friends&summary=1&after=" + friends['paging']['cursors']['after'])