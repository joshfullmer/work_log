"""
Provides functions to search for tasks in a CSV of tasks

Is passed a list of dicts???
"""
import pandas as pd

import work_log


def filter_input(selection):
    tasks = pd.read_csv('work_log.csv')
    tasks['date'] = pd.to_datetime(tasks['date'])
    tasks = tasks.fillna('')
    # print(tasks)
    if selection == 'd':
        return date_search(tasks)
    if selection == 't':
        return duration_search(tasks)
    if selection == 'k':
        raise NotImplementedError
    if selection == 'p':
        raise NotImplementedError
    if selection == 'r':
        raise NotImplementedError


def date_search(tasks):
    tasks.sort_values(by='date', inplace=True)
    dates = pd.to_datetime(tasks.date.unique())

    work_log.clear()
    print("Which date would you like to search on?\n")
    for i, date in enumerate(dates):
        print("({}) {}".format(i+1, date.strftime("%d/%m/%Y")))
    while True:
        index = input("> ")
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
    work_log.clear()
    print("What duration (in minutes) would you like to search by?")
    while True:
        duration = input("> ")
        try:
            duration = int(duration)
        except ValueError:
            print("Whole numbers only. Try again.")
            continue
        break
    return tasks.loc[tasks['duration'] == duration]


def task_pages(tasks):
    index = 0
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
    tasks = pd.read_csv('work_log.csv')
    task = {}
    message = "What do you want to update?"
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
            key = 'note'
            value = work_log.get_task_notes()
        break
    tasks.loc[index, key] = value
    tasks.to_csv('work_log.csv', index=False)
    input("Task has been updated. Press Enter to return to the main menu.")


def delete_task(index):
    tasks = pd.read_csv('work_log.csv')
    tasks = tasks.drop(tasks.index[index])
    tasks.to_csv('work_log.csv', index=False)
    input("Task has been deleted. Press Enter to return to the main menu.")
