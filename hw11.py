from collections import UserDict
from datetime import datetime


def input_error(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            return 'Wrong name'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'Pls print: name and number'
        except TypeError:
            return 'Wrong command.'
    return wrapper


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


    def iterator(self, page_number, num_of_records):
        new_data = list(self.data.items())
        total_items = page_number * num_of_records
        yield list(new_data[(total_items - num_of_records):total_items])


class Record:
    def __init__(self, new_name):
        self.name = Name(new_name)
        self.phones = []
        self.birthday = None


    @input_error
    def add_phone(self, new_phone):
        add_phone = Phone()
        add_phone.value = new_phone
        self.phones.append(add_phone)


    @input_error
    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                new_pn = Phone()
                new_pn.value = new_phone
                self.phones.append(new_pn)
                self.phones.remove(phone)
        


    def remove_phone(self, old_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.phones.remove(phone)
        else:
            print("Phone number does't exist")


    @input_error
    def add_birthday(self, birthday):
        bday = Birthday()
        bday.value = birthday
        self.birthday = bday


    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            if self.birthday.value.replace(year=today.year) >= today:
                result = self.birthday.value.replace(year=today.year) - today
            else:
                result = self.birthday.value.replace(
                    year=today.year) - today.replace(year=today.year - 1)
            print(result)
        else:
            print('Empty')


    def __repr__(self):
        return f'{self.phones}'


class Field:
    def __init__(self):
        self.value = None


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __init__(self, name) -> None:
        self.value = name


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if len(value) < 10 or len(value) > 12:
            raise ValueError("Phone must contains 10 symbols.")
        if not value.isnumeric():
            raise ValueError('Wrong phones.')
        self._value = value


    
class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        birth_date = datetime.strptime(value, '%Y-%m-%d').date()
        if birth_date > today:
            raise ValueError("Birthday must be less than current year and date.")
        self._value = value


addressbook = AddressBook()


@input_error
def get_user_input():
    user_input = input('Enter command: ').lower().split(' ')
    return user_input


@input_error
def get_handler(actions):
    return OPERATIONS[actions]


def hello_func(*args):
    print('How can I help you?')


@input_error
def add_func(user_input):
    if user_input[1] not in addressbook.data:
        add_record = Record(user_input[1])
        add_record.add_phone(user_input[2])
        addressbook.add_record(add_record)
        print(f'New contact added')
    else:
        add_phone = addressbook.data[user_input[1]]
        add_phone.add_phone(user_input[2])
        print(f'New phone number to {user_input[1]} has been added')


@input_error
def change_func(user_input):
    if user_input[1] in addressbook.data:
        old_phone = input('Enter phone number to change: ')
        renew_phone = addressbook.data[user_input[1]]
        renew_phone.change_phone(old_phone, user_input[2])
        print(f'Phone number {old_phone} has been changed to {user_input[2]}')
    else:
        print(f"Contact {user_input[1]} doesn't exist")


@input_error
def phone_func(user_input):
    if user_input[1] in addressbook.data:
        print(
            f'{user_input[1]} has {addressbook.data[user_input[1]]} phone number')
    else:
        print(f"Contact '{user_input[1]}' doesn't exist")


@input_error
def delete_func(user_input):
    if user_input[1] in addressbook.data:
        addressbook.data.pop(user_input[1])
        print(f'Contact "{user_input[1]}" has been deleted')
    else:
        print(f"Contact '{user_input[1]}' doesn't exist")


@input_error
def remove_phone_func(user_input):
    if user_input[1] in addressbook.data:
        removing = addressbook.data[user_input[1]]
        removing.remove_phone(user_input[2])
        print(f'Phone number "{user_input[2]}" has been removed')
    else:
        print(f"Contact '{user_input[1]}' doesn't exist")


@input_error
def set_birthday(user_input):
    if user_input[1] in addressbook.data:
        setbday = addressbook.data[user_input[1]]
        setbday.add_birthday(user_input[2])
        print(f'Birthday {user_input[2]} has added to {user_input[1]}')
    else:
        print(f"Contact '{user_input[1]}' doesn't exist")


@input_error
def show_birthday(user_input):
    if user_input[1] in addressbook.data:
        addressbook.data[user_input[1]].days_to_birthday()
    else:
        print(f"Contact '{user_input[1]}' doesn't exist")


@input_error
def show_all_func(*args):
    page_number = int(input('Enter page number: '))
    num_of_records = int(input('How many records we need: '))
    page = addressbook.iterator(page_number, num_of_records)
    print(next(page))


def break_func(*a):   
    result = 'Good bye, see you soon:)'
    print('Good bye, see you soon:)')
    return result


OPERATIONS = {
    'hello': hello_func,
    'add': add_func,
    'change': change_func,
    'phone': phone_func,
    'delete': delete_func,
    'remove': remove_phone_func,
    'set_birthday': set_birthday,
    'birthday': show_birthday,
    'show all': show_all_func,
    'good bye': break_func,
    'close': break_func,
    'exit': break_func
}


def main():
    print('Hello, your assistants start working)')
    while True:
        user_input = get_user_input()

        if user_input == ['']:
            continue
        elif user_input[0] == 'show':
            actions = 'show all'
        else:
            actions = user_input[0]

        handler = get_handler(actions)
        if handler is None:
            continue

        result = handler(user_input)
        if result == 'Good bye, see you soon:)':
            break


if __name__ == '__main__':
    main()