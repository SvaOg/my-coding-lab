import pytest

from loot_ledger import hello
from loot_ledger.inventory import Inventory
from loot_ledger.event_store import EventStore
from loot_ledger.item import Item


@pytest.fixture(scope="function")
def inventory():
    yield Inventory(EventStore[Item]())


def test_001():
    assert hello() == "Hello from loot_ledger!"


def test_002():
    Inventory(EventStore[Item]())


def test_003(inventory):
    sword1 = Item(name="sword", rarity="rare", origin="castle")
    inventory.add_item(sword1)
    assert inventory.get_count(sword1) == 1

    sword2 = Item(name="sword", rarity="common", origin="castle")
    inventory.add_item(sword2)
    inventory.add_item(sword2)
    assert inventory.get_count(sword2) == 2

    inventory.remove_item(sword2)
    assert inventory.get_count(sword2) == 1


#     inventory = Inventory(EventStore())
#     inventory.add_item("Sword")
#     inventory.add_item("Bow")
#     inventory.add_item("Banana")
#     items = inventory.get_items()
#     assert items == sorted([("Sword", 1), ("Bow", 1), ("Banana", 1)])
#     assert inventory.get_count("Banana") == 1
#     assert inventory.get_count("Hammer") == 0
#     inventory.remove_item("Banana")
#     assert inventory.get_count("Banana") == 0


# def test_004(inventory):
#     with pytest.raises(ValueError):
#         inventory.remove_item("Test")


# def test_005(inventory):
#     inventory.add_item("Banana")
#     assert inventory.get_count("Banana") == 1

#     inventory.remove_item("Banana")
#     assert inventory.get_count("Banana") == 0

#     with pytest.raises(ValueError):
#         inventory.remove_item("Banana")
