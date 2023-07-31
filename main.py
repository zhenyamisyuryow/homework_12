from addr_book import *


contacts = AddressBook()

def input_error(func):
    def handler(*args):
        argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
        try:
            return func(*args)
        except KeyError:
            return "Error: key doesn't exist."
        except ValueError:
            return "Error: invalid format. Correct format for phone is: +380(12)345-67-89. For birthday: DD-MM-YYYY"
        except IndexError:
            return "Error: provide both name and phone number."
        except TypeError:
            return f"Error: provide all required parameters: {', '.join(argnames)}"
    return handler


@input_error
def hello(*args):
    return "Hi! How can I help you today?"


@input_error
def showall():
    number = int(input("How many records would you like to retrieve in one iteration?\n>>> "))
    result = contacts.iterator(number)
    for records_batch in result:
        for i in records_batch:
            print(i,"\n")
        answer = input("Press Enter to continue. Press Q to exit.\n>>> ")
        if answer.upper() == "Q":
            break
    return f"Total contacts: {len(contacts)}.\nEnter the command: "


@input_error
def add(name:str, *args) -> None:
    if name not in contacts.data:
        name = Name(name)
        phone = Phone(args[0])
        rec = Record(name, phone)
        if len(args) > 1:
            birthday = Birthday(args[1])
            rec.add_birthday(birthday)
        contacts.add_record(rec)
        return f"Success! {name} has been added to your contacts list."
    else:
        if contacts[name].add_phone(Phone(args[0])):
            return f"Phone {phone} has been added to {name}"
        else:
            return f"Error: Phone {phone} already exists."


@input_error
def change(name: str, old_phone: str, new_phone: str):
    if name in contacts.data:
        if contacts[name].edit_phone(old_phone, new_phone):
            return f"Phone {old_phone} for {name} has been successfully changed to {new_phone}."
        else:
            return f"Phone {old_phone} was not found."
    return f"Name was not found."


@input_error
def phone(name):
    return contacts.get_record(name)


@input_error
def delete(name, phone):
    if name not in contacts.data:
        return f"Name was not found."
    if contacts[name].del_phone(phone):
        return f"Success! {phone} has been deleted."
    else:
        return f"Phone was not found"

def main():

    func_maps = {
        "hello" : hello,
        "add" : add,
        "change" : change,
        "delete" : delete,
        "phone" : phone,
        "showall" : showall
    }

    print("Enter the first command:")
    
    while True:

        user_input = input(">>> ").lower()
        if not user_input:
            print("Error: provide a command.")
            continue

        if user_input in ["good bye", "exit", "close"]:
            print("Good bye!")
            break

        input_parts = user_input.split()
        command = input_parts[0]
        args = input_parts[1:]

        if command in func_maps:
            print(func_maps[command](*args))
        else:
            print("Command is not supported. Please choose between: hello, add, change, delete, phone or showall.")

if __name__ == "__main__":
    main()