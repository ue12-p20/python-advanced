---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
  notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
nbhosting:
  title: TP profiling
---

# Optimisation de code avec les outils de *profiling*

Hubert, votre super co-stagiaire arrivant tout droit de Centrale Gif-Sur-Yvette, vient vous voir tout affolé. Il a écrit un petit script Python pour analyser un jeu de données qui met des plombes à tourner, d'après ses propres mots "plus long qu'un Saclay-Paris un jour de grève". Voilà à peu près ce qu'il vous explique :

- *Hubert :* "Je comprends pas pourquoi ça rame comme ça, j'ai utilisé des dictionnaires pour un accès rapide. Mon code marchait super vite sur une dizaine de données mais maintenant que j'ai pris les 10 000 lignes ça prends presque 20 secondes alors que je calcule une moyenne."
- *P20 :* "Mais pourquoi tu n'utilises pas `numpy.mean` ?"
- *Hubert :* "C'est plus compliqué que ça, j'ai un fichier `data.dat` contenant des résultats de simulations. Les 5 premières colonnes sont les paramètres que j'ai mis en entrée et les deux dernières les résultats. Ensuite, j'ai fait du clustering pour créer des groupes dans toutes ces données. J'ai stocké ça dans `groups.dat`. Le problème c'est que les résultats ne sont pas dans le même ordre dans les deux fichiers. Tu veux bien jeter un coup d'oeil à mon code ?"
- *P20* : "Waah c'est tordu ton truc quand même."

Vous vous retrouvez deux minutes plus tard dans le bureau d'Hubert, il vous montre son code ouvert dans **Notepad** et vous tombez de votre chaise : 

```python
import numpy as np

def main():
    # First data file, model outputs
    # 5 columns of parameters, 2 columns of results
    data1 = np.loadtxt('data.dat')
    params1 = data1[:, :5]
    results = data1[:, 5:]

    # Second data file, groups
    # 5 columns of parameters, 1 column with group
    data2 = np.loadtxt('groups.dat')
    params2 = data2[:, :5]
    groups = data2[:, 5].astype(int)

    # Reordering the data using dict to have 
    # a constant time access.
    myData = dict()
    for params, res in zip(params1, results):
        # Need a hashable as key
        myData[str(params)] = (params, res)

    # Here we will have a list by group
    myGroups = dict()
    for params, group in zip(params2, groups):
        if not group in myGroups.keys():
            myGroups[group] = []
        myGroups[group].append(str(params))

    # Now computing the means per group
    # Here we will store the sum of the first output
    value1 = {key: 0. for key in myGroups}
    # Here we will store the sum of the second output
    value2 = {key: 0. for key in myGroups}
    # Here we will store the number of elements in each group
    number = {key: 0 for key in myGroups}

    for params, res in myData.values():
        for group, elems in myGroups.items():
            if str(params) in elems:
                break
        value1[group] += res[0]
        value2[group] += res[1]
        number[group] += 1

    mean1 = {key: value1[key]/number[key] for key in myGroups}
    mean2 = {key: value2[key]/number[key] for key in myGroups}

    print(mean1, mean2)

if __name__ == '__main__':
    main()
```

En effet c'est pas joli joli, et ça met des plombes à tourner. Vu le contenu algorithmique du script, la lenteur est seulement due à une (très) mauvaise implémentation. Utilisez les outils de profiling que l'on vient de vous présenter pour identifier les opérations qui prennent du temps et creusez vous les méninges pour faire le même boulot bien plus vite.

```{code-cell} ipython3
%%writefile 'script.py'
# Garder cette magic en première ligne du script.
# C'est elle qui permet de sauver le contenu de la cellule
# dans le fichier script.py

import numpy as np

def main():
    # First data file, model outputs
    # 5 columns of parameters, 2 columns of results
    data1 = np.loadtxt('data/data.dat')
    params1 = data1[:, :5]
    results = data1[:, 5:]

    # Second data file, groups
    # 5 columns of parameters, 1 column with group
    data2 = np.loadtxt('data/groups.dat')
    params2 = data2[:, :5]
    groups = data2[:, 5].astype(int)

    # Reordering the data using dict to have 
    # a constant time access.
    myData = dict()
    for params, res in zip(params1, results):
        # Need a hashable as key
        myData[str(params)] = (params, res)

    # Here we will have a list by group
    myGroups = dict()
    for params, group in zip(params2, groups):
        if not group in myGroups.keys():
            myGroups[group] = []
        myGroups[group].append(str(params))

    # Now computing the means per group
    # Here we will store the sum of the first output
    value1 = {key: 0. for key in myGroups}
    # Here we will store the sum of the second output
    value2 = {key: 0. for key in myGroups}
    # Here we will store the number of elements in each group
    number = {key: 0 for key in myGroups}

    for params, res in myData.values():
        for group, elems in myGroups.items():
            if str(params) in elems:
                break
        value1[group] += res[0]
        value2[group] += res[1]
        number[group] += 1

    mean1 = {key: value1[key]/number[key] for key in myGroups}
    mean2 = {key: value2[key]/number[key] for key in myGroups}

    print(mean1, mean2)

if __name__ == '__main__':
    main()
```

Vous pouvez utiliser la cellule ci-dessous avec un `!` comme ligne de commande terminal. À chaque fois que vous évaluez la cellule précédente, le fichier `script.py` est écrasé.

```{code-cell} ipython3
! python -m cProfile script.py
```
