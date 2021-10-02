import datetime
import pydantic
import uuid

import inflection

from typing import Optional


class BaseMessage(pydantic.BaseModel):
    """
    todo
    """
    _channel: Optional[str]
    
    def __init__(self, **data):
        """
        Create a new BaseMessage. Here channel is used as a way to explicitly
        specify the name of the channel within the message broker that this
        message type is sent on.
        """
        super().__init__(**data)
        
    @classmethod
    @property
    def channel(cls):
        return cls._channel or inflection.underscore(cls.__name__)


class OrderedMessage(BaseMessage):
    """
    For messages that have a definite ordering
    """
    order: int
    
    
class Event(OrderedMessage):
    """
    todo
    """
    id: uuid.UUID = uuid.uuid4()
    event_type: str
    timestamp: datetime.datetime = datetime.datetime.utcnow()
    
    
class Command(OrderedMessage):
    """
    todo
    """
    id: uuid.UUID = uuid.uuid4()
    type: str
    timestamp: datetime.datetime = datetime.datetime.utcnow()