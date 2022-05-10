from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML,CSV
from pprint import pprint
import os
import numpy
import csv
from csv import reader
from csv import writer

diseases = ["Rheumatoid_arthritis",
"Cirrhosis",
"Alcoholic_liver_disease",
"Hepatitis_B",
"Hepatitis_C",
"Non-alcoholic_steatohepatitis",
"Streptococcal_pharyngitis",
"Infectious_mononucleosis"]

languages = ['en','es','ca','eus','fr']

#create csv file
folder = 'diseases_info2.csv'
mydirname = './' + folder
if not os.path.exists(mydirname):
    os.makedirs(os.path.dirname(mydirname), exist_ok=True)

first = True
first_row = []
for dis in diseases:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql/")
    array = []

    sparql.setQuery('''SELECT DISTINCT ?symptoms ?causes  ?icd9 ?icd10 ?meshId ?diagnosis
    WHERE {
    OPTIONAL{ dbr:''' + dis + ''' dbp:symptoms  ?symptoms . }
    OPTIONAL{ dbr:''' + dis + ''' dbp:causes  ?causes . }
    OPTIONAL{ dbr:''' + dis + ''' dbo:icd10  ?icd10 . }
    OPTIONAL{ dbr:''' + dis + ''' dbo:icd9  ?icd9 . }
    OPTIONAL{ dbr:''' + dis + ''' dbo:meshId  ?meshId. }
    OPTIONAL{ dbr:''' + dis + ''' dbo:medicalDiagnosis  ?diagnosis. }
    }''')

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    select_term = ""
    i = 0
    for result in results["head"]["vars"]:
        select_term = result
        array.insert(i, [])
        #this is the first row of the csv file
        if first:
            first_row.append(result)
        for r in results["results"]["bindings"]:
            try:
                string1 = r[select_term]["value"]
                array[i].append(string1)
            except:
                pass
        i += 1

    if first:
        #open the csv file
        myFile = open(mydirname, 'w')
        writer = csv.writer(myFile)

        #inset values in the csv file
        #first, insert the first row
        first_row.insert(0, 'disease')
        writer.writerow(first_row)

    #get other values
    row = []
    row.append(dis)
    for i in range(len(first_row)-1):
        lagUV = numpy.unique(array[i])
        string = ",".join(lagUV)
        row.append(string)
    writer.writerow(row)

    first = False