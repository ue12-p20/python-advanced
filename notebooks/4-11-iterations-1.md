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
  title: "les it\xE9rations en Python"
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

+++ {"slideshow": {"slide_type": "slide"}}

# les itérations en Python

+++

* la boucle `for` est la méthode **préférée**   
  pour itérer sur un ensemble de valeurs

* en général préférable au `while` en Python
  * on peut faire un `for` sur n'importe quel itérable
  * ce n'est pas le cas pour le `while`
  * avec `for` c'est l'itérable qui se charge de la logique
* de nombreuses techniques pour itérer de manière optimisée
  * compréhensions
  * itérateurs
  * expressions génératrices
  * générateurs (encore appelées fonctions génératrices)
  * (rappel : avec numpy, pas de `for`, programmation vectorielle)

+++ {"slideshow": {"slide_type": "slide"}}

## la boucle `for`

+++ {"slideshow": {"slide_type": ""}}

une instruction `for` ressemble à ceci :

```python
for item in iterable:
    bloc
    aligné
    d_instructions
```

+++ {"slideshow": {"slide_type": "slide"}}

### `break` et `continue`

+++

comme dans beaucoup d'autres langages :

* `break` sort complètement de la boucle
* `continue` termine abruptement l'itération courante et passe à la suivante
* on parle toujours de la boucle **la plus imbriquée**

l'instruction `else` attachée à un `for` est d'un usage plutôt rare en pratique

+++ {"slideshow": {"slide_type": "slide"}}

### `for .. else`

+++ {"slideshow": {"slide_type": ""}}

en fait la forme générale de la boucle `for` c'est


```python
for item in iterable:
    bloc
    aligné
else:
    bloc     # exécuté lorsque la boucle sort "proprement"
    aligné   # c'est-à-dire pas avec un break
```

mais c'est d'un usage assez rare

+++ {"slideshow": {"slide_type": "slide"}}

### ~~`for i in range(len(truc))`~~

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
liste = [10, 20, 40, 80, 120]

# la bonne façon de faire un for

for item in liste:
    print(item, end=" ")
```

```{code-cell} ipython3
:cell_style: split

# et **non pas** cette
# horrible périphrase !

for i in range(len(liste)):
    item = liste[i]
    print(item, end=" ")
```

+++ {"cell_style": "center", "tags": ["level_advanced"]}

* voir [une revue de code intéressante ici](http://sametmax.com/revue-de-code-publique/)

+++ {"slideshow": {"slide_type": "slide"}}

### boucle `for` sur un dictionnaire

+++

* on peut facilement itérer sur un dictionnaire
* mais il faut choisir si on veut le faire 
  * sur les clés,
  * sur les valeurs,
  * ou sur les deux
* c'est à ça que servent les méthodes
  * `keys()`
  * `values()`
  * `items()`

+++ {"slideshow": {"slide_type": "slide"}}

#### boucle `for` sur un dictionnaire

```{code-cell} ipython3
:cell_style: split

agenda = {
    'paul': 12, 
    'pierre': 14,
    'jean': 16,
}
```

```{code-cell} ipython3
:cell_style: split

# l'unpacking permet d'écrire 
# un code élégant
for key, value in agenda.items():
    print(f"{key} → {value}")
```

---

```{code-cell} ipython3
:cell_style: split

# un raccourci
for key in agenda:      # ou agenda.keys()
    print(key, end=" ")
```

```{code-cell} ipython3
:cell_style: split

for value in agenda.values():
    print(value, end=" ")
```

+++ {"slideshow": {"slide_type": "slide"}}

### exemple de boucle

```{code-cell} ipython3
# pour illustrer break, et for .. else


# boucle (1)
for p in range(2, 10):
    # boucle (2)
    for i in range(2, p):
        if p % i == 0:
            print(f"{p} = {i} x {p//i}")
            # on sort de la boucle (2)
            break
    else:
        print(f"{p} est un nombre premier")
```

+++ {"slideshow": {"slide_type": "slide"}}

### boucles `for` : limite importante

+++

* **règle très importante:** à l'intérieur d'une boucle
* il ne faut **pas modifier l’objet** sur lequel on itère
* on peut, par contre, en faire une copie

+++ {"cell_style": "split"}

ce code-ci provoquerait une boucle infinie
```
L = ['a', 'b', 'c']
for i in L:
    if i == 'c':
        L.append(i)
```

```{code-cell} ipython3
:cell_style: split

# il suffit de prendre la précaution
# de faire une (shallow) copie
L = ['a', 'b' , 'c']
for i in L[:]:
    if i == 'c':
        L.append(i)
L
```

+++ {"slideshow": {"slide_type": "slide"}}

### boucles pythoniques ou pas

+++

#### soyez explicite

```{code-cell} ipython3
:cell_style: split

D = {
    'alice': 35,
    'bob': 9,
    'charlie': 6,
}

# pas pythonique (implicite)
for t in D.items():         
    print(t[0], t[1])
```

```{code-cell} ipython3
:cell_style: split

# pythonique (explicite)

for nom, age in D.items():
    print(nom, age)
```

+++ {"slideshow": {"slide_type": "slide"}}

## itérables et itérateurs

+++ {"slideshow": {"slide_type": ""}}

### c'est quoi un itérable ?

* par définition, c'est un objet .. sur lequel on peut faire un `for`
* notamment avec les séquences natives : chaînes, listes, tuples, ensembles
* et aussi dictionnaires, et des tas d'autres objets, mais patience

```{code-cell} ipython3
:cell_style: split

# une chaine est un itérable

chaine = "un été"
for char in chaine:
    print(char, end=" ")
```

```{code-cell} ipython3
:cell_style: split

# un ensemble aussi

ensemble = {10, 40, 80} 
for element in ensemble:
    print(element, end=" ")
```

+++ {"slideshow": {"slide_type": "slide"}}

#### la boucle `for`, mais pas que

+++ {"cell_style": "split"}

* on a défini les itérables par rapport à la boucle `for` 
* mais plusieurs fonctions acceptent en argument des itérables
* `sum`, `max`, `min`
* `map`, `filter`
* etc...

```{code-cell} ipython3
:cell_style: split

L = [20, 34, 57, 2, 25]

min(L), sum(L)
```

+++ {"slideshow": {"slide_type": "slide"}}

### itérateurs

* les **itérateurs** sont une sous-famille des itérables
* qui présentent la particularité de **consommer peu de mémoire**
* en fait un objet itérateur capture uniquement  
  **la logique de l'itération**, mais pas les données
* c'est-à-dire où on en est, et comment passer au suivant

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
import sys

# l'exemple le plus simple 
# d'itérateur est range()
R = range(1000)
sys.getsizeof(R)
```

```{code-cell} ipython3
:cell_style: split

L = list(R)
sys.getsizeof(L)
```

+++ {"cell_style": "split", "slideshow": {"slide_type": "slide"}}

cette boucle Python
```python
for i in range(100_000):
    # do stuff
```

+++ {"cell_style": "split"}

est comparable à ceci en C
```C
for (int i=0; i<100000; i++) {
    /* do stuff */
}
```

+++ {"slideshow": {"slide_type": ""}}

on ne veut **pas devoir allouer** une liste de 100.000 éléments  
juste pour pouvoir faire cette boucle

+++ {"slideshow": {"slide_type": "slide"}}

### création d'itérateurs

+++

Python propose des outils pour **créer** et **combiner** les itérables:

* fonctions natives *builtin* qui créent des itérateurs:
  * `range`, `enumerate`, et `zip`
* dans un module dédié `itertools`:
  * `chain`, `cycle`, `islice`, ...

+++ {"slideshow": {"slide_type": "slide"}}

### `range`

+++

* `range` crée un itérateur qui itère sur un intervalle de nombres entiers
* arguments : même logique que le slicing
  * début (inclus), fin (exclus), pas
  * **sauf** (curiosité) : si un seul argument, c'est **la fin**

```{code-cell} ipython3
:cell_style: split

# les nombres pairs de 10 à 20
for i in range(10, 21, 2):
    print(i, end=" ")
```

```{code-cell} ipython3
:cell_style: split

# le début par défaut est 0
for i in range(5):
    print(i, end=" ")
```

+++ {"slideshow": {"slide_type": "slide"}}

### un `range` n'est **pas une liste**

+++

* l'objet retourné par `range` **n'est pas une liste**
* au contraire il crée un objet tout petit, un **itérateur**
* qui contient seulement la logique de l'itération
* la preuve:

```{code-cell} ipython3
:cell_style: split

# 10**20 c'est 100 millions de Tera

iterateur = range(10**20)
iterateur
```

```{code-cell} ipython3
:cell_style: split

for item in iterateur:
    if item >= 5:
        break
    print(item, end=" ")
```

+++ {"slideshow": {"slide_type": "slide"}}

**exercice**: comment créer **une vraie liste** des entiers de 1 à 10 ?

+++ {"slideshow": {"slide_type": "fragment"}}

**réponse** avec

```python
list(range(1, 11))
```

où le type `list` se comporte, comme tous les types, comme une usine à fabriquer des listes

+++ {"slideshow": {"slide_type": "slide"}}

### `count` : un itérateur infini

+++ {"slideshow": {"slide_type": ""}}

du coup un itérateur peut même .. ne jamais terminer :

```{code-cell} ipython3
# count fait partie du module itertools
from itertools import count
count?
```

```{code-cell} ipython3
# si on n'arrête pas la boucle nous mêmes
# ce fragment va boucler sans fin

for i in count():
    print(i, end=" ")
    if i >= 5:
        break
```

+++ {"slideshow": {"slide_type": "slide"}}

### `enumerate`

+++ {"cell_style": "split"}

on a dit qu'on ne faisait jamais

```python
for i in range(len(liste)):
    item = liste[i]
    print(item, end=" ")
```

+++ {"cell_style": "split"}

comment faire alors si on a vraiment besoin de l'index `i` ?

→ il suffit d'utiliser la *builtin* `enumerate()`

```{code-cell} ipython3
:cell_style: center

L = [1, 10, 100, 1000]
```

```{code-cell} ipython3
:cell_style: center

for i, item in enumerate(L):
    print(f"{i}: {item}")
```

+++ {"slideshow": {"slide_type": "slide"}}

![](media/iter-enumerate.png)

+++ {"slideshow": {"slide_type": "slide"}}

#### `enumerate()` ...

+++

* typiquement utile sur un fichier
* pour avoir le numéro de ligne 
* remarquez le deuxième argument de `enumerate` pour commencer à 1

```{code-cell} ipython3
with open("data/une-charogne.txt") as feed:
    for lineno, line in enumerate(feed, 1):
        print(f"{lineno}:{line}", end="")
```

+++ {"slideshow": {"slide_type": "slide"}}

### `zip`

+++

`zip` fonctionne un peu comme `enumerate` mais entre deux itérables:

![](media/iter-zip.png)

+++ {"slideshow": {"slide_type": "slide"}}

#### `zip`

```{code-cell} ipython3
:cell_style: split

liste1 = [10, 20, 30]
liste2 = [100, 200, 300]
```

```{code-cell} ipython3
:cell_style: split

for a, b in zip(liste1, liste2):
    print(f"{a}x{b}", end=" ")
```

**NOTES**: 

* `zip` fonctionne avec autant d'arguments qu'on veut
* elle s'arrête dès que l'entrée la plus courte est épuisée

+++ {"slideshow": {"slide_type": "slide"}}

### `enumerate = zip + count`

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
# par exemple on peut récrire enumerate
# à base de zip et count
L
```

```{code-cell} ipython3
:cell_style: split

# zip s'arrête dès que 
# l'un de ses morceaux s'arrête
for index, item in zip(count(), L):
    print(f"{index} {item}")
```

+++ {"cell_style": "split"}

![](media/iter-zip-count.png)

+++ {"slideshow": {"slide_type": "slide"}}

### un itérateur s'épuise

**ATTENTION** il y a toutefois une limite lorsqu'on utilise un itérateur 

* une fois que l'itérateur est arrivé à sa fin
* il est "épuisé" et on ne peut plus boucler dessus

```{code-cell} ipython3
:cell_style: split

L = [1, 2]

print('pass 1')
for i in L:
    print(i)

print('pass 2')
for i in L:
    print(i)
    
```

```{code-cell} ipython3
:cell_style: split

# iter() permet de construire
# un itérateur sur un itérable
R = iter(L)

print('pass 1')
for i in R:
    print(i)

print('pass 2')
for i in R:
    print(i)    
```

+++ {"slideshow": {"slide_type": "slide"}}

du coup par exemple,  
**ne pas essayer d'itérer deux fois** sur un `zip()` ou un `enumerate()`

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
Z = zip(range(3), range(4, 7))

print('pass 1')
for a, b in Z:
    print(a, b)
    
print('pass 2')
for a, b in Z:
    print(a, b)    
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
E = enumerate(L)

print('pass 1')
for a, b in E:
    print(a, b)
    
print('pass 2')
for a, b in E:
    print(a, b)    
```

**NB** il suffit de faire e.g. `for a, b in enumerate(L)` pour se débarrasser du problème

+++ {"slideshow": {"slide_type": "slide"}}

## le module `itertools` - assemblage d'itérables

+++

on trouve dans le module `itertools` plusieurs utilitaires très pratiques :

* `count` pour énumérer les entiers (un `range` sans borne)
* `chain` pour chainer plusieurs itérables
* `cycle` pour rejouer un itérable en boucle
* `repeat` pour énumérer plusieurs fois le même objet
* `islice` pour n'énumérer que certains morceaux
* `zip_longest` fonctionne comme `zip` mais s'arrête au morceau le plus long

+++ {"slideshow": {"slide_type": "slide"}}

### `chain`, `cycle` et `repeat`

```{code-cell} ipython3
---
cell_style: center
slideshow:
  slide_type: ''
---
from itertools import chain, cycle, repeat
data1 = (10, 20, 30)
data2 = (100, 200, 300)
```

```{code-cell} ipython3
:cell_style: center

# chain()
for i, d in enumerate(chain(data1, data2)):
    print(f"{i}x{d}", end=" ")
```

```{code-cell} ipython3
# cycle() ne termine jamais non plus

for i, d in enumerate(cycle(data1)):
    print(f"{i}x{d}", end=" ")
    if i >= 10:
        break
```

```{code-cell} ipython3
# repeat()
padding = repeat(1000, 3)

for i, d in enumerate(chain(data1, padding, data2)):
    print(f"{i}x{d}", end=" ")
```

+++ {"slideshow": {"slide_type": "slide"}}

### `islice`

```{code-cell} ipython3
:cell_style: split

# avec islice on peut par exemple 
# sauter une ligne sur deux dans un fichier
from pathlib import Path

# on crée un fichier 
with Path('islice.txt').open('w') as f:
    for i in range(6):
        f.write(f"{i}**2 = {i**2}\n")
```

```{code-cell} ipython3
:cell_style: split

# pour ne relire qu'une ligne sur deux

from itertools import islice

with Path('islice.txt').open() as f:
    for line in islice(f, 0, None, 2):
        print(line, end="")
```

```{code-cell} ipython3
:cell_style: split

# ou zapper les 3 premières

from itertools import islice

with Path('islice.txt').open() as f:
    for line in islice(f, 3, None):
        print(line, end="")
```

```{code-cell} ipython3
:cell_style: split

# ou ne garder que les 3 premières

from itertools import islice

with Path('islice.txt').open() as f:
    for line in islice(f, 3):
        print(line, end="")
```

```{raw-cell}
---
slideshow:
  slide_type: slide
---
### `zip_longest()`
```

```{code-cell} ipython3
:cell_style: split

from itertools import zip_longest
for i, d in zip_longest(
        range(6), L, fillvalue='X'):
    print(f"{i} {d}")
```

+++ {"cell_style": "split"}

![](media/iter-zip-longest.png)

+++ {"slideshow": {"slide_type": "slide"}}

### `itertools` & combinatoires

+++

Le module `itertools` propose aussi quelques combinatoires usuelles:

* `product`: produit cartésien de deux itérables
* `permutations`: les permutations ($n!$)
* `combinations`: *p parmi n*
* et d'autres... 
* https://docs.python.org/3/library/itertools.html

+++ {"slideshow": {"slide_type": "slide"}}

#### exemple avec `product`

```{code-cell} ipython3
from itertools import product

dim1 = (1, 2, 3)
dim2 = '♡♢♤'

for i, (d1, d2) in enumerate(product(dim1, dim2), 1):
    print(f"i={i}, d1={d1} d2={d2}")
```

+++ {"slideshow": {"slide_type": "slide"}}

**exercices** (voir notebook séparé)

* vigenere

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

## sous le capot

+++

### comment marche la boucle `for`

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

+++ {"slideshow": {"slide_type": "slide"}}

voici un équivalent approximatif

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
# cette boucle for 

for item in iterable:
    print(item)
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
# est en gros équivalente
# à ce fragment

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

pour savoir si un objet est un itérateur  
tester si  
  `iter(obj) is obj`

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
def is_iterator(obj):
    return iter(obj) is obj
```

+++ {"slideshow": {"slide_type": "slide"}}

### par exemple

* une liste **n'est pas** son propre itérateur
* un fichier **est** son propre itérateur

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: slide
---
# un fichier est son propre itérateur
with open("data/une-charogne.txt") as F:
    print(f"{is_iterator(F)=}")
```

```{code-cell} ipython3
:cell_style: split

# la liste non
L = list(range(5))
print(f"{is_iterator(L)=}")
```

```{code-cell} ipython3
:cell_style: split

# cycle en est un
C = cycle(L)
print(f"{is_iterator(C)=}")
```

```{code-cell} ipython3
:cell_style: split

# un zip() est un itérateur
Z = zip(L, L)
print(f"{is_iterator(Z)=}")
```

* Bien se souvenir : **un itérateur s'épuise**  
  de manière générale, un objet qui est un itérateur  
  ne peut être itéré qu'une seule fois
