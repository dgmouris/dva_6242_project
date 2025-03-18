from import_scripts.season import import_season
from import_scripts.games import import_games_for_season
from import_scripts.shots import import_all_shots
from app import app, db
from models import Season, Game, Shot
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def main():
    print("Importing data to database...")
    with app.app_context():
        import_season(db, Season)
        import_games_for_season("2023", db, Game)
        import_all_shots(db, Shot, Game)

    print("Importing succesful!")

if __name__ == "__main__":
    main()