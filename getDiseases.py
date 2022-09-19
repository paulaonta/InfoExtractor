from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML, CSV
import os
import numpy
import csv
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)

path = "./compareDiseases/errors_link_wikipedia.csv"
diseases_link_pos = 1
codes = ["disease", "symptoms", "treatment", "differentFrom", "risk", "cause", "diagnosis"]
languages = ['en', 'eu', 'ca', 'fr', 'es']

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

def makeQuery(query):
    res = return_sparql_query_results(query)
    first_row, prop = convertDictToArray(res)
    return first_row, prop

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


#open csv files
mycsv_wikipedia = csv.reader(open(path))

first = True
for line in mycsv_wikipedia:
    if first:
        first = False
    else:
        link = line[diseases_link_pos]
        i = 0
        while i < len(languages):
            errorCount = 0
            lang = languages[i]
            csv_path = './results/diseases_info_' + lang + '.csv'
            errors_path = './results/errors_log_' + lang

            # open the csv file
            myFile = open(csv_path, 'a')
            writer = csv.writer(myFile)

            query = '''SELECT DISTINCT ?item2Label ?item2 ?link 
                 WHERE {
                   ?item (wdt:P279*) wd:Q112193867. # subclass of
                    ?item2 (wdt:P31) ?item. # instance of     
                 OPTIONAL {
                  ?link schema:about ?item2 .
                  ?link schema:inLanguage "en".
                   ?link schema:isPartOf <https://en.wikipedia.org/> .
                  }
                  
                    FILTER (STR(?link)="'''+ link + '''")
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "'''+lang+'''". }
                }       
            '''
            try:
                first_row, array = makeQuery(query)
                errorCount = 0
                i += 1
                if array[0]:  # if it is not empty
                    lista = getValues(first_row, array)
                    writer.writerow(lista)

            except:
                errorCount += 1
                if errorCount == 10:
                    # append in the logger
                    myErrorFile = open(errors_path, 'a')
                    myErrorFile.write("This disease: \"" + line[0] +" can't be load\n")
                    errorCount = 0
                print("error")
                pass


