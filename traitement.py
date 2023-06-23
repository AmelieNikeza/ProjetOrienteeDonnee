import spacy
import pandas as pd
import re
import urllib
import bs4
from bs4 import BeautifulSoup
import pandas
import requests
from urllib import request



# Charger le modèle linguistique
nlp = spacy.load("fr_core_news_sm")

nlp.max_length = 2848830
"""
data = pd.read_csv('dataBretagne.csv')
data.to_csv("data.txt", sep=',', index=False)
"""

def addData(links,linkDict ):
    sortedLinks=dict(sorted(links.items(), key=lambda x: x[1]))

    for key in sortedLinks.keys():
        for key2 in linkDict.keys():
            if key2 in key :
                linkDict[key2][key] = links[key]


    return linkDict

def filterData(dict ,maxOccur):
    for key, val in dict.items():
        for key2, val2 in val.items():
            if val2 < maxOccur:
                del dict[key][key2]

    return dict
           


with open("dataBretagne.txt", "r", encoding="utf-8") as file:
    text = file.read()

    # Appliquer le modèle sur le texte
    linKRegex = r"(http|https)://[^\s]+"
    doc = nlp(text)

    print("analyse du fichier...")
    
    # Ensemble des URL du projet + celle de ark.frantiq trouvée dans les données
    linkDict = {
                "http://bibliotheque-numerique-sra-bretagne.huma-num.fr/s/sra-bretagne/":{},
                "https://cidoc-crm.org/" : {},
                "https://vocabs.dariah.eu/":{},
                "http://www.geonames.org/":{},
                "https://www.catalogueoflife.org/":{},
                "https://ark.frantiq.fr/ark:/26678/":{}
            }
    orgs = {}
    people = {}
    links = {}
    linkList = []

    """
    for ent in doc.ents:
        if ent.label_ == "PER":  # Personne
            print("Nom de personne :", ent.text)
        elif ent.label_ == "ORG":  # Organisation
            print("Nom d'organisation :", ent.text)
    
    """
    for ent in doc.ents:
        
        if re.match(linKRegex,ent.text)  and ent.text not in links.keys():
            links[ent.text] = 1
            linkList.append(ent.text)
        elif re.match(linKRegex,ent.text)  and ent.text in links.keys():
            links[ent.text] = links[ent.text] + 1
            linkList.append(ent.text)
        elif ent.label_ == "PER" and ent.text not in people.keys():  # Personne
            people[ent.text] = 1 
        elif ent.label_ == "PER" and ent.text in people.keys():
            people[ent.text] = people[ent.text] +1
        elif ent.label_ == "ORG" and ent.text not in orgs.keys():  # Organisation
            orgs[ent.text] = 1
        elif ent.label_ == "ORG" and ent.text in orgs.keys():    
            orgs[ent.text] = orgs[ent.text] + 1
        

   # print(dict(sorted(orgs.items(), key=lambda x: x[1])))

   # print(dict(sorted(people.items(), key=lambda x: x[1])))
    """
    sortedLinks=dict(sorted(links.items(), key=lambda x: x[1]))

    for key in sortedLinks.keys():
        for key2 in linkDict.keys():
            if key2 in key and sortedLinks[key] >= 10:
                
                linkDict[key2][key] = key
    """

    print(links)
    print("\n\n")
    print(linkList)
    print("\n\n")
    addData(links,linkDict)


   
    objLoc =[]

   
    #création de la liste contenant des dictionnaires avec pour clé, le nom du lieu et pour valeurle nombre de fois mentionné
    # à partir des liens récupérés

    for elt in linkDict["https://ark.frantiq.fr/ark:/26678/"]:
        req = requests.get(elt.split(" ")[0])
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        archObj = soup.find(id="containerIndex:rightTab:textPrefLabel")
        linkDict["https://ark.frantiq.fr/ark:/26678/"][elt] = {archObj.text :  linkDict["https://ark.frantiq.fr/ark:/26678/"][elt] }
        objLoc.append(archObj.text)
    
    print("\n\n")
    print(linkDict)

    objectsInLoc = {}

    #création du dictionnaire avec les lieux où des objets archéologiques ont été trouvés
    
    for i in range(len(linkList)-2):
        
        while (linkList[i+1] in linkDict["https://ark.frantiq.fr/ark:/26678/"].keys()):
            if (linkList[i+1] in linkDict["https://ark.frantiq.fr/ark:/26678/"].keys() and linkList[i] in linkDict["http://www.geonames.org/"].keys() and linkList[i].split(" ")[1] not in objectsInLoc.keys()):  
                

                req = requests.get(linkList[i+1].split(" ")[0])
                soup = bs4.BeautifulSoup(req.text, "html.parser")
                archObj = soup.find(id="containerIndex:rightTab:textPrefLabel")
            
            
                objectsInLoc[linkList[i].split(" ")[1]] = [archObj.text]
            elif (linkList[i+1] in linkDict["https://ark.frantiq.fr/ark:/26678/"].keys() and linkList[i] in linkDict["http://www.geonames.org/"].keys() and linkList[i].split(" ")[1] in objectsInLoc.keys()):

                req = requests.get(linkList[i+1].split(" ")[0])
                soup = bs4.BeautifulSoup(req.text, "html.parser")
                archObj = soup.find(id="containerIndex:rightTab:textPrefLabel")
            
            
                objectsInLoc[linkList[i].split(" ")[1]].append(archObj.text)

            i+=1
        
        



    print(objectsInLoc)
    nbObjects = {}

# Ajout des données de Bretagne car l'ensemble bretagne est celui contenant le plus de données,
# en effet, les autres lieux contiennent qu'un ou deux objets ce qui nous permet pas de classer 
# de manière optimale les données par régions.
 
    for obj in objectsInLoc["Bretagne"] :
        if (obj not in nbObjects.keys()):
            nbObjects[obj] = 1
        else:
            nbObjects[obj] = nbObjects[obj]+1
        
    
#Création du CSV contenant les objets archéologiques et le nombre d'entre eux repérés dans le corpus
    fileObjects = pd.DataFrame({"Objets Archeologiques":nbObjects.keys(),"nombre": nbObjects.values()})
    fileObjects.to_csv("result.csv", index=False)


    """
    organizedData = {}
    start = 0
    for loc in linkDict["http://www.geonames.org/"]:
        print(linkDict["http://www.geonames.org/"][loc])
        organizedData[loc] = objLoc[start : linkDict["http://www.geonames.org/"][loc]]
        start += linkDict["http://www.geonames.org/"][loc]

    print(organizedData)
    """
    



