from import_scripts.season import import_season
from import_scripts.games import import_games_for_season
from app import app, db
from models import Season, Game
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def main():
    print("Importing data to database...")
    with app.app_context():
        import_season(db, Season)
        import_games_for_season("2023", db, Game)
    print("Importing succesful!")

if __name__ == "__main__":
    main()