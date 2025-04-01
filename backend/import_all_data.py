from import_scripts.season import import_season
from import_scripts.games import import_games_for_season
from import_scripts.shots import import_all_shots
from import_scripts.players import import_players_for_season
from import_scripts.import_shifts import import_shifts_for_games
from import_scripts.import_poiu import import_poiu_all
from import_scripts.import_player_shift_track import import_player_shift_tracking
from import_scripts.update_game_shift_track_poiu import update_game_shift_track_poiu
from import_scripts.import_shot_poiu import import_shot_poiu
from app import app, db
from models import Season, Game, Shot, Player, POIU, ShotPOIU, get_or_create, PlayerShiftTrack, GameShiftTrack
from sqlalchemy import text, insert, update
import re

def main():
    print("Importing data to database...")
    with app.app_context():
        # with this import script just comment out the ones that fail.
        import_season(db, Season)
        import_games_for_season("2023", db, Game)

        import_all_shots(db, Shot)
        import_players_for_season("2023", db, Player)
        import_shifts_for_games(db, Game)
        import_player_shift_tracking(db, insert, Game, PlayerShiftTrack, GameShiftTrack, text) #Checks for Goalie Positions, needs to be after players loaded
        
        import_poiu_all(db, text, POIU)
        update_game_shift_track_poiu(db, text, GameShiftTrack, POIU, update)
        import_shot_poiu (db, text, Shot, POIU, insert, ShotPOIU)

    print("Importing all data succesful!")

if __name__ == "__main__":
    main()
