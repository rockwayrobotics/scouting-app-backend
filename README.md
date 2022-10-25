# Scouting App Backend
The backend app for FIRST Competition scouting.

## To-Do
- [x] Django
- [x] Vision Code
- [ ] Integrate VC
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
`python3 -m venv .`
`source bin/activate`
`pip install -r requirements.txt`
`cd frontend/`
`python manage.py migrate`

### Run
`python manage.py runserver`

### Alternative setup using pipenv
```
pip install pipenv

pipenv install
pipenv run python manage.py migrate
```
### Running the server
`pipenv run python manage.py runserver`

Alternatively, you can use `pipenv shell` to active the venv and run commands from inside of it
