import time
import csv
from datetime import datetime

from pathlib import Path


def import_players_for_season(beginning_season_year, db, Player):
    print(F"Importing players for season {beginning_season_year}...")

    file_path = Path(__file__)
    root = file_path.parent.parent.parent

    shots_data_file = Path(root / "data" / "players" / F"skaters_{beginning_season_year}.csv")

    all_players = []

    last_player_id = 0
    with open(shots_data_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers
        for row in reader:
            player_id = int(row["playerId"])
            position = row["position"]
            full_name = row["name"]
            # skip over players that are already added
            if player_id == last_player_id:
                continue
            last_player_id = player_id

            # add them to the database
            player = Player(
                id=player_id,
                full_name=full_name,
                position=position
            )
            all_players.append(player)

    db.session.add_all(all_players)
    db.session.commit()
    print("Importing successful!")
