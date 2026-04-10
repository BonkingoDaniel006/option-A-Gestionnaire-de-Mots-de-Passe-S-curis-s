mode_de_passe=input("essaie: ")
score =10
if mode_de_passe.isdigit() or mode_de_passe.isalpha():
            print("mais non veuillez modifier")
else:
    score=score+10
    print("ok")