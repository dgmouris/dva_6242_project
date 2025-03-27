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
def import_shot_game_data(season, shots_file):
    print("parsing shots...")

    all_shot_rows = []
    with open(shots_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers

        for row in reader:
            # converts string numbers and all nubmers to float
            row_clean = make_rows_values_correct_type(row)
            # skip if not in test game id remove when serious
            if int(row["season"]) == season:
                all_shot_rows.append(row_clean)

    return all_shot_rows


def import_all_shots(db, Shot):
    print("Importing all Shots...")
    file_path = Path(__file__)
    root = file_path.parent.parent.parent.parent

    season = 2007
    shots_data_file = Path(root / "data" / "shots" / "shots_2007-2023.csv")

    #for season in seasons_to_evaluate:
    while season < 2024:
        print('Importing ' + str(season))
        all_shot_rows = import_shot_game_data(season, shots_file=shots_data_file)

        shot_objects = []

        print(F"Importing {len(all_shot_rows)} shots.")
        for index, row in enumerate(all_shot_rows):
            if row['goalieIdForShot'] == '':
                row['goalieIdForShot'] = -1.0
            shot_objects.append(Shot(**row))
            
        try:
            db.session.bulk_save_objects(shot_objects)
            db.session.commit()
        except Exception as error:
            print("FIX ME")
            print(error)
            print(row)

        season = season + 1

    print("Importing Shots Successful!")
