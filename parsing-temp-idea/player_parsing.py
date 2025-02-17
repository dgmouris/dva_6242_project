import json
import csv
from pathlib import Path
import pprint

import requests

TEST_PLAYER_ID = 8482747.0

# there's some duplication ehre here but we can figure that out later.
def get_players_file():
    cwd = Path.cwd()
    players_file_path = cwd.parent / "data" / "players" / "skaters_2023.csv"
    return players_file_path

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
def import_players_file(players_file):
    print("importing players...")

    # dictionary of players

    all_players = {}
    with open(players_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers

        for row in reader:
            # converts string numbers and all nubmers to float
            row_clean = make_rows_values_correct_type(row)

            if row_clean["playerId"] in all_players.keys():
                continue

            # remove after testing
            if row_clean["playerId"] != TEST_PLAYER_ID:
                continue

            all_players[row_clean["playerId"]] = {}

            # skip if not in test game id remove when serious
            # all_player_rows.append(row_clean)
    return all_players

def import_player_information_data(all_players):
    for player_id in all_players.keys():
        URL = F"https://api-web.nhle.com/v1/player/{int(player_id)}/landing"
        # do it all in one step
        data = requests.get(URL).json()
        # get the data we want.
        player_data = {}
        player_data["firstName"] = data["firstName"]["default"]
        player_data["lastName"] =  data["lastName"]["default"]
        player_data["position"] = data["position"]
        player_data["shoots"] = data["shootsCatches"]
        player_data["playerImageUrl"] = data["headshot"]

        # sets the object.
        all_players[player_id] = player_data

    return all_players

def write_to_game_json_file(all_players_data):
    print("writing to json file...")
    output_shot_data_file_name = F"players_data.json"
    cwd = Path.cwd()
    full_path = cwd / "outputs" / output_shot_data_file_name
    with open(full_path, 'w') as jsonfile:
        json.dump(all_players_data, jsonfile, indent=4, ensure_ascii=False)

def main():
    players_file = get_players_file()

    all_players = import_players_file(players_file)

    all_players = import_player_information_data(all_players)

    write_to_game_json_file(all_players)
    pprint.pprint(all_players)

if __name__ == "__main__":
    main()
