import time
import requests
import csv
from datetime import datetime

from pathlib import Path


# we'll fix this later when we have more data by tyler.
DEFAULT_SEASON = "2023"
DEFAULT_COMPARISON_TYPE = "year"

def import_similarity(db, POIUSimilarities):
    print("Importing all Similarities...")
    file_path = Path(__file__)
    root = file_path.parent.parent.parent

    similarity_file = Path(root / "data" / "similarity" / "similarity_penalty_kill_2023.csv")

    # read all of the data and format it in the model format
    all_similarity_rows = []
    with open(similarity_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers

        for row in reader:
            model_data = map_csv_fields_to_model_data(row)
            all_similarity_rows.append(model_data)

    # committing all of the data to the database.
    try:
        db.session.bulk_insert_mappings(POIUSimilarities, all_similarity_rows)
        db.session.commit()
        print(F"Imported {len(all_similarity_rows)} similarities.")
    except Exception as error:
        print(error)
        print("Importing similarities failed.")
        db.session.rollback()


# create the mapping.
def map_csv_fields_to_model_data(row):
    csv_to_model_fields_mapping = {
        "poiu_id": "poiu_id",
        "neighbor_1" : "similar_poiu_id_one",
        "similarity_1" : "similar_poiu_id_one_score",
        "neighbor_2" : "similar_poiu_id_two",
        "similarity_2" : "similar_poiu_id_two_score",
        "neighbor_3" : "similar_poiu_id_three",
        "similarity_3" : "similar_poiu_id_three_score",
        "neighbor_4" : "similar_poiu_id_four",
        "similarity_4" : "similar_poiu_id_four_score",
        "neighbor_5" : "similar_poiu_id_five",
        "similarity_5" : "similar_poiu_id_five_score",
    }
    # add the default data
    model_data = {
        "season": DEFAULT_SEASON,
        "comparison_type": DEFAULT_COMPARISON_TYPE
    }
    for key, value in csv_to_model_fields_mapping.items():
        if key in row:
            model_data[value] = row.pop(key)
    return model_data











