---
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
notebookname: exos
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

# exercices

+++

## comptage dans un fichier

un exercice qui demande 

* d'ouvrir des fichiers en lecture et en écriture
* de faire diverses opérations sur les chaines


https://nbhosting.inria.fr/auditor/notebook/python-mooc:exos/w3/w3-s2-x1-comptage

+++

## la calculette postfix

un exercice pour évaluer les expressions numériques du genre de 

* `10 20 +`  (= 30)
* `30 40 + 30 *`  (=2 100)

**indices**

* cet exercice se prête à l'utilisation d'une pile
* on découpe la chaine en morceaux (des `tokens`)
* on empile les opérandes lorsqu'ils sont des nombres
* lorsqu'on traite un token parmi `+-*/` :
  * on dépile deux fois pour obtenir les opérandes
  * on effectue l'opération
  * on empile le résultat


en version auto-corrigée:

https://nbhosting.inria.fr/auditor/notebook/python-mooc:exos/w6/w6-s9-x1b-postfix

seul le premier exo est obligatoire, les rapides peuvent s'attaquer au second

+++

## le palindrome

+++

### version simple 

écrivez une fonction qui vérifie si une chaine est un palindrome

par exemple

* `palindrome("Eva, Can I Stab Bats In A Cave?")` → `True`
* `palindrome("A Man, A Plan, A Canal-Panama")` → `True`

indice pour ignorer la ponctuation :

```python
In [1]: import string

In [2]: string.punctuation
Out[2]: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
```

+++

### un peu moins simple

même exercice, mais on veut aussi voir pourquoi :

par exemple:

* quand le mot est un palindrome

```python
>>> display_palindrome("kayak")
kayak
kayak
OK
```

* quand il n'en est pas un

```python
>>> display_palindrome("follet")
follet
tellof
^^  ^^
```

pour cette variante on suppose que le mot ne contient pas de ponctuation

+++

## gravity flip

https://www.codewars.com/kata/5f70c883e10f9e0001c89673

+++

## les files de supermarché

https://www.codewars.com/kata/57b06f90e298a7b53d000a86
