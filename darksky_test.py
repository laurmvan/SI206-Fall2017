import requests
import json
from datetime import datetime


base_url = 'https://api.darksky.net/forecast/'
api_key = '13c846e2deb97661c79a55ca57c287dd'
lat_lng = '42.280841,-83.738115'
full_url = base_url+api_key+'/'+lat_lng

response = requests.get(full_url)
data = json.loads(response.text)
#print(json.dumps(data, indent=4))
data2 = (data['hourly']['data'])
for item in data2:
	print ((datetime.fromtimestamp(item['time'])), (item['summary']), (item['temperature']))