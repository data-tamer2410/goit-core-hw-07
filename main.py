"""Консольний бот помічник(2.0), який розпізнає команди, що вводяться з клавіатури,
                                    та відповідає відповідно до введеної команди."""

from functionality_for_bot import AddressBook, Record, ValidationError


def input_error(func):
    """Декоратор для обробки винятків."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as ex:
            return ex
        except (ValueError, IndexError) as ex:
            if str(ex)[1:11].isdigit() or str(ex).startswith('Invalid date'):
                return str(ex) + '.'
            else:
                return 'Enter the argument for the command.'
        except (AttributeError, KeyError):
            return 'Contact not found.'

    return inner


@input_error
def parse_input(user_input: str) -> tuple[str, str] | str:
    """
    Парсер команд ведених користувачем з консолі.

    :param user_input:
    :return: Кортеж з обробленим веденням користувача.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """
    Додає контакт до записної книги.

    :param args: Список з веденням користувача.
    :param book: Бажана записна книга.
    :return: Рядок логування для користувача.
    """

    name, phone = args[:2] if len(args[:2]) == 2 else (args[0], None)
    record = book.find(name)
    msg = 'Contact update.'
    if record is None:
        record = Record(name)
        book.add_record(record)
        msg = 'Contact added.'
    if phone:
        record.add_phone(phone)
    return msg


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
    record.edit_phone(old_phone, new_phone)
    return 'Contact changed.'


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
    record.remove_phone(phone)
    return 'Phone remove.'


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """
    Видаляє контакт.

    :param args: Список з веденням користувача.
    :param book: Бажана записна книга.
    :return: Рядок логування для користувача.
    """
    name, *_ = args
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
    return f'Phones: {'; '.join(str(p) for p in record.phones)}'


@input_error
def show_all_contacts(book: AddressBook) -> AddressBook:
    """
    Повертає записну книгу для друку всіх записів.

    :param book: Бажана записна книга.
    :return: Об'єкт записної книги типу AddressBook.
    """
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
    msg = 'Birthday update.'
    if record.birthday is None:
        msg = 'Birthday added.'
    record.add_birthday(birthday)
    return msg


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
    return f'Birthday: {str(record.birthday)}'


@input_error
def birthdays(book: AddressBook) -> str:
    """
    Визначає контакти, у яких день народження припадає вперед на 7 днів включаючи поточний день.

    :param book: Бажана записна книга.
    :return: Рядок з іменами та датами привітання.
    """
    res = ''
    count_rec = 1
    for d in book.get_upcoming_birthdays():
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
