"""
Manage the menu-ing of the work log
"""
import datetime
import os

import pandas as pd

from task import Task
import task_search as ts


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


def search_task_menu(message=None):
    clear()
    if not message:
        message = "Enter criteria below:"
    print("What criteria would you like to use for searching?\n")
    print("Search by (D)ate")
    print("Search by Dura(t)ion")
    print("Search by (K)eyword")
    print("Search by Regex (p)attern")
    print("Search by Date (R)ange")
    print("\n{}\n".format(message))
    return input("> ")


if __name__ == '__main__':
    message = None
    while True:
        menu_input = main_menu(message).lower()
        while True:
            if menu_input in ['a', 's', 'q']:
                break
            else:
                menu_input = main_menu("Selection not recognized. Try again.")

        if menu_input == 'a':
            task = Task(**create_task_menu())
            task.add_to_csv()
            clear()
            print("Task entry has been added!\n")
            print("Date: {}\nTitle: {}\nDuration: {}\nNotes: {}\n".format(
                datetime.datetime.strftime(task.date, "%d/%m/%Y"),
                task.title,
                task.duration,
                task.notes,
            ))
            input("Press Enter to return to the main menu.")

        if menu_input == 's':
            task_input = search_task_menu().lower()
            while True:
                if task_input in ['d', 't', 'k', 'p', 'r']:
                    break
                else:
                    task_input = search_task_menu(
                        "Selection not recognized. Try again.")
            tasks = ts.filter_input(task_input)
            ts.task_pages(tasks)
            continue

        if menu_input == 'q':
            clear()
            print("Thanks for using the work log!\n")
            break
