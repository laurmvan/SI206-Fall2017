from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


url = input('Enter URL: ')
count2 = input('Enter count: ')
position = input('Enter position: ')
count2 = int(count2)
position = int(position)
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")
tags = soup('a')

count = 0
names_list = []


while (count < count2):
	names_list.append(soup.find_all('a')[17].get_text())
	url = soup.find_all('a')[position-1]["href"]
	print ("Retrieving: ", url)
	html = urlopen(url, context=ctx).read()
	soup = BeautifulSoup(html, "html.parser")
	tags = soup('a')
	count +=1

print (names_list)
length = int(len(names_list))
print ("The answer to the assignment for this execution is",(names_list[length-1]))
