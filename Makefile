.PHONY: run
run:
	poetry run python ./src/main.py

.PHONY: format
format:
	poetry run isort .
	poetry run black .

.PHONY: lint
lint:
	poetry run flake8 .

.PHONY: type-check
type-check:
	poetry run mypy .

.PHONY: flt
flt:
	make format
	make lint
	make type-check

DEFAULT_GOAL: run