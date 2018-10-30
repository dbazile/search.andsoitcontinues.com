#!/bin/bash

set -e

cd $(dirname $(dirname $0))  # Return to project root

if [[ "$PORT" == "" ]]; then
	PORT=5000
fi

if [[ ! -d venv ]]; then
	echo 'creating virtual environment...'
	python3 -m venv venv
	(. venv/bin/activate && pip install -r requirements.txt)
fi

. venv/bin/activate

export REPO_URL=~/src/bazile.org

gunicorn search.server:app \
	--bind localhost:$PORT \
	--reload
