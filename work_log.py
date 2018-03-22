"""
An application for managing tasks that have been completed.

A user can add tasks to the work log and search through existing
tasks, all of which are stored in a CSV for persistent storage.

This file contains all of the functions to control the menu, as well
as the logic to run the menu.
"""
import datetime
import os

from task import Task
import task_search as ts


def clear():
    """
    Clears the screen for a clean menu

    Looks at OS version, making it compatible for all OS's.
    """

    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    while True:
        # Main menu input loop
        menu_input = main_menu(message).lower()
        while True:
            if menu_input in menu:
                break
            else:
                menu_input = main_menu("Selection not recognized. Try again.")

        # Runs selected function
        menu[menu_input]()

        # Quit program if selection is q
        if menu_input == 'q':
            break


def add_task():
    # Unpacks the dictionary into kwargs to create the task
    task = Task(**create_task_menu())

    # Add task to CSV
    task.add_to_csv()

    # Display results and
    # return to main menu
    clear()
    print("Task entry has been added!\n")
    print("Date: {}\nTitle: {}\nDuration: {}\nNotes: {}\n".format(
        datetime.datetime.strftime(task.date, "%d/%m/%Y"),
        task.title,
        task.duration,
        task.notes,
    ))
    input("Press Enter to return to the main menu.")


def search_task():
    # Task input loop
    if not os.path.isfile("work_log.csv"):
        clear()
        return input("No tasks have been created."
                     "Press enter to return to main menu.\n> ")
    task_input = search_task_menu().lower()
    while True:
        if task_input in ['d', 't', 'k', 'p', 'r']:

            # Run search based on user input
            tasks = ts.filter_input(task_input)

            # Restart input loop if no search results are found
            if tasks.empty:
                task_input = search_task_menu(
                    "No results were found using your criteria\n"
                    "Please try again.")
                continue
            break
        else:
            task_input = search_task_menu(
                "Selection not recognized. Try again.")
            continue

    # Display results from search
    ts.task_pages(tasks)


def quit_program():
    clear()
    print("Thanks for using the work log!\n")


def main_menu(message=None):
    """
    Runs the main menu.

    Takes one argument 'message' to allow control over a potential
    error message.  Shows a default message if none is provided.

    Returns the user selection from the main menu.
    """
    clear()
    print("WORK LOG\n========\n")
    if message:
        print(message+"\n")
    else:
        print("What would you like to do?\n")
    print("(A)dd a task")
    if os.path.isfile("work_log.csv"):
        print("(S)earch for a task")
    print("(Q)uit")
    return input("> ")


def create_task_menu():
    """
    Run the menu for task creation.

    Returns a dictionary for the task to create.
    """
    date = get_task_date()
    title = get_task_title()
    duration = get_task_duration()
    notes = get_task_notes()
    return {'date': date, 'title': title, 'duration': duration, 'notes': notes}


def get_task_date():
    """
    Prompts the user to provide a completion date for the task.

    Validates user input for proper date formatting.

    Returns a datetime object.
    """
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
    """
    Prompts the user to provide a title for the task.

    Task title cannot be empty and will prompt the user again
    if they don't enter a title.

    Returns title as a string.
    """
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
    """
    Prompts the user to enter task duration.

    Validates the duration by coercing to integer.

    Returns the duration integer object.
    """
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
    """
    Prompts the user for notes.

    Notes are optional, so hitting enter on the input is a valid
    option.

    Returns the notes string.
    """
    clear()
    return input("Enter any additional notes (optional): ")


def search_task_menu(message=None):
    """
    Runs the menu to search through tasks.

    Takes an optional 'message' argument to allow for error messages
    to be displayed.

    Returns the user input string.
    """
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


menu = {
    'a': add_task,
    's': search_task,
    'q': quit_program,
}


if __name__ == '__main__':
    # Instantiate error message
    message = None

    # Main Menu loop
    menu_loop()
