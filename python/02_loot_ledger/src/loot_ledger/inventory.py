from collections import Counter
from .event import Event, EventType
from .event_store import EventStore
from functools import cache


class Inventory:
    def __init__(self, store: EventStore) -> None:
        self.store = store

    def add_item(self, item: str) -> None:
        self.store.append(Event(EventType.ITEM_ADDED, item))
        self._invalidate_cache()

    def remove_item(self, item: str) -> None:
        if self.get_count(item) == 0:
            raise ValueError(f"Item {item} not in inventory.")
        self.store.append(Event(EventType.ITEM_REMOVED, item))
        self._invalidate_cache()

    def _invalidate_cache(self):
        self.get_items.cache_clear()

    @cache
    def get_items(self) -> list[tuple[str, int]]:
        counter = Counter()
        for event in self.store.get_all_events():
            if event.type == EventType.ITEM_ADDED:
                counter[event.data] += 1
            elif event.type == EventType.ITEM_REMOVED:
                counter[event.data] -= 1

        return sorted((k, v) for k, v in counter.items() if v > 0)

    def get_count(self, item: str) -> int:
        return dict(self.get_items()).get(item, 0)
