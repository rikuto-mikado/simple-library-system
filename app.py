import pandas as pd
from datetime import datetime, timedelta

# CSV file import
df_books = pd.read_csv("books.csv", dtype={"id": str})
df_members = pd.read_csv("members.csv", dtype={"id": str})
df_loans = pd.read_csv("loans.csv", dtype=str)


class Book:
    def __init__(self, book_id):
        self.book = book_id
        self.title = df_books.loc[df_books["id"] == self.book_id, "title"].squeeze()
        self.author = df_books.loc[df_books["id"] == self.book_id, "author"].squeeze()
        self.genre = df_books.loc[df_books["id"] == self.book_id, "genre"].squeeze()

    def is_available(self):
        """Check whether the book is available for loan"""
        status = df_books.loc[df_books["id"] == self.book_id, "available"].squeeze()
        return status == "yes"

    def borrow(self):
        """Place the book on loan"""
        df_books.loc[df_books["id"] == self.book_id, "available"] = "no"
        df_books.to_csv("books.csv", index=False)

    def return_book(self):
        """Return the book to its returned state"""
        df_books.loc[df_books["id"] == self.book_id, "available"] = "yes"
        df_books.to_csv("books.csv", index=False)


class DigitalBook(Book):
    def __init__(self, book_id):
        super().__init__(book_id)
        self.download_url = df_books.loc[
            df_books["id"] == self.book_id, "download_url"
        ].squeeze()

    def download(self):
        """Download digital books (simulate)"""
        return f"📱 Downloading: {self.title} from {self.download_url}"


class Member:
    def __init__(self, member_id):
        self.member_id = member_id
        self.name = df_members.loc[df_members["id"] == self.member_id, "name"].squeeze()
        self.email = df_members.loc[
            df_members["id"] == self.member_id, "email"
        ].squeeze()
        self.member_type = df_members.loc[
            df_members["id"] == self.member_id, "type"
        ].squeeze()

    def is_valid(self):
        """Check whether the member is valid"""
        status = df_members.loc[df_members["id"] == self.member_id, "active"].squeeze()
        return status == "yes"

    def get_borrowed_books(self):
        """Obtain a list of borrowed books"""
        borrowed = df_loans.loc[
            (df_loans["member_id"] == self.member_id) & (df_loans["returned"] == "no")
        ]
        return borrowed["book_id"].tolist()
