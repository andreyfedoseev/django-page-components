all:
	docker-compose build

shell:
	docker-compose run --rm app /bin/bash

test:
	docker-compose run --rm app tox

upload:
	python3 setup.py sdist upload

check-flake8:
	docker-compose run --rm app flake8 ./src ./tests

check-black:
	docker-compose run --rm app black --check ./src ./tests

apply-black:
	docker-compose run --rm app black ./src ./tests

check-isort:
	docker-compose run --rm app isort --check ./src ./tests

apply-isort:
	docker-compose run --rm app isort ./src ./tests
