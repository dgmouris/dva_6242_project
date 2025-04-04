import time
import requests

# this needs to be called before the POIU import.
def import_shifts_for_games(db, Game):
    print("Importing shift data for season")


    games = db.session.query(Game).filter_by(shift_data=None).all()

    for index, game in enumerate(games):
        # if the shift data is not none just continue because it's filled
        external_shift_data = import_shift_data(game.get_nhl_game_id())
        if game.shift_data is not None:

            continue

        try:
            game.shift_data = external_shift_data

            db.session.add(game)
            db.session.commit()
        except Exception as error:
            print(error)

        # add two seconds to sleep to not spam
        # yes this takes long about 30 mins to complete
        time.sleep(1)

    print("Importing successful")

def convert_minute_format_to_seconds(string_time_value):
    # fix this handle none values better.
    if string_time_value is None:
        return 0.0
    minutes, seconds = string_time_value.split(':')
    total_time = float(minutes)*60 + float(seconds)
    return float(total_time)

def import_shift_data(full_game_id):
    print(F"getting the shift data from nhl.com for {full_game_id}...")
    # URL building
    # full_game_id = get_full_game_id(game_id, season)
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