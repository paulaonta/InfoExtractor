import csv

wiki_directory = "./errors_link_wikipedia.csv"

def is_repeted(text, i):
    mycsv_wikidata = csv.reader(open(wiki_directory))
    j = 0
    for line in mycsv_wikidata:
        if j <= i:
            j += 1
        else:
            text2 = line[1]
            if text2 == text:
                return True
    return False

#open csv files
mycsv_wikipedia = csv.reader(open(wiki_directory))

rows = []
first = True
i = 0
for line in mycsv_wikipedia:
    if first:
        first = False
        rows.append(line)
    else:
        link = line[1]
        if not is_repeted(link,i): #remove all repeted diseases
            rows.append(line)
    i += 1

file = open(wiki_directory, 'w')
writer = csv.writer(file)
writer.writerows(rows)