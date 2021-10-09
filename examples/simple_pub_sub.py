import uvloop
import asyncio

from lucette import Lucette
from lucette.message import BaseMessage


class MyMessage(BaseMessage):
    _channel = 'my_channel'
    msg: str

 
lucy = Lucette()


@lucy.subscribe
async def my_handler(message: MyMessage) -> None:
    print(f'received message: "{message.msg}"')


async def main():
    await lucy.publish(MyMessage(msg='This is a message'))


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(asyncio.gather(lucy.run(), main()))
