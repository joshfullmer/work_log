"""
Class for tasks that will be added to the work log

Need to implement:
- Date
- Title
- Time spent
- Notes
"""
import csv

from csv_tools import initialize_csv, FILENAME


class Task():
    def __init__(self, date, title, duration, notes=None):
        self.date = date
        self.title = title
        self.duration = duration
        self.notes = notes

    def add_to_csv(self):
        initialize_csv()
        with open(FILENAME, 'a', newline='') as csvfile:
            fieldnames = ['date', 'title', 'duration', 'notes']
            writer = csv.DictWriter(csvfile, fieldnames)
            row = {'date': self.date,
                   'title': self.title,
                   'duration': self.duration,
                   'notes': self.notes, }
            writer.writerow(row)
