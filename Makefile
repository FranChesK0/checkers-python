.PHONY: build
build:
	python ./src/build.py

.PHONY: run
run:
	python ./src/main.py

.PHONY: format
format:
	isort .
	black .

.PHONY: lint
lint:
	flake8 .

.PHONY: type-check
type-check:
	mypy .

.PHONY: flt
flt:
	make format
	make lint
	make type-check

DEFAULT_GOAL: build