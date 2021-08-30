---
celltoolbar: Slideshow
jupytext:
  cell_metadata_filter: all, -hidden, -heading_collapsed, -run_control, -trusted
  encoding: '# -*- coding: utf-8 -*-'
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
notebookname: "expressions r\xE9guli\xE8res"
rise:
  autolaunch: true
  slideNumber: c/t
  start_slideshow_at: selected
  theme: sky
  transition: cube
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat
</div>

+++ {"slideshow": {"slide_type": ""}}

# expressions régulières

+++

* notion transverse aux langages de programmation
* présente dans la plupart d'entre eux
* en particulier historiquement Perl  
  qui en avait fait un *first-class citizen*

+++ {"slideshow": {"slide_type": "slide"}}

## exemples

+++ {"slideshow": {"slide_type": ""}}

* `a*` décrit tous les mots  
  composés **de 0 ou plusieurs** `a`

  * `''`, `'a'`, `'aa'`, …  
    sont les mots reconnus 

* `(ab)+` : toutes les suites de  
  **au moins 1 occurrence** de `ab`  

  * `'ab'`, `'abab'`, `'ababab'`, …  
    sont les mots reconnus

+++ {"slideshow": {"slide_type": "slide"}}

## le module `re`

+++ {"slideshow": {"slide_type": ""}}

en Python, les expressions régulières sont accessibles au travers du module `re`

```{code-cell} ipython3
import re

# en anglais on dit pattern
# en français on dit filtre, 
# ou encore parfois motif
pattern = "a*"

# la fonction `match` 
re.match(pattern, '')
```

```{code-cell} ipython3
:cell_style: split

re.match(pattern, 'a')
```

```{code-cell} ipython3
:cell_style: split

re.match(pattern, 'aa')
```

```{code-cell} ipython3
:cell_style: split

re.match('(ab)+', 'ab')
```

```{code-cell} ipython3
:cell_style: split

# pas conforme : retourne None
re.match('(ab)+', 'ba')
```

+++ {"slideshow": {"slide_type": "slide"}}

### `re.match()`

+++ {"slideshow": {"slide_type": ""}}

* **ATTENTION** car `re.match()` vérifie si l'expression régulière peut être trouvée **au début** de la chaine

```{code-cell} ipython3
:cell_style: center

# ici seulement LE DÉBUT du mot est reconnu

match = re.match('(ab)+', 'ababzzz')
match
```

```{code-cell} ipython3
:cell_style: split

# commence au début 
match.start()
```

```{code-cell} ipython3
:cell_style: split

# mais pas jusque la fin
match.end()
```

+++ {"slideshow": {"slide_type": "slide"}}

### `re.search()`

+++ {"slideshow": {"slide_type": ""}}

* `re.search()` cherche la première occurrence de l'expression régulière  
* **pas forcément** au début de la chaine

```{code-cell} ipython3
:cell_style: center

# match répond non car seulement LE DÉBUT de la chaine est essayé

re.match('abzz', 'ababzzz')
```

```{code-cell} ipython3
:cell_style: center

re.search('abzz', 'ababzzz')
```

+++ {"slideshow": {"slide_type": "slide"}}

### les objets `Match`

+++ {"slideshow": {"slide_type": ""}}

* le résultat de `re.match()` est de type `Match` 
* pour les détails de ce qui a été trouvé  
  (par exemple quelle partie de la chaine)

* et aussi les sous-chaines  
  correspondant aux **groupes**  
  (on en reparlera)

+++ {"slideshow": {"slide_type": "slide"}}

### autres façons de chercher

+++ {"slideshow": {"slide_type": ""}}

* `re.findall()` et `re.finditer()` pour trouver toutes les occurences du filtre dans la chaine
* `re.sub()` pour remplacer …

**notre sujet**

* ici nous nous intéressons surtout à la façon de **construire les regexps**
* se reporter à [la documentation du module](https://docs.python.org/3/library/re.html) pour ces variantes

+++ {"slideshow": {"slide_type": "slide"}}

#### pour visualiser

```{code-cell} ipython3
# digression : un utilitaire pour montrer
# le comportement d'un pattern / filtre

def match_all(pattern, strings):
    """
    match a pattern against a set of strings and shows result
    """
    col_width = max(len(x) for x in strings) + 2 # for the quotes
    for string in strings:
        string_repr = f"'{string}'"
        print(f"'{pattern}' ⇆ {string_repr:<{col_width}} → ", end="")
        match = re.match(pattern, string)
        if not match:
            print("NO")
        elif match.end() != len(string):
            # start() is always 0
            print(f"BEGINNING ONLY (until {match.end()})")
        else:
            print("FULL MATCH")
```

```{code-cell} ipython3
:cell_style: center

match_all('(ab)+', ['ab', 'abab', 'ababzzz', ''])
```

+++ {"slideshow": {"slide_type": "slide"}}

## construire un pattern

+++ {"slideshow": {"slide_type": "slide"}}

### n'importe quel caractère : `.`

```{code-cell} ipython3
match_all('.', ['', 'a', '.', 'Θ', 'ab'])
```

+++ {"slideshow": {"slide_type": "slide"}}

### filtrer **un seul** caractère : `[..]`

+++ {"slideshow": {"slide_type": ""}}

* avec les `[]` on peut désigner un **ensemble** de caractères :
* `[a-z]` les lettres minuscules
* `[a-zA-Z0-9_]` les lettres et chiffres et underscore

```{code-cell} ipython3
:cell_style: split

match_all('[a-z]', ['a', '', '0'])
```

```{code-cell} ipython3
---
cell_style: split
slideshow:
  slide_type: ''
---
match_all('[a-z0-9]', ['a', '9', '-'])
```

```{code-cell} ipython3
:cell_style: center

# pour insérer un '-', le mettre à la fin
# sinon ça va être compris comme un intervalle
match_all('[0-9+-]', ['0', '+', '-', 'A'])
```

+++ {"cell_style": "split", "slideshow": {"slide_type": "slide"}}

### idem mais à l'envers : `[^..]`

+++ {"cell_style": "split"}

* si l'ensemble de caractères entre `[]` commence par un `^`
* cela désigne le **complémentaire** dans l'espace des caractères

```{code-cell} ipython3
:cell_style: split

# complémentaires
match_all('[^a-z]', ['a', '0', '↑', 'Θ'])
```

```{code-cell} ipython3
:cell_style: split

match_all('[^a-z0-9]', ['a', '9', '-'])
```

+++ {"slideshow": {"slide_type": "slide"}}

### 0 ou plusieurs occurrences : `..*`

```{code-cell} ipython3
:cell_style: split

match_all('[a-z]*', ['', 'cba', 'xyz9'])
```

```{code-cell} ipython3
:cell_style: split

match_all('(ab)*', ['', 'ab', 'abab'])
```

+++ {"slideshow": {"slide_type": ""}}

### 1 ou plusieurs occurrences : `..+`

```{code-cell} ipython3
:cell_style: split

match_all('[a-z]+', ['', 'cba', 'xyz9'])
```

```{code-cell} ipython3
:cell_style: split

match_all('(ab)+', ['', 'ab', 'abab'])
```

+++ {"slideshow": {"slide_type": "slide"}}

### concaténation

quand on concatène deux filtres, la chaine doit matcher l'un puis l'autre

```{code-cell} ipython3
:cell_style: split

# c'est le seul mot qui matche
match_all('ABC', ['ABC']) 
```

```{code-cell} ipython3
:cell_style: split

match_all('A*B', ['B', 'AB', 'AAB', 'AAAB']) 
```

+++ {"slideshow": {"slide_type": "slide"}}

### groupement : `(..)`

+++

* permet d'appliquer un opérateur sur une regexp
  * comme déjà vu avec `(ab)+`
* cela définit un **groupe** qui peut être retrouvé dans le match
  * grâce à la méthode `groups()`

```{code-cell} ipython3
:cell_style: split

# groupes anonymes
pattern = "([a-z]+)=([a-z0-9]+)"

string = "foo=barbar99"

match = re.match(pattern, string)
match
```

```{code-cell} ipython3
:cell_style: split

# dans l'ordre où ils apparaissent
match.groups()
```

+++ {"slideshow": {"slide_type": "slide"}}

### alternative : `..|..`

+++

pour filtrer avec une regexp **ou** une autre :

```{code-cell} ipython3
:cell_style: split

match_all('ab|cd', ['ab', 'cd', 'abcd'])
```

```{code-cell} ipython3
:cell_style: split

match_all('ab|cd*', ['ab', 'c', 'cd', 'cdd'])
```

```{code-cell} ipython3
:cell_style: split

match_all('ab|(cd)*', ['ab', 'c', 'cd', 'cdd'])
```

```{code-cell} ipython3
:cell_style: split

match_all('(ab|cd)*', ['ab', 'c', 'cd', 'cdd', 'abcd'])
```

+++ {"slideshow": {"slide_type": "slide"}}

### 0 ou 1 occurrences : `..?`

```{code-cell} ipython3
:cell_style: split

match_all('[a-z]?', ['', 'b', 'xy'])
```

+++ {"slideshow": {"slide_type": "slide"}}

### nombre d'occurrences dans un intervalle : `..{n,m}`

+++

* `a{3}` : exactement 3 occurrences de `a`
* `a{3,}` : au moins 3 occurrences
* `a{3,6}` : entre 3 et 6 occurrences

```{code-cell} ipython3
:cell_style: center

match_all('(ab){1,3}', ['', 'ab', 'abab', 'ababab', 'ababababababab'])
```

+++ {"slideshow": {"slide_type": "slide"}}

### classes de caractères

+++ {"slideshow": {"slide_type": ""}}

raccourcis qui filtrent **un caractère** dans une classe  
définis en fonction de la configuration de l'OS en termes de langue

* `\s` (pour Space) : exactement un caractère de séparation (typiquement Espace, Tabulation, Newline)
* `\w` (pour Word) : exactement un caractère alphabétique ou numérique
* `\d` (pour Digit) : un chiffre
* `\S`, `\W` et `\D` : les complémentaires

```{code-cell} ipython3
:cell_style: split

match_all('\w+', ['eFç0', 'été', ' ta98'])
```

```{code-cell} ipython3
:cell_style: split

match_all('\s?\w+', ['eFç0', 'été', ' ta98'])
```

+++ {"slideshow": {"slide_type": "slide"}}

### groupe nommé : `(?P<name>..)`

+++ {"slideshow": {"slide_type": ""}}

* le même effet que les groupes anonymes,
* mais on peut retrouver le contenu depuis le nom du groupe
* plutôt que le rang (numéro) du groupe
  * qui peut rapidement devenir une notion fragile / peu maintenable

```{code-cell} ipython3
:cell_style: center

# groupes nommés
pattern = "(?P<variable>[a-z]+)=(?P<valeur>[a-z0-9]+)"

string = "foo=barbar99"

match = re.match(pattern, string)
match
```

```{code-cell} ipython3
:cell_style: split

match.group('variable')
```

```{code-cell} ipython3
:cell_style: split

match.group('valeur')
```

+++ {"slideshow": {"slide_type": "slide"}}

### plusieurs occurrences du même groupe : `(?P=name)`

+++ {"slideshow": {"slide_type": ""}}

on peut spécifier qu'un groupe doit apparaître plusieurs fois

```{code-cell} ipython3
:tags: []

# la deuxième occurrence de <nom> doit être la même que la première
pattern = '(?P<nom>\w+).*(?P=nom)'

string1 = 'Jean again Jean'
string2 = 'Jean nope Pierre'
string3 = 'assez comme ça'

match_all(pattern, [string1, string2, string3])
```

+++ {"slideshow": {"slide_type": "slide"}}

### début et fin de chaine : `^` et `$`

```{code-cell} ipython3
:cell_style: center

match_all('ab|cd', ['ab', 'abcd'])
```

```{code-cell} ipython3
# pour forcer la chaine à matcher jusqu'au bout
# on ajoute un $ 
match_all('(ab|cd)$', ['ab', 'abcd'])
```

+++ {"slideshow": {"slide_type": "slide"}}

## pour aller plus loin

+++ {"slideshow": {"slide_type": ""}}

* beaucoup d'autres possibilités

* testeurs en ligne  
  <https://pythex.org>  
  <https://regex101.com/> (bien choisir Python)

* un peu de détente, avec ce jeu de mots croisés basé sur les regexps 
  <https://regexcrossword.com>  
  commencer [par le tutorial](https://regexcrossword.com/challenges/tutorial/puzzles/1)

* tour complet de la syntaxe des regexps  
  <https://docs.python.org/3/library/re.html#regular-expression-syntax>
