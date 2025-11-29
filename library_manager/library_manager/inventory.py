import json
from pathlib import Path
from typing import List, Optional
from .book import Book
import logging

LOG = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, path: str = "catalog.json"):
        self.path = Path(path)
        self.books: List[Book] = []
        self.load()

    def load(self):
        try:
            if not self.path.exists():
                self.books=[]
                return
            data=json.loads(self.path.read_text(encoding="utf-8"))
            self.books=[Book(**b) for b in data]
        except:
            self.books=[]

    def save(self):
        data=[b.to_dict() for b in self.books]
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add_book(self, title, author, isbn):
        if self.search_by_isbn(isbn):
            raise ValueError("Book with this ISBN exists.")
        b=Book(title,author,isbn)
        self.books.append(b)
        self.save()
        return b

    def search_by_title(self, query):
        q=query.lower()
        return [b for b in self.books if q in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return [str(b) for b in self.books]

    def issue_book(self, isbn):
        b=self.search_by_isbn(isbn)
        if not b: return False
        ok=b.issue()
        if ok: self.save()
        return ok

    def return_book(self, isbn):
        b=self.search_by_isbn(isbn)
        if not b: return False
        ok=b.return_book()
        if ok: self.save()
        return ok
