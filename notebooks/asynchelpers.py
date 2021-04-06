from datetime import datetime

import asyncio

####################
# Use a module global to keep things simple

_global_start = None

def start_timer():
    """
    reset global timer to 0.
    """
    global _global_start
    print("---------- zero")
    _global_start = datetime.now()

def show_timer(*args):
    """
    just like print, but with the current time
    """
    delta = datetime.now() - _global_start
    duration = f"{delta.seconds}s + {delta.microseconds//1000:03d}ms"
    print(duration, *args)


# just make sure the timer is started
def _start_timer_if_needed():
    if _global_start is None:
        start_timer()

##############################
async def sequence(*messages, delay=1):
    """
    print messages, async waits for <delay> seconds, and prints messages again
    """
    _start_timer_if_needed()
    show_timer(">>>", *messages)
    await asyncio.sleep(delay)
    show_timer("<<<", *messages)
    return 10 * delay

# ##########
# def reset_loop():
#     asyncio.set_event_loop(asyncio.new_event_loop())
