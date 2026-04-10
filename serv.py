from flask import Flask, render_template
import secrets
import string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create_mdp")
def create_mdp(longueur=64):
    
    
    lettres = "".join(c for c in string.ascii_letters )
    chiffres = "".join(c for c in string.digits )
    
    speciaux = "!@#$%" 
    
    source = lettres + chiffres + speciaux
    
    
    password = ''.join(secrets.choice(source) for _ in range(longueur))
    print(f"le mot de passe est : {password}")
    return "ok"






if __name__== "__main__":
    app.run(debug=True)