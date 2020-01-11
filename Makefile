#!/usr/bin/make

include .env

SHELL = /bin/sh
CURRENT_UID := $(shell id -u):$(shell id -g)

export CURRENT_UID

up:
	docker-compose up -d
upb:
	docker-compose up -d --force-recreate --build
down:
	docker-compose down
sh:
	docker exec -it /django /bin/sh
migrations:
	docker exec -it /django python3 manage.py makemigrations
su:
	docker exec -it /django python3 manage.py createsuperuser
dump:
	docker exec -it /django python3 manage.py dumpdata -o $(filter-out $@,$(MAKECMDGOALS))
load:
	docker exec -it /django python3 manage.py loaddata $(filter-out $@,$(MAKECMDGOALS))
%:
	@:
