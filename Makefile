up:
	docker-compose up

down:
	docker-compose down --remove-orphans

stop:
	docker-compose stop

build:
	docker-compose build

test:
	docker-compose run app python manage.py test

migrations:
	docker-compose run app python manage.py makemigrations

migrate:
	docker-compose run app python manage.py migrate