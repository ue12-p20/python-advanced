import asyncio

from asynchelpers import (
    start_timer, show_timer, sequence)

# deux jobs, un court et un long
async def short():
    await sequence("short", delay=1)

async def long():
    await sequence("long", delay=2)

start_timer()

# au démarrage on insère le job le plus long
asyncio.ensure_future(long())

# ici on va tout exécuter dans la boucle
# mais seulement jusqu'à la fin
# du job le plus court
loop = asyncio.get_event_loop()
loop.run_until_complete(short())

print("done")

# en fait ici il reste des trucs à faire !

# et donc on peut reprendre ensuite
# et traiter ce qui reste dans la queue

# ne pas oublier d'interrompre
# après quelques secondes
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print("bye")

