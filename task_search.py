"""
Provides functions to search for tasks in a CSV of tasks

Uses dataframes to search, filter, edit, and delete from the work log CSV
"""
import datetime
import pandas as pd

import work_log


def filter_input(selection):
    """
    Filters user input to the proper search function.

    Also reads the CSV, stores in Dataframe, converts the 'date' column
    to datetime format, and fills null values with empty strings.
    """
    # Read CSV to dataframe
    tasks = pd.read_csv('work_log.csv')

    # Convert date column to datetime
    tasks['date'] = pd.to_datetime(tasks['date'])

    # Fill null values with empty string
    tasks = tasks.fillna('')

    # Filter user input to proper search function
    if selection == 'd':
        return date_search(tasks)
    if selection == 't':
        return duration_search(tasks)
    if selection == 'k':
        return keyword_search(tasks)
    if selection == 'p':
        return regex_search(tasks)
    if selection == 'r':
        return date_range_search(tasks)


def date_search(tasks):
    """
    Allows user to choose from a unique list of dates that appear in the
    date column.

    Returns dataframe of tasks based on the user's chosen date.
    """
    # Sort dataframe by date for displaying dates in order to the user
    tasks.sort_values(by='date', inplace=True)

    # Get unique list of dates from the data
    dates = pd.to_datetime(tasks.date.unique())

    # Date search menu loop
    work_log.clear()
    print("Which date would you like to search on?\n")
    for i, date in enumerate(dates):
        print("({}) {}".format(i+1, date.strftime("%d/%m/%Y")))
    while True:
        index = input("> ")

        # Validates input. Must be an integer between 1 and the total
        # number of unique dates
        try:
            index = int(index)
        except ValueError:
            print("Must be a number. Try again.")
            continue
        else:
            if index < 1 or index > len(dates):
                print("Invalid selection, try again.")
                continue
            break
    return tasks[tasks['date'] == dates[index-1]]


def duration_search(tasks):
    """
    Allows the user to search through existing tasks by duration

    User must give an integer.

    Returns a dataframe of tasks that have the exact duration given.
    """
    # Duration search input loop
    work_log.clear()
    print("What duration (in minutes) would you like to search by?")
    while True:
        duration = input("> ")

        # User input must be an integer
        try:
            duration = int(duration)
        except ValueError:
            print("Whole numbers only. Try again.")
            continue
        break
    return tasks.loc[tasks['duration'] == duration]


def keyword_search(tasks):
    """
    Allows the user to search through existing tasks by a given keyword

    Returns a dataframe of tasks that contain the given keyword
    """
    # User input
    work_log.clear()
    keyword = input("What keyword would you like to search by?\n> ")

    # Instantiate the indices set for return
    indices = set()
    for column in tasks:
        # Convert column to string
        tasks[column] = tasks[column].astype(str)

        # Check if the string contains the given keyword
        results = tasks.loc[tasks[column].str.contains(keyword)]

        # Adds any results to the set of indices
        indices |= set(results.index.values)
    return tasks.iloc[list(indices)]


def regex_search(tasks):
    """
    Allows the user to search through existing tasks by a given regex pattern

    Returns a dataframe of tasks that match the given regex pattern
    """
    # User input
    work_log.clear()
    regex = input("What regex pattern would you like to search by?\n> ")

    # Instantiate the indices set for return
    indices = set()
    for column in tasks:

        # Convert column to string
        tasks[column] = tasks[column].astype(str)

        # Check if string matches the given regex pattern
        results = tasks.loc[tasks[column].str.match(regex)]

        # Adds any results to set of indices
        indices |= set(results.index.values)
    return tasks.iloc[list(indices)]


def date_range_search(tasks):
    """
    Allows user to search through existing tasks using a date range

    User input is validated on date formats

    Returns dataframe of tasks between the given date range
    """

    # Date range input loop
    work_log.clear()
    from_date = input("What is the date range you would like to search by?\n"
                      "(DD/MM/YYYY date format)\n"
                      "FROM: ")
    while True:

        # Must be date with DD/MM/YYYY format
        try:
            from_date = datetime.datetime.strptime(from_date, "%d/%m/%Y")
        except ValueError:
            work_log.clear()
            print("Couldn't convert input into date. Try again.")
            from_date = input("From when? (DD/MM/YYYY)\n> ")
            continue
        break
    to_date = input("TO: ")
    while True:

        # Must be date with DD/MM/YYYY format
        try:
            to_date = datetime.datetime.strptime(to_date, "%d/%m/%Y")
        except ValueError:
            print("Couldn't convert input into date. Try again.")
            from_date = input("To when? (DD/MM/YYYY)\n> ")
            continue
        break

    # Swap the TO and FROM dates if TO comes before FROM
    if to_date < from_date:
        to_date, from_date = from_date, to_date

    # Return dataframe of tasks in the date range
    return tasks.loc[tasks['date'].isin(pd.date_range(from_date, to_date))]


def task_pages(tasks):
    """
    Runs the task pagination menu.
    """
    # Uses an index variable to keep track of which task is being shown.
    index = 0

    # Store a message in case an error needs to be shown.
    message = "What would you like to do?"
    while True:
        task = tasks.iloc[index]
        work_log.clear()
        print("TASK\n====\n")
        print("Task #{}".format(task.name))
        print("Date: {}".format(task.date))
        print("Title: {}".format(task.title))
        print("Duration: {}".format(task.duration))
        print("Notes: {}".format(task.notes))
        print("\n{}\n".format(message))

        # Generate valid options and messaging based on current index
        if len(tasks) == 1:
            options = ['e', 'd']
            print("(E)dit, (D)elete,")
        elif index == 0:
            options = ['e', 'd', 'n']
            print("(E)dit, (D)elete, view (N)ext,")
        elif index == len(tasks) - 1:
            options = ['e', 'd', 'p']
            print("(E)dit, (D)elete, view (P)revious,")
        else:
            options = ['e', 'd', 'n', 'p']
            print("(E)dit, (D)elete, view (N)ext, view (P)revious,")
        print("Or go (B)ack.")
        options.append('b')

        # Filter user input
        choice = input("> ").lower()
        if choice not in options:
            message = "Choice not recognized. Try again."
            continue
        if choice == 'e':
            edit_task(task.name)
        if choice == 'd':
            delete_task(task.name)
        if choice == 'n':
            index += 1
            continue
        if choice == 'p':
            index -= 1
            continue
        break


def edit_task(index):
    """
    Allows user to edit an existing task located at the given index

    Updates the CSV with the edited task
    """
    # Read CSV
    # This function can't access the full list of tasks, so the full
    # file is read to memory again
    tasks = pd.read_csv('work_log.csv')

    # Set message so an error can be generated if needed
    message = "What do you want to update?"

    # Edit input loop
    while True:
        work_log.clear()
        print("{}\n".format(message))
        print("(D)ate")
        print("(T)itle")
        print("D(u)ration")
        print("(N)otes\n")
        field = input("> ").lower()
        if field not in ['d', 't', 'u', 'n']:
            message = "Choice not recognized. Try again."
            continue
        if field == 'd':
            key = 'date'
            value = work_log.get_task_date()
        if field == 't':
            key = 'title'
            value = work_log.get_task_title()
        if field == 'u':
            key = 'duration'
            value = work_log.get_task_duration()
        if field == 'n':
            key = 'notes'
            value = work_log.get_task_notes()
        break

    # Updates the tasks dataframe from given user input
    tasks.loc[index, key] = value

    # Writes updated dataframe to CSV
    tasks.to_csv('work_log.csv', index=False)
    input("Task has been updated. Press Enter to return to the main menu.")


def delete_task(index):
    """
    Allows user to delete a row from the CSV using the given index
    """
    # Read from CSV because this function can't access the original full
    # dataframe
    tasks = pd.read_csv('work_log.csv')

    # Delete row at given index
    tasks = tasks.drop(tasks.index[index])

    # Write changes to CSV
    tasks.to_csv('work_log.csv', index=False)
    input("Task has been deleted. Press Enter to return to the main menu.")
