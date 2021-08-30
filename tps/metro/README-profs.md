---
jupytext:
  cell_metadata_filter: all, -hidden, -heading_collapsed, -run_control, -trusted
  cell_metadata_json: true
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
notebookname: "m\xE9tro parisien"
version: '1.0'
---

# le réseau du métro parisien

+++

<img src="media/metro-map.png" width="600px" />

```{code-cell} ipython3
from pathlib import Path
import numpy as np
import pandas as pd
```

## introduction

+++

### les données

+++

on vous a préparé deux jeux de données qui décrivent le métro parisien

```{code-cell} ipython3
# a few constants
data = Path("data")
```

```{code-cell} ipython3
# load data
stations  = pd.read_csv(data / "stations.txt", index_col="station_id")
hops =      pd.read_csv(data / "hops.txt")
```

```{code-cell} ipython3
:cell_style: split

stations.head()
```

```{code-cell} ipython3
:cell_style: split

hops.head()
```

**SOURCE :** à l'origine [la source de ces données est la RATP](https://dataratp2.opendatasoft.com/explore/dataset/offre-transport-de-la-ratp-format-gtfs/information/) et [plus précisément ceci](http://dataratp.download.opendatasoft.com/RATP_GTFS_LINES.zip), prétraité par nos soins

**DISCLAIMER** comme vous le verrez ces données ne sont pas parfaites, mais dans l'ensemble c'est un niveau de qualité suffisant pour notre propos d'aujourd'hui.

+++

### ce qu'on veut en faire

1. dessiner le réseau sur une carte
1. s'en servir de support pour visualiser deux algorithmes de parcours de graphe
  * DFS : *depth-first-search*
  * BFS : *breadth-first-search*

+++

### comment on se propose de le faire

1. construire une structure de données pour
  * ranger le graphe,
  * pouvoir le parcourir rapidement/efficacement
2. afficher la carte avec la librairie `folium`
3. parcours :
  1. implémenter les 2 parcours de graphe
  1. numéroter les stations (en partant de Chatelet) selon les deux parcours
  1. afficher les résultats

+++

## les algorithmes de parcours

Il y a deux algorithmes standard pour parcourir un graphe à partir de l'un de ses sommets :

* DFS (depth-first-scan)
* BFS (breadth-first scan)

intuitivement, en partant de cet échantillon (ici un simple arbre) :

```{code-cell} ipython3
from simpletree import tree

tree
```

+++ {"cell_style": "split"}

DFS donnerait l'énumération suivante (les sauts de ligne ne sont pas significatifs) :
```
v v1 v11 v111 v112
v12 v121 v122
v2 v21 v211 v212
v22 v221 v222
```

+++ {"cell_style": "split"}

alors que BFS verrait au contraire :
```
v
v1 v2
v11 v12 v21 v22
v111 v112 v121 v122 v211 v212 v221 v222
```

+++

pour simplifier au maximum les deux algorithmes de parcours que l'on veut implémenter, on peut les décrire informellement de la façon suivante :

* en entrée on nous passe le sommet qui sert de point de départ `start`
* on initialise un ensemble vide de sommets `scanned`  
  qui contiendra tous les sommets qu'on a déjà parcourus
* on initialise une file d'attente `waiting_area`, dans laquelle on met `start`
* le parcours consiste alors à faire, tant que `waiting_area` n'est pas vide :
  * prendre (et enlever) un élément `next` de `waiting_area`  
    l'afficher (ou en faire ce que le parcours doit en faire)
  * ajouter `next` dans `scanned` pour matérialiser le fait qu'on y est déjà passé
  * pour tous les voisins de `waiting_area` qui ne sont pas encore dans `scanned`, les ajouter dans `waiting_area`

+++

ce qui est assez remarquable, c'est que les deux ordres de parcours (DFS et BFS) peuvent être toutes les deux réalisés avec ce même algorithme, la seule chose qui change entre les deux étant l'ordre dans lequel `waiting_area` "rend" les choses qu'on y insère

ainsi si `waiting_area` est une FILO (first-in-last-out), l'algorithme ci-dessus fait un parcours DFS

et inversement si `waiting_area` est une FIFO (first-in-first-out), alors on parcourt le graphe en BFS

c'est ce que nous visualiserons à la fin de ce TP

+++

## structures de données - intro

+++

on va représenter le graphe avec plusieurs classes d'objet :
* `Station` : contient les détails de l'arrêt ; ici on n'a gardé, parmi tous les détails exposés par la RATP, que les coordonnées latitude et longitude, mais dans un exemple plus réaliste on pourrait avoir ici plein de détails...
* `Node` : modélise un noeud (sommet) dans le graphe, et ses noeuds voisins ;
* `Graph` : contient l'ensemble des noeuds du réseau.

+++

![](media/data-structures.png)

+++

## spécifications

+++

### specs (1) : construction du graphe

+++

voici pour commencer le code qu'on **aimerait pouvoir écrire**

```{code-cell} ipython3
# on rappelle que stations et hops sont des dataframes
# on peut itérer sur les lignes d'une dataframe avec iterrows()

def build_graph(stations: pd.DataFrame, hops: pd.DataFrame):

    graph = Graph()

    # créer un node par station
    for index, station in stations.iterrows():
        node = graph.add_node(station)

    # créer une arête par hop, annotée par le numéro de ligne
    for index, hop in hops.iterrows():
        graph.add_edge(hop['from_station_id'], hop['to_station_id'], hop['line'])

    return graph
```

ainsi une fois qu'on aura implémenté la classe `Graph` (et la classe `Node` sous-jacente) on pourra construire notre graphe en écrivant

```python
metro = build_graph(stations, hops)
```

+++

### specs (2) : dessin de la carte

+++

pour ce qui est d'afficher le réseau sur une carte, le code qu'on va vouloir écrire ressemble à ceci (on reparlera plus en détail de la librairie `folium` en temps voulu) :

```python
def build_map(metro: Graph, show_labels=True):

    map = folium.Map(...)

    for node in metro.iter_nodes():
        # si le noeud a un label
        if show_labels and node.label:
            # l'afficher à la position du noeud
            # donc on a besoin d'accéder à
            node.latitude, node.longitude, node.label

    # quand on itère sur les arêtes on retourne
    # un triplet avec le numéro de ligne
    # qu'on utilisera ici pour trouver la couleur attachée à chaque ligne
    for node, neighbour, line in metro.iter_edges():
        # pour tracer un trait entre les deux
        # on a besoin d'accéder à
        (node.latitude, node.longitude),
        (neighbour.latitude, neighbour.longitude)

    return map
```

+++

### specs (3) : parcours

+++

en ce qui concerne les algorithmes de parcours, compte tenu de ce qu'on a vu plus haut, le code qu'on va vouloir écrire aura besoin aussi d'itérer sur les voisins d'un noeud, et ressemblera schématiquement à ceci :

```{code-cell} ipython3
def scan(start_node, storage):

    storage.store(start_node)
    ...

    while storage:
        current_node = storage.retrieve()

        ...

        for neighbour, line in current_node.iter_neighbours():
            storage.store(neighbour)
```

### specs : résumé

+++ {"cell_style": "split"}

pour résumer les besoins sur les classes `Graph` et `Node` :

```python3

# création
node = graph.add_node(station)

graph.add_edge(
   from_station_id, to_station_id, line)

# parcours des noeuds
for node in graph.iter_nodes():
   # accès à partir d'un noeud
   node.station, node.label
   node.latitude, node.longitude

# parcours des arêtes
for node, neighbour, line in graph.iter_edges():
   ...

for neighbour, line in node.iter_edges():
   ...
```

+++ {"cell_style": "split"}

et on peut ajouter quelques fonctions de confort

```python3

len(graph) # le nombre de noeuds

graph.nb_edges()

graph.find_node_from_station_id(
    station_id)

node.nb_edges()

```

+++

## implémentation

+++

### le type `Station`

+++

pour le type Station on n'a rien à écrire, c'est l'intérêt d'avoir séparé la couche 'données' (dataframe) de la couche 'connectivité' (Graph), un objet de type `Station` est en fait une instance de `pandas.Series`

et rappelez-vous, pour accéder à une dataframe on peut utiliser:

* `df.loc[]` pour les accès par index (notre cas ici)
* `df.iloc[]` pour les accès par indice (pas utile ici)

du coup, voici comment utiliser les objets de type `Station`

```{code-cell} ipython3
# le type Station correspond à une ligne
# dans la dataframe chargée à partir de stations.txt
# ce serait assez redondant d'avoir à se redéfinir un type pour cela

# et grâce à la dataframe - que l'on a indexée par station_id
# on peut trouver la station correspondant à un station_id
# par accès direct (comme dans un dictionnaire)


# si je cherche par exemple la station dont l'id vaut 2152
station_sample = stations.loc[2152]
station_sample
```

```{code-cell} ipython3
# pour accéder aux positions géographiques c'est simple
station_sample.latitude
```

```{code-cell} ipython3
# par contre pour accéder au station_id, qui sert d'index,
# c'est différent
try:
    station_sample.station_id
except Exception as exc:
    print(f"OOPS - {type(exc)} : {exc}")
```

```{code-cell} ipython3
# il faut utiliser l'attribut name (ça n'est pas très logique d'ailleurs !)
station_sample.name
```

```{code-cell} ipython3
station_sample.name
```

```{code-cell} ipython3
:cell_style: split

# quel est le type de cet objet
type(station_sample)
```

```{code-cell} ipython3
:cell_style: split

# définissons un type pour les type hints
Station = pd.Series
```

### le type `Node`

pour modéliser les relations entre stations, on *enrobe* le type `Station` avec un objet `Node` qui possède une référence vers une station, et aussi vers les noeuds voisins

la première idée consisterait à garder dans un attribut `self.neighbours` un `set` d'objets `Node` (c'est d'ailleurs ce qu'on a représenté sur le diagramme simplifié ci-dessus)

mais il se trouve que dans `hops.txt` on nous donne aussi le numéro de la ligne de métro qui connecte deux stations, on va donc vouloir attacher à chaque lien ce numéro de ligne, et du coup un ensemble n'est sans doute pas ce qu'il y a de mieux...

```{code-cell} ipython3
# version étudiant : à vous de compléter le code

class Node:
    """
    a node has a reference to a unique Station object
    and also logically a set of neighbours,
    each tagged with a line among the 14 metro lines
    finally it has an optional 'label' attribute that we will use when
    drawing the graph on a map
    """
    def __init__(self, station: Station):
        # xxx ...
        self.station = station
        # use a dictionary to attach a value to each link (here the line number)
        self.line_by_neighbour = dict() # type: Dict[Node -> str]
        self.label = None

    # xxx remove
    def __repr__(self):
        return str(f"[Node {self.station.name}]")

    def add_edge(self, neighbour: "Node", line):
        # xxx ...
        self.line_by_neighbour[neighbour] = line

    def nb_edges(self):
        # xxx ...
        return len(self.line_by_neighbour)

    def iter_neighbours(self):
        "iterates (neighbour, line) over neighbours"
        # xxx ...
        for neighbour, line in self.line_by_neighbour.items():
            yield neighbour, line

    # we also need to be able to use
    # node.latitude
    # node.longitude
    # xxx remove
    @property
    def latitude(self):
        return float(self.station['latitude'])

    @property
    def longitude(self):
        return float(self.station['longitude'])
```

```{code-cell} ipython3
# version étudiant : à vous de compléter le code

# NOTE : vous remarquerez qu'on a choisi de créer les arêtes
# à partir de `station_id`s
# il faut donc pouvoir retrouver un noeud à partir de cette information

class Graph:
    """
    the toplevel object that models the complete graph
    as essentially a set of nodes (thus of stations)
    """
    def __init__(self):
        # xxx ...
        self.nodes = set()
        # for efficiency we also maintain an index of those hashed by station_id
        self.nodes_by_station_id = {}

    def add_node(self, station):
        """
        insert a station in graph; duplicates are simply ignored
        """
        # xxx ...
        # this is how to retrieve the 'index' column
        # in an indexed dataframe (must not be indexed with inplace=True)
        station_id = station.name

        # don't add it if already there
        if station_id in self.nodes_by_station_id:
            return
        node = Node(station)
        self.nodes.add(node)
        self.nodes_by_station_id[station_id] = node

    def find_node_from_station_id(self, station_id):
        """
        spot a node from a specific station id
        """
        # xxx ...
        return self.nodes_by_station_id[station_id]

    def add_edge(self, from_station_id, to_station_id, line):
        """
        insert an edge - both ends must exist already
        """
        # xxx ...
        # locate both ends that MUST be present already
        node_from = self.find_node_from_station_id(from_station_id)
        node_to = self.find_node_from_station_id(to_station_id)
        if not node_from or not node_to:
            print(f"OOPS - cannot add edge {from_station_id}->{to_station_id}")
            return
        node_from.add_edge(node_to, line)

    def iter_nodes(self):
        """
        an iterator on nodes
        """
        # xxx ...
        return iter(self.nodes)

    def iter_edges(self):
        """
        iterates over triples (node_from, node_to, line)
        """
        # xxx ...
        for node in self.iter_nodes():
            for neighbour, line in node.iter_neighbours():
                yield node, neighbour, line

    # optionnel
    def __len__(self):
        # xxx ...
        return len(self.nodes)

    def nb_edges(self):
        # xxx ...
        return sum(node.nb_edges() for node in self.nodes)
```

## construction du graphe

+++

maintenant on devrait pouvoir construire le graphe

```{code-cell} ipython3
metro = build_graph(stations, hops)

print(f"notre graphe a {len(metro)} stations et {metro.nb_edges()} liens")
```

```{code-cell} ipython3
# exercice: calculer le nombre de lignes
# xxx nb_lines = ...
lines = {line for node, neighbour, line in metro.iter_edges()}
nb_lines = len(lines)

print(nb_lines)
```

## dessiner le graphe sur une carte

+++

on va utiliser la librairie `folium` pour afficher les cartes

pas de code à écrire de votre part dans cette partie, mais vous pouvez prendre le temps de voir comment c'est fait

```{code-cell} ipython3
import folium

STATION_RADIUS = 100
MARKER_DIAMETER = 20

LINE_WIDTH = 7.5
STATION_COLOR = '#d22'
```

### les couleurs des lignes

```{code-cell} ipython3
from nuancier import nuancier
nuancier
```

### afficher les labels

pour mettre en évidence une station (un peu fastidieux en folium)

```{code-cell} ipython3
from labelicon import label_icon
```

### Chatelet au centre de la carte

```{code-cell} ipython3
chatelet_station_id = 2221
chatelet_station = stations.loc[chatelet_station_id]
```

```{code-cell} ipython3
map_center = [chatelet_station['latitude'], chatelet_station['longitude']]
```

### ma première carte en folium

```{code-cell} ipython3
autre_station = stations.loc[2122]
autre_position = [autre_station['latitude'], autre_station['longitude']]

une_couleur = nuancier["7"]
```

On n'aura besoin que des classes suivantes

* `folium.map`
* `folium.map.Marker` pour attacher un label à chaque station
* `folium.Circle`
* `folium.PolyLine` pour tracer un trait

```{code-cell} ipython3
map = folium.Map(location=map_center, zoom_start=13)

folium.map.Marker(map_center, icon=label_icon('0')).add_to(map)
folium.Circle(map_center, STATION_RADIUS,
              fill=True, fill_color=une_couleur).add_to(map)

folium.map.Marker(autre_position, icon=label_icon('100')).add_to(map)
folium.Circle(autre_position, STATION_RADIUS,
              fill=True, fill_color=une_couleur).add_to(map)

folium.PolyLine([map_center, autre_position],
                weight=LINE_WIDTH, color=une_couleur).add_to(map)

map
```

### contruire une `folium.Map` à partir du graphe

+++

Nous voulons visualiser les stations, et les lignes. En option (si `show_labels=True`), on affichera aussi l'attribut `label` des objets `Node` lorsqu'il est défini.

```{code-cell} ipython3
def build_map(metro, show_labels=True):

    map = folium.Map(location=map_center, zoom_start=13)

    for node in metro.iter_nodes():
        if show_labels and node.label:
            folium.map.Marker(
                [node.latitude-0.0001, node.longitude-0.0001],
                icon=label_icon(node.label)
            ).add_to(map)
        folium.Circle(
            [node.latitude, node.longitude],
             STATION_RADIUS,
             fill=True,
             fill_color=STATION_COLOR,
        ).add_to(map)
    for node, neighbour, line in metro.iter_edges():
        line_color = nuancier[line]
        locations = [(node.latitude, node.longitude),
                     (neighbour.latitude, neighbour.longitude)]
        folium.PolyLine(locations=locations,
                        weight=LINE_WIDTH, color=line_color).add_to(map)

    return map
```

à ce stade si votre code pour `Node` et `Graph` est correct vous pouvez voir ici la carte du réseau avec la station Chatelet numérotée `0`

```{code-cell} ipython3
# on met au moins un label pour voir l'effet
metro.find_node_from_station_id(chatelet_station_id).label = '0'

build_map(metro)
```

## parcours : implémentation et illustration

+++

### rappel des objectifs

+++

nous voulons écrire un **generateur** qui implémente les deux stratégies de parcours, à partir d'un sommet du graphe

bien entendu, seuls les sommets accessibles seront parcourus, ce qui dans notre cas n'a pas d'importance puisque le graphe du métro est connexe

+++

nous avons vu qu'on pouvait unifier les deux parcours, en utilisant une file d'attente FIFO ou FILO selon le parcours que l'on veut faire

nous avons simplement besoin dans les deux cas d'un objet `Storage` qui implémente `store()` et `retrieve()` avec la bonne politique; aussi de manière accessoire on a besoin de pouvoir tester si une file est vide ou non, c'est à dire de pouvoir écrire `while storage: ...`

+++

### FIFO / FILO

```{code-cell} ipython3
:cell_style: split

from collections import deque
class Fifo:
    def __init__(self):
        # xxx ...
        self.line = deque()
    def store(self, item):
        # xxx ...
        self.line.append(item)
    def retrieve(self):
        # xxx ...
        if self.line:
            return self.line.popleft()
    # pour 'while storage:'
    def __len__(self):
        # xxx ...
        return len(self.line)
```

```{code-cell} ipython3
:cell_style: split

from collections import deque
class Filo:
    def __init__(self):
        # xxx ...
        self.line = deque()
    def store(self, item):
        # xxx ...
        self.line.append(item)
    def retrieve(self):
        # xxx ...
        if self.line:
            return self.line.pop()
    # ditto
    def __len__(self):
        # xxx ...
        return len(self.line)
```

```{code-cell} ipython3
:cell_style: split

# pour vérifier
fifo = Fifo()
for i in range(1, 4):
    fifo.store(i)
while fifo:
    print(f"retrieve → {fifo.retrieve()}")
```

```{code-cell} ipython3
:cell_style: split

# pour vérifier
filo = Filo()
for i in range(1, 4):
    filo.store(i)
while filo:
    print(f"retrieve → {filo.retrieve()}")
```

### parcours générique

```{code-cell} ipython3
# avec nos spécifications, on peut écrire le parcours
# en utilisant principalement
# for neighbour, line in node.iter_neighbours():
#
def scan(start_node, storage):
    """
    scan all vertices reachable from start vertex
    in an order that is DF or BF depending on the
    storage policy (fifo or filo)
    storage should have store() and retrieve() methods
    and be testable for emptiness (if storage: ...)
    also it should be empty when entering the scan
    """

    storage.store(start_node)
    # keep track of what we've seen
    # xxx ...
    scanned = set()

    while storage:
        # xxx ...
        current_node = storage.retrieve()
        # skip vertices already seen
        # station.name is actually station['station_id']
        # but it is now indexed
        if current_node.station.name in scanned:
            continue
        yield current_node
        scanned.add(current_node.station.name)
        for neighbour, line in current_node.iter_neighbours():
            storage.store(neighbour)
```

### les deux parcours spécifiques

```{code-cell} ipython3
def DFS(metro, station):
    node = metro.find_node_from_station_id(station.name)
    storage = Filo()
    yield from scan(node, storage)
```

```{code-cell} ipython3
def BFS(metro, station):
    node = metro.find_node_from_station_id(station.name)
    storage = Fifo()
    yield from scan(node, storage)
```

### illustration

+++

pour illustrer les deux parcours, on va simplement utiliser l'attribut `label` des noeuds, et y ranger l'ordre dans lequel se fait le parcours

+++

#### depth-first scan

```{code-cell} ipython3
# labelling all stations according to a DFS scan
for index, node in enumerate(DFS(metro, chatelet_station)):
    node.label = str(index)
print(f"index={index}")
build_map(metro)
```

#### breadth-first scan

```{code-cell} ipython3
# same with a BFS
for index, node in enumerate(BFS(metro, chatelet_station)):
    node.label = str(index)
print(f"index={index}")
build_map(metro)
```
