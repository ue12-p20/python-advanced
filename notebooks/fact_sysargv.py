# on importe sys pour pouvoir accéder à sys.argv
import sys

def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

# le programme principal est souvent appelé `main`
def main():
    # sys.argv est une liste avec d'abord le nom du lanceur
    # puis les paramètres de la ligne de commande
    print(f"argv={sys.argv}")
    # on extrait le premier paramètre
    # qui est à l'index 1 car l'index 0 contient le lanceur
    number = int(sys.argv[1])
    # ya plus ka
    print(f"factorial({number})={factorial(number)}")

# un idiome fréquent : pour les points d'entrée
# on n'exécute ceci
# **SEULEMENT** si le fichier est vraiment le point d'entrée,
# et **PAS** s'il est importé
if __name__ == '__main__':
    main()
