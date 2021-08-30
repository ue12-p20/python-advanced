---
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
nbhosting:
  title: 'TP: le fast-food'
---

+++ {"slideshow": {"slide_type": "-"}}

# Le problème du fast-food

On se propose d'illustrer ici la puissance de la programmation asynchrone sur un cas très concret : celui du service dans un restaurant. L'objectif du TP est de vous faire sentir que l'on pense très aisément en asynchrone et que cela peut amener un gain de performances substantiel sur de petits programmes. 

Commençons d'abord comme d'habitude avec les imports :

```{code-cell} ipython3
---
slideshow:
  slide_type: '-'
---
import asyncio
import time
from datetime import datetime
from typing import List, Dict
from asynchelpers import start_timer, show_timer
```

L'idée du TP est de gérer des commandes variés. Chacune des commandes correspond à une liste d'articles qui mettent plus ou moins de temps à être préparés. Vous avez dans la cellule suivante deux dictionnaires : 
 * le premier `TASK_LENGTHS` qui associe à un article la durée de préparation nécessaire ; 
 * le deuxième `ORDERS` qui associe à des clients une liste d'articles. 
Vous pouvez bien entendu ajouter des éléments dans ces deux dictionnaires !

```{code-cell} ipython3
TASKS_LENGTHS = {
    'burger': 2.,
    'fries': 1.5,
    'soda': 0.5,
    'sundae': 1.,
    'coffee': 0.5
}

ORDERS = {
    'A': ['burger', 'fries', 'soda', 'sundae'],
    'B': ['burger', 'fries', 'soda'],
    'C': ['burger', 'burger', 'fries', 'sundae', 'soda'],
    'D': ['coffee'],
    'E': ['burger', 'fries'],
}
```

## Une première approche en programmation synchrone

Nous allons dans un premier temps tenter de résoudre le problème de manière synchrone. Pour cela écrire une fonction `execute(client: str, tasks: List[str])` qui prend en argument le nom du client et sa commande sous la forme d'une liste de chaînes de caractères. Le fragment de code :
```python
start_timer()
execute('A', ORDERS['A'])
```
doit produire une sortie du type: 
```
---------- zero
2s + 002ms burger for client A.
3s + 504ms fries for client A.
4s + 006ms soda for client A.
5s + 007ms sundae for client A.
```

```{code-cell} ipython3
def execute(client: str, tasks: List[str]):
    # À vous !
    pass
```

```{code-cell} ipython3
# Vérifiez votre code ici
start_timer()
execute('A', ORDERS['A'])
```

Pour évaluer la performance du système, il nous faut calculer le temps écoulé entre la commande du client de le service. Pour cela, il faut encapsuler l'appel à `execute` dans un fonction `take_order(client: str, tasks: List[str], order_time: datetime)`. 

**Note :** on utilise ici `datetime.now()` pour récuperer le temps courant.

```{code-cell} ipython3
def take_order(client: str, tasks: List[str], order_time: datetime):
    show_timer(f"Client {client}'s order is treated.")
    execute(client, tasks)
    dtime = datetime.now() - order_time
    print(f">>> Client {client} served in {dtime.seconds} s + {dtime.microseconds//1000:03d} ms.")
```

```{code-cell} ipython3
# Voici un exemple d'appel
start_timer()
take_order('A', ORDERS['A'], datetime.now())
```

Intéressons nous maintenant au cas où plusieurs clients passent des commandes. On pourrait écrire le code suivant :

```{code-cell} ipython3
start_timer()
for client, tasks in ORDERS.items():
    take_order(client, tasks, datetime.now())
```

## Un fonctionnement plus réaliste

Ce code ne représente pas du tout la réalité, car on attend que la commande de `A` soit servie pour prendre celle de `B`. Bien que cela ressemble pas mal au fonctionnement actuel des restaurant, ce n'est pas *nominal*. 

Il faudrait donc être capables d'avoir un conteneur dans lequel on stocke les commandes quand elles sont passées et duquel la cuisine tire ses prochaines tâches. Dans le cadre de la programmation synchrone, cela peut se faire en créant deux objets `Process`. Le conteneur faisant le lien entre les deux sera une `Queue`. Un processus sera responsable d'ajouter les commandes dans la queue au fil de l'eau tandis que le deuxième traitera les commandes. 

**Note sur le fonctionnement des objets `Queue` :** ces objets présentent deux méthode principales :
 * la méthode `get` qui permet de récupérer l'élément le plus ancien de la queue. Si la queue est vide, l'appel est bloquant et on attend qu'un élément soit ajouté à la queue.
 * la méthode `put` qui permet d'ajouter un élément à la queue. 
Pour éviter d'avoir des `Process` qui ne se terminent jamais, il faut pouvoir indiquer à la `Queue` qu'elle a fini de travailler, c'est généralement fait en y mettant `None`. Le process écoutant la queue détecte cela et s'arrête.

**Note sur le fonctionnement des `Process` :** dans le TP actuel, nous allons avoir un usage assez simple des `Process`. Il seront créés et utilisés comme suit : 
```python
# Création des process
proc1 = Process(target=function_to_execute, args=function_args_as_tuple)
proc2 = Process(target=function2_to_execute, args=function2_args_as_tuple)

[p.start() for p in [proc1, proc2]]
[p.join() for p in [proc1, proc2]]
```

Il vous faut donc maintenant écrire deux fonctions qui seront passées aux `Process`. La première `treat_orders(queue: Queue)` écoutera la queue jusqu'à ce que cette dernière renvoie `None` et lancera la préparation en cuisine (un appel à `take_order` en somme). La deuxième `make_orders(orders_dict: Dict[str, List[str]], queue: Queue, delay: float)` parcoura le dictionnaire des commanders (`orders_dict`) et mettra un commande dans la queue à une fréquence donnée par le temps d'attente `delay`.

```{code-cell} ipython3
from multiprocessing import Queue, Process

def treat_orders(queue: Queue):
    # À vous
    pass
        
def make_orders(orders_dict: Dict[str, List[str]], queue: Queue, delay: float):
    # À vous
    pass
```

Si vous avez bien suivi les spécifications précédentes, le code de la cellule suivante devrait bien s'exécuter. Faites varier la valeur de `delay` et regardez l'impact sur le temps d'attente des clients (surtout `D` qui commande seulement un pauvre café).

```{code-cell} ipython3
delay = 1.2

queue = Queue()

processes = [
    Process(target=make_orders, args=(ORDERS, queue, delay)),
    Process(target=treat_orders, args=(queue,))
]

start_timer()
[p.start() for p in processes]
[p.join() for p in processes]
show_timer("Finished")
```

## Et si on passe en asynchrone ? (Version facile, mais peu réaliste)

Dans les faits, la préparation du burger ou des frites ne requièrent pas que le cuisinier reste devant à attendre que ça cuise. L'organisation de la cuisine est donc naturellement asynchrone : on met les frites à cuire et quand friteuse fait **Ding**, les retire en ayant fait autre chose entre temps. 

Nous allons donc réécrire certaines des fonctions précédentes sous la forme de coroutines à commencer par `async def execute(client: str, tasks: List[str])` qui traite de manière asynchrone la commande d'un client.

```{code-cell} ipython3
async def async_execute(client: str, tasks: List[str]):
    # À vous
    pass
```

```{code-cell} ipython3
start_timer()
await async_execute('A', ORDERS['A'])
```

Vous voyez en exécutant la cellule précédente que le temps d'attente est maintenant piloté par la tâche la plus longue. Encapsulons `async_execute` dans `async_take_order` pour mesurer le temps d'attente. (Vous pouvez vous inspirer de l'encapsulation faite en synchrone).

```{code-cell} ipython3
async def async_take_order(client: str, tasks: List[str], order_time: datetime):
    # À vous
    pass
```

Le code de la cellule suivante permet de valider votre implémentation.

```{code-cell} ipython3
start_timer()
await async_take_order('A', ORDERS['A'], datetime.now())
```

Puisque l'objectif même de l'asynchrone est de faire coexister des programmes qui fonctionnent à des fréquences différentes, nous n'aurons pas à passer par un système de queue ici. Il faut juste définir une coroutine `async def async_make_orders(orders_dict: Dict[str, List[str]], delay: float)` qui envoie une commande puis attend `delay` secondes avant d'en envoyer une autre jusqu'à avoir épuisé les commandes. 

**Note :** il faut ici attendre que toutes les commandes aient été traitées avant de quitter la coroutine. Le module `asyncio` implémente pour cela la fonction `wait` qui prend comme argument une liste d'instances de `Task`. Nous avons parlé de `Task` dans les supports de cours, cela peut vous aiguiller sur la stratégie à adopter.

```{code-cell} ipython3
async def async_make_orders(orders_dict, delay):
    # À vous
    pass
```

Le code suivant devrait s'executer sans soucis :

```{code-cell} ipython3
start_timer()
await async_make_orders(ORDERS, 1.2)
```

On voit que les performances sont bien améliorées. Notamment le client `D` est servi en 0.5 secondes contrairement au cas synchrone.

## Un certain manque de réalisme

En mettant la valeur de `delay` à 0, on traite le cas où toutes les commandes sont passées en même temps. Augmentons la taille des commandes en duplicant les données et testez dans la cellule suivante :

```{code-cell} ipython3
MANY_ORDERS = {f"{client}_{i+1}": tasks for client, tasks in ORDERS.items() for i in range(10)}

start_timer()
await async_make_orders(MANY_ORDERS, 0.)
```

On n'est plutôt sur du **as fast as light food** : un nombre incroyable de burgers sont **TOUS** servis aux alentours des 2 secondes. En effet, dans notre code nous n'avons en rien limité notre capacité de préparation. Il peut y avoir un très grand nombre de burgers en préparation en même temps. 

Le moyen de limiter ces ressources est d'utiliser des `asyncio.Lock()` et des `asyncio.Semaphore(int: n)`. Nous vous laissons chercher la syntaxe d'utilisation de ces objets. Sur le principe, si un `Lock` à l'échelle globale est associé aux frites par exemples, lorsqu'un client commandera des frites, une coroutine prendra le `Lock` associé le temps nécessaire (1,5 secondes ici) et le rendra une fois les frites prêtes. Pendant ce temps, aucune autre coroutine ne pourra produire de frites. Les `Semaphore` fonctionne de la même manière mais autorise au plus `n` coroutine en même temps. 

Un exemple de ressources disponibles est proposé dans le dictionnaire `RESSOURCES`:

```{code-cell} ipython3
RESSOURCES= {
    'burger': asyncio.Semaphore(3),
    'fries': asyncio.Lock(),
    'sundae': asyncio.Lock(),
    'coffee': asyncio.Lock(),
    'soda': asyncio.Semaphore(2)
}
```

À vous de jouer maintenant, en redéfinissant les coroutines `async_execute_ressources`, `async_take_order_ressources` et `async_make_orders_ressources` pour prendre en compte ces restrictions. 

**Note :** seule la coroutine `async_execute_ressources` sera très différente des précédentes. ;-)

```{code-cell} ipython3
async def async_execute_ressources(client: str, tasks: List[str]):
    # À vous
    pass

async def async_take_order_ressources(client: str, tasks: List[str], order_time: datetime):
    # À vous
    pass

async def async_make_orders_ressources(orders_dict: Dict[str, List[str]], delay: float):
    # À vous
    pass
```

```{code-cell} ipython3
start_timer()
await async_make_orders_ressources(MANY_ORDERS, 0.)
```

L'idée originale de l'exercice vient de [ce post sur la programmation asynchrone en Python.](https://zestedesavoir.com/articles/1568/decouvrons-la-programmation-asynchrone-en-python/)

```{code-cell} ipython3

```
