InfoExtractor
=======

**InfoExtractor** is a tool which extracts the differents diseases of Wikidata in 5 different languages (English, Spanish, Basque, Catalan, Italian).  

For each language and disease we store in a .csv file the following (in orden): disease name, disease code, symptoms, symptom codes, treatments, treatment codes, 'different from' property values and their codes, risks, risk codes, causes, cause codes, different diagnosis, different diagnosis codes, ICD-9, ICD-10, UMLS, MESH, NCI, Wikipedia Link, the description and the different names of the disease.
In the English language we also have the symptoms obtained using the NCI code.

Below is a brief description of each file:

definitions.py
-----------
Contains the functions that are uses more than ones in different files. Also contains the values of global variables.


wikidataExtractor.py 
-----------
Extracts for each language all the data of Wikidata.  
The data is store in **'results'** folder. There you will find for each language:  
1. **disease_info_language.csv**: all the data in 'language' language
	- **disease_info_en_nci.csv**: all the data in english + the symptoms obtained using the NCI co
2. **errors_log_language**: the diseases that couldn't be loaded in 'language' language     


append2.py 
-----------
Extracts for each language all the data of Wikidata that is missing doing a query that gets more diseases than the first (the query that was done in the file above) 


NCI_ID.py
-----------
For each disease gets the symptoms using the NCI code.  
_**WARNING!!!**_ Make a copy of mydirname BEFORE running, the copy will be the data in english and the other will be the data + the symptoms obtained using the NCI code


wikipediaLink.py
-----------
Gets a list with all the names of the diseases that are in the Wikipedia  
The data is store in **'WikipediaLinks'** folder. There you will find for each letter:  
- **Wikipedia_links_letter.csv**: we have all the diseases which start with 'letter'. We have in the .csv file, in order, the following: disease name, wikipedia link, if the link is redirected or not and if it's redirected the redirect link and otherwise, the wikipedia link.
		
		
removeLinks.py
-----------
Removes the repeted links that are in WikipediaLinks.
	
		
compareDiseases.py
-----------
Compares the list of all the diseases that are in the Wikipedia with the diseases of Wikidata.  
The result is store in **"./compareDiseases/errors_link_wikipedia.csv"**. Here we have for each disease of the list the ones which are **NOT** in Wikidata
	

getDiseases.py 
-----------
Tries to get the diseases which are not in Wikidata (the diseases of ./compareDiseases/errors_link_wikipedia.csv" directory) making a query in which the link is used as a filter.


remove.py 
-----------
After analysing the data this file removes diseases.


append.py
-----------
Tries to get the diseases which are not in Wikidata (the diseases of ./compareDiseases/errors_link_wikipedia.csv" directory) simulating a search of the link in the Wikidata browser.

---

In the **trash folder** are files that have not been deleted just in case
