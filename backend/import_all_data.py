from import_scripts.season import import_season
from import_scripts.games import import_games_for_season
from import_scripts.shots import import_all_shots
from import_scripts.players import import_players_for_season
from import_scripts.import_shifts import import_shifts_for_games
from app import app, db
from models import Season, Game, Shot, Player
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def main():
    print("Importing data to database...")
    with app.app_context():
        # with this import script just comment out the ones that fail.
        import_season(db, Season)
        import_games_for_season("2023", db, Game)
        import_all_shots(db, Shot, Game)
        import_players_for_season("2023", db, Player)
        import_shifts_for_games(db, Game)



    print("Importing all data succesful!")

if __name__ == "__main__":
    main()