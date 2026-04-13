import string

def generer_password_lisible(longueur=12):
    
    ambigus = "ilI1Lo0O"
    
    lettres = "".join(c for c in string.ascii_letters if c not in ambigus)
    chiffres = "".join(c for c in string.digits if c not in ambigus)
    
    speciaux = "!@#$%" 
    
    source = lettres + chiffres + speciaux
    
    
    password = ''.join(secrets.choice(source) for _ in range(longueur))
    return password


mon_password = generer_password_lisible(10)
print(mon_password)
