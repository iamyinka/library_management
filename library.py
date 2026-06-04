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
    def get_display_title(self) -> str: ...


class Book(LibraryItem):
    def __init__(self, title: str, author: str, isbn: str) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = BookStatus.AVAILABLE
        self.borrowed_by: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(data["title"], data["author"], data["isbn"])

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
            print(f"    {book.get_display_title()}")

    def borrow_book(self, isbn: str, member_id: str) -> None:
        book = self.find_book(isbn=isbn)
        member = self.find_member(member_id=member_id)

        if book.status != BookStatus.AVAILABLE:
            raise BookNotAvailableError(
                f'"{book.title}" is currently {book.status.value}'
            )

        book.status = BookStatus.BORROWED
        book.borrowed_by = member.name
        member.borrowed_books.append(isbn)

        print(f'{member.name} borrowed "{book.title}"')

    def return_book(self, isbn: str, member_id: str) -> None:
        book = self.find_book(isbn=isbn)
        member = self.find_member(member_id=member_id)

        if book.status != BookStatus.BORROWED:
            raise BookAlreadyReturnedError(f'"{book.title} is not currently borrowed"')

        book.status = BookStatus.AVAILABLE
        book.borrowed_by = None
        member.borrowed_books.remove(isbn)
        print(f'{member.name} returned "{book.title}"')


def main() -> None:
    library = Library("London City Central Library")
    book1 = Book.from_dict(
        {"title": "Clean Code", "author": "Robert Martin", "isbn": "9780132350884"}
    )
    book2 = Book.from_dict(
        {
            "title": "The Pragmatic Programmer",
            "author": "David Thomas",
            "isbn": "9780135957059",
        }
    )
    book3 = Book("Python Crash Course", "Eric Matthes", "9781593279288")

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    alice = Member(name="Alice", member_id="M001")
    bob = Member(name="Bob", member_id="M002")

    library.add_member(alice)
    library.add_member(bob)

    library.list_books()

    print("\n--- Alice borrows Clean Code ---")
    library.borrow_book("9780132350884", "M001")
    library.list_books()

    print("\n--- Bob tries to borrow the same book ---")
    try:
        library.borrow_book("9780132350884", "M002")
    except BookNotAvailableError as e:
        print(f"Error: {e}")

    print("\n--- Alice returns Clean Code ---")
    library.return_book("9780132350884", "M001")
    library.list_books()

    print("\n--- Invalid ISBN test ---")
    try:
        library.add_book(Book("Bad Book", "Nobody", "123"))
    except ValueError as e:
        print(f"Error: {e}")

    print("\n--- Static method test ---")
    print(f"'9780132350884' valid? {Book.is_valid_isbn('9780132350884')}")
    print(f"'123' valid? {Book.is_valid_isbn('123')}")


if __name__ == "__main__":
    main()
