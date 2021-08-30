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
  title: containers (1/2)
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

# les containers (1/2)

+++ {"slideshow": {"slide_type": "slide"}, "tags": []}

## les listes

+++

* permet de créer une liste de n’importe quels objets
  * techniquement, c’est un tableau de pointeurs vers les objets
  * les listes sont dynamiques, de taille variable
  * comme une liste est un objet, on peut avoir une liste de listes

+++ {"slideshow": {"slide_type": "slide"}}

### les listes

```{code-cell} ipython3
:cell_style: split

L = []
L = [4, 'bob', 10 + 1j, True]
```

```{code-cell} ipython3
:cell_style: split

L
```

```{code-cell} ipython3
:cell_style: split

# les indices en python
# commencent à 0
L[2]
```

```{code-cell} ipython3
:cell_style: split

L[0] = 10
```

```{code-cell} ipython3
:cell_style: split

L
```

+++ {"slideshow": {"slide_type": "slide"}}

### modification des listes

```{code-cell} ipython3
:cell_style: split

L
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
L[2:]
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
L[2:] = [6, 7, 8, 'alice']
L
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
L[1:4] = []
L
```

+++ {"slideshow": {"slide_type": "slide"}}

#### attention

+++ {"slideshow": {"slide_type": ""}}

* `L[i] = L2`
  * **remplace** le i-ème élément de `L` par la liste `L2`
* `L[i:j] = L2`
  * **insère** tous les éléments de la liste `L2` à la position `i`
  * après avoir supprimé les éléments `i` jusqu’à `j-1` dans `L`

+++ {"slideshow": {"slide_type": "slide"}}

#### modification des listes...

```{code-cell} ipython3
:cell_style: split

L = [1, 2, 3, 4, 5]
L
```

```{code-cell} ipython3
:cell_style: split

L[2:4] = [10, 11, 12]
L
```

```{code-cell} ipython3
L[3] = [3, 4]
L
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
%load_ext ipythontutor
```

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
%%ipythontutor curInstr=1 width=800
L = [1, 2, 3, 4, 5]
L[2:4] = [10, 11, 12]
L[3] = [3, 4]
```

+++ {"slideshow": {"slide_type": "slide"}}

### méthodes sur les listes

+++

* toutes les méthodes sur les séquences
* optimisé pour les ajouts **à la fin** de la liste

```{code-cell} ipython3
:cell_style: split

L = []
for i in range(4):
    L.append(i)
```

```{code-cell} ipython3
:cell_style: split

while L:
    print(L.pop())
```

si nécessaire, envisager la liste **doublement chainée**

```{code-cell} ipython3
from collections import deque
deque?
```

+++ {"slideshow": {"slide_type": "slide"}}

#### méthodes sur les listes...

+++

* des méthodes spécifiques aux types mutables  
  (modifications *in-place*)

  * `L.append(x)` ajoute `x` à la fin de `L`
  * `L.extend(L2)` ajoute chaque élément de `L2` à la fin de `L`
  * `L.insert(i, x)` ajoute x à la position `i`
  * `L.sort()`  trie `L`
  * `L.reverse()` renverse les éléments de `L`

+++ {"slideshow": {"slide_type": "slide"}}

#### méthodes sur les listes...

+++

* `L.pop(i)` supprime l’élément à la position `i`, si i n’est pas fourni, supprime le dernier élément. La fonction retourne l’élément supprimé
  * utilisé pour faire une pile d’éléments
* `L.remove(x)` supprime la première occurrence de `x` dans `L`. S’il n’y a pas de `x`, une exception est retournée
* `del L[i:j:k]` supprime tous les éléments entre `i` et `j-1` par pas de `k` éléments
  * si `i == j` supprime l’élément `i`

+++ {"slideshow": {"slide_type": "slide"}}

### digression: `range()`

+++ {"cell_style": "center"}

* `range()` est une fonction *builtin* ou native
* qui retourne un objet **itérateur**
* c'est-à-dire sur lequel on peut faire un `for`
* on y reviendra longuement

```{code-cell} ipython3
:cell_style: center

for i in range(4):
    print(i, end=" ")
```

+++ {"slideshow": {"slide_type": "slide"}}

#### digression: `range()` ...

+++

* essentiellement, **même logique que le slicing**
* `range(j)` balaie de `0` à `j-1`
* `range(i, j)` balaie de `i` à `j-1`
* `range(i, j, k)` balaie de `i` à `j-1` par pas de `k`
* pour obtenir une liste on transforme (*cast*)  
  en liste en appelant `list()`

```{code-cell} ipython3
:cell_style: split

for i in range(1, 21, 5):
    print(i, end=" ")
```

```{code-cell} ipython3
:cell_style: split

list(range(1, 21, 5))
```

+++ {"slideshow": {"slide_type": "slide"}}

### méthodes sur les listes...

```{code-cell} ipython3
:cell_style: split

L = list(range(5))
L.append(100)
L
```

```{code-cell} ipython3
:cell_style: split

# comme si append(10)
#     puis append(20)
L.extend([10, 20])
L
```

```{code-cell} ipython3
:cell_style: split

L.remove(10)
L
```

```{code-cell} ipython3
:cell_style: split

L.sort()
L
```

+++ {"slideshow": {"slide_type": "slide"}}

### tri sur les listes

+++

* le tri des listes est très puissant en Python
  * tri **en place** méthode `list.sort()`
* il a aussi la fonction built-in `sorted()`  
  qui trie toutes les séquences

```{code-cell} ipython3
:cell_style: split

L = [10, -5, 3, 100]

# tri en place
L.sort()
L
```

```{code-cell} ipython3
:cell_style: split

L1 = [10, -5, 3, 100]

# crée une copie
L2 = sorted(L1)
print(L1)
print(L2)
```

* https://docs.python.org/3.5/howto/sorting.html

+++ {"slideshow": {"slide_type": "slide"}}

### avertissement sur les listes

+++ {"slideshow": {"slide_type": ""}}

* outil très très pratique
* **mais** parfois (souvent) pas nécessaire
* car nécessite de la mémoire
* alors qu'on veut juste itérer sur le contenu
* dans ce cas, techniques + adaptées : itérateurs et autres générateurs
* sujet avancé que l’on verra plus tard

+++ {"slideshow": {"slide_type": "slide"}}

## les tuples

+++

* comme des listes, mais **immutables**
* syntaxe: `()` au lieu de `[]`
* mais attention si un seul élément

```{code-cell} ipython3
:cell_style: split

# syntaxe pour un tuple vide
T = ()
T
```

```{code-cell} ipython3
:cell_style: split

# syntaxe pour un singleton
T1 = (4,)
# ou encore
T2 = 4,

T1 == T2
```

* **attention** `(4)` est un **entier** et `(4,)` est un **tuple**
* c'est la virgule qui est importante
* on peut omettre les `()` - la plupart du temps  
  (mais pas toujours malheureusement)

+++ {"slideshow": {"slide_type": "slide"}}

### les tuples

```{code-cell} ipython3
:cell_style: split

# syntaxe pour plusieurs éléments
T1 = (3, 5, 'alice', 10+1j)

# ou encore
T2 =  3, 5, 'alice', 10+1j

# ou encore
T3 =  3, 5, 'alice', 10+1j,
```

```{code-cell} ipython3
:cell_style: split

T1 == T2
```

```{code-cell} ipython3
:cell_style: split

T1 == T3
```

+++ {"slideshow": {"slide_type": "slide"}}

* un tuple est **non mutable**
* ce qui le rend hashable :  
  on **peut l'utiliser** dans un **ensemble**  
  ou comme clé dans un **dictionnaire**
* par contre bien sûr les fonctions faisant des modifications  
  *in-place* ne s’appliquent pas aux tuples

```{code-cell} ipython3
try: 
    T1[3] = 5   # python n'est pas content
except Exception as exc:
    print(f"OOPS {type(exc)} {exc}")
```
