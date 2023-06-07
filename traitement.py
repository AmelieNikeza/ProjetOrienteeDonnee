import spacy
import pandas as pd


# Charger le modèle linguistique
nlp = spacy.load("fr_core_news_sm")

nlp.max_length = 2848830
"""
data = pd.read_csv('dataBretagne.csv')
data.to_csv("data.txt", sep=',', index=False)
"""

with open("dataBretagne.txt", "r", encoding="utf-8") as file:
    text = file.read()

    # Appliquer le modèle sur le texte
    
    doc = nlp(text)

    print("anlyse du fichier...")
    # Parcourir les entités nommées extraites

    orgs = {}

    for ent in doc.ents:
        if ent.label_ == "PER":  # Personne
            print("Nom de personne :", ent.text)
        elif ent.label_ == "ORG":  # Organisation
            print("Nom d'organisation :", ent.text)