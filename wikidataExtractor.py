from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML, CSV
import os
import numpy
import csv
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)

languages = ['en']#, 'es', 'eu', 'ca', 'fr']

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

def getValues(first_row, array):
    lista = []
    lista.append(array[0][0])
    for j in range(1, len(first_row)):
        aux = numpy.unique(array[j])
        string = ",".join(aux)
        lista.append(string.replace(';', ','))
    return lista

sparql = SPARQLWrapper("https://query.wikidata.org/")

# create file for log
file = 'errors_log'
errorFile = './' + file
if not os.path.exists(errorFile):
    os.makedirs(os.path.dirname(errorFile), exist_ok=True)


try:
    sparql_query = ''' SELECT ?item2 ?item2Label
        WHERE
        {
        ?item (wdt:P279*) wd:Q12136. # subclass of
        ?item2 (wdt:P31) ?item. # instance of
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
        }'''
    res = return_sparql_query_results(sparql_query)
    first_row, prop = convertDictToArray(res)

    sparql_query = ''' SELECT ?item2 ?itemLabel 
        WHERE
        {
       { ?item (wdt:P279*) wd:Q9190427. }# subclass of animals diseases}
        UNION
        { ?item (wdt:P279*) wd:Q2662845.} #plants diseases
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
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
        }'''
    res = return_sparql_query_results(sparql_query)
    first_row, prop1 = convertDictToArray(res)

    #remove the elements in array1 that there are in array
    for elem in prop1[0]:
        if elem in prop[0]:
            prop[0].remove(elem)

    wdt = [elem.split("http://www.wikidata.org/entity/")[1] for elem in prop[0]]

except:
    print("error")

for lang in languages:
    first = True
    # create csv file for each language
    folder = 'diseases_info_' + lang + '.csv'
    mydirname = './' + folder
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

    # open the csv file
    myFile = open(mydirname, 'w')
    writer = csv.writer(myFile)
    i, errorCount = 0, 0
    lista2 = []
    while i < len(wdt):
        prop_num = wdt[i]
        try:
            sparql_query = ''' SELECT DISTINCT ?diseaseLabel ?symptomsLabel ?treatmentLabel ?differentFromLabel ?riskLabel
             ?causeLabel ?diagnosisLabel ?icd9 ?icd10 ?umls ?mesh 
             WHERE {
                ?disease wdt:* wd:''' + prop_num + '''.
              OPTIONAL { ?disease wdt:P780 ?symptoms. }
              OPTIONAL { ?disease wdt:P2176 ?treatment. }
              OPTIONAL { ?disease wdt:P1889 ?differentFrom. }
              OPTIONAL { ?disease wdt:P5642 ?risk. }
              OPTIONAL { ?disease wdt:P828 ?cause. }
              OPTIONAL { ?disease wdt:P923 ?diagnosis. }
              OPTIONAL { ?disease wdt:P1692 ?icd9. }
              OPTIONAL { ?disease wdt:P4229 ?icd10. }
              OPTIONAL { ?disease wdt:P2892 ?umls. }
              OPTIONAL { ?disease wdt:P486 ?mesh. }
              SERVICE wikibase:label { bd:serviceParam wikibase:language "''' + lang + '''". }
            }
            '''
            res = return_sparql_query_results(sparql_query)
            first_row, array = convertDictToArray(res)
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
            if errorCount == 5:
                #append in the logger
                myFile = open(errorFile, 'a')
                myFile.write("This disease: \"" +prop[1][i] + "\"" + " (" + prop_num + ") can't be load\n")
                errorCount = 0
                i += 1
            print("error")
            pass

    writer.writerows(lista2)

