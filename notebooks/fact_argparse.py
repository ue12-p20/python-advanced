import sys
from argparse import ArgumentParser

def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

def main():
    # on construit un objet ArgumentParser
    parser = ArgumentParser()
    # ensuite le code est déclaratif
    # on se contente de dire quel.le.s sont les options et paramètres
    parser.add_argument("-v", "--verbose", default=False, action='store_true',
                        # en donnant un petit text d'explication
                        help="enable verbose mode")
    # on peut aussi dire leur type, pas besoin de les convertir
    parser.add_argument("number", type=int, help="the input integer")
    
    # on déclenche l'analyse de la ligne de commande
    # en fonction de ces spécifications
    args = parser.parse_args()

    # et on récupère les valeurs qui nous intéressent
    # dans les attributs du résultat de parse_args()
    verbose = args.verbose
    number = args.number

    # le reste est comme avant
    if verbose:
        print(f"factorial({number})={factorial(number)}")
    else:
        print(factorial(number))

# un idiome fréquent : pour les points d'entrée
# on n'exécute ceci
# **SEULEMENT** si le fichier est vraiment le point d'entrée,
# et **PAS** s'il est importé
if __name__ == '__main__':
    main()
