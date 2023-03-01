include .env

run:
	@echo "Formatting code...\n"
	@black *.py
	@black **/*.py
	@echo "\nRunning server...\n"
	@pipenv run python manage.py runserver ${DJANGO_PORT}

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__/
	@rm -f db.sqlite3
	@rm -f db.sqlite3-journal
	@rm -f *.log

setup:
	@echo "Installing dependencies...\n"
	@pipenv install
	@echo "\nMigrating database...\n"
	@pipenv run python manage.py migrate
