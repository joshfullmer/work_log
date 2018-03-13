"""
Task class for the work log.

Initialized with:
- date
- title
- duration
- notes (optional)

Has one method:
- add_to_csv
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
        """
        Add the Task instance to CSV
        """
        # Create CSV if it doesn't exist, add headers if they don't exist
        initialize_csv()

        # Write to CSV
        with open(FILENAME, 'a', newline='') as csvfile:
            fieldnames = ['date', 'title', 'duration', 'notes']
            writer = csv.DictWriter(csvfile, fieldnames)
            row = {'date': self.date,
                   'title': self.title,
                   'duration': self.duration,
                   'notes': self.notes, }
            writer.writerow(row)
