import pandas as pd
from datetime import datetime, timedelta

# CSV file import
df_books = pd.read_csv("books.csv", dtype={"id": str})
df_members = pd.read_csv("members.csv", dtype={"id": str})
df_loans = pd.read_csv("loans.csv", dtype=str)


class Book:
    def __init__(self, book_id):
        self.book_id = book_id
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
        return f"Downloading: {self.title} from {self.download_url}"


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


class PremiumMember(Member):
    def __init__(self, member_id):
        super().__init__(member_id)
        self.max_books = 10

    def extend_loan(self, book_id):
        """Extend the loan period"""
        loan_index = df_loans.loc[
            (df_loans["member_id"] == self.member_id)
            & (df_loans["book_id"] == book_id)
            & (df_loans["returned"] == "no")
        ].index

        if not loan_index.empty:
            # Return date extended by 7 days
            current_due = pd.to_datetime(df_loans.loc[loan_index[0], "due_date"])
            new_due = current_due + timedelta(days=7)
            df_loans.loc[loan_index[0], "due_date"] = new_due.strftime("%Y-%m-%d")
            df_loans.to_csv("loans.csv", index=False)
            return f"Loan extended until {new_due.strftime('%Y-%m-%d')}"
        return "Book not found in your loans"


class LibraryCard:
    def __init__(self, member_id, pin):
        self.member_id = member_id
        self.pin = pin

    def authenticate(self):
        """Library card authentication"""
        member_data = df_members.loc[df_members["id"] == self.member_id, "pin"]
        if member_data.empty:
            return False  # Member ID not found
        stored_pin = str(member_data.squeeze())  # Convert to string
        return self.pin == stored_pin


class LoanReceipt:
    def __init__(self, member_name, book_title, due_date):
        self.member_name = member_name
        self.book_title = book_title
        self.due_date = due_date

    def generate(self):
        """Generate a loan receipt"""
        content = f"""
        === Library Loan Receipt ===
        Member Name: {self.member_name}
        Book Title: {self.book_title}
        Loan Date: {datetime.now().strftime('%Y-%m-%d')}
        Due Date: {self.due_date}
        ================================
        Please return by the due date!
        """
        return content


def main():
    print("=== Library Management System ===")
    print("Book Collection:")
    print(df_books[["id", "title", "author", "available"]])
    print()
    print("Available Member IDs: M001, M002, M003")
    print()

    # Member authentication
    member_id = input("Please enter your member ID: ")

    # Check if member exists
    if member_id not in df_members["id"].values:
        print(f"Member ID '{member_id}' not found.")
        print("Available Member IDs: M001, M002, M003")
        return

    pin = input("Please enter your PIN: ")

    card = LibraryCard(member_id, pin)
    if not card.authenticate():
        print("Authentication failed. Please check your PIN.")
        return

    # Branch by membership type
    member_type = df_members.loc[df_members["id"] == member_id, "type"].squeeze()
    if member_type == "premium":
        member = PremiumMember(member_id)
        print(f"Welcome, {member.name}! (Premium Member)")
    else:
        member = Member(member_id)
        print(f"Welcome, {member.name}!")

    if not member.is_valid():
        print("Member status is invalid.")
        return

    # Choice of books
    book_id = input("Please enter the ID of the book you want to borrow: ")

    # Check if book exists
    if book_id not in df_books["id"].values:
        print(f"Book ID '{book_id}' not found.")
        return

    # Check if it's a digital book
    book_type = df_books.loc[df_books["id"] == book_id, "type"].squeeze()
    if book_type == "digital":
        book = DigitalBook(book_id)
        print(book.download())
    else:
        book = Book(book_id)

    if not book.is_available():
        print("Sorry, this book is currently on loan.")
        return

    # Loan processing
    book.borrow()
    print(f"'{book.title}' has been loaned out!")

    # Add loan record
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    new_loan = {
        "loan_id": f"L{len(df_loans) + 1:03d}",
        "member_id": member_id,
        "book_id": book_id,
        "loan_date": datetime.now().strftime("%Y-%m-%d"),
        "due_date": due_date,
        "returned": "no",
    }

    # Add new row to df_loans
    df_loans.loc[len(df_loans)] = new_loan
    df_loans.to_csv("loans.csv", index=False)

    # Generate receipt
    receipt = LoanReceipt(member.name, book.title, due_date)
    print(receipt.generate())

    # Extension option for premium members
    if isinstance(member, PremiumMember):
        extend = input("Would you like to extend the loan period? (yes/no): ")
        if extend.lower() == "yes":
            print(member.extend_loan(book_id))


if __name__ == "__main__":
    main()
