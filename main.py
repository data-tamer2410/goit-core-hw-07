"""Консольний бот помічник(2.0), який розпізнає команди, що вводяться з клавіатури,
                                    та відповідає відповідно до введеної команди."""

from functionality_for_bot import AddressBook, Record, ContactNotFoundError, ValidationError, BirthdayNotFoundError, \
    PhoneNotFoundError


def input_error(func):
    """Декоратор для обробки винятків."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PhoneNotFoundError as ex:
            return ex
        except ContactNotFoundError as ex:
            return ex
        except ValueError as ex:
            if str(ex).startswith('Invalid date'):
                return ex
            else:
                return 'Enter the argument for the command.'
        except BirthdayNotFoundError as ex:
            return ex
        except ValidationError as ex:
            return ex

    return inner


@input_error
def parse_input(user_input: str) -> tuple[str, str] | str:
    """
    Парсер команд ведених користувачем з консолі.

    :param user_input:
    :return: Кортеж з обробленим веденням користувача.
    """
    try:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args
    except ValueError:
        return 'Error'


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """
    Додає контакт до записної книги.

    :param args: Список з веденням користувача.
    :param book: Бажана записна книга.
    :return: Рядок логування для користувача.
    """
    name, *phones = args
    record = book.find(name)
    if record is None:
        book.add_record(Record(name, set(phones)))
        return 'Contact added.'
    else:
        for phone in phones:
            if record.find_phone(phone) is None:
                record.add_phone(phone)
        return 'Contact updated.'


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """
    Змінює номер телефону.

    :param args: Список з веденням користувача.
    :param book: Бажана записна книга.
    :return: Рядок логування для користувача.
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise ContactNotFoundError
    elif record.find_phone(old_phone) is None:
        raise PhoneNotFoundError
    else:
        if record.find_phone(new_phone) is None:
            record.edit_phone(old_phone, new_phone)
        else:
            if old_phone != new_phone:
                record.remove_phone(old_phone)
        return f'Contact changed.'


@input_error
def remove_phone(args: list[str], book: AddressBook) -> str:
    """
    Видаляє номер телефону.

    :param args: Список з веденням користувача.
    :param book: Бажана записна книга.
    :return: Рядок логування для користувача.
    """
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        raise ContactNotFoundError
    elif record.find_phone(phone) is None:
        raise PhoneNotFoundError
    else:
        record.remove_phone(phone)
        return 'Phones remove.'


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """
    Видаляє контакт.

    :param args: Список з веденням користувача.
    :param book: Бажана записна книга.
    :return: Рядок логування для користувача.
    """
    name, *_ = args
    if book.find(name) is None:
        raise ContactNotFoundError
    else:
        book.delete(name)
        return 'Contact delete.'


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """
    Повертає номера телефонів бажаного контакту.

    :param args: Список з веденням користувача.
    :param book: Бажана записна книга.
    :return: Рядок з номерами телефонів.
    """
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ContactNotFoundError
    else:
        return f'Phones: {'; '.join(str(p) for p in record.phones)}'


@input_error
def show_all_contacts(book: AddressBook) -> AddressBook:
    """
    Повертає записну книгу для друку всіх записів.

    :param book: Бажана записна книга.
    :return: Об'єкт записної книги типу AddressBook.
    """
    if not book:
        raise ContactNotFoundError
    else:
        return book


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """
    Додає дату народження до контакту.

    :param args: Список з веденням користувача.
    :param book: Бажана записна книга.
    :return: Рядок логування для користувача.
    """
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise ContactNotFoundError
    elif record.birthday is not None:
        record.add_birthday(birthday)
        return 'Birthday updated'
    else:
        record.add_birthday(birthday)
        return 'Birthday added.'


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """
    Повертає дату дня народження бажаного контакту.

    :param args: Список з веденням користувача.
    :param book: Бажана записна книга.
    :return: Рядок з датою народження.
    """
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ContactNotFoundError
    elif record.birthday is None:
        raise BirthdayNotFoundError
    else:
        return f'Birthday: {str(record.birthday)}'


@input_error
def birthdays(book: AddressBook) -> str:
    """
    Визначає контакти, у яких день народження припадає вперед на 7 днів включаючи поточний день.

    :param book: Бажана записна книга.
    :return: Рядок з іменами та датами привітання.
    """
    if not book:
        raise ContactNotFoundError
    else:
        res = ''
        count_rec = 1
        for d in book.get_upcoming_birthdays:
            res += f'{count_rec}. Contact name: {d['name']}, birthday: {d['birthday']};\n'
            count_rec += 1
        return res


def main():
    """Головна функція."""
    book = AddressBook()
    print('Welcome to the assistant bot!')
    while True:
        user_input = input('Enter a command:')
        command, *args = parse_input(user_input)

        if command in ['close', 'exit']:
            print('Good bye!')
            break
        elif command == 'hello':
            print('How can I help you?')
        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'remove-phone':
            print(remove_phone(args, book))
        elif command == 'phone':
            print(show_phone(args, book))
        elif command == 'all':
            print(show_all_contacts(book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(args, book))
        elif command == 'birthdays':
            print(birthdays(book))
        elif command == 'delete':
            print(delete_contact(args, book))
        else:
            print('Invalid command.')


if __name__ == '__main__':
    main()
