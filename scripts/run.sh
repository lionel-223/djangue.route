#!/bin/bash

if [ "$container" == "" ]; then
	python -m venv .venv
	source .venv/bin/activate
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt
fi

pip install alembic
alembic upgrade head
flask run -h 0.0.0.0 -p ${1:-5000}
