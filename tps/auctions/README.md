---
jupyter:
  jupytext:
    cell_metadata_filter: all, -hidden, -heading_collapsed, -run_control, -trusted
    main_language: python
    notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
      -jupytext.text_representation.format_version, -language_info.version, -language_info.codemirror_mode.version,
      -language_info.codemirror_mode, -language_info.file_extension, -language_info.mimetype,
      -toc
    text_representation:
      extension: .md
      format_name: markdown
  language_info:
    name: python
    pygments_lexer: ipython3
---

# python-inheritance

OOP and inheritance ... in Python!

## Instructions

Votre but est d'implémenter des ventes aux enchères. Une vente aux enchères à l'aveugle a déjà été implémentée pour vous dans le fichier `blind.py`.
Vous pouvez exécuter chacun des fichiers directement, pour "jouer" aux enchères:

```
$ python blind.py
```

Des tests pour ces enchères on été implementés dans `test_blind.py`. Vous pouvez les exécuter avec VSCode, ou bien directement dans le terminal:

```
$ python test_blind.py
```

Votre but va être d'implémenter d'autres types d'enchères. Pour chaque type d'enchères, un fichier de test vous est fourni.

Il y a également un certain nombre d'utilitaires dans le projet (`utils.py`, `testing_utils.py`), mais pour ce TP, vous n'avez pas besoin de les regarder.
Je vous déconseille fortement de les modifier 🙃

### Avant toute chose

- Chacune des enchères a déjà un constructeur. Vous pouvez ajouter des choses dans ce constructeur, mais **pas en supprimer**.
- Pour intéragir avec la ligne de commande, vous devez **impérativement** utiliser l'utilitaire `self.cli` qui est dans les enchères.
  - Vous pouvez faire l'équivalent de `print()` en faisant `self.cli.display()`
  - Vous pouvez demander à l'utilisateur de saisir des choses sur la ligne de commande, l'équivalent de `value = input("Entrez une valeur")`, en faisant `value = self.cli.prompt("Entrez une valeur")`
  - L'usage direct de `print()` et `input()` est proscrit, sinon les tests ne marcheront pas
  - Cette classe nous sert à simuler `print` et `input` dans les tests automatisés
- Pour ce TP, vous pouvez estimer que les utilisateurs du programme ne font que des choses "légales"
  - Par exemple, quand on leur demande d'enchérir, ils tapent "10" ou "115", mais ils ne tapent pas "toto 1234 %&@# 💣💩🤮"
  - Par exemple, quand on leur demande de sur-enchérir sur une enchère de 30, ils tapent "45" ou une chaîne vide pour passer leur tour, mais pas "12"
  - Le but n'est pas de tester toutes les possibilités !
- Les exemples sont écrits avec en gris le texte affiché par le programme, et en orange pour le texte saisi par l'utilisateur (sur Github, ca peut varier selon les éditeurs de code). Ignorez les `#` et les `!`, qui ne sont là que pour le formattage:

```diff
# Le programme affiche ceci.
# Veuillez saisir une valeur:
! 30
# Vous avez saisi: 30
```

### Comment exécuter les tests dans VSCode

1. Ouvrez tout le dossier dans VSCode
2. Dans le menu View, ouvrez la Command Palette (Ctrl + Shift + P / Cmd + Shift + P)

![one](https://raw.githubusercontent.com/Kehrlann/python-inheritance/master/images/one.png)

3. Tapez "python test" et sélectionnez "Python: Run all tests"

![two](https://raw.githubusercontent.com/Kehrlann/python-inheritance/master/images/two.png)

4. Cliquez sur la pop-up en bas à droite

![three](https://raw.githubusercontent.com/Kehrlann/python-inheritance/master/images/three.png)

5. Dans le menu, sélectionnez `unittest` (c'est l'outil qu'on utilise pour cet exercice)

![four](https://raw.githubusercontent.com/Kehrlann/python-inheritance/master/images/four.png)

6. Puis sélectionnez `. Root directory`

![five](https://raw.githubusercontent.com/Kehrlann/python-inheritance/master/images/five.png)

7. Puis `test_*.py` (c'est comme ca que s'appellent nos fichiers de test):

![six](https://raw.githubusercontent.com/Kehrlann/python-inheritance/master/images/six.png)

8. Ca vous donnera accès à un nouvel onglet (1). Dans cet onglet faites le 2 pour "découvrir" les fichiers de test, "3" pour les exécuter et "4" pour ouvrir une console. Vous pouvez aussi exécuter les tests un par un:

![seven](https://raw.githubusercontent.com/Kehrlann/python-inheritance/master/images/seven.png)

---

Passons au TP, enfin !

### 1. Blind auction: les règles

Voici les règles des enchères à l'aveugle, ou [Blind auction](https://en.wikipedia.org/wiki/First-price_sealed-bid_auction):

- Les enchères démarrent avec un prix minimum
- Les enchérisseurs doivent sur-enchérir par rapport au prix minimum
- Les enchérisseurs ne savent pas quel est la plus haute enchère (on estime qu'ils ne peuvent pas lire ce que les autres on saisi dans le terminal)
- Il n'y a qu'un seul tour
- Le gagnant est celui qui a proposé le prix le plus haut
- Le prix final est le prix le plus haut proposé

Exemple:

```diff
# Started auction of type: Blind
# Please enter the opening bid:
! 30
# Opening bid is: 30
# Enter bidder (enter nothing to move on):
! alice
# Enter bidder (enter nothing to move on):
! bob
# Enter bidder (enter nothing to move on):
! carol
# Enter bidder (enter nothing to move on):
!
# Bidders are: alice, bob, carol
#
# Opening bid is 30. alice bids:
! 35
# Opening bid is 30. bob bids:
! 50
# Opening bid is 30. carol bids:
! 40
# ~~~~~~~~
#
# Winner is bob. Winning bid is 50.
```

### 2. Blind auction: le code

🚀 Regardez le fichier `blind.py`, tout a déjà été implémenté pour vous. Lisez le code, exécutez le fichier, faites une partie d'enchères.

Vous pouvez également regarder `test_blind.py` pour avoir une idée de comment les tests sont écrits, si vous êtes curieux.

🚀 Exécutez `test_blind.py`, de préférence avec VS Code. Si vous exécutez dans le terminal, vous devriez avoir ce genre de résultat:

```
$ python test_auctions.py

...
----------------------------------------------------------------------
Ran 3 tests in 0.303s

OK
```

Les 3 points indiquent 3 tests qui fonctionnent, et le "OK" indique que tous les tests passent. C'est important, parce que vous allez, plus tard dans le TP, modifier `blind.py`.

### 3. English auction: les règles

Vous allez maintenant implémenter des enchères anglaises, ou [English auction](https://en.wikipedia.org/wiki/English_auction). Voici les règles:

- Les enchères démarrent avec un prix minimum
- Les enchérisseurs doivent sur-enchérir par rapport à la meilleure enchère en cours
- Les enchérisseurs voient la plus haute enchère en cours
- Il y a plusieurs tours
- L'enchère est finie lorsque tous les participants passent leur tour (ne tapent rien dans le terminal)
- Le gagnant est celui qui a proposé le prix le plus haut
- Le prix final est le prix le plus haut proposé

Exemple:

```diff
# Started auction of type: English
# Please enter the opening bid:
! 50
# Opening bid is: 30
# Enter bidder (enter nothing to move on):
! alice
# Enter bidder (enter nothing to move on):
! bob
# Enter bidder (enter nothing to move on):
! carol
# Enter bidder (enter nothing to move on):
!
# Bidders are: alice, bob, carol
#
# Standing bid is 30. alice bids:
! 35
# Standing bid is 35. bob bids:
! 40
# Standing bid is 40. carol bids:
!
# Standing bid is 40. alice bids:
! 45
# Standing bid is 45. bob bids:
!
# Standing bid is 45. carol bids:
!
# Standing bid is 45. alice bids:
!
# Standing bid is 45. bob bids:
!
# Standing bid is 45. carol bids:
!
# ~~~~~~~~
#
# Winner is alice. Winning bid is 45.
```

🚀 Implémentez l'English auction dans `english.py`. Vous avez le droit de tout copier-coller depuis `blind.py` pour commencer! Vous devez exécuter les tests jusqu'à ce que `test_english.py` fonctionne à 100%.

### 4. Mise en commun: le facile

Remarquez maintenant les similitudes entre `blind` et `english`.

🚀 Introduisez une classe de base, par exemple `Auction` dans le fichier `auction.py`, et mutualisez les étapes en commun dans `blind` et `english`, par exemple en introduisant des fonctions spécifiques.

N'oubliez pas d'exécuter les tests de `blind` et `english` pour être sûrs que vous n'avez rien cassé!

### 5. Mise en commun: un peu plus intéressant

🚀 Essayez de ne définir la méthode "play" que dans la classe de base, `auction`. Comment s'y prendre ?

### 6. Vickrey auction

Il devrait être facile d'implémenter une nouvelle enchère!

Voici les règles des enchères en plis cachetés à un tour au second prix, ou [Enchère de Vickrey](https://en.wikipedia.org/wiki/Vickrey_auction):

- Les enchères démarrent avec un prix minimum
- Les enchérisseurs doivent sur-enchérir par rapport au prix minimum
- Les enchérisseur ne savent pas quel est la plus haute enchère (on estime qu'ils ne peuvent pas lire ce que les autres on saisi dans le terminal)
- Il n'y a qu'un seul tour
- Le gagnant est celui qui a proposé le prix le plus haut
- Le prix final est la _deuxième enchère la plus haute_

Exemple:

```diff
# Started auction of type: Vickrey
# Please enter the opening bid:
! 30
# Opening bid is: 30
# Enter bidder (enter nothing to move on):
! alice
# Enter bidder (enter nothing to move on):
! bob
# Enter bidder (enter nothing to move on):
! carol
# Enter bidder (enter nothing to move on):
!
# Bidders are: alice, bob, carol
#
# Opening bid is 30. alice bids:
! 35
# Opening bid is 30. bob bids:
! 50
# Opening bid is 30. carol bids:
! 40
# ~~~~~~~~
#
# Winner is bob. Winning bid is 40.
```

🚀 A vous de jouer, comme d'habitude vous avez un fichier de test `test_vickrey.py`. Le cas ci-dessus est intéressant pour votre implémentation.

### 7. Jeu libre

Si vous avez encore le temps, n'hésitez pas à modifier votre programme pour mettre une méthode qui représente "un tour" d'enchères dans la classe de base, et voir comment modifier vos classes filles pour l'utiliser. Pas de test particulier pour ça, mais, comme d'habitude, il ne faut rien casser !
