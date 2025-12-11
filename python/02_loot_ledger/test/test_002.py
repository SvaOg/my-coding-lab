from dataclasses import dataclass


# @dataclass(frozen=True)
@dataclass(frozen=True)
class Thing:
    name: str
    id: int


def test_001():
    thing1 = Thing("something", 1)
    thing2 = Thing("tool", 2)
    data = {}
    data[thing1] = 1
    data[thing2] = 2

    assert data[thing2] == 2
