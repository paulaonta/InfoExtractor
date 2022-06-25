from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML, CSV
import os
import numpy
import csv
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
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

query = '''SELECT ?item2 ?itemLabel 
                WHERE
                { ?item (wdt:P279*) wd:Q8294850. #physiological plant disorders 
                ?item2 (wdt:P31) ?item. # instance of }'''

languages, sparql_query_prop, sparql_query_prop_del, codes = define()
sparql = SPARQLWrapper("https://query.wikidata.org/")


first_row, prop = makeQuery(sparql_query_prop)
first_row, prop1 = makeQuery(sparql_query_prop_del)
print(str(len(prop[1])))
print(str(len(prop1[1])))

#remove the elements in prop1 that there are in prop
for elem in prop1[0]:
    if elem in prop[0]:
        prop[0].remove(elem)
print(str(len(prop[0])))
print(str(len(prop[1]) - len(prop1[1])))
final_prop_code = [elem.split("http://www.wikidata.org/entity/")[1] for elem in prop[0]]