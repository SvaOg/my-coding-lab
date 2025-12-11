"""
Basic example showing how to read and validate data from a file using Pydantic
"""

import json
from typing import Annotated
from pydantic import BaseModel, ConfigDict, AfterValidator, model_validator


def isbn10_valid(value: str) -> str:
    """Validator to check whether ISBN10 has a valid value."""
    chars = [ch for ch in value if ch in "0123456789xX"]
    if len(chars) != 10:
        raise ValueError(f"{value} should be 10 digits long.")

    def char_to_int(ch: str) -> int:
        return 10 if ch in "xX" else int(ch)

    weighted_sum = sum((10 - i) * char_to_int(x) for i, x in enumerate(chars))
    if weighted_sum % 11:
        raise ValueError(value, "Digit sum should be divisible by 11.")

    return value


class Book(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    subtitle: str
    author: str
    publisher: str
    isbn_10: Annotated[str | None, AfterValidator(isbn10_valid)] = None
    isbn_13: str | None = None
    price: float

    @model_validator(mode="after")
    def check_at_least_one_isbn(self) -> "Book":
        if self.isbn_10 is None and self.isbn_13 is None:
            raise ValueError("Must provide at least one ISBN (10 or 13)")
        return self


def main() -> None:
    with open("data/data.json") as file:
        data = json.load(file)
        books: list[Book] = [Book(**v) for v in data]

    print(books[0].title)
    print(books[0].model_dump_json())


if __name__ == "__main__":
    main()
