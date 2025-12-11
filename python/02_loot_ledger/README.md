# loot_ledger

Topic: [Python, Design Patterns, Event Sourcing]

Source: [https://youtu.be/t-LC1dWLpNs?si=X1tFXvWpv6j_HUmC]

Date: 2025-12-10

Tags: #learning #python #[design-patterns]

## 🚀 Quick Start (uv)

How to run this project after cloning the repo.

```
# 1. Install dependencies
uv sync

# 2. Run tests
uv run pytest
```

## 🧠 Key Concepts Learned

- **Event Sourcing:** We store the sequence of events and when we need state (the inventory items) - we calculate it on the fly by replaying the history. The philosophy is to store **verbs** (changes) instead of **nouns** (state).

- **Immutability**: The events are write-once and frozen using ``@dataclass(frozen=True)``. This is non-negotiable in Event Sourcing - you never rewrite the history.

- **Projectionsn**: Creating different views from the same event stream is the "killer feature" of this pattern.
    
- **dataclass - dynamic or mutable defaults** When I write ``timestamp: datetime = field(default_factory=datetime.now)`` in the class body, the @dataclass decorator will generate __init__ method which will remove the class attribute and will initialize instance's timestamp attribute when the instance is created. Another reason to use this pattern is if our class has a list attribute and we need each instance to have it's own copy of the list.
    
- **typing.ClassVar** typing.ClassVar allows us to have trully class attributes that @dataclass will not touch.

- **Summary of the Dataclass "Type System":**
    - ``x: int`` -> **Instance Variable** (Managed by dataclass)
    - ``x: int = field(...)`` -> **Instance Variable** (Managed by dataclass, customized)
    - ``x: ClassVar[int]`` -> **Class Variable** (Ignored by dataclass)

## 🏗️ Design Decisions & Architecture
       
- **Folder Structure:**
    
    - `src/`: Application logic.
        
    - `tests/`: TestClient integration.
        
## 🔮 Future Improvements / Ideas

Some changes are required if we implement this pattern in production:

- Replace generic event wrapper with specific event classes
```Python
@dataclass(frozen=True)
class ItemAdded:
    item: Item
    timestamp: datetime

@dataclass(frozen=True)
class InventoryCleared:
    reason: str
    timestamp: datetime
```
    
- Introduce **Snapshots** (The Performance Fix)
    - **The Problem:** In a real app replaying from the beginning every time the app restarts or the cache clears is too slow.
    - **The Fix:** Implement **Snapshots**. Every N events we calculate the state and save it into a database. When we need the current state, we load the latest snapshot and only replay the events that happened after that snapshot.

- **Separation of Write and Read (CQRS)**
    - **Write Model:** Accepts commands ("Add Sword"), checks rules ("Do we have enough space"), and emits events. It doesn't care about answering queries
    - **Read Model:** Listens to events and updates a separate database table or data structure optimized for reading. We wouldn't need to replay events to ``get_items``; we would just query the "Read Model" which is already up to date.

- **Handling "Business Logic" Checks**

    In the lesson we check to see if an item exists before removing it by replaying history. This is accurate for the pattern, but expensive. In production, this is where the "Write Model" (Aggregate) keeps a tiny, simplified version of the state just to validate rules, ensuring we don't sell an item we don't have.
    
