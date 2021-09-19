import uvloop
import asyncio

from lucette import Lucette


# defaults to SimpleBroker if nothing is provided
lucy = Lucette()


@lucy.subscriber
async def my_handler(event: MyEvent) -> None:
    pass


def main():
    await lucy.publish()


uvloop.install()
asyncio.run(main())
