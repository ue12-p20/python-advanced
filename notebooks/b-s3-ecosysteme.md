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
  title: "\xE9cosyst\xE8me"
---

<span style="float:left;">Licence CC BY-NC-ND</span><span style="float:right;">Thierry Parmentelat<img src="media/inria-25-alpha.png" style="display:inline"></span><br/>

+++ {"slideshow": {"slide_type": "slide"}}

# `asyncio` : historique et écosystème

+++

Nous avons vu quelques exemples simples
de programmation asynchrone avec
asyncio. Dans cette séquence, après un
rapide historique nous allons 
voir quelles sont les librairies
disponibles pour tirer profit de ce
nouveau paradigme

+++ {"slideshow": {"slide_type": "slide"}}

## historique - python3

+++ {"slideshow": {"slide_type": "fragment"}}

Dans sa forme actuelle avec 'async def'
et 'await', la syntaxe date de
python-3.5, en 2015 donc.   

* python-3.5 
  * syntaxe moderne `async` / `await`

+++

Je vous
signale rapidement que asyncio avait en
fait été introduite un an plus tôt dans
python-3.4,mais avec une syntaxe différente, que je
vous montre ici rapidement, il se peut
que vous trouviez du code avec cette
ancienne syntaxe.

+++ {"slideshow": {"slide_type": "fragment"}}

* python-3.4 : première introduction de `asyncio`

  * `async def` → `@asyncio.coroutine` 
  * `await` → `yield from`

+++ {"slideshow": {"slide_type": "slide"}}

## historique - python2

+++ {"slideshow": {}}

enfin il faut savoir que les mécanismes
dont on a besoin pour implémenter une
boucle d'événements sont présents dans
le langage depuis déjà python-2.5 c'est
à dire 2006 !

* python-2.5 (2006 !)

  * générateurs avec `send()`

+++ {"slideshow": {"slide_type": "slide"}}

## inspiré de (pre-asyncio)

+++

je vous signale d'ailleurs plusieurs
projets qui ont tiré profit de cette
possibilité, qui sont ces trois-ci

+++ {"slideshow": {}}

* gevent : http://www.gevent.org/
* tornado : http://www.tornadoweb.org/en/stable/
* twisted : https://twistedmatrix.com/trac/

+++

qui
utilisent une technologie similaire
depuis bien avant asyncio, et qui
d'ailleurs l'ont largement inspiré.

à cet égard, s'il est fréquent de
résumer ce style de programmation sous
le simple nom de `asyncio`, il faut bien distinguer
entre les traits qui appartiennent au
langage - qui sont donc par définition
peu flexibles - de ceux qui sont
implémentées dans la librairie.

+++ {"slideshow": {"slide_type": "slide"}}

## langage *vs* librairie (1) : langage

+++

La distinction est assez nette, le
langage contient principalement 

* la notion de coroutine, qui se
matérialise avec les mots clés `async
def` et `await`, 

* et quelques produits dérivés comme
`async for` et `async with` que l'on
aura l'occasion de voir plus tard :

+++ {"slideshow": {"slide_type": "fragment"}}

  * itérateurs asynchrones - `async for` - compréhensions asynchrones

+++ {"slideshow": {"slide_type": "fragment"}}

  * context managers asynchrones - `async with`

+++

Notez que la notion de coroutine est assez voisine donc de la notion de générateur, on y reviendra

+++ {"slideshow": {"slide_type": "slide"}}

## langage *vs* librairie (2) : librairie

+++

La librairie quant à elle implémente
principalement la boucle d'événements.

C'est important de comprendre la
distinction, car cela signifie qu'il est
tout à fait possible d'envisager
d'autres librairies asynchrones qui
partagent toutes le même modèle de
coroutines, et qui coexistent.

+++

Outre la boucle d'événements, on trouve
aussi dans asyncio, un peu en vrac:

* des objets de base pour la
synchronisation, comme les classes
`Queue`, `Lock` et `Semaphore`

* un package `Subprocess` pour l'interaction
avec les processus, la version
asynchrone de la librairie standard
`subprocess`

et des abstractions, qu'on peut
voir si on veut comme des frameworks -
ou des design patterns - pour
l'implémentation de comportements plus
évolués, comme les notions de transport
et de protocole, pour l'implémentation
par exemple d'une pile http; pour faire simple 
il y a deux grandes influences qui sont

* `Transport` et `Protocol` / plutôt orienté callback
* `Streams` / API orientées coroutine

+++

Nous avons déjà un peu rencontré les
coroutines, et la boucle d'événements
pour faire tourner nos premiers exemples
dans la précédente vidéo. Pour le reste,
à nouveau, il ne sera pas question de
couvrir exhaustivement tous ces sujets,
mais nous verrons d'autres exemples de
tout ça dans les prochaines vidéos.

Pour l'instant, je voudrais vous donner
quelques généralités à propos de ce
paradigme.

+++ {"slideshow": {"slide_type": "slide"}}

## est-ce que c'est utilisable en production ?

+++

On a pu se poser la question en 2015 quand les premières versions sont sorties, tout cela avait un petit coté improbable.
En 2021, la réponse à cette question est très clairement OUI, l'API est classée comme stable et sera supportée dans la durée avec le reste de Python.

+++

En terme de performance et de passage à l'échelle, il est admis qu'à ressources
constantes, on peut heberger avec de paradigme plus
d'acteurs concurrents qu'avec des
threads, et donc à priori qu'avec des
processus, dans un rapport **de plusieurs
ordres de grandeur** - au moins 100.

+++

À savoir également, il y a aujourd'hui
une offre très complète, notamment tous les protocoles réseau les
plus populaires, les drivers de base de
données, essentiellement tout est
disponible dans une forme compatible
avec ce paradigme.

+++ {"slideshow": {"slide_type": "fragment"}}

* nombreux protocoles réseau disponibles
  * HTTP `aiohttp`
  * ssh `asyncssh`
  * telnet `telnetlib3`
* drivers bases de données
  * postgres `asyncpg`
  * ...
* ...

+++ {"slideshow": {"slide_type": "slide"}}

## mais ..

+++

une fois qu'on a dit ça, il n'y a pas que des avantages naturellement

le principal reproche qu'on fait a ce modèle est le coté très contagieux des
coroutines; dès qu'on se met à utiliser
`asyncio`, on se retrouve à avoir envie
d'une version asynchrone pour .. à peu
près tout.

Et comme on a fait le choix que les
changements de contexte sont explicites
avec `await` - il faut récrire le code
pour tirer profit de ce modèle de
programmation. Mais bon, comme on vient
de le voir, cela n'est pas un souci,
l'écosystème est très complet.

L'autre incertitude que je voulais
signaler pour terminer, c'est que le
consensus n'est pas total sur les choix
faits dans la librairie asyncio. Tout
le monde est d'accord sur le concept de
coroutine, mais je signale tout de même
quelques travaux très intéressants
qui visent à en tirer un meilleur
profit, et qui pourraient bien
influencer une version 2 de asyncio dans
le futur:

+++ {"slideshow": {"slide_type": "fragment"}}

  * `uvloop` 
  * `curio`
  * `trio`

+++

Bon même si ça devait arriver,
rassurez-vous, ce qu'on
va apprendre sur la syntaxe, les coroutines, les
awaitables, et de façon plus générale le
modèle mental, tout cela restera valable.
