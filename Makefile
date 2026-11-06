COV_REPORT ?= html
# uv runs every command in the project environment (.venv, synced with uv.lock); no activation needed.
# CI sets UV_LOCKED=1, so a uv.lock that is out of date with pyproject.toml fails instead of being re-resolved.
RUN ?= uv run

test:
	$(RUN) pytest .
test-cov:
	$(RUN) pytest -v -rs --cov=hangman --cov-report=$(COV_REPORT)

lint:
	$(RUN) pre-commit run --all-files

# known vulnerabilities in uv.lock (OSV-Scanner); needs the network, CI also runs it weekly
audit:
	$(RUN) pre-commit run osv-scanner --hook-stage manual --all-files

# every check; must pass before a change is done (CI runs the same targets)
check: lint test-cov

all: check

.PHONY: test test-cov lint audit check all
