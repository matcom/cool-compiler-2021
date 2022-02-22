pytest:
	docker-compose run compiler make test

compile:
	docker-compose run compiler python3 cool.py program.cl


