from dataclasses import field, dataclass
from enum import StrEnum
from datetime import datetime


class EventType(StrEnum):
    ITEM_ADDED = "item_added"
    ITEM_REMOVED = "item_removed"


@dataclass(frozen=True)
class Event:
    type: EventType
    data: str
    timestamp: datetime = field(default_factory=datetime.now)
