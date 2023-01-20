# Scouting App Backend
The backend app for FIRST Competition scouting.

## To-Do
- [x] Django
- [x] Vision Code
- [x] Integrate VC
- [ ] Make it pretty
- [ ] Make it epic

## Technologies
- Python (🚀 BLAZINGLY SLOW 🚀 MEMORY UNSAFE 🚀)
- OpenCV - Reading QR's
- Django - Frontend
- SQLite - DB

## Functionality
- Frontend webapp GUI
- QR code reading
- Algorithms to rank teams

## Steps
### Set Up
```bash
python3 -m venv .
source bin/activate
pip install -r requirements.txt
python manage.py migrate
```

### Run
`python manage.py runserver`

### Alternative setup using pipenv
```bash
pip install pipenv

pipenv install
pipenv run python manage.py migrate
```

### Running the server
`pipenv run python manage.py runserver`

Alternatively, you can use `pipenv shell` to active the venv and run commands from inside of it

### Formatting
We're using the [Black](https://black.readthedocs.io/en/stable/) code formatter.
After you've changed some files, make sure to run it on the files you've changed!

```bash
black <source_file_or_directory> # format file
```
