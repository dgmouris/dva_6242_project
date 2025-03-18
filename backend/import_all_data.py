from import_scripts.season import import_season
from app import app, db
from models import Season
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def main():
    print("Importing data to database...")
    with app.app_context():
        import_season(db, Season)

if __name__ == "__main__":
    main()