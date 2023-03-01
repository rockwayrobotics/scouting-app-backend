run:
	@echo "Formatting code...\n"
	@black *.py
	@black **/*.py
	@echo "\nRunning server...\n"
	@pipenv run python manage.py runserver

setup:
	@echo "Installing dependencies...\n"
	@pipenv install
	@echo "\nMigrating database...\n"
	@pipenv run python manage.py migrate
