# /// script
# requires-python = ">=3.12"
# dependencies = [
# ]
# ///

from dataclasses import dataclass

@dataclass
class Item:
    name: str
    rarity: str

class ItemStore[T=str]:
    def __init__(self) -> None:
        self._store = []

    def add_item(self, item: T):
        self._store.append(item)


def main():
    store = ItemStore[str]()
    store.add_item("test")
    store2 = ItemStore[Item]()
    print("Done!")
    print("Done!")
    print("Done!")
    print("Done!")
    print("Done!")
    print("Done!")
    print("Done!")
    print("Done!")

if __name__ == "__main__":
    main()
