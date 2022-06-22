import csv
from urllib.request import urlopen
import bs4


# Function to convert
def listToString(s):
   # initialize an empty string
   str1 = ""
   count = 0
   # traverse in the string
   while count < len(s):
      if count == len(s)-1:
         str1 += s[count]
      else:
         str1 += s[count] + ","
      count += 1

   # return string
   return str1

folder = 'diseases_info_en.csv'
mydirname = './' + folder
first = True
nci_pos = 11
symptom_pos = 1
nci_link_first_part = "https://ncit.nci.nih.gov/ncitbrowser/pages/concept_details.jsf?dictionary=NCI_Thesaurus&version=22.05e&code="
nci_link_second_part = "&ns=ncit&type=relationship&key=null&b=1&n=0&vse=null"

mycsv = csv.reader(open(mydirname))
csv_array = []

for line in mycsv:
   i, errorCount = 0, 0
   if first:
      first = False
   else:
      text = line[nci_pos] #get the NCI ID
      if len(text) != 0 and len(text) != 1: #if we have the id
         code_array = text.split(",")
         while i < len(code_array):
            code = code_array[i]
            # complete the link
            nci_link = nci_link_first_part + code + nci_link_second_part
            try:
               # open the link
               soup = bs4.BeautifulSoup(urlopen(nci_link), features="lxml")
               # find tags by CSS class
               rows = soup.find_all("td", class_="dataCellText")

               errorCount = 0
               i += 1
               next = False

               for row in rows:
                  if next: #if TRUE--> get the symptoms
                     next = False

                     #get symptoms
                     text_symptoms = line[symptom_pos]

                     if len(text_symptoms) == 0 or len(text_symptoms) == 1 or text_symptoms == None: #the aren't symptoms
                        text_symptoms = []
                     else: #there are
                        text_symptoms = text_symptoms.split(",")

                     try:
                        new_symptoms = (row.find('a').next_element).split(",")
                     except:
                        print("error: row hasn't got next_element")
                        new_symptoms = " "
                        text_symptoms = []

                     #see which symptoms are not in the csv and then add
                     for symptom in new_symptoms:
                        if symptom not in text_symptoms: #if the isn't add
                           line.pop(symptom_pos)
                           text_symptoms.append(symptom)

                     line.insert(symptom_pos, listToString(text_symptoms))

                  elif 'Disease_May_Have_Finding' in row.getText() or 'Disease_Has_Finding' in row.get_text(): #row has the symptom
                     next = True

            except:
               errorCount += 1
               if errorCount == 5:
                  print("error: an error occurs while opening the link")
                  errorCount = 0
                  i += 1
               pass

   csv_array.append(line)

#insert the new symptoms in the csv
myFile = open(mydirname, 'w')
writer = csv.writer(myFile)
writer.writerows(csv_array)