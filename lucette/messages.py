import datetime
import pydantic
import uuid

from typing import UUI


class BaseMessage(pydantic.BaseModel):
    """
    todo
    """
    channel: str


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