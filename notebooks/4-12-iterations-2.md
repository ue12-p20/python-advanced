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

c'est le propos de la compréhension (de liste):

```python
[expression(x) for x in iterable
                 if condition(x)]
```

+++ {"cell_style": "split"}

équivalent à 

```python
result = []
for x in iterable:
    if condition(x):
        result.append(expression(x))
```

+++ {"slideshow": {"slide_type": "slide"}}

#### compréhensions de liste - équivalence

```{code-cell} ipython3
:cell_style: split

[x**3 for x in range(6) if x % 2 == 0]
```

```{code-cell} ipython3
:cell_style: split

result = []
for x in range(6):
    if x % 2 == 0:
        result.append(x**3)
result
```

+++ {"slideshow": {"slide_type": "slide"}}

### compréhension de liste - imbrications

+++

* la clause `if condition` est bien entendu optionnelle
* on peut imbriquer plusieurs niveaux de boucle
  * la profondeur du résultat dépend **du nombre de `[`**  
    et **pas du nombre de `for`**

```{code-cell} ipython3
# une liste toute plate comme résultat
# malgré deux boucles for imbriquées
[x+y for x in (1, 2) for y in (3, 4)]
```

+++ {"slideshow": {"slide_type": "slide"}}

#### compréhensions imbriquées - équivalence

+++ {"cell_style": "center"}

l'ordre dans lequel se lisent les compréhensions imbriquées:

```{code-cell} ipython3
:cell_style: split

[(x, y) for x in range(7) 
        if x % 2 == 0 
            for y in range(x) 
                if y % 2 == 1]
```

```{code-cell} ipython3
:cell_style: split

# est équivalent à
L = []
for x in range(7):
    if x % 2 == 0:
        for y in range(x):
            if y % 2 == 1:
                L.append((x, y))
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
{x**2 for x in range(-4, 5) 
 if x % 2 == 0}
```

```{code-cell} ipython3
:cell_style: split

# ATTENTION, rappelez-vous
# que {} est un dict !
result = set()

for x in range(-4, 5):
    if x % 2 == 0:
        result.add(x**2)
        
result
```

+++ {"slideshow": {"slide_type": "slide"}}

### compréhension de dictionnaire

+++

syntaxe voisine, avec un `:` pour associer clé et valeur

```{code-cell} ipython3
# créer une table qui permet un accès direct à partir du nom
personnes = [
    {'nom': 'Martin', 'prenom': 'Julie', 'age': 18},
    {'nom': 'Dupont', 'prenom': 'Jean', 'age': 32},
    {'nom': 'Durand', 'prenom': 'Pierre', 'age': 25},  
]

hash = {personne['nom']: personne for personne in personnes}
hash
```

```{code-cell} ipython3
# ici hash ressemble à un index dans une base de données
# en termes d'accès rapide à partir du nom
hash['Martin']
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

finalement c'est la même discussion que itérateur *vs* itérable  
e.g. quand on avait comparé `range()` avec une liste

+++ {"slideshow": {"slide_type": "slide"}}

### expression génératrice


* ça se présente un peu comme une compréhension de liste  
* mais **avec des `()` à la place des `[]`**
* supporte aussi les `if` et les imbrications

```{code-cell} ipython3
data = [1, 3]
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

# genexp

G = (x**2+y**2 for x in data for y in data)

for y in G:
    print(y)
```

+++ {"slideshow": {"slide_type": "slide"}}

### compréhension ou genexp ?

* les compréhensions de dictionnaire et d'ensemble sont souvent justifiées
* par contre, pour les listes: **toujours bien se demander**  
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

apprenez à bien choisir

```
les deux formes
(*) compréhension et
(*) genexp 
sont utiles
```

```{code-cell} ipython3
:cell_style: split

# remplissons une classe imaginaire
from random import randint

matieres = ('maths', 'français', 'philo')
eleves = ('jean', 'julie', 'marie')

def notes_eleve_aleatoires():
    return [randint(0, 20) for matiere in matieres]
```

```{code-cell} ipython3
:cell_style: center

# ici je crée une compréhension; pourquoi ?
notes_classe = [notes_eleve_aleatoires() for eleve in eleves]
notes_classe
```

```{code-cell} ipython3
# pour calculer la moyenne de la classe en maths
# pas besoin de garder les résultats intermédiaires
# du coup, on fabrique une genexp
# en toute rigueur il aurait fallu écrire ceci
sum((maths for maths, français, philo in notes_classe)) / len(eleves)
```

```{code-cell} ipython3
# mais la syntaxe nous permet de nous en affranchir
# (remarquez une seul niveau de parenthèses, et l'absence de [])
sum(maths for maths, français, philo in notes_classe) / len(eleves)
```

+++ {"cell_style": "split", "slideshow": {"slide_type": "slide"}}

typiquement utile avec `sum()`, `min()` et similaires

```{code-cell} ipython3
---
cell_style: center
slideshow:
  slide_type: ''
---
# j'ai un ensemble de valeurs
# je veux la somme des carrés de ces valeurs
data = {-10, 5, -9, 15, -21}
```

```{code-cell} ipython3
# je peux faire ceci
sum([x**2 for x in data])
```

```{code-cell} ipython3
# mais aussi juste ceci - remarquez l'absence des []
sum(x**2 for x in data)
```

+++ {"slideshow": {"slide_type": "slide"}}

### type `generator`

```{code-cell} ipython3
:cell_style: split

# on peut examiner ces deux objets
[x**2 for x in data]
```

```{code-cell} ipython3
:cell_style: split

# attention ici il faut les parenthèses
(x**2 for x in data)
```

* les objets construits avec une expression génératrice sont de type `generator`
* en particulier ce sont des itérateurs

+++

### benchmark

```{code-cell} ipython3
---
cell_style: center
slideshow:
  slide_type: slide
---
# comme ce sont des itérateurs, il y a potentiellement
# un énorme bénéfice à utiliser un générateur

# une fonction qui ne parcourt pas
# entièrement son paramètre iterable

def search_100(iterable):
    for i in iterable:
        if i == 100:
            return True
```

```{code-cell} ipython3
:cell_style: split

# cherchons 100 parmi les <n> premiers carrés
n = 10**6

# avec une compréhension 
# on fait beaucoup de travail
# pour rien
%timeit search_100([x**2 for x in range(n)])
```

```{code-cell} ipython3
:cell_style: split

# avec une exp. génératrice ...
# entre 50 et 100.000 fois plus rapide,
# c'est normal :
# on n'a pas eu besoin de créer
# la liste des carrés 
%timeit search_100(x**2 for x in range(n))
```

+++ {"slideshow": {"slide_type": "slide"}}

## fonction génératrice

+++

* la **fonction génératrice** est une dernière forme très commune d'itérateurs
* écrite sous la forme d'une fonction  
  qui fait `yield` au lieu de `return`
* souvent appelé simplement *générateur* (par abus de langage car techniquement l'expression génératrice
  est un générateur aussi)

* c'est plus clair avec un exemple

```{code-cell} ipython3
:cell_style: split

for square in squares(3):
    print(square, end=" ")
```

+++ {"slideshow": {"slide_type": "slide"}}

### expression génératrice *vs* fonction génératrice

+++

* les deux formes de générateur produisent des objets de même type `generator`
* la fonction a une puissance d'expression supérieure
* notamment elle permet de conserver l'état  
  sous la forme de variables locales
* et même en fait c'est plus fort que ça  
  car une fonction génératrice peut en appeler d'autres

```{code-cell} ipython3
:cell_style: split

generator1 = (x**2 for x in range(2))
type(generator1)
```

```{code-cell} ipython3
:cell_style: split

def squares(n):
    for i in range(n):
        yield i**2
        
generator2 = squares(2)
type(generator2)
```

+++ {"slideshow": {"slide_type": "slide"}}

### `yield from`

+++

partant d'une fonction génératrice qui énumère  
tous les diviseurs d'un entier (1 et lui-même exclus)

```{code-cell} ipython3
:cell_style: split

def divs(n):
    for i in range(2, n):
        if n % i == 0:
            yield i
```

```{code-cell} ipython3
:cell_style: split



for div in divs(30):
    print(div, end=" ")
```

* maintenant si je veux écrire une fonction génératrice  
  qui énumère tous les diviseurs des diviseurs de `n`

* il s'agit donc d'une fonction génératrice qui en appelle une autre
* il y a nécessité pour une syntaxe spéciale: `yield from`

+++ {"slideshow": {"slide_type": "slide"}}

#### `yield from`

```{code-cell} ipython3
:cell_style: split

def divdivs(n):
    for i in divs(n):
        yield from divs(i)
```

```{code-cell} ipython3
:cell_style: split

for div in divdivs(30):
    print(div, end=" ")
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_advanced"]}

### fonction génératrice - épilogue

+++

pour évaluer la boucle `for` dans ce dernier cas:

* la **pile** principale (de la fonction qui fait `for`)
* **et** une **pile** annexe qui évalue la fonction génératrice
* et qui se fait "mettre au congélateur" à chaque itération de la boucle
* l'état de l'itération: toutes les variables locales de la pile annexe
  * les deux `i` dans l'exemple précédent

c'est cette propriété qui est utilisée pour implémenter la librairie asynchrone `asyncio`

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### sous le capot de la boucle `for`

+++ {"cell_style": "split"}

lorsqu'on itère sur un itérable

```{code-cell} ipython3
:cell_style: split

iterable = [10, 20, 30]
```

sous le capot, la boucle `for` va faire:

  * créer un itérateur en appelant `iter(iterable)`
  * appeler `next()` sur cet itérateur
  * jusqu'à obtenir l'exception `StopIteration`

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: slide
---
for item in iterable:
    print(item)
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
iterateur = iter(iterable)
while True:
    try:
        item = next(iterateur)
        print(item)
    except StopIteration:
        # print("fin")
        break
```

+++ {"slideshow": {"slide_type": "slide"}}

#### sous le capot de la boucle `for`

+++

* `next()` et `iter()` sont des fonctions natives
* et naturellement:
  * `iter(obj)` appelle `obj.__iter__()`
  * `next(obj)` appelle `obj.__next__()`

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_advanced"]}

## itérations et itérables (partie optionnelle)

+++ {"slideshow": {"slide_type": "slide"}}

### rendre un objet itérable

+++

* en python, avec les classes, on peut 
  * se définir des types utilisateur
  * et bien les intégrer dans le langage 
* par exemple, il existe un *protocole* 
  * pour rendre un objet itérable
  * i.e. pour pouvoir l'utiliser dans un for
* deux moyens
  * via `__getitem__` (une séquence - accès direct)
  * via `__iter__()` qui doit retourner un itérateur

+++ {"slideshow": {"slide_type": "slide"}}

### itérable avec `__getitem__`

+++

* si votre objet est une séquence
* vous pouvez définir la méthode `__getitem__()`
  * qui sera alors appelée par le `for` 
  * avec en argument `0`, `1`, ...
  * jusqu'à ce que `__getitem__` lève `StopIteration`
* c'est adapté pour des objets qui ont un accès direct 
  * à leurs sous-composants
* technique assez *old-school* 
  * conservé pour compatibilité
  * mais on n'en parle plus dans la suite du cours

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: slide
---
# un itérable implémenté avec __getitem__

class PseudoSequence:
    
    def __init__(self, top):
        self.top = top
        
    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError
        if 0 <= index < self.top: 
            return 2 ** index
        else:
            raise IndexError
```

```{code-cell} ipython3
:cell_style: split

seq = PseudoSequence(4)
for i in seq:
    print(i)
```

```{code-cell} ipython3
:cell_style: split

seq[0], seq[2]
```

+++ {"slideshow": {"slide_type": "slide"}}

### itérable avec itérateur

+++

* on peut rendre un objet **itérable**
  * en écrivant la méthode magique `__iter__()`  
    qui doit retourner un itérateur

* Q: d'accord, mais alors c'est quoi un itérateur ?  
  A: ici à nouveau il y a un *protocole*

+++

* protocole **itérateur**
  * une méthode `__next__()`  
    qui à chaque appel retourne l’élément suivant
    ou qui lève une exception `StopIteration`  
    lorsqu’il n’y a plus d’élément à retourner

  * une méthode `__iter__()` qui retourne l’itérateur lui-même
    * et donc un itérateur est lui-même itérable

+++ {"slideshow": {"slide_type": "slide"}}

### séparer itérateur et itérable

+++

* le plus souvent possible
  * on définit les itérateurs "sans donnée"
  * comme `range()` ou `count()`
  * ou comme des générateurs
* lorsqu'on définit un itérateur sur une "vraie" structure de données
  * l'itérable contient les données
  * l'iterateur ne contient **que** la logique/état d'itération
  * il est important alors **séparer** les deux objets
  * ne serait-ce que pour pouvoir faire des boucles imbriquées

+++ {"slideshow": {"slide_type": "slide"}}

#### séparer itérateur et itérable

```{code-cell} ipython3
:cell_style: center

liste = [0, 10, 100]
```

```{code-cell} ipython3
:cell_style: split

for item in liste:
    print(item, end=" ")
```

```{code-cell} ipython3
:cell_style: split

# avec une seule boucle, 
# on peut itérer sur l'itérateur
iterator = iter(liste)

for item in iterator:
    print(item, end=" ")
```

```{code-cell} ipython3
:cell_style: split

# avec deux boucles par contre
for item1 in liste:
    for item2 in liste:
        print(f"{item1}x{item2}")
```

```{code-cell} ipython3
:cell_style: split

# ça ne fonctionne plus du tout !
iterator = iter(liste)

for item1 in iterator:
    for item2 in iterator:
        print(f"{item1}x{item2}")
```

+++ {"slideshow": {"slide_type": "slide"}}

### utilisation des itérables

+++

* on a défini les itérables par rapport à la boucle `for` 
* mais plusieurs fonctions acceptent en argument des itérables
* `sum`, `max`, `min`
* `map`, `filter`
* etc...

+++ {"slideshow": {"slide_type": "slide"}}

### exemple de la puissance des itérateurs

+++

* imaginons que je veuille afficher toutes les lignes d’un fichier qui contienne le mot 'matin'
* est-ce possible de le faire en seulement 4 lignes ?
* sans notation cryptique et incompréhensible

```{code-cell} ipython3
with open('../data/une-charogne.txt') as feed:
    for lineno, line in enumerate(feed, 1):
        if 'matin' in line:
            print(f"{lineno}:{line}", end="")
```

+++ {"slideshow": {"slide_type": "slide"}}

### quel objet est itérable ?

+++

* il existe beaucoup d’objets itérables en python
  * tous les objets séquence: listes, tuples, chaînes, etc.
  * les sets, les dictionnaires
  * les vues (dict.keys(), dict.values()), etc.
  * les fichiers
  * les générateurs
* il faut les utiliser, c’est le plus rapide et le plus lisible

+++ {"slideshow": {"slide_type": "slide"}}

### quel objet est un itérateur ?

+++ {"cell_style": "split"}

* on peut voir si  
  `iter(obj) is obj`

```{code-cell} ipython3
:cell_style: split

def is_iterator(obj):
    return iter(obj) is obj
```

* à la lumière de ce qu'on a vu
  * une liste **n'est pas** son propre itérateur
  * un fichier **est** son propre itérateur

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: slide
---
# un fichier est son propre itérateur
with open("../data/une-charogne.txt") as F:
    print("propre itérateur ? ",
          is_iterator(F))
```

```{code-cell} ipython3
:cell_style: split

# la liste non
L = list(range(5))
print("propre itérateur ? ",
      is_iterator(L))
```

```{code-cell} ipython3
:cell_style: split

# range() non plus 
R = range(5)
print("propre itérateur ? ",
      is_iterator(R))
```

```{code-cell} ipython3
:cell_style: split

# range() non plus 
Z = zip(L, L)
print("propre itérateur ? ",
      is_iterator(Z))
```

* de manière générale, un objet qui est un itérateur  
  ne peut être itéré qu'une seule fois

* attention donc par exemple à ne pas essayer  
  d'itérer plusieurs fois sur le même objet `zip`
