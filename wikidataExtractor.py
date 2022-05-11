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

sparql = SPARQLWrapper("https://query.wikidata.org/")
try:
    sparql_query = ''' SELECT ?disease  
                 WHERE{
                  ?disease wdt:P31 wd:Q12136.
                  }'''
    res = return_sparql_query_results(sparql_query)
    first_row, array = convertDictToArray(res)
except:
    print("error")

wdt = [elem.split("http://www.wikidata.org/entity/")[1] for elem in array[0]]

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

    for prop in wdt:
        try:
            sparql_query = ''' SELECT DISTINCT ?diseaseLabel ?symptomsLabel ?treatmentLabel ?differentFromLabel ?riskLabel
             ?causeLabel ?diagnosisLabel ?icd9 ?icd10 ?umls ?mesh 
             WHERE {
                ?disease wdt:P31 wd:''' + prop + '''.
         
              OPTIONAL { ?disease wdt:P923 ?diagnosis. }
              OPTIONAL { ?disease wdt:P1692 ?icd9. }
              OPTIONAL { ?disease wdt:P4229 ?icd10. }
              OPTIONAL { ?disease wdt:P2892 ?umls. }
              OPTIONAL { ?disease wdt:P486 ?mesh. }
              SERVICE wikibase:label { bd:serviceParam wikibase:language "''' + lang + '''". }
            }
            ORDER BY (?disease)'''

            res = return_sparql_query_results(sparql_query)
            first_row, array = convertDictToArray(res)
        except:
            print("error")
            pass
        if array[0]:
            # get diseases values
            uniqueValues, lista, indicesList = getUniqueValuesIndices(array[0])
            # get other values
            lista = getOtherValues(first_row, indicesList, array, lista)

            if first:
                # insert in the csv
                writer.writerow(first_row)
                first = False
                uniqueValues2 = uniqueValues.copy()
                lista2 = lista.copy()
            else:
                # insert the others values
                # we have two list to merge: lista and lista2
                for elem in uniqueValues:
                    if elem in uniqueValues2:  # append the values
                        pos = uniqueValues.index(elem)
                        lista2.append(lista[pos])

    writer.writerows(lista2)

