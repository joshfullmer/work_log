import csv
import os


FILENAME = "work_log.csv"


def initialize_csv():
    csv_exists = os.path.isfile(FILENAME)
    fieldnames = ['date', 'title', 'duration', 'notes']
    if not csv_exists or os.path.getsize(FILENAME) == 0:
        with open(FILENAME, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames)
            writer.writeheader()
