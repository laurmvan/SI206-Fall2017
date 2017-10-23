
import requests

from bs4 import BeautifulSoup


umsi_titles={}
page_count=0
umsi_titles={}
base_url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All&page='+str(page_count)

i=0
x=0
while i<13:
    result=requests.get(base_url, headers={'User-Agent': 'SI_CLASS'})
    soup=BeautifulSoup(result.content, 'html.parser')
    directory=soup(class_='views-row')
    for person in directory:
        for count in range(1):
            #name=title.find_all(class_='dc:title')
            title=soup(class_='field-name-field-person-titles')
            name=(soup('h2'))[count]
            name=name.text
            
            title=(title[count].text)
            umsi_titles[name]=title

    
    pager=soup(class_='pager-next')
    for page in pager:
        href=page('a')
        for link in href:
            link=link.get('href', None)
            if len(link)>0:
                base_url='https://www.si.umich.edu'+link

    i+=1

print (umsi_titles)