from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"


class LibraryError(Exception):
    pass


class BookNotFoundError(LibraryError):
    pass


class BookNotAvailableError(LibraryError):
    pass


class BookAlreadyReturnedError(LibraryError):
    pass


class LibraryItem(ABC):
    @abstractmethod
    def get_summary(self) -> str: ...

    @abstractmethod
    def get_dipslay_title(self) -> str: ...


class Book(LibraryItem):
    def __init__(self, title: str, author: str, isbn: str) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = BookStatus.AVAILABLE
        self.borrowed_by: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(data["title", data["author"], data["isbn"]])

    @staticmethod
    def is_valid_isbn(isbn: str) -> bool:
        cleaned = isbn.replace("-", "").replace(" ", "")
        return len(cleaned) in (10, 13) and cleaned.isdigit()

    def get_summary(self) -> str:
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn})"

    def get_display_title(self) -> str:
        return f"[{self.status.value.upper()}] {self.title} - {self.author}"

    def __str__(self) -> str:
        return self.get_summary()


@dataclass
class Member:
    name: str
    member_id: str
    borrowed_books: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Member({self.name}, ID: {self.member_id})"


class Library:
    def __init__(self, name: str) -> None:
        self.name = name
        self._books: list[Book] = []
        self._members: list[Member] = []

    def add_book(self, book: Book) -> None:
        if not Book.is_valid_isbn(book.isbn):
            raise ValueError(f"Invalid ISBN: {book.isbn}")
        self._books.append(book)
        print(f"Added: {book.get_summary()}")

    def find_book(self, isbn: str) -> Book:
        for book in self._books:
            if book.isbn == isbn:
                return book
        raise BookNotFoundError(f"No book found with ISBN: {isbn}")

    def add_member(self, member: Member) -> None:
        self._members.append(member)
        print(f"Registered: {member}")

    def find_member(self, member_id: str) -> Member:
        for member in self._members:
            if member.member_id == member_id:
                return member
        raise LibraryError(f"No member found with ID: {member_id}")

    def list_books(self) -> None:
        if not self._books:
            print("No books in the library")
            return
        print(f"\n{self.name} - Catalogue:")
        for book in self._books:
            print(f"    {book.get_dipslay_title()}")
