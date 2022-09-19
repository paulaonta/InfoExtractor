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

def remove_properties(prop1):
    mycsv_wikidata = csv.reader(open("./emaitza/diseases_info_en.csv"))
    first = True
    prop = [elem.split("http://www.wikidata.org/entity/")[1] for elem in prop1[0]]

    for line in mycsv_wikidata:
        if first:
            first = False
        else:
            code = line[1]
            if code in prop:
                prop.remove(code)
    return prop

def getValues(first_row, array):
    lista = []
    lista.append(array[0][0])
    for j in range(1, len(first_row)):
        if first_row[j] in codes:
            unique_values = numpy.unique(array[j])
            print(unique_values)
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
                           UNION
                           {?item (wdt:P279*) wd:Q3281225.}
                           UNION
                           {?item (wdt:P279*) wd:Q44512.}
                           UNION
                           { ?item (wdt:P279*) wd:Q9190427. }# subclass of animals diseases
                            UNION
                            { ?item (wdt:P279*) wd:Q2662845.} #plants diseases
                            UNION
                            { ?item (wdt:P279*) wd:Q8294850.} #physiological plant disorders 
                               UNION
                            { ?item (wdt:P279*) wd:Q98379923.} #aspect in a geographic region
                               UNION
                            { ?item (wdt:P279*) wd:Q216866.} #siames
                              UNION
                            { ?item (wdt:P279*) wd:Q44512.} #epidemic
                              UNION
                            { ?item (wdt:P279*) wd:Q178059.} #paraphilia
                             UNION
                            { ?item (wdt:P279*) wd:Q191355.}  #hunger strike
                              UNION
                            { ?item (wdt:P279*) wd:Q4215775.} #metal poisoning
                              UNION
                            { ?item (wdt:P279*) wd:Q114953.} #poisoning
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
                           UNION
                           {?item (wdt:P279*) wd:Q3281225.}
                           UNION
                           {?item (wdt:P279*) wd:Q44512.}
                           UNION
                           { ?item (wdt:P279*) wd:Q9190427. }# subclass of animals diseases
                            UNION
                            { ?item (wdt:P279*) wd:Q2662845.} #plants diseases
                            UNION
                            { ?item (wdt:P279*) wd:Q8294850.} #physiological plant disorders 
                               UNION
                            { ?item (wdt:P279*) wd:Q98379923.} #aspect in a geographic region
                               UNION
                            { ?item (wdt:P279*) wd:Q216866.} #siames
                              UNION
                            { ?item (wdt:P279*) wd:Q44512.} #epidemic
                              UNION
                            { ?item (wdt:P279*) wd:Q178059.} #paraphilia
                             UNION
                            { ?item (wdt:P279*) wd:Q191355.}  #hunger strike
                              UNION
                            { ?item (wdt:P279*) wd:Q4215775.} #metal poisoning
                              UNION
                            { ?item (wdt:P279*) wd:Q114953.} #poisoning
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
print(str(len(prop[0])))

final_prop_code = remove_properties(prop)
print(str(len(final_prop_code)))

for lang in languages:
    csv_path ='./results/diseases_info_' + lang + '.csv'
    errors_path = './results/errors_log_' + lang
    first = True
    i, errorCount = 0, 0
    lista2 = []

    # open the csv file
    myFile = open(csv_path, 'w')
    writer = csv.writer(myFile)
    rows = []
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
                rows.append(lista)
        except:
            errorCount += 1
            if errorCount == 10:
                #append in the logger
                myErrorFile = open(errors_path, 'a')
                myErrorFile.write("This disease: \"" + prop[1][i] + "\"" + " (" + prop_num + ") can't be load\n")
                errorCount = 0
                i += 1
            print("error")
            pass
    print("amaitu")

    writer.writerows(rows)

