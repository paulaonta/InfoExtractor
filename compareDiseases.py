import csv
from definitions import define3

mydirname, wiki_directory, wikiD_link_pos, wikiP_link_pos, also_pos, errors_path = define3()
first = True

myErrorFile = open(errors_path, 'a')
writerP = csv.writer(myErrorFile)
writerP.writerow(['name', 'link'])

def contains_disease(name_wiki, link):
    first = True
    contains = False
    mycsv_wikidata = csv.reader(open(mydirname))
    for line in mycsv_wikidata:
        if first:
            first = False
        else:
            text = line[wikiD_link_pos]
            name = line[0]
            if len(text) != 0:
                if str(text) == link or name.lower() == name_wiki.lower():
                    contains = True
                    break

    return contains

def also_known_diseases(name):
    first = True
    contains = False
    mycsv_wikidata = csv.reader(open(mydirname))
    # iterate the csv file
    for line in mycsv_wikidata:
        if first:
            first = False
        else:
            also_known = line[also_pos] #get the name
            also_known_diseases = [elem.lower().replace(" ", "") for elem in also_known.split(",")]
            if name.lower().replace(" ", "") in also_known_diseases:
                contains = True
                break

    return contains

def get_wikipedia_diseases():
    mycsv = csv.reader(open(wiki_directory)) #open
    first = True

    #iterate the csv file
    for line in mycsv:
        if len(line) == 4:
            text = ""
        else:
            text = line[wikiP_link_pos+1]

        if first:
            first = False
        elif text != 'Yes':
            # append in the error file
            writerP.writerow([line[0],line[wikiP_link_pos]])

#open csv files
mycsv_wikipedia = csv.reader(open(wiki_directory))

rows = []
for line in mycsv_wikipedia:
    if first:
        first = False
        line.insert(wikiP_link_pos + 1, "Is it in Wikidata?")
        rows.append(line)
    else:
        link = line[wikiP_link_pos]
        name_wiki = line[0]
        if contains_disease(name_wiki, link) or also_known_diseases(name_wiki):
            line.insert(wikiP_link_pos + 1, "Yes")
        rows.append(line)

file = open(wiki_directory, 'w')
writer = csv.writer(file)
writer.writerows(rows)

#get diseases which are in wikipedia but not in wikidata
get_wikipedia_diseases()

