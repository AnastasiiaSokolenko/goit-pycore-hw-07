# goit-pycore-hw-07
Home work for Topic 10: Add birthday functionality to the AddressBook class. Update assistant bot to use AddressBook.

# Assistant Bot

A simple Python console bot for managing contacts and birthdays.

## Features

This bot helps you:

✅ Add, update, and display contacts and phone numbers  
✅ Manage birthdays for your contacts  
✅ See upcoming birthdays in the next 7 days, adjusted for weekends  
✅ Handle errors gracefully with helpful messages

---

## Commands

### Basic Commands

- **hello**  
    Prints a greeting from the bot.

- **add <name> <phone>**  
    Adds a new contact with a phone number, or adds a phone to an existing contact.  
    - Example:

      ```
      add John 0501234567
      ```

- **change <name> <old_phone> <new_phone>**  
    Changes a phone number for a contact.  
    - Example:

      ```
      change John 0501234567 0987654321
      ```

- **phone <name>**  
    Displays all phone numbers for a contact.  
    - Example:

      ```
      phone John
      ```

- **all**  
    Lists all saved contacts with phones and birthdays.

- **close** or **exit**  
    Exits the bot.

---

### Birthday Commands (Task 02)

- **add-birthday <name> <DD.MM.YYYY>**  
    Adds a birthday for the specified contact.  
    - Example:

      ```
      add-birthday John 20.07.1990
      ```

- **show-birthday <name>**  
    Displays the birthday for the specified contact.  
    - Example:

      ```
      show-birthday John
      ```

- **birthdays**  
    Lists users whose birthdays fall in the next 7 days and on which date they should be congratulated.  
    Birthdays falling on weekends are shifted to Monday.  
    - Example output:

      ```
      John should be congratulated on 21.07.2025
      ```

---

## Validation Rules

- Phone numbers **must be exactly 10 digits.**  
- Birthday format is **DD.MM.YYYY** (e.g. `20.07.1990`).

---

## Error Handling

- The bot will prompt you if you enter:
  - An unknown command
  - Missing arguments
  - Invalid phone numbers
  - Invalid birthday format

---

## How to Run

Run the script from the terminal:

```bash
python assistant_bot.py
```
