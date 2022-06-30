from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML, CSV
import os
import numpy
import csv
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
from definitions import define
from definitions import main_query

def getUniqueValuesIndices(array):
    # get unique values of diseases
    uniqueValues, indicesLists = numpy.unique(array, return_index=True)
    zipped_pairs = zip(indicesLists, uniqueValues)
    z = [x for _, x in sorted(zipped_pairs)]

    # get only the name of the diseases
    lista = [[elem] for elem in z]
    indicesList = ([elem for elem in indicesLists])
    indicesList.sort()

    return z, lista, indicesList

def getOtherValues(first_row, indicesList, array, lista):
    for j in range(1, len(first_row)):
        i = -1
        for i in range(0, len(indicesList) - 1):
            l = array[j][indicesList[i]:indicesList[i + 1]]
            lagUV = numpy.unique(l)
            string = ",".join(lagUV)
            lista[i].append(string.replace(';', ','))
        # LAST. when i = len(indices)-1
        i += 1
        l = array[j][indicesList[i]:]
        lagUV = numpy.unique(l)
        string = ",".join(lagUV)
        lista[i].append(string.replace(';', ','))

    return lista


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

def createFile(path):
    mydirname = './' + path
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)


languages, sparql_query_prop, sparql_query_prop_del, codes = define()
sparql = SPARQLWrapper("https://query.wikidata.org/")

#get properties
prop_code, prop = getProperties()
#for each language get info
for lang in languages:
    csv_path ='diseases_info_' + lang + '.csv'
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

    #for each property
    while i < len(prop_code):
        prop_num = prop_code[i] #get the property
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
                #append in the logger
                myErrorFile = open(errors_path, 'a')
                myErrorFile.write("This disease: \"" + prop[1][i] + "\"" + " (" + prop_num + ") can't be load\n")
                errorCount = 0
                i += 1
            print("error")
            pass

    writer.writerows(lista2)

