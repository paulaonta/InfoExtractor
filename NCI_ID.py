import csv
from urllib.request import urlopen
import bs4
from definitions import define2

mydirname, nci_pos, symptom_pos, nci_link_first_part, nci_link_second_part = define2()
first = True

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

#open csv file
mycsv = csv.reader(open(mydirname))

csv_array = []
#for each line in the csv file
for line in mycsv:
   i, errorCount = 0, 0
   if first:
      first = False
      line.insert(symptom_pos+2, "symptomLabel_NCI")
   else:
      text = line[nci_pos] #get the NCI ID
      new_symptoms_array = [ ]
      if len(text) != 0 and len(text) != 1: #if we have the id
         code_array = text.split(",") #get the nci id codes
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

                     #get symptoms of the csv
                     text_symptoms = line[symptom_pos]

                     if len(text_symptoms) == 0 or len(text_symptoms) == 1 or text_symptoms == None: #the aren't symptoms
                        text_symptoms = []
                     else: #there are
                        text_symptoms = text_symptoms.split(",")

                     try:
                        new_symptoms = (row.find('a').next_element)
                     except:
                        print("error: row hasn't got next_element")
                        new_symptoms = " "
                        text_symptoms = []

                     #see which symptoms are not in the csv
                     new_symptoms_array = new_symptoms.split(",")
                     for symptom in new_symptoms_array:
                        if symptom  in text_symptoms: #if the is remove
                           new_symptoms_array.remove(symptom)

                  elif 'Disease_May_Have_Finding' in row.getText() or 'Disease_Has_Finding' in row.get_text(): #row has the symptom
                     next = True

            except:
               errorCount += 1
               if errorCount == 5:
                  print("error: an error occurs while opening the link")
                  errorCount = 0
                  i += 1
               pass
      line.insert(symptom_pos+2, listToString(new_symptoms_array))
   csv_array.append(line)

#insert the new symptoms in the csv
myFile = open(mydirname, 'w')
writer = csv.writer(myFile)
writer.writerows(csv_array)