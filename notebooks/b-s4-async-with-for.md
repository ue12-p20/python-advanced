---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

<span style="float:left;">Licence CC BY-NC-ND</span><span style="float:right;">Thierry Parmentelat<img src="media/inria-25-alpha.png" style="display:inline"></span><br/>

+++ {"slideshow": {"slide_type": "slide"}}

# extensions asynchrones du langage

Vous avez maintenant compris dans les grandes lignes à quoi sert asyncio; on a vu aussi
très sommairement les notions de coroutines et de boucle d'événement, maintenant dans
cette séquence nous allons voir des exemples, toujours assez simples mais plus réalistes,
de codes asyncio.

+++ {"slideshow": {"slide_type": "slide"}}

## accès http avec `async with`

Pour commencer nous allons voir comment faire par exemple des accès concurrents à
plusieurs pages web. Imaginons qu'on a plusieurs pages web à aller chercher

```{code-cell} ipython3
import time

urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
        "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]
```

+++ {"slideshow": {"slide_type": "slide"}}

##### en version séquentielle

Comme on l'a vu en introduction, si on va chercher ces 4 pages séquentiellement ça peut
prendre un certain temps, selon les conditions réseau ... ici pour moi environ 12s - ça
dépend bien sûr de vos conditions réseau.

```{code-cell} ipython3
import requests

beg = time.time()

for url in urls:
    req = requests.get(url)
    print(f"{url} returned {len(req.text)} chars")

print(f"duration = {time.time()-beg}s")
```

Alors souvenez-vous, on a bien dit qu'avec `asyncio` on allait pouvoir simplement faire la
même chose mais de manière concurrente, sans bloquer l'exécution entre tous les délais
réseau qui interviennent ici.

Alors voyons cela. Je commence par importer la librairie `aiohttp` qui est, vous l'avez
compris, une version asynchrone pour aller chercher des pages web.

Je dois vous signaler que cette librairie n'est **pas dans la librairie standard**, vous
devez l'installer comme d'habitude avec
`pip install aiohttp`.

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
import asyncio
import aiohttp
```

grâce à quoi je peux construire une coroutine qui va chercher une page web, je l'ai
appelée `fetch`.

Comment ça marche ? de manière assez standard, je construis un objet session; à
l'intérieur de cette session, je crée une requête avec `session.get()`, pour obtenir un
objet `response`, sur lequel je peux lire le contenu brut de la page web.

Ce qui est intéressant ici, c'est la syntaxe `async with` - vous en voyez ici deux
exemplaires; de même qu'en python synchrone on peut faire `with` sur un context manager,
on peut faire `async with` sur un context manager asynchrone.

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
async def fetch(url):

    async with aiohttp.ClientSession() as session:
        print(f"fetching {url}")

        async with session.get(url) as response:
            #print(f"{url} returned status {response.status}")
            raw = await response.read()
            print(f"{url} returned {len(raw)} bytes")
```

C'est quoi un context manager asynchrone ?

Rappelez-vous, on ouvre un fichier avec un `with` pour être bien sûr de fermer le fichier;
un context manager normal a deux étapes prédéfinies qu'on exécute au début et à la fin du
`with` (ce sont les dunder rméthodes `__enter__` et `__exit__`)

Eh bien c'est comme un context manager normal, sauf que les deux étapes de
construction/destruction sont faites aussi de manière asynchrone - au travers d'un await -
(et elles s'appellent `__aenter__` et `__aexit__`)

Ça se prête donc très bien à toutes les applications réseau ou autres bases de données, où
la création du contexte, et aussi sa destruction, sont au moins aussi asynchrones que ce
qu'on fait avec

Ici par exemple, pour créer l'objet `session` on doit créer une connexion réseau, c'est
une étape relativement lente, il est important que l'on ne garde pas le processeur pendant
ce temps-là.

Bref, la construction 'async with' est très fréquente dans du code asynchrone.

Je vous [signale à cet égard la
PEP-0492](https://www.python.org/dev/peps/pep-0492/#asynchronous-context-managers-and-async-with),
si vous voulez creuser tout ceci, qui explique ce protocole de *context manager*
asynchrone, et dont je vous recommande la lecture si vous décidez de vous lancer avec
asyncio.

+++

Je peux maintenant utiliser gather pour aller chercher mes 4 URLs en même temps. Pour cela
je crée une coroutine fetch_urls,

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# une coroutine qui va chercher toutes les URLs
# ne fait toujours rien, naturellement
async def fetch_urls():
    await asyncio.gather(*(fetch(url) for url in urls))
```

que je peux ensuite invoquer au travers d'une boucle d'événements, comme on l'a déjà vu,
et cette fois avec ce code

```{code-cell} ipython3
---
slideshow:
  slide_type: fragment
---
beg = time.time()
await fetch_urls()
print(f"duration = {time.time()-beg}s")
```

qui va chercher mes quatre pages, tout est fait en même temps, je n'ai pas perdu de temps
à attendre, les 4 requêtes se déroulent complètement en même temps, pour moi ça ne prend
que 2 secondes environ, soit le délai que j'avais observé pour le plus lent des 4 liens.

+++ {"slideshow": {"slide_type": "slide"}}

## itérations asynchrones

De la même façon, le langage supporte les itérateurs asynchrones, et aussi les
compréhensions asynchrones (ajoutées plus tard [dans la
PEP-530](https://www.python.org/dev/peps/pep-0530/))

Voyons tout d'abord un exemple pratique; je vais reprendre le même exemple, ça a le mérite
d'être simple, mais plutôt que de lire d'un seul coup tout le contenu de la page web,
imaginons que je veuille traiter les lignes au fur et à mesure qu'elles arrivent.

```{code-cell} ipython3
import asyncio

# une variante
async def fetch2(url, i):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # avec ici une itération asynchrone
            async for line in response.content:
                print(f'{i}', end='')
    return url
```

C'est un exemple un peu artificiel, mais ce serait la même chose avec par exemple une
requête de base de données, ou similaire.

J'ai repris le code de fetch, mais cette fois j'utilise un for asynchrone `async for` pour
lire les lignes au fur et à mesure.

Malgré le fait que je ne fais aucun `await` explicitement dans ce `for`, les lignes sont
bel et bien lues de manière asynchrone et pour bien le montrer, j'imprime en vrac l'indice
de l'URL, que l'on va bien voir arriver dans le désordre.

```{code-cell} ipython3
# un peu de gymnastique pour passer à gather les 4 coroutines
await asyncio.gather(*(fetch2(url, i) for i, url in enumerate(urls)))
```

## résumé (1)

À ce stade, c'est certainement utile que l'on fasse un résumé de ce que nous avons vu
jusqu'ici au sujet des extensions asynchrones du langage à proprement parler;

Nous avons vu jusqu'ici

* la notion de coroutine; j'insiste bien à nouveau sur la différence entre une fonction
  coroutine (qui est définie par `async def`) et ce qu'elle renvoie, un objet coroutine.

* le fait d'appeler une coroutine n'exécute rien, cela renvoie immédiatement un objet
  coroutine qui ne provoquera une exécution que si on lui applique un await, ou si on la
  passe à une boucle d'évènements

* tout ceci n'a de sens qu'au travers d'une boucle d'événements, qui joue le rôle de
  *scheduler*; même si on ne crée pas explicitement de *event loop*, lorsqu'on utilise
  `await` depuis le toplevel cela crée pour nous une boucle d'événements.

* enfin on a vu les notions de context managers et d'itérateurs asynchrones, qui indiquent
  au langage que les méthodes spéciales en jeu sont des coroutines 
  * `__aenter__()` et `__aexit__()` pour les *context managers*
  * `__aiter__()` et `__anext__()` pour les itérateurs

+++ {"cell_style": "split", "slideshow": {"slide_type": "fragment"}}

## résumé 2

* enfin, une coroutine peut appeler une autre coroutine avec `await`; on ne peut pas faire
  `await` dans une fonction ordinaire, seulement dans une coroutine

+++

* si on définit une fonction coroutine `async def foo():`

* `foo()` → objet *coroutine* :  faire `await foo()`

+++ {"cell_style": "split", "slideshow": {"slide_type": "fragment"}}

**autorisé**

````
async def bar():
    await foo()
````

+++ {"cell_style": "split", "slideshow": {"slide_type": "-"}}

**pas autorisé** : *SyntaxError*

````
def bar():
    await foo()
````
