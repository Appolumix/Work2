from typing import List, Iterator, Generator
from pydantic import BaseModel
import logging


class BookModel(BaseModel):
    title: str
    author: str
    year: int


class Book:
    def __init__(self, book_model: BookModel):
        self.book_model = book_model

    def __repr__(self):
        return f"{self.book_model.title} by {self.book_model.author} ({self.book_model.year})"

    def info(self):
        return f"Назва: {self.book_model.title}, Автор: {self.book_model.author}, Рік видання: {self.book_model.year}"


class Library:  
    def __init__(self):
        self._books: List[Book] = []


    @staticmethod
    def log_add_book(func):
        def wrapper(self, book: Book):
            logging.info(f"Додається нова книга: {book.info()}")
            func(self, book)
        return wrapper


    @staticmethod
    def check_book_exists(func):
        def wrapper(self, book_title: str):
            if any(book.book_model.title == book_title for book in self._books):
                func(self, book_title)
            else:
                logging.error(f"Книги '{book_title}' немає у бібліотеці")
        return wrapper

    @log_add_book
    def add_book(self, book: Book):
        self._books.append(book)

    @check_book_exists
    def remove_book(self, book_title: str):
        self._books = [book for book in self._books if book.book_model.title != book_title]

    def __iter__(self) -> Iterator[Book]:
        return iter(self._books)

    def books_by_author(self, author: str) -> Generator[Book, None, None]:
        for book in self._books:
            if book.book_model.author == author:
                yield book

class FileManager:
    @staticmethod
    def save_books_to_file(library: Library, filename: str):
        with open(filename, 'w') as f:
            for book in library:
                f.write(f"{book.info()}\n")
        logging.info(f"Список книг збережено у файл {filename}")

    @staticmethod
    def load_books_from_file(filename: str) -> List[Book]:
        books = []
        with open(filename, 'r') as f:
            for line in f:
                title, author, year = line.strip().split(', ')
                book_model = BookModel(title=title, author=author, year=int(year))
                book = Book(book_model)
                books.append(book)
        logging.info(f"Список книг завантажено з файлу {filename}")
        return books

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    library = Library()
    book1 = Book(BookModel(title="Book 1", author="Author 1", year=2000))
    book2 = Book(BookModel(title="Book 2", author="Author 2", year=2005))
    library.add_book(book1)
    library.add_book(book2)


    print("Усі книги у бібліотеці:")
    for book in library:
        print(book)

    library.remove_book("Book 1")
    print("\nКнига 'Book 1' видалена з бібліотеки. Оновлений список книг:")
    for book in library:
        print(book)

    print("\nКниги автора 'Author 2':")
    for book in library.books_by_author("Author 2"):
        print(book)

