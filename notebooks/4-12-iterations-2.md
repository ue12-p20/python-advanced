---
celltoolbar: Slideshow
jupytext:
  cell_metadata_filter: all
  formats: md:myst
  notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
kernelspec:
  display_name: Python 3
  language: python
  name: python3
notebookname: "les it\xE9rations - suite"
rise:
  autolaunch: true
  slideNumber: c/t
  start_slideshow_at: selected
  theme: sky
  transition: cube
version: '1.0'
---

+++ {"slideshow": {"slide_type": "slide"}}

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat</span>
<span><img src="media/inria-25-alpha.png" /></span>
</div>

+++ {"slideshow": {"slide_type": ""}}

# les itérations - suite

+++ {"slideshow": {"slide_type": "slide"}}

## compréhensions

+++

très fréquemment on veut construire un mapping

+++ {"cell_style": "split"}

* appliquer une fonction à un ensemble de valeurs: `map`

![](media/iter-map.png)

+++ {"cell_style": "split"}

* idem en excluant certaines entrées: `map` + `filter`

![](media/iter-map-filter.png)

+++ {"slideshow": {"slide_type": "slide"}}

### compréhension de liste

+++ {"cell_style": "split"}

c'est le propos de la  
compréhension (de liste):

```python
[expr(x) for x in iterable]
```

+++ {"cell_style": "split"}

qui est  
équivalent à 

```python
result = []
for x in iterable:
    result.append(expr(x))
```

+++ {"slideshow": {"slide_type": "slide"}}

### compréhension de liste avec filtre

+++ {"cell_style": "split"}

si nécessaire on peut
ajouter un test de filtre:

```python
[expr(x) for x in iterable if condition(x)]
```

+++ {"cell_style": "split"}

qui est  
équivalent à 

```python
result = []
for x in iterable:
    if condition(x):
        result.append(expr(x))
```

+++ {"slideshow": {"slide_type": "slide"}}

#### compréhensions de liste - exemple 1

```{code-cell} ipython3
:cell_style: split

# la liste des carrés 
# des entiers entre 0 et 5

[x**2 for x in range(6)]
```

```{code-cell} ipython3
:cell_style: split

# si on décortique

result = []

for x in range(6):
    result.append(x**2)

result
```

+++ {"slideshow": {"slide_type": "slide"}}

#### compréhensions de liste - exemple 2

```{code-cell} ipython3
:cell_style: split

# la liste des cubes
# des entiers pairs entre 0 et 5

[x**3 for x in range(6) if x % 2 == 0]
```

```{code-cell} ipython3
:cell_style: split

# si on décortique

result = []

for x in range(6):
    if x % 2 == 0:
        result.append(x**3)

result
```

+++ {"slideshow": {"slide_type": "slide"}}

### compréhension de liste - imbrications

+++

* on peut **imbriquer plusieurs niveaux** de boucle
* la profondeur du résultat dépend **du nombre de `[`**  
  et **pas du nombre de `for`**

```{code-cell} ipython3
# une liste toute plate comme résultat
# malgré deux boucles for imbriquées
[x+10*y for x in (1, 2) for y in (1, 2)]
```

+++ {"slideshow": {"slide_type": "slide"}}

#### compréhensions imbriquées - exemple

+++ {"cell_style": "center"}

l'ordre dans lequel se lisent les compréhensions imbriquées:
il faut imaginer des for imbriqués **dans le même ordre**

```{code-cell} ipython3
:cell_style: split

[x + 10*y for x in range(1, 5) 
     if x % 2 == 0 
         for y in range(1, 5)
             if y % 2 == 1]
```

```{code-cell} ipython3
:cell_style: split

# est équivalent à
# (dans le même ordre)
L = []
for x in range(1, 5):
    if x % 2 == 0:
        for y in range(1, 5):
            if y % 2 == 1:
                L.append(x + 10*y)
L
```

+++ {"slideshow": {"slide_type": "slide"}}

### compréhension d'ensemble

+++

même principe exactement, mais avec des `{}` au lieu des `[]`

```{code-cell} ipython3
:cell_style: split

# en délimitant avec des {} 
# on construit une
# compréhension d'ensemble
{x**2 for x in range(-6, 7) 
    if x % 2 == 0}
```

```{code-cell} ipython3
:cell_style: split

# ATTENTION, rappelez-vous
# que {} est un dict !
result = set()

for x in range(-6, 7):
    if x % 2 == 0:
        result.add(x**2)
        
result
```

+++ {"slideshow": {"slide_type": "slide"}}

### compréhension de dictionnaire

+++

syntaxe voisine, avec un `:` pour associer clé et valeur

```{code-cell} ipython3
:cell_style: split

# sans filtre
 
{x : x**2 for x in range(4)}
```

```{code-cell} ipython3
:cell_style: split

# avec filtre

{x : x**2 for x in range(4) if x%2 == 0}
```

+++ {"slideshow": {"slide_type": "slide"}, "cell_style": "center"}

#### exemple : créer un index par une compréhension

+++

un idiome classique :

* on a une liste d'éléments (beaucoup, genre $10^6$)
* on veut pouvoir accéder **en temps constant** à un élément  
  à partir d'un id
* solution: créer un dictionnaire - qu'on appelle un *index*  
  (comme dans les bases de données)

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# créer une table qui permet un accès direct à partir du nom
personnes = [
    {'nom': 'Martin', 'prenom': 'Julie', 'age': 18},
    {'nom': 'Dupont', 'prenom': 'Jean', 'age': 32},
    {'nom': 'Durand', 'prenom': 'Pierre', 'age': 25},  
]

index = {personne['nom']: personne for personne in personnes}
index
```

```{code-cell} ipython3
# le concept est le même que dans une base de données
# en termes d'accès rapide à partir du nom qui jour le rôle d'id
index['Martin']
```

+++ {"slideshow": {"slide_type": "slide"}}

## expression génératrice

+++ {"slideshow": {"slide_type": ""}}

### performance des compréhensions

la compréhension **n'est pas l'arme absolue**  
elle a un **gros défaut**, c'est qu'on va toujours :

* parcourir **tout** le domaine
* et **allouer** de la mémoire   
* au moment où on évalue la compréhension,  
  i.e. **avant même** de faire quoi que ce soit d'autre

+++

finalement c'est **exactement** la même discussion que itérateur *vs* itérable  
e.g. quand on avait comparé `range()` avec une liste

+++ {"slideshow": {"slide_type": "slide"}}

### expression génératrice

* ça se présente un peu comme une compréhension de liste  
* mais **avec des `()` à la place des `[]`**
* supporte les `if` et les imbrications  
  exactement comme les compréhensions

```{code-cell} ipython3
data = [0, 1]
```

```{code-cell} ipython3
:cell_style: split

# compréhension

C = [x**2+y**2 for x in data for y in data]

for y in C:
    print(y)
```

```{code-cell} ipython3
:cell_style: split

# genexpr

G = (x**2+y**2 for x in data for y in data)

for y in G:
    print(y)
```

+++ {"slideshow": {"slide_type": "slide"}}

### les genexprs sont des itérateurs

+++

* les objets construits avec une expression génératrice sont de type `generator`
* en particulier ce sont des itérateurs

```{code-cell} ipython3
:cell_style: split

# compréhension

C = [x**2 for x in range(4)]

C
```

```{code-cell} ipython3
:cell_style: split

# genexpr

G = (x**2 for x in range(4))

G
```

```{code-cell} ipython3
:cell_style: split

# une compréhension est une vraie liste

C2 = [x**2 for x in range(100_000)]

import sys
sys.getsizeof(C2)
```

```{code-cell} ipython3
:cell_style: split

# les genexprs sont des itérateurs
# et donc sont tout petits

G2 = (x**2 for x in range(100_000))

sys.getsizeof(G2)
```

+++ {"slideshow": {"slide_type": "slide"}}

### compréhension ou genexpr ?

* les compréhensions de *dictionnaire* et d'*ensemble* sont souvent justifiées
* par contre, pour les *listes*: **toujours bien se demander**  
  si on a vraiment besoin de **construire la liste**

* ou si au contraire on a juste **besoin d'itérer** dessus  
  (souvent une seule fois d'ailleurs)

+++

* si on a vraiment besoin de cette liste  
  alors la compréhension est OK

* mais dans le cas contraire il faut **préférer un itérateur**   
  c'est le propos de l'**expression génératrice**

* qui souvent revient à remplacer `[]` par `()`  
  (ou même juste enlever les `[]`)

* exemple...

+++ {"cell_style": "split", "slideshow": {"slide_type": "slide"}}

apprenez à bien choisir entre  
compréhension et genexpr  
(les deux sont utiles)

```{code-cell} ipython3
:cell_style: split

# remplissons une classe imaginaire
from random import randint

matieres = ('maths', 'français', 'philo')

def notes_eleve_aleatoires():
    return {matiere: randint(0, 20) 
            for matiere in matieres}
```

```{code-cell} ipython3
:cell_style: center

# ici je crée une compréhension; pourquoi ?
notes_classe = [notes_eleve_aleatoires() for _ in range(4)]
notes_classe
```

```{code-cell} ipython3
# pour calculer la moyenne de la classe en maths
# pas besoin de garder les résultats intermédiaires
# du coup, on fabrique une genexpr
# en toute rigueur il aurait fallu écrire ceci
sum((notes_eleve['maths'] for notes_eleve in notes_classe)) / len(notes_classe)
```

```{code-cell} ipython3
# mais la syntaxe nous permet de nous en affranchir
# (remarquez une seul niveau de parenthèses, et l'absence de [])
sum(notes_eleve['maths'] for notes_eleve in notes_classe) / len(notes_classe)
```

+++ {"slideshow": {"slide_type": "slide"}}

## fonction génératrice

+++

* la **fonction génératrice** est une dernière forme très commune d'itérateurs
* écrite sous la forme d'une fonction  
  qui fait `yield` au lieu de `return`

```{code-cell} ipython3
:cell_style: split

# si une fonction contient
# au moins un yield
# elle devient une
# fonction génératrice

def squares(iterable):
    for i in iterable:
        yield i**2
```

```{code-cell} ipython3
:cell_style: split

data = (4, 1, 7)

# cet objet est un générateur
squares(data)
```

```{code-cell} ipython3
:cell_style: split

# en particulier
# on peut itérer dessus

for square in squares(data):
    print(square, end=" ")
```

+++ {"slideshow": {"slide_type": "slide"}}

### vocabulaire

* une expression génératrice retourne un objet de type `generator`
* il est fréquent - par abus de langage - d'appeler aussi simplement *générateur*  
  une fonction génératrice
* mais précisément, c'est **l'appel** à une fonction génératrice  
  qui retourne un objet de type `generator`
  
* on a donc **deux syntaxes différentes** pour construire  
  des objets qui sont **tous de type `generator`**

+++ {"slideshow": {"slide_type": "slide"}}

### expression génératrice *vs* fonction génératrice

```{code-cell} ipython3
:cell_style: split

# ces deux objets sont équivalents
gen1 = (x**2 for x in data)
```

```{code-cell} ipython3
:cell_style: split

def squares(iterable):
    for i in iterable:
        yield i**2
        
gen2 = squares(data)
```

```{code-cell} ipython3
:cell_style: split

for x in gen1:
    print(x)
```

```{code-cell} ipython3
:cell_style: split

for x in gen2:
    print(x)
```

+++ {"slideshow": {"slide_type": "slide"}}

#### expression génératrice *vs* fonction génératrice

+++

* les deux formes de générateur (expression et fonction)  
  produisent des objets de même type `generator`

```{code-cell} ipython3
:cell_style: split

# une genexpr
gen1 = (x**2 for x in data)
type(gen1)
```

```{code-cell} ipython3
:cell_style: split

# (le résultat d'une)
# fonction génératrice
gen2 = squares(data)
type(gen2)
```

* la fonction a toutefois une puissance d'expression supérieure
* notamment elle permet de **conserver l'état** de l'itération  
  sous la forme de variables locales

+++ {"slideshow": {"slide_type": "slide"}}

### exercice

implémenter un générateur qui parcourt tous les nombres premiers

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### `yield from`

+++

* une fonction génératrice est une fonction
* donc elle peut appeler d'autres fonctions
* qui peuvent elles-mêmes être des fonctions génératrices

+++

exemple :
partant d'une fonction génératrice qui énumère  
tous les diviseurs d'un entier (1 et lui-même exclus)

+++ {"cell_style": "center"}

comment écrire un générateur  
qui énumère tous les diviseurs  
... des diviseurs de `n` ?

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: slide
---
# on énumère les diviseurs
# en partant du plus grand
def divs(n):
    for i in range(n-1, 1, -1):
        if n % i == 0:
            yield i
```

```{code-cell} ipython3
:cell_style: split

for div in divs(12):
    print(div, end=" ")
```

```{code-cell} ipython3
:cell_style: center

# quelque chose qui fasse en gros
n = 12
for d1 in divs(n):
    for d2 in divs(d1):
        print(d2)
```

mais sous forme de fonction génératrice

+++ {"slideshow": {"slide_type": "slide"}}

#### `yield from`

+++

pour énumérer les diviseurs des diviseurs, on pourrait penser écrire

```{code-cell} ipython3
:cell_style: split

# première idée

# pourquoi ça ne marche pas ?

def divsdivs1(n):
    for d in divs(n):
        return divs(d)
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: fragment
---
# c'est bien un générateur
divsdivs1(12)
```

```{code-cell} ipython3
:cell_style: split

# mais...
for d in divsdivs1(12):
    print(d)    
```

+++ {"slideshow": {"slide_type": "fragment"}}

* on entre dans le `for` avec d=6
* on évalue `divs(6)` (un générateur) 
* **et c'est ça qu'on retourne** de suite

+++ {"slideshow": {"slide_type": "slide"}}

**deuxième idée**  
pour énumérer les diviseurs des diviseurs, on pourrait penser écrire

```{code-cell} ipython3
:cell_style: split

# pourquoi ça ne marche pas ?
def divsdivs2(n):
    for d in divs(n):
        yield divs(d)
```

```{code-cell} ipython3
:cell_style: split

# c'est bien un générateur
divsdivs2(12)
```

```{code-cell} ipython3
:cell_style: split

# mais...
for d in divsdivs2(12):
    print(d)
```

+++ {"slideshow": {"slide_type": "fragment"}}

* cette fois on va bien énumérer `divs(6)`, `divs(4)`, `divs(3)` puis `divs(2)` 
* **mais pas itérer** sur ces 4 générateurs
* c'est pourquoi ils se retrouvent imprimés tels quels

+++ {"slideshow": {"slide_type": "slide"}}

#### `yield from`

+++

* on voit que lorsqu'une fonction génératrice en appelle une autre
* il y a nécessité pour une syntaxe spéciale: `yield from`

```{code-cell} ipython3
:cell_style: split

def divdivs(n):
    for i in divs(n):
        yield from divs(i)
```

```{code-cell} ipython3
:cell_style: split

for div in divdivs(12):
    print(div)
```
