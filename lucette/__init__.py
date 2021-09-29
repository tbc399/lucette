import asyncio

from inspect import getfullargspec
from typing import Callable
from functools import update_wrapper
from collections import defaultdict

from broker import SimpleBroker


class Lucette:

    def __init__(self, broker=SimpleBroker()):
        self.__broker = broker
        self.__subscriber_registry = defaultdict(list)

    def subscribe(self, func: Callable):
        """
        todo: add check to have no more than one channel per message type
        """
        update_wrapper(self, func)
        arg_details = getfullargspec(func)
        if len(arg_details.args) != 1:
            raise AttributeError(
                'subscriber handler must have exactly one argument'
            )
        first_arg = arg_details.args[0]
        arg_type = arg_details.annotations.get(first_arg, None)
        if arg_type is None:
            raise AttributeError(
                'subscriber must either have a type hint on the '
                'message parameter or the channel must be given'
            )
        # todo: if type hint given, get the channel if there is one
        self.__subscriber_registry[arg_type].append(func)
        
    async def publish(self, event: object):
        await self.__broker.publish(event)

    async def run(self):
        while True:
            message = await self.__broker.get_message()
            handlers = self.__subscriber_registry[type(message)]
            for func in handlers:
                await func(message)
            await asyncio.sleep(0.01)  # add some advanced backoff logic when low traffic


#asyncio.get_event_loop().create_task(__listen_for_events())
