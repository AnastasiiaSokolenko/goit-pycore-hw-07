"""
Assistant Bot

A simple console bot for managing contacts.

Available commands:

- hello
    Greets the user.

- add <name> <phone>
    Adds a new contact or adds a phone number to an existing contact.

- change <name> <old_phone> <new_phone>
    Updates an existing contact's phone.

- phone <name>
    Shows the phone numbers for a contact.

- all
    Lists all saved contacts.

- add-birthday <name> <DD.MM.YYYY>
    Adds a birthday to a contact.

- show-birthday <name>
    Shows a contact's birthday.

- birthdays
    Lists users whose birthdays are coming up in the next 7 days, and on which day they should be congratulated.

- exit or close
    Exits the bot.

If input is incorrect or missing, helpful error messages will be shown.
"""

from collections import UserDict
from datetime import datetime, date, timedelta
import re

# ----------------------
# Data Classes
# ----------------------

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self._is_valid(value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

    @staticmethod
    def _is_valid(value):
        return bool(re.fullmatch(r"\d{10}", value))

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        if self.find_phone(phone_number):
            raise ValueError(f"Phone {phone_number} already exists.")
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_number, new_number):
        phone = self.find_phone(old_number)
        if phone:
            self.add_phone(new_number)
            self.phones.remove(phone)

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "None"
        birthday_str = self.birthday.value if self.birthday else "None"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.date
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days
                if 0 <= delta_days <= 7:
                    if birthday_this_year.weekday() == 5:
                        congratulation_date = birthday_this_year + timedelta(days=2)
                    elif birthday_this_year.weekday() == 6:
                        congratulation_date = birthday_this_year + timedelta(days=1)
                    else:
                        congratulation_date = birthday_this_year

                    congratulation_date_str = congratulation_date.strftime("%d.%m.%Y")
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date_str
                    })

        return upcoming_birthdays

# ----------------------
# Bot Logic
# ----------------------

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter a command and necessary arguments."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return f"Phone number updated for {name}."

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if record.phones:
        return f"{name}: " + "; ".join(phone.value for phone in record.phones)
    else:
        return f"{name} has no phone numbers."

def show_all(book: AddressBook):
    if not book.data:
        return "No contacts available."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found. Add the contact first."
    record.add_birthday(birthday_str)
    return f"Birthday added for {name}."

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    if record.birthday:
        return f"{name}'s birthday is {record.birthday.value}"
    else:
        return f"No birthday set for {name}."

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays this week."
    result = []
    for item in upcoming:
        result.append(f"{item['name']} should be congratulated on {item['congratulation_date']}")
    return "\n".join(result)

# ----------------------
# CLI Loop
# ----------------------

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            print("Please enter a command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command. Choose from: hello, add, change, phone, all, add-birthday, show-birthday, birthdays, close, exit.")

if __name__ == "__main__":
    main()