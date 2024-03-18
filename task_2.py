from collections import UserDict
import re


def input_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except ValueError:
            return 'For "add" and "change" give me name and phone.\n'\
                'For "phone" give me name.\n'\
                'For "all" give me no arguments.'
        except KeyError:
            return 'Contact does not exists!'
        except PhoneFormatException:
            return 'Number should contain 10 digits!'
    return inner


class PhoneFormatException(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        match = re.fullmatch('\\d{10}', value)

        # Exception for future error handling
        if match == None:
            raise PhoneFormatException('Number should contain 10 digits!')

        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f'Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}'

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_list = [phone.value for phone in self.phones]
        index = phone_list.index(phone)
        self.phones.pop(index)

    def edit_phone(self, old_phone, new_phone):
        phone_list = [phone.value for phone in self.phones]
        index = phone_list.index(old_phone)
        self.phones[index].value = new_phone

    def find_phone(self, phone):
        phone_list = [phone.value for phone in self.phones]
        index = phone_list.index(phone)
     
        return self.phones[index].value


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data[name]

    def delete(self, name):
        self.data.pop(name)


def main():
    book = AddressBook()
    print(book)

    john_record = Record('John')
    john_record.add_phone('1234567890')
    john_record.add_phone('5555555555')
    book.add_record(john_record)

    jane_record = Record('Jane')
    jane_record.add_phone('9876543210')
    book.add_record(jane_record)

    for record in book.data.values():
        print(record)

    john = book.find('John')
    john.edit_phone('5555555555', '1112223333')
    print(john)  # Displaying: Contact name: John, phones: 1112223333; 5555555555
    john.remove_phone('1112223333')
    print(john)  # Displaying: Contact name: John, phones: 1112223333; 5555555555

    found_phone = john.find_phone('1234567890')
    print(f"{john.name}: {found_phone}")  

    book.delete('Jane')
    print(book)


if __name__ == '__main__':
    main()
