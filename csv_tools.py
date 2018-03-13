"""
One function and one constant for use with managing
the work log CSV

The CSV filename can be set from the FILENAME constant.

The CSV can be created using the 'initialize_csv' function
"""
import csv
import os


FILENAME = "work_log.csv"


def initialize_csv():
    """
    Creates a CSV using the constant 'FILENAME' if it doesn't exist
    and adds headers if they don't exist
    """

    # Check if file exists
    csv_exists = os.path.isfile(FILENAME)
    fieldnames = ['date', 'title', 'duration', 'notes']

    # If file doesn't exist, or it's empty, the CSV is (re)created
    if not csv_exists or os.path.getsize(FILENAME) == 0:
        with open(FILENAME, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
