---
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
notebookname: "\xE9crire un lanceur"
---

+++ {"slideshow": {"slide_type": "-"}, "tags": []}

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat</span>
</div>

<style>
.smaller {font-size: smaller}
</style>

+++ {"slideshow": {"slide_type": ""}}

# écrire un lanceur / point d'entrée

+++

Quand on écrit un projet en Python, on peut publier uniquement une librairie : un paquet de classes, de fonctions, destinées à être utilisées depuis une autre application.

Il est parfois aussi utile de publier un vrai "lanceur", c'est-à-dire un programme complet, destiné à être lancé en tant que tel avec une commande dans le terminal, genre

```console
$ python script.py
```

On appelle alors ce fichier `script.py` un **lanceur**, ou encore un **point d'entrée**

+++

## lire les arguments

+++

Il est souvent utile de pouvoir passer à ce lanceur **des paramètres**

Par exemple si vous avez écrit un programme qui calcule la factorielle, on veut pouvoir passer au lanceur l'entier dont on veut calculer la factorielle, en écrivant 

```console
$ python factorielle.py 6
factorial(6)=720
```

+++

Il nous faut donc trouver un moyen de "faire passer" ce paramètre `6` depuis le terminal jusqu'à l'application Python; pour cela on dispose de deux mécanismes :

* `sys.argv`
* le module `argparse`

De manière générale, sauf dans les cas simplissimes, il est préférable d'utiliser le second, bien qu'un tout petit peu plus complexe que le premier; voyons cela

+++

## `sys.argv`

+++

Python permet de retrouver la commande de lancement du point d'entrée au travers de l'attribu `sys.argv`, sous la forme d'une liste de chaines (la commande initiale est découpée selon les espaces)

+++

Considérons pour commencer le programme suivant

```{code-cell} ipython3
# %cat est une 'magic' de IPythion
# qui permet d'afficher le contenu de fact_sysargv.py

%cat fact_sysargv.py
```

```{code-cell} ipython3
# avec le ! je fais comme si je tapais ça dans le terminal
!python fact_sysargv.py 6
```

Cette mécanique fonctionne mais présente **de gros défauts** :

* principalement, on ne fait **aucun contrôle** sur les paramètres; si vous appelez le programme avec trop ou pas assez d'arguments, il se passe des trucs pas forcément très nets
* et si vous ne vous souvenez plus de comment il faut appeler le programme, vous en êtes quittes pour retrouver et relire le code...

```{code-cell} ipython3
# par exemple si on essaie de lancer le programme sans le paramètre
# on obtient une erreur - c'est normal - 
# mais franchement ce n'est pas très clair de comprendre ce qu'on a mal fait

! python fact_sysargv.py
```

```{code-cell} ipython3
# et avec deux paramètres, le second est simplement ignoré...

! python fact_sysargv.py 6 20
```

## les options

+++

en plus de tout cela, il arrive fréquemment qu'on ait envie de passer des **options**; par exemple, notre programme pourrait avoir deux modes d'affichage, bavard ou pas.

traditionnellement, les options **commencent par un tiret haut**, comme ceci :

```{code-cell} ipython3
# le -v est une option (v pour verbose)
# du coup le programme fonctionne en mode bavard

! python fact_sysargv2.py -v 6
```

```{code-cell} ipython3
# sans option il marche en mode silencieux, pas de baratin

! python fact_sysargv2.py 6
```

Vous pouvez regarder le code de `fact_sysargv2.py` pour voir comment on a implémenté cela; notez surtout que le code devient vite un peu torturé, même pour traiter ce cas hyper-simple où on n'a qu'une seule option

+++

## `argparse`

+++

`argparse` est un module de la librairie standard, conçu spécialement pour traiter de manière plus lisible ce genre de cas

on ne va pas ici entrer dans les détails, mais simplement montrer le code qui se comporterait comme `fact_sysargv2`.py

```{code-cell} ipython3
%cat fact_argparse.py
```

ce code peut sembler un peu plus bavard que tout à l'heure; mais d'abord il donne un programme plus agréable à utiliser

```{code-cell} ipython3
# si on ne passe pas les paramètres imposés, 
# le programme ne fait rien, 
# mais il nous explique comment on aurait dû l'appeler
! python fact_argparse.py
```

```{code-cell} ipython3
# on peut avoir de l'aide
! python fact_argparse.py --help
```

```{code-cell} ipython3
# et les options sont disponibles en version courte 
# (-v comme tout à l'heure)
# mais aussi en version longue
! python fact_argparse.py --verbose 6
```

mais fondamentalement, le plus gros avantage c'est la lisibilité, et la simplicité de maintenance, car analyser les options "à la main" devient rapidement compliqué, fouillis, et donc peu lisible et peu maintenable.

+++

pour tous les détails sur `argparse`, [reportez-vous à ce tutoriel](https://docs.python.org/3/howto/argparse.html)

+++ {"tags": ["level_intermediate"]}

## packaging

+++

on va conclure ce notebook sur une note plus avancée

si maintenant vous avez besoin que votre lanceur s'installe en même temps que le reste de votre librairie, vous allez utilisez `setup.py` et écrire une clause comme ceci :

+++

```python
setup(
    ...,
    entry_points={
        'console_scripts': [
            'lanceur = monpackage.fact_argparse:main',
        ]
)
```

+++

et de cette façon, après avoir installé le package avec `pip install` (localement ou pas), vous ou votre utilisateur pourra lancer la commande `bidule` qui sera branchée sur la fonction `main` du module `monmodule` dans le package `monpackage`

+++

pour davantage de détails, [reportez-vous à la documentation de `setuptools` à ce sujet](https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#entry-points-and-automatic-script-creation)

+++

## conclusion

+++

on vient de voir l'essentiel des techniques qui permettent d'écrire un lanceur en Python

comme vous l'avez compris on recommande d'utiliser `argparse`, de préférence à l'accès direct à `sys.argv`, qui donne un code plus lisible, plus maintenable, et beaucoup plus court dans la plupart des cas réels

enfin pour installer de tels lanceurs, il est préférable de sous-traiter le travail à `setuptools`, qui se chargera de tous les détails - souvent sordides - pour une installation propre sur tous les OS de vos éventuels utilisateurs
