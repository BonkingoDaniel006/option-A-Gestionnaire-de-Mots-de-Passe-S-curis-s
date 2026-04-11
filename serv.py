from flask import Flask, render_template, request
import random
import string
import csv
import os

app = Flask(__name__)

FICHIER_CSV = 'mots_de_passe.csv'

def initialiser_csv():
    if not os.path.exists(FICHIER_CSV):
        with open(FICHIER_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['site', 'mot_de_passe'])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create_mdp", methods=["POST"])
def create_mdp():
    site = request.form.get("nom_site")
    longueur_str = request.form.get("longueur")
    longueur = int(longueur_str) if longueur_str and longueur_str.isdigit() else 12
    
    # Choix du type de mot de passe (via le formulaire)
    type_mdp = request.form.get("type_mdp")

    if type_mdp == "prononcable":
        # Définition des sets de caractères (sans ambigus)
        voyelles = "aeiouy"
        consonnes = "bcdfghjkmnpqrstvwxz"
        
        password = ""
        for i in range(longueur):
            if i % 2 == 0:
                password += random.choice(consonnes)
            else:
                password += random.choice(voyelles)
    else:
        # Ta logique actuelle (aléatoire complet)
        source = string.ascii_letters + string.digits + "!@#$%"
        ambigus = "0Ol1I"
        source_filtree = "".join([c for c in source if c not in ambigus])
        password = ''.join(random.choice(source_filtree) for _ in range(longueur))
    
    initialiser_csv()
    with open(FICHIER_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([site, password])
    
    return render_template("okmdp.html", mdp=password, name_site=site)

@app.route("/form")
def form():
    return render_template("formulaire-d'ajout.html")


@app.route("/rechercher")
def rechercher():
    query = request.args.get("query", "").lower()
    resultats = []
    
    if os.path.exists(FICHIER_CSV):
        with open(FICHIER_CSV, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for ligne in reader:
                # On cherche si le nom du site contient le texte tapé
                if query in ligne['site'].lower():
                    resultats.append(ligne)
    
    return render_template("resultats.html", resultats=resultats, query=query)

if __name__ == "__main__":
    app.run(debug=True)