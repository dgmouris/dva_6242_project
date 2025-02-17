import json
import csv
from pathlib import Path
import pprint

import requests

# I want to test this on a single game first
TEST_GAME_ID = 20001.0
TEST_GAME_SEASON = 2023.0

# helpers
def get_full_game_id(partial_id, season):
    return f"{int(season)}0{int(partial_id)}"

# is numeric wasn't perfect.
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def convert_minute_format_to_seconds(string_time_value):
    # fix this handle none values better.
    if string_time_value is None:
        return 0.0
    minutes, seconds = string_time_value.split(':')
    total_time = float(minutes)*60 + float(seconds)
    return float(total_time)

def make_rows_values_correct_type(row):
    # row is a on object because of the dictreader here.
    # essentially just converts numbers to floats
    # and keeps the strings the same.
    for key in row.keys():
        value = row[key]
        if is_number(value):
            row[key] = float(value)

    return row

def get_shots_file_path():
    cwd = Path.cwd()
    shots_file_path = cwd.parent / "data" / "shots" / "shots_2023_2024.csv"
    return shots_file_path

# the meat of the parsing.
def import_shot_game_data(shots_file):
    print("importing shots...")

    all_shot_rows = []
    with open(shots_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers

        for row in reader:
            # converts string numbers and all nubmers to float
            row_clean = make_rows_values_correct_type(row)
            # skip if not in test game id remove when serious
            if row_clean["game_id"] != TEST_GAME_ID:
                continue


            all_shot_rows.append(row_clean)


    # get the shot data from ../data/shots/
    return all_shot_rows

# note we'll have to be carful with this to not ddos them
def import_shift_data(game_id, season):
    print("importing shifts...")
    # URL building
    full_game_id = get_full_game_id(game_id, season)
    full_url = f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={full_game_id}"

    response = requests.get(full_url)

    full_shift_data = response.json()

    # need to get the times of shifts in numbers
    # this is needed for the money puck data.
    for index, shift in enumerate(full_shift_data["data"]):
        start_time_number = convert_minute_format_to_seconds(shift["startTime"])
        end_time_number = convert_minute_format_to_seconds(shift["endTime"])
        duration_number = convert_minute_format_to_seconds(shift["duration"])

        # update the
        full_shift_data["data"][index]["startTimeNumber"] = start_time_number
        full_shift_data["data"][index]["endTimeNumber"] = end_time_number
        full_shift_data["data"][index]["durationNumber"] = duration_number


    return full_shift_data["data"]

def assign_players_on_ice_to_shots(shot_data, shift_data):
    print("assigning player shifts to shots...")
    for index, shot in enumerate(shot_data):
        # shot_time = shot["time"]
        # team_for = shot["teamCode"]
        players_for, players_against = get_players_on_ice_for_shot(shot, shift_data)

        shot_data[index]["playersOnIceFor"] = players_for
        shot_data[index]["playersOnIceAgainst"] = players_against

    return shot_data

# there's probably a better way of doing this with sets
# but if we need to process it once and then have the data then we should be good.
def get_players_on_ice_for_shot(shot, shift_data):
    players_for = []
    players_against = []
    period = shot["period"]
    shot_time = shot["time"]
    for shift in shift_data:
        # get the shot time and period
        # this goes to the next shift if they are not on the ice.
        if not (shift["startTimeNumber"] < shot_time
            and shift["endTimeNumber"] > shot_time
            and shift["period"] == period):
            continue

        if shot["teamCode"] == shift["teamAbbrev"]:
            players_for.append(shift)
        else:
            players_against.append(shift)

    return players_for, players_against

def write_to_game_json_file(game_id, season, shot_data_with_players_on_ice):
    print("writing to json file...")
    output_shot_data_file_name = F"{get_full_game_id(game_id, season)}.json"
    cwd = Path.cwd()
    full_path = cwd / "outputs" / output_shot_data_file_name
    with open(full_path, 'w') as jsonfile:
        json.dump(shot_data_with_players_on_ice, jsonfile, indent=4, ensure_ascii=False)


def main():
    shots_file = get_shots_file_path()
    # get the shots
    shot_data = import_shot_game_data(shots_file)
    # get the shift data for a given game.
    # we could save these to json files or even a json field in a db
    # to not hit these so often
    shift_data = import_shift_data(TEST_GAME_ID, TEST_GAME_SEASON)

    # assign shifts to players on ice.
    shot_data_with_players_on_ice = assign_players_on_ice_to_shots(shot_data, shift_data)

    # write the json data
    write_to_game_json_file(TEST_GAME_ID, TEST_GAME_SEASON, shot_data_with_players_on_ice)

if __name__ == "__main__":
    main()


