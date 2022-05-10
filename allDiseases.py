from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML,CSV
from pprint import pprint
import os
import numpy
import csv
import pandas as pd
from csv import reader
from csv import writer

#create csv file
folder = 'diseases_info.csv'
mydirname = './' + folder
if not os.path.exists(mydirname):
    os.makedirs(os.path.dirname(mydirname), exist_ok=True)

sparql = SPARQLWrapper("http://dbpedia.org/sparql/")
array = []
try:
    sparql.setQuery('''SELECT DISTINCT ?disease ?symptoms ?causes ?diagnosis ?icd9 ?icd10 ?disDB ?meshID ?mlp ?omim ?emed 
    WHERE {
         ?disease a <http://dbpedia.org/ontology/Disease>.
         ?disease rdf:type <http://www.wikidata.org/entity/Q12136>.
         OPTIONAL { ?disease dbp:symptoms ?symptoms.  }
         OPTIONAL { ?disease dbp:causes ?causes. }
         OPTIONAL { ?disease dbo:medicalDiagnosis ?diagnosis.}
         OPTIONAL { ?disease dbo:icd9 ?icd9. }
         OPTIONAL { ?disease dbo:icd10 ?icd10. }
         OPTIONAL { ?disease dbo:diseasesDb ?disDB. }
         OPTIONAL { ?disease dbp:meshId ?meshID. }
         OPTIONAL { ?disease dbo:medlineplus ?mlp. }
         OPTIONAL { ?disease dbo:omim ?omim. }
         OPTIONAL { ?disease dbp:emedicinetopic ?emed. }
    }''')

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    select_term = ""
    i = 0
    first_row = []
    for result in results["head"]["vars"]:
        select_term = result
        array.insert(i, [])
        #this is the first row of the csv file
        first_row.append(result)
        for r in results["results"]["bindings"]:
            try:
                string1 = r[select_term]["value"]
                array[i].append(string1)
            except:
                pass
        i += 1
except:
    pass

#get unique values of diseases
uniqueValues, indicesLists = numpy.unique(array[0], return_index=True)
zipped_pairs = zip(indicesLists, uniqueValues)
z = [x for _, x in sorted(zipped_pairs)]

#get only the name of the diseases
lista = [[(elem.split('http://dbpedia.org/resource/')[1]).replace("_", " ")] for elem in z]
indicesList = ([elem for elem in indicesLists])
indicesList.sort()

#open the csv file
myFile = open(mydirname, 'w')
writer = csv.writer(myFile)

#inset values in the csv file
#first, insert the first row
writer.writerow(first_row)

#insert diseases -> there are in uniqueValues array
#writer.writerows(lista)

#get other values
for j in range(1, len(first_row)):
    for i in range(0, len(indicesList)-1):
        l = array[j][indicesList[i]:indicesList[i+1]]
        lagUV = numpy.unique(l)
        string = ",".join(lagUV)
        lista[i].append(string.replace(';',','))
    #LAST. when i =len(indices)-1
    i += 1
    l = array[j][indicesList[i]:]
    lagUV = numpy.unique(l)
    string = ",".join(lagUV)
    lista[i].append(string.replace(';', ','))

writer.writerows(lista)
