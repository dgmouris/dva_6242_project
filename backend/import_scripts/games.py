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
