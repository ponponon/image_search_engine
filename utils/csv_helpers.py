from pathlib import Path
import csv


def csv_append(filename: Path, row: list[str]):
    with open(filename, 'a+', newline="") as csv_file:
        csv_appender = csv.writer(csv_file)
        csv_appender.writerow(row)
