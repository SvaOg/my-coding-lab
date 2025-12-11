import pytest

from loot_ledger import hello
from loot_ledger.inventory import Inventory
from loot_ledger.event_store import EventStore


@pytest.fixture(scope="function")
def inventory():
    yield Inventory(EventStore())


def test_001():
    assert hello() == "Hello from loot_ledger!"


def test_002():
    Inventory(EventStore())


def test_003():
    inventory = Inventory(EventStore())
    inventory.add_item("Sword")
    inventory.add_item("Bow")
    inventory.add_item("Banana")
    items = inventory.get_items()
    assert items == sorted([("Sword", 1), ("Bow", 1), ("Banana", 1)])
    assert inventory.get_count("Banana") == 1
    assert inventory.get_count("Hammer") == 0
    inventory.remove_item("Banana")
    assert inventory.get_count("Banana") == 0


def test_004(inventory):
    with pytest.raises(ValueError):
        inventory.remove_item("Test")


def test_005(inventory):
    inventory.add_item("Banana")
    assert inventory.get_count("Banana") == 1

    inventory.remove_item("Banana")
    assert inventory.get_count("Banana") == 0

    with pytest.raises(ValueError):
        inventory.remove_item("Banana")
