def define():
    languages = ['es', 'eu', 'ca', 'fr', 'en']

    sparql_query_prop = ''' SELECT ?item2 ?item2Label
                WHERE
                {
                ?item (wdt:P279*) wd:Q12136. # subclass of
                ?item2 (wdt:P31) ?item. # instance of     
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
                }'''

    sparql_query_prop_del = ''' SELECT ?item2 ?itemLabel 
                WHERE
                {
               { ?item (wdt:P279*) wd:Q9190427. }# subclass of animals diseases
                UNION
                { ?item (wdt:P279*) wd:Q2662845.} #plants diseases
                UNION
                { ?item (wdt:P279*) wd:Q8294850.} #physiological plant disorders 
                   UNION
                { ?item (wdt:P279*) wd:Q98379923.} #aspect in a geographic region
                   UNION
                { ?item (wdt:P279*) wd:Q216866.} #siames
                  UNION
                { ?item (wdt:P279*) wd:Q44512.} #epidemic
                  UNION
                { ?item (wdt:P279*) wd:Q178059.} #paraphilia
                 UNION
                { ?item (wdt:P279*) wd:Q191355.}  #hunger strike
                  UNION
                { ?item (wdt:P279*) wd:Q4215775.} #metal poisoning
                  UNION
                { ?item (wdt:P279*) wd:Q114953.} #poisoning

                ?item2 (wdt:P31) ?item. # instance of
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
                }'''
    codes = ["disease", "symptoms", "treatment", "differentFrom" , "risk" , "cause", "diagnosis"]
    return languages, sparql_query_prop, sparql_query_prop_del, codes

def main_query(prop_num, lang):
    return  '''SELECT DISTINCT ?diseaseLabel ?disease ?symptomsLabel ?symptoms ?treatmentLabel ?treatment 
            ?differentFromLabel ?differentFrom ?riskLabel ?risk ?causeLabel ?cause  ?diagnosisLabel ?diagnosis
            ?icd9 ?icd10 ?umls ?mesh ?nci ?link ?description ?alsoKnownAs
             WHERE {
                ?disease wdt:* wd:''' + prop_num + '''.
              OPTIONAL { ?disease wdt:P780 ?symptoms. }
              OPTIONAL { ?disease wdt:P2176 ?treatment. }
              OPTIONAL { ?disease wdt:P1889 ?differentFrom. }
              OPTIONAL { ?disease wdt:P5642 ?risk. }
              OPTIONAL { ?disease wdt:P828 ?cause. }
              OPTIONAL { ?disease wdt:P923 ?diagnosis. }
              OPTIONAL { ?disease wdt:P1692 ?icd9. }
              OPTIONAL { ?disease wdt:P4229 ?icd10. }
              OPTIONAL { ?disease wdt:P2892 ?umls. }
              OPTIONAL { ?disease wdt:P486 ?mesh. }
              OPTIONAL { ?disease wdt:P1748 ?nci. } 
              OPTIONAL {
              ?link schema:about ?disease .
              ?link schema:inLanguage "''' + lang + '''".
              ?link schema:isPartOf <https://''' + lang + '''.wikipedia.org/> .
              }
              OPTIONAL{
              ?disease schema:description ?description. 
              FILTER(LANG(?description) = "''' + lang + '''")
              }
              OPTIONAL{
              ?disease skos:altLabel ?alsoKnownAs. 
              FILTER(LANG(?alsoKnownAs) = "''' + lang + '''")
              }
                SERVICE wikibase:label { bd:serviceParam wikibase:language "''' + lang + '''". }
            }           
            '''

def define2():
    folder = 'diseases_info_en.csv'
    mydirname = './' + folder

    nci_pos = 18
    symptom_pos = 2
    nci_link_first_part = "https://ncit.nci.nih.gov/ncitbrowser/pages/concept_details.jsf?dictionary=NCI_Thesaurus&version=22.05e&code="
    nci_link_second_part = "&ns=ncit&type=relationship&key=null&b=1&n=0&vse=null"

    return mydirname, nci_pos, symptom_pos, nci_link_first_part, nci_link_second_part

def define3():
    folder = 'diseases_info_en.csv'
    mydirname = './emaitza/' + folder
    wiki_directory = "./wikipediaLinks/wikipedia_links_all.csv"
    wikiD_link_pos = 19
    wikiP_link_pos = 3
    also_pos = 21
    errors_path = 'errors_link_wikipedia.csv'

    return mydirname, wiki_directory, wikiD_link_pos, wikiP_link_pos, also_pos,errors_path

def define4():
    languages = ['en', 'es', 'eu', 'fr', 'ca']

    link_first_part = "https://www.wikidata.org/w/index.php?search="
    link_second_part  = "+-article+-trial&title=Special:Search&profile=advanced&fulltext=1&advancedSearch-current={\"fields\"%3A{\"not\"%3A[\"article\"%2C\"trial\"]}}&ns0=1&ns120=1"
    wikipediaErrorsFile_path = "./compareDiseases/errors_link_wikipedia.csv"
    errorsFile_path = "./errors_link_wikipedia_def.csv"

    return languages, link_first_part, link_second_part, wikipediaErrorsFile_path, errorsFile_path



