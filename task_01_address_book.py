from collections import UserDict
from datetime import datetime, timedelta
import re

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
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_number, new_number):
        phone = self.find_phone(old_number)
        if phone:
            self.phones.remove(phone)
            self.add_phone(new_number)

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
        today = datetime.today().date()
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

# Example usage
if __name__ == "__main__":
    book = AddressBook()

    jane = Record("Jane")
    jane.add_birthday("14.07.1995")
    book.add_record(jane)

    mark = Record("Mark")
    mark.add_birthday("19.07.1995") # Saturday
    book.add_record(mark)

    john = Record("John")
    john.add_birthday("20.07.1990") # Sunday
    book.add_record(john)

    sonia = Record("Sonia")
    sonia.add_birthday("22.07.1978") # More than 7 days away
    book.add_record(sonia)

    upcoming = book.get_upcoming_birthdays()
    for item in upcoming:
        print(f"{item['name']} should be congratulated on {item['congratulation_date']}")
