from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML, CSV
import os
import numpy
import csv
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)

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

def is_repeted(text, i):
    if lang == 'nci':
        csv_path = './emaitza/diseases_info_en_nci.csv'
    else:
        csv_path = './emaitza/diseases_info_' + lang + '.csv'
    mycsv_wikidata = csv.reader(open(csv_path))
    j = 0
    for line in mycsv_wikidata:
        if j <= i:
            j += 1
        else:
            text2 = line[1]
            if text2 == text:
                return True
    return False


sparql = SPARQLWrapper("https://query.wikidata.org/")
languages = ['en', 'eu', 'ca', 'fr', 'es', 'nci']

sparql_query = ''' SELECT ?item2 ?itemLabel 
                        WHERE {                                    
                           { ?item (wdt:P279*) wd:Q65091757.}
                            UNION
                           { ?item (wdt:P279*) wd:Q8294850.}#physiological plant disorders 
                           UNION
                           { ?item (wdt:P279*) wd:Q9190427.} #animal diseases
                           UNION
                           {?item (wdt:P279*) wd:Q207791.} 
                           ?item2 (wdt:P31) ?item. # instance of
                        }'''
first_row, prop = makeQuery(sparql_query)
final_prop_code = [elem.split("http://www.wikidata.org/entity/")[1] for elem in prop[0]]
final_prop_code.append('Q102322953')
final_prop_code.append('Q17450153')
final_prop_code.append('Q2662861')
final_prop_code.append('Q2040895')
final_prop_code.append('Q3049298')
final_prop_code.append('Q30912812')
final_prop_code.append('Q109270553')


for lang in languages:
    rows = []
    if lang == 'nci':
        csv_path = './emaitza/diseases_info_en_nci.csv'
    else:
        csv_path ='./emaitza/diseases_info_' + lang + '.csv'
    mycsv_wikidata = csv.reader(open(csv_path))

    first = True
    i = 0
    for line in mycsv_wikidata:
        i += 1
        if first:
            first = False
            rows.append(line)
        else:
            text = line[1]
            if len(text) != 1:
                if not is_repeted(text,i): #remove all repeted diseases
                    if text not in final_prop_code: #remove the diseases with codes are in the query we had done before
                        rows.append(line)

    mydir = open(csv_path, 'w')
    writer = csv.writer(mydir)
    writer.writerows(rows)