import requests

from bs4 import BeautifulSoup

titles_list= []
names_list= []

umsi_titles= {}

for i in range(13):
	base_url= 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All'
	url= base_url + '&page=%s' % str(i)
	r= requests.get(url, headers={'User-Agent': 'SI_CLASS'})
	soup= BeautifulSoup(r.text, "html.parser")
	tags= soup.find_all('div', {'class': "field field-name-title field-type-ds field-label-hidden"})
	for tag in tags: 
		names_list.append(tag.text)

	tags2= soup.find_all('div', {'class': 'field field-name-field-person-titles field-type-text field-label-hidden'})
	for tag2 in tags2:
		titles_list.append(tag2.text)

diction= zip(names_list, titles_list)
umsi_titles= dict(diction)
print (umsi_titles)