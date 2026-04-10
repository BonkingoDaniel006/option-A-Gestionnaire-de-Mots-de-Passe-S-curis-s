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
def create_mdp(longueur=64):
    site = request.form.get("nom_site")
    
    lettres = string.ascii_letters
    chiffres = string.digits
    speciaux = "!@#$%" 
    
    ambigus = "0Ol1I"
    
    source_complete = lettres + chiffres + speciaux
    source_filtree = "".join([char for char in source_complete if char not in ambigus])
    
    password = ''.join(random.choice(source_filtree) for _ in range(longueur))
    
    initialiser_csv()
    with open(FICHIER_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([site, password])
    
    return render_template("okmdp.html", mdp=password, name_site=site)

@app.route("/form")
def form():
    return render_template("formulaire-d'ajout.html")

if __name__ == "__main__":
    app.run(debug=True)