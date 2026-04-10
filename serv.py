from flask import Flask, render_template,request
import secrets
import string
import csv

app = Flask(__name__)



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create_mdp", methods=["POST"])
def create_mdp(longueur=64):
    
    site= request.form.get("nom_site")
    lettres = "".join(c for c in string.ascii_letters )
    chiffres = "".join(c for c in string.digits )
    
    speciaux = "!@#$%" 
    
    source = lettres + chiffres + speciaux
    
    password = ''.join(secrets.choice(source) for _ in range(longueur))
    

    print(f"le mot de passe est : {password} pour le site: {site}")
    return render_template("okmdp.html")
@app.route("/form")
def form():
    return render_template("formulaire-d'ajout.html")






if __name__== "__main__":
    app.run(debug=True)