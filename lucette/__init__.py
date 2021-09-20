import asyncio

from typing import Callable
from functools import update_wrapper
from collections import defaultdict
from inspect import getfullargspec

from brokers import SimpleBroker


class Lucette:

    def __init__(self, broker=SimpleBroker()):
        self.__broker = broker
        self.__subscriber_registry = defaultdict(list)

    def subscribe(self, func: Callable):
        update_wrapper(self, func)
        arg_details = getfullargspec(func)
        if len(arg_details.args) == 0:
            raise AttributeError(
                'event handler must have at least one argument'
            )
        first_arg = arg_details.args[0]
        self.__subscriber_registry[arg_details.annotations[first_arg]].append(func)
        
    async def publish(self, event: object):
        await self.__broker.publish(event)

    async def __listen_for_events():

        while True:
            message = await __message_queue.get()
            handlers = __registry[type(message)]
            for func in handlers:
                await func(message)


#asyncio.get_event_loop().create_task(__listen_for_events())
