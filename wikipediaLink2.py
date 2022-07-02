import csv
import wptools
import wikipedia as wiki
import os
import requests
from urllib.request import urlopen
import bs4

def createFile(path):
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

def createDirectory(path):
    if not os.path.exists(path):
        os.mkdir(path)


alphabetical_list = ['0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                    'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

partial_link = "https://en.wikipedia.org/wiki/List_of_diseases_"
next = False
i, errorCount = 0, 0

wiki_directory = "./wikipediaLinks"
createDirectory(wiki_directory)

while i < len(alphabetical_list):
    alpha = alphabetical_list[i]
    link = partial_link + "(" + alpha + ")"

    #create a file to save all links for each letter
    folder = 'wikipedia_links_' + alpha +'.csv'
    mydirname = wiki_directory + "/" + folder
    createFile(mydirname)

    # open the csv file
    myFile = open(mydirname, 'w')
    writer = csv.writer(myFile)

    writer.writerow(['Name', 'Wikipedia link (en)', 'Redirected', 'Redirect link'])

    try:
        # open the link
        soup = bs4.BeautifulSoup(urlopen(link), features="lxml")
        # find tags by CSS class
        if soup.find("span", class_="toctext") is not None:
            content = soup.find("span", class_="toctext").getText()
        else:
            content = alpha

        errorCount = 0
        i += 1
        span = soup.find_all("span", id=content)

        for s in span:
            li = s.find_all_next("li")
            for elem in li:
                if "li" in str(elem):
                    link_tag = elem.find_next('a')
                    name = link_tag.text
                    link = link_tag.get('href')

                    if "class=\"mw-redirect\"" in str(link_tag):
                        redirect = "Yes"

                        # get the link of the redirect page
                        soup1 = bs4.BeautifulSoup(urlopen("https://en.wikipedia.org" + link), features="lxml")
                        redirect_link = soup1.find('link', rel="canonical").get('href')
                    else:
                        redirect = "No"
                        redirect_link = "https://en.wikipedia.org" + link #the redirect link is the same of the web link

                    if "/wiki" in link and name != "Lists of diseases" and name != "edit" : #if we have a disease
                        row = [name, "https://en.wikipedia.org" + link, redirect, redirect_link]
                        writer.writerow(row)

    except:
        errorCount += 1
        if errorCount == 5:
            print("error: an error occurs while opening the link")
            errorCount = 0
            i += 1
        pass