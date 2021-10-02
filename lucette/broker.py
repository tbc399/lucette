import asyncio
import abc

import aioredis

from .message import BaseMessage


class MessageBroker(abc.ABC):
    
    @abc.abstractmethod
    async def publish_message(self, message: BaseMessage):
        pass

    @abc.abstractmethod
    async def get_message(self) -> BaseMessage:
        pass
    
    @abc.abstractmethod
    async def subscribe_to_channel(self, channel: str):
        pass


class SimpleBroker(MessageBroker):
    """
    The default message broker used in Lucette. It's a simple in memory broker
    for the current process.
    TODO: handle a queue that fills with events that don't have a handler
    """

    def __init__(self):
        self.__message_queue = None
        
    def __initialize_queue(self):
        if self.__message_queue is None:
            self.__message_queue = asyncio.Queue()

    async def publish_message(self, message: BaseMessage):
        self.__initialize_queue()
        await self.__message_queue.put(message)
    
    async def get_message(self) -> BaseMessage:
        self.__initialize_queue()
        return await self.__message_queue.get()
    
    async def subscribe_to_channel(self, channel: str):
        pass


class RedisBroker(MessageBroker):
    """
    A message broker using Redis Pub/Sub
    """
    
    def __init__(self, url):
        self._client = aioredis.from_url(url=url)
        self._pubsub = self._client.pubsub()
    
    async def publish_message(self, message: BaseMessage):
        await self._client.publish_message(message.channel, message.json())
    
    async def get_message(self) -> BaseMessage:
        return await self._pubsub.get_message()
    
    async def subscribe_to_channel(self, channel: str):
        await self._pubsub.subscribe(channel)
        
        
class BrokerGroup(MessageBroker):
    """
    A broker group has the same interface as a broker, but it's allows for
    multiple individual brokers to be combined and used in a single Lucette app
    """
    
    async def publish_message(self, message: BaseMessage):
        pass
    
    async def get_message(self) -> BaseMessage:
        pass
    
    async def subscribe_to_channel(self, channel: str):
        pass
