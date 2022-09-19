from SPARQLWrapper import SPARQLWrapper, JSON, N3, XML, CSV
import os
import numpy
import csv


sparql = SPARQLWrapper("https://query.wikidata.org/")
languages = ['eu', 'ca', 'fr', 'es', 'nci']

def contains(text):
    first_ = True
    ref_path = './results/diseases_info_en.csv'
    ref_csv = csv.reader(open(ref_path))
    for ref_line in ref_csv:
        if first_:
            first_ = False
        else:
            ref_text = ref_line[1]
            if len(ref_text) != 1 and ref_text == text:
                return True
    return False

for lang in languages:
    rows = []
    if lang == 'nci':
        csv_path = './results/diseases_info_en_nci.csv'
    else:
        csv_path ='./results/diseases_info_' + lang + '.csv'
    mycsv_wikidata = csv.reader(open(csv_path))

    first = True
    for line in mycsv_wikidata:
        if first:
            first = False
            rows.append(line)
        else:
            text = line[1]
            if len(text) != 1:
                if contains(text): #if the code is in english csv
                    rows.append(line)

    mydir = open(csv_path, 'w')
    writer = csv.writer(mydir)
    writer.writerows(rows)