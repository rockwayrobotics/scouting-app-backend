include .env

run: format scss runserver

setup: clean install migrate TBA admin

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__/
	@rm -f db.sqlite3
	@rm -f db.sqlite3-journal
	@rm -f *.log
	@rm -rf static/

install:
	@echo "Installing dependencies...\n"
	@pipenv install

migrate:
	@echo "\nMigrating database...\n"
	@pipenv run python manage.py migrate

TBA: db.sqlite3
	@echo "\nFetching TBA data...\n"
	@pipenv run python manage.py setupEvent

admin:
	@echo "\nCreating Admin superuser...\n"
	@pipenv run python manage.py createsuperuser

format:
	@echo "Formatting code...\n"
	@pipenv run black *.py
	@pipenv run black **/*.py

scss:
	@echo "\nGenerating SCSS...\n"
	@pipenv run python manage.py collectstatic --no-input


runserver:
	@echo "\nRunning server...\n"
	@pipenv run python manage.py runserver ${DJANGO_PORT}
	@exit
