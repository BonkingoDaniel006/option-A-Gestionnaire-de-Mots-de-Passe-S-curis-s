from flask import Flask, render_template, request
import random
import string
import csv
import json
import os
import math
from datetime import datetime

app = Flask(__name__)

FICHIER_JSON = 'coffre_fort.json'
FICHIER_CSV = 'sauvegarde_export.csv'
CATEGORIES = ["Réseaux sociaux", "Banque", "Email", "Travail", "Autre"]

def sauvegarder(comptes):
    with open(FICHIER_JSON, 'w', encoding='utf-8') as f:
        json.dump(comptes, f, indent=4, ensure_ascii=False)
    
    with open(FICHIER_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['site', 'categorie', 'mdp', 'date_creation', 'score'])
        for c in comptes:
            writer.writerow([c['site'], c['categorie'], c['mdp'], c['date_creation'], c['score']])

def charger_donnees():
    if not os.path.exists(FICHIER_JSON):
        return []
    try:
        with open(FICHIER_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def generer_mdp(longueur=16, type_mdp="complexe"):
    ambigus = "0Ol1I"
    
    if type_mdp == "prononcable":
        # 1. Préparation des listes sans caractères ambigus
        voyelles = "".join([c for c in "aeiouy" if c not in ambigus])
        consonnes = "".join([c for c in "bcdfghjkmnpqrstvwxz" if c not in ambigus])
        numbers = "".join([c for c in string.digits if c not in ambigus])
        
        # 2. Construction du mot de passe en alternant 3 types
        mdp_list = []
        for i in range(longueur):
            if i % 3 == 0:
                mdp_list.append(random.choice(consonnes))
            elif i % 3 == 1:
                mdp_list.append(random.choice(voyelles))
            else:
                mdp_list.append(random.choice(numbers))
        mdp = "".join(mdp_list)
        
    else:
        # Mode complexe (mélange total)
        source = "".join([c for c in (string.ascii_letters + string.digits + "!@#$%") if c not in ambigus])
        mdp = "".join(random.choice(source) for _ in range(longueur))
        
    return mdp

def analyser_force(mdp):
    longueur = len(mdp)
    r = 0
    if any(c in string.ascii_lowercase for c in mdp): r += 26
    if any(c in string.ascii_uppercase for c in mdp): r += 26
    if any(c in string.digits for c in mdp): r += 10
    if any(c in "!@#$%" for c in mdp): r += 5
    
    if r == 0: return 0
    entropie = longueur * math.log2(r)
    return min(100, int((entropie / 80) * 100))

def calculer_stats(comptes):
    if not comptes:
        return {"total": 0, "moyenne": 0, "faibles": 0}
    moyenne = sum(c['score'] for c in comptes) / len(comptes)
    faibles = len([c for c in comptes if c['score'] < 50])
    return {"total": len(comptes), "moyenne": round(moyenne, 2), "faibles": faibles}

def detecter_doublons(comptes):
    groupes_mdp = {}
    for c in comptes:
        mdp = c['mdp']
        if mdp in groupes_mdp:
            groupes_mdp[mdp].append(c['site'])
        else:
            groupes_mdp[mdp] = [c['site']]
    
    doublons = {mdp: sites for mdp, sites in groupes_mdp.items() if len(sites) > 1}
    return doublons

@app.route("/rechercher")
def rechercher():
    query = request.args.get("query", "").lower()
    comptes = charger_donnees()
    resultats = [c for c in comptes if query in c['site'].lower() or query in c['categorie'].lower()]
    return render_template("resultats.html", resultats=resultats, query=query)

@app.route("/create_mdp", methods=["POST"])
def ajouter_compte():
    comptes = charger_donnees()
    site = request.form.get("nom_site")
    cat = request.form.get("categorie")
    long = int(request.form.get("longueur", 16))
    t_mdp = request.form.get("type_mdp")

    if any(c['site'].lower() == site.lower() for c in comptes):
        return "Erreur : Ce site existe déjà !", 400

    password = generer_mdp(long, t_mdp)
    score = analyser_force(password)

    nouveau = {
        "site": site,
        "categorie": cat,
        "mdp": password,
        "date_creation": datetime.now().strftime("%Y-%m-%d"),
        "score": score
    }

    comptes.append(nouveau)
    sauvegarder(comptes)
    return render_template("okmdp.html", mdp=password, name_site=site, score=score)

@app.route("/")
def home():
    comptes = charger_donnees()
    stats = calculer_stats(comptes)
    doublons = detecter_doublons(comptes)
    return render_template("home.html", stats=stats, doublons=doublons)

@app.route("/form")
def form():
    return render_template("formulaire-d'ajout.html", categories=CATEGORIES)

@app.route("/liste")
def lister_comptes():
    comptes = charger_donnees()
    return render_template("liste.html", comptes=comptes)

if __name__ == "__main__":
    app.run(debug=True)