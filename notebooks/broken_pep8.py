# si on écrit du code trop large, ça empêche de l'arranger pour le juxtaposer avec un autre fichier ou ouvrir deux fenêtres sur le même fichier
d = {1:'un',2:'deux'}

def another (c):
    return 2*c

def broken(a,b,c):
    d=undefined(a,b)+another (c)
    return d
