import asyncio
import sys
import random
import string

import logbook

from inspect import getfullargspec
from typing import Callable
from functools import update_wrapper
from collections import defaultdict

from .broker import SimpleBroker, MessageBroker
from .message import BaseMessage


logbook.StreamHandler(sys.stdout).push_application()
log = logbook.Logger('lucette')


class Lucette:

    def __init__(self, broker=None):
        self.__subscriber_registry = defaultdict(list)
        self.__broker = broker or SimpleBroker()
        
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
        param_name = arg_details.args[0]
        param_type = arg_details.annotations.get(param_name, None)
        if param_type is None:
            raise AttributeError(
                'subscriber must either have a type hint on the '
                'message parameter or the channel must be given'
            )
        # todo: if type hint given, get the channel if there is one
        self.__subscriber_registry[param_type.channel].append((func, param_type))
        
    async def publish(self, msg: BaseMessage):
        await self.__broker.publish_message(msg)

    async def run(self):
        if self.__broker is None:
            raise AttributeError('No message broker has been registered')
        for channel in self.__subscriber_registry.keys():
            await self.__broker.subscribe_to_channel(channel)
        log.info('running with simple broker')
        while True:
            msg = await self.__broker.get_message()
            if msg is not None:
                handlers = self.__subscriber_registry[msg[0]]
                for func, msg_type in handlers:
                    await func(msg_type.parse_raw(msg[1]))
            await asyncio.sleep(0.05)  # todo: add some advanced backoff logic when low traffic
