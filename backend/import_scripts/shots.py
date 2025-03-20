import time
import requests
import csv
from datetime import datetime

from pathlib import Path

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def make_rows_values_correct_type(row):
    # row is a on object because of the dictreader here.
    # essentially just converts numbers to floats
    # and keeps the strings the same.
    for key in row.keys():
        value = row[key]
        if is_number(value):
            row[key] = float(value)
    return row

# create an object of player ids.
def import_shot_game_data(shots_file):
    print("importing shots...")

    all_shot_rows = []
    with open(shots_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers

        for row in reader:
            # converts string numbers and all nubmers to float
            row_clean = make_rows_values_correct_type(row)
            # skip if not in test game id remove when serious



            all_shot_rows.append(row_clean)

    return all_shot_rows

def import_all_shots(db, Shot, Game):
    print("Importing all Shots...")
    file_path = Path(__file__)
    root = file_path.parent.parent.parent

    shots_data_file = Path(root / "data" / "shots" / "shots_2023_2024.csv")

    all_shot_rows = import_shot_game_data(shots_file=shots_data_file)

    print(F"Importing {len(all_shot_rows)} shots.")
    for index, row in enumerate(all_shot_rows):
        if index % 10000 == 0:
            print(F"imported {index} shots.")
        try:
            # Check if the shot already exists in the database
            existing_shot = db.session.query(Shot).filter_by(id=row["id"]).first()
            if existing_shot:
                #print(f"Shot with id {row['id']} already exists. Skipping...")
                continue

            shot = Shot(**row)
            db.session.add(shot)
            db.session.commit()
        except Exception as error:
            db.session.rollback()  # Rollback the transaction in case of an error
            print("Error occurred while adding shot:")
            print(error)
            print(row)

    print("Importing Shots Successful!")
