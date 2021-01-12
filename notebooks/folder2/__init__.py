# le code dans un __init__.py
# est exécuté lors du chargement du package

# avec cet import, on force le chargement de folder2.foo
# si l'appelant fais simplement 'import folder2'

from .foo import function
