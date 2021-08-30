---
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
notebookname: properties
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

# properties

+++

en guise de complément, ce notebook introduit la notion de *property*

+++

## propos

+++ {"tags": []}

on a vu qu'en général, une classe expose

* des attributs, pour accéder directement aux différents 'morceaux' qui constituent une instance
* et des méthodes, qui sont des fonctions

+++

il arrive qu'on se trouve dans une situation un peu mixte, où on voudrait 

* pouvoir accéder aux morceaux de données,
* mais **au travers d'une fonction**; qui puisse, par exemple, faire des contrôles sur la validité des valeurs; ou simplement parce que l'accès en question se fait au travers d'une indirection

+++

## exemple 1 : indirection

+++

imaginez par exemple que vous avez lu une dataframe, qui contient la liste des stations de métro

```{code-cell} ipython3
import pandas as pd

stations = pd.read_csv("data/stations.txt")
```

```{code-cell} ipython3
stations.head(2)
```

et maintenant, on veut définir une classe `Station` pour manipuler ce contenu

```{code-cell} ipython3
class Station:
    def __init__(self, indice):
        self.row = stations.iloc[indice]
```

on a donc une classe qui 'emballe' un objet de type `pandas.Series`  
et on aimerait bien d'exposer un attribut `latitude`, pour pouvoir écrire par exemple

```{code-cell} ipython3
# ce code ne marche pas

class Station:
    def __init__(self, indice):
        self.row = stations.iloc[indice]
    def __repr__(self):
        # ici self.latitude ne veut rien dire
        return f"[Station {self.latitude:.2f}]"
```

mais bien entendu, ça ne fonctionne pas dans l'état, puisque l'attibut `latitude` n'est pas présent dans l'objet `station`

```{code-cell} ipython3
# ça ne marche pas !
# Station(0)
```

ça oblige à écrire plutôt `station.row.latitude` (ou, encore pire, à copier les colonnes de la dataframe sous forme d'attributs - une trè mauvaise idée); mais ça n'est pas du tout pratique, il va falloir se souvenir de cette particularité à chaque fois qu'on aura besoin d'accéder à `latitude`

+++

dans ce premier exemple, on peut s'en sortir simplement avec une *property* :

```{code-cell} ipython3
# maintenant ça fonctionne

class Station:
    def __init__(self, indice):
        self.row = stations.iloc[indice]
    def __repr__(self):
        # plus de problème
        return f"[Station {self.latitude:.2f}]"
    
    # grâce à cett property, on peut accéder à l'attribut self.latitude
    @property
    def latitude(self):
        return self.row.latitude
```

```{code-cell} ipython3
station0 = Station(0)
station0
```

## exemple 2 : une jauge

+++

on veut une classe qui manipule une valeur, dont on veut être sûr qu'elle appartient à un intervalle; disons entre 0 et 100

+++

sans les properties, on est obligé de définir une méthode `set_value`; comme c'est une fonction, elle va pouvoir faire des contrôles

```{code-cell} ipython3
# en définissant un setter
# ça marche mais c'est vraiment moche comme approche

class Gauge:
    def __repr__(self):
        return f"[Gauge {self._value}]"
    def __init__(self, value):
        self.set_value(value)
    def set_value(self, newvalue):
        # on force la nouvelle valeur à être dans l'intervalle
        self._value = max(0, min(newvalue, 100))
```

```{code-cell} ipython3
Gauge(1000)
```

mais à nouveau ce n'est pas du tout pratique :

* d'abord il faut "cacher" l'attribut pour éviter que l'on fasse accidentellement `gauge.value = 1000`
* ensuite du coup il faut aussi exposer une autr méthode `self.get_value()` pour lire la valeur
* et une fois qu'on a fait tout ça, on se retrouve à devoir écrire un code bavard et pas très lisible, bref c'est super moche
* enfin, ça change l'API, et s'il y a déjà du code qui utilise l'attibut `.value` il faut tout changer

pour information, cette technique est celle employée dans les langages comme C++ et Java, on appelle ces méthodes des *getters* et *setters*; pas du tout pythonique comme pratique !

+++

à nouveau dans cette situtation les properties viennent à la rescousse; voici comment ça se présenterait

```{code-cell} ipython3
# version avec une property

class Gauge:
    
    @property
    def value(self):
        return self._value
    
    # la syntaxe pour définir le 'setter' correspondant 
    # à la property 'value'
    # et c'est pour ça bien sûr qu'on écrit '@value'
    @value.setter
    def value(self, newvalue):
        self._value = max(0, min(newvalue, 100))
        
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return f"[Gauge {self._value}]"
```

avec ce code, on peut manipuler les objets de la classe "normalement", 
et pourtant on contrôle bien la validité de la valeur

```{code-cell} ipython3
# à la création
g = Gauge(1000); g
```

```{code-cell} ipython3
# ou à la modification
g.value = -10
g
```

+++ {"tags": ["level_intermediate"]}

## l'autre syntaxe

+++ {"tags": ["level_intermediate"]}

en fait il y a deux syntaxes pour définir une property, choisir entre les deux est une question de goût

voici la deuxième syntaxe utilisée dans la classe `Gauge`

```{code-cell} ipython3
:tags: [level_intermediate]

# version avec une property - deuxième syntaxe

class Gauge:
    
    # je choisis de cacher cette méthode car elle n'est 
    # pas supposée être appelée directement
    def _get_value(self):
        return self._value

    # pareil
    def _set_value(self, newvalue):
        self._value = max(0, min(newvalue, 100))
        
    # la syntaxe pour définir la property
    value = property(_get_value, _set_value)

    # le reste est inchangé        
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return f"[Gauge {self._value}]"
```

```{code-cell} ipython3
:tags: [level_intermediate]

# à la création
g = Gauge(1000); g
```

```{code-cell} ipython3
:tags: [level_intermediate]

# ou à la modification
g.value = -10
g
```

## conclusion

+++

* en Python, on aime bien **accéder aux attributs** d'un objet **directement**, et ne pas **s'encombrer de *getters* et *setters*** qui obscurcissent le code pour rien
* on a parfois besoin que l'accès à un attribut passe par une **couche de logique**
  * soit pour implémenter une indirection
  * soit pour contrôler la validité des arguments
* et dans ces cas-là on **définit une property**
* qui permet de conserver le code existant (pas de changement de l'API)
