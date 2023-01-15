def frequence(text:str) -> dict[str,int]:
    dictionnaire = []
    for t1 in text:
        dictionnaire[ord(t1)]=0
    for t2 in text:
        dictionnaire[ord(t2)]+= 1
    return dictionnaire

def croissant(dico:dict[str,int]) -> dict[str,int]:
    dico2 = sorted(dico.items(), key=lambda t: t[1])
    return dico2

print(croissant(frequence("banane")))

def frequence(text:str) -> list[int]:
    dictionnaire = []
    for i in range(255):
        dictionnaire.append(i)
        dictionnaire[i] = 0
    for t2 in text:
        dictionnaire[ord(t2)]+= 1
    print(dictionnaire)
    return dictionnaire

def croissant(dico:list[int]) -> list[int]:
    #pp
    return dico


print(croissant(frequence("banane")))