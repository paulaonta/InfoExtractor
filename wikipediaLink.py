import csv
from urllib.request import urlopen
import bs4

alphabetical_list = ['0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
partial_link = "https://en.wikipedia.org/wiki/List_of_diseases_"
i, errorCount = 0, 0

while i < len(alphabetical_list):
    alpha = alphabetical_list[i]
    link = partial_link + "(" + alpha + ")"

    try:
        # open the link
        soup = bs4.BeautifulSoup(urlopen(link), features="lxml")
        # find tags by CSS class
        rows = soup.find_all("span", class_="toctext")
        errorCount = 0
        i += 1

        #for row in rows:
        for row in rows:
            print(row.next_element)
    except:
        errorCount += 1
        if errorCount == 5:
            print("error: an error occurs while opening the link")
            errorCount = 0
            i += 1
        pass