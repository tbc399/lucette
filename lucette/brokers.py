import asyncio


#  TODO: handle a queue that fills with events that don't have a handler
class SimpleBroker:
    """
    This is the default broker that handles messages in the system. It runs in
    memory of the current app.
    """

    def __init__(self):
        self.__message_queue = asyncio.Queue()

    def publish(self, msg: object):