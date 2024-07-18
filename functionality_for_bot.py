"""Функціонал для консольного бота помічника(2.0), який розпізнає команди, що вводяться з клавіатури,
                                    та відповідає відповідно до введеної команди."""
from collections import UserDict
from datetime import datetime, timedelta


class ValidationError(Exception):
    pass


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str | datetime):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону. Має валідацію формату (10 цифр)."""

    def __init__(self, value: str):
        if value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValidationError('The phone must have 10 numbers.')


class Birthday(Field):
    """Клас для зберігання дати дня народження в форматі DD.MM.YY."""

    def __init__(self, value: str):
        try:
            birthday = datetime.strptime(value, '%d.%m.%Y')
            super().__init__(self.__validation(birthday))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    @staticmethod
    def __validation(birthday: datetime) -> datetime:
        """
        Виконую валідацію вхідної дати.

        :param birthday: Бажана дата.
        :return: Вхідну дату якщо вона пройшла провірку.
        """
        now = datetime.now()
        if birthday.date() <= now.date():
            return birthday
        else:
            raise ValidationError('Incorrect date.')

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я, список телефонів та дату народження."""

    def __init__(self, name: str, phone: str = None):
        self.name = Name(name)
        self.phones = Phone(phone) if phone else []
        self.birthday = None

    def add_birthday(self, birthday: str):
        """
        Додавання дати народження.

        :param birthday: Бажана дата народження.
        """
        self.birthday = Birthday(birthday)

    def add_phone(self, phone: str):
        """
        Додавання телефонів.

        :param phone: Бажаний номер телефону.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """
        Видалення телефонів.

        :param phone: Бажаний номер телефону.
        """
        i = [v.value for v in self.phones].index(Phone(phone).value)
        self.phones.pop(i)

    def edit_phone(self, old_phone: str, new_phone: str):
        """
        Редагування телефонів.

        :param old_phone: Старий номер телефону.
        :param new_phone: Новий номер телефону.
        """
        i = [v.value for v in self.phones].index(Phone(old_phone).value)
        self.phones[i] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        """
        Пошук телефону.

        :param phone: Бажаний номер телефону.
        :return: Об'єкт номера телефону(Phone) за вказаним номером(phone).
        """
        res = [p for p in self.phones if p.value == Phone(phone).value]
        if not res:
            return None
        return res[0]

    def __str__(self):
        return (f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)},"
                f" birthday: {str(self.birthday)}")


class AddressBook(UserDict):
    """Клас для зберігання та управління записами."""

    def get_upcoming_birthdays(self) -> list[dict]:
        """
        Визначає контакти, у яких день народження припадає вперед на 7 днів включаючи поточний день.

        :return: Список словників з датами привітання.
        """
        now = datetime.now()
        res = []
        for rec in self.data.values():
            if rec.birthday is None:
                continue

            birthday = rec.birthday.value.replace(year=now.year)
            if birthday.date() < now.date():
                birthday = birthday.replace(year=now.year + 1)

            if 0 <= birthday.toordinal() - now.toordinal() <= 7:
                weekday = birthday.weekday()
                if weekday == 5 or weekday == 6:
                    days = 7 - weekday
                    birthday = birthday + timedelta(days=days)
                birthday = birthday.strftime('%d.%m.%Y')
                res.append({'name': str(rec.name), 'birthday': birthday})
        return res

    def add_record(self, record: Record):
        """
        Додавання записів.

        :param record: Бажаний запис.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """
        Пошук записів за іменем.

        :param name: Бажане ім'я для пошуку запису.
        :return: Об'єкт запису(Records) за вказаним ім'ям(name).
        """
        return self.data.get(name)

    def delete(self, name: str):
        """
        Видалення записів за іменем.

        :param name: Бажане ім'я для видалення запису.
        """
        self.data.pop(name)

    def __str__(self):
        res = ''
        count_rec = 1
        for key in self.data:
            res += f'{count_rec}. {self.data[key]};\n'
            count_rec += 1
        return res
