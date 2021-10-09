from inspect import getfullargspec
from collections import defaultdict
from typing import Callable, Iterable, Tuple
from functools import update_wrapper


class Subscriber:
    """
    A subscriber is used to help group message handler together. This is useful
    in larger apps where things are spread out across your project structure.
    """

    def __init__(self):
        self.__handler_registry = list()

    def subscribe(self, func: Callable):
        """
        todo: add check to have no more than one channel per message type
        """
        update_wrapper(self, func)
        arg_details = getfullargspec(func)
        if len(arg_details.args) != 1:
            raise AttributeError(
                'message handler must have exactly one argument'
            )
        param_name = arg_details.args[0]
        param_type = arg_details.annotations.get(param_name, None)
        if param_type is None:
            raise AttributeError(
                'message handler must either have a type hint on the '
                'message parameter or the channel must be given'
            )
        # todo: if type hint given, get the channel if there is one
        self.__handler_registry.append((func, param_type))
    
    @property
    def handlers(self) -> Iterable[Tuple[Callable, type]]:
        return self.__handler_registry
