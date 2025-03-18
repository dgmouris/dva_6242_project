import time
import requests
import csv
from datetime import datetime

from pathlib import Path


def import_games_for_season(beginning_season_year, db, Game):
    print(F"Importing games for season {beginning_season_year}...")

    file_path = Path(__file__)
    root = file_path.parent.parent.parent

    shots_data_file = Path(root / "data" / "shots" / "shots_2023_2024.csv")

    # dictionary holding the game id and the year
    all_games = {}


    with open(shots_data_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers


        for row in reader:
            game_id = int(row["game_id"])
            beginning_year = int(row["season"])
            is_playoff_game = int(row["isPlayoffGame"])
            # breakpoint()
            end_year = beginning_year + 1
            all_year_id = int(F"{beginning_year}{end_year}")
            all_games[game_id] = {}
            all_games[game_id]["season"] = all_year_id
            all_games[game_id]["game_type"] = is_playoff_game

    all_sql_games = []

    for game_id in all_games.keys():
        season_id = all_games[game_id]["season"]
        game_type = all_games[game_id]["game_type"]

        game = Game(
            id=game_id,
            season_id=season_id,
            game_type=game_type
        )
        all_sql_games.append(
           game
        )
        try:
            db.session.add(game)
            db.session.commit()
        except Exception as error:
            print("FIX ME!")
            print(error)
            print(game_id)



    print("Successful!")








    # # starts in october
    # next_start_date = F"{beginning_season_year}-10-10"

    # BASE_GAMES_SCHEDULE_URL = "https://api-web.nhle.com/v1/schedule/"

    # response = requests.get(f"{BASE_GAMES_SCHEDULE_URL}{next_start_date}")
    # data_for_week = response.json()




    # # get each game in the week
    # game_week = data_for_week["gameWeek"]

    # all_games = []

    # for day_games in game_week:
    #     day = datetime.strptime(day_games["date"], '%Y-%m-%d').date()
    #     for game in day_games["games"]:
    #         game_id = game["id"]
    #         season_id = game["season"]
    #         game_type = game["gameType"]
    #         # create a game object
    #         all_games.append(
    #             Game(
    #                 id=game_id,
    #                 season_id=season_id,
    #                 date=day,
    #                 game_type=game_type
    #             )
    #         )

    # print(beginning_season_year)
    # print(F"Attempting to add {len(all_games)}")

    # # get the next start date and continue the loop
    # next_start_date = data_for_week["nextStartDate"]

    # db.session.add_all(all_games)
    # db.session.commit()
    # print(F"Successfully")
