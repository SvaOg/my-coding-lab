import json
from pydantic import ValidationError
import pytest
from main import Book

data1 = """
[
    {
        "title": "Zero to One",
        "subtitle": "Notes on Startups, or How to Build the Future",
        "author": "Peter Thiel",
        "publisher": "Crown Currency",
        "isbn_10": "0307887898",
        "isbn_13": "978-0307887894",
        "price": 16.99
    },
    {
        "title": "Zero to One",
        "subtitle": "Notes on Startups, or How to Build the Future",
        "author": "Peter Thiel",
        "publisher": "Crown Currency",
        "isbn_13": "978-0307887894",
        "price": 16.99
    },
    {
        "title": "Zero to One",
        "subtitle": "Notes on Startups, or How to Build the Future",
        "author": "Peter Thiel",
        "publisher": "Crown Currency",
        "isbn_10": "0307887898xxx",
        "isbn_13": "978-0307887894",
        "price": 16.99
    },
    {
        "title": "Zero to One",
        "subtitle": "Notes on Startups, or How to Build the Future",
        "author": "Peter Thiel",
        "publisher": "Crown Currency",
        "isbn_10": "0307887890",
        "isbn_13": "978-0307887894",
        "price": 16.99
    },
    {
        "title": "Zero to One",
        "subtitle": "Notes on Startups, or How to Build the Future",
        "author": "Peter Thiel",
        "publisher": "Crown Currency",
        "price": 16.99
    }
]
"""


def test_good_book():
    """Fully formatted book object"""
    book = Book(**json.loads(data1)[0])
    assert book.title == "Zero to One"


def test_book_should_be_immutable():
    """Fully formatted book object should be immutable"""
    book = Book(**json.loads(data1)[0])
    with pytest.raises(ValidationError):
        book.title = "New title"


def test_isbn10_is_missing():
    book = Book(**json.loads(data1)[1])
    assert book.title == "Zero to One"


def test_isbn10_is_longer():
    with pytest.raises(ValidationError):
        Book(**json.loads(data1)[2])


def test_isbn10_wrong_weighted_sum():
    with pytest.raises(ValidationError):
        Book(**json.loads(data1)[3])


def test_both_isbn_are_missing():
    with pytest.raises(ValidationError):
        Book(**json.loads(data1)[4])
