---
celltoolbar: Slideshow
jupytext:
  cell_metadata_filter: all, -hidden, -heading_collapsed, -run_control, -trusted
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -language_info.version, -language_info.codemirror_mode.version, -language_info.codemirror_mode,
    -language_info.file_extension, -language_info.mimetype, -toc
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
language_info:
  name: python
  pygments_lexer: ipython3
nbhosting: 
  title: containers (2/2)
rise:
  autolaunch: true
  slideNumber: c/t
  start_slideshow_at: selected
  theme: sky
  transition: cube
version: '1.0'
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat</span>
<span><img src="media/inria-25-alpha.png" /></span>
</div>

+++

# les containers (2/2)

* les listes ne sont pas la panacée

+++ {"slideshow": {"slide_type": "slide"}}

## problème avec les séquences

```{code-cell} ipython3
a = range(30000000)
'x' in a      # c’est long !
```

```{code-cell} ipython3
a[3]          # on peut utiliser un indice entier
```

```{code-cell} ipython3
a = []
# on ne peut pas indexer avec un nom ou autre chose qu'un entier
try:
    a['alice'] = 10
except TypeError as e:
    print("OOPS", e)
```

+++ {"slideshow": {"slide_type": "slide"}}

### problème avec les séquences...

+++

* une séquence est une liste ordonnée d’éléments  
  indexés par des entiers

  * les recherches sont longues *O(n)*
  * impossible d’avoir un index autre qu’entier
  * comment faire, par exemple, un annuaire ?
* on voudrait
  * une insertion, effacement et recherche en *O(1)*
  * une indexation par clef quelconque

+++ {"slideshow": {"slide_type": "slide"}}

## la solution : les tables de hash

+++

* une table de hash T indexe des valeurs par des clefs
  * chaque clef est unique
  * T[clef] = valeur
  * insertion, effacement, recherche en O(1)

+++ {"slideshow": {"slide_type": "slide"}}

### comment ça marche ?

+++

![hash](media/hash.png)

+++ {"slideshow": {"slide_type": "slide"}}

### fonction de hachage

+++

* la fonction de hash *f()* choisie de façon à ce que
  * *f(key, size)* retourne toujours la même valeur 
  * *key* doit être **immutable**
* minimise le risque de collision
  * *f(key1, size)* == *f(key2, size)*
* une bonne façon de minimiser les collisions  
  est de garantir une distribution uniforme

+++ {"slideshow": {"slide_type": "slide"}}

### table de hash et Python

+++

* le dictionnaire `dict` est une table de hash  
  qui utilise comme clef un **objet immutable**  
  et comme valeur n’importe quel objet

  * association clé → valeur

+++ {"slideshow": {"slide_type": ""}}

* l'ensemble `set` est une table de hash  
  qui utilise comme clef un **objet immutable**  
  et qui n’associe pas la clef à une valeur

  * notion d’ensemble mathématique

+++ {"slideshow": {"slide_type": "slide"}}

## le `set`

+++

* collection non ordonnée d’objets uniques et **immutables**
* utile pour tester l’appartenance
  * optimisé, beaucoup + rapide que `list`
* et éliminer les entrées doubles d’une liste
* test d’appartenance plus rapide que pour les listes
* les sets autorisent les opérations sur des ensembles
  * union (|), intersection (&), différence (-), etc.

+++ {"slideshow": {"slide_type": "slide"}}

### construire un `set`

```{code-cell} ipython3
:cell_style: split

# attention: {} c'est 
# un DICTIONNAIRE vide 
set()          # ensemble vide
```

```{code-cell} ipython3
:cell_style: split

L1 = [1, 2, 3, 1, 1, 6, 4]
S1 = set(L1)
S1
```

+++ {"slideshow": {"slide_type": "slide"}}

#### construire un `set`...

```{code-cell} ipython3
:cell_style: center

# attention: il faut passer 
# à set UN itérable
try:
    S = set(1, 2, 3, 4, 5)
except Exception as exc:
    print(f"OOPS {type(exc)}")    
```

+++ {"slideshow": {"slide_type": "slide"}}

### `set` et opérateurs

```{code-cell} ipython3
:cell_style: split

S1
```

```{code-cell} ipython3
:cell_style: split

L2 = [3, 4, 1]
S2 = set(L2)
S2
```

```{code-cell} ipython3
:cell_style: split

4 in S2
```

```{code-cell} ipython3
:cell_style: split

S1 - S2            # différence
```

```{code-cell} ipython3
:cell_style: split

S1 | S2            # union
```

```{code-cell} ipython3
:cell_style: split

S1 & S2            # intersection
```

+++ {"slideshow": {"slide_type": "slide"}}

### le `set`: méthodes

```{code-cell} ipython3
:cell_style: split

# ensemble littéral
S3 = {1, 2, 3, 4}        
S3
```

```{code-cell} ipython3
:cell_style: split

# ajout d'un élément

S3.add('spam')
S3
```

```{code-cell} ipython3
:cell_style: split

# pas de duplication
# et pas d'ordre particulier
S3.update([10, 11, 10, 11])
S3
```

```{code-cell} ipython3
:cell_style: split

S3.remove(11)
S3
```

+++ {"slideshow": {"slide_type": "slide"}}

### `frozenset`

+++

* un `set` est un objet **mutable**
* le `frozenset` est équivalent mais **non mutable**
* un peu comme `list` et `tuple`
* par exemple pour servir de clé dans un hash

```{code-cell} ipython3
:cell_style: split

fs = frozenset([1, 2, 3, 4])
```

```{code-cell} ipython3
:cell_style: split

# frozenset pas mutable
try:
    fs.add(5)
except AttributeError as e:
    print("OOPS", e)   
```

+++ {"slideshow": {"slide_type": "slide"}}

## rapide test de performance

+++ {"cell_style": "split"}

pour la recherche d’un élément  
les sets sont **beaucoup plus rapides**

```{code-cell} ipython3
:cell_style: split

import timeit
```

```{code-cell} ipython3
timeit.timeit(setup= "x = list(range(100000))", stmt = '"c" in x',
              number = 300)
```

```{code-cell} ipython3
timeit.timeit(setup= "x = set(range(100000))", stmt = '"c" in x',
              number = 300)
```

+++ {"slideshow": {"slide_type": "slide"}}

### rapide test de performance...

+++

même si la liste est très petite

```{code-cell} ipython3
timeit.timeit(setup= "x = list(range(2))", stmt = '"c" in x',
              number = 6000000)
```

```{code-cell} ipython3
timeit.timeit(setup= "x = set(range(2))", stmt = '"c" in x',
              number = 6000000)
```

+++ {"slideshow": {"slide_type": "slide"}}

### remarque

+++

avec `ipython` ou dans un notebook, vous pouvez faire vos benchmarks un peu plus simplement

```{code-cell} ipython3
# en Python pur

timeit.timeit(setup= "x = set(range(2))", stmt = '0 in x',
              number = 6000000)
```

```{code-cell} ipython3
# avec ipython / notebook vous pouvez 
# faire comme ceci à la place

x = set(range(2))
%timeit -n 6000000 0 in x
```

+++ {"slideshow": {"slide_type": "slide"}}

## le dictionnaire

+++

* généralisation d’une table de hash
* collection non ordonnée d’objets
* techniquement, uniquement les pointeurs sont stockés, mais pas une copie des objets
* on accède aux objets à l’aide d’une clef (et non d’un indice comme pour une liste)
* une **clef** peut être n’importe quel objet **immutable**: chaîne, nombre, tuple d’objets immutables...
* c’est une structure de données très puissante
* le dictionnaire est un type **mutable**

+++ {"slideshow": {"slide_type": "slide"}}

### construire un dictionnaire

```{code-cell} ipython3
# ATTENTION : {} n'est pas un ensemble
# les dictionnaires étaient là avant les ensembles !
D = {}
D
```

```{code-cell} ipython3
# un dictionnaire créé de manière littérale
{ 'douze' : 12, 1: 'un', 'liste' : [1, 2, 3] }
```

```{code-cell} ipython3
:cell_style: split

# une autre façon quand 
# les clés sont des chaînes
dict( a = 'A', b = 'B')
```

```{code-cell} ipython3
:cell_style: split

# à partir d'une liste de couples
dict( [ ('a', 'A'), ('b', 'B') ] )
```

+++ {"slideshow": {"slide_type": "slide"}}

### utiliser un dictionnaire

+++ {"cell_style": "split"}

formes les plus courantes

* `D[clef]` retourne la valeur pour la clef
* `D[clef] = x` change la valeur pour la clef
* `clef in D` teste l’existence de clef dans D
* `for k, v in D.items():` itère sur D
* `for f in D:` itère sur les clés

+++ {"cell_style": "split"}

et aussi

* `del D[clef]` supprime la clef et la valeur
* `len(D)` retourne le nombre de clefs dans D
* `clef not in D` teste la non existence
* `D.copy()` *shallow copy* de D

+++

***

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: slide
---
d = {'alice': 35, 'bob' : 9, 'charlie': 6}
d
```

```{code-cell} ipython3
:cell_style: split

# nombre de clés
len(d)
```

```{code-cell} ipython3
:cell_style: split

# accéder en lecture
d['alice']
```

```{code-cell} ipython3
:cell_style: split

# test d'appartenance
'bob' in d
```

```{code-cell} ipython3
:cell_style: split

# accéder en écriture
d['jim'] = 32
d
```

```{code-cell} ipython3
:cell_style: split

# détruire une clé (et la valeur)
del d['jim']
d
```

+++ {"slideshow": {"slide_type": "slide"}}

### méthodes sur les dictionnaires

+++

* `D.get(clef)`
  * retourne la valeur associée à cette clé si elle est présente, `None` sinon
  * notez bien que `D[clef]` lance **une exception** si la clé n'est **pas présente**
  * `D.get(clef, un_truc)` retourne `un_truc` quand la clé n'est pas présente

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# au départ
d
```

```{code-cell} ipython3
:cell_style: split

# la clé n'est pas présente
try:
    d['marc']
except KeyError as e:
    print("OOPS", e)
```

```{code-cell} ipython3
:cell_style: split

# on peut utiliser `get` plutôt 
# si on préfère un retour de fonction
d.get('marc', '?')
```

+++ {"slideshow": {"slide_type": "slide"}}

### `defaultdict`

+++ {"cell_style": "split"}

cas d'usage fréquent :

* on veut créer un dictionnaire
* dont les valeurs sont des listes
* on se retrouve à devoir tester  
  l'existence de la clé à chaque fois

```python
D = {}
for ...:
    if x not in D:
        D[x] = list()
    D[x].append(y)
```

+++ {"cell_style": "split"}

+ joli avec un `defaultdict`

```python
from collections import defaultdict

D = defaultdict(list)
for ...:
    # defaultdict crée automatiquement
    # D[x] = list() si x n'est pas présent
    D[x].append(y)
```

```{code-cell} ipython3
---
cell_style: center
slideshow:
  slide_type: slide
---
from collections import defaultdict

# on peut utiliser le type qu'on veut
dd = defaultdict(set)
# ici on n'a pas encore de valeur 
# pour la clé '0' mais defaultdict 
# crée pour nous à la volée une liste vide
dd[0].add(1)
dd[0]
```

+++ {"slideshow": {"slide_type": "slide"}}

### les composantes du dictionnaires

+++

* `D.items()` retourne **une vue** sur les (clef, valeur) de `D`
* `D.keys()` retourne une vue sur les clefs de `D`
* `D.values()` retourne une vue sur les valeurs de `D`

+++ {"slideshow": {"slide_type": "slide"}}

### qu’est-ce qu’une vue ?

+++

* c’est un objet qui donne une vue **dynamique** sur un dictionnaire `D`
* dynamique, c'est-à-dire que si `D` est modifié après la création de la vue  
  la vue continue de refléter la réalité
* permet le test d’appartenance avec `in`
* permet l’itération (une vue est itérable)

```{code-cell} ipython3
:cell_style: split

clefs = d.keys()
clefs
```

```{code-cell} ipython3
:cell_style: split

d['eve'] = 100
d
```

```{code-cell} ipython3
:cell_style: split

clefs
```

+++ {"slideshow": {"slide_type": "slide"}}

### méthodes sur les dictionnaires - épilogue

+++

* comme pour toutes les autres types de base de Python
* la librairie contient **beaucoup** d'autres méthodes
* il faut aller chercher dans la doc en ligne
* https://docs.python.org/3/tutorial/datastructures.html#dictionaries

+++ {"slideshow": {"slide_type": "slide"}}

### ordre des éléments dans un dictionnaire

+++

##### remarque d'ordre historique

* dans les versions avant 3.5, un dictionnaire ne préservait pas l'ordre
  * ce qui est logique par rapport à la technologie de hachage
  * mais peut être déroutant pour les débutants, - et les autres aussi parfois...
* depuis 3.6, l'**ordre de création** est préservé
  * i.e. c'est dans cet ordre que se font les itérations
