from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML, CSV
import os
import numpy
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
from urllib.request import urlopen
import bs4
import csv
from definitions import define4, define, main_query

languages, sparql_query_prop, sparql_query_prop_del, codes = define()
languages, link_first_part, link_second_part, wikipediaErrorsFile_path, errorsFile_path = define4()

sparql = SPARQLWrapper("https://query.wikidata.org/")

mycsv = csv.reader(open(wikipediaErrorsFile_path)) #open

myFile = open(errorsFile_path, 'a')
myErrorFile = csv.writer(myFile)
myErrorFile.writerow(['name', 'link'])

first = True

def convertDictToArray(res):
    select_term = ""
    i = 0
    first_row = []
    array = []
    for result in res["head"]["vars"]:
        select_term = result
        array.insert(i, [])
        # this is the first row of the csv file
        first_row.append(result)
        for r in res["results"]["bindings"]:
            try:
                string1 = r[select_term]["value"]
                array[i].append(string1)
            except:
                array[i].append(" ")
                pass
        i += 1

    return first_row, array

def getValues(first_row, array):
    lista = []
    lista.append(array[0][0])
    for j in range(1, len(first_row)):
        if first_row[j] in codes:
            unique_values = numpy.unique(array[j])
            if ' ' not in unique_values:
                aux = [elem.split("http://www.wikidata.org/entity/")[1] for elem in unique_values]
            else:
                aux = unique_values
        else:
            aux = numpy.unique(array[j])
        string = ",".join(aux)
        lista.append(string.replace(';', ','))
    return lista

def makeQuery(query):
    res = return_sparql_query_results(query)
    first_row, prop = convertDictToArray(res)
    return first_row, prop

def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

def getDisease(prop_code):
    for lang in languages:
        csv_path = 'diseases_info_' + lang + '.csv'
        errors_path = 'errors_log_' + lang
        first = True
        i, errorCount = 0, 0
        lista2 = []

        # create csv file for each language
        createFile(csv_path)
        # create file to save the errors for each language
        createFile(errors_path)

        # open the csv file
        myFile = open(csv_path, 'w')
        writer = csv.writer(myFile)

        # for each property
        while i < len(prop_code):
            prop_num = prop_code[i]  # get the property
            try:
                sparql_query_main = main_query(prop_num, lang)
                first_row, array = makeQuery(sparql_query_main)

                if first:
                    lista2.append(first_row)
                    first = False
                errorCount = 0
                i += 1
                if array[0]:  # if it is not empty
                    lista = getValues(first_row, array)
                    lista2.append(lista)
            except:
                errorCount += 1
                if errorCount == 10:
                    # append in the logger
                    myErrorFile = open(errors_path, 'a')
                    myErrorFile.write("This disease: " + prop_num + " can't be load\n")
                    errorCount = 0
                    i += 1
                print("error")
                pass

        writer.writerows(lista2)

#iterate the csv file
prop_code = []
for line in mycsv:
    if first:
        first = False
    else:
        name_parts = line[0].split(" ")
        index = 0
        link_disease_part = ""
        while index < len(name_parts):
            if index == len(name_parts)-1:
                link_disease_part += name_parts[index]
            else:
                link_disease_part += name_parts[index] + "+"
            index += 1

        link = link_first_part + link_disease_part[0:len(link_disease_part)] + link_second_part

        try:
            # open the link
            soup = bs4.BeautifulSoup(urlopen(link), features="lxml")
            # find tags by CSS class
            content = soup.find("ul", class_="mw-search-results").find_all('a')[0]
            code = content.getText().split('(')[1].split(')')[0]
            prop_code.append(code)

        except:
            print("error: an error occurs while searching the disease")
            # append in the logger
            myFile = open(errorsFile_path, 'a')
            myErrorFile = csv.writer(myFile)
            myErrorFile.writerow([line[0], line[1]])
            pass
getDisease(prop_code)