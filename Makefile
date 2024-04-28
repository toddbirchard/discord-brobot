PROJECT_NAME := $(shell basename $CURDIR)
VIRTUAL_ENVIRONMENT := $(CURDIR)/.venv
LOCAL_PYTHON := $(VIRTUAL_ENVIRONMENT)/bin/python3

define HELP
Manage $(PROJECT_NAME). Usage:

make run        - Run $(PROJECT_NAME).
make install    - Create virtual env, install dependencies, and run project.
make update     - Update pip dependencies via Poetry and output requirements.txt.
make format     - Format code with Python's `Black` library.
make lint       - Check code formatting with flake8.
make clean      - Remove cached files and lock files.
endef
export HELP


.PHONY: run restart deploy update format lint clean help

requirements: update
env: ./.venv/bin/activate


all help:
	@echo "$$HELP"


env: $(VIRTUAL_ENV)


$(VIRTUAL_ENV):
	if [ ! -d $(VIRTUAL_ENV) ]; then \
		echo "Creating Python virtual env in \`${VIRTUAL_ENV}\`"; \
		python3 -m venv $(VIRTUAL_ENV); \
	fi
	poetry config virtualenvs.path $(VIRTUAL_ENV)


.PHONY: run
run: env
	  $(LOCAL_PYTHON) -m asgi


.PHONY: install
install: env
	$(LOCAL_PYTHON) -m pip install --upgrade pip setuptools wheel && \
	$(LOCAL_PYTHON) -m pip install -r requirements.txt && \
	echo "Installed dependencies in virtualenv \`${VIRTUAL_ENVIRONMENT}\`";


.PHONY: update
update: env
	$(LOCAL_PYTHON) -m pip install --upgrade pip setuptools wheel && \
	poetry update --with dev && \
	poetry export -f requirements.txt --output requirements.txt --without-hashes && \
	echo Installed dependencies in \`${VIRTUAL_ENV}\`;


.PHONY: format
format: env
	$(LOCAL_PYTHON) -m isort --multi-line=3 . && \
	$(LOCAL_PYTHON) -m black .


.PHONY: lint
lint: env
	$(LOCAL_PYTHON) -m flake8 . --count \
			--select=E9,F63,F7,F82 \
			--exclude .git,.github,__pycache__,.pytest_cache,.venv,logs,creds,.venv,docs,logs,.reports \
			--show-source \
			--statistics

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name 'poetry.lock' -delete
	find . -name 'Pipefile.lock' -delete
	find . -name '*.log' -delete
	find . -wholename 'logs/*.json' -delete
	find . -wholename '.pytest_cache' -delete
	find . -wholename '**/.pytest_cache' -delete
	find . -wholename './logs/*.json' -delete
	find . -wholename '.webassets-cache/*' -delete
	find . -wholename './logs' -delete