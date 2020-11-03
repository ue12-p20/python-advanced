---
celltoolbar: Slideshow
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed
  formats: md:myst
  notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
notebookname: classes et objets
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

+++ {"slideshow": {"slide_type": ""}}

# classes : rappels (1)

+++ {"slideshow": {"slide_type": ""}}

les classes servent à définir **de nouveau types**  

* en sus des types prédéfinis `str`, `list`, `set`, `dict`, ...
* plus adaptés à l'application

+++ {"cell_style": "center", "slideshow": {"slide_type": "slide"}}

## `class` 

* avec le mot-clé `class` on définit **un nouveau type**  
* une classe définit des **méthodes spéciales**  
  ici **`__init__`** et **`__repr__`**

```{code-cell} ipython3
:cell_style: split

class User:

    # le constructeur
    def __init__(self, name, age):
        # un objet User a deux attributs
        # name et age
        self.name = name
        self.age = age

    # l'afficheur
    def __repr__(self):
        return f"{self.name}, {self.age} ans"
```

```{code-cell} ipython3
:cell_style: split

# une fois qu'on a défini une classe, 
# on peut s'en servir pour créer
# des objets - on dit des instances 
# de la classe

user1 = User("Lambert", 25)
user1
```

+++ {"slideshow": {"slide_type": "slide"}}

## une classe est un type

* comme tous les types, la classe est une **usine à objets**  
  * `user = User("Dupont", 59)`  
  * à rapprocher de `s = set()` ou `n = int('32')`
  
* chaque objet (on dit instance) contient des données 
  * rangées dans des **attributs** de l'objet
  * ici `name` et `age`

+++ {"slideshow": {"slide_type": "slide"}}

## affichage

* la méthode spéciale `__repr__(self)` doit renvoyer une chaine  
* elle est utilisée pour
  * imprimer l'objet avec `print()`
  * convertir un objet en chaine

```{code-cell} ipython3
:cell_style: center

print(f"je viens de voir {user1}")
```

```{code-cell} ipython3
:cell_style: center

str(user1)
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### affichage et conversion en chaine

+++ {"tags": ["level_intermediate"]}

en fait il est possible d'être plus fin, et de définir **deux** méthodes spéciales qui sont

* `__repr__(self)` et
* `__str__(self)` 

cela dit pour commencer on peut se contenter de ne définir que `__repr__()` qui est alors utilisée pour tous les usages

+++ {"slideshow": {"slide_type": "slide"}}

## méthodes

+++

* une classe peut définir **des méthodes**
* qui sont des fonctions qui s'appliquent sur un objet (de cette classe)

```{code-cell} ipython3
:cell_style: split

# une implémentation très simple
# d'une file FILO
# premier entré dernier sorti

class Stack:
    
    def __init__(self):
        self.frames = [] 
        
    def __repr__(self):
        return " > ".join(self.frames)            
    
    def push(self, item):
        self.frames.append(item)
        
    def pop(self):
        return self.frames.pop()
```

```{code-cell} ipython3
:cell_style: split

# instance
stack = Stack()

stack.push('fact(3)')
stack.push('fact(2)')
stack.push('fact(1)')

stack
```

```{code-cell} ipython3
:cell_style: split

stack.pop()
```

```{code-cell} ipython3
:cell_style: split

stack
```

+++ {"cell_style": "center", "slideshow": {"slide_type": "slide"}}

## méthodes et paramètres

remarquez qu'ici 

* on a défini la méthode `push` avec **2** paramètres  
```
def push(self, item):
```

* ce qui fait qu'on peut l'appeler sur un objet avec **1** paramètre 
```
stack.push(some_item)
```

* car le premier paramètre `self` est lié  
  à **l'objet sur lequel on envoie** la méthode

* et la phrase `stack.push(some_item)`  
  est en fait équivalente à 
  `Stack.push(stack, some_item)`

+++ {"slideshow": {"slide_type": "slide"}}

## intérêts de cette approche

+++

* définir vos propres types de données
* grouper les données qui vont ensemble dans un  
  objet unique, facile à passer à d'autres fonctions
* invariants: garantir de bonnes propriétés 
  si on utilise les objets au travers des méthodes 

et aussi (sera vu ultérieurement)

* héritage 
  * réutiliser une classe en modifiant  
    seulement quelques aspects
* intégrer les objets dans le langage  
  i.e. donner un sens à des constructions comme  
  * `x in obj`
  * `obj[x]`
  * `if obj:`
  * `for item in obj:`
  * ...

+++ {"slideshow": {"slide_type": "slide"}}

## exemples

+++ {"slideshow": {"slide_type": "slide"}}

### exemple : `np.ndarray`

* c'est une classe que vous utilisez tous les jours !
* en fait il n'y a pas de différence de fond 
  * entre les types prédéfinis (`str`, ...)
  * et les classes créées avec `class`

+++ {"slideshow": {"slide_type": "slide"}}

### exemple : `class Point`

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
import math

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x:.2f} x {self.y:.2f})"
    
    def distance(self, other):
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
```

```{code-cell} ipython3
:cell_style: split

a = Point(4, 3)
b = Point(7, 7)
a, b
```

```{code-cell} ipython3
:cell_style: split

a.distance(b)
```

+++ {"slideshow": {"slide_type": "slide"}}

### exemple : `class Circle` (1)

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
tags: []
---
class Circle1:

    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius
        
    def __repr__(self):
        return f"[{self.center} ⟷ {self.radius:.2f}]"
    
    def contains(self, point: Point):
        """
        returns a bool; does point belong in the circle ?
        """
        print(self.center.distance(point))
        return math.isclose(self.center.distance(point), self.radius)
```

```{code-cell} ipython3
c1 = Circle1(Point(0, 0), 5)
c1.contains(a)
```

+++ {"slideshow": {"slide_type": "slide"}}

### exemple : `class Circle` (2)

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
tags: []
---
class Circle2:

    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius
        
    def __repr__(self):
        return f"[{self.center} ⟷ {self.radius:.2f}]"
    
    # si on transforme cette méthode en méthode spéciale...
    def __contains__(self, point: Point):
        """
        returns a bool; does point belong in the circle ?
        """
        print(self.center.distance(point))
        return math.isclose(self.center.distance(point), self.radius)
```

```{code-cell} ipython3
c2 = Circle2(Point(0, 0), 5)

# alors on peut faire le même calcul, mais
# l'écrire comme un test d'appartenance habituel 'x in y'
a in c2
```

+++ {"slideshow": {"slide_type": "slide"}}

### exemple : `class datetime.date` etc..

* bien sûr il y a des classes dans la bibliothèque standard
* voyez par exemple [le module `datetime`](https://docs.python.org/3/library/datetime.html)
* et notamment `datetime.date` (une date)  
  et `datetime.timedelta` (une durée)

+++

* bien sûr il y a des classes dans la bibliothèque standard
* voyez par exemple [le module `datetime`](https://docs.python.org/3/library/datetime.html)
* et notamment `datetime.date` (une date)  
  et `datetime.timedelta` (une durée)

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# normalement la classe date aurait dû s'appeler Date
from datetime import date as Date
# pareil
from datetime import timedelta as TimeDelta

Date.today()
```

```{code-cell} ipython3
:cell_style: split

TimeDelta(weeks=2)
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
# il y a 3 semaines nous étions le
today = Date.today()
three_weeks = 3 * TimeDelta(weeks=1)

today - three_weeks
```

```{code-cell} ipython3
:tags: []

def timedelta_as_year_month(age):
    """
    convert a duration in years and months (as a str)
    """
    year = TimeDelta(days=365.2425)
    years, leftover = age // year, age % year
    month = year/12
    months, leftover = leftover // month, leftover % month
    return f"{years} ans, {months} mois"
```

+++ {"slideshow": {"slide_type": "slide"}}

### exemple : `class Student`

```{code-cell} ipython3
:tags: []

class Student:
    
    def __init__(self, first_name, last_name, 
                 birth_year, birth_month, birth_day):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        
    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
    
    def age(self):
        """
        retourne un TimeDelta
        """
        birth = Date(self.birth_year, self.birth_month, self.birth_day)
        now = Date.today()
        # la différence entre 2 Dates c'est une 
        return now - birth
    
    def repr_age(self):
        return timedelta_as_year_month(self.age())
```

+++ {"slideshow": {"slide_type": "slide"}}

#### `class Student` - utilisation

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
achille = Student("Achille", "Talon", 2001, 7, 14)
achille
```

```{code-cell} ipython3
:cell_style: split

achille.age()
```

```{code-cell} ipython3
:cell_style: split

type(achille.age())
```

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
print(f"{achille} a {achille.repr_age()}")
```

+++ {"slideshow": {"slide_type": "slide"}}

### exemple : class `Class` 

(dans le sens: groupe de `Student`s)

* bien sûr on peut combiner nos types (les classes)  
  avec les types de base
* et ainsi créer e.g. des listes de `Student`

```{code-cell} ipython3
class Class:
    
    def __init__(self, classname, students):
        self.classname = classname
        self.students = students
        
    def __repr__(self):
        return f"{self.classname} with {len(self.students)} students"
        
    def average_age(self):
        # on aimerait pouvoir écrire simplement ceci
        # return ((sum(student.age() for student in self.students)
        #          / len(self.students))
        # mais ça ne fonctionne pas, il faut passer à sum 
        # l'élément neutre de l'addition - ici TimeDelta(0)
        # car '0' ne peut pas s'additionner à un TimeDelta
        return (sum((student.age() for student in self.students), TimeDelta(0)) 
                / len(self.students))
```

+++ {"slideshow": {"slide_type": "slide"}}

#### `class Class` - utilisation

```{code-cell} ipython3
hilarion = Student("Hilarion", "Lefuneste", 1998, 10, 15)
gaston = Student("Gaston", "Lagaffe", 1995, 2, 28)
haddock = Student("Capitaine", "Haddock", 2000, 1, 14)
tournesol = Student("Professeur", "Tournesol", 1996, 2, 29)

# attention je ne peux pas utiliser une variable 
# qui s'appellerait 'class' car c'est un mot-clé de Python

cls = Class("CIC1A", [achille, hilarion, gaston, haddock, tournesol])
cls
```

```{code-cell} ipython3
# la moyenne d'âge de la classe
cls.average_age()
```

```{code-cell} ipython3
# la moyenne d'âge de la classe, pour les humains
timedelta_as_year_month(cls.average_age())
```

+++ {"slideshow": {"slide_type": "slide"}}

## résumé (1/2)

* avec `class` on peut définir un **nouveau type** 
  * qui nous permet de **créer des objets**
  * qui représentent mieux que les types de base les données de notre application
  
* pas de différence entre un type prédéfini et une classe :  
  un objet créé par une classe s'utilise *normalement*
  * une variable peut désigner un objet
  * un objet peut être dans une liste (ou autre type) *builtin*  
    (attention pour les clés de `dict` qui doivent être immutables)
  * ou passé en paramètre à une fonction,
  * etc, etc...

+++ {"slideshow": {"slide_type": "slide"}}

### résumé (2/2)
  
* une classe peut définir des **méthodes**
  * qui travaillent sur un objet (souvent appelé `self`)
  * souvent on ne modifie les objets  
    qu'au travers des méthodes fournies par la classe
  * ce qui permet de garantir certains invariants
