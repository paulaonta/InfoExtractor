import csv
from definitions import define3

mydirname, wiki_directory, wikiD_link_pos, wikiP_link_pos, also_pos, errors_pathD, errors_pathP = define3()
first = True
myErrorFile = open(errors_pathD, 'w')
writerD = csv.writer(myErrorFile)
writerD.writerow(['name', 'code', 'link'])

myErrorFile = open(errors_pathP, 'a')
writerP = csv.writer(myErrorFile)
writerP.writerow(['name', 'link'])

def contains_disease(text,name, directory):
    rows = []
    first = True
    contains = False
    mycsv_wikipedia = csv.reader(open(directory))
    for line in mycsv_wikipedia:
        if first:
            first = False
            if len(line) == 4:
                line.insert(wikiP_link_pos+1, "Is it in wikidata?")
            rows.append(line)
        else:
            link = line[wikiP_link_pos]
            name_wiki = line[0]

            if str(text) == link or name == name_wiki:
                if len(line) == 4:
                    line.insert(wikiP_link_pos+1, "Yes")
                    contains = True

            rows.append(line)

    mydir = open(directory, 'w')
    writer = csv.writer(mydir)
    writer.writerows(rows)
    return contains

def also_known_diseases():
    mycsv = csv.reader(open(wiki_directory))  # open
    first = True
    rows = [ ]
    # iterate the csv file
    for line in mycsv:
        first2 = True
        if len(line) == 4:
            text = ""
        else:
            text = line[wikiP_link_pos + 1]

        if first:
            first = False
            rows.append(line)
        elif text != 'Yes':
            mycsv_wikidata = csv.reader(open(mydirname))  # open

            for line2 in mycsv_wikidata:
                if first2:
                    first2 = False
                else:
                    also_known = line2[also_pos] #get the name
                    also_known_diseases = [elem.title() for elem in also_known.split(" , ")]
                    if len(text) != 1:
                        if line[0].title() == "Acne vulgaris":
                            print(also_known_diseases)
                        if not line[0].title() in also_known_diseases:
                            # append in the error file
                            writerD.writerow([line2[0],line2[1],line2[wikiD_link_pos]])
                        else:
                            line.insert(wikiP_link_pos + 1, "Yes")
            rows.append(line)
    mydir = open(wiki_directory, 'w')
    writer = csv.writer(mydir)
    writer.writerows(rows)

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
mycsv_wikidata = csv.reader(open(mydirname))

for line in mycsv_wikidata:
    if first:
        first = False
    else:
        text = line[wikiD_link_pos]  # get the link
        name = line[0] #get the name
        if len(text) != 1:
            if not contains_disease(text, name, wiki_directory):
                # append in the error file
                writerD.writerow([line[0],line[1],text])

also_known_diseases()
#get diseases which are in wikipedia but not in wikidata
get_wikipedia_diseases()

