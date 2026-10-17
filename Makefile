test:
	pytest .
test-cov:
	pytest -v --cov=hangman --cov-report=html

lint:
	pre-commit run --all-files

all: lint test-cov
