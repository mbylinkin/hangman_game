test:
	pytest .
test-cov:
	pytest -v --cov=app --cov-report=html

lint:
	pre-commit run --all-files

all: lint test-cov
