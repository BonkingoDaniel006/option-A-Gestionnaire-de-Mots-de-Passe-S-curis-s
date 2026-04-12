mode_de_passe = input("Saisir votre mot de passe: ")
import string

def analyse_force(c):
    score = 0

    if any(char in string.ascii_uppercase for char in c):
        score += 26

    if any(char in string.ascii_lowercase for char in c):
        score += 26

    if any(char in string.digits for char in c):
        score += 10

    return score

resultat = analyse_force(mode_de_passe)
print(f"Score: {resultat}")


