import  csv
import wptools
import wikipedia as wiki
import os
import requests
from urllib.request import urlopen
import bs4
from definitions import define3

mydirname, wiki_directory, wikiD_link_pos, wikiP_link_pos, errors_pathD, errors_pathP =  define3()
first = True

def get_directory(letter):
    directory = wiki_directory + "/wikipedia_links_" + letter + ".csv"
    return directory

def contains_disease(text, directory):
    rows = []
    first = True
    contains = False
    mycsv_wikipedia = csv.reader(open(directory))
    for line in mycsv_wikipedia:
        if first:
            first = False
            if len(line) == 2:
                line.insert(wikiP_link_pos+1, "Is it in wikidata?")
            rows.append(line)
        else:
            link = line[wikiP_link_pos]
            soup = bs4.BeautifulSoup(link, features="lxml")
            url = soup.find('a').get('href')
            print(url)
            if str(text) == link and len(line) == 2:
                line.insert(wikiP_link_pos+1, "Yes")
                contains = True
            rows.append(line)

    mydir = open(directory, 'w')
    writer = csv.writer(mydir)
    writer.writerows(rows)
    return contains

def get_wikipedia_diseases():
    alphabetical_list = ['0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for alpha in alphabetical_list: #for each letter
        directory = get_directory(alpha) #get directory
        mycsv = csv.reader(open(directory)) #open
        first = True

        #iterate the csv file
        for line in mycsv:
            if len(line) == 2:
                text = ""
            else:
                text = line[wikiP_link_pos+1]
            if first:
                first = False
            elif text != 'Yes':
                # append in the error file
                myErrorFile = open(errors_pathP, 'a')
                myErrorFile.write("This disease: \"" + line[0] + " \" is not in wikidata\n")

#open csv files
mycsv_wikidata = csv.reader(open(mydirname))

for line in mycsv_wikidata:
    if first:
        first = False
    else:
        text = line[wikiD_link_pos]  # get the link

        if len(text) != 1:
            #get the first letter and open the conrespond file
            if '/wiki/' in text:
                text_split = text.split('/')
            else:
                text_split = text.split('?title=')
            letter = text_split[len(text_split)-1][0]
            if letter.isnumeric():
                letter = '0-9'
            mycsv_wikipedia_directory = get_directory(letter.title())

            if not contains_disease(text, mycsv_wikipedia_directory):
                # append in the error file
                myErrorFile = open(errors_pathD, 'a')
                myErrorFile.write("This disease: \"" + text +"\" is not in wikipedia\n")

#get diseases which are in wikipedia but not in wikidata
get_wikipedia_diseases()