print("Mode de passe")
mode_de_passe = input("Saisir votre mot de passe: ")
 
def analyse_mdp(a):
    score = 0
    longueur = len(a)
    if longueur < 8:
        print("court")
    elif 8 <= longueur <= 64:
        print("validé")
        score = score+10
        if mode_de_passe.isdigit() or mode_de_passe.isalpha():
            print("mais non veuillez modifier")
        else:
            score=score+10
            print(score) 
        

    else:
        print("long")

    
    return score

resultat = analyse_mdp(mode_de_passe)
print(f"Score: {resultat}")


    