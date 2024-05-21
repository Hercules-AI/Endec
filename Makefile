.PHONY: init install-dependencies decrypt-secrets encrypt-secrets use-prod-env use-staging-env use-dev-env migrate-new run

SOURCE_DIR=.

init: decrypt-secrets install-dependencies

install-dependencies:
	poetry install

init-pre-commit:
	pre-commit install --install-hooks

use-prod-env:
	cp .env.prod .env

use-staging-env:
	cp .env.staging .env

use-dev-env:
	cp .env.dev .env

run:
	poetry run python -m app.main

isort:
	@echo "> Running isort.." && poetry run isort $(SOURCE_DIR)

black:
	@echo "> Running black.." && poetry run black $(SOURCE_DIR)

pylint:
	@echo "> Running pylint.." && poetry run pylint $(SOURCE_DIR)

autoflake:
	@echo "> Running autoflake.." && poetry run autoflake -r $(SOURCE_DIR)

isort-check:
	@echo "> Running isort (check).." && poetry run isort $(SOURCE_DIR) --check 

black-check:
	@echo "> Running black (check).." && poetry run black $(SOURCE_DIR) --check

autoflake-check:
	@echo "> Running autoflake.." && poetry run autoflake -r -c $(SOURCE_DIR)

fmt: isort black autoflake

lint: isort-check black-check autoflake-check
