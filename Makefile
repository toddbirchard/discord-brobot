PROJECT_NAME := $(shell basename $(CURDIR))
VIRTUAL_ENVIRONMENT := $(CURDIR)/.venv

define HELP
Manage $(PROJECT_NAME). Usage:

make run        - Run $(PROJECT_NAME).
make install    - Create virtual env & install dependencies via uv.
make update     - Upgrade dependencies via uv and output requirements.txt.
make format     - Format code with Python's `Black` library.
make lint       - Check code formatting with flake8.
make clean      - Remove cached files.
endef
export HELP


.PHONY: all help run install update requirements format lint clean

all help:
	@echo "$$HELP"


.PHONY: install
install:
	uv sync && \
	echo "Installed dependencies in virtualenv \`${VIRTUAL_ENVIRONMENT}\`";


.PHONY: run
run:
	uv run python -m asgi


.PHONY: update
update:
	uv lock --upgrade && \
	uv export --format requirements-txt --no-dev --no-hashes --no-emit-project -o requirements.txt && \
	echo "Updated dependencies in \`${VIRTUAL_ENVIRONMENT}\`";


requirements: update


.PHONY: format
format:
	uv run isort --multi-line=3 . && \
	uv run black .


.PHONY: lint
lint:
	uv run flake8 . --count \
			--select=E9,F63,F7,F82 \
			--exclude .git,.github,__pycache__,.pytest_cache,.venv,logs,creds,.venv,docs,logs,.reports \
			--show-source \
			--statistics


.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name '*.log' -delete
	find . -wholename 'logs/*.json' -delete
	find . -wholename '.pytest_cache' -delete
	find . -wholename '**/.pytest_cache' -delete
	find . -wholename './logs/*.json' -delete
	find . -wholename '.webassets-cache/*' -delete
	find . -wholename './logs' -delete
