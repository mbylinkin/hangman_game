COV_REPORT ?= html

test:
	pytest .
test-cov:
	pytest -v -rs --cov=hangman --cov-report=$(COV_REPORT)

lint:
	pre-commit run --all-files

# every check; must pass before a change is done (CI runs the same targets)
check: lint test-cov

all: check

.PHONY: test test-cov lint check all
