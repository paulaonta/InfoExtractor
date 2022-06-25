# -*- coding: utf-8 -*-
import wptools
import wikipedia as wiki
import os
import requests
from urllib.request import urlopen
import bs4


diseases = ["rheumatoid arthritis", 
"Cirrhosis",
"Alcoholic liver disease",
"Hepatitis B",
"Hepatitis C",
"Non-alcoholic steatohepatitis",
"Streptococcal pharyngitis",
"infectious mononucleosis"]

languages = ['en','es','ca','fr','eu']


# attributes of interest contained within the wiki infoboxes
features = [['symptoms','diagnosis','differential','causes'],['síntomas','a causa de','causas','diagnóstico', 'diferencial'],['símptomes','diagnosi','Tractament','Causa de','Causat per'],['Symptômes','Diagnostic','difféntiel','Causes'],[]]

boxterm = ['box', 'Ficha', 'Infotaula','Taxobox','infobox']

def get_infobox(page_title, langu, index):
    page = wptools.page(page_title, lang = langu, boxterm=boxterm[index]) # create a page object
    try:
        page.get_parse() # call the API and parse the data
        if langu == 'ca' and page_title == 'Artritis reumatoide':
            print(page.data.get('parsetree'))
        if page.data['infobox'] != None:
            # if infobox is present
            infobox = page.data['infobox']
            # get data for the interested features/attributes
            data = { feature : infobox[feature] if feature in infobox else ' ' 
                         for feature in features[index] }
        else:
            data = { feature : '' for feature in features[index] }
        return data  
    
    except KeyError:
        pass

folder = 'diseases_info'
mydirname = './' + folder
if not os.path.exists(mydirname):
    os.makedirs(os.path.dirname(mydirname), exist_ok=True)

for d in diseases:
    #create a file for each disease
    file = mydirname + '/'+d
    if not os.path.exists(file):
        os.makedirs(os.path.dirname(file), exist_ok=True)
    page_title = d
    index = 0
    try:
        while index <= len(languages)-1:
            language = languages[index]
            if language != 'en':
                # URL
                URL = wiki.page(d).url

                # sending the request
                response = requests.get(URL)

                # parsing the response
                #getting the link in the language
                soup = bs4.BeautifulSoup(response.text, features = "lxml")
                link = soup.find('a', hreflang = language).get('href')
                #open the link
                soup1 = bs4.BeautifulSoup(urlopen(link), features = "lxml")

                # getting title
                page_title = soup1.find('h1', id = 'firstHeading').next_element

            data = get_infobox(page_title, language, index)
            index += 1
            with open(file, 'a') as f:
                for key, value in data.items():
                    f.write('%s:%s\n' % (key, value))

    except AttributeError:
        pass

   