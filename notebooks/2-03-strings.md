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
notebookname: chaines et binaire
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

# chaines et binaire (`str` et `bytes`)

+++ {"slideshow": {"slide_type": "slide"}}

## rappels

+++ {"cell_style": "split"}

### les séquences

* suite finie et ordonnée d'objets
* du coup indexable `seq[n]`
* indices **commencent à 0**
* peuvent contenir des duplications

+++ {"cell_style": "split"}

### mutable et immutable

* mutable
  * `list`, `bytearray`
* immutable
  * `str`, `bytes`, `tuple`, `range`

+++

un chaine - de type `str` - est une **séquence immutable**

+++ {"slideshow": {"slide_type": "slide"}}

## fonctions sur (toutes) les séquences

+++ {"cell_style": "split"}

* `S[i]`
  * retourne l’élément d'indice i
* `len(S)` 
  * donne la taille en nombre d’éléments

+++ {"cell_style": "split"}

* `S + T`
 * retourne une nouvelle séquence qui est la concaténation de S et T
* `S*n` ou `n*S`
  * retourne une nouvelle séquence qui est la concaténation de n *shallow* copies de S

+++ {"slideshow": {"slide_type": "slide"}}

### fonctions sur les séquences...

+++ {"slideshow": {"slide_type": ""}, "cell_style": "split"}

* `x in S`; selon les types:
 * `True` si un élément de S est égal à x (e.g. `list`)
 * `True` si S contient x (e.g. `str`)

+++ {"slideshow": {"slide_type": ""}, "cell_style": "split"}

* `S.index(a)`
  * retourne l’indice de la première occurrence de a dans S
* `S.count(a)`
  * retourne le nombre d’occurrences de a dans S

+++ {"slideshow": {"slide_type": "slide"}}

## slicing

+++

* `S[i:j]` retourne 
  * une nouvelle séquence de même type
  * contenant tous les éléments de l’indice i à l’indice j-1
* `S[i:j:k]` retourne
  * une nouvelle séquence de même type
  * prenant tous les éléments de l’indice i à l’indice j-1, par sauts de k éléments

+++ {"cell_style": "split", "slideshow": {"slide_type": "slide"}}

<img src="media/egg-bacon.png"/>

+++ {"cell_style": "split"}

### *slicing*

+++ {"cell_style": "split"}

* on peut compter du début ou de la fin
* on peut omettre les bornes

```{code-cell} ipython3
:cell_style: split

s = "egg, bacon"
s[0:3]
```

```{code-cell} ipython3
:cell_style: split

# si on omet une borne 
# ce sera le début ..
s[:3]
```

```{code-cell} ipython3
:cell_style: split

# ... ou la fin:
s[5:]
```

```{code-cell} ipython3
:cell_style: split

# les indices peuvent être négatifs
s[-3:10]
```

```{code-cell} ipython3
# tout entier: une shallow-copy
s[:]
```

+++ {"cell_style": "split", "slideshow": {"slide_type": "slide"}}

<img src="media/egg-bacon-bornes.png" text-align="center">

+++ {"cell_style": "split", "slideshow": {"slide_type": ""}}

### les bornes

+++ {"cell_style": "split"}

La convention est choisie pour pouvoir facilement encastrer les slices:

```{code-cell} ipython3
:cell_style: split

s[0:3]
```

```{code-cell} ipython3
:cell_style: split

s[3:6]
```

```{code-cell} ipython3
:cell_style: split

s[6:]
```

```{code-cell} ipython3
:cell_style: split

s[0:3] + s[3:6] + s[6:] == s
```

+++ {"cell_style": "split", "slideshow": {"slide_type": "slide"}}

<img src="media/egg-bacon.png" text-align="center">

+++ {"cell_style": "split"}

### le pas

+++ {"cell_style": "split"}

* on peut préciser un pas
* peut aussi être négatif
* ou omis (défaut 1)

```{code-cell} ipython3
:cell_style: split

s[0:10:2]
```

```{code-cell} ipython3
:cell_style: split

s[::2]
```

```{code-cell} ipython3
:cell_style: split

s[:8:3]
```

```{code-cell} ipython3
:cell_style: split

s[-2::-3]
```

+++ {"cell_style": "split", "slideshow": {"slide_type": "slide"}}

<img src="media/egg-bacon.png" text-align="center">

+++ {"cell_style": "split"}

### pas d'exception

+++ {"cell_style": "split"}

les slices ont un comportement plus permissif que l'indexation

```{code-cell} ipython3
# Si j'essaie d'utiliser un index inexistant
try: s[100]
except Exception as e: print("OOPS", e)
```

```{code-cell} ipython3
:cell_style: split

# par contre avec un slice, pas de souci
s[5:100]
```

```{code-cell} ipython3
:cell_style: split

# vraiment..
s[100:200]
```

+++ {"slideshow": {"slide_type": "slide"}}

<img src="media/egg-bacon.png" text-align="center">

```{code-cell} ipython3
:cell_style: split

s[-1]
```

```{code-cell} ipython3
:cell_style: split

s[-3:-1]
```

```{code-cell} ipython3
:cell_style: split

s[:-3]
```

```{code-cell} ipython3
:cell_style: split

s[::-1]
```

```{code-cell} ipython3
:cell_style: split

# le 2 est inclus et le 0 exclus
s[2:0:-1]
```

```{code-cell} ipython3
:cell_style: split

s[2::-1]
```

+++ {"slideshow": {"slide_type": "slide"}}

### slicing, formes idiomatiques

```{code-cell} ipython3
s = [1, 2, 3]
```

```{code-cell} ipython3
:cell_style: split

# une copie simple
s[:]
```

```{code-cell} ipython3
:cell_style: split

# copie renversée
s[::-1]
```

+++ {"slideshow": {"slide_type": "slide"}}

# `str` et `bytes`

+++

* deux cas particuliers de **séquences**
  * `str` pour manipuler **du texte**
  * `bytes` pour manipuler **de la donnée brute** (des octets)
  
* **ATTENTION**
  * les caractères alphanumériques (sans accent)  
    et la ponctuation tiennent sur 1 octet
  * mais **ce n'est pas le cas** en général

+++ {"slideshow": {"slide_type": "slide"}}

# chaînes de caractères `str`

+++

* un cas particulier de séquence
* une chaîne de caractères est définie de manière équivalente par des simples ou doubles guillemets (`'` ou `"`)
* on peut ainsi facilement inclure un guillemet

```{code-cell} ipython3
:cell_style: split

# une chaine entre double quotes
# pas de souci pour les accents 
print("c'est l'été")
```

```{code-cell} ipython3
:cell_style: split

# entre simple quotes
print('on se dit "pourquoi pas"')
```

+++ {"slideshow": {"slide_type": "slide"}}

### chaînes de caractères `str`

```{code-cell} ipython3
:cell_style: split

s = "l'hôtel"
print(s)
```

```{code-cell} ipython3
:cell_style: split

s = 'une "bonne" idée'
print(s)
```

```{code-cell} ipython3
:cell_style: split

s = """une très longue phrase
avec saut de ligne"""
print(s)
```

```{code-cell} ipython3
:cell_style: split

s = '  un backslash \\ un quote \' ' 
print(s)
```

+++ {"slideshow": {"slide_type": "slide"}}

## opérations sur les `str`

* toutes les opérations des séquences

```{code-cell} ipython3
:cell_style: split

s1 = 'abcdéfg'
s2 = 'bob'
len(s1)
```

```{code-cell} ipython3
:cell_style: split

# concaténation
s1 + s2
'abcdefbob'
```

```{code-cell} ipython3
:cell_style: split

s1[-1::-2]
```

```{code-cell} ipython3
:cell_style: split

'=' * 30
```

+++ {"slideshow": {"slide_type": "slide"}}

### opérations sur les `str`

```{code-cell} ipython3
:cell_style: split

s1
```

```{code-cell} ipython3
:cell_style: split

'x' in s1
```

```{code-cell} ipython3
:cell_style: split

'cdé' in s1
```

```{code-cell} ipython3
:cell_style: split

s1.index('cdé')
```

+++ {"slideshow": {"slide_type": "slide"}}

### opérations sur les `str`

+++

* par contre **ATTENTION** un `str` n'est **pas mutable**

```{code-cell} ipython3
try: 
    s1[2] = 'x'
except TypeError as e:
    print("OOPS", e, type(e))    
```

+++ {"slideshow": {"slide_type": "slide"}}

## formatage des chaînes : f-strings

+++ {"cell_style": "split"}

* depuis Python-3.6
* utilisez les ***f-strings***
* qui évitent les répétitions fastidieuses

+++ {"cell_style": "split"}

* entre `{` et `}` : **du code** 
* embarqué directement dans le format
* n'importe quelle expression

```{code-cell} ipython3
:cell_style: split

import math
```

```{code-cell} ipython3
:cell_style: split

nom, age = "Pierre", 42
```

```{code-cell} ipython3
:cell_style: split

f"{nom} a {age} ans"
```

```{code-cell} ipython3
:cell_style: split

f"360° = {2*math.pi} radians"
```

+++ {"slideshow": {"slide_type": "slide"}}

### formatage des chaînes de caractères

+++ {"slideshow": {"slide_type": ""}}

![](media/f-string.png)

```{code-cell} ipython3
print(f"ᴨ arrondi à deux décimales = {math.pi:.2f}")
```

+++ {"slideshow": {"slide_type": "slide"}}

### formats - scientifiques

+++

formats scientifiques usuels: `e` `f` et `g`, cf. `printf`

```{code-cell} ipython3
x = 23451.23423536563
f'{x:e} | {x:f} | {x:g} | {x:010.1f} | {x:.2f}'
```

```{code-cell} ipython3
y = 769876.11434
f'{x:e} | {y:f} | {x:g} | {y:010.2f} | {x:.2f}'
```

Voir aussi pour plus de détails:  
https://mkaz.blog/code/python-string-format-cookbook/

+++ {"slideshow": {"slide_type": "slide"}}

### formats pour f-string : justification

+++

justification: formats `<` `ˆ` et `>`

```{code-cell} ipython3
f"|{nom:<12}|{nom:^12}|{nom:>12}|"
```

```{code-cell} ipython3
# on peut aussi préciser avec quel caractère remplir
num = 123
f"|{num:<12}|{num:-^12}|{num:0>12}|"
```

+++ {"slideshow": {"slide_type": "slide"}}

## méthodes sur les `str`

+++

* de nombreuses méthodes disponibles

```{code-cell} ipython3
s = "une petite phrase"
s.replace('petite', 'grande')
```

```{code-cell} ipython3
s.find('hra')
```

```{code-cell} ipython3
liste = s.split()
liste
```

+++ {"slideshow": {"slide_type": "slide"}}

### sur les `str` : `split()` et `join()`

```{code-cell} ipython3
liste
```

```{code-cell} ipython3
:cell_style: split

"".join(liste)
```

```{code-cell} ipython3
:cell_style: split

" ".join(liste)
```

```{code-cell} ipython3
"_".join(liste)
```

```{code-cell} ipython3
:cell_style: split

s2 = "_".join(liste)
s2
```

```{code-cell} ipython3
:cell_style: split

s2.split('_')
```

+++ {"slideshow": {"slide_type": "slide"}}

# `str` *vs* `bytes`

+++ {"slideshow": {"slide_type": "slide"}}

## contenus binaires et textuels

+++ {"slideshow": {"slide_type": ""}}

* toutes les données ne sont pas textuelles
  * exemple: fichiers exécutables comme `cmd.exe`
  * stockage de données propriétaires (.doc, .xls, ...)
* dès qu'on utilise des données textuelles,
  * on décode une suite de bits
  * il faut leur **donner un sens**
  * c'est l'encodage

+++ {"slideshow": {"slide_type": "slide"}}

## le problème

+++

* dès que vous échangez avec l'extérieur, i.e.
  * Internet (Web, mail, etc.)
  * stockage (disque dur, clef USB)
  * terminal ou GUI, etc..
* vous traitez en fait des flux **binaires**
  * et donc vous êtes confrontés à l'encodage des chaines
  * et notamment en présence d'accents
  * ou autres caractères non-ASCII

+++ {"slideshow": {"slide_type": "slide"}}

## codage et décodage en python

+++ {"cell_style": "split"}

* le type `bytes` correspond,  
  comme son nom l'indique,  
  à une suite d'**octets**

  * dont la signification  
   (le décodage) est à la  
   charge du programmeur

* ce qui **n'est pas du tout**  
  le cas du type `str`
  * décodage fait par Python
  * le programmeur choisit un  
    encodage (défaut UTF-8)

+++ {"slideshow": {"slide_type": ""}, "cell_style": "split"}

![](media/str-bytes.png)

+++ {"slideshow": {"slide_type": "slide"}}

# Unicode

+++

* ***une*** liste des caractères 
  * avec **chacun un *codepoint*** - un nombre entier unique
  * de l'ordre de 137.000 + en Juin 2018 (*and counting*)
  * limite théorique 1,114,112 caractères

* ***trois*** encodages:
    * **UTF-8**: taille variable 1 à 4 octets, **compatible ASCII**
    * UTF-32: taille fixe, 4 octets par caractère
    * UTF-16: taile variable, 2 ou 4 octets

+++ {"slideshow": {"slide_type": "slide"}}

## l'essentiel sur UTF-8

* c'est l'encodage le plus répandu aujourd'hui 
  * la famille des ISO-latin et autres cp1252 sont à proscrire absolument
  * en 2020, c'est de moins en moins un souci

* avec UTF-8, les caractères usuels (dits ASCII),   
  sans accent, **sont codés sur 1 octet**
* mais ce n'est pas le cas en général :
  * les caractères **accentués** européens  
    sont codés sur **2 octets**

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_intermediate"]}

## UTF-8 illustré

+++ {"slideshow": {"slide_type": ""}, "tags": []}

le codepoint du caractère `é` est `0xe8` c'est-à-dire `232` 

![](media/unicode-table.png)

+++ {"slideshow": {"slide_type": "slide"}}

voici le flux binaire correspondant à la chaine `"été\n"`

![](media/unicode-decode-example.png)

+++ {"slideshow": {"slide_type": "slide"}, "tags": ["level_advanced"]}

## UTF-8 - le codage

+++

* le nombre d'octets utilisé pour encoder un caractère dépend
  * du caractère et de l'encodage
  * texte ASCII : identique en UTF-8
  * en particulier, ne prennent qu'un octet

+++ {"slideshow": {"slide_type": ""}}

![](media/unicode-utf8-areas.png) 

+++ {"slideshow": {"slide_type": "slide"}, "hide_input": true, "tags": []}

# UTF-8 et Python: `encode` et `decode`

```{code-cell} ipython3
:cell_style: split

text = 'été\n'
type(text)
```

```{code-cell} ipython3
:cell_style: split

# on compte les 
# caractères 

len(text)
```

```{code-cell} ipython3
:cell_style: split

octets = text.encode(encoding="utf-8")
for b in octets:
    print(f"{b:02x}", end=" ")
```

```{code-cell} ipython3
:cell_style: split

# ici par contre on
# compte les octets

len(octets)
```

+++ {"slideshow": {"slide_type": "slide"}, "tags": []}

## Unicode et Python: `chr` et `ord`

+++ {"cell_style": "split"}

![](media/unicode-e-accent.png)

```{code-cell} ipython3
:cell_style: split

# le codepoint du é accent aigu
codepoint = 0xe9
codepoint
```

```{code-cell} ipython3
:cell_style: split

chr(codepoint)
```

```{code-cell} ipython3
:cell_style: split

ord('é')
```

+++ {"slideshow": {"slide_type": "slide"}}

# pourquoi l’encodage c’est souvent un souci ?

+++

* chaque fois qu'une application écrit du texte dans un fichier
  * elle utilise un encodage
* cette information (quel encodage?) est **parfois** disponible
  * dans ou avec le fichier
  * ex. `# -*- coding: utf-8 -*-`
  * HTTP headers
* mais le plus souvent on ne peut pas sauver cette information
  * pas prévu dans le format
  * il faudrait des **métadata**

+++ {"slideshow": {"slide_type": "slide"}}

## pourquoi l’encodage c’est souvent un souci ?

+++

* du coup on utilise le plus souvent des heuristiques
  * ex: un ordinateur (OS) configuré pour `cp-1252`
  * applications qui utilisent l'encodage défini pour tout l'ordi
* c'est comme ça qu'on reçoit des mails comme
  * `j'ai Ã©tÃ© reÃ§u Ã\xa0 l'Ã©cole`
  * au lieu de
  * `j'ai été reçu à l'école`
* sans parler des polices de caractères..

```{code-cell} ipython3
---
cell_style: center
slideshow:
  slide_type: slide
---
# Jean écrit un mail
envoyé = "j'ai été reçu à l'école"
```

```{code-cell} ipython3
---
cell_style: center
slideshow:
  slide_type: ''
---
# son OS l'encode pour le faire passer sur le réseau
binaire = envoyé.encode(encoding="utf-8")
```

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
# Pierre reçoit le binaire
# mais se trompe d'encodage
reçu = binaire.decode(encoding="cp1252")
```

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
# Pierre voit ceci dans son mailer
reçu
```
