import uvloop
import asyncio

from lucette import Lucette
from lucette.message import BaseMessage
from lucette.broker import RedisBroker


class MyMessage(BaseMessage):
    _channel = 'my_channel'
    msg: str


lucy = Lucette(broker=RedisBroker(url='redis://localhost'))


@lucy.subscribe
async def handler(message: MyMessage) -> None:
    print(message.msg)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(lucy.run())
