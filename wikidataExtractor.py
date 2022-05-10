from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML,CSV
import os
import numpy
import csv
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)

languages = ['en', 'es', 'eu', 'ca', 'fr']
wdt = [ 'P31', 'P279']
array1, array2 = [],[]

def convertDictToArray(res):
    select_term = ""
    i = 0
    first_row = []
    array  = []
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


for lang in languages:
    #create csv file for each language
    folder = 'diseases_info_' + lang + '.csv'
    mydirname = './' + folder
    if not os.path.exists(mydirname):
        os.makedirs(os.path.dirname(mydirname), exist_ok=True)

    sparql = SPARQLWrapper("https://query.wikidata.org/")

    try:
        sparql_query = ''' SELECT DISTINCT ?diseaseLabel ?symptomsLabel ?treatmentLabel ?differentFromLabel ?riskLabel 
         WHERE {
            ?disease wdt:P31 ?m. 
            ?m wdt:P279 wd:Q12136.
          OPTIONAL { ?disease wdt:P780 ?symptoms. }
          OPTIONAL {?disease wdt:P2176 ?treatment.}
          OPTIONAL {?disease wdt:P1889 ?differentFrom.}
          OPTIONAL { ?disease wdt:P5642 ?risk.}
          SERVICE wikibase:label { bd:serviceParam wikibase:language "''' + lang + '''". }
        }
        ORDER BY (?disease)'''
        res = return_sparql_query_results(sparql_query)
        first_row, array = convertDictToArray(res)

        sparql_query2 = ''' SELECT DISTINCT ?diseaseLabel ?causeLabel ?diagnosisLabel ?icd9 ?icd10 ?umls ?mesh 
         WHERE {
            ?disease wdt:P31 ?m. 
            ?m wdt:P279 wd:Q12136.
          OPTIONAL { ?disease wdt:P828 ?cause. }
          OPTIONAL { ?disease wdt:P923 ?diagnosis. }
          OPTIONAL { ?disease wdt:P1692 ?icd9. }
          OPTIONAL { ?disease wdt:P4229 ?icd10. }
          OPTIONAL { ?disease wdt:P2892 ?umls. }
          OPTIONAL { ?disease wdt:P486 ?mesh. }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "''' + lang + '''". }
        }
        ORDER BY (?disease)'''
        res2 = return_sparql_query_results(sparql_query2)
        first_row2, array2 = convertDictToArray(res2)

        #get diseases values
        uniqueValues, lista, indicesList = getUniqueValuesIndices(array[0])
        uniqueValues2, lista2, indicesList2 = getUniqueValuesIndices(array2[0])

        #get other values
        lista = getOtherValues(first_row, indicesList, array, lista)
        lista2 = getOtherValues(first_row2, indicesList2, array2, lista2)

        # open the csv file
        myFile = open(mydirname, 'w')
        writer = csv.writer(myFile)

        # inset values in the csv file. We need to merge values
        # first, insert the first row
        for i in range(1, len(first_row)): #merge first_row and first_row2
            first_row2.append(first_row[i])

        #insert in the csv
        writer.writerow(first_row2)

        #insert the others values
        #we have two list to merge: lista and lista2
        j = 0
        for elem in uniqueValues2:
            if elem in uniqueValues:#append the values of the new columns
                pos = uniqueValues.index(elem)
                for i in range(1, len(first_row)):
                    lista2[j].append(lista[pos][i])
            else:
                lista2[j].append(" ")
            j += 1

        writer.writerows(lista2)

    except:
        print("error")