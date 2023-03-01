# Scouting App Backend
The backend app for FIRST Competition scouting.

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
### Makefile
```bash
make setup # install dependencies & migrate DB
make run # run the server
```

### Manually
```bash
pip install pipenv # install pipenv

pipenv install # install dependencies
pipenv run python manage.py migrate # migrate DB

pipenv run python manage.py runserver # run server
```

Alternatively, you can use `pipenv shell` to active the venv and run commands from inside of it
