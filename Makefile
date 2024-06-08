all: install check

install:
	poetry install --with dev

test:
	poetry run pytest

lint:
	poetry run mypy src
	poetry run ruff src

publish:
	poetry publish --build

check: lint test

.PHONY: check install lint publish test
