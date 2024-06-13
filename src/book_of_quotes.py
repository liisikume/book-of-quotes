import csv
import re
from dataclasses import dataclass, field


@dataclass
class UserInputHandler:
    @staticmethod
    def get_valid_name_input():
        while True:
            user_name = input("Enter your first and last name: ").strip()
            name_parts = user_name.split()

            if len(name_parts) >= 1 and all(part.isalpha() for part in user_name.split()):
                return " ".join(part.capitalize() for part in name_parts)
            else:
                print("Invalid name. Please enter your first name and last name (optional) containing only letters.")

    @staticmethod
    def valid_email():
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+"

        while True:
            email = input("Enter your email here: ")
            if re.match(pattern, email):
                print(email, "\n")
                return email
            else:
                print("Oops! Invalid email. Try again.")


@dataclass
class BookOfQuotes:
    user_input_handler: UserInputHandler = field(default_factory=UserInputHandler)
    user: str = ""
    user_email: str = ""
    quotes: list[dict] = field(default_factory=list)
    file_path: str = "my_quotes.txt"

    def get_user_input(self):
        self.user = self.user_input_handler.get_valid_name_input()
        print(f"Username: {self.user} \n")
        self.user_email = self.user_input_handler.valid_email()

    def __post_init__(self):
        self.read_quotes_from_file()

    def read_quotes_from_file(self):
        try:
            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                self.quotes = [{"quote": row[0].strip(), "author": row[1].strip()} for row in reader if len(row) >= 2]
        except FileNotFoundError:
            print(f"File not found. Creating a new file at {self.file_path}.")
            with open(self.file_path, "w", newline="", encoding="utf-8") as file:
                pass  # Create an empty file

    def save_quotes_to_file(self):
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            for quote in self.quotes:
                file.write(f'"{quote["quote"]}", {quote["author"]}\n')

    def enter_quote(self, author, quote):
        new_quote = {"author": author, "quote": quote}
        self.quotes.append(new_quote)
        self.save_quotes_to_file()

        print(f"Quote by {author} added successfully.")

    def delete_quote(self):
        print("Select the quote you want to delete: ")
        self.view_all_quotes()

        try:
            quote_to_delete = int(input("Enter the number of the quote you want to delete: "))
            quote_index = quote_to_delete - 1
            if 0 <= quote_index < len(self.quotes):
                deleted_quote = self.quotes.pop(quote_index)["quote"]
                print(f"Quote '{deleted_quote}' removed successfully.")
            else:
                print(f"Invalid quote number.")

        except ValueError:
            print("Invalid number. Please provide a valid number: ")

    def edit_quote(self):
        print("Here's a list of quotes you can edit: ")
        self.view_all_quotes()

        try:
            quote_number = int(input("Select the number of the quote you want to edit: "))
            quote_index = quote_number - 1
            if 0 <= quote_index < len(self.quotes):
                edited_quote = input("Enter the new version of the quote you want to edit: ")
                old_quote = self.quotes[quote_index]["quote"]
                self.quotes[quote_index]["quote"] = edited_quote
                print("Quote edited successfully.")

                with open(self.file_path, "r", newline='', encoding="utf-8") as file:
                    lines = file.readlines()
                with open(self.file_path, "w", newline='', encoding="utf-8") as file:
                    for line in lines:
                        if old_quote in line:
                            file.write(f'{edited_quote},{self.quotes[quote_index]["author"]}\n')
                        else:
                            file.write(line)

            else:
                print("Invalid quote number.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def search_quotes_by_author_or_keyword(self):
        keyword_or_author = input("Enter the author or keyword you want to search: ").split(" ")
        keyword_or_author = [s.strip().lower() for s in keyword_or_author if s.strip()]
        keyword_or_author = " ".join(keyword_or_author)
        found_quotes = [
            quote
            for quote
            in self.quotes
            if keyword_or_author in quote["author"].lower() or keyword_or_author in quote["quote"].lower()
        ]
        if not found_quotes:
            print(f"No results found with '{keyword_or_author}'.")
        else:
            print(f"Results with '{keyword_or_author}': ")
            for i, quote in enumerate(found_quotes, start=1):
                print(f"{i}. '{quote['quote']}', {quote['author']}")

    def get_quote_iterator(self, page=1, page_size=10):
        start_idx = ((page - 1) * page_size)
        quote_start_nr = start_idx + 1

        if page_size == 0:  # special case - return all quotes
            for i, quote in enumerate(self.quotes, start=quote_start_nr):
                yield i, quote

        else:
            for i, quote in enumerate(self.quotes[start_idx:start_idx + page_size], start=quote_start_nr):
                yield i, quote

    def view_all_quotes(self, page=1, page_size=10):
        print(f"Showing {page_size} quotes from page {page} in this Book of Quotes:")
        print("  --- Quote --- | --- Author ---")
        for i, quote in self.get_quote_iterator(page, page_size):
            print(f"{i}. '{quote['quote']}' by {quote['author']}")


def main():
    book_of_quotes = BookOfQuotes()

    book_of_quotes.get_user_input()

    while True:
        print("*** Book of Quotes ***")
        print("---------------------------")
        print("1. Add author and quote")
        print("2. Delete quote")
        print("3. Edit quote")
        print("4. Search quotes by author or keyword")
        print("5. View all quotes")
        print("6. Exit")
        print("---------------------------")

        choice = input("Enter your choice between numbers 1-6: ")

        if choice == '1':
            author = input("Add the name of the author here: ").strip()
            author_name_parts = author.split()
            if len(author_name_parts) >= 1 and all(part.isalpha() or part == "'" for part in author.split()):
                author = " ".join(part.capitalize() for part in author_name_parts)
            else:
                print("Invalid name. Please enter a name containing only letters.")

            quote = input("Add the quote by this author here: ")
            book_of_quotes.enter_quote(author, quote)

        elif choice == '2':
            book_of_quotes.delete_quote()

        elif choice == '3':
            book_of_quotes.edit_quote()

        elif choice == '4':
            book_of_quotes.search_quotes_by_author_or_keyword()

        elif choice == '5':
            page_size = 10
            nr_pages = round(len(book_of_quotes.quotes) / page_size) or 1
            page = int(input(f"Enter page (1-{nr_pages}): "))
            book_of_quotes.view_all_quotes(page, page_size)

        elif choice == '6':
            print("Thank you for using the Book of Quotes")
            break

        else:
            print("Incorrect number. Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
