# Team 117 DVA Project

## Demo

If you want a working [version of the demo click here](https://dva-6242-project.vercel.app/)

## Data
copy all of the [data found here](https://drive.google.com/drive/folders/1hpB9x9Pjlp3rQ6dhihEff1CPZxI6Slyc)
in a folder with the same structure as defined in the folder. Should look like below.

data/
    shots/
    players/
    lines/
    goalies/
    similarity/

## Installation

### Prereqs
- python and pip
- node.js and npm
- postgresql server running locally

### Frontend (visulization)
- create a file in the `frontend` folder called `.env` and populate that folder with:
for testing
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```
to test again production backend populate `.env` file with
```
NEXT_PUBLIC_BACKEND_URL=http://http://dva_6242_project.dgmouris.com/
```
- open a terminal or command line and install dependencies
`npm install`
- run the frontend appliation
`npm run dev`

### Similarity
- create a virtual environment locally in the root of the project
`python -m venv ./venv` and activate it.
- in the same virtual environment as above install dependencies `pip install -r requirements.txt`
- navigate to the folder `similarity` and run the file `python similarity_calc.py` which creates the similarities
- there are these files already in the data.

Note: [more info here on backend setup](similarity/README.md)

### Backend (serving the data)
- create a virtual environment locally in the root of the project (if not created in the similarity section)
`python -m venv ./venv` and activate it.
- open a terminal go into the backend folder and install the dependencies
`pip install -r requirements.txt`
- for a fresh setup run the following steps after navigating to the `backend` folder in the terminal:
  - create a file called `.env` in the folder `backend` and populate with the following:
```
DB_CONNECTION_STRING=postgresql+psycopg2://username:password@localhost:5432/databasename
```
  - run the database setup `python create_database_tables.py` (will take a really long time)
  - populate the data  `python import_all_data.py`
  - run the project locally `flask --app server.py run --debug`
- for an existing database installation (production)
  - in the `.env` file change the content to
```
DB_CONNECTION_STRING=production_url
```
  - run the project locally `flask --app server.py run --debug`

Note: [more info here on backend setup](backend/README.md)

