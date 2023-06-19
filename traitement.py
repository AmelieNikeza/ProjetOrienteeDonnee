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

    print("anlyse du fichier...")
    # Parcourir les entités nommées extraites
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
                print("lol")
                linkDict[key2][key] = key
    """

    print(links)
    print(linkList)
    addData(links,linkDict)

    #filterData(linkDict,10)

   
    objLoc =[]

   

    for elt in linkDict["https://ark.frantiq.fr/ark:/26678/"]:
        req = requests.get(elt.split(" ")[0])
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        archObj = soup.find(id="containerIndex:rightTab:textPrefLabel")
        linkDict["https://ark.frantiq.fr/ark:/26678/"][elt] = {archObj.text :  linkDict["https://ark.frantiq.fr/ark:/26678/"][elt] }
        objLoc.append(archObj.text)
    
    print("\n\n")
    print(linkDict)
    """
    organizedData = {}
    start = 0
    for loc in linkDict["http://www.geonames.org/"]:
        print(linkDict["http://www.geonames.org/"][loc])
        organizedData[loc] = objLoc[start : linkDict["http://www.geonames.org/"][loc]]
        start += linkDict["http://www.geonames.org/"][loc]

    print(organizedData)
    """
    



