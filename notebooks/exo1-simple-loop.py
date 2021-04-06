import asyncio

from asynchelpers import start_timer, show_timer

async def loop1():
    for _ in range(3):
        show_timer('tick1')
        await asyncio.sleep(0.1)

async def loop2():
    for _ in range(6):
        show_timer('tick2')
        await asyncio.sleep(0.05)

async def both():
    await asyncio.gather(loop1(), loop2())

start_timer()

# Cannot do await both() here !!

loop = asyncio.new_event_loop()
loop.run_until_complete(both())
