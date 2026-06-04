# Library Management CLI

- Enum — fixed named values, no magic strings
- Custom exception hierarchy — LibraryError → specific errors
- ABC + @abstractmethod — enforced contract on child classes
- @classmethod — factory method, alternative constructor
- @staticmethod — utility function parked in the class
- @dataclass + field(default_factory=list) — auto-generated **init**
- Exception bubbling — borrow_book lets find_book's error travel up automatically
