.PHONY: build
build:
	python ./src/build.py

.PHONY: run
run:
	python ./src/main.py

.PHONY: lint
lint:
	isort .
	black .
	flake8 .
	mypy .

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

DEFAULT_GOAL: build
