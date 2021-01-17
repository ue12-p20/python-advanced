import sys

def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

def main():
    # on analyse à la main la ligne de commande
    # pour voir si elle contient une option ou pas
    verbose = False
    counter = 1
    if sys.argv[counter] == "-v":
        verbose = True
        counter += 1
    number = int(sys.argv[counter])
    # agir selon l'option demandée
    if verbose:
        print(f"factorial({number})={factorial(number)}")
    else:
        print(factorial(number))

if __name__ == '__main__':
    main()
