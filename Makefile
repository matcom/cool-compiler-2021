pytest:
	docker-compose run compiler make test

compile:
	docker-compose run compiler python3 cool.py program.cl
exec:
	docker-compose run compiler bash -c "python3 cool.py program.cl && spim output.out result.s && cat result.s"

spim:
	docker-compose run compiler spim

