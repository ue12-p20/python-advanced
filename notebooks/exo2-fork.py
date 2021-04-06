import asyncio

from asynchelpers import start_timer, show_timer

async def c1():
    show_timer(">>> c1")
    await asyncio.sleep(1)
    show_timer("forking")
    # fork
    asyncio.ensure_future(c2())
    await asyncio.sleep(1)
    show_timer("<<< c1")


# sera forkée par c1() après une seconde

async def c2():
    show_timer(">>> c2")
    await asyncio.sleep(2)
    show_timer("<<< c2")


start_timer()

loop = asyncio.new_event_loop()
asyncio.ensure_future(c1(), loop=loop)

# pensez à interrompre après 2s
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("bye")
