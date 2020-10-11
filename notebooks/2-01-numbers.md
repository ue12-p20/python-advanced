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
notebookname: nombres
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

# les nombres

+++ {"slideshow": {"slide_type": "slide"}}

## types de base `int`, `float`, `complex`

* conversion automatique si nécessaire
* les `int` ont une précision illimitée
  * Python peut calculer nativement

```{code-cell} ipython3
92857234957203457234572203957 * 948572349572039457029347529347
```

* ceux qui ont eu à faire ça en C apprécieront

+++ {"slideshow": {"slide_type": "slide"}}

### division

```{code-cell} ipython3
# division exacte/flottante
5 / 2           
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
# division entière
8 // 3          
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
# division entière
8.0 // 3        
```

+++ {"slideshow": {"slide_type": "slide"}}

### nombres : opérateurs

```{code-cell} ipython3
:cell_style: split

# reste div. entière
5 % 3       
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
# reste div. entière
5 % 1.5       
```

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
2 ** 32         # puissance
```

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
int(234.5)      # cast float ➔ int
```

+++ {"slideshow": {"slide_type": "slide"}}

### nombres complexes

```{code-cell} ipython3
1j * 1j         # nombres complexes
```

```{code-cell} ipython3
a = 3 + 4j
a.real          # partie réelle
```

```{code-cell} ipython3
a.imag          # partie imaginaire
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### en hexa, binaire, octal

```{code-cell} ipython3
0xff            # hexadécimal
```

```{code-cell} ipython3
0b11111111      # binaire
```

```{code-cell} ipython3
0o377           # octal
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### sous forme hexa, binaire, octale

```{code-cell} ipython3
hex(255)    # traduire en hexa (-> str)
```

```{code-cell} ipython3
bin(255)    # traduire en binaire (-> str)
```

```{code-cell} ipython3
oct(255)    # traduire en octal (-> str)
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### décalages

```{code-cell} ipython3
:cell_style: split

x = 3
y = x << 10 # décalage à gauche 
y
```

```{code-cell} ipython3
:cell_style: split

2**11 + 2**10
```

```{code-cell} ipython3
x          # l'argument n'est pas modifié
```

```{code-cell} ipython3
:cell_style: split

y >> 3     # décalage à droite 
```

```{code-cell} ipython3
:cell_style: split

2**8 + 2**7
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### opérations *bitwise*

```{code-cell} ipython3
y = 4
y | 2      # bitwise OR de 0100 (4) et 0010 (2) 
```

```{code-cell} ipython3
y & 2      # bitwise AND de 0100 (4) et 0010 (2)
```

```{code-cell} ipython3
y & 15     # bitwise AND de 0100 (4) et 1111 (15)
```

```{code-cell} ipython3
y ^ 15     # bitwise XOR de 0100 (4) et 1111 (15)
```

* rarement utile d’utiliser les opérations bitwise en Python
* mieux vaut utiliser les structures de données fournies
* parfois utile avec numpy toutefois

+++ {"slideshow": {"slide_type": "slide"}}

### le module `math`

```{code-cell} ipython3
:cell_style: split

# pour anticiper un peu 
# sur les listes...
# les 6 derniers symboles
# dans le module math
import math
dir(math)[-6:]
```

```{code-cell} ipython3
:cell_style: split

math.tau
```

```{code-cell} ipython3
:cell_style: split

math.sin(math.pi)
```

**Important**: Entraînez vous aussi à trouver la doc dans google:

https://www.google.com/search?q=python+module+math

+++ {"slideshow": {"slide_type": "slide"}}

## booléens

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
True == 1
```

```{code-cell} ipython3
:cell_style: split


False == 0
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
3 + True
```

```{code-cell} ipython3
:cell_style: split

3 + False
```

+++ {"slideshow": {"slide_type": "slide"}}

### booléens et tests (1)

```{code-cell} ipython3
:cell_style: split

# on peut faire un `if`
# (ou un while) sur un booléen
a = 3
b = 4

type(a == b)
```

```{code-cell} ipython3
:cell_style: split

# sujet du if = booléen

if a == b:
    print("pareils")
else:
    print("différents")
```

+++ {"slideshow": {"slide_type": "slide"}}

### booléens et tests (2)

```{code-cell} ipython3
:cell_style: split

# mais aussi : avec n'importe quoi d'autre

if a:
    print("pas faux")
```

```{code-cell} ipython3
:cell_style: split

# en fait équivalent à ceci:

if bool(a):
    print("pas faux")
```

+++ {"slideshow": {"slide_type": "slide"}}

## conversions

+++

* c'est la **mécanique générale** pour convertir entre types de données:

```{code-cell} ipython3
:cell_style: split

# si on appelle int() on convertit en entier
int(3.4)
```

```{code-cell} ipython3
:cell_style: split

# si on appelle bool() on convertit en booléen

bool(3.4)
```

```{code-cell} ipython3
:cell_style: split

bool(0)
```

```{code-cell} ipython3
:cell_style: split

bool("")
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

### booléens - épilogue

+++

* attention à ne pas confondre
* les opérations bit à bit avec les opérations booléennes

```{code-cell} ipython3
---
slideshow:
  slide_type: '-'
---
a = True; b = True
print("a", bool(a), "b", bool(b), "a^b", bool(a^b))
```

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
a = 1; b = 2
print("a", bool(a), "b", bool(b), "a^b", bool(a^b))
```

+++ {"slideshow": {"slide_type": "slide"}}

## l'encodage des flottants

+++

* représentés en machine comme des fractions en base 2
* le plus souvent une **approximation**
  * quand pas une fraction binaire exacte
* pas une spécificité de Python
  * IEE-754: [WikiPedia](https://en.wikipedia.org/wiki/IEEE_754) - [interactif **64bits**](http://www.binaryconvert.com/convert_double.html)

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: '-'
---
0.1 + 0.2
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: '-'
---
0.1 + 0.2 == 0.3
```

+++ {"slideshow": {"slide_type": "slide"}}

### contournements

+++

##### selon les usages

* le [module `decimal`](https://docs.python.org/3/library/decimal.html), pour travailler sur des nombres décimaux
  * avec plus de précision et de contrôle qu’avec le type `float`
* le [module `fractions`](https://docs.python.org/3/library/fractions.html) permet de travailler sur des rationnels

+++ {"slideshow": {"slide_type": "slide"}}

### exemples - `decimal`

```{code-cell} ipython3
:cell_style: split

from decimal import Decimal
x = Decimal('0.1') + Decimal('0.2')
```

```{code-cell} ipython3
:cell_style: split

x == Decimal('0.3')
```

+++ {"slideshow": {"slide_type": "slide"}}

### exemples - `fractions`

```{code-cell} ipython3
:cell_style: center

from fractions import Fraction
x = Fraction(1, 10) + Fraction(2, 10)
x
```

```{code-cell} ipython3
:cell_style: split

x == Fraction(3, 10)
```

```{code-cell} ipython3
:cell_style: split

x == 0.3
```
