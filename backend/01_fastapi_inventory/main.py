from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from enum import Enum

app = FastAPI()

# --- Data Models (Pydantic) ---


# Define the Category Enum
# Inheriting from 'str' ensures it serializes to JSON simply as "tools", not Category.TOOlS
class Category(str, Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


# Base model with shared attributes
class ItemBase(BaseModel):
    name: str
    price: float
    count: int
    category: Category


# Model for creating an item (ID is not required from user)
class ItemCreate(ItemBase):
    pass


# Model for returning an item (includes ID)
class Item(ItemBase):
    id: int


# --- In-Memory Database ---
items_db = {
    0: {
        "id": 0,
        "name": "Hammer",
        "price": 9.99,
        "count": 20,
        "category": Category.TOOLS,
    },
    1: {
        "id": 1,
        "name": "Nails",
        "price": 1.99,
        "count": 100,
        "category": Category.CONSUMABLES,
    },
}

# --- API Endpoints ---


@app.get("/")
def read_root():
    """Health check or welcome message."""
    return {"message": "Welcome to the Inventory API"}


# 1. GET all items
# URL is a noun (/items)
@app.get("/items", response_model=list[Item])
def get_items():
    return list(items_db.values())


# 2. GET a specific item by ID
# Uses path parameter for ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in items_db:
        # CRITICAL: We MUST 'raise' the exception, not just call it.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return items_db[item_id]


# 3. CREATE a new item
# Uses POST verb on the collection URL (/items)
# Returns 201 Created status
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemCreate):
    # Simple ID generation strategy
    new_id = max(items_db.keys()) + 1 if items_db else 0

    # Create new item dict
    new_item = item_in.model_dump()
    new_item["id"] = new_id

    # Save to DB
    items_db[new_id] = new_item
    return new_item


# 4. UPDATE an existing item
# Uses PUT verb for full updates
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_in: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )

    # Update logic
    items_db[item_id].update(item_in.model_dump())
    items_db[item_id]["id"] = item_id  # Ensure ID doesn't change

    return items_db[item_id]


# 5. DELETE an item
# Uses DELETE verb
# Returns 204 No Content (standard for delete operations)
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )

    del items_db[item_id]
    # Do not return anything for 204 responses
    return
