"""
Manage the menu-ing of the work log
"""
import datetime
import os

from task import Task


def clear():
    """
    Clears the screen for a clean menu

    Looks at OS version, making it compatible for all OS's.
    """

    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu(message=None):
    clear()
    print("WORK LOG\n========\n")
    if message:
        print(message+"\n")
    else:
        print("What would you like to do?\n")
    print("(A)dd a task")
    print("(S)earch for a task")
    print("(Q)uit")
    return input("> ")


def create_task_menu():
    date = get_task_date()
    title = get_task_title()
    duration = get_task_duration()
    notes = get_task_notes()
    return {'date': date, 'title': title, 'duration': duration, 'notes': notes}


def get_task_date():
    clear()
    date_string = input("When was this task completed? (DD/MM/YYYY)\n> ")
    while True:
        try:
            date = datetime.datetime.strptime(date_string, "%d/%m/%Y")
        except ValueError:
            clear()
            print("Couldn't convert input into date. Try again.")
            date_string = input(
                "When was this task completed? (DD/MM/YYYY)\n> ")
            continue
        else:
            return date


def get_task_title():
    clear()
    title = input("Enter a short description of the task.\n> ")
    while True:
        if not title:
            clear()
            print("Task title is required")
            title = input("Provide a task title.\n> ")
            continue
        else:
            return title


def get_task_duration():
    clear()
    duration = input("Enter the duration of the task in minutes.\n> ")
    while True:
        try:
            duration = int(duration)
        except ValueError:
            clear()
            print("Please enter the duration in whole minutes, no decimals.")
            duration = input("Enter the duration of the task in minutes.\n> ")
            continue
        else:
            return duration


def get_task_notes():
    clear()
    return input("Enter any additional notes (optional): ")

if __name__ == '__main__':
    message = None
    while True:
        menu_input = main_menu(message)
        while True:
            if menu_input.lower() in ['a', 's', 'q']:
                break
            else:
                menu_input = main_menu("Selection not recognized. Try again.")

        if menu_input.lower() == 'a':
            task = Task(**create_task_menu())
            task.add_to_csv()
            clear()
            print("Task entry has been added!")
            print("Date: {}\nTitle: {}\nDuration: {}\nNotes: {}".format(
                datetime.datetime.strftime(task.date, "%d/%m/%Y"),
                task.title,
                task.duration,
                task.notes,
            ))
            input("Press Enter to return to the main menu.")

        if menu_input.lower() == 's':
            message = "Not implemented yet.  Try something else."
            continue

        if menu_input.lower() == 'q':
            clear()
            print("Thanks for using the work log!\n")
            break
