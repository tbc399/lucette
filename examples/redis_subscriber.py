import uvloop
import asyncio

from lucette import Lucette
from lucette.message import BaseMessage


# defaults to SimpleBroker if nothing is provided
lucy = Lucette()


@lucy.subscribe
async def my_handler(message: MyMessage) -> None:
    pass


uvloop.install()
asyncio.run(lucy.run())
