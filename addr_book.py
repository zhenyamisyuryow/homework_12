from collections import UserDict
from collections.abc import Iterator
import re
from datetime import datetime

class AddressBook(UserDict):

    def add_record(self, record):
        key = record.name.value
        value = record
        self.data[key] = value
        
    def get_record(self, name):
        return f"{self.data[name].phones}"
    
    def iterator(self, number):
        current_index = 0
        records = list(self.data.values())
        if number < 0: number*-number
        while current_index < len(records):
            yield records[current_index:current_index+number]
            current_index += number

    
class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __repr__(self):
        return f"{self._value}"

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, new_value):
        result = re.findall(r"^(?=\+\d{3}\(\d{2}\)\d{3}-\d{1,2}-\d{2,3}).{17}$", new_value)
        if not result:
            raise ValueError
        self._value = new_value
   

class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, birthday):
        try:
            birthday = datetime.strptime(birthday, "%d-%m-%Y")
            if birthday.year > datetime.now().year:
                raise ValueError(f"Unable to add {birthday} as it's year is in the a future.")
            else:
                self._value = birthday.date()
        except:
            raise ValueError

class Record:
    def __init__(self, name:Name, phone:Phone, birthday:Birthday = None):
        self.name = name
        self.phones = list()
        self.phones.append(phone)
        self.birthday = birthday
    
    def add_phone(self, new_phone):
        if new_phone.value in [x.value for x in self.phones]:
            return False
        self.phones.append(new_phone)
        return True
    
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return True
        return False
    
    def del_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)
                return True
        return False
    
    def add_birthday(self, birthday):
        self.birthday = birthday

    def days_to_birthday(self, birthday:Birthday):
        if not isinstance(birthday, Birthday):
            raise ValueError
        today = datetime.today().date()
        bd_month = birthday.value.month
        bd_day = birthday.value.day
        delta1 = datetime(today.year, bd_month, bd_day).date()
        delta2 = datetime(today.year+1, bd_month, bd_day-1).date()
        return ((delta1 if delta1 > today else delta2) - today).days

    def __repr__(self):
        if self.birthday:
            return f"Name: {self.name.value}\nPhones: {self.phones}\nBirthday: {self.birthday}\nDays until birthday: {self.days_to_birthday(self.birthday)}"
        return f"Name: {self.name.value}\nPhones: {self.phones}\nBirthday: {self.birthday}"
