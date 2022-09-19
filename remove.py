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
        csv_path = './results/diseases_info_en_nci.csv'
    else:
        csv_path = './results/diseases_info_' + lang + '.csv'
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
                           UNION
                            {?item (wdt:P279*) wd:Q31208391.} 
                            UNION
                            {?item (wdt:P279*) wd:Q133780.} 
                             UNION
                            {?item (wdt:P279*) wd:Q3241045.} 
                            UNION
                            {?item (wdt:P279*) wd:Q223393.} 
                           ?item2 (wdt:P31) ?item. # instance of
                        }'''
first_row, prop = makeQuery(sparql_query)
final_prop_code = [elem.split("http://www.wikidata.org/entity/")[1] for elem in prop[0]]
#we want to delete the diseases with this codes because there aren't human diseases
codes = ['Q102322953', 'Q17450153', 'Q7002141',  'Q2662861',  'Q26842138',  'Q2040895',  'Q3049298',  'Q749342',  'Q30912812' , \
 'Q109270553', 'Q109353029',  'Q2597715',  'Q96414735',  'Q1553361',  'Q97184013' , 'Q738101',  'Q89498598',  'Q66424263', \
 'Q4684101',  'Q66424104',  'Q1329680',  'Q207066',  'Q1092510',  'Q1759544',  'Q7822519',  'Q492728',  'Q24628669', \
 'Q1758551',  'Q5467519',  'Q1799748',  'Q41808675',  'Q75393351',  'Q43405',  'Q5142432',  'Q5750929',  'Q315940',  \
 'Q29310572',  'Q57620918',  'Q7263711',  'Q20917015',  'Q7272353',  'Q15761553',  'Q7272353']
final_prop_code.extend(codes)

for lang in languages:
    rows = []
    if lang == 'nci':
        csv_path = './results/diseases_info_en_nci.csv'
    else:
        csv_path ='./results/diseases_info_' + lang + '.csv'
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
                    if text not in final_prop_code: #remove the diseases which codes are in the query we had done before
                        rows.append(line)

    mydir = open(csv_path, 'w')
    writer = csv.writer(mydir)
    writer.writerows(rows)