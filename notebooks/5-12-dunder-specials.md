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

# classes : rappels (2)

les méthodes spéciales (aussi appelées *dunder methods*)

+++ {"slideshow": {"slide_type": "slide"}}

## méthodes spéciales / *dunder methods*

* sur une classe on peut définir des **méthodes spéciales**  
* pour bien intégrer les objets dans le langage  
* c'est-à-dire donner du sens à des constructions du langage

e.g. que peuvent vouloir dire :

* avec les fonctions *builtin*, e.g. `len(obj)`, `int(obj)`
* opérateurs comme `obj + x`  
* itération `for item in obj`
* test d'appartenance `x in obj` 
* indexation `obj[x]` 
* même appel! `obj(x)`
* etc...

+++ {"slideshow": {"slide_type": "slide"}}

## `len(obj)`

```{code-cell} ipython3
:cell_style: split

class Classe:
    
    def __init__(self, students):
        self.students = students
        
    def __len__(self):
        return len(self.students)
```

```{code-cell} ipython3
:cell_style: split

classe = Classe(['jean', 'laurent', 'benoit'])

len(classe)
```

de manière similaire : 
* `__int__(self)` pour redéfinir `int(obj)` et similaires

+++ {"slideshow": {"slide_type": "slide"}}

## `bool(obj)`

```{code-cell} ipython3
:cell_style: split

class Classe:
    
    def __init__(self, students):
        self.students = students
        
    def __bool__(self):
        return self.students != []
```

```{code-cell} ipython3
:cell_style: split

classe1 = Classe([])
classe2 = Classe(['jean', 'laurent', 'benoit'])

if not classe1:
    print("classe1 est fausse")
if classe2:
    print("classe2 est vraie")
```

+++ {"slideshow": {"slide_type": "slide"}}

## opérateurs

```{code-cell} ipython3
:cell_style: split

class Classe:
    
    def __init__(self, students):
        self.students = students
        
    def __add__(self, other):
        return Classe(self.students + other.students)
    
    def __repr__(self):
        return f"[{len(self.students)} students]"
```

```{code-cell} ipython3
:cell_style: split

classe1 = Classe(['marie', 'claire'])
classe2 = Classe(['jean', 'laurent'])

classe1 + classe2
```

+++ {"slideshow": {"slide_type": "slide"}}

## itérations

```{code-cell} ipython3
:cell_style: split

class Classe:

    def __init__(self, students):
        self.students = students

    def __iter__(self):
        return iter(self.students)
```

```{code-cell} ipython3
:cell_style: split

classe = Classe(['jean', 'laurent', 'benoit'])

for s in classe:
    print(s)
```

+++ {"slideshow": {"slide_type": "slide"}}

## appartenance

```{code-cell} ipython3
:cell_style: split

class Classe:

    def __init__(self, students):
        self.students = students

    def __contains__(self, student):
        return student in self.students
```

```{code-cell} ipython3
:cell_style: split

classe = Classe(['jean', 'laurent', 'benoit'])

'jean' in classe
```

+++ {"slideshow": {"slide_type": "slide"}}

## indexations

```{code-cell} ipython3
:cell_style: split

class Classe:

    def __init__(self, students):
        self.students = students

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.students[index]
        elif isinstance(index, str):
            if index in self.students:
                return index
            else:
                return None
```

```{code-cell} ipython3
:cell_style: split

classe = Classe(['jean', 'laurent', 'benoit'])

classe[1]
```

```{code-cell} ipython3
:cell_style: split

classe['jean']
```

```{code-cell} ipython3
:cell_style: split

classe['pierre'] is None
```

+++ {"slideshow": {"slide_type": "slide"}}

## appel

on peut même donner du sens à `obj(x)`

```{code-cell} ipython3
:cell_style: split

class Line:
    """
    modelling the line of equation
    y = ax + b
    """
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def __call__(self, x):
        return self.a * x + self.b
```

```{code-cell} ipython3
:cell_style: split
:tags: []

# cet objet se comporte
# comme une fonction

line = Line(2, 2)


# c'est intéressant de pouvoir l'appeler
# comme si c'était une fonction

line(1)
```

+++ {"slideshow": {"slide_type": "slide"}}

## pour en savoir plus

la liste exhaustive des méthodes spéciales est donnée dans la documentation officielle ici

https://docs.python.org/3/reference/datamodel.html#special-method-names

+++ {"slideshow": {"slide_type": "slide"}}

## résumé
  
une classe peut définir des **méthodes spéciales**

* notamment le constructeur pour l'initialisation,
* souvent un afficheur pour `print()`
* optionnellement d'autres pour donner du sens à  
  des constructions du langage sur ces objets
* ces méthodes ont toutes un nom en `__truc__` (*dunder methods*)
