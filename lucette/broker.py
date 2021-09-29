import asyncio
import abc

import aioredis

from .message import BaseMessage


class MessageBroker(abc.ABC):
    
    @abc.abstractmethod
    async def publish(self, message: BaseMessage):
        pass
    
    @abc.abstractmethod
    async def get_message(self) -> BaseMessage:
        pass


class SimpleBroker(MessageBroker):
    """
    The default message broker used in Lucette. It's a simple in memory broker
    for the current process.
    TODO: handle a queue that fills with events that don't have a handler
    """

    def __init__(self):
        self.__message_queue = asyncio.Queue()

    async def publish(self, message: BaseMessage):
        await self.__message_queue.put(message)
    
    async def get_message(self) -> BaseMessage:
        return await self.__message_queue.get()


class RedisBroker(MessageBroker):
    """
    A message broker using Redis Pub/Sub
    """
    
    def __init__(self, url):
        self._client = aioredis.from_url(url=url)
        self._pubsub = self._client.pubsub()
    
    async def publish(self, message: BaseMessage):
        await self._client.publish(message.channel, message.json())
    
    async def get_message(self) -> BaseMessage:
        await self._pubsub.get_message()