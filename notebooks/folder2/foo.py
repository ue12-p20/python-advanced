# le module bar se trouve dans le même dossier
# le plus simple du coup c'est d'utiliser
# ce qu'on appelle un import relatif comme ceci

from .bar import Bar

# maintenant je peux utiliser la variable Bar

def function(x):
    print(Bar(x))
    
