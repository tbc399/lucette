from typing import Callable
from functools import update_wrapper
from inspect import getfullargspec


class Subscriber:
    
    def __init__(self, func: Callable):
        update_wrapper(self, func)
        self.func = func
        arg_details = getfullargspec(func)
        if len(arg_details.args) == 0:
            raise AttributeError(
                'event handler must have at least one argument'
            )
        first_arg = arg_details.args[0]
        global __registry
        __registry[arg_details.annotations[first_arg]].append(func)
    
    async def __call__(self, *args, **kwargs):
        await self.func(*args, **kwargs)
