from dataclasses import dataclass, asdict

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"

    def __str__(self):
        return f"{self.title} - {self.author} (ISBN: {self.isbn}) [{self.status}]"

    def to_dict(self):
        return asdict(self)

    def issue(self):
        if self.status == "issued":
            return False
        self.status = "issued"
        return True

    def return_book(self):
        if self.status == "available":
            return False
        self.status = "available"
        return True

    def is_available(self):
        return self.status == "available"
