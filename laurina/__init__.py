import asyncio

from typing import Callable
from functools import update_wrapper
from collections import defaultdict
from inspect import getfullargspec


__message_queue = asyncio.Queue()
__registry = defaultdict(list)


#  TODO: handle a queue that fills with events that don't have a handler
async def publish(event: object):
    await __message_queue.put(event)


class subscriber:

    def __init__(self, func: Callable):
        update_wrapper(self, func)
        self.func = func
        arg_details = getfullargspec(func)
        if len(arg_details.args) == 0:
            raise AttributeError(
                'event handler must have at least one argument'
            )
        first_arg = arg_details.args[0]
        global __registry
        __registry[arg_details.annotations[first_arg]].append(func)

    async def __call__(self, *args, **kwargs):
        await self.func(*args, **kwargs)


async def __listen_for_events():

    while True:
        message = await __message_queue.get()
        handlers = __registry[type(message)]
        for func in handlers:
            await func(message)


asyncio.get_event_loop().create_task(__listen_for_events())
