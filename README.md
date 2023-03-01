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

### Environment Variables
You'll need to create a `.env` file that contains the values for the **Django** secret keys, **The Blue Alliance** authentication key, as well as the port you want the webserver to listen on.
The `DJANGO_PORT` can be set to whatever you want, and the keys can be gotten from another code team member.
```
DJANGO_SETTINGS_KEY=<key>
TBA_AUTH=<key>
DJANGO_PORT=8000
```

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
