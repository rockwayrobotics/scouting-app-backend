run:
	pipenv run python manage.py runserver

setup:
	pipenv install
	pipenv run python manage.py migrate
