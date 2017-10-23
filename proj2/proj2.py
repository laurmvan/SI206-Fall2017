
## SI 206 W17 - Project 2

## COMMENT HERE WITH:
## Your name:
## Anyone you worked with on this project:

## Below we have provided import statements, comments to separate out the 
#parts of the project, instructions/hints/examples, and at the end, TESTS.

###########

## Import statements
import unittest
import requests
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl

# Ignore SSL certificate errors



## Part 1 -- Define your find_urls function here.
## INPUT: any string
## RETURN VALUE: a list of strings that represents all of the URLs in the input string


## For example: 
## find_urls("http://www.google.com is a great site") should return ["http://www.google.com"]
## find_urls("I love looking at websites like http://etsy.com and http://instagram.com and stuff") should return ["http://etsy.com","http://instagram.com"]
## find_urls("the internet is awesome #worldwideweb") should return [], empty list




## PART 2  - Define a function grab_headlines.
## INPUT: N/A. No input.
## Grab the headlines from the "Most Read" section of 
## http://www.michigandaily.com/section/opinion
def grab_headlines():
    base_url = 'https://www.michigandaily.com/section/opinion'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "lxml")
    return_list = []
 
    for most_read in soup.find_all(class_="pane-mostread"): 
        for title in most_read.find_all('a'):
            return_list.append(title.text)

    return return_list
    



## PART 3 (a) Define a function called get_umsi_data.  It should create a dictionary
## saved in a variable umsi_titles whose keys are UMSI people's names, and whose 
## associated values are those people's titles, e.g. "PhD student" or "Associate 
## Professor of Information"...
## Start with this page: https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All  
## End with this page: https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All&page=12 
## INPUT: N/A. No input.
## OUTPUT: Return umsi_titles
## Reminder: you'll need to use the special header for a request to the UMSI site, like so:
## requests.get(base_url, headers={'User-Agent': 'SI_CLASS'}) 

def get_umsi_data():
    pass
    #Your code here

## PART 3 (b) Define a function called num_students.  
## INPUT: The dictionary from get_umsi_data().
## OUTPUT: Return number of PhD students in the data.  (Don't forget, I may change the input data)
def num_students(data):
    pass
    #Your code here



########### TESTS; DO NOT CHANGE ANY CODE BELOW THIS LINE! ###########
def test(got, expected, pts):
    score = 0;
    if got == expected:
        score = pts
        print(" OK ",end=" ")
    else:
        print (" XX ", end=" ")
    print("Got: ",got, "Expected: ",expected)

    return score


def main():
    total = 0


    print('\n\nTask 2: Michigan Daily')
    total += test(grab_headlines(), ['Students attempt to shut down speech by controversial social scientist Charles Murray ', 'Orion Sang: Michigan should see what it has with Peters', "Protesters grapple with Charles Murray's appearance on campus", "'Lil Pump' delivers hype despite a lack of substance", "'Jane the Virgin' becomes Adam the Virgo in season 4 shift"],50)
   

if __name__ == '__main__':
    main()