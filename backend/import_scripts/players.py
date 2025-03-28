import time
import csv
from datetime import datetime

from pathlib import Path


def import_players_for_season(beginning_season_year, db, Player):
    print(F"Importing players for season {beginning_season_year}...")

    file_path = Path(__file__)
    root = file_path.parent.parent.parent.parent


    files_to_run = []

    shots_data_file0 = Path(root / "data" / "players" / "skaters.csv")
    files_to_run.append(shots_data_file0)
    shots_data_file1 = Path(root / "data" / "players" / "skaters (1).csv")
    files_to_run.append(shots_data_file1)
    shots_data_file2 = Path(root / "data" / "players" / "skaters (2).csv")
    files_to_run.append(shots_data_file2)
    shots_data_file3 = Path(root / "data" / "players" / "skaters (3).csv")
    files_to_run.append(shots_data_file3)
    shots_data_file4 = Path(root / "data" / "players" / "skaters (4).csv")
    files_to_run.append(shots_data_file4)
    shots_data_file5 = Path(root / "data" / "players" / "skaters (5).csv")
    files_to_run.append(shots_data_file5)
    shots_data_file6 = Path(root / "data" / "players" / "skaters (6).csv")
    files_to_run.append(shots_data_file6)
    shots_data_file7 = Path(root / "data" / "players" / "skaters (7).csv")
    files_to_run.append(shots_data_file7)
    shots_data_file8 = Path(root / "data" / "players" / "skaters (8).csv")
    files_to_run.append(shots_data_file8)
    shots_data_file9 = Path(root / "data" / "players" / "skaters (9).csv")
    files_to_run.append(shots_data_file9)
    shots_data_file10 = Path(root / "data" / "players" / "skaters (10).csv")
    files_to_run.append(shots_data_file10)
    shots_data_file11 = Path(root / "data" / "players" / "skaters (11).csv")
    files_to_run.append(shots_data_file11)
    shots_data_file12 = Path(root / "data" / "players" / "skaters (12).csv")
    files_to_run.append(shots_data_file12)
    shots_data_file13 = Path(root / "data" / "players" / "skaters (13).csv")
    files_to_run.append(shots_data_file13)
    shots_data_file14 = Path(root / "data" / "players" / "skaters (14).csv")
    files_to_run.append(shots_data_file14)





    all_players = []
    all_player_ids = []

    last_player_id = 0
    for fileName in files_to_run:
        with open(fileName, newline='') as csvfile:
            reader = csv.DictReader(csvfile)  # Uses the first line as column headers
            for row in reader:
                player_id = int(row["playerId"])
                position = row["position"]
                full_name = row["name"]

                player_attr = {"playerId": player_id, "position": position, "name": full_name}

                if player_id in all_player_ids:
                    continue

                # add them to the database
                player = Player(
                    id=player_id,
                    full_name=full_name,
                    position=position
                )
                all_players.append(player)
                all_player_ids.append(player_id)

    db.session.add_all(all_players)
    db.session.commit()
    print("Importing successful!")
