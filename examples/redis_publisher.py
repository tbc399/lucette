import uvloop
import asyncio

from lucette import Lucette
from lucette.message import BaseMessage
from lucette.broker import RedisBroker


class MyMessage(BaseMessage):
    _channel = 'my_channel'
    msg: str


lucy = Lucette(broker=RedisBroker(url='redis://localhost'))


async def receive_input():
    while True:
        msg = input("message: ")
        if msg == 'stop':
            break
        await lucy.publish(MyMessage(msg=msg))


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(receive_input())
