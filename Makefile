#!/usr/bin/make

include .env

SHELL = /bin/bash
CURRENT_UID := $(shell id -u):$(shell id -g)

export CURRENT_UID

up:
	docker-compose up -d
upb:
	docker-compose up -d --force-recreate --build
down:
	docker-compose down
sh:
	docker exec -it /nav_client /bin/bash
navlogs:
	docker logs /nav_client -f
