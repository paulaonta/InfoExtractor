from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML, CSV
import os
import numpy
import csv
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
from definitions import main_query
from definitions import define

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

def getProperties():
    try:
        first_row, prop = makeQuery(sparql_query_prop)
        first_row, prop1 = makeQuery(sparql_query_prop_del)

        #remove the elements in prop1 that there are in prop
        for elem in prop1[0]:
            if elem in prop[0]:
                prop[0].remove(elem)

        final_prop_code = [elem.split("http://www.wikidata.org/entity/")[1] for elem in prop[0]]
        return final_prop_code, prop
    except:
        print("error")

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

languages, sparql_query_prop, sparql_query_prop_del, codes = define()
sparql = SPARQLWrapper("https://query.wikidata.org/")
languages = ['en', 'eu', 'ca', 'fr', 'es']

sparql_query = ''' SELECT ?item2 ?item2Label
                WHERE
                {
                ?item (wdt:P279*) wd:Q112193867. # subclass of
                ?item2 (wdt:P31) ?item. # instance of     
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
                }'''
first_row, prop = makeQuery(sparql_query)

sparql_query = ''' SELECT ?item2 ?itemLabel 
                        WHERE {                                    
                           { ?item (wdt:P279*) wd:Q65091757.}
                            UNION
                           { ?item (wdt:P279*) wd:Q8294850.}#physiological plant disorders 
                           UNION
                           { ?item (wdt:P279*) wd:Q9190427.} #animal diseases
                           UNION
                           {?item (wdt:P279*) wd:Q207791.} 
                           UNION
                           {?item (wdt:P279*) wd:Q98379923.}
                           ?item2 (wdt:P31) ?item. # instance of
                        }'''
first_row, prop1 = makeQuery(sparql_query)

#get properties
prop_code, prop2 = getProperties()

#remove the elements in prop1 that there are in prop
for elem in prop2[0]:
    if elem in prop[0] :
        prop[0] = [value for value in prop[0] if value != elem]

#remove the elements in prop1 that there are in prop
for elem in prop1[0]:
    if elem in prop[0] :
        prop[0] = [value for value in prop[0] if value != elem]

final_prop_code = [elem.split("http://www.wikidata.org/entity/")[1] for elem in prop[0]]

for lang in languages:
    csv_path ='./emaitza/diseases_info_' + lang + '.csv'
    errors_path = './emaitza/errors_log_' + lang
    first = True
    i, errorCount = 0, 0
    lista2 = []

    # open the csv file
    myFile = open(csv_path, 'a')
    writer = csv.writer(myFile)

    #for each property
    while i < len(final_prop_code):
        prop_num = final_prop_code[i] #get the property
        try:
            sparql_query_main = main_query(prop_num, lang)
            first_row, array = makeQuery(sparql_query_main)

            errorCount = 0
            i += 1
            if array[0]:  # if it is not empty
                lista = getValues(first_row, array)
                writer.writerow(lista)
        except:
            errorCount += 1
            if errorCount == 10:
                #append in the logger
                myErrorFile = open(errors_path, 'a')
                myErrorFile.write("This disease: \"" + prop[1][i] + "\"" + " (" + prop_num + ") can't be load\n")
                errorCount = 0
                i += 1
            #print("error")
            pass
    print("amaitu")

