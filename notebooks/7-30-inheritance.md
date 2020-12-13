---
celltoolbar: Slideshow
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control
  encoding: '# -*- coding: utf-8 -*-'
  notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
notebookname: "h\xE9ritage"
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
</div>

<style>
.smaller {font-size: smaller}
</style>

+++ {"slideshow": {"slide_type": ""}}

# POO & héritage

+++ {"slideshow": {"slide_type": "slide"}}

## pour réutiliser du code en python

+++

* fonctions
  * pas d'état après exécution
* modules
  * garde l'état
  * une seule instance par programme
* **classes**
  * **instances multiples**
  * **chacune garde l'état**
  * **héritage**

+++ {"slideshow": {"slide_type": "slide"}}

### programmation orientée objet

pourquoi et comment ?

+++ {"cell_style": "split"}

#### deux objectifs

* modularité
* réutilisabilité

+++ {"cell_style": "split"}

#### deux moyens

* espaces de nom
* héritage

+++ {"slideshow": {"slide_type": "slide"}}

### modularité & réutilisabilité

+++ {"cell_style": "split"}

* du code modulaire
  * grouper le code dans une classe
  * grouper les données dans un objet

* plus on découpe en petits morceaux
  * plus on a de chances de pouvoir réutiliser

+++ {"cell_style": "split"}

* DRY *don't repeat yourself*
  * *cut'n paste is evil*
* code générique
  * ex: un simulateur fait "avancer" une collection d'objets
  * dès qu'un objet explique comment il avance
  * il peut faire partie de la simulation
* c'est là qu'intervient l'héritage

+++ {"slideshow": {"slide_type": "slide"}}

## espaces de nom

+++

* tous les objets qui sont
  * un package
  * un module
  * une classe
  * une instance (sauf des classes *builtin*)
* constituent chacun **un espace de nom**
  * i.e. une association *attribut* → *objet*

+++ {"slideshow": {"slide_type": "slide"}}

### espaces de nom - pourquoi

+++

* permet de lever l'ambigüité en cas d'homonymie
  * si 2 modules utilisent tous les 2 une globale `truc`
  * elles peuvent coexister sans souci
* les espaces de nom sont imbriqués (*nested*)
  * ex. `package.module.classe.methode`
* on peut accéder à tous les objets
  * dès qu'on sait le faire partir d'une variable
  * par exemple un module importé
* l'héritage rend cela dynamique
  * i.e. la résolution des attributs **est faite à *runtime***

+++ {"slideshow": {"slide_type": "slide"}}

### espaces de nom - variables et attributs

+++ {"cell_style": "split"}

#### deux mondes étanches

* variables
* attributs

+++ {"cell_style": "split"}

#### se mélangent

* apparemment seulement
* apprenez à bien lire

+++

typiquement dans une expression comme `a.b.c.d`

+++ {"cell_style": "split"}

* `a` est une **variable**

+++ {"cell_style": "split"}

* `b`, `c` et `d` sont des **attributs**

+++ {"slideshow": {"slide_type": "slide"}}

#### variables statiques / attributs dynamiques

+++ {"cell_style": "split", "slideshow": {"slide_type": ""}}

##### résolution des **variables**

* entièrement **lexical**
* en remontant dans le code
* avec les règles LEGB  
  local, englobant, global, *builtin*

+++ {"cell_style": "split", "slideshow": {"slide_type": ""}}

##### résolution des **attributs**

* dans le monde des **objets**
* en remontant les espaces de nom
* essentiellement **dynamique**  
  *i.e.* à *runtime*

+++ {"cell_style": "center", "slideshow": {"slide_type": ""}}

*par ex* dans `a.b.c.d`

* la variable `a` est identifiée lexicalement  
  (variable locale, paramètre de fonction,  
   souvenez-vous par exemple des clôtures)
* la variable référence un objet
* `b` est cherché comme un attribut à partir de cet objet

+++ {"slideshow": {"slide_type": "slide"}}

## résolution d'attribut

+++ {"slideshow": {"slide_type": ""}}

* la **résolution des attributs**
* fournit la **mécanique de base** de la POO
* et sous-tend notamment (mais pas que)  
  la mécanique de l'héritage

+++ {"slideshow": {"slide_type": "slide"}}

### ex: une classe et une instance

```{code-cell} ipython3
:cell_style: split

# une classe sans heritage
# et juste un constructeur
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

```{code-cell} ipython3
:cell_style: split

# comme toujours, la classe 
# est une usine à objets

point = Point(2, 3)
point.x
```

+++ {"slideshow": {"slide_type": "slide"}}

### 2 espaces de nommage

+++ {"cell_style": "split"}

**à ce stade nous avons deux espaces de nom**

* la classe `Point`
  * `Point.__init__` : la méthode
* l'instance
  * `point.x` : 2 pour cette instance
  * `point.y`

```{code-cell} ipython3
:cell_style: split

# on va voir ça
# dans pythontutor
%load_ext ipythontutor
```

+++ {"slideshow": {"slide_type": "slide"}}

**la classe et l'instance: deux espaces de nom distinct**

```{code-cell} ipython3
%%ipythontutor width=1000 height=450

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

point = Point(2, 3)
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### digression : l'attribut spécial `__dict__`

+++ {"slideshow": {"slide_type": ""}, "tags": ["level_intermediate"], "cell_style": "split"}

les (objets qui sont des) espaces de nom

* ont un **attribut spécial**
* qui s'appelle `__dict__`
* qui permet d'inspecter un espace de nom

ce n'est pas une notion à retenir,  
mais on va s'en servir dans la suite  
pour regarder le contenu des espaces de nom

```{code-cell} ipython3
:cell_style: split
:tags: [level_intermediate]

# quand on n'a pas pythontutor
# on peut simplement regarder __dict__

point.__dict__
```

+++ {"slideshow": {"slide_type": "slide"}}

### deux espaces de nom (classe et instance) - fin

+++

on l'a bien vu sous pythontutor, mais redisons les choses

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
# la classe possède
# l'attribut '__init__'
'__init__' in Point.__dict__
```

```{code-cell} ipython3
:cell_style: split

# c'est la méthode
# qu'on a définie
type(Point.__init__)
```

```{code-cell} ipython3
:cell_style: split

# par contre elle ne possède
# pas d'attribut x
'x' in Point.__dict__
```

```{code-cell} ipython3
:cell_style: split

# l'attribut x se trouve
# bien dans l'espace de nom
# de l'instance
'x' in point.__dict__
```

+++ {"slideshow": {"slide_type": "slide"}}

### recherche de bas en haut

+++

**pour la lecture :**  
la règle pour chercher un attribut en partant d'un objet consiste à

* le chercher dans l'espace de nom de l'objet lui-même
* sinon dans l'espace de nom de sa classe
* sinon dans les super-classes
* on verra les détails plus loin

+++ {"slideshow": {"slide_type": "slide"}}

## ex. de résolution d'attribut

```{code-cell} ipython3
:cell_style: split

# cas simple sans héritage
# appel d'une méthode
import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return math.sqrt(
            self.x**2 + self.y**2)
```

```{code-cell} ipython3
:cell_style: split

# quand on cherche vector.length
# on cherche
# 1. dans vector - pas trouvé
# 2. dans Vector - bingo

vector = Vector(3, 4)
vector.length()
```

+++ {"cell_style": "split"}

voyons ça en détail..

+++ {"slideshow": {"slide_type": "slide"}}

### espaces de nom

+++ {"cell_style": "split", "slideshow": {"slide_type": ""}}

* la classe `Vector` a les attributs
  * `__init__`
  * `length`

+++ {"cell_style": "split", "slideshow": {"slide_type": ""}}

* l'objet `vector` a les attributs
  * `x` et `y`,
  * mais pas `length` !

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
%%ipythontutor width=1000 height=400 curInstr=7
import math
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

vector = Vector(2, 2)
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

pour visualiser la même chose à base d'introspection dans le code

(rappel : tous les espaces de nom ont un attribut `__dict__`)

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
tags: [level_intermediate]
---
# les attributs 'intéressants' de Vector
[att for att in Vector.__dict__ if '__' not in att or att == '__init__']
```

```{code-cell} ipython3
:tags: [level_intermediate]

# et dans l'instance
list(vector.__dict__)
```

+++ {"slideshow": {"slide_type": "slide"}}

### exemple avec héritage

+++ {"slideshow": {"slide_type": ""}}

* jusqu'ici on n'a pas encore de l'héritage  
  puisque pour l'instant on n'a qu'une classe
* mais l'héritage  
  est une **simple prolongation** de cette logique

```{code-cell} ipython3
# une classe fille sans aucun contenu
class SubVector(Vector):
    pass

subvector = SubVector(6, 8)

# comment fait-on pour trouver subvector.length ?
subvector.length()
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
%%ipythontutor width=1000 height=400 curInstr=8
import math
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
class SubVector(Vector):
    pass

subvector = SubVector(6, 8)
```

+++ {"slideshow": {"slide_type": "slide"}}

* c'est exactement le même mécanisme qui est à l'oeuvre :
* quand on va vouloir appeler `subvector.length()`
  * on cherche l'attribut `length` dans l'instance : non
  * dans la classe : non
  * dans la super-classe : ok, on prend ça

+++ {"slideshow": {"slide_type": "slide"}}

## **remarque importante** : lecture ≠ écriture

+++ {"slideshow": {"slide_type": ""}}

* le mécanisme de recherche d'attribut qu'on vient de voir
* ne fonctionne que **pour la lecture des attributs**
* quand on **écrit** un attribut dans un objet,  
  c'est un mécanisme différent (slide suivant)

```{code-cell} ipython3
:cell_style: split

# quand on évalue un attribut en lecture
# on recherche en partant de l'objet
# et donc ici on trouve la méthode
# dans l'espace de noms de la super-classe
subvector.length()
```

```{code-cell} ipython3
:cell_style: split

# mais quand on écrit un attribut
# c'est une autre histoire complètement
# l'attribut est créé directement dans l'objet
subvector.foo = 12

'foo' in subvector.__dict__
```

+++ {"slideshow": {"slide_type": "slide"}}

### lecture ≠ écriture - discussion

* mais attention lorsqu'on **écrit** un attribut
  * *i.e.* si l'expression `foo.bar` est **à gauche** d'une affectation
* alors l'attribut `bar` est créé/écrit **dans l'objet `foo`**
* il n'y a **pas de recherche** dans ce cas !
* et heureusement d'ailleurs :  
  c'est le cas notamment à chaque fois qu'un constructeur fait  
  `self.name = name`

+++ {"slideshow": {"slide_type": ""}}

<div class=smaller>

* cela ne se remarque pas avec les méthodes
  * car c'est très rare d'écrire `instance.methode = ...`
* mais du coup, se souvenir que lire et écrire un attribut ne **sont pas symétriques**

</div>

+++ {"slideshow": {"slide_type": "slide"}}

### lecture *vs* écriture

+++ {"cell_style": "split"}

* il y a écriture si  
  et seulement si il y a **affectation**
* dans 1. il y a
  * **lecture** de l'attribut `liste`
  * même si on modifie l'objet
* dans 2. il y a
  * **écriture de l'attribut**
  * donc écrit dans (l'espace de nom) `obj`

+++ {"cell_style": "split"}

* 1. lecture !

```python
obj.liste.append('foo')
```

* 2. écriture

```python
obj.liste += ['foo']
```

+++ {"slideshow": {"slide_type": "slide"}}

## héritage

+++ {"slideshow": {"slide_type": ""}, "cell_style": "split"}

* une classe peut hériter d’une (ou plusieurs) autre classes
* si A hérite de B
  * on dit que A est la sous-classe de B
  * et B est la super-classe de A
* la sous-classe hérite des attributs de sa super-classe
* l’instance hérite de la classe qui la crée

```{code-cell} ipython3
:cell_style: split
:tags: [raises-exception]

# la syntaxe est
class Class(Super):
    pass

# ou 
class Class(Super1, Super2):
    pass
```

+++ {"slideshow": {"slide_type": "slide"}}

### graphe d'héritage

* on peut donc construire un graphe d’héritage
* allant des super-classes aux instances

+++ {"cell_style": "split"}

![arbre de classes](media/classes.png)

```{code-cell} ipython3
:cell_style: split

class C1:
    pass
class C2:
    pass
class C(C1, C2):
    def func(self, x):
        self.x = 10
o1 = C()
o2 = C()
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### recherche dans l’arbre d’héritage

+++ {"tags": ["level_intermediate"]}

* MRO : method resolution order
* l’algorithme est le suivant
  * liste toutes les super-classes en utilisant  
    un algorithme DFLR (depth first, left to right)

  * si classe dupliquée,  
    **ne garder que la dernière** occurrence

+++ {"cell_style": "split", "slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

![MRO](media/mro.png)

```{code-cell} ipython3
:cell_style: split
:tags: [level_intermediate]

class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
```

+++ {"tags": ["level_intermediate"]}

* parcours DFLR: `D`, `B`, `A`, `object`, `C`, `A`, `object`
* suppressions : `D`, `B`, ~~`A`~~, ~~`object`~~, `C`, `A`, `object`

+++ {"slideshow": {"slide_type": "slide"}}

## `isinstance()` et `issubclass()`

+++

* `isinstance(x, class1)` retourne `True` si `x` est une instance de `class1` ou d’une super classe
* `issubclass(class1, class2)` retourne `True` si `class1` est une sous-classe de `class2`
* ces fonctions *builtin* sont à privilégier par rapport à l'utilisation de `type()`

```{code-cell} ipython3
:cell_style: split

# A est la superclasse de B
a, b = A(), B()
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
isinstance(a, A), isinstance(b, B)
```

```{code-cell} ipython3
:cell_style: split

# bien sûr NON
isinstance(a, B)
```

```{code-cell} ipython3
:cell_style: split

# OUI, et NON
isinstance(b, A), type(b) is A
```

```{code-cell} ipython3
:cell_style: split

issubclass(B, A)
```

```{code-cell} ipython3
:cell_style: split

isinstance(B, A)
```

+++ {"tags": [], "slideshow": {"slide_type": "slide"}}

## attributs de classe

+++

dans (l'espace de nom d')une classe, on peut mettre 

* des méthodes (on le savait) 
* et aussi attributs *normaux* - qui référencent des données

rien de nouveau point de vue syntaxe : 

* on écrit juste la déclaration dans la classe,
* au même niveau d'imbrication que les méthodes

voyons cela sur un exemple

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: slide
tags: []
---
class Factory:
    # un compteur global à la classe
    # dans lequel on va pouvoir mémoriser 
    # tous les labels de toutes les instances
    all_labels = []

    def __init__(self, label):
        self.label = label
        Factory.all_labels.append(label)
        # on aurait pu écrire
        # self.all_labels.append(label)
        # mais c'est dangereux (voir suite)


Factory.all_labels
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
tags: []
---
f1 = Factory('premier')
Factory.all_labels
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
tags: []
---
f2 = Factory('second')
Factory.all_labels
```

```{code-cell} ipython3
# on trouve le même objet quel que soit l'endroit d'où on part
f1.all_labels is f2.all_labels is Factory.all_labels
```

```{code-cell} ipython3
---
cell_style: center
slideshow:
  slide_type: slide
tags: [level_advanced]
---
%%ipythontutor width=1000 height=400
class Factory:
    all_labels = []
    def __init__(self, label):
        self.label = label
        # ça marche aussi, mais ATTENTION
        self.all_labels.append(label)
f1 = Factory('premier')
f2 = Factory('second')
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
tags: [level_advanced]
---
%%ipythontutor width=1000 height=400 curInstr=1
class Factory:
    all_labels = []

    def __init__(self, label):
        self.label = label
        # cette forme ne fonctionne pas comme attendu
        # parce que à droite d'une affectation
        self.all_labels = self.all_labels + [label]

f1 = Factory('premier')
f2 = Factory('second')
```

+++ {"slideshow": {"slide_type": "slide"}}

## `super()`

+++

* utile lorsque la spécialisation  
  consiste à ajouter ou modifier  
  par rapport à la classe mère

* le cas typique est d'ailleurs le constructeur  
  dès qu'on ajoute un attribut de donnée

* permet de ne pas mentionner explicitement
  le nom de la classe mère (code + générique)

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: slide
---
# illustration de super() 
# dans le constructeur

class C:
    def __init__(self, x):
        print("init x par superclasse")
        self.x = x

class D(C):

    def __init__(self, x, y):
        # initialiser : la classe C
        super().__init__(x)
        print("init y par classe")
        self.y = y
```

```{code-cell} ipython3
:cell_style: split

c = C(10)
```

```{code-cell} ipython3
:cell_style: split

d = D(100, 200)
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: slide
---
# super() est souvent rencontrée
# dans __init__ mais s'applique
# partout
class C:
    def f(self):
        print('spam')
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
class D(C):
    def f(self):
        # remarquez l'absence
        # de self !
        super().f()
        print('beans')
```

```{code-cell} ipython3
:cell_style: split

c = C(); c.f()
```

```{code-cell} ipython3
:cell_style: split

d = D(); d.f()
```

+++ {"slideshow": {"slide_type": "slide"}}

## résumé

* les instances et classes sont des objets mutables (sauf classes *builtin*)
* on utilise `isinstance()` pour tester le type d'un objet
* chaque instance et chaque classe est un espace de nom
* lorsqu'on écrit un attribut, on écrit directement dans l'espace de nom de cet objet
* en lecture, on résoud la référence d'un attribut de bas en haut
* en général
  * les classes ont des attributs de type méthode
  * les objets ont des attributs de type donnée
  * mais le modèle est flexible
* une méthode peut faire référence à la super-classe avec `super()`
