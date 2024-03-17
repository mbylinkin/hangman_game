test:
	pytest .
test-cov:
	pytest -v --cov=. --cov-report=html

all: test test-cov
