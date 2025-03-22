# Backend

## Install Dependencies

1. make a virtual environment (or just install it.)

python -m venv ./venv

2. initialize the virtual environment.
venv\scripts\activate

3. install dependencies
pip install -r requirements.txt

## Initialize the database

1. Create the database in pgadmin
2. edit the .env file DB_CONNECTION_STRING=postgresql+psycopg2://username:password@localhost:5432/databasename
3. in this folder run `python create_database_tables.py`
4. in the same folder run `python import_all_data.py`
5. run test.py it should show some data.


## Needed directories

from the root of the project you should have with the data from the google drive.

data/
    shots/
    players/
    lines/

## Running the Flask Server and using it.

In the `backend` directory you need to the following in the terminal (with your virtual environemnt.)

`flask --app server.py run --debug`

Create your flask routes in `server.py`

Important note here you need to have both the frontend and the backend running at the same time for this to work properly.
